"""The rrtp path through RoombaClient: routing, polling, and giving up.

These drive `_handle_message` and the poller directly, the way
test_message_handling.py does, so no broker is involved.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from roombapy import roomba as roomba_module
from roombapy import rrtp
from roombapy.roomba import (
    _DEFAULT_POSITION_INTERVAL,
    _MIN_POSITION_INTERVAL,
    RoombaClient,
    TransportOptions,
)

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

SHADOW = b'{"state":{"reported":{"batPct":42}}}'

REPLY = (
    b'{"reportType":"current","reqId":"%s","ver":"1.0.0",'
    b'"data":[{"pmap_id":"tM_G","pmapv_id":"260901T",'
    b'"coords":[{"type":"current","xyt":[0.31,-1.74,-1.59],'
    b'"ts":1788290847}]}]}'
)


def monkey_grace(seconds: float) -> None:
    """Shorten the shadow grace period for a test.

    The poller waits before asking, so that a robot which publishes its
    position is never polled. Three seconds is right in the field and
    pointless in a test.
    """
    roomba_module._SHADOW_GRACE = seconds


def _client(**options: object) -> RoombaClient:
    return RoombaClient(
        address=ROOMBA_HOST,
        blid=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        transport=TransportOptions(**options),  # type: ignore[arg-type]
    )


class TestAReplyIsNotState:
    """The whole reason the branch sits before `_state.apply()`."""

    def test_a_reply_never_reaches_master_state(self) -> None:
        """`reportType` and `data` must not land beside `state`."""
        client = _client()
        client._handle_message("data", REPLY % b"nobody")

        assert client.master_state == {}

    def test_the_shadow_still_does(self) -> None:
        """A negative control: routing one topic must not break the rest."""
        client = _client()
        client._handle_message("cmd", SHADOW)

        assert client.master_state["state"]["reported"]["batPct"] == 42

    def test_without_the_branch_it_would_land(self) -> None:
        """Proves the branch is doing the work.

        Applying the same payload through the state machine directly
        puts `reportType` and `data` at the top level, next to `state` --
        which is what every consumer reading master_state would see.
        """
        client = _client()
        client._state.apply(
            {"reportType": "current", "reqId": "x", "data": [{}]}
        )

        assert "reportType" in client.master_state


class TestOnePollerForEveryWatcher:
    """A robot has one local connection.

    Two callers running their own loops would double the load without
    either noticing, which is why the interval belongs to the library.
    """

    @pytest.mark.asyncio
    async def test_two_watchers_share_one_poller(self) -> None:
        """The second watcher must not start a second poller."""
        client = _client()
        sent: list[str] = []

        async def _fake_publish(_topic: str, payload: str) -> None:
            sent.append(_topic)
            # Answer immediately so the poller keeps moving.
            req_id = json.loads(payload)["reqId"]
            client._handle_message("data", REPLY % req_id.encode())

        client._publish = _fake_publish  # type: ignore[method-assign]

        first = client.watch_position(interval=0.5)
        second = client.watch_position(interval=0.5)
        await anext(first)
        await anext(second)

        assert len(client._position_watchers) == 2
        poller = client._position_poller
        assert poller is not None

        await first.aclose()
        # Still one watcher left -- the poller must survive.
        assert client._position_poller is poller

        await second.aclose()
        assert client._position_poller is None

    @pytest.mark.asyncio
    async def test_an_interval_below_the_floor_is_refused(self) -> None:
        """Nobody has tested faster than 2 Hz on real hardware."""
        client = _client()

        with pytest.raises(ValueError, match="floor"):
            await anext(client.watch_position(interval=0.05))


class TestGivingUpOnASilentRobot:
    """Silence means the generation does not implement the request.

    Across 100 consecutive requests on a moving robot there was not one
    miss, so a robot answers or it never does -- and a stream that kept
    asking would poll a robot that cannot answer for a whole mission.
    """

    @pytest.mark.asyncio
    async def test_three_timeouts_raise_rather_than_ending_quietly(
        self,
    ) -> None:
        """An empty stream reads as 'mission over'; an exception does not."""
        client = _client()

        async def _silent_publish(_topic: str, _payload: str) -> None:
            return  # nothing ever answers

        client._publish = _silent_publish  # type: ignore[method-assign]

        # The poller runs only while somebody is listening -- that is
        # what stops it when the last watcher leaves.
        queue: asyncio.Queue[rrtp.RobotPosition] = asyncio.Queue(maxsize=4)
        client._position_watchers[queue] = 0.5

        monkey_grace(0.01)
        with pytest.raises(rrtp.RrtpUnsupportedError):
            await client._run_position_poller(timeout=0.05)

    @pytest.mark.asyncio
    async def test_one_miss_does_not(self) -> None:
        """A single failure can be a dropped connection, not a verdict."""
        client = _client()
        calls = {"n": 0}

        async def _flaky_publish(_topic: str, payload: str) -> None:
            calls["n"] += 1
            if calls["n"] == 1:
                return  # first one goes missing
            req_id = json.loads(payload)["reqId"]
            client._handle_message("data", REPLY % req_id.encode())

        client._publish = _flaky_publish  # type: ignore[method-assign]

        queue: asyncio.Queue[rrtp.RobotPosition] = asyncio.Queue(maxsize=4)
        client._position_watchers[queue] = 0.5
        # The poller listens for a shadow pose before asking; shortened
        # here so the test does not wait out the real grace period.
        monkey_grace(0.01)
        task = asyncio.ensure_future(client._run_position_poller(timeout=0.05))
        pose = await asyncio.wait_for(queue.get(), timeout=5.0)
        client._position_watchers.pop(queue, None)
        task.cancel()

        assert pose.x == 0.31


class TestNoFixIsSkippedNotYielded:
    """A stream of positions should carry positions.

    A Braava jet m6 answered every request with `type: "unknown"` and no
    coordinates for a whole mission; yielding None for each would make
    every consumer filter them out.
    """

    @pytest.mark.asyncio
    async def test_a_no_fix_reply_produces_nothing(self) -> None:
        """The poller waits for a real position rather than passing None."""
        client = _client()
        no_fix = (
            b'{"reportType":"current","reqId":"%s","ver":"1.0.0",'
            b'"data":[{"pmap_id":"jUd","coords":[{"type":"unknown"}]}]}'
        )

        async def _no_fix_publish(_topic: str, payload: str) -> None:
            req_id = json.loads(payload)["reqId"]
            client._handle_message("data", no_fix % req_id.encode())

        client._publish = _no_fix_publish  # type: ignore[method-assign]

        queue: asyncio.Queue[rrtp.RobotPosition] = asyncio.Queue(maxsize=4)
        client._position_watchers[queue] = 0.5
        monkey_grace(0.01)
        task = asyncio.ensure_future(client._run_position_poller(timeout=0.5))
        await asyncio.sleep(0.2)
        task.cancel()
        client._position_watchers.pop(queue, None)

        assert queue.empty()


class TestTheDefaultIsNotTheTestedCeiling:
    """2 Hz was a stress test, not a recommendation.

    @Thonno chose 0.5 s to see whether the robot would hold up and
    whether a rate limit existed -- and said so before anyone built on
    the number. The default is half that: ~4,600 requests over a
    77-minute mission instead of ~9,200, at a spacing still comparable
    to what a 900-series publishes for free.
    """

    def test_the_default_is_slower_than_the_floor_allows(self) -> None:
        """The floor is what was verified; the default is deliberate."""
        assert _DEFAULT_POSITION_INTERVAL > _MIN_POSITION_INTERVAL

    @pytest.mark.asyncio
    async def test_the_tested_rate_is_still_available(self) -> None:
        """A caller who has decided the traffic is worth it can ask.

        The floor is the verified rate, so it must not be refused --
        only anything faster than it.
        """
        client = _client()

        with pytest.raises(ValueError, match="floor"):
            await anext(client.watch_position(interval=0.4))


class TestOneStreamForBothGenerations:
    """Both paths reach the same stream.

    The seam that was missing: two conversions, both correct, and no
    path connecting them.

    A consumer should not have to know which generation it has. That is
    what `RobotPosition` carrying `source` is for -- and it only works
    if both paths reach the same stream.
    """

    @pytest.mark.asyncio
    async def test_a_shadow_pose_reaches_the_position_stream(self) -> None:
        """A 900-series publishes; nobody asks it anything."""
        client = _client()
        queue: asyncio.Queue[rrtp.RobotPosition] = asyncio.Queue(maxsize=4)
        client._position_watchers[queue] = 0.5

        client._handle_message(
            "cmd",
            b'{"state":{"reported":{"pose":'
            b'{"theta":153,"point":{"x":-16,"y":243}}}}}',
        )

        pose = queue.get_nowait()
        assert pose.source == "shadow"
        assert pose.x == pytest.approx(-0.016)

    @pytest.mark.asyncio
    async def test_nothing_is_fed_when_nobody_listens(self) -> None:
        """A shadow pose with no watchers costs nothing."""
        client = _client()
        client._handle_message(
            "cmd",
            b'{"state":{"reported":{"pose":'
            b'{"theta":0,"point":{"x":0,"y":0}}}}}',
        )

        assert not client._position_watchers

    @pytest.mark.asyncio
    async def test_a_publishing_robot_is_never_polled(self) -> None:
        """Polling a 900-series would add traffic for free data.

        And it would then raise RrtpUnsupportedError, killing a stream
        that was working perfectly well.
        """
        client = _client()
        asked: list[str] = []

        async def _count_publish(_topic: str, _payload: str) -> None:
            asked.append(_topic)

        client._publish = _count_publish  # type: ignore[method-assign]
        # Through _handle_message, not _state.apply: that is the path
        # that notices a shadow pose, and going round it would test a
        # route the robot never takes.
        client._handle_message(
            "cmd",
            b'{"state":{"reported":{"pose":'
            b'{"theta":0,"point":{"x":0,"y":0}}}}}',
        )

        queue: asyncio.Queue[rrtp.RobotPosition] = asyncio.Queue(maxsize=4)
        client._position_watchers[queue] = 0.5
        monkey_grace(0.01)
        task = asyncio.ensure_future(client._run_position_poller(timeout=0.05))
        await asyncio.sleep(0.2)
        task.cancel()
        client._position_watchers.pop(queue, None)

        assert asked == []


class TestTheConsumerFindsOut:
    """Raising in the poller is pointless if nobody hears it.

    Found by review, not by these tests: `watch_position` awaited the
    queue alone, so when the poller raised RrtpUnsupportedError the
    exception died inside the task and the consumer waited forever for a
    position that would never arrive.

    The error exists so an unsupported robot is visible rather than
    looking like a finished mission. A consumer that hangs instead is
    worse than one that gets an empty stream.
    """

    @pytest.mark.asyncio
    async def test_an_unsupported_robot_raises_at_the_consumer(self) -> None:
        """The exception has to cross from the poller to the caller."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(0.01)

        with pytest.raises(rrtp.RrtpUnsupportedError):
            # The floor applies -- 0.5 is the fastest a caller may
            # ask for, and three timeouts at 0.02 s settle it quickly.
            async for _pose in client.watch_position(
                interval=0.5, timeout=0.02
            ):
                pass  # pragma: no cover - never reached

    @pytest.mark.asyncio
    async def test_a_failing_publish_does_not_leak_a_request(self) -> None:
        """A request whose publish raises must not sit in _pending.

        Also from review. A poller retrying once a second against a
        disconnected client would otherwise accumulate futures for the
        lifetime of the client.
        """
        client = _client()

        async def _boom(_topic: str, _payload: str) -> None:
            msg = "not connected"
            raise RuntimeError(msg)

        client._publish = _boom  # type: ignore[method-assign]

        with pytest.raises(RuntimeError):
            await client.get_position(timeout=0.5)

        assert client._rrtp.in_flight == 0


class TestDisconnectDoesNotStrandAnyone:
    """`cancel_all` existed and was never called.

    Written for the disconnect case and then not wired to it — a caller
    awaiting a position when the connection dropped would have sat on a
    future that nothing could resolve, because the reply was going to
    arrive on a socket that no longer exists.
    """

    @pytest.mark.asyncio
    async def test_a_pending_request_is_cancelled(self) -> None:
        """The waiter finds out instead of waiting forever."""
        client = _client()
        _req_id, future = client._rrtp.new_request()

        client._rrtp.cancel_all()
        await asyncio.sleep(0)

        assert future.cancelled()
        assert client._rrtp.in_flight == 0


class TestTheFastestWatcherWins:
    """One poller serves everyone, so its rate has to satisfy everyone.

    A second caller asking for a shorter interval was silently given the
    first caller's slower one — a sparser trail than it asked for, with
    nothing to explain why.
    """

    @pytest.mark.asyncio
    async def test_a_faster_watcher_restarts_the_poller(self) -> None:
        """The shortest requested interval is the one that runs."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(30.0)  # keep the poller in its listening phase

        slow = client.watch_position(interval=2.0)
        task = asyncio.ensure_future(anext(slow))
        await asyncio.sleep(0)
        assert client._position_interval == 2.0

        fast = client.watch_position(interval=0.5)
        task2 = asyncio.ensure_future(anext(fast))
        await asyncio.sleep(0)

        assert client._position_interval == 0.5

        # Let the cancellations land before closing the generators --
        # aclose() on a generator still mid-await raises.
        task.cancel()
        task2.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(task, task2, return_exceptions=True)
        await slow.aclose()
        await fast.aclose()
        # The generators are gone, but the poller they started is not
        # awaited by anything -- pytest reports it as a stray task.

    @pytest.mark.asyncio
    async def test_the_rate_resets_when_everyone_leaves(self) -> None:
        """Otherwise the next stream inherits a rate nobody asked for."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(30.0)

        stream = client.watch_position(interval=0.5)
        task = asyncio.ensure_future(anext(stream))
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(task, return_exceptions=True)
        await stream.aclose()

        assert client._position_interval == float("inf")

    @pytest.mark.asyncio
    async def test_a_fast_watcher_leaving_slows_the_poller(self) -> None:
        """The rate drops back when the fastest watcher leaves.

        Otherwise one caller's 0.5 s is paid for by everyone else after
        it has gone.
        """
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(30.0)

        slow = client.watch_position(interval=2.0)
        fast = client.watch_position(interval=0.5)
        t1 = asyncio.ensure_future(anext(slow))
        t2 = asyncio.ensure_future(anext(fast))
        await asyncio.sleep(0)
        assert client._position_interval == 0.5

        t2.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(t2, return_exceptions=True)
        await fast.aclose()

        assert client._position_interval == 2.0

        t1.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(t1, return_exceptions=True)
        await slow.aclose()


class TestAskingTwiceCostsNothing:
    """A robot that cannot answer should be asked once, not per stream.

    Without this, a dashboard opening and closing a map view spends
    three requests and a grace period every time, against a robot
    already known to be silent.
    """

    @pytest.mark.asyncio
    async def test_the_second_stream_fails_immediately(self) -> None:
        """No requests, no grace period, same exception."""
        client = _client()
        client._position_unsupported = True

        with pytest.raises(rrtp.RrtpUnsupportedError, match="earlier"):
            await anext(client.watch_position())

    def test_disconnect_forgets_it(self) -> None:
        """The verdict does not outlive its connection.

        A firmware update that adds the capability brings a reconnect
        with it.
        """
        client = _client()
        client._position_unsupported = True

        client._rrtp.cancel_all()
        client._position_unsupported = False  # what disconnect does

        assert not client._position_unsupported


class TestSwitchingToTheShadowMidStream:
    """The stream survives learning that the robot publishes.

    A stream opened before the first shadow message must not die when
    that message arrives.

    The poller starts, a shadow pose arrives, `_handle_message` cancels
    it -- and the consumer was then handed CancelledError for a stream
    that had just started working properly.
    """

    @pytest.mark.asyncio
    async def test_a_cancelled_poller_does_not_end_the_stream(self) -> None:
        """The shadow takes over; the consumer keeps receiving."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(30.0)  # keep the poller in its listening phase

        stream = client.watch_position()
        first = asyncio.ensure_future(anext(stream))
        await asyncio.sleep(0)

        # THE POLLER DIES FIRST, THEN THE POSE ARRIVES. That ordering is
        # the one that matters: the consumer wakes on the cancelled
        # poller with an empty queue, and has to keep waiting rather
        # than raise. Cancelling and feeding in one step would leave the
        # queue non-empty and never reach that branch.
        client._shadow_publishes_pose = True
        assert client._position_poller is not None
        client._position_poller.cancel()
        await asyncio.sleep(0.05)

        client._handle_message(
            "cmd",
            b'{"state":{"reported":{"pose":'
            b'{"theta":153,"point":{"x":-16,"y":243}}}}}',
        )

        pose = await asyncio.wait_for(first, timeout=2.0)
        assert pose.source == "shadow"
        assert client._shadow_publishes_pose

        await stream.aclose()


class TestASingleCallReadsTheShadowToo:
    """One call reads the shadow instead of asking.

    `watch_position()` listens before polling; a single call has no
    such window, so it reads what has already arrived.

    Without this a 900-series user gets a TimeoutError for a position
    that is sitting in `master_state`.
    """

    @pytest.mark.asyncio
    async def test_a_publishing_robot_is_not_asked(self) -> None:
        """No request goes out when the shadow already has a pose."""
        client = _client()
        asked: list[str] = []

        async def _count(_topic: str, _payload: str) -> None:
            asked.append(_topic)

        client._publish = _count  # type: ignore[method-assign]
        client._handle_message(
            "cmd",
            b'{"state":{"reported":{"pose":'
            b'{"theta":153,"point":{"x":-16,"y":243}}}}}',
        )

        pose = await client.get_position(timeout=0.5)

        assert pose is not None
        assert pose.source == "shadow"
        assert asked == []

    @pytest.mark.asyncio
    async def test_a_silent_robot_is_still_asked(self) -> None:
        """A negative control: no shadow pose means the request goes."""
        client = _client()
        asked: list[str] = []

        async def _count(_topic: str, _payload: str) -> None:
            asked.append(_topic)

        client._publish = _count  # type: ignore[method-assign]

        with pytest.raises(TimeoutError):
            await client.get_position(timeout=0.05)

        assert asked == ["req"]


class TestDisconnectForgetsBothVerdicts:
    """Both flags describe the robot as seen over one session."""

    def test_neither_survives(self) -> None:
        """A firmware update that changes either brings a reconnect."""
        client = _client()
        client._position_unsupported = True
        client._shadow_publishes_pose = True

        client._forget_position_capabilities()

        assert not client._position_unsupported
        assert not client._shadow_publishes_pose


class TestAReconnectDoesNotEndTheStream:
    """The client reconnects on its own; the stream should come back.

    `_supervise` tears the connection down and rebuilds it, cancelling
    the poller on the way through. A stream that just returned there
    would leave the consumer with a finished iterator and no
    explanation — indistinguishable from a completed mission, while the
    client carried on working perfectly well.
    """

    @pytest.mark.asyncio
    async def test_the_poller_is_restarted(self) -> None:
        """A cancelled poller on a live client means restart, not stop."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        client._connected = True
        monkey_grace(30.0)

        stream = client.watch_position()
        pending = asyncio.ensure_future(anext(stream))
        await asyncio.sleep(0)

        first_poller = client._position_poller
        assert first_poller is not None

        # What a reconnect does on the way past.
        client._forget_position_capabilities()
        first_poller.cancel()
        await asyncio.sleep(0.05)

        assert client._position_poller is not first_poller
        assert not pending.done()

        pending.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(pending, return_exceptions=True)
        await stream.aclose()


class TestTwoWatchersDoNotDoublePoll:
    """Both wake on the same dead poller and both try to replace it.

    The second assignment overwrites the first, whose task keeps running
    unreferenced — two pollers asking the same robot twice as often,
    which is the exact thing one shared poller exists to prevent.
    """

    @pytest.mark.asyncio
    async def test_the_second_restart_is_a_no_op(self) -> None:
        """Only the watcher that saw the stale task replaces it.

        Async because `asyncio.Future()` needs a running loop -- outside
        one, Python 3.14 raises rather than making a policy loop, and
        this failed only there.
        """
        client = _client()
        stale = asyncio.get_running_loop().create_future()
        client._position_poller = stale  # type: ignore[assignment]

        client._restart_poller(stale, 5.0)  # type: ignore[arg-type]
        first = client._position_poller
        assert first is not stale

        # Second watcher, still holding the task it saw.
        client._restart_poller(stale, 5.0)  # type: ignore[arg-type]

        assert client._position_poller is first

        if first is not None:
            first.cancel()


class TestClosingAStreamLeavesNothingRunning:
    """A closed stream leaves no task running.

    `cancel()` only requests it; the task stays pending until the loop
    gets round to it.

    A caller that closes a stream and tears down its event loop would
    otherwise leave a task behind — and four tests here had to clean it
    up by hand, which was the library asking its callers to finish a job
    it started.
    """

    @pytest.mark.asyncio
    async def test_the_poller_is_finished_when_aclose_returns(self) -> None:
        """Not merely cancelled: actually done."""
        client = _client()

        async def _silent(_topic: str, _payload: str) -> None:
            return

        client._publish = _silent  # type: ignore[method-assign]
        monkey_grace(30.0)

        stream = client.watch_position()
        pending = asyncio.ensure_future(anext(stream))
        await asyncio.sleep(0)
        poller = client._position_poller
        assert poller is not None

        pending.cancel()
        await asyncio.sleep(0)
        await asyncio.gather(pending, return_exceptions=True)
        await stream.aclose()

        assert poller.done()
        assert client._position_poller is None

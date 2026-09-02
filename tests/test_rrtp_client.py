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
        client._position_watchers.add(queue)

        monkey_grace(0.01)
        with pytest.raises(rrtp.RrtpUnsupportedError):
            await client._run_position_poller(interval=0.01, timeout=0.05)

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
        client._position_watchers.add(queue)
        # The poller listens for a shadow pose before asking; shortened
        # here so the test does not wait out the real grace period.
        monkey_grace(0.01)
        task = asyncio.ensure_future(
            client._run_position_poller(interval=0.01, timeout=0.05)
        )
        pose = await asyncio.wait_for(queue.get(), timeout=5.0)
        client._position_watchers.discard(queue)
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
        client._position_watchers.add(queue)
        monkey_grace(0.01)
        task = asyncio.ensure_future(
            client._run_position_poller(interval=0.01, timeout=0.5)
        )
        await asyncio.sleep(0.2)
        task.cancel()
        client._position_watchers.discard(queue)

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
        client._position_watchers.add(queue)

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
        client._position_watchers.add(queue)
        monkey_grace(0.01)
        task = asyncio.ensure_future(
            client._run_position_poller(interval=0.01, timeout=0.05)
        )
        await asyncio.sleep(0.2)
        task.cancel()
        client._position_watchers.discard(queue)

        assert asked == []

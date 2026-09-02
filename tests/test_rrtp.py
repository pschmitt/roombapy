"""Tests for the rrtp position request path.

Every payload here is a real field capture, not an invented one. Four
robots across three firmware families produced them, and the shapes that
matter -- a no-fix reply, a docked reading, the wrap at pi -- came from
runs nobody designed to produce them.
"""

from __future__ import annotations

import asyncio
import math

import pytest
from roombapy import rrtp

# @Thonno's i7+, parked on its dock. The -0.01 is the useful part: a
# hardcoded docked value would read exactly zero.
DOCKED = {
    "reportType": "current",
    "reqId": "probe-1",
    "ver": "1.0.0",
    "data": [
        {
            "pmap_id": "tM_GAKM5SmyBhqotQtQrtw",
            "pmapv_id": "260901T194353",
            "coords": [
                {"type": "current", "xyt": [-0.01, 0.0, 0.0], "ts": 1788292259}
            ],
        }
    ],
}

# @ScenicSystemsLLC's Braava jet m6, mid-mission. It answered, echoed the
# id, named the map -- and had no position. `type: "unknown"`, no `xyt`.
NO_FIX = {
    "reportType": "current",
    "reqId": "probe-1",
    "ver": "1.0.0",
    "data": [
        {
            "pmap_id": "jUdHT1VfTZCaZklWE-_6tw",
            "pmapv_id": "260825T211448",
            "coords": [{"type": "unknown", "ts": 1788288769}],
        }
    ],
}


class TestParsingRealReplies:
    """Real captures, parsed."""

    def test_a_docked_reading(self) -> None:
        """A real reply from a docked robot."""
        pose = rrtp.parse_response(DOCKED)

        assert pose is not None
        assert (pose.x, pose.y, pose.theta) == (-0.01, 0.0, 0.0)
        assert pose.timestamp == 1788292259
        assert pose.source == "request"
        assert pose.pmap_id == "tM_GAKM5SmyBhqotQtQrtw"

    def test_no_fix_is_none_not_an_exception(self) -> None:
        """`type: "unknown"` is an answer, not a failure.

        A Braava produced nothing else for a whole mission. Raising here
        would force every caller into a try/except it does not want.
        """
        assert rrtp.parse_response(NO_FIX) is None

    def test_an_unknown_version_is_not_guessed_at(self) -> None:
        """Reject a version this library does not know.

        The client cannot ask for one -- the robot picks from its own
        registry. An unfamiliar version means an unknown response shape,
        and reading it as 1.0.0 would invent coordinates.
        """
        reply = dict(DOCKED, ver="2.0.0")

        assert rrtp.parse_response(reply) is None

    def test_a_short_xyt_does_not_unpack(self) -> None:
        """A malformed list must not raise.

        Length-checked rather than truthy, because this runs inside the
        message handler.
        """
        reply = {
            "ver": "1.0.0",
            "data": [{"coords": [{"type": "current", "xyt": [1.0, 2.0]}]}],
        }

        assert rrtp.parse_response(reply) is None


class TestBothGenerationsAgree:
    """Both generations produce the same Pose.

    A 900-series shadow pose and a requested one describe the same
    frame in different units. Converting in the library rather than in
    each consumer is the point: five callers would write the same
    formula five times, and one would get a sign wrong.
    """

    def test_shadow_converts_to_the_same_units(self) -> None:
        """Millimetres and degrees become metres and radians."""
        pose = rrtp.pose_from_shadow(
            {"theta": 153, "point": {"x": -16, "y": 243}}
        )

        assert pose is not None
        # Negative on purpose -- a flipped sign in a unit conversion
        # survives a test built only from positive numbers.
        assert pose.x == pytest.approx(-0.016)
        assert pose.y == pytest.approx(0.243)
        assert pose.theta == pytest.approx(math.radians(153))

    def test_source_still_tells_them_apart(self) -> None:
        """Unifying the units must not hide the cost difference.

        listening to a shadow is free, every requested pose is a round
        trip.
        """
        shadow = rrtp.pose_from_shadow({"theta": 0, "point": {"x": 0, "y": 0}})
        requested = rrtp.parse_response(DOCKED)

        assert shadow is not None
        assert requested is not None
        assert shadow.source == "shadow"
        assert requested.source == "request"

    def test_a_malformed_shadow_pose_is_none(self) -> None:
        """A pose without a point is not a pose."""
        assert rrtp.pose_from_shadow({"theta": 0}) is None


class TestThetaWrapIsNotSmoothed:
    """A turn in place crossing pi, from a real rate run.

        -1.43 -> -0.53 -> 0.53 -> 1.33 -> 1.97 -> 2.40 -> 3.06 -> -2.63

    The library reports what arrived. Normalising here would hide a
    discontinuity that consumers computing heading deltas have to know
    about -- otherwise a 30-degree turn reads as a 330-degree one.
    """

    def test_values_pass_through_unchanged(self) -> None:
        """Both sides of the wrap survive intact."""
        for theta in (3.06, -2.63):
            reply = {
                "ver": "1.0.0",
                "data": [
                    {"coords": [{"type": "current", "xyt": [0.0, 0.0, theta]}]}
                ],
            }
            pose = rrtp.parse_response(reply)

            assert pose is not None
            assert pose.theta == theta


class TestRequestMatching:
    """reqId is the only correlation the protocol offers."""

    @pytest.mark.asyncio
    async def test_a_reply_resolves_its_own_request(self) -> None:
        """The matching id delivers the answer."""
        requests = rrtp.RrtpRequests()
        req_id, future = requests.new_request()

        assert requests.resolve(dict(DOCKED, reqId=req_id)) is True
        assert (await future) is not None

    @pytest.mark.asyncio
    async def test_a_stranger_reply_resolves_nothing(self) -> None:
        """Matched by id, never by arrival order.

        Another client on the same broker, or an answer to a request
        that already timed out, must not satisfy this one -- that is how
        a caller quietly receives somebody else's position.
        """
        requests = rrtp.RrtpRequests()
        _req_id, future = requests.new_request()

        assert requests.resolve(dict(DOCKED, reqId="not-ours")) is False
        assert not future.done()

    @pytest.mark.asyncio
    async def test_abandoning_leaves_nothing_behind(self) -> None:
        """A caller that gave up leaves no trace."""
        requests = rrtp.RrtpRequests()
        req_id, _future = requests.new_request()
        requests.abandon(req_id)

        assert requests.in_flight == 0
        assert requests.resolve(dict(DOCKED, reqId=req_id)) is False

    @pytest.mark.asyncio
    async def test_cancel_all_fails_everything_outstanding(self) -> None:
        """Disconnect fails every waiter."""
        requests = rrtp.RrtpRequests()
        _req_id, future = requests.new_request()
        requests.cancel_all()
        await asyncio.sleep(0)

        assert future.cancelled()
        assert requests.in_flight == 0


class TestTheRequestBody:
    """What goes out on the request topic."""

    def test_it_matches_what_the_app_sends(self) -> None:
        """Three fields, no more."""
        body = rrtp.build_request("abc")

        assert body == {
            "reqId": "abc",
            "reqType": "current",
            "conType": "local",
        }

    def test_only_current_is_offered(self) -> None:
        """`historical`, `update` and `adjustment` are in the firmware's.

        enum. lewis checks them and rejects them -- verified on an i7+,
        all three silent while a nonsense type was also silent, so the
        field is read and the silence means 'not implemented here'.

        Offering them would invite callers to send requests no shipping
        robot answers.
        """
        assert rrtp.REQUEST_TYPE_CURRENT == "current"
        assert not hasattr(rrtp, "REQUEST_TYPE_HISTORICAL")

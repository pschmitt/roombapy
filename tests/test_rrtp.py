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


#: THE SECOND REPLY SHAPE, from a real cloud run (@Thonno, i7+ on lewis
#: 22.52.10). Same `reportType`, same `ver`, same robot as the object
#: form above -- minutes apart.
#:
#: `coords` IS the triple here, `ts` sits on the entry rather than
#: inside the coordinate, and `pmapv_id` is absent. The robot had just
#: finished a mission and was in its dock with the base emptying: still
#: localised, no mission running.
BARE_TRIPLE = {
    "reportType": "current",
    "reqId": "cloud-1",
    "ver": "1.0.0",
    "data": [
        {
            "pmap_id": "tM_GAKM5SmyBhqotQtQrtw",
            "coords": [0.02, 0.07, -1.56],
            "ts": 1788511060,
        }
    ],
}

#: The same robot mid-mission, object form, for contrast.
MID_MISSION = {
    "reportType": "current",
    "reqId": "cloud-1",
    "ver": "1.0.0",
    "data": [
        {
            "pmap_id": "tM_GAKM5SmyBhqotQtQrtw",
            "pmapv_id": "260904T074144",
            "coords": [
                {
                    "type": "current",
                    "xyt": [-3.63, 3.17, 1.74],
                    "ts": 1788511012,
                }
            ],
        }
    ],
}


class TestBothReplyShapes:
    """Both structures a robot uses to answer `current`.

    Found by field run, not by reading: the bare form was being dropped
    silently. `_first_dict(coords)` wanted a dict, found a float,
    returned None, and the caller reported "no fix" for a reply carrying
    a real position.

    It matters more than its rarity suggests. The bare form appears when
    the robot is localised with no mission running -- which is where a
    robot sits at the end of a run, and exactly the reading a live map
    would want in order to record where the cleaning finished.
    """

    def test_the_bare_triple_is_a_position(self) -> None:
        """Read a position out of the bare form."""
        pose = rrtp.parse_response(BARE_TRIPLE)

        assert pose is not None
        assert (pose.x, pose.y, pose.theta) == (0.02, 0.07, -1.56)

    def test_the_timestamp_comes_from_the_entry(self) -> None:
        """Read `ts` from the entry, where this shape puts it.

        Reading it from the coordinate would silently produce 0 -- a
        position stamped at the epoch, which no caller would question.
        """
        pose = rrtp.parse_response(BARE_TRIPLE)

        assert pose is not None
        assert pose.timestamp == 1788511060

    def test_a_missing_pmapv_id_is_none_not_invented(self) -> None:
        """Leave it None; the bare form omits it.

        Every other field still resolves.
        """
        pose = rrtp.parse_response(BARE_TRIPLE)

        assert pose is not None
        assert pose.pmapv_id is None
        assert pose.pmap_id == "tM_GAKM5SmyBhqotQtQrtw"

    def test_the_object_form_still_parses(self) -> None:
        """Keep the shape that already worked.

        The negative control for the change itself: widening the parser
        must not cost the object form.
        """
        pose = rrtp.parse_response(MID_MISSION)

        assert pose is not None
        assert (pose.x, pose.y, pose.theta) == (-3.63, 3.17, 1.74)
        assert pose.timestamp == 1788511012
        assert pose.pmapv_id == "260904T074144"

    def test_a_list_of_strings_is_not_a_position(self) -> None:
        """Document the outcome; do NOT read this as guarding the check.

        Strings are stopped twice over -- by the type check here and,
        failing that, by `float("a")` raising inside the conversion
        below. Replacing the type check with a bare length test leaves
        this test passing. Kept because the behaviour is worth pinning,
        and labelled because a test that cannot fail is worse than no
        test when someone later reads it as coverage.
        """
        coords = ["a", "b", "c"]
        reply = {"ver": "1.0.0", "data": [{"coords": coords, "ts": 1}]}

        assert rrtp.parse_response(reply) is None

    def test_booleans_are_not_coordinates(self) -> None:
        """Guard the type check -- the only test here that does.

        `True` is an `int` in Python and `float(True)` is `1.0`, so a
        length test alone would turn three booleans into the position
        (1.0, 0.0, 1.0) and report it as a fix. Confirmed by reverting
        the check: this test fails, the string test above does not.
        """
        coords = [True, False, True]
        reply = {"ver": "1.0.0", "data": [{"coords": coords, "ts": 1}]}

        assert rrtp.parse_response(reply) is None

    def test_a_missing_ts_defaults_but_an_explicit_null_does_not(self) -> None:
        """Keep the strictness the parser had before both shapes existed.

        A missing key means "not stated" and has always yielded 0. An
        explicit `null` or `""` means the robot said something and it
        was not a timestamp -- that used to raise inside `int()` and
        reject the whole reply.

        The first version of this change read `int(raw_ts or 0)`, which
        collapsed all three into 0 and would have produced positions
        stamped at the epoch. Caught in review on PR #590.
        """
        missing = {"ver": "1.0.0", "data": [{"coords": [1.0, 2.0, 3.0]}]}
        pose = rrtp.parse_response(missing)
        assert pose is not None
        assert pose.timestamp == 0

        for bad in (None, ""):
            reply = {
                "ver": "1.0.0",
                "data": [{"coords": [1.0, 2.0, 3.0], "ts": bad}],
            }
            assert rrtp.parse_response(reply) is None, bad

    def test_the_object_form_keeps_the_same_ts_rules(self) -> None:
        """The two shapes must not disagree about what a bad ts means."""
        missing = {
            "ver": "1.0.0",
            "data": [
                {"coords": [{"type": "current", "xyt": [1.0, 2.0, 3.0]}]}
            ],
        }
        pose = rrtp.parse_response(missing)
        assert pose is not None
        assert pose.timestamp == 0

        explicit_null = {
            "ver": "1.0.0",
            "data": [
                {
                    "coords": [
                        {"type": "current", "xyt": [1.0, 2.0, 3.0], "ts": None}
                    ]
                }
            ],
        }
        assert rrtp.parse_response(explicit_null) is None

    def test_a_short_bare_triple_does_not_unpack(self) -> None:
        """Refuse two numbers where three are needed."""
        reply = {"ver": "1.0.0", "data": [{"coords": [1.0, 2.0], "ts": 1}]}

        assert rrtp.parse_response(reply) is None


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

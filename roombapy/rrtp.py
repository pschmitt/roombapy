"""Real-time position requests (rrtp).

Newer robots do not publish their position. They answer when asked:
publish to `req`, the reply arrives on `data`, matched by `reqId`.

Confirmed against four robots across three firmware families -- lewis
(i7+, two S9+), sanmarino (Braava jet m6) and daredevil (i3). The topic
name came from the app's own initialiser; everything else came off the
wire.

    request   req    {"reqId": "...", "reqType": "current",
                      "conType": "local"}
    reply     data   {"reportType": "current", "reqId": <echo>,
                      "ver": "1.0.0",
                      "data": [{"pmap_id": ..., "pmapv_id": ...,
                                "coords": [{"type": "current",
                                            "xyt": [x_m, y_m, theta_rad],
                                            "ts": <unix>}]}]}

Only `reqType: "current"` is implemented on lewis. `historical`,
`update` and `adjustment` are in the firmware's enum, are checked, and
are rejected -- verified on hardware, not assumed.
"""

from __future__ import annotations

import asyncio
import logging
import math
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from collections.abc import Callable

_LOGGER = logging.getLogger(__name__)

REQUEST_TOPIC = "req"
RESPONSE_TOPIC = "data"

#: The only request type any robot has been seen to implement.
REQUEST_TYPE_CURRENT = "current"

#: `local` and `remote` are both valid firmware literals. A robot
#: answers either over a local connection, so `conType` is not the
#: routing switch its name suggests -- but sending the honest one costs
#: nothing.
CONNECTION_TYPE_LOCAL = "local"


class RrtpUnsupportedError(Exception):
    """Raised when a robot does not answer position requests.

    Raised by the position stream after repeated silence, so a consumer
    finds out rather than watching an empty map. A single request that
    times out raises nothing -- that is the caller's to interpret.
    """


@dataclass(frozen=True)
class RobotPosition:
    """Where the robot is, however that was obtained.

    NAMED APART FROM `types.Pose` ON PURPOSE. That one is the raw shadow
    shape -- a TypedDict of integer millimetres and degrees, exactly as
    the 900-series sends it. This is the interpreted form: floats,
    metres and radians, and a `source` saying which path produced it.
    Two names because they are two things, and collapsing them would
    hide a unit change behind a shared type.

    ALWAYS metres and radians, origin at the dock, x-axis along the
    direction the robot faces when docked.

    A 900-series publishes `pose` into its shadow as integer millimetres
    and degrees; lewis and later answer in metres and radians on
    request. Same frame, different units -- and if every caller converts
    for itself, every caller writes the same conversion and one of them
    gets a sign wrong.

    `source` says where it came from. Not for the geometry, which is
    identical, but because the COST differs: listening to a shadow is
    free, while every requested pose costs a round trip. A consumer
    choosing a poll interval needs to know whether it is paying for one.

    `theta` WRAPS AT PI. A field capture went from 3.06 to -2.63 across
    one turn. Anything computing heading deltas has to handle that, or
    it reads a 30-degree turn as a 330-degree one. Not normalised here:
    the library reports what arrived.
    """

    x: float
    y: float
    theta: float
    timestamp: int
    source: Literal["shadow", "request"]
    #: Which saved floorplan the coordinates belong to. Only the
    #: requested path carries these; the shadow keeps its map id
    #: elsewhere, and inventing a value here would be worse than None.
    pmap_id: str | None = None
    pmapv_id: str | None = None


def build_request(req_id: str) -> dict[str, str]:
    """Build the request body, exactly as the app sends it."""
    return {
        "reqId": req_id,
        "reqType": REQUEST_TYPE_CURRENT,
        "conType": CONNECTION_TYPE_LOCAL,
    }


def _first_dict(value: Any) -> dict[str, Any] | None:
    """First element of a list, when it is a dict; otherwise None."""
    if not isinstance(value, list) or not value:
        return None
    first = value[0]
    return first if isinstance(first, dict) else None


def _xyt_and_ts(entry: dict[str, Any]) -> tuple[Any, Any] | None:
    """Return the coordinate triple and timestamp from one entry.

    Handles whichever of the two reply shapes the robot used.

    THERE ARE TWO, AND THE SECOND WAS UNKNOWN UNTIL A FIELD RUN FOUND
    IT. Same `reportType`, same `ver: "1.0.0"`, same robot, minutes
    apart:

        coords: [{"type": "current", "xyt": [x, y, t], "ts": 123}]
        coords: [x, y, t]        with "ts" one level up, on the entry

    The second arrived from an i7+ on lewis 22.52.10 that had just
    finished a mission and was sitting in its dock while the base
    emptied (@Thonno, cloud path). It also omits `pmapv_id`, which the
    object form carries.

    WHAT IT COST BEFORE THIS EXISTED: the bare form was dropped
    silently. `_first_dict(coords)` found a float where it wanted a
    dict, returned None, and the caller reported "no fix" -- for a reply
    that carried a real position. That window matters more than its
    rarity suggests: it is precisely "localised, but no mission
    running", which is where a robot sits at the end of a run. A live
    map would have thrown away the one reading that says where the
    cleaning ended.

    Both shapes are accepted and neither is guessed at. A third shape
    returns None rather than being coerced into one of these.
    """
    coords = entry.get("coords")
    if not isinstance(coords, list) or not coords:
        return None

    first = coords[0]

    # The documented object form.
    if isinstance(first, dict):
        # `type: "unknown"` omits `xyt` entirely -- a robot that answered
        # and has no fix. Handled by the length check in the caller, not
        # here, so that "no coordinates" and "malformed coordinates"
        # stay one decision in one place.
        return first.get("xyt"), first.get("ts")

    # The bare form: coords IS the triple, and `ts` belongs to the entry.
    #
    # Checked by type rather than just by shape. A list of three
    # anythings would satisfy a length test, and coercing the wrong
    # thing into a position is worse than reporting no fix.
    numeric = (int, float)
    if all(
        isinstance(v, numeric) and not isinstance(v, bool) for v in coords
    ):
        return coords, entry.get("ts")

    return None


def _parse_v1(decoded: dict[str, Any]) -> RobotPosition | None:
    """Parse a `ver: 1.0.0` reply.

    Returns None when the robot answered but has no fix -- `type:
    "unknown"` with no `xyt`. That is a real state, not a failure: a
    Braava jet m6 produced it consistently while a vacuum on the same
    account returned coordinates.
    """
    first = _first_dict(decoded.get("data"))
    if first is None:
        return None
    found = _xyt_and_ts(first)
    if found is None:
        return None
    xyt, raw_ts = found

    # LENGTH-CHECKED, not just truthy. `type: "unknown"` omits the key
    # entirely, but a short or malformed list must not unpack.
    if not isinstance(xyt, (list, tuple)) or len(xyt) != 3:
        return None

    try:
        x, y, theta = (float(v) for v in xyt)
        ts = int(raw_ts or 0)
    except (TypeError, ValueError):
        _LOGGER.debug("rrtp: unparsable coordinates %r", xyt)
        return None

    return RobotPosition(
        x=x,
        y=y,
        theta=theta,
        timestamp=ts,
        source="request",
        pmap_id=first.get("pmap_id"),
        pmapv_id=first.get("pmapv_id"),
    )


#: Keyed on the `ver` the robot puts in its reply.
#:
#: The client cannot ASK for a version -- the request carries none, and
#: the robot picks from its own registry. lewis has exactly "1.0.0"
#: registered, and rejects anything else with a message parameterised by
#: version, which only makes sense if others can exist.
#:
#: One entry looks like over-engineering until a robot answers "2.0.0".
#: Then it is a line rather than a rewrite, and until then an unknown
#: version is logged instead of being misread as a known one.
_PARSERS: dict[str, Callable[[dict[str, Any]], RobotPosition | None]] = {
    "1.0.0": _parse_v1,
}


def parse_response(decoded: dict[str, Any]) -> RobotPosition | None:
    """Turn a reply into a RobotPosition, or None when there is no fix."""
    version = decoded.get("ver")
    parser = _PARSERS.get(str(version))
    if parser is None:
        _LOGGER.info(
            "rrtp: reply version %r is not supported by this library; "
            "the response shape is unknown and will not be guessed at",
            version,
        )
        return None
    return parser(decoded)


def pose_from_shadow(pose: dict[str, Any]) -> RobotPosition | None:
    """Convert a 900-series shadow `pose` into a RobotPosition.

    The shadow reports `{"theta": 153, "point": {"x": -16, "y": 243}}`
    -- integer millimetres and degrees. Same origin and same axis as the
    requested form, so only the units differ.

    Converting here rather than in each consumer is the whole point: it
    is one formula, and five callers would write it five times.
    """
    point = pose.get("point")
    if not isinstance(point, dict):
        return None
    try:
        x_mm = float(point["x"])
        y_mm = float(point["y"])
        theta_deg = float(pose["theta"])
    except (KeyError, TypeError, ValueError):
        return None

    return RobotPosition(
        x=x_mm / 1000.0,
        y=y_mm / 1000.0,
        theta=math.radians(theta_deg),
        timestamp=0,  # the shadow carries no timestamp for the pose
        source="shadow",
    )


class RrtpRequests:
    """Outstanding requests, matched by `reqId`.

    MATCHED BY ID, never by arrival order. Replies could in principle
    come back out of order, and assuming otherwise is how a request
    quietly resolves with somebody else's position.

    Holds no state beyond an in-flight request: a caller that stops
    waiting leaves nothing behind.
    """

    def __init__(self) -> None:
        """Start with nothing outstanding."""
        self._pending: dict[str, asyncio.Future[RobotPosition | None]] = {}

    def new_request(self) -> tuple[str, asyncio.Future[RobotPosition | None]]:
        """Register a request and return its id and future."""
        req_id = uuid.uuid4().hex[:12]
        future: asyncio.Future[RobotPosition | None] = (
            asyncio.get_running_loop().create_future()
        )
        self._pending[req_id] = future
        return req_id, future

    def resolve(self, decoded: dict[str, Any]) -> bool:
        """Deliver a reply to whoever asked for it.

        Returns True when the reply matched an outstanding request. An
        unmatched reply is dropped rather than resolving an arbitrary
        future -- it may be an answer to a request that already timed
        out, or to another client on the same broker.
        """
        req_id = str(decoded.get("reqId", ""))
        future = self._pending.pop(req_id, None)
        if future is None:
            _LOGGER.debug("rrtp: reply for unknown reqId %r, dropped", req_id)
            return False
        if not future.done():
            future.set_result(parse_response(decoded))
        return True

    def abandon(self, req_id: str) -> None:
        """Forget a request whose caller has given up."""
        self._pending.pop(req_id, None)

    def cancel_all(self) -> None:
        """Fail every outstanding request; used on disconnect."""
        for future in self._pending.values():
            if not future.done():
                future.cancel()
        self._pending.clear()

    @property
    def in_flight(self) -> int:
        """How many requests are waiting for a reply."""
        return len(self._pending)

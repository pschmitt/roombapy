"""Roomba state machine, independent of transport.

Extracted verbatim from ``Roomba`` so that the state logic can be driven by
either the threaded client or the async one. The method bodies below are
unchanged; only the class they hang off is new.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from roombapy.const import (
    ROOMBA_ERROR_MESSAGES,
    ROOMBA_STATES,
    ErrorCode,
    ErrorMessage,
    State,
)

RoombaMessage = dict[str, Any]


class RoombaStateMachine:
    """Accumulates reported state and derives the current mission state."""

    def __init__(self) -> None:
        """Start with an empty state."""
        self.log = logging.getLogger(__name__)
        self.master_state: RoombaMessage = {}
        self.co_ords = {"x": 0, "y": 0, "theta": 180}
        self.cleanMissionStatus_phase = ""
        self.previous_cleanMissionStatus_phase = ""
        self.current_state: State = None
        self.bin_full = False
        self.error_code: ErrorCode | None = None
        self.error_message: ErrorMessage | None = None

    def apply(self, decoded_message: RoombaMessage) -> None:
        """Merge a decoded payload and advance the state machine."""
        self.dict_merge(self.master_state, decoded_message)
        self.decode_topics(decoded_message)

    def republish_all(self) -> None:
        """Re-run decoding over the whole accumulated state."""
        self.decode_topics(self.master_state)

    def dict_merge(self, dct: RoombaMessage, merge_dct: RoombaMessage) -> None:
        """Recursive dict merge.

        Inspired by :meth:`dict.update`, instead
        of updating only top-level keys, dict_merge recurses down into dicts
        nested to an arbitrary depth, updating keys. The ``merge_dct`` is
        merged into ``dct``.

        TODO: Do not mutate arguments!
        """
        for k in merge_dct:
            if (
                k in dct
                and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)
            ):
                self.dict_merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]

    def decode_topics(
        self, state: RoombaMessage, prefix: str | None = None
    ) -> None:
        """Decode json data dict and publish as individual topics.

        Publish to brokerFeedback/topic the keys are concatenated with _
        to make one unique topic name strings are expressively converted
        to strings to avoid unicode representations
        """
        for key, value in state.items():
            mutable_key = key
            if isinstance(value, dict):
                if prefix is None:
                    self.decode_topics(value, key)
                else:
                    self.decode_topics(value, prefix + "_" + key)
            else:
                mutable_value = value
                if isinstance(value, list):
                    newlist = []
                    for i in value:
                        if isinstance(i, dict):
                            for ki, vi in i.items():
                                newlist.append((str(ki), vi))
                        else:
                            val = i
                            if isinstance(i, str):
                                val = str(i)
                            newlist.append(val)
                    mutable_value = newlist
                if prefix is not None:
                    mutable_key = prefix + "_" + key
                # all data starts with this, so it's redundant
                mutable_key = mutable_key.replace("state_reported_", "")
                # save variables for drawing map
                if mutable_key == "pose_theta":
                    self.co_ords["theta"] = mutable_value
                if mutable_key == "pose_point_x":  # x and y are reversed...
                    self.co_ords["y"] = mutable_value
                if mutable_key == "pose_point_y":
                    self.co_ords["x"] = mutable_value
                if mutable_key == "bin_full":
                    self.bin_full = mutable_value
                if mutable_key == "cleanMissionStatus_error":
                    try:
                        self.error_code = mutable_value
                        self.error_message = ROOMBA_ERROR_MESSAGES[
                            mutable_value
                        ]
                    except KeyError as e:
                        self.log.warning(
                            "Error looking up Roomba error message: %s", e
                        )
                        self.error_message = (
                            f"Unknown Error number: {mutable_value}"
                        )
                if mutable_key == "cleanMissionStatus_phase":
                    self.previous_cleanMissionStatus_phase = (
                        self.cleanMissionStatus_phase
                    )
                    self.cleanMissionStatus_phase = mutable_value

        if prefix is None:
            self.update_state_machine()

    def update_state_machine(self, new_state: State = None) -> None:
        """Roomba progresses through states (phases).

        Normal Sequence is "" -> charge -> run -> hmPostMsn -> charge
        Mid mission recharge is "" -> charge -> run -> hmMidMsn -> charge
                                   -> run -> hmPostMsn -> charge
        Stuck is "" -> charge -> run -> hmPostMsn -> stuck
                    -> run/charge/stop/hmUsrDock -> charge
        Start program during run is "" -> run -> hmPostMsn -> charge

        Need to identify a new mission to initialize map, and end of mission to
        finalise map.
        Assume  charge -> run = start of mission (init map)
                stuck - > charge = init map
        Assume hmPostMsn -> charge = end of mission (finalize map)
        Anything else = continue with existing map
        """
        current_mission = self.current_state

        try:
            if (
                self.master_state["state"]["reported"]["cleanMissionStatus"][
                    "mssnM"
                ]
                == "none"
                and self.cleanMissionStatus_phase == "charge"
                and self.current_state
                in (ROOMBA_STATES["pause"], ROOMBA_STATES["recharge"])
            ):
                self.current_state = ROOMBA_STATES["cancelled"]
        except KeyError:
            pass

        if (
            self.current_state == ROOMBA_STATES["charge"]
            and self.cleanMissionStatus_phase == "run"
        ):
            self.current_state = ROOMBA_STATES["new"]
        elif (
            self.current_state == ROOMBA_STATES["run"]
            and self.cleanMissionStatus_phase == "hmMidMsn"
        ):
            self.current_state = ROOMBA_STATES["dock"]
        elif (
            self.current_state == ROOMBA_STATES["dock"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            self.current_state = ROOMBA_STATES["recharge"]
        elif (
            self.current_state == ROOMBA_STATES["recharge"]
            and self.cleanMissionStatus_phase == "charge"
            and self.bin_full
        ):
            self.current_state = ROOMBA_STATES["pause"]
        elif (
            self.current_state == ROOMBA_STATES["run"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            self.current_state = ROOMBA_STATES["recharge"]
        elif (
            self.current_state == ROOMBA_STATES["recharge"]
            and self.cleanMissionStatus_phase == "run"
        ):
            self.current_state = ROOMBA_STATES["pause"]
        elif (
            self.current_state == ROOMBA_STATES["pause"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            self.current_state = ROOMBA_STATES["pause"]
            # so that we will draw map and can update recharge time
            current_mission = None
        elif (
            self.current_state == ROOMBA_STATES["charge"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            # so that we will draw map and can update charge status
            current_mission = None
        elif (
            self.current_state
            in (ROOMBA_STATES["stop"], ROOMBA_STATES["pause"])
        ) and self.cleanMissionStatus_phase == "hmUsrDock":
            self.current_state = ROOMBA_STATES["cancelled"]
        elif (
            (
                self.current_state
                in (ROOMBA_STATES["hmUsrDock"], ROOMBA_STATES["cancelled"])
            )
            and self.cleanMissionStatus_phase == "charge"
        ) or (
            self.current_state == ROOMBA_STATES["hmPostMsn"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            self.current_state = ROOMBA_STATES["dockend"]
        elif (
            self.current_state == ROOMBA_STATES["dockend"]
            and self.cleanMissionStatus_phase == "charge"
        ):
            self.current_state = ROOMBA_STATES["charge"]

        elif self.cleanMissionStatus_phase not in ROOMBA_STATES:
            self.log.error(
                "Can't find state %s in predefined Roomba states, "
                "please create a new issue: "
                "https://github.com/pschmitt/roombapy/issues/new",
                self.cleanMissionStatus_phase,
            )
            self.current_state = None
        else:
            self.current_state = ROOMBA_STATES[self.cleanMissionStatus_phase]

        if new_state is not None:
            self.current_state = ROOMBA_STATES[new_state]
            self.log.debug("Current state: %s", self.current_state)

        if self.current_state != current_mission:
            self.log.debug("State updated to: %s", self.current_state)

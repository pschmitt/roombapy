"""The typed view from D9."""

import ast
import pathlib
import typing
from typing import ClassVar

import orjson
import pytest
import roombapy.types
from roombapy.roomba import RoombaClient
from roombapy.types import ReportedState

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

PAYLOAD = (
    b'{"state":{"reported":{"batPct":100,"sku":"R980020",'
    b'"cap":{"pose":1,"maps":3},'
    b'"cleanMissionStatus":{"phase":"charge","error":0,"nMssn":209},'
    b'"pose":{"theta":45,"point":{"x":100,"y":-250}},'
    b'"bin":{"present":true,"full":false}}}}'
)


@pytest.fixture
def client() -> RoombaClient:
    """An unconnected client, fed directly."""
    return RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )


def test_reported_is_the_same_dict(client: RoombaClient) -> None:
    """The typed view is a view, not a copy — no parsing happens."""
    client._handle_message("test", PAYLOAD)

    reported: ReportedState = client.reported
    assert reported is client.master_state["state"]["reported"]


def test_reported_reads_nested_fields(client: RoombaClient) -> None:
    """Nested TypedDicts describe the real payload shape."""
    client._handle_message("test", PAYLOAD)
    reported = client.reported

    assert reported["batPct"] == 100
    assert reported["cap"]["pose"] == 1
    assert reported["cleanMissionStatus"]["phase"] == "charge"
    assert reported["pose"]["point"]["x"] == 100
    assert reported["bin"]["full"] is False


def test_reported_is_empty_before_any_message(client: RoombaClient) -> None:
    """No state yet is an empty mapping, not a KeyError."""
    assert client.reported == {}


def test_unknown_keys_survive(client: RoombaClient) -> None:
    """A key the TypedDict does not declare is still carried in the dict."""
    payload = orjson.dumps(
        {"state": {"reported": {"someFutureFirmwareKey": 42}}}
    )
    client._handle_message("test", payload)

    assert (
        client.master_state["state"]["reported"]["someFutureFirmwareKey"] == 42
    )


def test_lifetime_telemetry_is_typed(client: RoombaClient) -> None:
    """The bb* blocks are reachable through the typed view."""
    payload = orjson.dumps(
        {
            "state": {
                "reported": {
                    "bbrun": {"hr": 412, "nStuck": 7, "sqft": 15234},
                    "bbchg3": {"estCap": 1709, "nAvail": 489, "hOnDock": 88},
                    "bbmssn": {"nMssn": 209, "nMssnOk": 190, "nMssnF": 12},
                    "bbrstinfo": {"nOomRst": 1, "safCauses": [3, 3]},
                    "mssnNavStats": {"gLmk": 142, "l_drift": 2},
                }
            }
        }
    )
    client._handle_message("cmd", payload)
    reported = client.reported

    assert reported["bbrun"]["nStuck"] == 7
    assert reported["bbchg3"]["estCap"] == 1709
    assert reported["bbmssn"]["nMssnF"] == 12
    assert reported["bbrstinfo"]["safCauses"] == [3, 3]
    assert reported["mssnNavStats"]["l_drift"] == 2


def test_missing_telemetry_block_is_not_an_error(
    client: RoombaClient,
) -> None:
    """A robot with no bbchg3 is normal, not a failure."""
    client._handle_message(
        "cmd", orjson.dumps({"state": {"reported": {"batPct": 80}}})
    )
    assert "bbchg3" not in client.reported


def _hints() -> dict[str, object]:
    """Resolved annotations, not their `repr`.

    `ReportedState.__annotations__` holds `ForwardRef` objects under
    `from __future__ import annotations`, and their `repr` is not a
    stable API -- Python 3.14 appends `owner=...`, which broke a test
    that compared the string. `get_type_hints()` returns the real
    objects and is what a consumer would use.
    """
    return typing.get_type_hints(ReportedState)


class TestReportedStateCoversWhatRealRobotsSend:
    """`ReportedState` declared 37 keys; real robots send up to 69 each.

    The declarations were assembled from complete key dumps of four
    firmware families -- 9-series, lewis, soho and sanmarino -- whose
    union is 94 keys. These tests pin the parts of that which are easy
    to lose: the families themselves, and the fields where a firmware
    difference is the whole point.

    Nothing here asserts that a robot MUST send a key. `total=False`
    means every one is optional, and which ones arrive depends on the
    firmware family rather than on the hardware alone.
    """

    #: Seen on all four fully-dumped families.
    UNIVERSAL = (
        "bbpause",
        "bbswitch",
        "cloudEnv",
        "country",
        "ecoCharge",
        "mapUploadAllowed",
        "netinfo",
        "schedHold",
        "svcEndpoints",
        "timezone",
        "wifistat",
        "wlcfg",
    )

    def test_the_universal_fields_are_declared(self) -> None:
        """All four families send these."""
        declared = set(ReportedState.__annotations__)

        assert set(self.UNIVERSAL) <= declared

    def test_netinfo_is_a_mapping_with_an_open_inner_type(self) -> None:
        """The generation difference is inside it, not on it.

        Every capture shows a mapping. What differs is the ADDRESS
        FIELDS within it -- uint32 on 9-series, dotted strings on newer
        firmware. An earlier draft of this type made the outer field a
        union of dict/int/str, which no capture supports; the inner
        values are left open instead.
        """
        annotation = _hints()["netinfo"]

        assert typing.get_origin(annotation) is dict
        assert typing.get_origin(annotation) is not typing.Union

    def test_the_two_schedule_shapes_are_both_declared(self) -> None:
        """Both schedule shapes are declared.

        9-series sends `cleanSchedule`, i/s sends `cleanSchedule2`, and
        they never coexist. A consumer that knows only one silently sees
        no schedule on half the fleet.
        """
        declared = set(ReportedState.__annotations__)

        assert "cleanSchedule" in declared
        assert "cleanSchedule2" in declared

    def test_the_two_version_blocks_are_both_declared(self) -> None:
        """Both version blocks are declared.

        9-series spreads component versions across separate keys; i/s
        collapses them into `subModSwVer`.
        """
        declared = set(ReportedState.__annotations__)

        assert "subModSwVer" in declared
        for nine_series in ("navSwVer", "mobilityVer", "soundVer", "uiSwVer"):
            assert nine_series in declared

    def test_mission_telemetry_is_not_typed_as_telemetry(self) -> None:
        """It is not telemetry, despite the name.

        It carries a fixed set of "which reports are enabled" flags,
        verified unchanged byte-for-byte across four samples spanning a
        real room transition. Typing it as anything richer would invite
        a consumer to read progress out of it.
        """
        annotation = _hints()["missionTelemetry"]

        assert typing.get_origin(annotation) is dict
        assert typing.get_args(annotation) == (str, int)

    def test_nothing_is_declared_twice(self) -> None:
        """No field is declared twice.

        A TypedDict silently keeps the last definition, so a duplicate is
        invisible until the types disagree. One slipped in while this
        class was being extended.
        """
        source = pathlib.Path(
            ReportedState.__module__.replace(".", "/") + ".py"
        )
        if not source.exists():  # installed rather than checked out
            source = pathlib.Path(roombapy.types.__file__)

        tree = ast.parse(source.read_text(encoding="utf-8"))
        cls = next(
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.ClassDef) and n.name == "ReportedState"
        )
        names = [
            n.target.id
            for n in cls.body
            if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
        ]

        assert len(names) == len(set(names)), sorted(
            n for n in names if names.count(n) > 1
        )


class TestNoTypeIsDeclaredWithoutEvidence:
    """No annotation rests on a guess.

    A key can be evidenced without its shape being evidenced.

    Diagnostics downloads list key names only. One full value dump was
    available while this class was extended -- a Braava jet m6 -- and
    checking the declarations against it found three wrong: `chrgLrPtrn`
    and `deploymentState` and `pmapSGen`, all guessed from their names
    as structures or strings, all ints in reality. A fourth, `netinfo`,
    had been given a union of `dict | int | str` on the strength of a
    note about a generation difference that turns out to live in the
    fields INSIDE it.

    So: where no value has been seen, the annotation is `Any`. That is
    not laziness -- it is the accurate statement, and a wrong concrete
    type is worse than an honest open one.
    """

    #: Types confirmed against a real value dump.
    EVIDENCED: ClassVar[dict[str, str]] = {
        "chrgLrPtrn": "int",
        "deploymentState": "int",
        "pmapSGen": "int",
        "rankOverlap": "int",
        "tankLvl": "int",
        "lastDisconnect": "int",
        "childLock": "bool",
        "connected": "bool",
        "pmapCL": "bool",
        "schedHold": "bool",
        "cloudEnv": "str",
        "country": "str",
        "timezone": "str",
    }

    def test_the_evidenced_types_are_what_was_observed(self) -> None:
        """Each of these was read off a real robot, not inferred."""
        hints = _hints()
        for field, expected in self.EVIDENCED.items():
            assert (
                hints[field]
                is {"int": int, "bool": bool, "str": str}[expected]
            ), f"{field}: {hints[field]}"

    def test_the_three_corrected_fields_are_not_structures(self) -> None:
        """The specific mistake, pinned.

        All three read like they hold something structured, and all
        three are plain ints.
        """
        hints = _hints()
        for field in ("chrgLrPtrn", "deploymentState", "pmapSGen"):
            assert hints[field] is int, f"{field}: {hints[field]}"

    def test_the_nine_series_block_is_typed_from_its_dump(self) -> None:
        """Thirteen fields settled by one full 980 value dump.

        Two of them are worth naming: `soundVer` is a string despite
        reading as a number (`'32'`), and `langs` is a list of one-entry
        maps rather than a flat list of names.
        """
        hints = _hints()

        assert hints["soundVer"] is str
        assert typing.get_origin(hints["langs"]) is list
        assert hints["language"] is int
        assert typing.get_origin(hints["bbpanic"]) is dict

    def test_unobserved_fields_are_open(self) -> None:
        """Sampled from the group with no value dump behind it."""
        hints = _hints()
        for field in ("smartHome", "odoaMode", "sceneRecog", "hwDbgr"):
            assert hints[field] is typing.Any, f"{field}: {hints[field]}"

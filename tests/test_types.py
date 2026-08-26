"""The typed view from D9."""

import orjson
import pytest
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

"""Parity with the threaded client: topic exclusion and periodic re-derive."""

import pytest
from roombapy.roomba import RoombaClient, TransportOptions

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

PAYLOAD = b'{"state":{"reported":{"batPct":42}}}'


def _client(**options: object) -> RoombaClient:
    return RoombaClient(
        address=ROOMBA_HOST,
        blid=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        transport=TransportOptions(**options),  # type: ignore[arg-type]
    )


def test_excluded_topics_are_dropped() -> None:
    """A topic matching `exclude` never reaches the state machine."""
    client = _client(exclude="wifistat")

    client._handle_message("wifistat", PAYLOAD)
    assert client.master_state == {}

    client._handle_message("cmd", PAYLOAD)
    assert client.master_state["state"]["reported"]["batPct"] == 42


def test_exclude_is_off_by_default() -> None:
    """An empty `exclude` filters nothing, as in the threaded client."""
    client = _client()
    client._handle_message("wifistat", PAYLOAD)
    assert client.master_state["state"]["reported"]["batPct"] == 42


def test_periodic_rederive_advances_the_state_machine() -> None:
    """After `update_seconds`, derived state is recomputed from the whole."""
    client = _client(update_seconds=0)

    client._handle_message(
        "cmd",
        b'{"state":{"reported":{"cleanMissionStatus":'
        b'{"phase":"charge","mssnM":1}}}}',
    )
    assert client.current_state == "Charging"

    # A delta that does not mention the phase still triggers the periodic
    # re-derive, which re-runs the state machine over the accumulated state.
    client._handle_message("cmd", PAYLOAD)
    assert client.cleanMissionStatus_phase == "charge"


@pytest.mark.parametrize(
    "name", ["co_ords", "bin_full", "cleanMissionStatus_phase"]
)
def test_derived_properties_exist(name: str) -> None:
    """Derived values the threaded client exposes are reachable here too."""
    assert hasattr(_client(), name)

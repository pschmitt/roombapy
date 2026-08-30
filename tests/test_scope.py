"""Two protections derived from firmware and vendor-app evidence."""

import pytest
from roombapy.const import ROOMBA_STATES
from roombapy.roomba import (
    REGION_SCOPED_COMMANDS,
    RoombaClient,
    RoombaScopeError,
)

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

# The robot firmware's cleanMissionStatus.phase enum, in full.
FIRMWARE_PHASES = (
    "new",
    "run",
    "pause",
    "stop",
    "resume",
    "charge",
    "evac",
    "stuck",
    "spot",
    "completed",
    "cancelled",
    "hmUsrDock",
    "hmMidMsn",
    "hmPostMsn",
)


@pytest.fixture
def client() -> RoombaClient:
    """An unconnected client — the guard runs before any I/O."""
    return RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("empty", [[], None])
async def test_empty_regions_is_refused(
    client: RoombaClient, empty: list[str] | None
) -> None:
    """An empty region list would clean the whole house, so refuse it."""
    with pytest.raises(RoombaScopeError, match="whole house"):
        await client.send_command("start", {"regions": empty, "pmap_id": "x"})


@pytest.mark.asyncio
async def test_absent_regions_is_allowed(client: RoombaClient) -> None:
    """Omitting `regions` is how a whole-house run is expressed; allow it."""
    with pytest.raises(Exception) as excinfo:
        await client.send_command("start")
    assert not isinstance(excinfo.value, RoombaScopeError)


@pytest.mark.asyncio
async def test_non_empty_regions_passes_the_guard(
    client: RoombaClient,
) -> None:
    """A real region list is not what the guard is looking for."""
    with pytest.raises(Exception) as excinfo:
        await client.send_command(
            "start",
            {"regions": [{"region_id": "3", "type": "rid"}], "pmap_id": "x"},
        )
    assert not isinstance(excinfo.value, RoombaScopeError)


@pytest.mark.asyncio
async def test_guard_only_applies_to_scoped_commands(
    client: RoombaClient,
) -> None:
    """`dock` is not room-scoped, so an empty list there is not the trap."""
    assert "dock" not in REGION_SCOPED_COMMANDS
    with pytest.raises(Exception) as excinfo:
        await client.send_command("dock", {"regions": []})
    assert not isinstance(excinfo.value, RoombaScopeError)


@pytest.mark.parametrize("phase", FIRMWARE_PHASES)
def test_every_firmware_phase_has_a_state(phase: str) -> None:
    """An unlisted phase reaches the 'please open an issue' branch."""
    assert phase in ROOMBA_STATES

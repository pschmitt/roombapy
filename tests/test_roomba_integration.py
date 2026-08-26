"""Test Roomba integration with the mocked device."""

import asyncio

import pytest
from roombapy import Roomba


@pytest.mark.asyncio
async def test_roomba_connect(roomba: Roomba) -> None:
    """Connect to the Roomba."""
    is_connected = await roomba_connect(roomba)
    await roomba_disconnect(roomba)
    assert is_connected


@pytest.mark.asyncio
async def test_roomba_connect_error(broken_roomba: Roomba) -> None:
    """Test Roomba connect error."""
    is_connected = await roomba_connect(broken_roomba)
    assert not is_connected


async def roomba_connect(robot: Roomba) -> bool:
    """Connect to the Roomba."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, robot.connect)
    await asyncio.sleep(1)
    return robot.roomba_connected


async def roomba_disconnect(robot: Roomba) -> None:
    """Disconnect from the Roomba."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, robot.disconnect)

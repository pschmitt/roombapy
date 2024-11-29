"""Test Roomba integration with the mocked device."""

import asyncio
from asyncio import BaseEventLoop

import pytest
from roombapy import Roomba


@pytest.mark.asyncio
async def test_roomba_connect(roomba: Roomba, event_loop: BaseEventLoop) -> None:
    """Connect to the Roomba."""
    is_connected = await roomba_connect(roomba, event_loop)
    await roomba_disconnect(roomba, event_loop)
    assert is_connected


@pytest.mark.asyncio
async def test_roomba_connect_error(
    broken_roomba: Roomba, event_loop: BaseEventLoop
) -> None:
    """Test Roomba connect error."""
    is_connected = await roomba_connect(broken_roomba, event_loop)
    assert not is_connected


async def roomba_connect(robot: Roomba, loop: BaseEventLoop) -> bool:
    """Connect to the Roomba."""
    await loop.run_in_executor(None, robot.connect)
    await asyncio.sleep(1)
    return robot.roomba_connected


async def roomba_disconnect(robot: Roomba, loop: BaseEventLoop) -> None:
    """Disconnect from the Roomba."""
    await loop.run_in_executor(None, robot.disconnect)

import asyncio

import pytest


@pytest.mark.asyncio
async def test_roomba_connect(event_loop, roomba):
    is_connected = await roomba_connect(roomba, event_loop)
    await roomba_disconnect(roomba, event_loop)
    assert is_connected


@pytest.mark.asyncio
async def test_roomba_connect_error(broken_roomba, event_loop):
    is_connected = await roomba_connect(broken_roomba, event_loop)
    assert not is_connected


async def roomba_connect(robot, loop):
    await loop.run_in_executor(None, robot.connect)
    await asyncio.sleep(1)
    return robot.roomba_connected


async def roomba_disconnect(robot, loop):
    await loop.run_in_executor(None, robot.disconnect)

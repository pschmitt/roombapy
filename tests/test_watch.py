"""The watch() async iterator from D2."""

import asyncio
import logging
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from roombapy.roomba import RoombaClient

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME


@pytest_asyncio.fixture
async def client() -> AsyncIterator[RoombaClient]:
    """Yield a connected client, torn down afterwards."""
    instance = RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )
    await instance.connect()
    yield instance
    await instance.disconnect()


@pytest.mark.asyncio
async def test_two_watchers_both_receive(client: RoombaClient) -> None:
    """Fan-out: each watcher gets its own copy of every message."""

    async def take_one(
        stream: AsyncIterator[dict[str, object]],
    ) -> dict[str, object]:
        async for message in stream:
            return message
        msg = "stream ended"
        raise AssertionError(msg)

    first = asyncio.create_task(take_one(client.watch()))
    second = asyncio.create_task(take_one(client.watch()))
    await asyncio.sleep(0.1)

    await client.send_command("start")

    async with asyncio.timeout(5):
        got_first, got_second = await asyncio.gather(first, second)

    assert got_first["command"] == "start"
    assert got_second["command"] == "start"


@pytest.mark.asyncio
async def test_slow_watcher_drops_oldest(
    client: RoombaClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Drop the oldest message for a watcher that falls behind, and log it."""
    stream = client.watch(maxsize=2)

    # Advance once so the queue is registered, then stop consuming: the
    # generator stays suspended at its yield while messages pile up.
    first: asyncio.Task[dict[str, object]] = asyncio.ensure_future(
        anext(stream)
    )
    await asyncio.sleep(0.1)
    await client.send_command("start", {"n": 0})
    async with asyncio.timeout(5):
        await first

    with caplog.at_level(logging.WARNING):
        for index in range(1, 6):
            await client.send_command("start", {"n": index})
        await asyncio.sleep(0.5)

    assert "fell behind" in caplog.text


@pytest.mark.asyncio
async def test_watcher_detaches_on_exit(client: RoombaClient) -> None:
    """Leaving the async for removes the queue."""

    async def consume() -> None:
        async for _message in client.watch():
            return

    await asyncio.sleep(0.05)
    task = asyncio.create_task(consume())
    await asyncio.sleep(0.1)
    await client.send_command("start")
    async with asyncio.timeout(5):
        await task
    await asyncio.sleep(0.1)

    assert not client._watchers

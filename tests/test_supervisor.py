"""Reconnect ownership, as agreed in the review of the design."""

import asyncio
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from roombapy.roomba import RoombaClient

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME


async def _drop_session(client: RoombaClient) -> None:
    """Tear the transport out from under the supervisor."""
    transport = client._client
    assert transport is not None
    await transport.__aexit__(None, None, None)


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
async def test_auth_failure_after_connect_does_not_retry() -> None:
    """A rejected credential is not transient; retrying would never end.

    The guard on the first connect is not enough: a robot that is
    re-provisioned mid-session rejects the old password on the next
    reconnect, and before this the supervisor backed off and tried forever.
    """
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)
    await client.connect()

    # Rotate the credential the way a re-provisioned robot would, then drop
    # the session so the supervisor reconnects with the stale password.
    client.password = "wrong"
    await _drop_session(client)

    async with asyncio.timeout(15):
        while client.auth_error is None:
            await asyncio.sleep(0.1)

    assert not client.connected
    # Give the supervisor time to loop again if it were going to.
    await asyncio.sleep(3)
    assert not client.connected
    assert client._task is None or client._task.done()

    await client.disconnect()


@pytest.mark.asyncio
async def test_connection_state_callback_reports_both_directions(
    client: RoombaClient,
) -> None:
    """A caller marking an entity unavailable needs both transitions."""
    seen: list[tuple[str, str | None]] = []
    client.register_on_connection_state_callback(
        lambda state, error: seen.append((state, error))
    )

    await _drop_session(client)

    async with asyncio.timeout(20):
        while [s for s, _ in seen] != ["disconnected", "connected"]:
            await asyncio.sleep(0.1)

    assert seen[0][0] == "disconnected"
    assert seen[0][1] is not None
    assert seen[1] == ("connected", None)


@pytest.mark.asyncio
async def test_state_callback_unsubscribes(client: RoombaClient) -> None:
    """The detach handle works here too."""
    seen: list[str] = []
    unsubscribe = client.register_on_connection_state_callback(
        lambda state, _error: seen.append(state)
    )
    unsubscribe()

    await _drop_session(client)
    await asyncio.sleep(3)

    assert seen == []

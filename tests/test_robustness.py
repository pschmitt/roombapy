"""Robustness of the supervisor and the lifecycle.

Each of these covers a failure that was found by probing the implementation
rather than by a report, and each failed before the corresponding fix.
"""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

import pytest
import pytest_asyncio
from roombapy.roomba import (
    RECONNECT_BACKOFF_JITTER,
    RoombaClient,
    RoombaConnectionError,
    RoombaError,
    TransportOptions,
)

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
async def test_unexpected_error_does_not_kill_the_supervisor() -> None:
    """A fault in the message path must not end reconnection for good.

    Only ``MqttError`` used to be caught, so a malformed payload the state
    machine choked on escaped the task: no reconnect, no callback, and the
    exception sitting unretrieved until someone awaited the task.
    """
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)
    await client.connect()

    calls = 0
    original = client._state.apply

    def explode_once(decoded_message: dict[str, Any]) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            msg = "simulated fault in the state machine"
            raise RuntimeError(msg)
        original(decoded_message)

    client._state.apply = explode_once  # type: ignore[method-assign]

    await client.send_command("start")

    # First the fault must actually take the session down, otherwise the
    # recovery check below would pass without anything having happened.
    async with asyncio.timeout(10):
        while client.connected:
            await asyncio.sleep(0.05)

    # Then the supervisor should back off and come back on its own.
    async with asyncio.timeout(20):
        while not client.connected:
            await asyncio.sleep(0.1)

    assert client._task is not None
    assert not client._task.done()

    # And the message path still works afterwards.
    await client.send_command("stop")
    async with asyncio.timeout(10):
        while calls < 2:
            await asyncio.sleep(0.05)

    await client.disconnect()


@pytest.mark.asyncio
async def test_second_connect_raises(client: RoombaClient) -> None:
    """Connecting twice was a silent no-op that looked like success."""
    with pytest.raises(RoombaError, match="Already connected"):
        await client.connect()


@pytest.mark.asyncio
async def test_disconnect_waits_for_callbacks_in_flight() -> None:
    """A callback persisting state should not be dropped on unload."""
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)
    finished: list[int] = []

    async def slow(_message: dict[str, Any]) -> None:
        await asyncio.sleep(1)
        finished.append(1)

    await client.connect()
    client.register_on_message_callback(slow)
    await client.send_command("start")
    await asyncio.sleep(0.2)

    await client.disconnect()

    assert finished, "callback was cancelled instead of being awaited"
    assert not client._pending_callbacks


def test_backoff_has_jitter() -> None:
    """Robots in one household should not all return in lockstep."""
    assert RECONNECT_BACKOFF_JITTER > 0


@pytest.mark.asyncio
async def test_transport_errors_do_not_leak_out_of_send_command() -> None:
    """A caller told to catch RoombaError should not meet aiomqtt's types.

    The connected check in _publish is only a pre-check: the session can
    drop between it and the publish itself.
    """
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)
    await client.connect()

    transport = client._client
    assert transport is not None
    await transport.__aexit__(None, None, None)

    with pytest.raises(RoombaConnectionError):
        await client.send_command("start")

    await client.disconnect()


@pytest.mark.asyncio
async def test_connect_can_be_bounded_by_the_caller() -> None:
    """Cancelling connect() tears the client down rather than leaking a task.

    Reaching an unreachable host takes about 18s by default — three
    attempts, each waiting out a TCP connect. A config flow wanting less
    should be able to wrap it.
    """
    client = RoombaClient("10.255.255.1", "x", "y")

    with pytest.raises(TimeoutError):
        async with asyncio.timeout(2):
            await client.connect()

    assert client._task is None
    assert not client.connected


@pytest.mark.asyncio
async def test_reconnect_after_auth_failure_is_allowed() -> None:
    """Re-provisioning a robot must not require a disconnect() first.

    The supervisor deliberately ends on an auth failure rather than
    retrying, which leaves the task set but done. Refusing to connect on
    that basis blocked the one recovery a caller actually wants — and the
    error message named that very case as the reason to try.
    """
    # The failure has to happen mid-session: a first connect that fails
    # cleans up after itself, so it would not exercise this at all.
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)
    await client.connect()

    client.password = "wrong"
    await _drop_session(client)

    async with asyncio.timeout(15):
        while client.auth_error is None:
            await asyncio.sleep(0.1)

    assert not client.connected
    assert client._task is not None
    assert client._task.done()

    # Correct credentials, as after re-provisioning. No disconnect() first.
    client.password = ROOMBA_PASSWORD
    await client.connect()
    assert client.connected
    assert client.auth_error is None

    await client.disconnect()


@pytest.mark.asyncio
async def test_unsubscribe_is_idempotent() -> None:
    """Handles land in finally blocks; a second call must not raise.

    list.remove raises ValueError when the callback is already gone, which
    turns a tidy-up path into a second failure.
    """
    client = RoombaClient(ROOMBA_HOST, ROOMBA_USERNAME, ROOMBA_PASSWORD)

    def noop(_payload: object) -> None:
        return

    for register in (
        client.register_on_message_callback,
        client.register_on_disconnect_callback,
        client.register_on_connection_state_callback,
    ):
        unsubscribe = register(noop)  # type: ignore[arg-type]
        unsubscribe()
        unsubscribe()


@pytest.mark.asyncio
async def test_failed_first_connect_reports_no_disconnect() -> None:
    """Retries during the initial connect are not losses.

    A consumer would otherwise mark an entity unavailable that had never
    been available in the first place.
    """
    client = RoombaClient(
        ROOMBA_HOST,
        ROOMBA_USERNAME,
        ROOMBA_PASSWORD,
        transport=TransportOptions(port=8884),
    )
    disconnects: list[str | None] = []
    states: list[str] = []
    client.register_on_disconnect_callback(disconnects.append)
    client.register_on_connection_state_callback(
        lambda state, _error: states.append(state)
    )

    with pytest.raises(RoombaConnectionError):
        await client.connect()
    await asyncio.sleep(0.3)

    assert disconnects == []
    assert states == []

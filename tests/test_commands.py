"""Outbound commands and the D2 callback contract."""

import asyncio
import ssl
from collections.abc import AsyncIterator

import aiomqtt
import orjson
import pytest
import pytest_asyncio
from roombapy.roomba import RoombaClient, RoombaConnectionError

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME


async def _collect(
    topic: str, ready: asyncio.Event
) -> list[dict[str, object]]:
    """Subscribe as a bystander and capture what the client publishes."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.set_ciphers("DEFAULT:!DH")
    seen: list[dict[str, object]] = []
    async with aiomqtt.Client(
        hostname=ROOMBA_HOST,
        port=8883,
        identifier="observer",
        username=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        tls_context=context,
        tls_insecure=True,
    ) as observer:
        await observer.subscribe(topic)
        ready.set()
        async for message in observer.messages:
            seen.append(orjson.loads(message.payload))
            break
    return seen


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
async def test_send_command_payload(client: RoombaClient) -> None:
    """send_command puts the documented envelope on the cmd topic."""
    ready = asyncio.Event()
    observer = asyncio.create_task(_collect("cmd", ready))
    await ready.wait()

    await client.send_command("start", {"ordered": 1})

    async with asyncio.timeout(5):
        seen = await observer

    assert seen[0]["command"] == "start"
    assert seen[0]["initiator"] == "localApp"
    assert seen[0]["ordered"] == 1
    assert isinstance(seen[0]["time"], int)


@pytest.mark.asyncio
async def test_set_preference_parses_boolean_strings(
    client: RoombaClient,
) -> None:
    """ "true" becomes a real boolean, as in the threaded client."""
    ready = asyncio.Event()
    observer = asyncio.create_task(_collect("delta", ready))
    await ready.wait()

    await client.set_preference("binPause", "true")

    async with asyncio.timeout(5):
        seen = await observer

    assert seen[0] == {"state": {"binPause": True}}


@pytest.mark.asyncio
async def test_publish_while_disconnected_raises() -> None:
    """Commands sent without a session fail loudly rather than vanishing."""
    instance = RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )
    with pytest.raises(RoombaConnectionError):
        await instance.send_command("start")


@pytest.mark.asyncio
async def test_async_callback_is_awaited(client: RoombaClient) -> None:
    """An async def callback runs, on the loop."""
    seen: list[dict[str, object]] = []

    async def handler(message: dict[str, object]) -> None:
        await asyncio.sleep(0)
        seen.append(message)

    client.register_on_message_callback(handler)
    await client.send_command("start")

    async with asyncio.timeout(5):
        while not seen:
            await asyncio.sleep(0.01)


@pytest.mark.asyncio
async def test_one_bad_callback_does_not_silence_the_others(
    client: RoombaClient,
) -> None:
    """A raising callback must not stop delivery to the rest."""
    seen: list[dict[str, object]] = []

    def explodes(_message: dict[str, object]) -> None:
        msg = "callback failure"
        raise RuntimeError(msg)

    client.register_on_message_callback(explodes)
    client.register_on_message_callback(seen.append)

    await client.send_command("start")

    async with asyncio.timeout(5):
        while not seen:
            await asyncio.sleep(0.01)

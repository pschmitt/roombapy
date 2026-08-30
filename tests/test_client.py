"""Vertical slice for the prototype async client, against a real broker."""

import asyncio
import ssl

import aiomqtt
import pytest
from roombapy.roomba import (
    RoombaAuthError,
    RoombaClient,
    RoombaConnectionError,
    TransportOptions,
)

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

PAYLOAD = (
    '{"state":{"reported":{"cleanMissionStatus":{"cycle":"none",'
    '"phase":"charge","error":0,"mssnM":108,"nMssn":209},'
    '"bin":{"present":true,"full":false},"batPct":100}}}'
)


def _publisher_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.set_ciphers("DEFAULT:!DH")
    return context


async def _publish(topic: str, payload: str) -> None:
    """Stand in for the robot pushing an update."""
    async with aiomqtt.Client(
        hostname=ROOMBA_HOST,
        port=8883,
        identifier="publisher",
        username=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        tls_context=_publisher_context(),
        tls_insecure=True,
    ) as client:
        await client.publish(topic, payload)


@pytest.mark.asyncio
async def test_slice_connect_receive_disconnect() -> None:
    """Connect, receive one push, drive the state machine, disconnect."""
    client = RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )
    received: list[dict[str, object]] = []
    client.register_on_message_callback(received.append)

    await client.connect()
    assert client.connected

    await _publish("test", PAYLOAD)
    async with asyncio.timeout(5):
        while not received:
            await asyncio.sleep(0.01)

    assert client.master_state["state"]["reported"]["batPct"] == 100
    assert client.current_state == "Charging"  # dead before the phase fix

    await client.disconnect()
    assert not client.connected


@pytest.mark.asyncio
async def test_slice_bad_credentials_raise() -> None:
    """A rejected connection raises rather than leaving a flag unset."""
    client = RoombaClient(
        address=ROOMBA_HOST, blid="wrong", password=ROOMBA_PASSWORD
    )
    with pytest.raises(RoombaAuthError):
        await client.connect()
    assert not client.connected


@pytest.mark.asyncio
async def test_slice_unreachable_host_raises() -> None:
    """An unreachable host gives up after the retry budget."""
    client = RoombaClient(
        address="127.0.0.1",
        blid=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        transport=TransportOptions(port=8884),
    )
    with pytest.raises(RoombaConnectionError):
        await client.connect()


@pytest.mark.asyncio
async def test_slice_unsubscribe_detaches() -> None:
    """The handle returned by registration actually removes the callback."""
    client = RoombaClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )
    received: list[dict[str, object]] = []
    unsubscribe = client.register_on_message_callback(received.append)
    unsubscribe()

    await client.connect()
    await _publish("test", PAYLOAD)
    await asyncio.sleep(0.5)
    await client.disconnect()

    assert received == []

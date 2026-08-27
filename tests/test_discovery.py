"""Async discovery and password retrieval, against local fakes."""

import asyncio
import ssl
import struct
from pathlib import Path

import pytest
from roombapy.discovery import ROOMBA_MESSAGE, UDP_PORT, RoombaDiscovery
from roombapy.getpassword import (
    PASSWORD_REQUEST,
    UNSUPPORTED_MAGIC,
    RoombaPassword,
)
from roombapy.roomba import RoombaConnectionError, RoombaError

# The repository's own test certificates, the same ones CI feeds mosquitto.
# Do not point this outside the repo: it then passes only on the machine that
# happens to have that directory.
CERTS = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "mosquitto"
    / "tls-certificates"
)

ROOMBA_REPLY = (
    b'{"ver":"3","hostname":"Roomba-31B8091051311850",'
    b'"robotname":"Roomba","ip":"127.0.0.1","mac":"00:11:22:33:44:55",'
    b'"sw":"2.4.17-138","sku":"R980020","nc":0,"proto":"mqtt",'
    b'"cap":{"pose":1}}'
)


class _FakeRobot(asyncio.DatagramProtocol):
    """Answers the discovery broadcast the way a robot would."""

    def __init__(self) -> None:
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport  # type: ignore[assignment]

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        if data == ROOMBA_MESSAGE and self.transport is not None:
            self.transport.sendto(ROOMBA_REPLY, addr)


@pytest.mark.asyncio
async def test_discovery_finds_a_robot() -> None:
    """A robot answering on the discovery port is decoded into RoombaInfo."""
    loop = asyncio.get_running_loop()
    robot_transport, _ = await loop.create_datagram_endpoint(
        _FakeRobot, local_addr=("127.0.0.1", UDP_PORT)
    )
    discovery = RoombaDiscovery(bind_port=0)
    try:
        found = await discovery.get("127.0.0.1", timeout=2.0)
    finally:
        await discovery.aclose()
        robot_transport.close()

    assert found is not None
    assert found.hostname == "Roomba-31B8091051311850"
    assert found.blid == "31B8091051311850"
    assert found.sku == "R980020"


@pytest.mark.asyncio
async def test_discovery_times_out_without_a_robot() -> None:
    """No answer means None, not a hang."""
    discovery = RoombaDiscovery(bind_port=0)
    try:
        async with asyncio.timeout(5):
            found = await discovery.get("127.0.0.2", timeout=0.5)
    finally:
        await discovery.aclose()
    assert found is None


async def _serve_password(payload: bytes) -> tuple[asyncio.Server, int]:
    """A TLS server that replies to the password request with ``payload``."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERTS / "test.crt", CERTS / "test.key")

    async def handle(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        request = await reader.read(len(PASSWORD_REQUEST))
        if request == PASSWORD_REQUEST:
            writer.write(payload)
            await writer.drain()
        writer.close()

    server = await asyncio.start_server(handle, "127.0.0.1", 0, ssl=context)
    return server, server.sockets[0].getsockname()[1]


@pytest.mark.asyncio
async def test_password_is_decoded() -> None:
    """The length-prefixed reply is unwrapped into the password."""
    secret = b":1:1234567890:abcdefghijklmnop"
    body = secret + b"\x00" * (35 - len(secret))
    payload = b"\xf0" + struct.pack("B", len(body)) + b"\x00" * 5 + body

    server, port = await _serve_password(payload)
    try:
        password = RoombaPassword("127.0.0.1", port=port)
        result = await password.get_password(timeout=5.0)
    finally:
        server.close()
        await server.wait_closed()

    assert result == ":1:1234567890:abcdefghijklmnop"


@pytest.mark.asyncio
async def test_cloud_only_model_returns_none() -> None:
    """The unsupported-magic reply means no local password exists."""
    server, port = await _serve_password(UNSUPPORTED_MAGIC)
    try:
        password = RoombaPassword("127.0.0.1", port=port)
        result = await password.get_password(timeout=5.0)
    finally:
        server.close()
        await server.wait_closed()

    assert result is None


@pytest.mark.asyncio
async def test_refused_connection_returns_none() -> None:
    """A closed port yields None rather than raising."""
    password = RoombaPassword("127.0.0.1", port=1)
    assert await password.get_password(timeout=2.0) is None


@pytest.mark.asyncio
async def test_unresolvable_address_fails_fast() -> None:
    """A hostname typo should not look like a robot that is switched off.

    The datagram never leaves, the error lands on error_received where
    nobody is looking, and without this the caller waits out the whole
    window for a None.
    """
    discovery = RoombaDiscovery(bind_port=0)
    try:
        with pytest.raises(RoombaConnectionError, match="Cannot resolve"):
            await discovery.get("no.such.host.invalid", timeout=5.0)
    finally:
        await discovery.aclose()


@pytest.mark.asyncio
async def test_send_without_socket_raises_a_library_error() -> None:
    """Errors from this package should be catchable as RoombaError."""
    discovery = RoombaDiscovery(bind_port=0)
    with pytest.raises(RoombaError, match="not open"):
        discovery._send("127.0.0.1")


@pytest.mark.asyncio
async def test_dead_endpoint_is_reopened() -> None:
    """A closed socket must not be handed back as if it were usable.

    asyncio closes the endpoint on a fatal socket error. Reusing the stale
    protocol left _send calling into a dead transport, which surfaced as a
    bare AttributeError out of the public API.
    """
    discovery = RoombaDiscovery(bind_port=0)
    try:
        protocol = await discovery._open()
        assert discovery._transport is not None
        discovery._transport.close()
        await asyncio.sleep(0.1)
        assert protocol.closed

        # The next call must build a fresh endpoint rather than reuse it.
        reopened = await discovery._open()
        assert reopened is not protocol
        assert not reopened.closed

        # And discovery still works rather than raising AttributeError.
        assert await discovery.get("127.0.0.1", timeout=0.5) is None
    finally:
        await discovery.aclose()

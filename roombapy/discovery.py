"""Async discovery of Roomba devices on the local network.

Same wire behaviour as the blocking implementation: a UDP broadcast of
``irobotmcs`` on port 5678, with replies parsed into ``RoombaInfo``. The
socket handling is the only thing that changed.
"""

from __future__ import annotations

import asyncio
import logging
import socket
from json import JSONDecodeError
from typing import TYPE_CHECKING, Self

from mashumaro import exceptions as merr

from roombapy.roomba import RoombaConnectionError, RoombaError
from roombapy.roomba_info import RoombaInfo, validate_hostname

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

# Discovery must hear broadcast replies, so it binds all interfaces.
UDP_BIND_ADDRESS = "0.0.0.0"  # noqa: S104
UDP_ADDRESS = "<broadcast>"
UDP_PORT = 5678
ROOMBA_MESSAGE = b"irobotmcs"
BROADCAST_COUNT = 5
DEFAULT_TIMEOUT = 5.0


class _DiscoveryProtocol(asyncio.DatagramProtocol):
    """Collects datagrams into a queue for the discovery loop to drain."""

    def __init__(self) -> None:
        """Prepare the queue replies are pushed onto."""
        self.replies: asyncio.Queue[tuple[bytes, str]] = asyncio.Queue()

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """Queue one reply."""
        self.replies.put_nowait((data, addr[0]))

    def error_received(self, exc: Exception) -> None:
        """Log transport-level errors without tearing the endpoint down."""
        logging.getLogger(__name__).debug("Discovery socket error: %s", exc)


class RoombaDiscovery:
    """Discover Roomba devices on the local network.

    The ``timeout`` arguments below are collection *windows*, not abort
    deadlines, which is why ASYNC109 is suppressed for them: discovery
    broadcasts and then gathers whatever answers within the window,
    returning normally when it closes. Wrapping the call in
    ``asyncio.timeout`` instead would cancel it and lose the replies
    already collected.
    """

    def __init__(
        self, *, port: int = UDP_PORT, bind_port: int | None = None
    ) -> None:
        """Create the discovery client; no socket is opened yet.

        ``bind_port`` defaults to ``port`` because some robots reply to the
        discovery port rather than to the source port. Tests override it so
        that a fake robot can hold the discovery port.
        """
        self.log = logging.getLogger(__name__)
        self.port = port
        self.bind_port = port if bind_port is None else bind_port
        self._transport: asyncio.DatagramTransport | None = None
        self._protocol: _DiscoveryProtocol | None = None

    async def get_all(
        self,
        timeout: float = DEFAULT_TIMEOUT,  # noqa: ASYNC109
    ) -> set[RoombaInfo]:
        """Return every Roomba that answers within ``timeout``."""
        protocol = await self._open()
        for index in range(BROADCAST_COUNT):
            self._send(UDP_ADDRESS)
            self.log.debug("Broadcast message sent: %s", index)

        robots: set[RoombaInfo] = set()
        async for info, _address in self._replies(protocol, timeout):
            robots.add(info)
        return robots

    async def get(
        self,
        ip: str,
        timeout: float = DEFAULT_TIMEOUT,  # noqa: ASYNC109
    ) -> RoombaInfo | None:
        """Return the Roomba at ``ip``, or None if it does not answer."""
        protocol = await self._open()
        await self._resolve(ip)
        self._send(ip)
        async for info, address in self._replies(protocol, timeout):
            if address == ip:
                return info
        return None

    async def aclose(self) -> None:
        """Close the socket."""
        transport, self._transport = self._transport, None
        self._protocol = None
        if transport is not None:
            transport.close()

    async def __aenter__(self) -> Self:
        """Open the socket on entry."""
        await self._open()
        return self

    async def __aexit__(self, *_exc: object) -> None:
        """Close the socket on exit."""
        await self.aclose()

    # ------------------------------------------------------------------

    async def _open(self) -> _DiscoveryProtocol:
        if self._protocol is not None:
            return self._protocol
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            _DiscoveryProtocol,
            local_addr=(UDP_BIND_ADDRESS, self.bind_port),
            allow_broadcast=True,
        )
        transport.get_extra_info("socket").setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1
        )
        self._transport = transport
        self._protocol = protocol
        self.log.debug("Socket server started, port %s", self.bind_port)
        return protocol

    async def _resolve(self, address: str) -> None:
        """Fail fast on an address that cannot be resolved.

        Without this a typo in the hostname is indistinguishable from a
        robot that is switched off: the datagram never leaves, the error
        arrives on ``error_received`` where nobody is looking, and the
        caller waits out the whole window for a ``None``.
        """
        loop = asyncio.get_running_loop()
        try:
            await loop.getaddrinfo(address, self.port, type=socket.SOCK_DGRAM)
        except OSError as err:
            msg = f"Cannot resolve {address}: {err}"
            raise RoombaConnectionError(msg) from err

    def _send(self, address: str) -> None:
        if self._transport is None:
            msg = "Discovery socket is not open"
            raise RoombaError(msg)
        self._transport.sendto(ROOMBA_MESSAGE, (address, self.port))

    async def _replies(
        self,
        protocol: _DiscoveryProtocol,
        timeout: float,  # noqa: ASYNC109
    ) -> AsyncIterator[tuple[RoombaInfo, str]]:
        """Yield decoded replies until ``timeout`` elapses without one."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while True:
            remaining = deadline - loop.time()
            if remaining <= 0:
                return
            try:
                async with asyncio.timeout(remaining):
                    raw, address = await protocol.replies.get()
            except TimeoutError:
                self.log.info("Socket timeout")
                return
            self.log.debug("Received response: %s, address: %s", raw, address)
            info = _decode_data(raw)
            if info is not None:
                yield info, address


def _decode_data(raw_response: bytes) -> RoombaInfo | None:
    """Parse one discovery reply, or None if it is not from a robot."""
    try:
        data = raw_response.decode()
    except UnicodeDecodeError:
        # Not a Roomba: routers and other devices answer the broadcast too.
        return None

    if data == ROOMBA_MESSAGE.decode():
        # Filter our own broadcast, which comes back to us.
        return None

    try:
        raw_info = RoombaInfo.from_json(data)
        validate_hostname(raw_info.hostname)
    except JSONDecodeError:
        return None
    except (
        merr.MissingField,
        merr.UnserializableDataError,
        merr.InvalidFieldValue,
        merr.MissingDiscriminatorError,
        merr.SuitableVariantNotFoundError,
    ):
        return None
    except ValueError:
        return None
    else:
        return raw_info

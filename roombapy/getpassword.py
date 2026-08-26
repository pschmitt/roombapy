"""Async retrieval of the local password from a Roomba.

The robot must be on its dock and powered on. Press and hold HOME until a
series of tones plays; release, and the Wi-Fi LED flashes. Then call
``get_password``.

Wire behaviour is unchanged from the blocking implementation: the same
request magic, the same length-prefixed reply framing, the same handling of
models that only serve the password from the cloud.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import ssl
import struct

from roombapy.tls import generate_tls_context

PASSWORD_REQUEST = bytes.fromhex("f005efcc3b2900")
UNSUPPORTED_MAGIC = bytes.fromhex("f005efcc3b2903")
DEFAULT_PORT = 8883
DEFAULT_TIMEOUT = 10.0
HEADER_LENGTH = 2
INITIAL_RESPONSE_LENGTH = 35


class RoombaPassword:
    """Retrieve the local password from a Roomba in listening mode."""

    def __init__(
        self,
        roomba_ip: str,
        *,
        port: int = DEFAULT_PORT,
        tls_context: ssl.SSLContext | None = None,
    ) -> None:
        """Store connection parameters; no I/O happens here."""
        self.roomba_ip = roomba_ip
        self.roomba_port = port
        self.log = logging.getLogger(__name__)
        self._tls_context = tls_context or generate_tls_context()

    async def get_password(
        self,
        timeout: float = DEFAULT_TIMEOUT,  # noqa: ASYNC109
    ) -> str | None:
        """Return the password, or None if the robot will not give one.

        ASYNC109 suggests the caller wrap this in ``asyncio.timeout``. That
        would raise ``TimeoutError`` where this returns ``None`` — and "the
        robot did not answer" is an ordinary outcome here, not an error: a
        robot that is not in listening mode simply stays quiet.
        """
        try:
            async with asyncio.timeout(timeout):
                reader, writer = await asyncio.open_connection(
                    self.roomba_ip, self.roomba_port, ssl=self._tls_context
                )
        except (ConnectionRefusedError, ssl.SSLError, OSError) as err:
            self.log.debug("Could not connect: %s", err)
            return None
        except TimeoutError:
            self.log.warning("Socket timeout")
            return None

        self.log.debug(
            "Connected to Roomba %s:%s", self.roomba_ip, self.roomba_port
        )
        try:
            async with asyncio.timeout(timeout):
                writer.write(PASSWORD_REQUEST)
                await writer.drain()
                raw_data = await self._read_response(reader)
        except TimeoutError:
            self.log.warning("Socket timeout")
            return None
        except OSError as err:
            self.log.debug("Socket error: %s", err)
            return None
        finally:
            writer.close()
            with contextlib.suppress(OSError, ssl.SSLError):
                await writer.wait_closed()

        if not raw_data:
            return None
        return _decode_password(raw_data)

    async def _read_response(self, reader: asyncio.StreamReader) -> bytes:
        """Read until the length prefix says the reply is complete."""
        raw_data = b""
        response_length = INITIAL_RESPONSE_LENGTH
        while len(raw_data) < response_length + HEADER_LENGTH:
            response = await reader.read(1024)
            if not response:
                break
            if response == UNSUPPORTED_MAGIC:
                # This model serves its password from the cloud only.
                return b""
            raw_data += response
            if len(raw_data) >= HEADER_LENGTH:
                response_length = struct.unpack("B", raw_data[1:2])[0]
        return raw_data


def _decode_password(data: bytes) -> str:
    return str(data[7:].decode().rstrip("\x00"))

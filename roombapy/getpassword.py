"""The class helps you to get password for your Roomba."""

from __future__ import annotations

import logging
import socket
import struct

from roombapy.remote_client import generate_tls_context

PASSWORD_REQUEST = bytes.fromhex("f005efcc3b2900")
UNSUPPORTED_MAGIC = bytes.fromhex("f005efcc3b2903")


class RoombaPassword:
    """Main class to get a password."""

    roomba_ip: str
    roomba_port: int = 8883
    server_socket: socket.socket
    log: logging.Logger

    def __init__(self, roomba_ip: str) -> None:
        """Init default values."""
        self.roomba_ip = roomba_ip
        self.server_socket = _get_socket()
        self.log = logging.getLogger(__name__)

    """
    Roomba have to be on Home Base powered on.
    Press and hold HOME button until you hear series of tones.
    Release button, Wi-Fi LED should be flashing
    After that execute get_password method
    """

    def get_password(self) -> str | None:
        """Get password for roomba."""
        try:
            self._connect()
        except ConnectionRefusedError:
            return None
        self._send_message()
        response = self._get_response()
        if response:
            return _decode_password(response)
        return None

    def _connect(self) -> None:
        self.server_socket.connect((self.roomba_ip, self.roomba_port))
        self.log.debug(
            "Connected to Roomba %s:%s", self.roomba_ip, self.roomba_port
        )

    def _send_message(self) -> None:
        self.server_socket.send(PASSWORD_REQUEST)
        self.log.debug("Message sent")

    def _get_response(self) -> bytes | None:
        try:
            raw_data = b""
            response_length = 35
            while True:
                if len(raw_data) >= response_length + 2:
                    break

                response = self.server_socket.recv(1024)

                if len(response) == 0:
                    break

                if response == UNSUPPORTED_MAGIC:
                    # Password for this model can be obtained only from cloud
                    break

                raw_data += response
                if len(raw_data) >= 2:
                    response_length = struct.unpack("B", raw_data[1:2])[0]
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except socket.timeout:
            self.log.warning("Socket timeout")
            return None
        except OSError as e:
            self.log.debug("Socket error: %s", e)
            return None
        else:
            return raw_data


def _decode_password(data: bytes) -> str:
    return str(data[7:].decode().rstrip("\x00"))


def _get_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(10)
    context = generate_tls_context()
    return context.wrap_socket(server_socket)

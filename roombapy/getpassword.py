"""The class helps you to get password for your Roomba."""

import logging
import socket
import struct

from roombapy.remote_client import generate_tls_context


class RoombaPassword:
    """Main class to get a password."""

    roomba_ip: str
    roomba_port: int = 8883
    message: bytes
    server_socket: socket.socket
    log: logging.Logger

    def __init__(self, roomba_ip: str):
        """Init default values."""
        self.roomba_ip = roomba_ip
        self.message = bytes.fromhex("f005efcc3b2900")
        self.server_socket = _get_socket()
        self.log = logging.getLogger(__name__)

    """
    Roomba have to be on Home Base powered on.
    Press and hold HOME button until you hear series of tones.
    Release button, Wi-Fi LED should be flashing
    After that execute get_password method
    """

    def get_password(self):
        """Get password for roomba."""
        self._connect()
        self._send_message()
        response = self._get_response()
        return _decode_password(response)

    def _connect(self):
        self.server_socket.connect((self.roomba_ip, self.roomba_port))
        self.log.debug(
            "Connected to Roomba %s:%s", self.roomba_ip, self.roomba_port
        )

    def _send_message(self):
        self.server_socket.send(self.message)
        self.log.debug("Message sent")

    def _get_response(self):
        try:
            raw_data = b""
            response_length = 35
            while True:
                if len(raw_data) >= response_length + 2:
                    break

                response = self.server_socket.recv(1024)

                if len(response) == 0:
                    break

                raw_data += response
                if len(raw_data) >= 2:
                    response_length = struct.unpack("B", raw_data[1:2])[0]
            self.server_socket.close()
            return raw_data
        except socket.timeout:
            self.log.warning("Socket timeout")
            return None
        except socket.error as e:
            self.log.debug("Socket error", e)
            return None


def _decode_password(data):
    return str(data[7:].decode().rstrip("\x00"))


def _get_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(10)
    context = generate_tls_context()
    return context.wrap_socket(server_socket)

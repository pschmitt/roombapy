"""Module for discovering Roomba devices on the local network."""

from __future__ import annotations

import logging
import socket

from mashumaro import exceptions as merr
from orjson import JSONDecodeError

from roombapy.roomba_info import RoombaInfo, validate_hostname


class RoombaDiscovery:
    """Class for discovering Roomba devices on the local network."""

    udp_bind_address = ""
    udp_address = "<broadcast>"
    udp_port = 5678
    roomba_message = "irobotmcs"
    amount_of_broadcasted_messages = 5
    server_socket: socket.socket
    log: logging.Logger

    def __init__(self) -> None:
        """Initialize the discovery class."""
        self.server_socket = _get_socket()
        self.log = logging.getLogger(__name__)

    def get_all(self) -> set[RoombaInfo]:
        """Get all Roomba devices on the local network."""
        self._start_server()
        self._broadcast_message(self.amount_of_broadcasted_messages)
        robots = set()
        while True:
            response = self._get_response()
            if response:
                robots.add(response)
            else:
                break
        return robots

    def get(self, ip: str) -> RoombaInfo | None:
        """Get Roomba device with the specified IP address."""
        self._start_server()
        self._send_message(ip)
        return self._get_response(ip)

    def _get_response(self, ip: str | None = None) -> RoombaInfo | None:
        """Get a response from the Roomba device."""
        try:
            while True:
                raw_response, addr = self.server_socket.recvfrom(1024)
                if ip is not None and addr[0] != ip:
                    continue
                self.log.debug(
                    "Received response: %s, address: %s", raw_response, addr
                )
                response = _decode_data(raw_response)
                if not response:
                    continue
                return response
        except socket.timeout:
            self.log.info("Socket timeout")
            return None

    def _broadcast_message(self, amount: int) -> None:
        for i in range(amount):
            self.server_socket.sendto(
                self.roomba_message.encode(), (self.udp_address, self.udp_port)
            )
            self.log.debug("Broadcast message sent: %s", i)

    def _send_message(self, udp_address: str) -> None:
        self.server_socket.sendto(
            self.roomba_message.encode(), (udp_address, self.udp_port)
        )
        self.log.debug("Message sent")

    def _start_server(self) -> None:
        self.server_socket.bind((self.udp_bind_address, self.udp_port))
        self.log.debug("Socket server started, port %s", self.udp_port)


def _decode_data(raw_response: bytes) -> RoombaInfo | None:
    try:
        data = raw_response.decode()
    except UnicodeDecodeError:
        # Unknown ND response (routers, etc.)
        return None

    if data == RoombaDiscovery.roomba_message:
        # Filter our own messages
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


def _get_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.settimeout(5)
    return server_socket

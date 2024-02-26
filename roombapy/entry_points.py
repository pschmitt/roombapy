"""Entry points for the roombapy package."""
import logging
import sys

from roombapy import RoombaConnectionError, RoombaFactory
from roombapy.discovery import RoombaDiscovery
from roombapy.getpassword import RoombaPassword

LOGGER = logging.getLogger(__name__)


def discovery():
    """Discover Roomba devices on the local network."""
    roomba_ip = _get_ip_from_arg()

    roomba_discovery = RoombaDiscovery()
    if roomba_ip is not None:
        LOGGER.info(roomba_discovery.get(roomba_ip))
        return

    robots_info = roomba_discovery.get_all()
    for robot in robots_info:
        LOGGER.info(robot)


def password():
    """Get password for a Roomba device."""
    roomba_ip = _get_ip_from_arg()
    _validate_ip(roomba_ip)
    _wait_for_input()

    roomba_discovery = RoombaDiscovery()
    roomba_info = roomba_discovery.get(roomba_ip)
    _validate_roomba_info(roomba_info)

    roomba_password = RoombaPassword(roomba_ip)
    found_password = roomba_password.get_password()
    roomba_info.password = found_password
    LOGGER.info(roomba_info)


def connect():
    """Connect to a Roomba device."""
    roomba_ip = _get_ip_from_arg()
    _validate_ip(roomba_ip)

    roomba_password = _get_password_from_arg()
    _validate_password(roomba_password)

    roomba_discovery = RoombaDiscovery()
    roomba_info = roomba_discovery.get(roomba_ip)
    _validate_roomba_info(roomba_info)

    roomba = RoombaFactory.create_roomba(
        roomba_info.ip, roomba_info.blid, roomba_password
    )
    roomba.register_on_message_callback(lambda msg: LOGGER.info(msg))
    roomba.connect()

    while True:
        pass


class ValidationError(Exception):
    """Validation error."""

    def __init__(self, *, field: str) -> None:
        """Initialize the exception."""
        super().__init__(f"{field} cannot be null")


def _validate_ip(ip):
    if ip is None:
        raise ValidationError(field="IP")


def _validate_password(ip):
    if ip is None:
        raise ValidationError(field="Password")


def _validate_roomba_info(roomba_info):
    if roomba_info is None:
        msg = "cannot find roomba"
        raise RoombaConnectionError(msg)


def _wait_for_input():
    LOGGER.info(
        "Roomba have to be on Home Base powered on.\n"
        "Press and hold HOME button until you hear series of tones.\n"
        "Release button, Wi-Fi LED should be flashing"
    )
    input("Press Enter to continue...")


def _get_ip_from_arg():
    if len(sys.argv) < 2:
        return None
    return str(sys.argv[1])


def _get_password_from_arg():
    if len(sys.argv) < 3:
        return None
    return str(sys.argv[2])

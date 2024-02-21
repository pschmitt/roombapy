from __future__ import annotations

import sys

from roombapy import RoombaFactory, RoombaInfo
from roombapy.discovery import RoombaDiscovery
from roombapy.getpassword import RoombaPassword


def discovery() -> None:
    roomba_ip = _get_ip_from_arg()
    roomba_discovery = RoombaDiscovery()
    if roomba_ip is not None:
        print(roomba_discovery.find(roomba_ip))
        return

    robots_info = roomba_discovery.find()
    if isinstance(robots_info, set):
        for robot in robots_info:
            print(robot)
    else:
        print(robots_info)


def password() -> None:
    roomba_ip = _get_ip_from_arg()
    _validate_ip(roomba_ip)
    _wait_for_input()

    roomba_discovery = RoombaDiscovery()
    roomba_info = roomba_discovery.find(roomba_ip)
    assert roomba_info is not None
    _validate_roomba_info(roomba_info)

    info = roomba_info
    if isinstance(roomba_info, set):
        info = next(iter(roomba_info))

    assert isinstance(info, RoombaInfo)

    roomba_password = RoombaPassword(info.ip)
    found_password = roomba_password.get_password()
    info.password = found_password
    print(info)


def connect() -> None:
    roomba_ip = _get_ip_from_arg()
    _validate_ip(roomba_ip)

    roomba_password = _get_password_from_arg()
    _validate_password(roomba_password)

    roomba_discovery = RoombaDiscovery()
    roomba_info = roomba_discovery.find(roomba_ip)
    assert roomba_info is not None
    _validate_roomba_info(roomba_info)

    info = roomba_info
    if isinstance(roomba_info, set):
        info = next(iter(roomba_info))

    assert isinstance(info, RoombaInfo)
    assert roomba_password

    roomba = RoombaFactory.create_roomba(info.ip, info.blid, roomba_password)
    roomba.register_on_message_callback(lambda msg: print(msg))
    roomba.connect()

    while True:
        pass


def _validate_ip(ip: str | None) -> None:
    if ip is None:
        raise Exception("ip cannot be null")


def _validate_password(ip: str | None) -> None:
    if ip is None:
        raise Exception("password cannot be null")


def _validate_roomba_info(
    roomba_info: RoombaInfo | set[RoombaInfo] | None,
) -> None:
    if roomba_info is None:
        raise Exception("cannot find roomba")


def _wait_for_input() -> None:
    print(
        "Roomba have to be on Home Base powered on.\n"
        "Press and hold HOME button until you hear series of tones.\n"
        "Release button, Wi-Fi LED should be flashing"
    )
    input("Press Enter to continue...")


def _get_ip_from_arg() -> str | None:
    if len(sys.argv) < 2:
        return None
    return str(sys.argv[1])


def _get_password_from_arg() -> str | None:
    if len(sys.argv) < 3:
        return None
    return str(sys.argv[2])

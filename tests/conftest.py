"""Tools and fixtures for tests."""
from dataclasses import dataclass

import pytest
from roombapy import Roomba, RoombaFactory

ROOMBA_CONFIG = {
    "host": "127.0.0.1",
    "username": "test",
    "password": "test",
    "name": "Roomba",
    "continuous": True,
    "delay": 120,
}


@dataclass
class Message:
    """MQTT-like message."""

    topic: str
    payload: bytes
    qos: str = "qos"


@pytest.fixture()
def roomba() -> Roomba:
    """Mock for robot."""
    return RoombaFactory.create_roomba(
        address=ROOMBA_CONFIG["host"],
        blid=ROOMBA_CONFIG["username"],
        password=ROOMBA_CONFIG["password"],
        continuous=ROOMBA_CONFIG["continuous"],
        delay=ROOMBA_CONFIG["delay"],
    )


@pytest.fixture()
def broken_roomba():
    """Mock for robot with broken credentials."""
    return RoombaFactory.create_roomba(
        address=ROOMBA_CONFIG["host"],
        blid="wrong",
        password=ROOMBA_CONFIG["password"],
        continuous=ROOMBA_CONFIG["continuous"],
        delay=ROOMBA_CONFIG["delay"],
    )

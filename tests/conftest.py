"""Tools and fixtures for tests."""
from dataclasses import dataclass

import paho.mqtt.client as mqtt
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


def as_message(payload: bytes, *, topic: bytes = b"test") -> mqtt.MQTTMessage:
    """Craft MQTT message from bytes."""
    message = mqtt.MQTTMessage(topic=topic)
    message.payload = payload
    return message


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

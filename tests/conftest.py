"""Tools and fixtures for tests."""

from dataclasses import dataclass

import paho.mqtt.client as mqtt
import pytest
from roombapy import Roomba, RoombaFactory

ROOMBA_HOST = "127.0.0.1"
ROOMBA_USERNAME = "test"
ROOMBA_PASSWORD = "test"
ROOMBA_NAME = "Roomba"
ROOMBA_CONTINUOUS = True
ROOMBA_DELAY = 120


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
        address=ROOMBA_HOST,
        blid=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        continuous=ROOMBA_CONTINUOUS,
        delay=ROOMBA_DELAY,
    )


@pytest.fixture()
def broken_roomba() -> Roomba:
    """Mock for robot with broken credentials."""
    return RoombaFactory.create_roomba(
        address=ROOMBA_HOST,
        blid="wrong",
        password=ROOMBA_PASSWORD,
        continuous=ROOMBA_CONTINUOUS,
        delay=ROOMBA_DELAY,
    )


@pytest.fixture()
def empty_mqtt_client() -> mqtt.Client:
    """Mock for mqtt Client."""
    return mqtt.Client(client_id="test")

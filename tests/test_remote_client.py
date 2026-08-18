"""Test the Roomba remote client."""

import logging

import pytest
from roombapy.remote_client import RoombaRemoteClient

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME


@pytest.fixture
def remote_client() -> RoombaRemoteClient:
    """Remote client that has never been connected."""
    return RoombaRemoteClient(
        address=ROOMBA_HOST, blid=ROOMBA_USERNAME, password=ROOMBA_PASSWORD
    )


def test_subscribe_without_connection_is_logged(
    remote_client: RoombaRemoteClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Report a SUBSCRIBE that never left the client."""
    with caplog.at_level(logging.ERROR):
        remote_client.subscribe("test")

    assert "Failed to subscribe to topic test" in caplog.text
    assert "not currently connected" in caplog.text


def test_publish_without_connection_is_logged(
    remote_client: RoombaRemoteClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Report a PUBLISH that never left the client."""
    with caplog.at_level(logging.ERROR):
        remote_client.publish("cmd", '{"command": "start"}')

    assert "Failed to publish to topic cmd" in caplog.text
    assert "not currently connected" in caplog.text

"""Test for the discovery module."""
from roombapy.discovery import RoombaDiscovery


def test_discovery_with_wrong_msg() -> None:
    """Test discovery with wrong message."""
    discovery = RoombaDiscovery()
    discovery.roomba_message = "test"
    response = discovery.get_all()

    assert not response

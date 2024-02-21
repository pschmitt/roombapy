"""Test for the discovery module."""
from roombapy.discovery import RoombaDiscovery


class TestDiscovery:
    """Test the discovery module."""

    def test_discovery_with_wrong_msg(self):
        """Test discovery with wrong message."""
        # given
        discovery = RoombaDiscovery()

        # when
        discovery.roomba_message = "test"
        response = discovery.find()

        # then
        assert not response

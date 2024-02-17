from roombapy.discovery import RoombaDiscovery


def test_discovery_with_wrong_msg():
    discovery = RoombaDiscovery()
    discovery.roomba_message = "test"
    response = discovery.find()

    assert not response

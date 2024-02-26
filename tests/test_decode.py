"""Test the decoding of the Roomba discovery messages."""
from roombapy.discovery import RoombaDiscovery, _decode_data

TEST_ROOMBA_INFO = """
{
    "hostname": "hostname_placeholder",
    "sw": "1.2.3",
    "ip": "192.168.0.2",
    "mac": "aa:bb:cc:dd:ee:ff",
    "robotname": "test",
    "sku": "123",
    "cap":{}
}
"""


def test_skip_garbage() -> None:
    """Test skipping garbage data."""
    assert _decode_data(b"\x0f\x00\xff\xf0") is None


def test_skip_own_messages() -> None:
    """Test skipping own messages."""
    assert _decode_data(RoombaDiscovery.roomba_message.encode()) is None


def test_skip_broken_json() -> None:
    """Test skipping broken JSON."""
    assert _decode_data(b'{"test": 1') is None


def test_skip_unknown_json() -> None:
    """Test skipping unknown JSON."""
    assert _decode_data(b'{"test": 1}') is None


def test_skip_unknown_hostname() -> None:
    """Test skipping unknown hostname."""
    assert _decode_data(b'{"hostname": "test"}') is None
    assert _decode_data(TEST_ROOMBA_INFO.encode()) is None


def test_skip_hostnames_without_blid() -> None:
    """Test skipping hostnames without BLID."""
    decoded = _decode_data(
        TEST_ROOMBA_INFO.replace("hostname_placeholder", "iRobot-").encode()
    )
    assert decoded is None


def test_allow_approved_hostnames() -> None:
    """Test allowing approved hostnames."""
    blid = "test"
    for hostname in [f"Roomba-{blid}", f"iRobot-{blid}"]:
        decoded = _decode_data(
            TEST_ROOMBA_INFO.replace("hostname_placeholder", hostname).encode()
        )
        assert decoded is not None
        assert decoded.hostname == hostname
        assert decoded.blid == blid

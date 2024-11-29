"""Test the decoding of the Roomba messages."""

from roombapy.roomba import _decode_payload


def test_skip_garbage() -> None:
    """Skip garbage data in payload."""
    assert _decode_payload(b"\x00") is None


def test_skip_broken_json() -> None:
    """Skip broken JSON."""
    assert _decode_payload(b"[") is None
    assert _decode_payload(b"{") is None


def test_skip_non_object_json() -> None:
    """Allow only objects in messages."""
    assert _decode_payload(b"[]") is None
    assert _decode_payload(b"12") is None


def test_allow_empty_json() -> None:
    """Allow empty objects."""
    assert _decode_payload(b"{}") == {}


def test_allow_valid_json() -> None:
    """Properly decode valid JSON object."""
    payload = b"""
    {"state": {"reported": {"signal": {"rssi": -45, "snr": 18, "noise": -63}}}}
    """
    decoded = {
        "state": {
            "reported": {"signal": {"rssi": -45, "snr": 18, "noise": -63}}
        }
    }
    assert _decode_payload(payload) == decoded

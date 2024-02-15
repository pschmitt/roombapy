from roombapy.roomba import _decode_payload


def test_skip_garbage():
    assert _decode_payload(b"\x00") is None


def test_skip_broken_json():
    assert _decode_payload(b"[") is None
    assert _decode_payload(b"{") is None


def test_skip_non_object_json():
    assert _decode_payload(b"[]") is None
    assert _decode_payload(b"12") is None


def test_allow_empty_json():
    assert _decode_payload(b"{}") == {}


def test_allow_valid_json():
    payload = b"""
    {"state": {"reported": {"signal": {"rssi": -45, "snr": 18, "noise": -63}}}}
    """
    decoded = {
        "state": {
            "reported": {"signal": {"rssi": -45, "snr": 18, "noise": -63}}
        }
    }
    assert _decode_payload(payload) == decoded

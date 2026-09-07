"""Test the decoding of the Roomba messages."""

import asyncio

from roombapy.roomba import RobotPreference, RoombaClient, _decode_payload


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


# ---------------------------------------------------------------------
# Preference payloads.
#
# Tested here rather than in test_commands.py because the question is
# what gets BUILT, not what a broker does with it -- these need no
# connection, and a grouped write is exactly the case where the shape
# of the payload is the whole point.
# ---------------------------------------------------------------------


class _Capturing(RoombaClient):
    """A client that records publishes instead of making them."""

    def __init__(self) -> None:
        self.published: list[tuple[str, str]] = []

    async def _publish(self, topic: str, payload: str) -> None:
        self.published.append((topic, payload))


def test_a_preference_group_goes_out_as_one_message() -> None:
    """Keep a preference group in one message.

    Some preferences are read by one firmware handler that needs its
    whole group present, and a message carrying half of one is dropped
    without a word -- no error, no echo, nothing on the wire. Two
    single-key messages therefore set nothing at all.
    """
    client = _Capturing()
    asyncio.run(
        client.set_preferences({"noAutoPasses": True, "twoPass": True})
    )

    assert len(client.published) == 1, "the group must not be split"
    topic, payload = client.published[0]
    assert topic == "delta"
    assert payload == '{"state":{"noAutoPasses":true,"twoPass":true}}'


def test_boolean_strings_are_coerced_in_a_group_too() -> None:
    """Coerce boolean strings in the plural form too.

    Callers have passed str(True) for years, and routing the single
    form through the plural one must not change that for either.
    """
    client = _Capturing()
    asyncio.run(
        client.set_preferences({"carpetBoost": "false", "vacHigh": "TRUE"})
    )

    assert (
        client.published[0][1]
        == '{"state":{"carpetBoost":false,"vacHigh":true}}'
    )


def test_a_single_preference_still_sends_a_single_key() -> None:
    """The negative control for the delegation.

    `set_preference()` now routes through `set_preferences()`. An
    ungrouped setting must keep its exact previous payload -- a stray
    extra key would be a behaviour change for every existing caller.
    """
    client = _Capturing()
    asyncio.run(client.set_preference("openOnly", setting=True))

    assert client.published == [("delta", '{"state":{"openOnly":true}}')]


def test_a_boolean_setting_is_accepted_by_the_annotation() -> None:
    """`RobotPreference` is `str | int | dict[str, int]`, with no `bool`.

    A review flagged that as breaking type-checking for callers passing
    True. It does not: `bool` is a subclass of `int`, so `True` is
    already a valid `RobotPreference` and mypy --strict accepts it.

    Pinned as a runtime check rather than argued in a comment, because
    the observation is easy to make again and the answer is not obvious
    from reading the alias.
    """
    assert issubclass(bool, int)

    # And the alias really is the one under discussion.
    assert "bool" not in str(RobotPreference)

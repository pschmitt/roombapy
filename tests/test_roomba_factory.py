"""Test the RoombaFactory class."""

import pytest
from roombapy import RoombaFactory


def test_roomba_factory() -> None:
    """Test RoombaFactory with dummy params."""
    roomba = RoombaFactory.create_roomba(
        address="dummy",
        blid="dummy",
        password="dummy",
    )

    assert roomba.conn_mode == "continuous"
    assert roomba.delay == 1


def test_roomba_factory_compatibility() -> None:
    """Test RoombaFactory compatibility mapping."""
    roomba = RoombaFactory.create_roomba(
        address="dummy",
        blid="dummy",
        password="dummy",
        continuous=False,
        delay=60,
    )

    assert roomba.conn_mode == "periodic"
    assert roomba.delay == 60


def test_roomba_factory_adhoc() -> None:
    """Test RoombaFactory with adhoc connection mode."""
    roomba = RoombaFactory.create_roomba(
        address="dummy",
        blid="dummy",
        password="dummy",
        mode="adhoc",
    )

    assert roomba.conn_mode == "adhoc"
    assert roomba.delay == 1


def test_roomba_factory_throws_exclusive() -> None:
    """Test RoombaFactory with mutualy exclusive parameters."""
    with pytest.raises(
        ValueError,
        match="The continuous and mode parameters are mutually exclusive!",
    ):
        _roomba = RoombaFactory.create_roomba(
            address="dummy",
            blid="dummy",
            password="dummy",
            mode="adhoc",
            continuous=True,
        )


def test_roomba_factory_throws_invalid_mode() -> None:
    """Test RoombaFactory with invalid connection mode."""
    with pytest.raises(
        ValueError,
        match="The mode parameter does not contain a recognized value!",
    ):
        _roomba = RoombaFactory.create_roomba(
            address="dummy",
            blid="dummy",
            password="dummy",
            mode="temporary",
        )

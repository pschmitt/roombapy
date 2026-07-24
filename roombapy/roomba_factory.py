"""Factory class to create Roomba class to control your robot."""

from roombapy import Roomba
from roombapy.const import _SENTINEL_UNSET, CONNECTION_MODES
from roombapy.remote_client import RoombaRemoteClient


class RoombaFactory:
    """Allows you to create Roomba class to control your robot."""

    @staticmethod
    def create_roomba(
        address: str,
        blid: str,
        password: str,
        *,
        continuous: bool | object = _SENTINEL_UNSET,
        mode: str | object = _SENTINEL_UNSET,
        delay: int = 1,
    ) -> Roomba:
        """Create a Roomba instance."""
        if continuous is not _SENTINEL_UNSET and mode is not _SENTINEL_UNSET:
            msg = "The continuous and mode parameters are mutually exclusive!"
            raise ValueError(msg)

        if continuous is not _SENTINEL_UNSET and mode is _SENTINEL_UNSET:
            # backwards compatibility logic:
            #   - continuous=True  --> mode="continuous"
            #   - continuous=False --> mode="periodic"
            mode = "continuous" if continuous is True else "periodic"

        if mode is _SENTINEL_UNSET:
            mode = "continuous"

        if mode not in CONNECTION_MODES:
            msg = "The mode parameter does not contain a recognized value!"
            raise ValueError(msg)

        remote_client = _create_remote_client(address, blid, password)
        return Roomba(remote_client, mode=mode, delay=delay)


def _create_remote_client(
    address: str,
    blid: str,
    password: str,
) -> RoombaRemoteClient:
    return RoombaRemoteClient(address=address, blid=blid, password=password)

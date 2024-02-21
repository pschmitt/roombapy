from roombapy import Roomba
from roombapy.remote_client import RoombaRemoteClient


class RoombaFactory:
    """Allows you to create Roomba class to control your robot."""

    @staticmethod
    def create_roomba(
        address: str,
        blid: str,
        password: str,
        continuous: bool = True,
        delay: int = 1,
    ) -> Roomba:
        remote_client = RoombaFactory._create_remote_client(
            address, blid, password
        )
        return Roomba(remote_client, continuous=continuous, delay=delay)

    @staticmethod
    def _create_remote_client(
        address: str, blid: str, password: str
    ) -> RoombaRemoteClient:
        return RoombaRemoteClient(address=address, blid=blid, password=password)

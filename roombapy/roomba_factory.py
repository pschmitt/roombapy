from roombapy.protocols import IRoombaFactory
from roombapy.remote_client import RoombaRemoteClient
from roombapy.roomba import Roomba


class RoombaFactory(IRoombaFactory):
    @staticmethod
    def create_roomba(
        address: str,
        blid: str,
        password: str,
        continuous: bool = True,
        delay: int = 1,
    ) -> Roomba:
        remote_client = _create_remote_client(address, blid, password)
        return Roomba(remote_client, continuous, delay)


def _create_remote_client(
    address: str,
    blid: str,
    password: str,
) -> RoombaRemoteClient:
    return RoombaRemoteClient(address=address, blid=blid, password=password)

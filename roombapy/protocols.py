"""Protocols for HA to ensure guarantees for strict API compatibility"""

from typing import Optional, Protocol, Set

from roombapy.roomba import Roomba
from roombapy.roomba_info import RoombaInfo


class IRoombaDiscovery(Protocol):
    def __init__(self) -> None:
        """
        Initialize helper for UDP discovery
        """
        ...

    def get(self, ip: str) -> Optional[RoombaInfo]:
        """Get information about robot by specified IP"""
        ...

    def get_all(self) -> Set[RoombaInfo]:
        """
        Get information about all robots
        """
        ...


class IRoombaFactory(Protocol):
    @staticmethod
    def create_roomba(
        address: str,
        blid: str,
        password: str,
        continuous: bool = True,
        delay: int = 1,
    ) -> Roomba:
        """
        Create Roomba class to control your robot
        """
        ...

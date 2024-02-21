import asyncio
from asyncio import BaseEventLoop

import pytest
from roombapy import Roomba

from tests import abstract_test_roomba


class TestRoombaIntegration(abstract_test_roomba.AbstractTestRoomba):
    @pytest.mark.asyncio()
    async def test_roomba_connect(self, event_loop: BaseEventLoop) -> None:
        # given
        roomba = self.get_default_roomba()

        # when
        is_connected = await self.roomba_connect(roomba, event_loop)
        await self.roomba_disconnect(roomba, event_loop)

        # then
        assert is_connected

    @pytest.mark.asyncio()
    async def test_roomba_connect_error(
        self, event_loop: BaseEventLoop
    ) -> None:
        # given
        roomba = self.get_default_roomba(blid="wrong")

        # when
        is_connected = await self.roomba_connect(roomba, event_loop)

        # then
        assert not is_connected

    async def roomba_connect(self, roomba: Roomba, loop: BaseEventLoop) -> bool:
        await loop.run_in_executor(None, roomba.connect)
        await asyncio.sleep(1)
        return roomba.roomba_connected

    async def roomba_disconnect(
        self, roomba: Roomba, loop: BaseEventLoop
    ) -> None:
        await loop.run_in_executor(None, roomba.disconnect)

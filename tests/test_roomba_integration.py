"""Test Roomba integration with the real device."""
import asyncio

import pytest

from tests import abstract_test_roomba


class TestRoombaIntegration(abstract_test_roomba.AbstractTestRoomba):
    """Test Roomba integration with the real device."""

    @pytest.mark.asyncio()
    async def test_roomba_connect(self, event_loop):
        """Test Roomba connect."""
        # given
        roomba = self.get_default_roomba()

        # when
        is_connected = await self.roomba_connect(roomba, event_loop)
        await self.roomba_disconnect(roomba, event_loop)

        # then
        assert is_connected

    @pytest.mark.asyncio()
    async def test_roomba_connect_error(self, event_loop):
        """Test Roomba connect error."""
        # given
        roomba = self.get_default_roomba(blid="wrong")

        # when
        is_connected = await self.roomba_connect(roomba, event_loop)

        # then
        assert not is_connected

    async def roomba_connect(self, roomba, loop):
        """Connect to the Roomba."""
        await loop.run_in_executor(None, roomba.connect)
        await asyncio.sleep(1)
        return roomba.roomba_connected

    async def roomba_disconnect(self, roomba, loop):
        """Disconnect from the Roomba."""
        await loop.run_in_executor(None, roomba.disconnect)

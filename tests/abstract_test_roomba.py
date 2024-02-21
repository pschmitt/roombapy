
import paho.mqtt.client as mqtt
from roombapy import Roomba, RoombaFactory

ROOMBA_CONFIG = {
    "host": "127.0.0.1",
    "username": "test",
    "password": "test",
    "name": "Roomba",
    "continuous": True,
    "delay": 120,
}


class AbstractTestRoomba:
    @staticmethod
    def get_default_roomba(
        address: str = "127.0.0.1",
        blid: str = "test",
        password: str = "test",
        continuous: bool = True,
        delay: int = 120,
    ) -> Roomba:
        return RoombaFactory.create_roomba(
            address=address,
            blid=blid,
            password=password,
            continuous=continuous,
            delay=delay,
        )

    @staticmethod
    def get_message(topic: bytes, payload: bytes) -> mqtt.MQTTMessage:
        message = mqtt.MQTTMessage(topic=topic)
        message.payload = payload
        return message

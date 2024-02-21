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
        address=ROOMBA_CONFIG["host"],
        blid=ROOMBA_CONFIG["username"],
        password=ROOMBA_CONFIG["password"],
        continuous=ROOMBA_CONFIG["continuous"],
        delay=ROOMBA_CONFIG["delay"],
    ) -> Roomba:
        return RoombaFactory.create_roomba(
            address=address,
            blid=blid,
            password=password,
            continuous=continuous,
            delay=delay,
        )

    @staticmethod
    def get_message(topic, payload):
        class Message:
            pass

        message = Message
        message.topic = topic
        message.payload = payload
        message.qos = "qos"

        return message

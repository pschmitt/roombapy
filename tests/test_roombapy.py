import unittest
from roomba import Roomba


class RoombaTest(unittest.TestCase):

    def test_roomba_create(self):
        roomba = Roomba(
            address="host",
            blid="username",
            password="password",
            cert_name="certificate",
            continuous=False,
            delay=1,
        )
        self.assertIsNotNone(roomba)

    def test_roomba_with_client(self):
        roomba = Roomba(
            address="host",
            blid="username",
            password="password",
            cert_name="certificate",
            continuous=True,
            delay=10
        )
        client = RoombaClientStub()
        roomba.set_client(client)
        roomba.connect()
        self.assertIsNotNone(roomba)


class RoombaClientStub:
    on_message = None
    on_connect = None
    on_disconnect = None
    on_publish = None
    on_subscribe = None

    def connect(self):
        print('connect')
        return True

    def disconnect(self):
        print('disconnect')

    def reconnect(self):
        print('reconnect')

    def loop_start(self):
        print('loop_start')

    def loop_stop(self):
        print('loop_stop')


if __name__ == '__main__':
    unittest.main()

"""Roomba remote client."""
import logging
import ssl
from functools import cache

import paho.mqtt.client as mqtt

from roombapy.const import MQTT_ERROR_MESSAGES

MAX_CONNECTION_RETRIES = 3


@cache
def generate_tls_context() -> ssl.SSLContext:
    """Generate TLS context.

    We only want to do this once ever because it's expensive.
    """
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.set_ciphers("DEFAULT:!DH")
    ssl_context.load_default_certs()
    # ssl.OP_LEGACY_SERVER_CONNECT is only available in Python 3.12a4+
    ssl_context.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
    return ssl_context


class RoombaRemoteClient:
    """Roomba remote client."""

    address = None
    port = None
    blid = None
    password = None
    log = None
    was_connected = False
    on_connect = None
    on_disconnect = None

    def __init__(self, address, blid, password, port=8883):
        """Initialize the Roomba remote client."""
        self.address = address
        self.blid = blid
        self.password = password
        self.port = port
        self.log = logging.getLogger(__name__)
        self.mqtt_client = self._get_mqtt_client()

    def set_on_message(self, on_message):
        """Set the on message callback."""
        self.mqtt_client.on_message = on_message

    def set_on_connect(self, on_connect):
        """Set the on connect callback."""
        self.on_connect = on_connect

    def set_on_publish(self, on_publish):
        """Set the on publish callback."""
        self.mqtt_client.on_publish = on_publish

    def set_on_subscribe(self, on_subscribe):
        """Set the on subscribe callback."""
        self.mqtt_client.on_subscribe = on_subscribe

    def set_on_disconnect(self, on_disconnect):
        """Set the on disconnect callback."""
        self.on_disconnect = on_disconnect

    def connect(self):
        """Connect to the Roomba."""
        attempt = 1
        while attempt <= MAX_CONNECTION_RETRIES:
            self.log.info(
                "Connecting to %s, attempt %s of %s",
                self.address,
                attempt,
                MAX_CONNECTION_RETRIES,
            )
            try:
                self._open_mqtt_connection()
            except Exception:
                self.log.exception("Can't connect to %s", self.address)
            else:
                return True
            attempt += 1

        self.log.error("Unable to connect to %s", self.address)
        return False

    def disconnect(self):
        """Disconnect from the Roomba."""
        self.mqtt_client.disconnect()

    def subscribe(self, topic):
        """Subscribe to a topic."""
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, payload):
        """Publish a message to a topic."""
        self.mqtt_client.publish(topic, payload)

    def _open_mqtt_connection(self):
        if not self.was_connected:
            self.mqtt_client.connect(self.address, self.port)
            self.was_connected = True
        else:
            self.mqtt_client.loop_stop()
            self.mqtt_client.reconnect()
        self.mqtt_client.loop_start()

    def _get_mqtt_client(self):
        mqtt_client = mqtt.Client(client_id=self.blid)
        mqtt_client.username_pw_set(username=self.blid, password=self.password)
        mqtt_client.on_connect = self._internal_on_connect
        mqtt_client.on_disconnect = self._internal_on_disconnect

        self.log.debug("Setting TLS certificate")
        ssl_context = generate_tls_context()
        mqtt_client.tls_set_context(ssl_context)
        mqtt_client.tls_insecure_set(True)  # noqa: FBT003

        return mqtt_client

    def _internal_on_connect(self, _client, _userdata, _flags, rc):
        self.log.debug(
            "Connected to Roomba %s, response code = %s", self.address, rc
        )
        connection_error = MQTT_ERROR_MESSAGES.get(rc)
        # If response code(rc) is 0 then connection was successful.
        if rc != 0 and connection_error is None:
            self.log.warning(
                "Unknown connection error: ID=%s."
                "Kindly use https://github.com/pschmitt/roombapy/issues/new",
                rc,
            )
            connection_error = "UNKNOWN_ERROR"
        if self.on_connect is not None:
            self.on_connect(connection_error)

    def _internal_on_disconnect(self, _client, _userdata, rc):
        self.log.debug(
            "Disconnected from Roomba %s, response code = %s", self.address, rc
        )
        connection_error = MQTT_ERROR_MESSAGES.get(rc)
        # If response code(rc) is 0 then connection was successful.
        if rc != 0 and connection_error is None:
            self.log.warning(
                "Unknown disconnection error: ID=%s."
                "Kindly use https://github.com/pschmitt/roombapy/issues/new",
                rc,
            )
            connection_error = "UNKNOWN_ERROR"
        if self.on_disconnect is not None:
            self.on_disconnect(connection_error)

"""Prove the supervisor actually reconnects — the load-bearing D4 claim.

This test kills a broker mid-session, so it runs its **own** broker on its
own port. Sharing the suite's broker made every later test that needs one
fail whenever the restart was slow: the symptom was four fixture errors and
twenty seconds of extra runtime, appearing perhaps once in fifteen runs and
never on demand. Isolation removes the class of problem rather than racing
against it.
"""

import asyncio
import contextlib
import getpass
import shutil
import socket
import ssl
import subprocess
import time
from collections.abc import Callable, Iterator
from pathlib import Path

import aiomqtt
import pytest
from roombapy.roomba import RoombaClient, TransportOptions

from tests.conftest import ROOMBA_HOST, ROOMBA_PASSWORD, ROOMBA_USERNAME

CERTS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
MOSQUITTO_DIR = CERTS / "mosquitto"

# CI runs the broker as a Docker service, so the runner itself has no
# mosquitto binary. This test needs to start and stop one of its own, so it
# skips there rather than failing. `nix develop` provides the binary, as does
# any local install.
_MOSQUITTO = shutil.which("mosquitto")
requires_mosquitto = pytest.mark.skipif(
    _MOSQUITTO is None,
    reason="needs a local mosquitto binary to run its own broker",
)

PAYLOAD_A = '{"state":{"reported":{"batPct":55}}}'
PAYLOAD_B = '{"state":{"reported":{"batPct":77}}}'


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


class PrivateBroker:
    """A mosquitto instance this test alone owns."""

    def __init__(self, workdir: Path) -> None:
        """Write a config pointing at the repo's own test certificates."""
        self.port = _free_port()
        self.workdir = workdir
        self.log = workdir / "mosquitto.log"
        self.process: subprocess.Popen[bytes] | None = None

        certs = MOSQUITTO_DIR / "tls-certificates"
        shutil.copy(certs / "test.crt", workdir / "test.crt")
        shutil.copy(certs / "test.key", workdir / "test.key")
        shutil.copy(MOSQUITTO_DIR / "mosquitto.passwd", workdir / "passwd")
        (workdir / "passwd").chmod(0o600)
        # mosquitto drops privileges to its own user by default and then
        # cannot read a config, password file or log inside a directory owned
        # by whoever ran the tests. Keep it as the current user.
        (workdir / "mosquitto.conf").write_text(
            f"user {getpass.getuser()}\n"
            f"allow_anonymous false\n"
            f"listener {self.port}\n"
            f"password_file {workdir / 'passwd'}\n"
            f"certfile {workdir / 'test.crt'}\n"
            f"keyfile {workdir / 'test.key'}\n"
            f"log_dest file {self.log}\n"
        )

    def start(self, timeout: float = 10.0) -> None:
        """Start it and wait until the port actually accepts connections."""
        assert _MOSQUITTO is not None
        self.process = subprocess.Popen(
            [_MOSQUITTO, "-c", str(self.workdir / "mosquitto.conf")],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with (
                contextlib.suppress(OSError),
                socket.create_connection(
                    ("127.0.0.1", self.port), timeout=0.5
                ),
            ):
                return
            time.sleep(0.1)
        output = b""
        if self.process is not None and self.process.stdout is not None:
            self.process.kill()
            output = self.process.stdout.read()
        msg = (
            f"private broker did not come up on {self.port}: "
            f"{output.decode(errors='replace')}"
        )
        raise AssertionError(msg)

    def _accepting(self) -> bool:
        """Whether the port currently accepts a connection."""
        try:
            with socket.create_connection(
                ("127.0.0.1", self.port), timeout=0.5
            ):
                return True
        except OSError:
            return False

    def stop(self, timeout: float = 10.0) -> None:
        """Stop it and wait until the port is genuinely closed."""
        if self.process is None:
            return
        self.process.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            self.process.wait(timeout=timeout)
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=timeout)
        self.process = None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self._accepting():
                return
            time.sleep(0.1)
        msg = f"private broker still listening on {self.port}"
        raise AssertionError(msg)


@pytest.fixture
def broker(tmp_path: Path) -> Iterator[PrivateBroker]:
    """A broker only this test can disturb."""
    instance = PrivateBroker(tmp_path)
    instance.start()
    yield instance
    instance.stop()


def _tls() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.set_ciphers("DEFAULT:!DH")
    return context


async def _publish(port: int, payload: str) -> None:
    """Stand in for the robot pushing an update."""
    async with aiomqtt.Client(
        hostname=ROOMBA_HOST,
        port=port,
        identifier="publisher",
        username=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        tls_context=_tls(),
        tls_insecure=True,
    ) as client:
        await client.publish("test", payload)


async def _wait_for(
    predicate: Callable[[], bool],
    timeout: float = 20.0,  # noqa: ASYNC109
) -> None:
    async with asyncio.timeout(timeout):
        while not predicate():
            await asyncio.sleep(0.05)


@requires_mosquitto
@pytest.mark.asyncio
async def test_reconnects_after_broker_restart(
    broker: PrivateBroker,
) -> None:
    """Survive the connection dropping, and resubscribe on the way back."""
    client = RoombaClient(
        address=ROOMBA_HOST,
        blid=ROOMBA_USERNAME,
        password=ROOMBA_PASSWORD,
        transport=TransportOptions(port=broker.port),
    )
    disconnects: list[str | None] = []
    client.register_on_disconnect_callback(disconnects.append)

    try:
        await client.connect()
        await _publish(broker.port, PAYLOAD_A)
        await _wait_for(
            lambda: (
                client.master_state.get("state", {})
                .get("reported", {})
                .get("batPct")
                == 55
            )
        )

        broker.stop()
        await _wait_for(lambda: not client.connected)
        assert disconnects, "disconnect callback never fired"

        broker.start()
        await _wait_for(lambda: client.connected)

        # The subscription must have been re-established, not just the socket.
        await _publish(broker.port, PAYLOAD_B)
        await _wait_for(
            lambda: client.master_state["state"]["reported"]["batPct"] == 77
        )
    finally:
        await client.disconnect()

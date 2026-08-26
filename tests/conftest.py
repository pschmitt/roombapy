"""Tools and fixtures for tests."""

import pathlib
from collections.abc import Generator
from dataclasses import dataclass

import paho.mqtt.client as mqtt
import pytest

ROOMBA_HOST = "127.0.0.1"
ROOMBA_USERNAME = "test"
ROOMBA_PASSWORD = "test"
ROOMBA_NAME = "Roomba"
ROOMBA_CONTINUOUS = True
ROOMBA_DELAY = 120


@dataclass
class Message:
    """MQTT-like message."""

    topic: str
    payload: bytes
    qos: str = "qos"


def as_message(payload: bytes, *, topic: bytes = b"test") -> mqtt.MQTTMessage:
    """Craft MQTT message from bytes."""
    message = mqtt.MQTTMessage(topic=topic)
    message.payload = payload
    return message


# --- diagnostics for the intermittent broker-dependent failures ------------
#
# A handful of runs have ended with four fixture errors and roughly twelve
# extra seconds of runtime, then dozens of clean runs in a row. The cause is
# not established: a broker-restart race was found and fixed, and the symptom
# recurred afterwards, so that was not it.
#
# Rather than keep guessing, capture the evidence the next time it happens.

# Where the broker writes, if it writes anywhere we can see. CI runs it in a
# container and nix in a temporary directory, so absence is normal — the
# diagnostics then report the listener state alone rather than failing.
_BROKER_LOG_CANDIDATES = (
    pathlib.Path("/var/log/mosquitto/mosquitto.log"),
    pathlib.Path("mosquitto.log"),
)


def _broker_log() -> pathlib.Path | None:
    """First readable broker log, or None."""
    return next((p for p in _BROKER_LOG_CANDIDATES if p.exists()), None)


def _broker_state() -> str:
    """Whether anything is listening on 8883, without needing `ss`."""
    try:
        table = pathlib.Path("/proc/net/tcp").read_text()
    except OSError:
        return "unknown"
    # 8883 == 0x22B3, state 0A == LISTEN.
    listening = any(
        ":22B3" in line and " 0A " in line for line in table.splitlines()
    )
    return "listening" if listening else "NOT listening"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,  # noqa: ARG001
    call: pytest.CallInfo[None],  # noqa: ARG001
) -> Generator[None, None, None]:
    """On a failure, record what the broker was doing at that moment.

    ``hookwrapper=True`` yields a result object, not the report itself —
    unwrapping it with ``get_result()`` is required, and getting this wrong
    makes pytest collect nothing at all rather than fail loudly.
    """
    outcome = yield
    report: pytest.TestReport = outcome.get_result()  # type: ignore[attr-defined]
    if report.outcome != "failed":
        return
    lines = [
        f"broker on 8883: {_broker_state()}",
        f"phase: {report.when}",
    ]
    log = _broker_log()
    if log is not None:
        tail = log.read_text().splitlines()[-15:]
        lines.append("last broker log lines:")
        lines.extend(f"  {line}" for line in tail)
    report.sections.append(("broker diagnostics", "\n".join(lines)))

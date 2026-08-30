"""Prototype async Roomba client — vertical slice.

Not the finished v2. This exists to test whether the interface proposed in
the design document survives contact with an implementation. It covers one
path end to end: construct, connect, subscribe, receive, drive the state
machine, reconnect, disconnect.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import logging
import random
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, Self, cast

import aiomqtt
import orjson

from roombapy.state import RoombaMessage, RoombaStateMachine
from roombapy.tls import generate_tls_context

if TYPE_CHECKING:
    import ssl

    from roombapy.const import ErrorCode, ErrorMessage, State
    from roombapy.types import ReportedState

__all__ = [
    "MAX_CONNECTION_RETRIES",
    "RoombaAuthError",
    "RoombaClient",
    "RoombaConnectionError",
    "RoombaError",
    "RoombaMessage",
    "RoombaScopeError",
    "TransportOptions",
]

MAX_CONNECTION_RETRIES = 3
RECONNECT_BACKOFF_MIN = 1.0
RECONNECT_BACKOFF_MAX = 60.0
# Without jitter every robot in a household comes back in lockstep after a
# router restart, which is the moment the network can least afford it.
RECONNECT_BACKOFF_JITTER = 0.25
# How long disconnect() waits for in-flight callbacks before cancelling.
CALLBACK_DRAIN_TIMEOUT = 5.0

# CONNACK codes meaning "your credentials are wrong": 4 and 5 in MQTT 3.1.1,
# 134 and 135 in MQTT 5.
AUTH_FAILURE_CODES = frozenset({4, 5, 134, 135})

# Whether a command is scoped to selected rooms is decided by one thing only:
# whether the `regions` array is present and non-empty. Null and empty are
# treated identically by the robot — the key is omitted and the robot cleans
# the whole house. `rid`/`region_id` are element fields inside the array, not
# a top-level scope gate, and `command_type`/`operatingMode` are orthogonal.
#
# Verified against MissionCommand::toPayload in the vendor app: the emit is
# gated on `regions != null && regions.length != 0`, and against field dumps
# (i7+ with region_ids populated versus i3+ with an empty list).
#
# The failure this guards against is not a wrong reply but a robot that
# leaves the dock and cleans an entire home when the caller asked for one
# room.
REGION_SCOPED_COMMANDS = frozenset({"start", "clean", "cleanRoom"})

MessageCallback = Callable[[RoombaMessage], Awaitable[None] | None]
ErrorCallback = Callable[[str | None], Awaitable[None] | None]
ConnectionState = Literal["connected", "disconnected"]
StateCallback = Callable[[ConnectionState, str | None], Awaitable[None] | None]
Unsubscribe = Callable[[], None]
RobotPreference = str | int | dict[str, int]


@dataclass(frozen=True, slots=True)
class TransportOptions:
    """Rarely-changed transport settings, kept out of the constructor."""

    port: int = 8883
    topic: str = "#"
    tls_context: ssl.SSLContext | None = None
    exclude: str = ""
    update_seconds: int = 300


class RoombaError(Exception):
    """Base class for errors raised by this client."""


class RoombaConnectionError(RoombaError):
    """The robot could not be reached."""


class RoombaAuthError(RoombaConnectionError):
    """The robot rejected the credentials."""


class RoombaScopeError(RoombaError, ValueError):
    """A room-scoped command would have run over the whole house."""


class RoombaClient:
    """Async client for a local Roomba MQTT connection."""

    def __init__(
        self,
        address: str,
        blid: str,
        password: str,
        *,
        transport: TransportOptions | None = None,
    ) -> None:
        """Store connection parameters; no I/O happens here."""
        self.log = logging.getLogger(__name__)
        self.address = address
        self.blid = blid
        self.password = password
        options = transport or TransportOptions()
        self.port = options.port
        self.topic = options.topic
        self.exclude = options.exclude
        self.update_seconds = options.update_seconds
        self._tls_context = options.tls_context or generate_tls_context()
        self._last_full_update = time.monotonic()

        self._state = RoombaStateMachine()
        self._client: aiomqtt.Client | None = None
        self._task: asyncio.Task[None] | None = None
        self._first_connect: asyncio.Future[None] | None = None
        self._connected = False
        self._closing = False
        self.client_error: str | None = None

        self._on_message: list[MessageCallback] = []
        self._on_disconnect: list[ErrorCallback] = []
        self._on_state: list[StateCallback] = []
        self.auth_error: RoombaAuthError | None = None
        self._pending_callbacks: set[asyncio.Task[None]] = set()
        self._watchers: set[asyncio.Queue[RoombaMessage]] = set()
        self._closed_event = asyncio.Event()

    # ------------------------------------------------------------------
    # state
    # ------------------------------------------------------------------

    @property
    def master_state(self) -> RoombaMessage:
        """Accumulated reported state, same shape as the threaded client."""
        return self._state.master_state

    @property
    def reported(self) -> ReportedState:
        """Typed view of the reported state — the same dict, checked.

        Opt-in: ``master_state`` is unchanged and still ``dict[str, Any]``.
        Coverage is partial by design; see ``roombapy.types``.
        """
        state: Any = self._state.master_state.get("state", {})
        return cast("ReportedState", state.get("reported", {}))

    @property
    def connected(self) -> bool:
        """Whether a session is currently established."""
        return self._connected

    @property
    def current_state(self) -> State:
        """Derived mission state."""
        return self._state.current_state

    @property
    def co_ords(self) -> dict[str, Any]:
        """Last reported pose, in the threaded client's shape."""
        return self._state.co_ords

    @property
    def bin_full(self) -> bool:
        """Whether the bin last reported itself full."""
        return self._state.bin_full

    @property
    def cleanMissionStatus_phase(self) -> str:  # noqa: N802
        """Current mission phase, verbatim from the robot."""
        return self._state.cleanMissionStatus_phase

    @property
    def previous_cleanMissionStatus_phase(self) -> str:  # noqa: N802
        """Mission phase before the current one."""
        return self._state.previous_cleanMissionStatus_phase

    @property
    def error_code(self) -> ErrorCode | None:
        """Last reported error code."""
        return self._state.error_code

    @property
    def error_message(self) -> ErrorMessage | None:
        """Last reported error message."""
        return self._state.error_message

    # ------------------------------------------------------------------
    # subscriptions
    # ------------------------------------------------------------------

    def register_on_message_callback(
        self, callback: MessageCallback
    ) -> Unsubscribe:
        """Register a message callback; returns a detach handle."""
        self._on_message.append(callback)
        return _detacher(self._on_message, callback)

    def register_on_disconnect_callback(
        self, callback: ErrorCallback
    ) -> Unsubscribe:
        """Register a disconnect callback; returns a detach handle."""
        self._on_disconnect.append(callback)
        return _detacher(self._on_disconnect, callback)

    def register_on_connection_state_callback(
        self, callback: StateCallback
    ) -> Unsubscribe:
        """Register for connection-state changes; returns a detach handle.

        Fires on every transition, not only on loss, so a caller can mark an
        entity unavailable and available again without inferring the second
        half from the absence of the first.
        """
        self._on_state.append(callback)
        return _detacher(self._on_state, callback)

    async def watch(
        self, *, maxsize: int = 100
    ) -> AsyncIterator[RoombaMessage]:
        """Yield messages as they arrive.

        Each watcher gets its own queue, so a slow consumer cannot starve the
        others or stall delivery. When a watcher falls ``maxsize`` messages
        behind, its oldest message is dropped and the loss is logged — state
        is cumulative, so the newest message is always the more useful one.
        """
        queue: asyncio.Queue[RoombaMessage] = asyncio.Queue(maxsize=maxsize)
        self._watchers.add(queue)
        try:
            while True:
                get = asyncio.ensure_future(queue.get())
                closed = asyncio.ensure_future(self._closed_event.wait())
                try:
                    done, pending = await asyncio.wait(
                        {get, closed}, return_when=asyncio.FIRST_COMPLETED
                    )
                except BaseException:
                    get.cancel()
                    closed.cancel()
                    raise
                for task in pending:
                    task.cancel()
                if pending:
                    await asyncio.gather(*pending, return_exceptions=True)
                if get not in done:
                    return
                yield get.result()
        finally:
            self._watchers.discard(queue)

    def _feed_watchers(self, message: RoombaMessage) -> None:
        for queue in self._watchers:
            if queue.full():
                with contextlib.suppress(asyncio.QueueEmpty):
                    queue.get_nowait()
                self.log.warning(
                    "Watcher for Roomba %s fell behind; dropped a message",
                    self.address,
                )
            with contextlib.suppress(asyncio.QueueFull):
                queue.put_nowait(message)

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Establish a session, or raise.

        Returns once subscribed. Losing the session afterwards is handled by
        the supervisor with backoff and does not surface here.

        Against an unreachable host this takes around 18 seconds: three
        attempts, each waiting out a TCP connect. Cancellation is clean, so
        a caller that needs a tighter bound — a config flow, say — can wrap
        this in ``asyncio.timeout`` and the client will tear itself down.
        """
        if self._task is not None and not self._task.done():
            msg = (
                f"Already connected to Roomba at {self.address}. "
                f"Call disconnect() first if you need to reconnect."
            )
            raise RoombaError(msg)

        if self._task is not None:
            # The supervisor has ended on its own — the auth path returns
            # rather than retrying. Reconnecting is exactly what a caller
            # should do after re-provisioning the robot, so clear the stale
            # task instead of refusing. Retrieving the exception keeps
            # asyncio from warning that it was never consumed.
            with contextlib.suppress(asyncio.CancelledError, Exception):
                self._task.exception()
            self._task = None
            self.auth_error = None
            self.client_error = None

        loop = asyncio.get_running_loop()
        self._closing = False
        self._closed_event = asyncio.Event()
        self._first_connect = loop.create_future()
        self._task = loop.create_task(self._supervise())

        try:
            await self._first_connect
        except BaseException:
            await self.disconnect()
            raise

    async def disconnect(self) -> None:
        """Tear the session down and stop reconnecting."""
        self._closing = True
        task, self._task = self._task, None
        if task is not None:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._connected = False
        self._closed_event.set()

        # Give callbacks already in flight a chance to finish. A consumer
        # persisting state from one would otherwise lose it on unload.
        pending = list(self._pending_callbacks)
        if pending:
            _finished, unfinished = await asyncio.wait(
                pending, timeout=CALLBACK_DRAIN_TIMEOUT
            )
            for stuck in unfinished:
                stuck.cancel()
            if unfinished:
                await asyncio.gather(*unfinished, return_exceptions=True)
                self.log.warning(
                    "%d Roomba callback(s) did not finish within %.0fs and "
                    "were cancelled",
                    len(unfinished),
                    CALLBACK_DRAIN_TIMEOUT,
                )

    async def __aenter__(self) -> Self:
        """Connect on entry."""
        await self.connect()
        return self

    async def __aexit__(self, *_exc: object) -> None:
        """Disconnect on exit."""
        await self.disconnect()

    # ------------------------------------------------------------------
    # supervisor
    # ------------------------------------------------------------------

    async def _supervise(self) -> None:
        """Hold a session open, reconnecting with backoff when it drops."""
        backoff = RECONNECT_BACKOFF_MIN
        attempt = 0

        while not self._closing:
            try:
                async with aiomqtt.Client(
                    hostname=self.address,
                    port=self.port,
                    identifier=self.blid,
                    username=self.blid,
                    password=self.password,
                    tls_context=self._tls_context,
                    tls_insecure=True,
                ) as client:
                    self._client = client
                    await client.subscribe(self.topic)
                    self._connected = True
                    self.client_error = None
                    self.auth_error = None
                    backoff = RECONNECT_BACKOFF_MIN
                    attempt = 0
                    self._resolve_first_connect(None)
                    await self._notify_state(connected=True, error=None)
                    self.log.info("Connected to Roomba %s", self.address)

                    async for message in client.messages:
                        self._handle_message(
                            str(message.topic), bytes(message.payload or b"")
                        )
            except asyncio.CancelledError:
                raise
            except aiomqtt.MqttError as err:
                attempt += 1
                error = self._classify(err, attempt)
                was_connected, self._connected = self._connected, False
                if was_connected:
                    await self._notify_state(connected=False, error=str(err))

                if isinstance(error, RoombaAuthError):
                    # Credentials do not fix themselves. Retrying here would
                    # hammer the robot forever, and on some brokers repeated
                    # bad logins are worth avoiding on their own.
                    self.auth_error = error
                    if not self._resolve_first_connect(error):
                        # Not .exception(): the traceback adds nothing to
                        # "the password is wrong", and this is a state the
                        # user must act on, not a defect to report.
                        self.log.error(  # noqa: TRY400
                            "Roomba %s rejected the credentials; not "
                            "retrying. Re-provision and reconnect.",
                            self.address,
                        )
                        await self._notify_auth_failure(
                            error, was_connected=was_connected
                        )
                    return

                if error is not None and self._resolve_first_connect(error):
                    return
                if was_connected:
                    # Only report a loss of something that existed. During
                    # the initial connect these attempts are retries, not
                    # disconnections, and a consumer would otherwise mark an
                    # entity unavailable that had never been available.
                    await self._notify_disconnect(str(err))
                self.log.warning(
                    "Roomba %s connection lost (%s), retrying in %.0fs",
                    self.address,
                    err,
                    backoff,
                )
            except Exception:
                # Anything that is not a transport error — a malformed
                # payload the state machine chokes on, a synchronous
                # callback that raises — would otherwise escape this task
                # and end it for good: no reconnect, no disconnect
                # callback, and the exception sitting unretrieved until
                # someone awaits the task. Treat it like a lost connection
                # and come back.
                was_connected, self._connected = self._connected, False
                self.log.exception(
                    "Unexpected error handling Roomba %s, reconnecting "
                    "in %.0fs",
                    self.address,
                    backoff,
                )
                if was_connected:
                    await self._notify_state(
                        connected=False, error="internal error"
                    )
                    await self._notify_disconnect("internal error")
            finally:
                self._connected = False
                self._client = None

            if self._closing:
                return
            await asyncio.sleep(
                backoff * (1 + random.random() * RECONNECT_BACKOFF_JITTER)  # noqa: S311
            )
            backoff = min(backoff * 2, RECONNECT_BACKOFF_MAX)

    def _classify(
        self, err: aiomqtt.MqttError, attempt: int
    ) -> RoombaConnectionError | None:
        """Turn a transport error into the exception connect() should raise."""
        text = str(err)
        self.client_error = text
        if self._is_auth_failure(err):
            return RoombaAuthError(
                f"Roomba at {self.address} rejected the credentials"
            )
        if attempt >= MAX_CONNECTION_RETRIES:
            return RoombaConnectionError(
                f"Unable to connect to Roomba at {self.address}: {text}"
            )
        return None

    @staticmethod
    def _is_auth_failure(err: aiomqtt.MqttError) -> bool:
        """Recognise a credential rejection from the broker's reason code.

        MQTT 3.1.1 answers CONNACK 4 (bad username or password) or 5 (not
        authorised); MQTT 5 answers 134 or 135. aiomqtt carries the code on
        ``MqttCodeError.rc``, which is checked first — the string fallback
        only covers transports that raise a bare ``MqttError``.
        """
        code = getattr(err, "rc", None)
        value = getattr(code, "value", code)
        if isinstance(value, int):
            return value in AUTH_FAILURE_CODES
        return "not authorized" in str(err).lower()

    def _resolve_first_connect(self, error: BaseException | None) -> bool:
        """Settle the future connect() is waiting on. True if it gave up."""
        future = self._first_connect
        if future is None or future.done():
            return False
        if error is None:
            future.set_result(None)
            return False
        future.set_exception(error)
        return True

    # ------------------------------------------------------------------
    # inbound
    # ------------------------------------------------------------------

    def _handle_message(self, topic: str, raw_payload: bytes) -> None:
        """Decode one payload, advance state, then fan out to callbacks."""
        if self.exclude and self.exclude in topic:
            return

        decoded = _decode_payload(raw_payload)
        if decoded is None:
            self.log.warning(
                "Got malformed message from %s: %r", self.address, raw_payload
            )
            return

        self._state.apply(decoded)

        # Periodically re-derive everything from the accumulated state, as the
        # threaded client does. Deltas only carry what changed, so some
        # derived values would otherwise never be revisited.
        now = time.monotonic()
        if now - self._last_full_update > self.update_seconds:
            self.log.debug("Republishing master_state %s", self.address)
            self._state.republish_all()
            self._last_full_update = now

        self._feed_watchers(decoded)

        for callback in list(self._on_message):
            self._dispatch(callback, decoded)

    async def _notify_state(
        self, *, connected: bool, error: str | None
    ) -> None:
        """Tell subscribers the connection state changed."""
        state: ConnectionState = "connected" if connected else "disconnected"
        for callback in list(self._on_state):
            self._dispatch_two(callback, state, error)

    def _dispatch_two(
        self, callback: Callable[..., Any], state: str, error: str | None
    ) -> None:
        """Two-argument variant of _dispatch, for state callbacks."""
        self._dispatch(lambda _ignored: callback(state, error), None)

    async def _notify_disconnect(self, error: str | None) -> None:
        for callback in list(self._on_disconnect):
            self._dispatch(callback, error)

    async def _notify_auth_failure(
        self, error: RoombaAuthError, *, was_connected: bool
    ) -> None:
        """Notify subscribers once for a terminal auth-failure teardown.

        ``was_connected`` reflects the state at the moment the failure was
        caught. If it was True, ``_supervise`` already sent the state
        change for this transition, so only the disconnect notice is new
        here. If it was False, nothing was connected to lose, so only the
        state change — the first notice of this failure — is sent.
        """
        if not was_connected:
            await self._notify_state(connected=False, error=str(error))
        if was_connected:
            await self._notify_disconnect(str(error))

    def _dispatch(self, callback: Callable[..., Any], payload: Any) -> None:
        """Run a callback on the event loop.

        An ``async def`` callback is dispatched as a task, so it yields at its
        await points and the read loop carries on. A synchronous one runs
        inline, because wrapping it in a task would change nothing: it never
        yields, so it blocks the loop either way. Isolating it would need an
        executor, which would break the guarantee that callbacks run on the
        loop.
        """
        try:
            result = callback(payload)
        except Exception:
            self.log.exception("Error in Roomba callback")
            return
        if inspect.isawaitable(result):
            task = asyncio.get_running_loop().create_task(
                _guard(result, self.log)
            )
            # Keep a reference so the task is not garbage collected.
            self._pending_callbacks.add(task)
            task.add_done_callback(self._pending_callbacks.discard)

    # ------------------------------------------------------------------
    # outbound
    # ------------------------------------------------------------------

    async def send_command(
        self, command: str, params: dict[str, Any] | None = None
    ) -> None:
        """Send a command to the Roomba.

        Raises ``RoombaScopeError`` if ``params`` carries a ``regions`` key
        that is null or empty. Such a payload does not mean "no rooms" to the
        robot, it means "every room" — see ``REGION_SCOPED_COMMANDS``.
        """
        _check_region_scope(command, params)
        roomba_command: dict[str, Any] = {
            "command": command,
            "time": int(datetime.timestamp(datetime.now())),
            "initiator": "localApp",
        }
        roomba_command.update(params or {})
        payload = orjson.dumps(
            roomba_command, option=orjson.OPT_NON_STR_KEYS
        ).decode("utf-8")
        await self._publish("cmd", payload)

    async def set_preference(
        self, preference: str, setting: RobotPreference
    ) -> None:
        """Set a preference on the Roomba."""
        value: RobotPreference | bool = setting
        if isinstance(setting, str):
            if setting.lower() == "true":
                value = True
            elif setting.lower() == "false":
                value = False
        payload = orjson.dumps({"state": {preference: value}}).decode("utf-8")
        await self._publish("delta", payload)

    async def _publish(self, topic: str, payload: str) -> None:
        client = self._client
        if client is None or not self._connected:
            msg = f"Not connected to Roomba at {self.address}"
            raise RoombaConnectionError(msg)
        self.log.debug("Publishing to %s: %s", topic, payload)
        try:
            await client.publish(topic, payload)
        except aiomqtt.MqttError as err:
            # The check above is only a pre-check: the session can drop
            # between it and the publish. Without this, aiomqtt's own
            # exception type escapes a caller who was told to catch
            # RoombaError, and arrives as an unhandled error instead.
            msg = f"Failed to send to Roomba at {self.address}: {err}"
            raise RoombaConnectionError(msg) from err


def _check_region_scope(command: str, params: dict[str, Any] | None) -> None:
    """Refuse a room-scoped command whose region list would vanish.

    The robot omits an absent or empty ``regions`` key and falls back to
    cleaning everything. A caller that built an empty list — no rooms
    selected, a filter that matched nothing, a lookup that failed — almost
    certainly did not mean that, and there is no way to tell afterwards.
    """
    if params is None or "regions" not in params:
        return
    if command not in REGION_SCOPED_COMMANDS:
        return
    regions = params["regions"]
    if regions:
        return
    msg = (
        f"{command!r} carries an empty 'regions' list. The robot omits the "
        f"key and cleans the whole house. Pass a non-empty list of "
        f"{{'rid'|'region_id', 'type'}} elements, or drop the key entirely "
        f"if a whole-house run is what you want."
    )
    raise RoombaScopeError(msg)


def _detacher(
    registry: list[Any], callback: Callable[..., Any]
) -> Unsubscribe:
    """Build an unsubscribe handle that is safe to call more than once.

    These end up in ``finally`` blocks and teardown paths, where raising
    ``ValueError`` because the callback was already removed turns tidy-up
    into a second failure.
    """

    def detach() -> None:
        with contextlib.suppress(ValueError):
            registry.remove(callback)

    return detach


async def _guard(awaitable: Awaitable[Any], log: logging.Logger) -> None:
    try:
        await awaitable
    except Exception:
        log.exception("Error in Roomba callback")


def _decode_payload(raw_payload: bytes) -> RoombaMessage | None:
    try:
        message = orjson.loads(raw_payload.decode())
    except (UnicodeDecodeError, orjson.JSONDecodeError):
        return None
    if not isinstance(message, dict):
        return None
    return message

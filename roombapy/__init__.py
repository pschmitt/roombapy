"""Public API of roombapy.

Version 2 is asynchronous throughout. The threaded client, its
``RoombaRemoteClient`` and ``RoombaFactory`` are gone; the README says what
each of them became.
"""

from roombapy.const import (
    MQTT_ERROR_MESSAGES,
    ROOMBA_ERROR_MESSAGES,
    ROOMBA_STATES,
    ErrorCode,
    ErrorMessage,
    State,
)
from roombapy.discovery import RoombaDiscovery
from roombapy.getpassword import RoombaPassword
from roombapy.roomba import (
    RoombaAuthError,
    RoombaClient,
    RoombaConnectionError,
    RoombaError,
    RoombaMessage,
    RoombaScopeError,
    TransportOptions,
)
from roombapy.roomba_info import RoombaInfo
from roombapy.rrtp import RobotPosition, RrtpUnsupportedError
from roombapy.state import RoombaStateMachine
from roombapy.tls import generate_tls_context
from roombapy.types import (
    BatteryInfo,
    BinState,
    Capabilities,
    ChargeStats,
    CleanMissionStatus,
    DockState,
    LegacyChargeStats,
    MissionNavStats,
    MissionStats,
    NavStats,
    Pose,
    PosePoint,
    ReportedState,
    ResetInfo,
    RunStats,
    SignalState,
    SystemStats,
)
from roombapy.vendor_errors import (
    UNVERIFIED_OVERLAP,
    VENDOR_ERROR_TEXTS,
    vendor_error_text,
)

__all__ = [
    "MQTT_ERROR_MESSAGES",
    "ROOMBA_ERROR_MESSAGES",
    "ROOMBA_STATES",
    "UNVERIFIED_OVERLAP",
    "VENDOR_ERROR_TEXTS",
    "BatteryInfo",
    "BinState",
    "Capabilities",
    "ChargeStats",
    "CleanMissionStatus",
    "DockState",
    "ErrorCode",
    "ErrorMessage",
    "LegacyChargeStats",
    "MissionNavStats",
    "MissionStats",
    "NavStats",
    "Pose",
    "PosePoint",
    "ReportedState",
    "ResetInfo",
    "RobotPosition",
    "RoombaAuthError",
    "RoombaClient",
    "RoombaConnectionError",
    "RoombaDiscovery",
    "RoombaError",
    "RoombaInfo",
    "RoombaMessage",
    "RoombaPassword",
    "RoombaScopeError",
    "RoombaStateMachine",
    "RrtpUnsupportedError",
    "RunStats",
    "SignalState",
    "State",
    "SystemStats",
    "TransportOptions",
    "generate_tls_context",
    "vendor_error_text",
]

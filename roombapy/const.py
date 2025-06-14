"""Constants for roombapy."""

from __future__ import annotations

TransportErrorCode = int
TransportErrorMessage = str | None
ErrorCode = int
ErrorMessage = str

MQTT_ERROR_MESSAGES: dict[TransportErrorCode, TransportErrorMessage] = {
    0: None,
    1: "Bad protocol",
    2: "Bad client id",
    3: "Server unavailable",
    4: "Bad username or password",
    5: "Not authorised",
    7: "The connection was lost",
}

# iRobot_6.3.1-release.apk / res/values-en-rGB/strings.xml
ROOMBA_ERROR_MESSAGES: dict[ErrorCode, ErrorMessage] = {
    0: "None",
    1: "Left wheel off floor",
    2: "Main brushes stuck",
    3: "Right wheel off floor",
    4: "Left wheel stuck",
    5: "Right wheel stuck",
    6: "Stuck near a cliff",
    7: "Left wheel error",
    8: "Bin error",
    9: "Bumper stuck",
    10: "Right wheel error",
    11: "Bin error",
    12: "Cliff sensor issue",
    13: "Both wheels off floor",
    14: "Bin missing",
    15: "Robot rebooted",
    16: "Bumped unexpectedly",
    17: "Path blocked",
    18: "Docking issue",
    19: "Undocking issue",
    20: "Docking issue",
    21: "Navigation problem",
    22: "Navigation problem",
    23: "Battery issue",
    24: "Navigation problem",
    25: "Reboot required",
    26: "Vacuum problem",
    27: "Vacuum problem",
    28: "Error",
    29: "Software update needed",
    30: "Vacuum problem",
    31: "Reboot required",
    32: "Smart map problem",
    33: "Path blocked",
    34: "Reboot required",
    35: "Unable to mop",
    36: "Bin full",
    37: "Tank needed refilling",
    38: "Robot error",
    39: "Reboot required",
    40: "Navigation problem",
    41: "Timed out",
    42: "Localization problem",
    43: "Navigation problem",
    44: "Pump issue",
    45: "Lid open",
    46: "Low battery",
    47: "Reboot required",
    48: "Path blocked",
    52: "Pad required attention",
    53: "Software update required",
    54: "Blades stuck",
    55: "Left blades stuck",
    56: "Right blades stuck",
    57: "Cutting deck stuck",
    58: "Navigation problem",
    59: "Tilt detected",
    60: "Rolled over",
    62: "Stop button pushed",
    63: "Hardware error",
    65: "Hardware problem detected",
    66: "Low memory",
    67: "Handle lifted",
    68: "Dead camera",
    69: "Navigation problem",
    70: "Problem sensing beacons",
    73: "Pad type changed",
    74: "Max area reached",
    75: "Navigation problem",
    76: "Hardware problem detected",
    78: "Left wheel error",
    79: "Right wheel error",
    85: "Path to charging station blocked",
    86: "Path to charging station blocked",
    88: "Navigation problem",
    89: "Timed out",
    91: "Workspace path error: Retrain %s",
    92: "Workspace path error: Retrain %s",
    93: "Workspace path error: Retrain %s",
    94: "Wheel motor over temp",
    95: "Wheel motor under temp",
    96: "Blade motor over temp",
    97: "Blade motor under temp",
    98: "Software error",
    99: "Navigation problem",
    101: "Battery isn't connected",
    102: "Charging error",
    103: "Charging error",
    104: "No charge current",
    105: "Charging current too low",
    106: "Battery too warm",
    107: "Battery temperature incorrect",
    108: "Battery communication failure",
    109: "Battery error",
    110: "Battery cell imbalance",
    111: "Battery communication failure",
    112: "Invalid charging load",
    114: "Internal battery failure",
    115: "Cell failure during charging",
    116: "Charging error of Home Base",
    118: "Battery communication failure",
    119: "Charging timeout",
    120: "Battery not initialized",
    121: "Clean the charging contacts",
    122: "Charging system error",
    123: "Battery not initialized",
    1000: "Left edge-sweeping brush stuck",
    1001: "Right edge-sweeping brush stuck",
    1002: "Cleaning unavailable. Check subscription status.",
    1003: "Dead vision board",
    1004: "Map was unavailable",
    1007: "Contact customer care",
    1008: "Cleaning arm is stuck",
    1009: "Robot stalled",
}

State = str | None
ROOMBA_STATES: dict[str, State] = {
    "charge": "Charging",
    "new": "New Mission",
    "run": "Running",
    "resume": "Running",
    "hmMidMsn": "Recharging",
    "recharge": "Recharging",
    "stuck": "Stuck",
    "hmUsrDock": "User Docking",
    "dock": "Docking",
    "dockend": "Docking - End Mission",
    "cancelled": "Cancelled",
    "stop": "Stopped",
    "pause": "Paused",
    "hmPostMsn": "End Mission",
    "evac": "Emptying Bin",
    "chargingerror": "Base Unplugged",
    "refill": "Refilling",
    "": None,
}

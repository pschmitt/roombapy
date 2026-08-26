"""Typed views over ``master_state``, additive and opt-in.

These describe the same dictionaries the client already returns; nothing is
parsed or converted, and ``master_state`` keeps its ``dict[str, Any]``
annotation. A caller that wants checking uses ``RoombaClient.reported``; a
caller that does not is unaffected.

Every field is optional, because the robot pushes deltas: a message carries
only what changed. Coverage is deliberately partial — the keys here are the
ones observed in real payloads and in a real consumer's reads. A key that is
not listed is simply not typed, which is the intended failure mode for
firmware-specific fields.
"""

from __future__ import annotations

from typing import Any, TypedDict


class Capabilities(TypedDict, total=False):
    """The ``cap`` object: what this robot can do."""

    pose: int
    carpetBoost: int
    maps: int
    pmaps: int
    dockComm: int
    estCap: int
    multiPass: int
    edge: int
    binFullDetect: int


class CleanMissionStatus(TypedDict, total=False):
    """The ``cleanMissionStatus`` object: what the robot is doing now."""

    cycle: str
    phase: str
    initiator: str
    error: int
    notReady: int
    nMssn: int
    mssnM: int
    mssnStrtTm: int
    expireM: int
    rechrgM: int
    sqft: int


class PosePoint(TypedDict, total=False):
    """Cartesian position in the robot's own frame, in millimetres."""

    x: int
    y: int


class Pose(TypedDict, total=False):
    """The ``pose`` object: position and heading."""

    theta: int
    point: PosePoint


class BinState(TypedDict, total=False):
    """The ``bin`` object."""

    present: bool
    full: bool


class SignalState(TypedDict, total=False):
    """The ``signal`` object: Wi-Fi quality."""

    rssi: int
    snr: int
    noise: int
    wlBars: int


class DockState(TypedDict, total=False):
    """The ``dock`` object.

    ``pwState``/``pdState``/``state`` have been observed as int in captures
    and as str in others, so they are typed as the union rather than
    forced to one.
    """

    known: bool
    state: int | str
    pwState: int | str
    pdState: int | str
    tankLvl: int
    fwVer: str
    error: int


class BatteryInfo(TypedDict, total=False):
    """The ``batInfo`` object: battery identity and cycle count."""

    mName: str
    mDate: str
    cCount: int


class RunStats(TypedDict, total=False):
    """``bbrun`` — lifetime run counters. Also seen as ``runtimeStats``.

    ``runtimeStats`` carries a subset (``hr``, ``min``, ``sqft``,
    ``nOpticalDD``, ``nOrients``) and has been observed with float values
    where ``bbrun`` uses int, so both are typed as ``float`` where they
    differ across captures.
    """

    hr: int
    min: int
    sqft: int
    nScrubs: int
    nStuck: int
    nPanics: int
    nPicks: int
    nCBump: int
    nCliffsF: int
    nCliffsR: int
    nMBStll: int
    nWStll: int
    nOpticalDD: int
    nPiezoDD: int
    nOrients: int


class ChargeStats(TypedDict, total=False):
    """``bbchg3`` — charging lifetime counters.

    ``estCap`` is the estimated battery capacity and the most useful field
    here: it is what makes aftermarket-cell health visible. Absence is
    normal and firmware/model-specific, not confined to any one series —
    a j7+ has been observed with no ``bbchg3`` key at all.
    """

    estCap: int
    avgMin: int
    hOnDock: int
    nAvail: int
    nDocks: int
    nLithChrg: int
    nNimhChrg: int
    smberr: int


class LegacyChargeStats(TypedDict, total=False):
    """``bbchg`` — the older charging block, alongside ``bbchg3``."""

    nChgOk: int
    nChgErr: int
    nChatters: int
    nKnockoffs: int
    nAborts: int
    nLithF: int
    aborts: list[int]
    smberr: int | str


class MissionStats(TypedDict, total=False):
    """``bbmssn`` — lifetime mission counters."""

    nMssn: int
    nMssnOk: int
    nMssnF: int
    nMssnC: int
    aMssnM: int
    aCycleM: int


class NavStats(TypedDict, total=False):
    """``bbnav`` — navigation lifetime counters."""

    nGoodLmrks: int
    aMtrack: float


class ResetInfo(TypedDict, total=False):
    """``bbrstinfo`` — reset causes. ``nOomRst`` counts software crashes."""

    nNavRst: int
    nMobRst: int
    nSafRst: int
    nMapLoadRst: int
    nOomRst: int
    safCauses: list[int]


class SystemStats(TypedDict, total=False):
    """``bbsys`` — total powered-on time."""

    hr: int
    min: int


class MissionNavStats(TypedDict, total=False):
    """``mssnNavStats`` — per-mission navigation telemetry.

    Populated during a mission and largely zero on the dock. ``l_drift`` and
    ``h_drift`` indicate pose confidence; ``gLmk``/``lmk`` the landmark
    density.
    """

    nMssn: int
    missionId: str
    gLmk: int
    lmk: int
    reLc: int
    plnErr: str
    mTrk: int
    kdp: int
    sfkdp: int
    nmc: int
    nmmc: int
    nrmc: int
    mpSt: str
    l_drift: int
    h_drift: int
    l_squal: int
    h_squal: int


class ReportedState(TypedDict, total=False):
    """The contents of ``master_state["state"]["reported"]``."""

    name: str
    sku: str
    batPct: int
    batteryType: str
    batInfo: BatteryInfo
    softwareVer: str
    hardwareRev: int
    cap: Capabilities
    cleanMissionStatus: CleanMissionStatus
    pose: Pose
    bin: BinState
    signal: SignalState
    dock: DockState
    # Lifetime telemetry blocks. Absence is normal and model-specific.
    bbrun: RunStats
    runtimeStats: RunStats
    bbchg3: ChargeStats
    bbchg: LegacyChargeStats
    bbmssn: MissionStats
    bbnav: NavStats
    bbrstinfo: ResetInfo
    bbsys: SystemStats
    mssnNavStats: MissionNavStats
    pmaps: list[dict[str, str]]
    lastCommand: dict[str, Any]
    cleanSchedule: dict[str, Any]
    carpetBoost: bool
    vacHigh: bool
    twoPass: bool
    noAutoPasses: bool
    openOnly: bool
    binPause: bool
    mopReady: dict[str, Any]
    tankPresent: bool
    tankLvl: int
    padWetness: dict[str, int]
    detectedPad: str
    lidOpen: bool


class RoombaState(TypedDict, total=False):
    """The ``state`` wrapper."""

    reported: ReportedState


class RoombaTopLevelState(TypedDict, total=False):
    """The shape of ``master_state`` itself."""

    state: RoombaState

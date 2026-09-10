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
    """The contents of ``master_state["state"]["reported"]``.

    ``total=False`` throughout, and that is not a formality: **which keys
    a robot sends depends on its firmware family**, not just on its
    hardware. The declarations below were assembled from complete key
    dumps of four families:

    ==================  ==================================  =====
    family              robot                               keys
    ==================  ==================================  =====
    9-series            Roomba 980, ``v2.4.17``               55
    lewis               Roomba i7+, ``lewis+22.52.10``        68
    soho                Roomba S9+, ``soho+22.29.10``         69
    sanmarino           Braava jet m6, ``sanmarino+22.29.6``  67
    ==================  ==================================  =====

    Two of the rows are confirmed twice. Two Braava jet m6 units
    belonging to different people report the same 67 keys, and two
    Roomba 980s -- differing in SKU, hardware revision and battery
    chemistry -- report the same 55. The ``lewis`` and ``soho`` rows
    rest on one robot each.

    Union: 94 keys. A fifth family, ``sapphire`` (j-series), is
    represented only by the fields listed at the end -- no complete dump
    of one exists here, so its absence from a group below means nothing.

    Consumers should keep reading the raw ``master_state`` dict for
    anything not declared here; this type is additive and never
    exhaustive.
    """

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

    # ------------------------------------------------------------------
    # Seen on ALL FOUR fully-dumped families. Types from the captures.
    # ------------------------------------------------------------------
    #: Network configuration. Always a mapping; the ADDRESS FIELDS
    #: INSIDE IT differ by generation, which is why the inner type is
    #: left open:
    #:
    #:   9-series          `{"addr": 169738246, "mask": 4294967040}`
    #:                     -- uint32: 10.30.0.6 and 255.255.255.0
    #:   lewis, sanmarino  `{"addr": "10.10.20.16", "mask": "255.255.255.0"}`
    #:
    #: All three from full value dumps, so the split is the 9-series
    #: against everything newer rather than a per-model quirk. A
    #: consumer reading `addr` has to handle both, or it renders an
    #: integer as an address on one generation and fails on the other.
    netinfo: dict[str, Any]
    bbpause: dict[str, Any]
    bbswitch: dict[str, Any]
    cloudEnv: str
    country: str
    ecoCharge: bool
    mapUploadAllowed: bool
    schedHold: bool
    svcEndpoints: dict[str, Any]
    timezone: str
    wifistat: dict[str, Any]
    wlcfg: dict[str, Any]

    # ------------------------------------------------------------------
    # Seen on three of the four. Absent on one is normal, not an error.
    #
    # `Any` WHERE NO VALUE WAS OBSERVED. A key can be evidenced without
    # its shape being evidenced: diagnostics downloads list key names
    # only, and the one full value dump available here covers a single
    # family. Declaring a plausible type from a field's NAME is how this
    # class already acquired three wrong ones -- `chrgLrPtrn` and
    # `deploymentState` and `pmapSGen` were all guessed as structures or
    # strings and are all ints. `Any` states what is actually known.
    # ------------------------------------------------------------------
    audio: dict[str, Any]
    batAuthEnable: Any
    behaviorFwk: Any
    childLock: bool
    #: Charge-light pattern. An int (2 observed), not a structure.
    chrgLrPtrn: int
    #: The i/s replacement for ``cleanSchedule``; the two never coexist.
    cleanSchedule2: list[dict[str, Any]]
    connected: bool
    #: An int (0 observed), despite reading like a name.
    deploymentState: int
    featureFlags: dict[str, Any]
    hwDbgr: Any
    hwPartsRev: dict[str, Any]
    langs2: dict[str, Any]
    #: `4` on the one robot where a value was seen. The union this
    #: carried before was a guess, like the four other types a real
    #: dump corrected.
    lastDisconnect: int
    #: NOT room or position telemetry, despite the name: a set of
    #: "which report categories are enabled" flags, all 1.
    #:
    #: Verified unchanged byte-for-byte across four samples spanning a
    #: real room transition, and again between mid-mission and docked
    #: on a second robot. THE SET VARIES BY MODEL -- 15 entries on a
    #: Braava m6, 16 on an S9+ (`hardknock_report`), 16 on an i7+
    #: (`learned_policy_report`) -- so treat the keys as open.
    missionTelemetry: dict[str, int]
    #: A mapping on two lewis robots (`{"pmaps": null}`) and `null`
    #: outright on a third. A key being present says nothing about the
    #: value being one -- `Any` covers both without claiming which.
    optFeats: Any
    pmapCL: bool
    pmapLearningAllowed: bool
    #: Map-generation number. An int (4 observed).
    pmapSGen: int
    pmapShare: dict[str, Any]
    rankOverlap: int
    reflexSettings: dict[str, Any]
    sceneRecog: Any
    secureBoot: dict[str, Any]
    subModSwVer: dict[str, str]
    tls: dict[str, Any]
    tz: dict[str, Any]

    # ------------------------------------------------------------------
    # Seen on one or two families only.
    # ------------------------------------------------------------------
    #: Clean Base evacuation permitted. i/s vacuums; absent on the Braava.
    evacAllowed: Any
    #: 9-series only -- merged into ``bbrun.nPanics`` on i/s.
    #: `{'panics': [8, 8, 8, 8, 8]}` on a 980.
    bbpanic: dict[str, Any]
    #: 9-series version block. i/s carries ``subModSwVer`` instead.
    #: A numeric string: `'4042'`.
    bootloaderVer: str
    #: `'5958'`.
    mobilityVer: str
    #: `'01.12.01#1'` -- not purely numeric.
    navSwVer: str
    #: `'32'` -- a string despite looking like a number.
    soundVer: str
    #: `'4582'`.
    uiSwVer: str
    #: `'6'`.
    umiVer: str
    wifiSwVer: str
    #: `1`. Not a structure.
    wifiAnt: int
    #: 9-series locale block. i/s carries ``langs2`` and ``tz``.
    #: `[{'en-UK': 0}, {'de-DE': 4}, ...]` -- a list of one-entry maps,
    #: not a flat list of names.
    langs: list[dict[str, int]]
    #: An index into `langs`: `4` for `de-DE` there.
    language: int
    #: Minutes: `120`.
    localtimeoffset: int
    #: Unix seconds.
    utctime: int
    #: `'c0:e4:34:93:ec:3a'`.
    mac: str
    #: 9-series. Dropped from a single write by the firmware; see the
    #: note on paired preferences in ``set_preferences``.
    noPP: bool
    binTypeDetect: Any
    bleDevLoc: Any
    wDevLoc: Any
    #: S9+ only among the dumps here.
    gentleMode: Any

    # ------------------------------------------------------------------
    # j-series (sapphire). NO complete dump of one exists here -- these
    # were recorded individually, so this group is certainly incomplete.
    # The camera and Genius machinery has no counterpart on the other
    # families.
    # ------------------------------------------------------------------
    odoaMode: Any
    odoaFeats: Any
    smartHome: Any
    streamingVideoStatus: Any
    peopleFilter: Any
    imgUpload: Any
    precheck: Any


class RoombaState(TypedDict, total=False):
    """The ``state`` wrapper."""

    reported: ReportedState


class RoombaTopLevelState(TypedDict, total=False):
    """The shape of ``master_state`` itself."""

    state: RoombaState

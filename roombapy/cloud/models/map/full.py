"""Full DTOs for map responses.

NOTE: DTO below are still incomplete in a subtle ways
      and may not work with some robots.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime  # noqa: TCH003 — mashumaro need this in runtime
from enum import IntEnum, StrEnum
from typing import Any

from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

from roombapy.cloud.models.serialization import (
    alias,
    irobot_dt_field,
    irobot_ts_field,
)


class Confidence(StrEnum):
    POOR_CONFIDENCE = "POOR_CONFIDENCE"
    PARTIAL_CONFIDENCE = "PARTIAL_CONFIDENCE"
    GOOD_CONFIDENCE = "GOOD_CONFIDENCE"
    INVALID = "INVALID"


class MapAuthor(StrEnum):
    ROBOT = "robot"
    USER = "user"


class TimeEstimateUnit(StrEnum):
    SECONDS = "seconds"
    MINUTES = "minutes"


class RegionType(StrEnum):
    BASEMENT = "basement"
    BATHROOM = "bathroom"
    BEDROOM = "bedroom"
    BREAKFAST_ROOM = "breakfast_room"
    CLOSET = "closet"
    CUSTOM = "custom"
    DEN = "den"
    DINING_ROOM = "dining_room"
    ENTRYWAY = "entryway"
    FAMILY_ROOM = "family_room"
    FOYER = "foyer"
    GARAGE = "garage"
    GUEST_BATHROOM = "guest_bathroom"
    GUEST_BEDROOM = "guest_bedroom"
    HALLWAY = "hallway"
    KIDS_ROOM = "kids_room"
    KITCHEN = "kitchen"
    LAUNDRY_ROOM = "laundry_room"
    LIVING_ROOM = "living_room"
    LOUNGE = "lounge"
    MEDIA_ROOM = "media_room"
    MUD_ROOM = "mud_room"
    OFFICE = "office"
    OUTSIDE = "outside"
    PANTRY = "pantry"
    PLAYROOM = "playroom"
    PRIMARY_BATHROOM = "primary_bathroom"
    PRIMARY_BEDROOM = "primary_bedroom"
    RECREATION_ROOM = "recreation_room"
    STORAGE_ROOM = "storage_room"
    STUDY = "study"
    SUN_ROOM = "sun_room"
    UNFINISHED_BASEMENT = "unfinished_basement"
    UNKNOWN = "unknown"
    WORKSHOP = "workshop"
    MASTER_BEDROOM = "master_bedroom"


class ZoneType(StrEnum):
    APPLIANCE = "appliance"
    BUILT_IN = "built_in"
    CHILDREN = "children"
    FLOORING = "flooring"
    FURNITURE = "furniture"
    PET = "pet"
    SEASONAL = "seasonal"
    OTHER = "other"
    UNSPECIFIED = "unspecified"


class ZoneExtentType(StrEnum):
    AROUND_BED = "around_bed"
    AROUND_SOFA = "around_sofa"
    AROUND_COFFEE_TABLE = "around_coffee_table"
    AROUND_DINING_TABLE = "around_dining_table"
    AROUND_TOILET = "around_toilet"
    AROUND_KITCHEN_ISLAND = "around_kitchen_island"
    AROUND_LITTER_BOX = "around_litter_box"
    AROUND_PET_BOWL = "around_pet_bowl"
    FRONT_OF_KITCHEN_COUNTER = "front_of_kitchen_counter"
    FRONT_OF_REFRIGERATOR = "front_of_refrigerator"
    FRONT_OF_OVEN = "front_of_oven"
    FRONT_OF_DISHWASHER = "front_of_dishwasher"
    RUG = "rug"
    AROUND_CHRISTMAS_TREE = "around_christmas_tree"
    UNSPECIFIED = "unspecified"


class PadType(StrEnum):
    DISPOSABLE = "disposable"
    REUSABLE = "reusable"


class OdoaMode(IntEnum):
    Unknown = 0
    EnabledForAllFeatures = 1
    EnabledForDocksOnly = 2
    Disabled = 3


class PadWetnessLevel(IntEnum):
    DAMP = 0
    MODERATE = 1
    WET = 2
    INVALID = 3


class OperatingMode(IntEnum):
    TRAVELING = 0
    VACUUMING = 1
    MOPPING = 2
    VIDEOSTREAMING = 3
    AIR_PURIFYING = 4
    COMBO_BIN_CLEANING = 5
    SCRUBBING = 6


@dataclass
class TimeEstimateParams(DataClassORJSONMixin):
    no_auto_passes: bool | None = None
    two_pass: bool | None = None
    no_koz: int | None = None
    carpet_boost: bool | None = None
    vac_high: bool | None = None
    scrub: int | None = None
    pad_wetness: dict[PadType, PadWetnessLevel] | None = None
    operating_mode: OperatingMode | None = None

    class Config(BaseConfig):
        """Camel-case all fields."""

        aliases: dict[str, str] = {  # noqa: RUF012 — conflicts with mypy
            "no_auto_passes": "noAutoPasses",
            "two_pass": "twoPass",
            "no_koz": "noKOZ",
            "carpet_boost": "carpetBoost",
            "vac_high": "vacHigh",
            "pad_wetness": "padWetness",
            "operating_mode": "operatingMode",
        }


@dataclass
class TimeEstimateInfo(DataClassORJSONMixin):
    confidence: Confidence
    estimate: int
    unit: TimeEstimateUnit
    params: TimeEstimateParams | None = None


@dataclass
class Region(DataClassORJSONMixin):
    """Mapped rooms."""

    id: str
    name: str
    region_type: RegionType
    policies: ZonePolicy
    time_estimates: list[TimeEstimateInfo] = field(default_factory=list)


@dataclass
class ZonePolicy(DataClassORJSONMixin):
    disabled_operating_modes: int
    odoa_mode: OdoaMode
    override_operating_modes: int
    odoa_feats: dict[str, int]


@dataclass
class ZoneDetailInfo(DataClassORJSONMixin):
    extent_type: ZoneExtentType
    id: str
    name: str
    policies: ZonePolicy
    recommend_id: str
    related_objects: list[str]
    tags: list[str]
    time_estimates: list[TimeEstimateInfo]
    zone_name_resourceid: str
    zone_type: ZoneType


@dataclass
class ObservedZoneQuality(DataClassORJSONMixin):
    confidence: int


Geometry = dict[str, Any]  # NOTE: all that extends SpatialGeometry class


@dataclass
class ObservedZoneInfo(DataClassORJSONMixin):
    extent_type: ZoneExtentType
    id: str
    quality: ObservedZoneQuality
    geometry: Geometry | None = None
    related_objects: list[str] = field(default_factory=list)


@dataclass
class MapHeader(DataClassORJSONMixin):
    id: str
    learning_percentage: int
    name: str
    resolution: float
    robot_orientation_rad: float
    user_orientation_rad: float
    create_time: datetime = irobot_ts_field("create_time")
    version: datetime = irobot_dt_field()
    mission_count: int | None = alias("nmssn", None)
    mission_id: str | None = None
    area: float | None = None


@dataclass
class KeepOutZone(DataClassORJSONMixin):
    id: str
    name: str
    recommend_id: str
    keep_out_zone_type: str = alias("keepoutzone_type")


@dataclass
class MapMetadata:
    creator: MapAuthor
    proc_state: str
    create_time: datetime = irobot_ts_field("create_time")
    user_version: datetime = irobot_dt_field("last_user_pmapv_id")
    user_timestamp: datetime = irobot_ts_field("last_user_ts")
    id: str = alias("pmap_id")
    map_version: datetime = irobot_dt_field("pmapv_id")
    learning_percentage: int | None = None
    # NOTE: It's, actually, proper class instance
    robot_cap: dict[str, int] | None = None
    robot_id: str | None = None
    shareability: int | None = None  # NOTE: Enum, actually
    mission_count: int | None = alias("nMssn", default=None)


@dataclass
class CopiedMap(DataClassORJSONMixin):
    robot_id: str
    map_version: datetime = irobot_dt_field("pmapv_id")
    id: str = alias("pmap_id")


@dataclass
class MergedMap(DataClassORJSONMixin):
    map_version: datetime = irobot_dt_field("pmapv_id")
    id: str = alias("pmap_id")
    ts: datetime = irobot_ts_field("ts")


@dataclass
class MapDetails(DataClassORJSONMixin):
    meta: MapMetadata = alias("active_pmapv")
    header: MapHeader = alias("map_header")
    keep_out_zones: list[KeepOutZone] = alias(
        "keepoutzones", default_factory=list
    )
    observed_zones: list[ObservedZoneInfo] = field(default_factory=list)
    regions: list[Region] = field(default_factory=list)


@dataclass
class Map(DataClassORJSONMixin):
    shared: int
    sku: str
    state: str
    visible: bool
    id: str = alias("pmap_id")
    details: MapDetails = alias("active_pmapv_details")
    active_version: datetime = irobot_dt_field("active_pmapv_id")
    robot_version: datetime = irobot_dt_field("robot_pmapv_id")
    user_version: datetime = irobot_dt_field("user_pmapv_id")
    last_version: datetime = irobot_ts_field("last_pmapv_ts")
    create_time: datetime = irobot_ts_field()
    robot_id: str | None = None
    robot_ids: list[str] = field(default_factory=list)
    copied_from: CopiedMap | None = None
    merged_maps: list[MergedMap] = alias(
        "merged_pmap_ids", default_factory=list
    )

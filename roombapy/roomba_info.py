"""Module for RoombaInfo class."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin

Capabilities = dict[str, int | None] | None


@dataclass
class RoombaInfo(DataClassORJSONMixin):
    """Class for storing information about a Roomba device."""

    hostname: str
    firmware: str = field(metadata=field_options(alias="sw"))
    ip: str
    mac: str
    robot_name: str = field(metadata=field_options(alias="robotname"))
    sku: str
    capabilities: Capabilities = field(metadata=field_options(alias="cap"))
    password: str | None = None

    @cached_property
    def blid(self) -> str:
        """Return the BLID."""
        return self.hostname.split("-")[1]

    def __hash__(self) -> int:
        """Return the hash of the RoombaInfo object."""
        return hash(self.mac)

    def __eq__(self, o: object) -> bool:
        """Return whether the RoombaInfo object is equal to another object."""
        return isinstance(o, RoombaInfo) and self.mac == o.mac


def validate_hostname(value: str) -> None:
    """Validate robot hostname."""
    if "-" not in value:
        msg = f"hostname does not contain a dash: {value}"
        raise ValueError(msg)
    model_name, blid = value.split("-")
    if blid == "":
        msg = f"empty blid: {value}"
        raise ValueError(msg)
    if model_name.lower() not in {"roomba", "irobot"}:
        msg = f"unsupported model in hostname: {value}"
        raise ValueError(msg)

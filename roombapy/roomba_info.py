"""Module for RoombaInfo class."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Ignored at runtime, but not by mypy
    from pydantic.v1 import (  # type: ignore[attr-defined]
        BaseModel,
        Field,
        field_validator,
    )
else:
    # Ignored by mypy, but not at runtime
    try:
        from pydantic.v1 import (  # type: ignore[attr-defined]
            BaseModel,
            Field,
            field_validator,
        )
    except ImportError:
        from pydantic import BaseModel, Field  # type: ignore[attr-defined]
        from pydantic import (
            validator as field_validator,  # type: ignore[attr-defined]
        )


class RoombaInfo(BaseModel):
    """Class for storing information about a Roomba device."""

    hostname: str
    firmware: str = Field(alias="sw")
    ip: str
    mac: str
    robot_name: str = Field(alias="robotname")
    sku: str
    capabilities: dict[str, int] = Field(alias="cap")
    password: str | None = None

    @field_validator("hostname")  # type: ignore[misc]
    @classmethod
    def hostname_validator(cls, value: str) -> str:
        """Validate the hostname."""
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
        return value

    @cached_property
    def blid(self) -> str:
        """Return the BLID."""
        return self.hostname.split("-")[1]

    class Config:
        """Pydantic configuration for the RoombaInfo class."""

        # NOTE: Used to ensure Pydantic v1 backwards compatibility
        #       See https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (cached_property,)

    def __hash__(self) -> int:
        """Return the hash of the RoombaInfo object."""
        return hash(self.mac)

    def __eq__(self, o: object) -> bool:
        """Return whether the RoombaInfo object is equal to another object."""
        return isinstance(o, RoombaInfo) and self.mac == o.mac

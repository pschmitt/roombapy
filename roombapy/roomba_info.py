from __future__ import annotations

from functools import cached_property

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
    hostname: str
    firmware: str = Field(alias="sw")
    ip: str
    mac: str
    robot_name: str = Field(alias="robotname")
    sku: str
    capabilities: dict[str, int] = Field(alias="cap")
    password: str | None = None

    @field_validator("hostname")
    @classmethod
    def hostname_validator(cls, value: str) -> str:
        if "-" not in value:
            raise ValueError(f"hostname does not contain a dash: {value}")
        model_name, blid = value.split("-")
        if blid == "":
            raise ValueError(f"empty blid: {value}")
        if model_name.lower() not in {"roomba", "irobot"}:
            raise ValueError(f"unsupported model in hostname: {value}")
        return value

    @cached_property
    def blid(self) -> str:
        return self.hostname.split("-")[1]

    class Config:
        # NOTE: Used to ensure Pydantic v1 backwards compatibility
        #       See https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (cached_property,)

    def __hash__(self) -> int:
        return hash(self.mac)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, RoombaInfo) and self.mac == o.mac

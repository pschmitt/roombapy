"""iRobot-specific serialization utilities."""

from __future__ import annotations

from dataclasses import MISSING, Field, field
from datetime import UTC, datetime
from typing import Any

from mashumaro import field_options
from mashumaro.types import SerializationStrategy


class _IRobotDT(SerializationStrategy):
    _format = "%y%m%dT%H%M%S"

    def deserialize(self, value: str) -> datetime:
        return datetime.strptime(value, self._format).replace(tzinfo=UTC)


class _IRobotTS(SerializationStrategy):
    def deserialize(self, value: int) -> datetime:
        return datetime.fromtimestamp(value, tz=UTC)


def irobot_dt_field(name: str | None = None) -> Field:
    """Shorthand to deserialize a datetime field."""
    if name is None:
        return field(metadata=field_options(serialization_strategy=_IRobotDT()))
    return field(
        metadata=field_options(alias=name, serialization_strategy=_IRobotDT())
    )


def irobot_ts_field(name: str | None = None) -> Field:
    """Shorthand to deserialize a timestamp field."""
    if name is None:
        return field(metadata=field_options(serialization_strategy=_IRobotTS()))
    return field(
        metadata=field_options(alias=name, serialization_strategy=_IRobotTS())
    )


def alias(
    name: str,
    default: Any = MISSING,
    default_factory: Any = MISSING,
) -> Field:
    """Shorthand for aliased field."""
    # noinspection PyArgumentList
    return field(
        metadata=field_options(alias=name),
        default=default,
        default_factory=default_factory,
    )


def check_map_response(payload: dict[str, Any]) -> bool:
    """Check whether map is well-formed."""
    return "active_pmapv_details" in payload

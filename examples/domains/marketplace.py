from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ComponentType(str, Enum):
    SKILL = "skill"
    AGENT = "agent"
    INSTRUCTION = "instruction"
    PROMPT = "prompt"
    HOOK = "hook"


class Availability(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ExternalDependency:
    type: str
    id: str
    name: str
    description: str
    required: bool
    availability: Availability


@dataclass(slots=True)
class Component:
    id: str
    type: ComponentType
    name: str
    description: str
    available_version: str
    release_summary: str
    tags: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    external_dependencies: tuple[ExternalDependency, ...] = ()
    compatible: bool = True
    compatibility_reason: str | None = None
    enabled: bool = False
    applied_version: str | None = None
    conflicts: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Profile:
    id: str
    name: str
    description: str
    version: str
    component_states: dict[str, bool]


@dataclass(frozen=True, slots=True)
class Activity:
    timestamp: datetime
    operation: str
    target_id: str | None
    previous_version: str | None
    new_version: str | None
    result: str
    conflict_count: int
    source_revision: str

    @classmethod
    def now(
        cls,
        *,
        operation: str,
        target_id: str | None,
        source_revision: str,
        previous_version: str | None = None,
        new_version: str | None = None,
        result: str = "succeeded",
        conflict_count: int = 0,
    ) -> "Activity":
        return cls(
            timestamp=datetime.now(timezone.utc),
            operation=operation,
            target_id=target_id,
            previous_version=previous_version,
            new_version=new_version,
            result=result,
            conflict_count=conflict_count,
            source_revision=source_revision,
        )


class MarketplaceError(Exception):
    """Expected domain failure that can safely cross the HTTP boundary."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = 409,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

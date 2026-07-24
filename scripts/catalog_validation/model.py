"""Shared catalog data structures and source projection helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

PAYLOAD_ROOTS = ("agents", "hooks", "instructions", "prompts", "skills")
COMPONENT_TYPE_DIRECTORIES = {
    "agent": "agents",
    "hook": "hooks",
    "instruction": "instructions",
    "prompt": "prompts",
    "skill": "skills",
}


@dataclass(order=True, frozen=True)
class ValidationError:
    manifest: str
    field: str
    message: str

    def render(self) -> str:
        location = f":{self.field}" if self.field else ""
        return f"{self.manifest}{location}: {self.message}"


@dataclass
class LoadedCatalog:
    root: Path
    catalog: dict[str, Any] = field(default_factory=dict)
    components: dict[str, dict[str, Any]] = field(default_factory=dict)
    component_files: dict[str, str] = field(default_factory=dict)
    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    profile_files: dict[str, str] = field(default_factory=dict)
    payload_owners: dict[str, str] = field(default_factory=dict)
    errors: list[ValidationError] = field(default_factory=list)


def declared_source_paths(component: dict[str, Any]) -> list[str]:
    source = component.get("source", {})
    if isinstance(source.get("path"), str):
        return [source["path"]]
    return [path for path in source.get("paths", []) if isinstance(path, str)]


def projected_paths(root: Path, component: dict[str, Any]) -> list[str]:
    source = component.get("source", {})
    if isinstance(source.get("path"), str):
        source_path = source["path"]
        source_root = root / PurePosixPath(source_path)
        if source_root.is_dir():
            return [
                item.relative_to(root).as_posix()
                for item in sorted(source_root.rglob("*"))
                if item.is_file() or item.is_symlink()
            ]
        return [source_path]
    return [path for path in source.get("paths", []) if isinstance(path, str)]


def source_signature(component: dict[str, Any]) -> str:
    return json.dumps(component.get("source"), sort_keys=True, separators=(",", ":"))


def behavior_metadata_signature(component: dict[str, Any]) -> str:
    relevant = {
        key: component.get(key)
        for key in (
            "compatibility",
            "default_state",
            "dependencies",
            "external_dependencies",
            "replaces",
        )
    }
    return json.dumps(relevant, sort_keys=True, separators=(",", ":"))

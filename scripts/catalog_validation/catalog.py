"""Orchestrate AI Context catalog validation."""

from __future__ import annotations

from pathlib import Path

from .loading import load_catalog
from .model import (
    COMPONENT_TYPE_DIRECTORIES,
    PAYLOAD_ROOTS,
    LoadedCatalog,
    ValidationError,
    behavior_metadata_signature,
    projected_paths,
    source_signature,
)
from .paths import validate_paths
from .relations import validate_relations


def validate_catalog(root: Path) -> LoadedCatalog:
    result = load_catalog(root)
    if result.catalog:
        validate_paths(result)
        validate_relations(result)
    result.errors.sort()
    return result


__all__ = [
    "COMPONENT_TYPE_DIRECTORIES",
    "PAYLOAD_ROOTS",
    "LoadedCatalog",
    "ValidationError",
    "behavior_metadata_signature",
    "projected_paths",
    "source_signature",
    "validate_catalog",
]

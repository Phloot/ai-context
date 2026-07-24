"""Validate component source paths, projection, and ownership."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path, PurePosixPath

from .model import (
    LoadedCatalog,
    ValidationError,
    declared_source_paths,
    projected_paths,
)


def validate_paths(result: LoadedCatalog) -> None:
    for component_id, component in sorted(result.components.items()):
        manifest = result.component_files[component_id]
        declared = declared_source_paths(component)
        _validate_source_shapes(result, manifest, component, declared)
        for relative in declared:
            _validate_source_path(result, manifest, relative)
        for source_path in projected_paths(result.root, component):
            _claim_path(
                result, manifest, source_path, component_id, result.payload_owners
            )


def _validate_source_shapes(
    result: LoadedCatalog,
    manifest: str,
    component: dict,
    declared: list[str],
) -> None:
    source = component.get("source", {})
    if "path" in source:
        candidate = result.root / PurePosixPath(source["path"])
        if candidate.exists() and not candidate.is_dir():
            _error(
                result,
                manifest,
                "source.path",
                "must identify a directory; use source.paths for files",
            )
        return
    for index, relative in enumerate(declared):
        if (result.root / PurePosixPath(relative)).is_dir():
            _error(
                result,
                manifest,
                f"source.paths[{index}]",
                "must identify a file; use source.path for a directory",
            )


def _validate_source_path(result: LoadedCatalog, manifest: str, relative: str) -> None:
    canonical = PurePosixPath(relative).as_posix()
    path = result.root / PurePosixPath(canonical)
    if not path.exists() and not path.is_symlink():
        _error(
            result, manifest, "source", f"{relative!r} does not exist; correct the path"
        )
        return
    candidates: Iterable[Path] = path.rglob("*") if path.is_dir() else (path,)
    for candidate in candidates:
        if not candidate.is_symlink():
            continue
        try:
            candidate.resolve(strict=True).relative_to(result.root)
        except (OSError, ValueError):
            relative_candidate = candidate.relative_to(result.root).as_posix()
            _error(
                result,
                manifest,
                "source",
                f"{relative_candidate!r} resolves outside the repository; remove it",
            )


def _claim_path(
    result: LoadedCatalog,
    manifest: str,
    relative: str,
    component_id: str,
    owners: dict[str, str],
) -> None:
    canonical = PurePosixPath(relative).as_posix()
    path = result.root / PurePosixPath(canonical)
    expanded = (
        [
            item.relative_to(result.root).as_posix()
            for item in sorted(path.rglob("*"))
            if item.is_file() or item.is_symlink()
        ]
        if path.is_dir()
        else [canonical]
    )
    for claimed in expanded:
        previous = owners.get(claimed)
        if previous and previous != component_id:
            _error(
                result,
                manifest,
                "source",
                f"{claimed!r} is also owned by {previous!r}; assign one owner",
            )
        else:
            owners[claimed] = component_id


def _error(result: LoadedCatalog, manifest: str, field: str, message: str) -> None:
    result.errors.append(ValidationError(manifest, field, message))

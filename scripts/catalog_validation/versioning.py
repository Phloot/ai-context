"""Validate component versions against a Git base revision."""

from __future__ import annotations

import subprocess
import tarfile
import tempfile
from pathlib import Path

from packaging.version import InvalidVersion, Version

from .catalog import (
    PAYLOAD_ROOTS,
    LoadedCatalog,
    ValidationError,
    behavior_metadata_signature,
    source_signature,
    validate_catalog,
)
from .git_snapshot import changed_paths, extract_revision, merge_base


def validate_version_changes(
    current: LoadedCatalog, base_revision: str
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if current.errors:
        return errors
    try:
        base_commit = merge_base(current.root, base_revision)
        with tempfile.TemporaryDirectory() as temporary:
            base_root = Path(temporary)
            extract_revision(current.root, base_commit, base_root)
            if (base_root / "catalog/catalog.yaml").is_file():
                base = validate_catalog(base_root)
            else:
                base = LoadedCatalog(base_root)
            if base.errors:
                errors.append(
                    ValidationError(
                        base_revision,
                        "",
                        "base revision has an invalid catalog; choose a valid base",
                    )
                )
                return errors
            changed = changed_paths(current.root, base_commit)
            _compare_components(current, base, changed, errors)
            _check_changed_payload_ownership(current, base, changed, errors)
    except (OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        errors.append(
            ValidationError(
                base_revision,
                "",
                f"cannot compare Git revision; verify the revision ({detail.strip()})",
            )
        )
    return sorted(errors)


def _compare_components(
    current: LoadedCatalog,
    base: LoadedCatalog,
    changed: set[str],
    errors: list[ValidationError],
) -> None:
    replacement_ids = {
        replacement.get("id")
        for component in current.components.values()
        for replacement in component.get("replaces", [])
    }
    for component_id, old in sorted(base.components.items()):
        new = current.components.get(component_id)
        if new is None:
            if component_id not in replacement_ids:
                errors.append(
                    ValidationError(
                        base.component_files[component_id],
                        "id",
                        f"component {component_id!r} was removed or renamed; declare replaces",
                    )
                )
            continue
        manifest = current.component_files[component_id]
        old_version = _version(old.get("version"))
        new_version = _version(new.get("version"))
        if (
            old_version is not None
            and new_version is not None
            and new_version < old_version
        ):
            errors.append(
                ValidationError(
                    manifest,
                    "version",
                    f"decreased from {old_version} to {new_version}; increment it",
                )
            )
        payload_changed = any(
            path in changed and owner == component_id
            for path, owner in {**base.payload_owners, **current.payload_owners}.items()
        )
        source_changed = source_signature(old) != source_signature(new)
        metadata_changed = behavior_metadata_signature(
            old
        ) != behavior_metadata_signature(new)
        if (
            payload_changed or source_changed or metadata_changed
        ) and new_version == old_version:
            if payload_changed:
                reason = "payload"
            elif source_changed:
                reason = "source declaration"
            else:
                reason = "dependency or compatibility metadata"
            errors.append(
                ValidationError(
                    manifest,
                    "version",
                    f"{reason} changed without a version change; increment the version",
                )
            )


def _check_changed_payload_ownership(
    current: LoadedCatalog,
    base: LoadedCatalog,
    changed: set[str],
    errors: list[ValidationError],
) -> None:
    owned = set(current.payload_owners) | set(base.payload_owners)
    for path in sorted(changed):
        first_part = path.split("/", 1)[0]
        if first_part in PAYLOAD_ROOTS and path not in owned:
            errors.append(
                ValidationError(
                    path,
                    "",
                    "changed payload has no component owner; add it to a manifest",
                )
            )


def _version(value: object) -> Version | None:
    try:
        return Version(str(value))
    except InvalidVersion:
        return None

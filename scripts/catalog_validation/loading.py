"""Load catalog YAML files and validate them against JSON Schemas."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, RefResolver, SchemaError

from .model import COMPONENT_TYPE_DIRECTORIES, LoadedCatalog, ValidationError


def load_catalog(root: Path) -> LoadedCatalog:
    result = LoadedCatalog(root.resolve())
    schemas = _load_schemas(result)
    if not schemas:
        return result
    result.catalog = _load_document(
        result, "catalog/catalog.yaml", schemas["catalog"], schemas
    )
    _load_components(result, schemas)
    _load_profiles(result, schemas)
    return result


def _load_schemas(result: LoadedCatalog) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name in ("catalog", "component", "profile"):
        relative = f"catalog/schema/{name}.schema.json"
        try:
            with (result.root / relative).open(encoding="utf-8") as source:
                schemas[name] = json.load(source)
        except (OSError, json.JSONDecodeError) as error:
            result.errors.append(
                ValidationError(
                    relative, "", f"cannot load JSON Schema; correct it ({error})"
                )
            )
    if len(schemas) != 3:
        return {}
    for name, schema in sorted(schemas.items()):
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            result.errors.append(
                ValidationError(
                    f"catalog/schema/{name}.schema.json",
                    "",
                    f"is not a valid JSON Schema; correct it ({error.message})",
                )
            )
    return schemas if not result.errors else {}


def _load_document(
    result: LoadedCatalog,
    relative: str,
    schema: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    try:
        with (result.root / relative).open(encoding="utf-8") as source:
            document = yaml.safe_load(source)
    except (OSError, yaml.YAMLError) as error:
        result.errors.append(
            ValidationError(relative, "", f"cannot load YAML; correct it ({error})")
        )
        return {}
    if not isinstance(document, dict):
        result.errors.append(
            ValidationError(relative, "", "must contain a YAML object")
        )
        return {}

    resolver = RefResolver.from_schema(
        schema,
        store={loaded["$id"]: loaded for loaded in schemas.values() if "$id" in loaded},
    )
    validator = Draft202012Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(document), key=_schema_error_key)
    for error in errors:
        result.errors.append(
            ValidationError(
                relative,
                _format_json_path(error.absolute_path),
                f"{error.message}; update the manifest to match the schema",
            )
        )
    return {} if errors else document


def _load_components(result: LoadedCatalog, schemas: dict[str, dict[str, Any]]) -> None:
    component_root = result.root / "catalog/components"
    for path in sorted(component_root.rglob("*.yaml")):
        relative = path.relative_to(result.root).as_posix()
        component = _load_document(result, relative, schemas["component"], schemas)
        component_id = component.get("id")
        component_type = component.get("type")
        if not isinstance(component_id, str):
            continue
        if component_id in result.components:
            result.errors.append(
                ValidationError(
                    relative, "id", f"duplicates component ID {component_id!r}"
                )
            )
            continue
        if path.stem != component_id:
            result.errors.append(
                ValidationError(
                    relative, "id", f"rename the manifest to {component_id}.yaml"
                )
            )
        expected_directory = COMPONENT_TYPE_DIRECTORIES.get(component_type)
        expected_path = (
            component_root / expected_directory / f"{component_id}.yaml"
            if expected_directory
            else None
        )
        if expected_path is not None and path != expected_path:
            result.errors.append(
                ValidationError(
                    relative,
                    "type",
                    "move the manifest to "
                    f"{expected_path.relative_to(result.root).as_posix()}",
                )
            )
        result.components[component_id] = component
        result.component_files[component_id] = relative


def _load_profiles(result: LoadedCatalog, schemas: dict[str, dict[str, Any]]) -> None:
    for path in sorted((result.root / "catalog/profiles").glob("*.yaml")):
        relative = path.relative_to(result.root).as_posix()
        profile = _load_document(result, relative, schemas["profile"], schemas)
        profile_id = profile.get("id")
        if not isinstance(profile_id, str):
            continue
        if profile_id in result.profiles:
            result.errors.append(
                ValidationError(relative, "id", f"duplicates profile ID {profile_id!r}")
            )
            continue
        if path.stem != profile_id:
            result.errors.append(
                ValidationError(
                    relative, "id", f"rename the profile to {profile_id}.yaml"
                )
            )
        result.profiles[profile_id] = profile
        result.profile_files[profile_id] = relative


def _schema_error_key(error: Any) -> tuple[str, str]:
    return (_format_json_path(error.absolute_path), error.message)


def _format_json_path(parts: Iterable[Any]) -> str:
    output = ""
    for part in parts:
        output += (
            f"[{part}]"
            if isinstance(part, int)
            else ("." if output else "") + str(part)
        )
    return output

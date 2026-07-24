"""Validate dependencies, dependency graphs, and profile references."""

from __future__ import annotations

from typing import Any

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from .model import LoadedCatalog, ValidationError


def validate_relations(result: LoadedCatalog) -> None:
    graph: dict[str, list[str]] = {}
    for component_id, component in sorted(result.components.items()):
        manifest = result.component_files[component_id]
        graph[component_id] = []
        seen: set[str] = set()
        for index, dependency in enumerate(component.get("dependencies", [])):
            dependency_id = dependency.get("id")
            field = f"dependencies[{index}]"
            if not isinstance(dependency_id, str):
                continue
            if dependency_id in seen:
                _error(result, manifest, field, "duplicates a dependency; remove it")
            seen.add(dependency_id)
            if dependency_id == component_id:
                _error(result, manifest, field, "cannot depend on itself")
                continue
            target = result.components.get(dependency_id)
            if target is None:
                _error(
                    result,
                    manifest,
                    field,
                    f"references missing component {dependency_id!r}",
                )
                continue
            graph[component_id].append(dependency_id)
            constraint = dependency.get("version")
            if constraint:
                _validate_constraint(
                    result, manifest, field, constraint, target.get("version")
                )
        _validate_external_dependencies(result, manifest, component)
    _detect_cycles(result, graph)
    _validate_profiles(result)


def _validate_external_dependencies(
    result: LoadedCatalog, manifest: str, component: dict[str, Any]
) -> None:
    seen: set[tuple[str, str]] = set()
    for index, dependency in enumerate(component.get("external_dependencies", [])):
        dependency_type = dependency.get("type")
        dependency_id = dependency.get("id")
        if not isinstance(dependency_type, str) or not isinstance(dependency_id, str):
            continue
        field = f"external_dependencies[{index}]"
        key = (dependency_type, dependency_id)
        if key in seen:
            _error(
                result,
                manifest,
                field,
                "duplicates an external dependency; remove it",
            )
        seen.add(key)
        constraint = dependency.get("version")
        if constraint:
            _validate_constraint(result, manifest, field, constraint, None)


def _validate_constraint(
    result: LoadedCatalog,
    manifest: str,
    field: str,
    constraint: Any,
    available_version: Any,
) -> None:
    try:
        specifier = SpecifierSet(constraint)
    except (InvalidSpecifier, TypeError):
        _error(
            result,
            manifest,
            field,
            f"{constraint!r} is not a valid version constraint",
        )
        return
    try:
        satisfied = Version(available_version) in specifier
    except (InvalidVersion, TypeError):
        return
    if not satisfied:
        _error(
            result,
            manifest,
            field,
            f"{constraint!r} does not allow available version {available_version}",
        )


def _detect_cycles(result: LoadedCatalog, graph: dict[str, list[str]]) -> None:
    visited: set[str] = set()
    active: list[str] = []

    def visit(component_id: str) -> None:
        if component_id in active:
            cycle = active[active.index(component_id) :] + [component_id]
            _error(
                result,
                result.component_files[component_id],
                "dependencies",
                f"dependency cycle {' -> '.join(cycle)}; remove one edge",
            )
            return
        if component_id in visited:
            return
        active.append(component_id)
        for dependency_id in sorted(graph.get(component_id, [])):
            visit(dependency_id)
        active.pop()
        visited.add(component_id)

    for component_id in sorted(graph):
        visit(component_id)


def _validate_profiles(result: LoadedCatalog) -> None:
    for profile_id, profile in sorted(result.profiles.items()):
        manifest = result.profile_files[profile_id]
        seen: set[str] = set()
        for index, entry in enumerate(profile.get("components", [])):
            component_id = entry.get("id")
            field = f"components[{index}]"
            if not isinstance(component_id, str):
                continue
            if component_id in seen:
                _error(result, manifest, field, "duplicates a component; remove it")
            elif component_id not in result.components:
                _error(
                    result,
                    manifest,
                    field,
                    f"references missing component {component_id!r}",
                )
            seen.add(component_id)


def _error(result: LoadedCatalog, manifest: str, field: str, message: str) -> None:
    result.errors.append(ValidationError(manifest, field, message))

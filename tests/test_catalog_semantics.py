from __future__ import annotations

import copy
import unittest

from catalog_test_support import (
    CatalogFixtureTest,
    read_yaml,
    rendered,
    write_yaml,
)
from catalog_validation.catalog import validate_catalog
from catalog_validation.model import projected_paths


class CatalogSemanticTests(CatalogFixtureTest):
    def test_missing_source_is_reported(self) -> None:
        component = self.component("maintainable-code")
        component["source"]["path"] = "skills/missing"
        self.write_component("maintainable-code", component)
        self.assertContains(
            rendered(validate_catalog(self.root).errors), "does not exist"
        )

    @unittest.skipIf(not hasattr(__import__("os"), "symlink"), "symlinks unavailable")
    def test_outside_symlink_is_rejected(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.txt"
        outside.write_text("outside", encoding="utf-8")
        link = self.root / "skills/maintainable-code/outside.txt"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"cannot create symlink: {error}")
        self.addCleanup(outside.unlink, missing_ok=True)
        self.assertContains(
            rendered(validate_catalog(self.root).errors), "resolves outside"
        )

    def test_sources_project_to_the_same_relative_paths(self) -> None:
        component = self.component("maintainability-hooks")
        self.assertEqual(
            [
                "hooks/maintainability-hooks.json",
                "hooks/scripts/maintainability_subagent_context.py",
            ],
            projected_paths(self.root, component),
        )

    def test_payload_ownership_collisions_are_reported(self) -> None:
        duplicate = copy.deepcopy(self.component("maintainable-code"))
        duplicate["id"] = "other-skill"
        duplicate["name"] = "Other Skill"
        self.write_component("other-skill", duplicate)
        self.assertContains(
            rendered(validate_catalog(self.root).errors), "also owned by"
        )

    def test_missing_and_self_dependencies_are_reported(self) -> None:
        component = self.component("maintainability-hooks")
        component["dependencies"] = [
            {"id": "missing"},
            {"id": "maintainability-hooks"},
        ]
        self.write_component("maintainability-hooks", component)
        errors = rendered(validate_catalog(self.root).errors)
        self.assertContains(errors, "references missing component")
        self.assertContains(errors, "cannot depend on itself")

    def test_duplicate_dependencies_are_rejected(self) -> None:
        component = self.component("maintainability-hooks")
        component["dependencies"].append(copy.deepcopy(component["dependencies"][0]))
        self.write_component("maintainability-hooks", component)
        self.assertContains(
            rendered(validate_catalog(self.root).errors), "has non-unique elements"
        )

    def test_dependency_cycle_is_reported(self) -> None:
        component = self.component("maintainable-code")
        component["dependencies"] = [{"id": "maintainability-hooks"}]
        self.write_component("maintainable-code", component)
        self.assertContains(
            rendered(validate_catalog(self.root).errors), "dependency cycle"
        )

    def test_invalid_and_unsatisfied_constraints_are_reported(self) -> None:
        component = self.component("maintainability-hooks")
        component["dependencies"] = [
            {"id": "maintainable-code", "version": "not-a-constraint"},
            {"id": "maintainable-code", "version": ">=2.0.0"},
        ]
        self.write_component("maintainability-hooks", component)
        errors = rendered(validate_catalog(self.root).errors)
        self.assertContains(errors, "not a valid version constraint")
        self.assertContains(errors, "does not allow available version")

    def test_external_dependencies_are_unique_and_have_valid_constraints(self) -> None:
        component = self.component("maintainable-code")
        requirement = {
            "type": "mcp",
            "id": "intellij",
            "name": "IntelliJ MCP",
            "description": "Provides IDE search.",
            "required": True,
            "version": "not-a-constraint",
        }
        duplicate = requirement.copy()
        duplicate["description"] = "The same MCP requirement."
        component["external_dependencies"] = [requirement, duplicate]
        self.write_component("maintainable-code", component)

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "duplicates an external dependency")
        self.assertContains(errors, "not a valid version constraint")

    def test_invalid_profile_entries_are_reported(self) -> None:
        profile_path = self.root / "catalog/profiles/maintainable-development.yaml"
        profile = read_yaml(profile_path)
        profile["components"] = [
            {"id": "missing", "enabled": True},
            {"id": "missing", "enabled": False},
        ]
        write_yaml(profile_path, profile)
        errors = rendered(validate_catalog(self.root).errors)
        self.assertContains(errors, "references missing component")
        self.assertContains(errors, "duplicates a component")

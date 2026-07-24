from __future__ import annotations

import shutil

from catalog_test_support import (
    REPOSITORY_ROOT,
    CatalogFixtureTest,
    read_yaml,
    rendered,
    run_git,
    write_yaml,
)
from catalog_validation.catalog import validate_catalog
from catalog_validation.versioning import validate_version_changes


class VersionChangeTests(CatalogFixtureTest):
    def setUp(self) -> None:
        super().setUp()
        run_git(self.root, "init")
        run_git(self.root, "config", "user.email", "catalog-tests@example.invalid")
        run_git(self.root, "config", "user.name", "Catalog Tests")
        run_git(self.root, "add", ".")
        run_git(self.root, "commit", "-m", "base")
        self.base = run_git(self.root, "rev-parse", "HEAD").strip()

    def test_payload_change_requires_version_change(self) -> None:
        payload = self.root / "skills/maintainable-code/SKILL.md"
        payload.write_text(payload.read_text(encoding="utf-8") + "\nchange\n")
        self.assertContains(
            self.version_errors(), "payload changed without a version change"
        )

    def test_version_decrease_is_rejected(self) -> None:
        component = self.component("maintainable-code")
        component["version"] = "0.9.0"
        self.write_component("maintainable-code", component)
        hook = self.component("maintainability-hooks")
        hook["dependencies"][0]["version"] = ">=0.9.0,<2.0.0"
        self.write_component("maintainability-hooks", hook)
        self.assertContains(self.version_errors(), "decreased from")

    def test_source_change_requires_version_change(self) -> None:
        component = self.component("maintainable-code")
        component["source"]["path"] = "skills"
        self.write_component("maintainable-code", component)
        self.assertContains(self.version_errors(), "source declaration changed")

    def test_component_rename_requires_replacement(self) -> None:
        old = self.component_path("maintainable-code")
        component = read_yaml(old)
        component["id"] = "renamed-skill"
        component["version"] = "2.0.0"
        old.unlink()
        self.write_component("renamed-skill", component)
        hook = self.component("maintainability-hooks")
        hook["dependencies"][0] = {"id": "renamed-skill", "version": ">=2.0.0"}
        self.write_component("maintainability-hooks", hook)
        profile_path = self.root / "catalog/profiles/maintainable-development.yaml"
        profile = read_yaml(profile_path)
        profile["components"][0]["id"] = "renamed-skill"
        write_yaml(profile_path, profile)
        self.assertContains(self.version_errors(), "was removed or renamed")

    def test_unowned_payload_change_is_rejected(self) -> None:
        directory = self.root / "prompts"
        directory.mkdir()
        (directory / "new.prompt.md").write_text("prompt", encoding="utf-8")
        run_git(self.root, "add", ".")
        self.assertContains(
            self.version_errors(), "changed payload has no component owner"
        )

    def test_initial_catalog_can_compare_with_pre_catalog_revision(self) -> None:
        pre_catalog = self.root.parent / (self.root.name + "-pre-catalog")
        pre_catalog.mkdir()
        self.addCleanup(shutil.rmtree, pre_catalog, ignore_errors=True)
        (pre_catalog / "README.md").write_text("base", encoding="utf-8")
        run_git(pre_catalog, "init")
        run_git(pre_catalog, "config", "user.email", "catalog-tests@example.invalid")
        run_git(pre_catalog, "config", "user.name", "Catalog Tests")
        run_git(pre_catalog, "add", ".")
        run_git(pre_catalog, "commit", "-m", "base")
        base = run_git(pre_catalog, "rev-parse", "HEAD").strip()
        for name in ("catalog", "skills", "hooks"):
            shutil.copytree(
                REPOSITORY_ROOT / name,
                pre_catalog / name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
        run_git(pre_catalog, "add", ".")
        catalog = validate_catalog(pre_catalog)
        self.assertEqual([], rendered(validate_version_changes(catalog, base)))

    def test_version_increment_allows_payload_change(self) -> None:
        payload = self.root / "skills/maintainable-code/SKILL.md"
        payload.write_text(payload.read_text(encoding="utf-8") + "\nchange\n")
        component = self.component("maintainable-code")
        component["version"] = "1.1.0"
        self.write_component("maintainable-code", component)
        self.assertEqual([], self.version_errors())

    def test_external_dependency_change_requires_version_change(self) -> None:
        component = self.component("maintainable-code")
        component["external_dependencies"] = [
            {
                "type": "mcp",
                "id": "intellij",
                "name": "IntelliJ MCP",
                "description": "Provides IDE search.",
                "required": True,
            }
        ]
        self.write_component("maintainable-code", component)

        self.assertContains(
            self.version_errors(), "dependency or compatibility metadata changed"
        )

    def version_errors(self) -> list[str]:
        catalog = validate_catalog(self.root)
        self.assertEqual([], rendered(catalog.errors))
        return rendered(validate_version_changes(catalog, self.base))

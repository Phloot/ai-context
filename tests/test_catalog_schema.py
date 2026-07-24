from __future__ import annotations

from catalog_test_support import CatalogFixtureTest, rendered, write_yaml
from catalog_validation.catalog import validate_catalog


class CatalogSchemaTests(CatalogFixtureTest):
    def test_repository_catalog_is_valid(self) -> None:
        catalog = validate_catalog(self.root)
        self.assertEqual([], rendered(catalog.errors))

    def test_invalid_yaml_is_reported(self) -> None:
        manifest = self.component_path("maintainable-code")
        manifest.write_text("id: [\n", encoding="utf-8")

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "cannot load YAML")

    def test_schema_violation_is_reported(self) -> None:
        component = self.component("maintainable-code")
        component["unexpected"] = True
        self.write_component("maintainable-code", component)

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "Additional properties are not allowed")

    def test_schema_type_violation_does_not_crash_semantic_validation(self) -> None:
        component = self.component("maintainable-code")
        component["source"] = "skills/maintainable-code"
        self.write_component("maintainable-code", component)

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "not valid under any")

    def test_invalid_json_schema_is_reported(self) -> None:
        schema = self.root / "catalog/schema/catalog.schema.json"
        schema.write_text('{"type": "not-a-json-schema-type"}', encoding="utf-8")

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "is not a valid JSON Schema")

    def test_duplicate_id_is_reported(self) -> None:
        duplicate = self.component("maintainable-code")
        duplicate["type"] = "hook"
        write_yaml(
            self.root / "catalog/components/hooks/duplicate.yaml",
            duplicate,
        )

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "duplicates component ID")

    def test_manifest_directory_must_match_component_type(self) -> None:
        component = self.component("maintainable-code")
        source = self.component_path("maintainable-code")
        source.unlink()
        write_yaml(
            self.root / "catalog/components/hooks/maintainable-code.yaml",
            component,
        )

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(
            errors,
            "move the manifest to catalog/components/skills/maintainable-code.yaml",
        )

    def test_invalid_id_and_version_are_reported(self) -> None:
        component = self.component("maintainable-code")
        component["id"] = "Bad ID"
        component["version"] = "next"
        self.write_component("maintainable-code", component)

        errors = rendered(validate_catalog(self.root).errors)

        self.assertContains(errors, "does not match")

    def test_unsafe_paths_are_rejected_by_schema(self) -> None:
        for unsafe in ("/tmp/payload", "../payload", "C:/payload"):
            with self.subTest(path=unsafe):
                component = self.component("maintainable-code")
                component["source"]["path"] = unsafe
                self.write_component("maintainable-code", component)
                errors = rendered(validate_catalog(self.root).errors)
                self.assertContains(errors, "not valid under any")

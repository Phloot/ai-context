from __future__ import annotations

import unittest

from catalog_test_support import CatalogFixtureTest, rendered
from catalog_validation.cue_schema import check_cue_contract, find_cue


class CueSchemaTests(CatalogFixtureTest):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            find_cue()
        except RuntimeError as error:
            raise unittest.SkipTest(str(error)) from error

    def test_generated_schemas_match_cue(self) -> None:
        self.assertEqual([], rendered(check_cue_contract(self.root)))

    def test_generated_schema_drift_is_reported(self) -> None:
        schema = self.root / "catalog/schema/catalog.schema.json"
        schema.write_text(
            schema.read_text(encoding="utf-8").replace(
                "AI Context Catalog", "Stale Catalog"
            ),
            encoding="utf-8",
        )

        errors = rendered(check_cue_contract(self.root))

        self.assertContains(errors, "does not match catalog.cue")

    def test_invalid_cue_schema_is_reported(self) -> None:
        schema = self.root / "catalog/schema/catalog.cue"
        schema.write_text(
            schema.read_text(encoding="utf-8") + "\ninvalid: {\n",
            encoding="utf-8",
        )

        errors = rendered(check_cue_contract(self.root))

        self.assertContains(errors, "CUE validation failed")

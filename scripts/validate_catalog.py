#!/usr/bin/env python3
"""Validate the AI Context catalog and optional component version changes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from catalog_validation.catalog import validate_catalog
    from catalog_validation.cue_schema import check_cue_contract
    from catalog_validation.versioning import validate_version_changes
except ModuleNotFoundError as error:
    if error.name in {"jsonschema", "packaging", "yaml"}:
        print(
            f"error: missing validation dependency {error.name!r}; run 'uv sync'",
            file=sys.stderr,
        )
        raise SystemExit(2) from error
    raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to the parent of this script directory.",
    )
    parser.add_argument(
        "--base",
        help="Git revision used to validate component version changes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = validate_catalog(args.root)
    errors = check_cue_contract(args.root)
    errors.extend(catalog.errors)
    if args.base and not errors:
        errors.extend(validate_version_changes(catalog, args.base))
    if errors:
        for error in sorted(errors):
            print(f"error: {error.render()}", file=sys.stderr)
        print(
            f"Catalog validation failed with {len(errors)} error(s).", file=sys.stderr
        )
        return 1
    print(
        "Catalog validation passed: "
        f"{len(catalog.components)} component(s), "
        f"{len(catalog.profiles)} profile(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

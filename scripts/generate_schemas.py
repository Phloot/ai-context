#!/usr/bin/env python3
"""Generate committed JSON Schemas from the authoritative CUE definitions."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from catalog_validation.cue_schema import check_cue_contract, write_schemas

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check generated files without changing them.",
    )
    args = parser.parse_args()
    if args.check:
        errors = check_cue_contract(ROOT)
        for error in errors:
            print(f"error: {error.render()}", file=sys.stderr)
        return 1 if errors else 0
    try:
        write_schemas(ROOT)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        print(f"error: {detail.strip()}", file=sys.stderr)
        return 2
    print("Generated 3 JSON Schemas from catalog/schema/catalog.cue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

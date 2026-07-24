"""Generate and validate the published JSON Schemas from CUE."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .model import ValidationError

CUE_VERSION = "v0.17.1"
SCHEMAS = {
    "catalog": ("#Catalog", "AI Context Catalog"),
    "component": ("#Component", "AI Context Component"),
    "profile": ("#Profile", "AI Context Profile"),
}


def find_cue() -> str:
    configured = os.environ.get("CUE_BIN")
    executable = configured or shutil.which("cue")
    if not executable:
        raise RuntimeError(f"CUE {CUE_VERSION} is required; install it or set CUE_BIN")
    completed = _run([executable, "version"])
    first_line = completed.stdout.splitlines()[0] if completed.stdout else ""
    if first_line != f"cue version {CUE_VERSION}":
        raise RuntimeError(
            f"CUE {CUE_VERSION} is required, but {first_line or 'version is unknown'}"
        )
    return executable


def generate_schemas(root: Path, cue: str) -> dict[str, dict[str, Any]]:
    source = root / "catalog/schema/catalog.cue"
    generated: dict[str, dict[str, Any]] = {}
    for name, (definition, title) in SCHEMAS.items():
        completed = _run(
            [
                cue,
                "def",
                "--out",
                "jsonschema",
                "-e",
                definition,
                str(source),
            ],
            cwd=root,
        )
        schema = json.loads(completed.stdout)
        schema["$id"] = f"{name}.schema.json"
        schema["title"] = title
        generated[name] = schema
    return generated


def check_cue_contract(root: Path) -> list[ValidationError]:
    try:
        cue = find_cue()
        generated = generate_schemas(root, cue)
        errors = _compare_generated_schemas(root, generated)
        errors.extend(_vet_manifests(root, cue))
        return sorted(errors)
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        return [
            ValidationError(
                "catalog/schema/catalog.cue",
                "",
                f"CUE validation failed; correct the schema or tool setup ({detail.strip()})",
            )
        ]


def write_schemas(root: Path) -> None:
    cue = find_cue()
    for name, schema in generate_schemas(root, cue).items():
        path = root / f"catalog/schema/{name}.schema.json"
        path.write_text(
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def _compare_generated_schemas(
    root: Path, generated: dict[str, dict[str, Any]]
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for name, expected in sorted(generated.items()):
        relative = f"catalog/schema/{name}.schema.json"
        try:
            actual = json.loads((root / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            actual = None
        if actual != expected:
            errors.append(
                ValidationError(
                    relative,
                    "",
                    "does not match catalog.cue; run python scripts/generate_schemas.py",
                )
            )
    return errors


def _vet_manifests(root: Path, cue: str) -> list[ValidationError]:
    source = str(root / "catalog/schema/catalog.cue")
    groups = (
        ("#Catalog", [root / "catalog/catalog.yaml"]),
        ("#Component", sorted((root / "catalog/components").rglob("*.yaml"))),
        ("#Profile", sorted((root / "catalog/profiles").glob("*.yaml"))),
    )
    errors: list[ValidationError] = []
    for definition, paths in groups:
        completed = _run(
            [cue, "vet", "-c", "-d", definition, source, *map(str, paths)],
            cwd=root,
            check=False,
        )
        if completed.returncode:
            errors.append(
                ValidationError(
                    "catalog/schema/catalog.cue",
                    definition,
                    f"manifest validation failed; correct the reported fields ({completed.stderr.strip()})",
                )
            )
    return errors


def _run(
    command: list[str], cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )

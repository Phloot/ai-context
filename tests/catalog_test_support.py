from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
if str(SCRIPTS) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(SCRIPTS))


class CatalogFixtureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for name in ("catalog", "skills", "hooks"):
            shutil.copytree(REPOSITORY_ROOT / name, self.root / name)
        shutil.copytree(REPOSITORY_ROOT / "cue.mod", self.root / "cue.mod")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def component(self, component_id: str) -> dict:
        return read_yaml(self.component_path(component_id))

    def write_component(self, filename: str, component: dict) -> None:
        directory = f"{component['type']}s"
        write_yaml(
            self.root / f"catalog/components/{directory}/{filename}.yaml", component
        )

    def component_path(self, component_id: str) -> Path:
        matches = list((self.root / "catalog/components").rglob(f"{component_id}.yaml"))
        if len(matches) != 1:
            self.fail(
                f"expected one manifest for {component_id!r}, found {len(matches)}"
            )
        return matches[0]

    def assertContains(self, errors: list[str], expected: str) -> None:
        self.assertTrue(
            any(expected in error for error in errors),
            f"{expected!r} not found in:\n" + "\n".join(errors),
        )


def read_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def write_yaml(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as destination:
        yaml.safe_dump(document, destination, sort_keys=False)


def rendered(errors: list) -> list[str]:
    return [error.render() for error in errors]


def run_git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

#!/usr/bin/env python3
"""Create a lightweight inventory of Python and Java test files."""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


IGNORED_DIRECTORIES = {
    ".git",
    ".gradle",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}

JAVA_TEST_FILE = re.compile(r"(?:Test|Tests|TestCase|IT)\.java$")
JAVA_TEST_ANNOTATION = re.compile(r"@(?:ParameterizedTest|RepeatedTest|Test)\b")
JAVA_DISABLED = re.compile(r"@(?:Disabled|Ignore)\b")
JAVA_ASSERTION = re.compile(
    r"\b(?:assert[A-Z]\w*|assertThat|fail|verify|verifyNoInteractions|verifyNoMoreInteractions)\s*\("
)
JAVA_MOCK = re.compile(r"(?:@Mock\b|\bMockito\.|\bmock\s*\(|\bspy\s*\(|\bwhen\s*\()")


@dataclass(frozen=True)
class FileInventory:
    path: str
    language: str
    lines: int
    tests: int
    assertions: int
    disabled: int
    mock_signals: int
    tests_without_assertion: tuple[str, ...] = ()


class PythonTestVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.tests = 0
        self.assertions = 0
        self.disabled = 0
        self.mock_signals = 0
        self.tests_without_assertion: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_test_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_test_function(node)

    def _visit_test_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if not node.name.startswith("test"):
            self.generic_visit(node)
            return

        self.tests += 1
        assertion_count = sum(1 for item in ast.walk(node) if self._is_assertion(item))
        self.assertions += assertion_count
        if assertion_count == 0:
            self.tests_without_assertion.append(node.name)

        decorators = " ".join(ast.unparse(item) for item in node.decorator_list)
        if "skip" in decorators or "xfail" in decorators:
            self.disabled += 1

        self.mock_signals += sum(1 for item in ast.walk(node) if self._is_mock_signal(item))

    @staticmethod
    def _is_assertion(node: ast.AST) -> bool:
        if isinstance(node, ast.Assert):
            return True
        if not isinstance(node, ast.Call):
            return False

        name = PythonTestVisitor._call_name(node.func)
        assertion_name = name.rsplit(".", 1)[-1]
        return assertion_name.startswith("assert") or name in {
            "fail",
            "pytest.fail",
            "pytest.raises",
            "pytest.warns",
        }

    @staticmethod
    def _is_mock_signal(node: ast.AST) -> bool:
        if not isinstance(node, ast.Call):
            return False
        name = PythonTestVisitor._call_name(node.func)
        return name in {
            "Mock",
            "MagicMock",
            "AsyncMock",
            "mock.patch",
            "patch",
            "patch.object",
        } or name.startswith("monkeypatch.")

    @staticmethod
    def _call_name(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = PythonTestVisitor._call_name(node.value)
            return f"{prefix}.{node.attr}" if prefix else node.attr
        return ""


def iter_test_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        if path.suffix == ".py" and (
            path.name.startswith("test_") or path.name.endswith("_test.py")
        ):
            yield path
        elif path.suffix == ".java" and JAVA_TEST_FILE.search(path.name):
            yield path


def inventory_python(path: Path, root: Path) -> FileInventory:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return FileInventory(
            path=str(path.relative_to(root)),
            language="python-unparsed",
            lines=len(text.splitlines()),
            tests=0,
            assertions=0,
            disabled=0,
            mock_signals=0,
        )

    visitor = PythonTestVisitor()
    visitor.visit(tree)
    return FileInventory(
        path=str(path.relative_to(root)),
        language="python",
        lines=len(text.splitlines()),
        tests=visitor.tests,
        assertions=visitor.assertions,
        disabled=visitor.disabled,
        mock_signals=visitor.mock_signals,
        tests_without_assertion=tuple(visitor.tests_without_assertion),
    )


def inventory_java(path: Path, root: Path) -> FileInventory:
    text = path.read_text(encoding="utf-8", errors="replace")
    return FileInventory(
        path=str(path.relative_to(root)),
        language="java",
        lines=len(text.splitlines()),
        tests=len(JAVA_TEST_ANNOTATION.findall(text)),
        assertions=len(JAVA_ASSERTION.findall(text)),
        disabled=len(JAVA_DISABLED.findall(text)),
        mock_signals=len(JAVA_MOCK.findall(text)),
    )


def collect(root: Path) -> list[FileInventory]:
    inventory: list[FileInventory] = []
    for path in sorted(iter_test_files(root)):
        if path.suffix == ".py":
            inventory.append(inventory_python(path, root))
        else:
            inventory.append(inventory_java(path, root))
    return inventory


def summarize(items: list[FileInventory]) -> dict[str, object]:
    return {
        "files": len(items),
        "tests": sum(item.tests for item in items),
        "assertions": sum(item.assertions for item in items),
        "disabled": sum(item.disabled for item in items),
        "mock_signals": sum(item.mock_signals for item in items),
        "tests_without_assertion": sum(len(item.tests_without_assertion) for item in items),
    }


def render_text(items: list[FileInventory]) -> str:
    summary = summarize(items)
    lines = [
        "Test inventory",
        (
            f"Files: {summary['files']}  Tests: {summary['tests']}  "
            f"Assertions: {summary['assertions']}  Disabled: {summary['disabled']}  "
            f"Mock signals: {summary['mock_signals']}"
        ),
    ]
    for item in items:
        lines.append(
            f"{item.path}: tests={item.tests}, assertions={item.assertions}, "
            f"disabled={item.disabled}, mock_signals={item.mock_signals}"
        )
        if item.tests_without_assertion:
            names = ", ".join(item.tests_without_assertion)
            lines.append(f"  candidate tests without assertions: {names}")
    lines.append("Counts are review leads. Inspect production behavior before making a finding.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory Python and Java tests without judging test quality."
    )
    parser.add_argument("root", type=Path, help="Repository root to scan.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {root}")

    items = collect(root)
    if args.format == "json":
        payload = {"summary": summarize(items), "files": [asdict(item) for item in items]}
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

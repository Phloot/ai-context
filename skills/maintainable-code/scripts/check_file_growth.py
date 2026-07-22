#!/usr/bin/env python3
"""Check source-file size and growth against a local Git baseline."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_EXTENSIONS = {
    ".groovy",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".py",
    ".ts",
    ".tsx",
}

DEFAULT_EXCLUDES = (
    "build/**",
    "**/build/**",
    "dist/**",
    "**/dist/**",
    "generated/**",
    "**/generated/**",
    "node_modules/**",
    "**/node_modules/**",
    "target/**",
    "**/target/**",
    "vendor/**",
    "**/vendor/**",
)


@dataclass(frozen=True)
class FileChange:
    path: str
    additions: int
    deletions: int
    untracked: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check changed source files for excessive size or growth."
    )
    parser.add_argument(
        "--base",
        default="HEAD",
        help="Git revision used as the comparison baseline. Default: HEAD.",
    )
    parser.add_argument("--max-file-lines", type=int, default=600)
    parser.add_argument("--max-added-lines", type=int, default=200)
    parser.add_argument("--max-growth-percent", type=float, default=50.0)
    parser.add_argument(
        "--min-baseline-lines",
        type=int,
        default=100,
        help="Minimum old file size before the percentage limit applies.",
    )
    parser.add_argument(
        "--extension",
        action="append",
        default=[],
        help="Add a source extension, such as .scala. Repeat for multiple extensions.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Add an excluded path pattern. Repeat for multiple patterns.",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Print violations but return a successful exit status.",
    )
    return parser.parse_args()


def run_git(root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode(errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return completed.stdout


def find_repository_root() -> Path:
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError("the current directory is not in a Git repository")
    return Path(completed.stdout.strip()).resolve()


def read_changes(root: Path, base: str) -> dict[str, FileChange]:
    merge_base = run_git(root, "merge-base", base, "HEAD").decode().strip()
    output = run_git(root, "diff", "--numstat", "--no-renames", merge_base, "--")
    changes: dict[str, FileChange] = {}
    for line in output.decode(errors="replace").splitlines():
        additions_text, deletions_text, path = line.split("\t", 2)
        if additions_text == "-" or deletions_text == "-":
            continue
        changes[path] = FileChange(path, int(additions_text), int(deletions_text))

    untracked_output = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    for raw_path in untracked_output.decode(errors="replace").split("\0"):
        if not raw_path:
            continue
        file_path = root / raw_path
        additions = count_lines(file_path) if file_path.is_file() else 0
        changes[raw_path] = FileChange(raw_path, additions, 0, untracked=True)
    return changes


def count_lines(path: Path) -> int:
    with path.open("rb") as source:
        return sum(1 for _ in source)


def is_excluded(path: str, patterns: tuple[str, ...]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def normalize_extensions(values: list[str]) -> set[str]:
    extensions = set(DEFAULT_EXTENSIONS)
    for value in values:
        extensions.add(value if value.startswith(".") else f".{value}")
    return extensions


def main() -> int:
    args = parse_args()
    try:
        root = find_repository_root()
        changes = read_changes(root, args.base)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    extensions = normalize_extensions(args.extension)
    excludes = (*DEFAULT_EXCLUDES, *args.exclude)
    violations: list[str] = []
    checked = 0

    for change in sorted(changes.values(), key=lambda item: item.path):
        path = Path(change.path)
        if path.suffix.lower() not in extensions or is_excluded(change.path, excludes):
            continue
        absolute_path = root / path
        if not absolute_path.is_file():
            continue

        checked += 1
        current_lines = count_lines(absolute_path)
        baseline_lines = max(0, current_lines - change.additions + change.deletions)
        growth_percent = (
            (current_lines - baseline_lines) / baseline_lines * 100
            if baseline_lines
            else 100.0
        )

        reasons: list[str] = []
        if current_lines > args.max_file_lines:
            reasons.append(f"{current_lines} lines > {args.max_file_lines}")
        if change.additions > args.max_added_lines:
            reasons.append(f"{change.additions} added lines > {args.max_added_lines}")
        if (
            baseline_lines >= args.min_baseline_lines
            and growth_percent > args.max_growth_percent
        ):
            reasons.append(
                f"{growth_percent:.1f}% growth > {args.max_growth_percent:.1f}%"
            )
        if reasons:
            violations.append(f"{change.path}: " + "; ".join(reasons))

    print(f"Checked {checked} changed source file(s) against the merge base of {args.base}.")
    if not violations:
        print("File growth check passed.")
        return 0

    print("File growth review required:", file=sys.stderr)
    for violation in violations:
        print(f"- {violation}", file=sys.stderr)
    print(
        "Review file responsibility before changing a threshold or adding an exclusion.",
        file=sys.stderr,
    )
    return 0 if args.warn_only else 1


if __name__ == "__main__":
    raise SystemExit(main())

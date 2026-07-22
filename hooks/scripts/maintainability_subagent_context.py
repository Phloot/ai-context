#!/usr/bin/env python3
"""Add maintainability guidance to delegated Copilot agent tasks."""

from __future__ import annotations

import json


CONTEXT = (
    "If this delegated task plans, writes, modifies, refactors, or reviews "
    "production code, invoke the /maintainable-code skill before implementation. "
    "Apply its feedback checkpoints after each coherent implementation slice and "
    "its final checkpoint before completion. If this task only explores or "
    "researches the repository, continue without invoking the skill."
)


def main() -> None:
    print(json.dumps({"additionalContext": CONTEXT}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Add maintainability guidance to delegated Copilot agent tasks."""

from __future__ import annotations

import json


CONTEXT = (
    "If this delegated task changes code or executable configuration, invoke "
    "the /maintainable-code skill before implementation. Apply the skill to "
    "application code, libraries, scripts, build logic, deployment logic, "
    "infrastructure code, migrations, and tests. Apply its feedback checkpoint "
    "after each coherent implementation slice and its final checkpoint before "
    "completion. Skip the skill only for documentation-only work, exploration "
    "without edits, or generated and vendored code outside the task scope."
)


def main() -> None:
    print(json.dumps({"additionalContext": CONTEXT}))


if __name__ == "__main__":
    main()

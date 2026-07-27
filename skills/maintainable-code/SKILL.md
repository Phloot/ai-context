---
name: maintainable-code
description: Prevent structural decay during tasks that plan, write, modify, refactor, or review code. Use before implementation, after each coherent slice, and before completion. Detect mixed responsibilities, inappropriate dependencies, speculative abstractions, excessive complexity, and disproportionate file growth.
---

# Maintainable code

Apply this workflow throughout the task. Prefer repository rules and configured tools over this skill's defaults.

Read a reference only when its condition applies:

- [references/architecture.md](references/architecture.md): The change adds or alters a boundary, module, integration, persistence mechanism, or public interface.
- [references/code-design.md](references/code-design.md): The change introduces behavior or reveals unclear ownership or abstractions.
- [references/python.md](references/python.md): Changed Python code needs review.
- [references/java.md](references/java.md): Changed Java code needs review.

## Complete a design checkpoint

Never create a plan if you are given one directly, or have found one via an Agility story.

If you've not been provided a plan, create a short file plan when one condition is true:

- The expected code diff exceeds 300 lines.
- The change adds a domain concept, boundary, integration, or public interface.
- The change affects more than three code files.
- One file is likely to gain more than 100 lines.
- The change adds responsibility to a large or mixed-purpose file.

Classify the affected architecture as established, emerging, or greenfield. State each affected file's responsibility, expected change, and dependency direction. Identify required new files before implementation.

Split code by responsibility and reason to change. Do not split cohesive code to satisfy a line limit.

## Implement one coherent slice

- Do not add another responsibility to a mixed-purpose file.
- Preserve intended dependency direction.
- Do not add speculative abstractions, pass-through layers, or unrelated utility containers.
- Do not hide complexity by moving it into generic helpers.
- Preserve behavior during refactoring.

Stop when one behavior can be tested independently. Then complete a feedback checkpoint.

## Complete a feedback checkpoint

Run this checkpoint after each coherent slice. Also run it when a file gains more than 100 lines, a boundary changes, or the implementation departs from the design.

1. Run focused tests.
2. Run configured quality checks on changed code when practical.
3. Review changed code with the applicable design reference.
4. Review changed files for cohesion, dependency direction, and growth.
5. Refactor each real maintainability problem before the next slice.

Do not postpone an emerging structural problem until final review.

## Select local checks

Use this precedence:

1. Repository-documented quality commands.
2. Repository-configured Ruff for Python.
3. Repository-configured PMD for Java.
4. Another repository-approved analyzer.
5. Manual review when no approved analyzer exists.

Do not install or configure an analyzer without approval.

When automated complexity checks are unavailable, report that limitation and recommend Ruff or PMD.

## Check file growth

For uncommitted work, run:

```bash
python "$HOME/.copilot/skills/maintainable-code/scripts/check_file_growth.py" --base HEAD
```

For a feature branch, replace `HEAD` with the target branch. If `COPILOT_HOME` is set, use that installation path.

Treat a violation as a design-review trigger. Document a cohesive exception instead of making a mechanical split.

## Complete the final checkpoint

1. Run applicable tests, configured quality checks, and the file-growth check.
2. Review the complete code diff for unresolved structural problems.
3. Report commands, unavailable checks, violations, and accepted exceptions.

If a final check finds a problem, return to the implementation loop.

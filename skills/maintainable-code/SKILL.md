---
name: maintainable-code
description: Produce maintainable code with the minimum sufficient change. Use when planning, writing, modifying, refactoring, or reviewing code. Prevent duplicate logic, speculative abstractions, excessive tests, mixed responsibilities, inappropriate dependencies, excessive complexity, and disproportionate file growth. Prefer existing repository patterns and configured quality commands.
---

# Maintainable code

Apply this workflow throughout the task. Prefer repository rules and configured tools over this skill's defaults.

Read a reference only when its condition applies:

- [references/architecture.md](references/architecture.md): The change adds or alters a boundary, module, integration, persistence mechanism, or public interface.
- [references/code-design.md](references/code-design.md): The change introduces behavior, extends an AI-heavy area, or reveals unclear ownership or abstractions.
- [references/python.md](references/python.md): Changed Python code needs complexity review.
- [references/java.md](references/java.md): Changed Java code needs complexity review.

## Find the existing implementation path

Before planning new code:

1. Locate the current entry point for the behavior.
2. Find related logic, models, validation, configuration, and tests.
3. Identify the component that owns the closest responsibility.
4. Search for equivalent behavior, including behavior with different names.

Extend a cohesive existing path when possible. Do not create a parallel implementation of an existing domain decision.

## Define the minimum sufficient change

Use this preference order:

1. Reuse existing behavior without changes.
2. Extend the existing owner.
3. Simplify or consolidate existing code.
4. Add a focused implementation.
5. Add an abstraction for a current boundary or multiple concrete consumers.

Do not design for hypothetical requirements, future variants, possible reuse, or pattern symmetry.

## Complete a design checkpoint

Create a short file plan when one condition is true:

- The expected code diff exceeds 300 lines.
- The change adds a domain concept, boundary, integration, or public interface.
- The change affects more than three code files.
- One file is likely to gain more than 100 lines.
- The change adds responsibility to a large or mixed-purpose file.

Classify the affected architecture as established, emerging, or greenfield. State each affected file's responsibility, expected change, and dependency direction.

Estimate the minimum production files, new files, public symbols, abstractions, and test changes. Treat the estimate as a budget, not a target. If implementation exceeds the budget, identify the requirement that caused the increase.

Justify each proposed new file or abstraction. State why an existing cohesive owner cannot contain the behavior.

Split code by responsibility and reason to change. Do not split cohesive code to satisfy a line limit.

## Implement one coherent slice

- Do not add another responsibility to a mixed-purpose file.
- Preserve intended dependency direction.
- Do not add speculative abstractions, pass-through layers, or unrelated utility containers.
- Do not hide complexity by moving it into generic helpers.
- Preserve behavior during refactoring.

Consolidate duplicate rules, validation decisions, state transitions, queries, and integration behavior. Keep local syntactic duplication when shared code would have different ownership or reasons to change.

Stop when one behavior can be verified independently. Then complete a feedback checkpoint.

## Add only valuable tests

Run existing focused tests after each coherent slice. Add or change tests for:

- new observable behavior;
- a defect with regression risk;
- a changed contract, boundary, or important failure mode;
- non-trivial branches or state transitions;
- behavior that no useful higher-level test covers.

Do not add tests that duplicate coverage without covering additional risk. Do not test private implementation details, trivial delegation, constants, data containers, or framework behavior.

Prefer an existing test at the closest useful boundary. Use the fewest cases that distinguish the required behavior and important failures.

## Complete a feedback checkpoint

Run this checkpoint after each coherent slice. Also run it when a file gains about 100 lines, a boundary changes, or the implementation departs from the design.

1. Run existing focused tests.
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

Do not require local SonarQube. Do not install or configure an analyzer without approval.

When automated complexity checks are unavailable, report that limitation and recommend Ruff or PMD.

## Check file growth

For uncommitted work, run:

```bash
python "$HOME/.copilot/skills/maintainable-code/scripts/check_file_growth.py" --base HEAD
```

For a feature branch, replace `HEAD` with the target branch. If `COPILOT_HOME` is set, use that installation path.

The script measures net growth. It does not penalize a large file that becomes smaller.

Treat a violation as a design-review trigger. Do not split a cohesive file only to satisfy a threshold.

## Complete a subtraction review

Before completion:

1. Replace new code with existing code when possible.
2. Remove duplicate implementations of the same decision.
3. Remove unnecessary helpers, wrappers, models, interfaces, options, and tests.
4. Confirm that each new file, abstraction, and public symbol has a current responsibility.

Prefer a smaller correct diff. Do not retain unnecessary code only because implementation is complete.

## Complete the final checkpoint

1. Run applicable tests, configured quality checks, and the file-growth check.
2. Review the complete code diff for unresolved structural problems and unnecessary additions.
3. Report commands, unavailable checks, violations, and accepted exceptions.

If a final check finds a problem, return to the implementation loop.

---
name: maintainable-code
description: Design, implement, refactor, or review production code while controlling cyclomatic complexity, cognitive complexity, file growth, coupling, cohesion, and architectural boundaries. Use for feature implementation, substantial code changes, refactoring, maintainability reviews, or code that is becoming large, nested, monolithic, duplicated, or difficult to test. Use for Java and Python repositories, including local development where SonarQube is not available.
---

# Maintainable code

Produce cohesive code that fits the repository architecture. Use local checks before completion. Do not require a local SonarQube instance.

## Inspect the repository

1. Read the applicable `AGENTS.md` files.
2. Inspect the package structure and adjacent implementations.
3. Identify the repository test, lint, format, and build commands.
4. Identify the files and responsibilities that the change affects.
5. Read [references/python.md](references/python.md) for Python code.
6. Read [references/java.md](references/java.md) for Java code.

Prefer repository rules and configured tools over this skill's default thresholds.

## Design the change

Prepare a short file-level design before implementation when one condition is true:

- The expected production diff is more than 300 lines.
- The change adds a domain concept, integration, persistence boundary, or public interface.
- The change affects more than three production files.
- An existing file is likely to gain more than 100 lines.
- The change adds a responsibility to an already large class or module.

For each affected file, state its responsibility and expected change. Identify new files before implementation.

Split code by responsibility and change reason. Do not split code only to satisfy a line limit. Keep related behavior together when extraction would increase coupling.

## Implement the change

- Follow existing repository patterns unless a pattern causes the identified problem.
- Keep transport, orchestration, domain logic, persistence, and external integrations separate.
- Keep one conceptual operation in each function or method.
- Use guard clauses when they reduce nesting.
- Prefer clear data structures or polymorphism to long conditional chains when the design supports them.
- Do not create a generic abstraction for one speculative use.
- Do not add unrelated behavior to a utility module, controller, service, or manager class.
- Preserve public behavior during a refactor.
- Add or update tests before a risky extraction.
- Do not suppress a quality finding without an explicit reason.

## Run local checks

Run the repository's normal test and quality commands first.

If the repository has no local complexity command, run:

```bash
python ~/.copilot/skills/maintainable-code/scripts/check_complexity.py src
```

Before completion, check growth relative to the current commit:

```bash
python ~/.copilot/skills/maintainable-code/scripts/check_file_growth.py --base HEAD
```

For a complete feature branch, compare with the target branch:

```bash
python ~/.copilot/skills/maintainable-code/scripts/check_file_growth.py --base origin/main
```

Treat a threshold violation as a design review trigger. Refactor a real maintainability problem. If the code is cohesive, document the exception instead of applying a mechanical split.

## Review the complete diff

Review all changed production files after the checks pass.

Confirm these conditions:

- Each file has a clear responsibility.
- New dependencies follow the intended architecture.
- No central module gained unrelated behavior.
- No extraction created unnecessary forwarding layers.
- Names describe domain behavior.
- Tests cover changed behavior and important branches.
- Local tests and quality checks pass.

Report the commands that ran. Report unresolved violations and approved exceptions.

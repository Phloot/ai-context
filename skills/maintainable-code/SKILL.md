---
name: maintainable-code
description: Apply maintainability controls throughout tasks that plan, write, modify, refactor, or review production code. Use before implementation to review architecture, after each coherent implementation slice to provide feedback, and before completion to validate the complete change. Prefer repository-configured Ruff, PMD, build, test, and lint commands. Detect monolithic files, excessive complexity, mixed responsibilities, inappropriate coupling, and disproportionate file growth. Use for Java and Python repositories, including local development where SonarQube is unavailable.
---

# Maintainable code

Produce cohesive code that fits the repository architecture. Apply this workflow throughout the task. Do not require a local SonarQube instance.

## Start the maintainability workflow

1. Read the applicable `AGENTS.md` files.
2. Inspect the package structure and adjacent implementations.
3. Identify the repository test, lint, format, and build commands.
4. Identify the approved local analyzers that the repository configures.
5. Identify the files and responsibilities that the change affects.
6. Read [references/python.md](references/python.md) for Python code.
7. Read [references/java.md](references/java.md) for Java code.

Prefer repository rules and configured tools over this skill's default thresholds.

## Complete the design checkpoint

Prepare a short file-level design before implementation when one condition is true:

- The expected production diff is more than 300 lines.
- The change adds a domain concept, integration, persistence boundary, or public interface.
- The change affects more than three production files.
- An existing file is likely to gain more than 100 lines.
- The change adds a responsibility to an already large class or module.

For each affected file, state its responsibility and expected change. Identify new files before implementation.

Split code by responsibility and change reason. Do not split code only to satisfy a line limit. Keep related behavior together when extraction would increase coupling.

## Implement one coherent slice

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

Stop after one coherent behavior can be tested independently. Then complete the feedback checkpoint.

## Complete the feedback checkpoint

Complete this checkpoint after each coherent implementation slice. Also complete it when one condition is true:

- A production file gains approximately 100 lines.
- The change adds a class, module, domain concept, or external boundary.
- A method or function gains significant branching or nesting.
- The implementation differs materially from the file-level design.
- The next slice will add another responsibility to an existing file.

At each feedback checkpoint:

1. Run focused tests for the completed behavior.
2. Run configured local quality checks on the changed code when practical.
3. Review changed functions and methods for branching, nesting, length, and parameters.
4. Review changed files for cohesion, coupling, and disproportionate growth.
5. Refactor a real maintainability problem before the next slice.
6. Update the file-level design when responsibilities or boundaries change.

Do not run an expensive full build after every small edit. Do not wait until final review to address an emerging monolithic file.

## Select local quality checks

Use this precedence:

1. Run the repository's documented quality commands.
2. Run repository-configured Ruff checks for Python.
3. Run repository-configured PMD checks for Java.
4. Run another repository-approved analyzer when documented.
5. If no approved analyzer exists, complete the manual maintainability review.

Do not install an analyzer or change repository configuration unless the task includes that work or the user approves it.

If no approved analyzer exists:

- Report that local complexity enforcement is unavailable.
- Recommend that the repository configure Ruff or PMD.
- Continue with the manual review and file-growth check.
- Do not claim that the code passed an automated complexity check.

## Check file growth

Run the bundled file-growth script from the personal skill installation.

For uncommitted work, run:

```bash
python "$HOME/.copilot/skills/maintainable-code/scripts/check_file_growth.py" --base HEAD
```

For a complete feature branch, run:

```bash
python "$HOME/.copilot/skills/maintainable-code/scripts/check_file_growth.py" --base origin/main
```

If `COPILOT_HOME` replaces `$HOME/.copilot`, use the corresponding skill path.

Treat a threshold violation as a design review trigger. Refactor a real maintainability problem. If the code is cohesive, document the exception instead of applying a mechanical split.

## Complete the final checkpoint

Before completion:

1. Run the repository's applicable test suite.
2. Run all configured local quality checks.
3. Run the file-growth check against `HEAD` or the target branch.
4. Review the complete production diff.
5. Confirm that new dependencies follow the intended architecture.
6. Confirm that each changed file has one cohesive responsibility.
7. Confirm that tests cover changed behavior and important branches.
8. Report each command that ran.
9. Report unavailable checks, unresolved violations, and approved exceptions.

If a final check finds a problem, return to the implementation loop. Do not report completion until the problem is fixed or documented.

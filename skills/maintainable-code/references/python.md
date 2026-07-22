# Python maintainability reference

Use this reference for Python production code.

## Preserve package boundaries

- Keep HTTP or command-line parsing outside domain functions.
- Keep use-case orchestration outside persistence adapters.
- Pass dependencies explicitly when practical.
- Avoid imports from a higher architectural layer.
- Avoid a shared `utils.py` file for unrelated behavior.
- Prefer a focused module name that describes one capability.

Create a class when behavior and state form one durable concept. Do not replace a group of independent functions with a class only to reduce file size.

## Control function complexity

Use these default review thresholds when the repository has no stricter policy:

| Measure | Review threshold |
| --- | ---: |
| Cyclomatic complexity | 10 |
| Function length | 75 lines |
| Parameters | 7 |
| File length | 600 physical lines |
| Added lines in one file | 200 |

Use a threshold as a review trigger. Do not perform a mechanical extraction that makes the code harder to follow.

Reduce complexity with these techniques:

- Use guard clauses to reduce nesting.
- Extract a named domain operation.
- Replace repeated condition mappings with a dictionary or data object.
- Separate parsing, validation, decisions, and side effects.
- Replace related primitive values with a typed object when the object represents a domain concept.

Do not hide control flow in decorators, callbacks, metaprogramming, or overly generic helpers.

## Use repository-native checks

Look for Ruff configuration in `pyproject.toml`, `ruff.toml`, or `.ruff.toml`. Look for Ruff in the repository dependency files and documented development commands.

If Ruff is configured, run the repository command. Use a focused command during an implementation checkpoint when practical:

```bash
ruff check --select C901,PLR0911,PLR0912,PLR0913,PLR0915 path/to/changed/code
```

Run the repository's complete Ruff command during the final checkpoint.

If Ruff is not configured, recommend this example as a possible baseline. Do not apply it unless the task includes analyzer configuration or the user approves it.

```toml
[tool.ruff.lint]
select = ["C901", "PLR0911", "PLR0912", "PLR0913", "PLR0915"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 7
max-branches = 10
max-returns = 6
max-statements = 50
```

If no approved analyzer exists, review each changed function manually. Report that automated local complexity enforcement was unavailable.

Tool references:

- [Ruff complex-structure rule](https://docs.astral.sh/ruff/rules/complex-structure/)

## Verify the change

Run focused tests during implementation. Run the repository test suite before completion when its runtime is reasonable.

Typical commands include:

```bash
pytest
python -m unittest
```

Do not select a test command only because it appears in this reference. Use the framework that the repository configures.

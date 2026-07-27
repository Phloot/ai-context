# Python review

Use repository-configured commands and thresholds first.

## Default review thresholds

| Measure | Threshold |
| --- | ---: |
| Cyclomatic complexity | 10 |
| Function length | 75 lines |
| Parameters | 7 |
| File length | 600 lines |
| Added lines in one file | 200 |

Thresholds trigger review. They do not require mechanical extraction.

## Run local checks

When Ruff is configured, use the repository command. Do not override its configured rule selection:

```bash
ruff check path/to/changed/code
```

If Ruff is not configured, recommend `C901`, `PLR0911`, `PLR0912`, `PLR0913`, `PLR0914`, `PLR0915`, and `PLR1702` as a possible baseline. Do not modify configuration without approval.

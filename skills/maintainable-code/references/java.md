# Java review

Use repository-configured commands and thresholds first.

## Default review thresholds

| Measure | Threshold |
| --- | ---: |
| Cyclomatic complexity | 10 |
| Cognitive complexity | 15 |
| Method length | 75 lines |
| Parameters | 7 |
| File length | 600 lines |
| Added lines in one file | 200 |

Thresholds trigger review. They do not require mechanical extraction.

## Run local checks

Use the Gradle or Maven wrapper when present.

Run only configured tasks or goals:

```bash
./gradlew test check
./mvnw test verify
```

Before running PMD-specific commands, confirm that the build configures PMD. If PMD is absent, recommend Cyclomatic Complexity and Cognitive Complexity rules as a possible baseline. Do not modify the build without approval.

# Java maintainability reference

Use this reference for Java production code.

## Preserve package boundaries

- Keep controllers responsible for transport concerns.
- Keep application services responsible for use-case orchestration.
- Keep domain behavior independent from web and persistence frameworks when practical.
- Keep repositories and external clients behind focused interfaces.
- Do not place domain decisions in controllers, mappers, or configuration classes.
- Do not add unrelated methods to a general `Service`, `Manager`, or `Util` class.

Create a class for one cohesive responsibility. Do not create an interface for one implementation unless a boundary, test seam, or likely alternative requires it.

## Control method complexity

Use these default review thresholds when the repository has no stricter policy:

| Measure | Review threshold |
| --- | ---: |
| Cyclomatic complexity | 10 |
| Cognitive complexity | 15 |
| Method length | 75 lines |
| Parameters | 7 |
| File length | 600 physical lines |
| Added lines in one file | 200 |

Reduce complexity with these techniques:

- Use guard clauses to reduce nesting.
- Extract a named domain operation.
- Separate validation, decisions, mapping, and side effects.
- Use a strategy or polymorphic type when behavior varies by a stable type.
- Use a value object when related values have shared rules.

Do not introduce a pattern only to remove an `if` statement. Do not split one method into many forwarding methods with no domain meaning.

## Use repository-native checks

Use the Gradle wrapper or Maven wrapper when the repository provides one.

Before you run PMD, confirm that the build configures the PMD plugin and its rules. Do not assume that a task or goal exists.

Common Gradle commands include:

```bash
./gradlew test check
./gradlew pmdMain pmdTest
```

Common Maven commands include:

```bash
./mvnw test verify
./mvnw pmd:check
```

Run only configured tasks and goals. Do not add PMD only to complete an unrelated feature.

If PMD is not configured, recommend these Java design rules as a possible baseline. Do not apply them unless the task includes analyzer configuration or the user approves it.

```xml
<?xml version="1.0"?>
<ruleset name="Maintainability"
         xmlns="http://pmd.sourceforge.net/ruleset/2.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://pmd.sourceforge.net/ruleset/2.0.0 https://pmd.sourceforge.io/ruleset_2_0_0.xsd">
    <description>Local maintainability rules.</description>

    <rule ref="category/java/design.xml/CyclomaticComplexity">
        <properties>
            <property name="classReportLevel" value="80"/>
            <property name="methodReportLevel" value="10"/>
        </properties>
    </rule>

    <rule ref="category/java/design.xml/CognitiveComplexity">
        <properties>
            <property name="reportLevel" value="15"/>
        </properties>
    </rule>
</ruleset>
```

If no approved analyzer exists, review each changed method manually. Report that automated local complexity enforcement was unavailable.

## Verify the change

Run focused tests during implementation. Run the repository test suite before completion when its runtime is reasonable.

Confirm that extracted components preserve transaction boundaries, dependency injection behavior, serialization, and framework annotations.

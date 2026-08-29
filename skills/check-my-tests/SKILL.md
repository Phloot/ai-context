---
name: check-my-tests
description: Audit an existing test suite for useful behavioral coverage, weak or redundant tests, brittle implementation coupling, test-design problems, and important missing scenarios. Use when a user asks to review, assess, improve, simplify, or find gaps in repository tests. Do not use for a request to write one already-specified test unless the user also requests a broader review.
---

# Check My Tests

Audit tests against the behavior and risks of the production code. Optimize for confidence relative to execution and maintenance cost.

## Preserve the task boundary

- Treat the audit as read-only unless the user asks for changes.
- Do not delete or rewrite a test without explicit authorization.
- Use repository instructions and configured commands.
- Do not install tools or change test configuration during an audit.
- State when unavailable runtime evidence limits a conclusion.

## Select the review scope

Determine whether the user wants a focused review or a repository-wide audit. Infer a focused scope from named files, a diff, or a feature.

For a large repository, review representative areas first. Expand the scope only when the evidence requires it.

## Audit the suite

1. Read repository instructions and test configuration.
2. Identify the production behavior in scope.
3. Identify public APIs, entry points, domain rules, and integration boundaries.
4. Inventory the related tests, fixtures, factories, fakes, and test helpers.
5. Run focused configured tests when practical.
6. Use existing coverage or mutation reports when available.
7. Evaluate each finding with the criteria in [review-criteria.md](references/review-criteria.md).
8. Find missing scenarios with [gap-analysis.md](references/gap-analysis.md).
9. Verify each removal or gap claim against nearby tests and higher-level suites.
10. Report the highest-value findings first.

For Python or Java repositories, run the bundled inventory script when a fast inventory will help. Treat its output as leads, not conclusions.

```bash
python3 <skill-root>/scripts/inventory_tests.py <repository-root>
```

Use `--format json` when structured output will help later analysis. Python results use syntax analysis. Java results use approximate text matching.

## Apply the test philosophy

- Test observable behavior through the narrowest stable boundary that gives useful confidence.
- Prefer a test that survives a behavior-preserving refactor.
- Give each test one coherent behavior and one understandable reason to fail.
- Permit multiple assertions when they describe the same behavior.
- Prefer real collaborators when they are fast, local, and deterministic.
- Use the smallest suitable test double when a real collaborator is unsuitable.
- Keep scenario-defining data visible. Extract noisy mechanics instead.
- Test important failures, boundaries, and state transitions.
- Use higher-level tests for wiring and integration risks that unit tests cannot detect.
- Add the fewest cases that distinguish the required behavior and risk.

Read [test-doubles.md](references/test-doubles.md) when mocks, stubs, spies, or fakes affect a finding.

Read [foundations.md](references/foundations.md) when the user requests the rationale or a review decision needs a testing principle.

Read the applicable language guide:

- [python.md](references/python.md) for `pytest`, `unittest`, and Python test patterns.
- [java.md](references/java.md) for JUnit, Mockito, and common Java integration tests.

## Classify findings

Use these actions:

| Action | Meaning |
| --- | --- |
| Remove or merge | The test provides no distinct, verified confidence. |
| Rewrite | The scenario matters, but the test uses an unstable boundary. |
| Strengthen | The scenario matters, but the assertion cannot detect a plausible defect. |
| Add | Important behavior or risk has no effective test. |
| Investigate | The available evidence cannot support a stronger conclusion. |
| Keep | The test is a useful example that needs no change. |

Use these confidence levels:

| Confidence | Requirement |
| --- | --- |
| Confirmed | Direct evidence proves the finding. |
| Strong | Multiple repository facts support the finding. |
| Likely | The evidence indicates a problem but has a plausible exception. |
| Needs context | Product or runtime information is missing. |

Do not call a test useless without direct evidence. Prefer `low-value`, `redundant`, or `unable to detect the intended defect`.

Before a removal recommendation, confirm all applicable facts:

- The test protects no distinct behavior.
- Another effective test covers the behavior, or the behavior has no value.
- The test is not a focused regression for a prior defect.
- Removing the test will not remove the only check of an important boundary.

## Report the result

Lead with the overall assessment and the most important risk. Then provide:

1. Prioritized findings with file and test identifiers.
2. Evidence and the protected or missing behavior.
3. The recommended action and expected benefit.
4. Confidence and any evidence limitation.
5. A short list of strong tests worth keeping, when useful.
6. Commands that ran and their results.

Separate confirmed gaps from inferred gaps. Do not use an overall numeric score unless the user requests one.

For each material finding, use this form:

```markdown
### [Action] Short finding title

- Location: `path/to/test_file.py::test_name`
- Confidence: Strong
- Evidence: The test stubs the result and asserts the same configured result.
- Impact: The test passes when the production mapping code is removed.
- Recommendation: Exercise the public operation with a small fake repository.
```

If the user asks for implementation, make the smallest coherent changes. Run the focused tests after each change.

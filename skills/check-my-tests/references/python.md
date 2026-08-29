# Python test review

Use repository conventions before these defaults. Inspect `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg`, and CI configuration when present.

## Review pytest and unittest tests

Check for:

- `pytest` fixtures with unrelated setup or broad scope.
- `autouse` fixtures that hide important preconditions.
- `unittest.mock.patch` targets that patch the definition instead of the lookup location.
- Mocks without `spec`, `spec_set`, or autospec when interface drift is a risk.
- Parameterized cases that repeat one behavioral partition.
- Large parameter tables with weak diagnostics.
- Exception tests that do not check the relevant message or state.
- Tests that depend on collection order without an ordering contract.
- Shared mutable fixtures or module state.
- Time, randomness, environment, locale, and filesystem state without control.
- `sleep` calls used for synchronization.

Do not require autospec for a small local stub or fake. Select the least complex substitute that detects relevant interface changes.

## Review fixtures

Keep scenario-defining values visible in the test. Use fixtures for stable mechanics and shared resources.

Investigate a fixture when:

- Its name does not explain the supplied state.
- It creates more state than most tests use.
- It depends on several other fixtures.
- It changes global state without reliable restoration.
- A reader must open many fixtures to understand one scenario.

Prefer small factories when tests need controlled variations. Do not replace clear inline construction with a generic builder.

## Review parameterization

Each row should represent a distinct partition, boundary, or failure. Give complex rows identifiers that explain their purpose.

Split a parameterized test when rows require different actions or assertions. Keep one parameterized test when the behavior and diagnostic meaning stay the same.

## Consider property-based tests

Property-based testing can help with parsers, serializers, transformations, and algorithms. Recommend it only when a stable invariant exists.

Examples include round trips, idempotency, ordering, conservation, and equivalence with a trusted implementation.

Keep focused examples for important named regressions and business scenarios.

## Review async tests

Use deterministic synchronization primitives. Do not use timing delays as proof of completion.

Check cancellation, timeout, and cleanup behavior when those risks matter. Confirm that tests close tasks, clients, files, and event-loop resources.

## Select commands

Use configured repository commands first. Common focused forms include:

```bash
pytest path/to/test_file.py -q
pytest path/to/test_file.py::test_name -q
python -m unittest package.tests.test_module
```

Do not add coverage, mutation, or property-testing dependencies during an audit.

# Test gap analysis

Find missing tests from behavior and risk. Do not create a test for each uncovered line or production method.

## Build a behavior map

Identify the applicable surfaces:

- Public functions, classes, commands, routes, and user operations.
- Domain rules and state transitions.
- Validation and authorization decisions.
- Persistence, network, filesystem, queue, and process boundaries.
- Serialization and compatibility contracts.
- Startup, dependency injection, and configuration wiring.
- Recovery, retry, timeout, and partial-failure behavior.

Map each existing test to one or more surfaces. Record the level at which the test protects the behavior.

## Prioritize missing scenarios

Use this order unless repository risks require another order:

1. Data loss, security, authorization, and irreversible operations.
2. Public behavior with no effective test.
3. Error paths and partial failures.
4. State transitions and idempotency.
5. Boundary values and malformed input.
6. Integration wiring that mocks cannot verify.
7. Complex transformations and branching.
8. Previously fixed defects.

Do not recommend tests for impossible internal inputs when a stable boundary excludes those inputs.

## Select representative cases

Partition inputs by behavior. Select the fewest values that distinguish the partitions.

For a range from 1 through 100, consider:

- `0` for below the range.
- `1` for the lower boundary.
- One representative valid value.
- `100` for the upper boundary.
- `101` for above the range.
- An absent value when absence can reach the public API.

For stateful behavior, test allowed transitions, rejected transitions, and repeated operations.

## Check test levels

Use focused tests for domain rules and transformations. Use integration tests for adapters, schemas, configuration, and real boundary behavior.

Use a small number of end-to-end tests for critical journeys. Do not duplicate every lower-level scenario through the user interface.

Identify these false-confidence patterns:

- Unit tests mock the database mapping and no test checks the real schema.
- Service tests mock serialization and no test checks the wire format.
- Controller tests call methods directly and no test checks routing or middleware.
- Tests replace dependency injection and no test starts the application graph.
- Adapter tests mock a third-party client type and no contract test checks the wrapper.

## Use history when available

Inspect nearby regression names, issue references, blame, or focused history when a removal finding is uncertain. Do not perform broad history research without a reason.

Treat a prior defect as evidence of risk. Preserve a focused regression test unless another test detects the same defect more clearly.

## State uncertainty

Classify a gap as confirmed only when the reviewed scope supports that conclusion. Use `likely` when another suite or external system can provide coverage.

State the missing evidence. Examples include unavailable integration tests, disabled coverage collection, or unclear product requirements.

# Test review criteria

Use these criteria to determine test value. Do not apply one criterion in isolation.

## Evaluate the protected behavior

A useful test protects behavior that matters to a caller, user, operator, or system boundary. The test must detect a plausible defect.

Prefer tests that answer these questions clearly:

- What condition does the scenario establish?
- What operation occurs?
- What observable result must follow?
- What defect will cause the test to fail?

## Evaluate sensitivity

A strong test has two forms of sensitivity:

- Behavior sensitivity: The test fails when required behavior changes.
- Structure insensitivity: The test stays valid after a behavior-preserving refactor.

Excessive structure sensitivity appears as private-method calls, exact internal call order, or mocks for every collaborator.

Some interactions are behavior. Verify an interaction when the interaction is the externally meaningful effect. Examples include sending a command or recording an audit event.

## Evaluate diagnostic value

A failure should identify one coherent scenario. Do not require one assertion when several assertions describe the same result.

Prefer Arrange, Act, Assert or Given, When, Then. Keep one clear action in most tests.

Keep relevant values in the test. Move unrelated setup mechanics into a helper or fixture.

## Evaluate reliability

Check that tests are:

- Deterministic across repeated runs.
- Independent of execution order.
- Independent of local time, locale, and machine state unless controlled.
- Explicit about random seeds when randomness is part of the test.
- Free of unbounded waits and timing assumptions.
- Responsible for cleaning persistent state that they create.

Treat a flaky test as a defect. Do not normalize reruns as the primary correction.

## Evaluate cost

Consider execution time, setup complexity, data maintenance, and refactor cost. A slow test can be valuable when it protects a real integration risk.

Prefer the lowest test level that can detect the defect. Keep enough higher-level tests to verify wiring and system boundaries.

## Identify low-value patterns

Flag these patterns only after repository review:

| Pattern | Evidence of low value | Important exception |
| --- | --- | --- |
| No meaningful assertion | The test only checks that code does not raise unexpectedly. | Successful completion is the documented behavior. |
| Stub echo | The test asserts the exact value configured on a stub. | Production transformation or routing also affects the result. |
| Production logic copy | Expected values use the same algorithm as production. | The test uses an independent reference implementation. |
| Framework test | The test proves library or language behavior only. | Project configuration changes that behavior. |
| Private implementation test | A stable public API reaches the same paths. | The component has complex behavior that is impractical to reach publicly. |
| Interaction overspecification | The test verifies irrelevant calls, counts, or order. | The interaction protocol is part of the contract. |
| Duplicate scenario | Another test detects the same defects with equal or better diagnostics. | The test protects a separate boundary or prior regression. |
| Broad snapshot | Reviewers cannot identify the meaningful contract. | The complete representation is the maintained contract. |
| Excessive mock graph | Most behavior comes from configured doubles. | The unit is an orchestration policy whose outputs are interactions. |
| Coverage-only test | The test executes code but cannot detect wrong behavior. | Execution itself checks a required safety property. |

## Strengthen weak assertions

Prefer assertions about returned values, durable state, emitted domain events, or meaningful external commands.

Avoid assertions that only confirm:

- An object is not null when its content matters.
- A collection is non-empty when exact membership matters.
- No exception occurred when an outcome is available.
- A mock returned its configured value.
- A snapshot changed without review of the contract.

For negative behavior, confirm both the rejection and the absence of an unwanted side effect.

## Use coverage correctly

Coverage locates code that did not execute. Coverage does not prove assertion quality or scenario value.

Use branch coverage to find candidate gaps in conditional code. Review each candidate against reachable behavior and risk.

Use mutation results when available. A surviving mutation is evidence that the current suite cannot detect that production change.

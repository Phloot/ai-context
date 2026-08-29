# Test doubles

Select a test double by purpose. Do not use `mock` as the design name for every substitute.

| Double | Purpose |
| --- | --- |
| Dummy | Satisfy an argument that the scenario does not use. |
| Stub | Supply controlled indirect input. |
| Spy | Record calls for later inspection. |
| Mock | Verify an expected interaction protocol. |
| Fake | Provide a lightweight working implementation. |

One library object can perform several roles. Classify the role by how the test uses the object.

## Prefer real collaborators when practical

Use the real collaborator when it is fast, deterministic, local, and easy to control. Unnecessary substitution can hide integration defects.

Use a fake when several tests need realistic stateful behavior. Verify that important fake behavior matches the real contract.

Use a stub when the test needs one controlled response or failure. Keep its configuration local to the scenario.

Use a spy or mock when the outgoing interaction is the observable effect. Verify only contract-relevant details.

## Avoid fragile interaction checks

Do not verify a getter call, internal query, logging call, or incidental call order unless the call is part of the contract.

This test is usually fragile:

```python
repository.find.assert_called_once_with(42)
cache.get.assert_called_once_with(42)
mapper.convert.assert_called_once()
```

Prefer an outcome check when the internal sequence can change:

```python
result = service.get_user(42)

assert result == UserView(id=42, name="Alice")
```

## Do not mock third-party types directly

Place a small owned interface around an external library when substitution is necessary. Stub or fake the owned interface in most tests.

Give the adapter focused tests against the real library behavior when practical. This approach limits assumptions about the third-party API.

## Detect mock-driven false confidence

Investigate when:

- The test configures the answer and then asserts the same answer.
- The test has more mock setup than production execution.
- Every internal collaborator is replaced.
- Refactoring call order breaks many tests without changing behavior.
- Mocks reproduce the implementation instead of describing a contract.
- No test checks the real boundary represented by the doubles.

Do not reject orchestration tests only because they verify interactions. For command dispatch, notification, and audit behavior, an interaction can be the correct outcome.

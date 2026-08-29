# Java test review

Use repository conventions before these defaults. Inspect Maven or Gradle configuration and CI test tasks when present.

## Review JUnit tests

Check for:

- Tests that call private methods through reflection.
- Broad `@BeforeEach` setup that hides scenario data.
- Shared mutable state or order-dependent tests.
- `@Disabled` tests without a current reason.
- Exception tests that check only the exception type when details matter.
- Repeated tests that do not control their source of nondeterminism.
- Parameterized cases that do not represent distinct behavior.
- Assertions with weak diagnostics for complex values.
- Tests that depend on collection order without an ordering contract.
- Thread sleeps used for synchronization.

Use AssertJ, Hamcrest, or JUnit assertions according to repository conventions. Do not introduce a new assertion library only for style.

## Review Mockito use

Investigate:

- `verifyNoMoreInteractions` applied as a universal rule.
- Exact call counts for interactions that are not contractual.
- Deep stubs and long chains of configured returns.
- Partial mocks or spies that expose unclear production design.
- Argument captors used when an observable result is available.
- Lenient stubbing that hides irrelevant setup.
- Mocks of data objects or simple value types.
- Direct mocks of third-party library types.

Use strict stubbing when the repository already supports it and the strictness improves diagnostics. Do not add strictness that encodes incidental calls.

## Review Spring tests

Select the smallest context that verifies the risk. A plain unit test is suitable for isolated domain logic.

Use slice tests for web, persistence, or serialization configuration. Use full-context tests for important application wiring and critical journeys.

Investigate tests that use Spring context startup but replace all meaningful beans. The test can pay integration cost without checking integration behavior.

Do not replace every integration test with a unit test. Database mappings, transactions, validation configuration, routing, and dependency injection need boundary evidence.

## Review integration infrastructure

Use repository-provided containers, embedded services, or test fixtures. Confirm that substitutes match production behavior that matters to the scenario.

An in-memory database is not always equivalent to the production database. Check SQL dialects, constraints, transactions, and migrations when those risks matter.

## Select commands

Use configured repository commands first. Common focused forms include:

```bash
./gradlew test --tests 'com.example.UserServiceTest'
./gradlew test --tests 'com.example.UserServiceTest.rejectsFutureBirthDate'
./mvnw -Dtest=UserServiceTest test
```

Do not add coverage, mutation, or test-container dependencies during an audit.

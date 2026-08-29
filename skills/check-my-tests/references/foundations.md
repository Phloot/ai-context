# Testing foundations

Use these principles to explain review decisions. Apply each principle with repository context.

## Prefer public behavior

Google's *Prefer Testing Public APIs Over Implementation-Detail Classes* treats many internal classes like private methods. Test them through a stable public API when that API can exercise their behavior.

Direct tests remain useful for complex internal components or behavior that is impractical to reach through the public API.

Related principle: A behavior-preserving refactor should not usually require substantive test changes.

## Structure tests clearly

Arrange, Act, Assert separates setup, execution, and verification. Given, When, Then expresses the same structure in behavioral language.

Keep one coherent action in most tests. Multiple assertions are appropriate when they describe one behavior.

## Balance desirable properties

The FIRST mnemonic recommends tests that are fast, independent, repeatable, self-validating, and timely.

Kent Beck's Test Desiderata adds properties such as behavioral, structure-insensitive, readable, specific, predictive, and confidence-inspiring.

Treat these properties as tradeoffs. A slower integration test can provide confidence that a fast unit test cannot provide.

## Keep tests descriptive

Production code often benefits from removing duplication. Tests sometimes benefit from local repetition that keeps a scenario understandable.

Use the DAMP principle: Descriptive And Meaningful Phrases. Extract repeated mechanics, but keep behavior-defining data visible.

## Select the correct test double

Gerard Meszaros defined dummy, stub, spy, mock, and fake as distinct test-double roles. Select a role from the test's need.

Freeman and Pryce advise against direct mocks of types that the project does not own. Use an owned adapter when substitution is necessary.

## Balance test levels

The test pyramid recommends many focused tests, fewer integration tests, and a small number of broad end-to-end tests.

Use the pyramid as an economic model, not a required ratio. Select the level that can detect the relevant defect.

## Test input spaces

Boundary-value analysis and equivalence partitioning select representative inputs by distinct behavior. They avoid many arbitrary examples of the same path.

Property-based testing checks stable invariants across generated inputs. It is useful for parsers, serializers, transformations, and algorithms.

## Measure test effectiveness carefully

Coverage shows which code executed. It does not show whether assertions can detect incorrect behavior.

Mutation testing changes production code and runs the suite. A surviving mutation can expose an ineffective or missing test.

## Use regression tests

For a defect correction, first reproduce the defect with a failing test. Then correct the production behavior and confirm that the test passes.

Keep the test at the smallest stable boundary that still detects the defect.

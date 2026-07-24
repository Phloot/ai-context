# Flightplan Context Marketplace User Interface Plan

## 1. Purpose

Coordinate implementation of the Context Marketplace user interface in
Flightplan.

The UI lets developers browse the catalog, understand component state, perform
safe marketplace actions, and recover from conflicts and failures. It consumes
the stable API produced by the complete backend sequence.

This plan defines shared UI invariants and execution order. The four
implementation specifications contain detailed behavior and tests.

## 2. Prerequisites

Complete and verify all backend specifications before UI implementation:

1. `02a-flightplan-marketplace-foundation-spec.md`
2. `02b-flightplan-marketplace-projection-spec.md`
3. `02c-flightplan-marketplace-lifecycle-spec.md`
4. `02d-flightplan-marketplace-api-spec.md`

Do not design frontend behavior around an unstable or assumed API.

## 3. Implementation sequence

Implement and review these specifications in order:

1. `03a-flightplan-marketplace-browser-spec.md`
2. `03b-flightplan-marketplace-actions-spec.md`
3. `03c-flightplan-marketplace-resilience-spec.md`
4. `03d-flightplan-marketplace-ui-quality-spec.md`

Do not start a later specification until the preceding completion gate and
focused tests pass.

### 3.1 Browser output

03a establishes:

- Marketplace navigation and page structure.
- Component list, search, and filters.
- Component details.
- Server-authoritative read-only state.

### 3.2 Actions output

03b establishes:

- Enable, disable, and update interactions.
- Synchronization.
- Profile preview and application.
- Activity presentation.

### 3.3 Resilience output

03c establishes:

- Conflict presentation.
- Catalog-failure recovery.
- Initial migration state.
- Known and unknown errors.
- Loading and empty states.

### 3.4 Quality output

03d establishes:

- Responsive desktop behavior.
- Accessibility.
- Final regression testing.
- Overall UI acceptance.

## 4. Shared invariants

Every UI slice must preserve these rules:

- Inspect and follow Flightplan's existing frontend framework, routing, styles,
  data layer, components, accessibility level, and test conventions.
- Do not introduce a new frontend framework.
- Keep server state authoritative.
- Do not duplicate dependency, compatibility, projection, or conflict rules.
- Use one component presentation model for every component type.
- Do not hard-code behavior for a named component.
- Update mutation state only after backend confirmation.
- Keep unrelated parts of the page usable during a scoped mutation.
- Use stable backend error codes for known failures.
- Keep detailed diagnostics in existing Flightplan logs.
- Never display payload contents, secrets, stack traces, or unrestricted local
  paths.
- Preserve keyboard navigation and visible focus.
- Do not overwrite unrelated working-tree changes.

## 5. Required end state

After all four specifications:

- Developers can browse, search, filter, and inspect every component type.
- Developers can safely enable, disable, and update components.
- Dependency and external-dependency effects are visible before confirmation.
- Developers can synchronize the catalog and apply profiles.
- Developers can view activity.
- Conflicts, migration, failures, loading, and empty states are understandable.
- The marketplace works at Flightplan's supported desktop widths.
- The page is keyboard accessible and announces important state changes.
- Focused and complete frontend tests pass.
- Existing Flightplan frontend tests pass.

## 6. Agent handoff protocol

For each implementation specification:

1. Provide this plan, specs 00 and 01, the completed backend API contract, and
   only the current detailed UI slice.
2. Require inspection of existing Flightplan frontend conventions.
3. Require focused tests for the current slice.
4. Review the completion gate before starting the next slice.
5. Use a fresh task or context for the next specification.

Each agent must report:

- Views and components changed.
- API operations connected.
- Accessibility behavior completed.
- Tests run.
- Remaining limitations or deferred work.

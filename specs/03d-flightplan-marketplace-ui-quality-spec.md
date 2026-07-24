# Flightplan Marketplace UI: Quality and Acceptance

## Purpose

Complete responsive behavior, accessibility, focused quality tests, and final
end-to-end acceptance for the marketplace UI.

## Prerequisites

- Complete 03a, 03b, and 03c.
- Read `03-flightplan-marketplace-ui-spec.md` for shared UI invariants.
- Run the complete backend and frontend applications together for final
  acceptance.

## 17. Responsive behavior

Support Flightplan's current desktop target.

At narrower widths:

- Stack the component detail below or above the list.
- Keep search and filters usable.
- Keep action controls visible.
- Avoid horizontal page scrolling.

Do not require a separate mobile application layout.

## 18. Accessibility

Meet the accessibility level that Flightplan currently requires.

At minimum:

- Use semantic headings.
- Use native buttons and form controls.
- Associate labels with inputs.
- Support keyboard navigation.
- Keep focus visible.
- Announce mutation results.
- Announce errors.
- Do not use color as the only status indicator.
- Provide accessible names for toggle controls.

Use `aria-checked` only for controls with switch semantics.

Use disabled state only when the action cannot run.

## 22. Tests

Use the existing Flightplan frontend test tools.

Test:

- Keyboard interaction.
- Accessible labels.
- Focus movement and restoration.
- Status announcements.
- Narrow desktop layouts.
- Absence of horizontal page scrolling.

Run the complete focused suites from 03a, 03b, and 03c as the final regression
suite.

Mock the backend at the network boundary or existing data-service boundary.

Do not duplicate backend filesystem tests in frontend tests.

## 23. Acceptance criteria

The user interface is complete when:

- Developers can view every catalog component type.
- Developers can search components.
- Developers can filter by component type.
- Developers can inspect component details.
- Developers can enable a component.
- Developers can see automatic dependency changes.
- Developers can disable a component safely.
- Developers can see blocked dependency removal.
- Developers can update a component.
- Developers can synchronize the catalog.
- Developers can apply a profile.
- Developers can view activity.
- Developers can understand conflicts.
- Mutation state changes occur only after backend confirmation.
- The page handles loading, empty, and error states.
- The page is keyboard accessible.
- Frontend tests pass.
- Existing Flightplan frontend tests pass.

## 24. Agent execution instructions

Inspect the existing Flightplan user interface before implementation.

Use the supplied graphical mockup as a design reference.

Follow existing Flightplan components and styles.

Do not introduce component-specific marketplace behavior.

Do not duplicate backend rules.

Do not add a new frontend framework.

Run focused tests after each implementation slice.

Run the complete frontend test suite before completion.

Report:

- Views added.
- Components added.
- API operations connected.
- Accessibility behavior.
- Tests run.
- Remaining limitations.

## Completion gate

This slice and the UI sequence are complete only when every acceptance
criterion above is satisfied, the focused suites from 03a through 03d pass, and
the existing Flightplan frontend suite remains green.

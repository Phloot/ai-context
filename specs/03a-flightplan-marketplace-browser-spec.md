# Flightplan Marketplace UI: Browser and Read-only State

## Purpose

Build the marketplace route, navigation, component browsing, search, filters,
details, and authoritative read-only state integration.

## Prerequisites

- Complete the full backend sequence 02a through 02d.
- Read `03-flightplan-marketplace-ui-spec.md` for shared UI invariants.
- Inspect Flightplan's frontend framework, router, component library, data
  layer, and test conventions.

Do not implement mutation controls in this slice.

## 3. Required views

Provide these views:

- Marketplace.
- Enabled.
- Updates.
- Profiles.
- Activity.

The implementation can use routes, tabs, or filtered states.

Keep the selected view in the URL when the current Flightplan router supports that behavior.

## 4. Marketplace page structure

Provide:

- Page title.
- Catalog synchronization status.
- Last synchronization time.
- `Sync now` action.
- Search input.
- Component-type filters.
- Summary counts.
- Component list.
- Component detail area.

Summary counts must include:

- Enabled components.
- Available updates.
- Conflicts.

Do not add decorative metrics that do not support a developer action.

## 5. Component list

Show:

- Component name.
- Component type.
- Concise description.
- Available version.
- Applied version when enabled.
- Enabled state.
- Update indicator.
- Conflict indicator.
- Compatibility indicator when incompatible.

Support filters for:

- All.
- Skills.
- Agents.
- Instructions.
- Prompts.
- Hooks.

Generate filters from backend-supported component types when possible.

Do not hard-code behavior for one named component.

## 6. Search

Search these fields:

- Name.
- Description.
- Component ID.
- Tags.
- Component type.

Use case-insensitive matching.

Keep search local when the complete component list is already loaded.

Show a clear empty state when no component matches.

## 7. Component detail

When the developer selects a component, show:

- Name.
- Type.
- Full description.
- Component ID.
- Available version.
- Applied version.
- Enabled state.
- Update state.
- Compatibility.
- Dependencies.
- Dependents.
- External dependencies and their availability status.
- Tags.
- Release summary.
- Conflict details.
- Applicable action.

Use one detail implementation for all component types.

Do not add component-name-specific presentation logic.

## 19. State management

Use the existing Flightplan frontend data layer.

Keep server state authoritative.

After a mutation:

- Use the mutation response when it contains complete refreshed state.
- Otherwise request the marketplace state again.

Do not duplicate dependency or conflict rules in the frontend.

The frontend can format backend data. The backend must make the decision.

## Focused tests

Test:

- Marketplace loading.
- Rendering every component type.
- Search and no-results behavior.
- Type and state filters.
- Selection and component details.
- URL-preserved view selection when supported by the router.
- Read-only loading and empty states.

## Completion gate

This slice is complete when developers can browse and inspect the complete
marketplace using server-authoritative data without mutation behavior.

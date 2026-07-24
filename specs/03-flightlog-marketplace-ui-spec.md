# Flightlog Context Marketplace User Interface Specification

## 1. Purpose

Implement the Context Marketplace user interface in Flightlog.

The page must let a developer inspect and manage all supported catalog component types.

This specification consumes the API from `02-flightlog-marketplace-backend-spec.md`.

This specification does not define catalog storage or filesystem projection.

## 2. Prerequisite

Complete the marketplace backend API before connecting mutation controls.

Use the supplied graphical mockup as a visual reference.

Follow Flightlog's existing frontend framework, routing, styling, state, and test conventions.

Do not add a new frontend framework only for this feature.

## 3. Required views

Provide these views:

- Marketplace.
- Enabled.
- Updates.
- Profiles.
- Activity.

The implementation can use routes, tabs, or filtered states.

Keep the selected view in the URL when the current Flightlog router supports that behavior.

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

## 8. Enable interaction

When a component has no disabled dependencies:

1. Send the enable request.
2. Disable the affected action controls.
3. Wait for backend confirmation.
4. Refresh marketplace state.
5. Show a concise result message.

When dependencies will also become enabled:

- Show the dependency IDs or names before confirmation.
- Explain that one action enables the complete required set.
- Send one backend operation after confirmation.

When a required external dependency is unavailable:

- Keep the component disabled.
- Show the external dependency name and type.
- Explain that it must be configured outside the marketplace.

When external dependency availability is unknown:

- Show a warning before enable.
- Explain that the component might not work until the dependency is configured.

Do not show the component as enabled before the backend confirms file projection.

## 9. Disable interaction

When no enabled dependent blocks the operation:

1. Send the disable request.
2. Disable the affected action controls.
3. Wait for backend confirmation.
4. Refresh marketplace state.
5. Show a concise result message.

When enabled dependents block the operation:

- Keep the component enabled.
- Show the dependent names.
- Explain that the developer must disable those dependents first.

Do not offer automatic cascade disable in the first release.

## 10. Update interaction

Show `Update` when the backend reports an available update.

Show:

- Applied version.
- Available version.
- Release summary.

After the developer selects `Update`:

1. Send the update request.
2. Show a working state.
3. Wait for backend confirmation.
4. Refresh marketplace state.
5. Show the result.

If the backend reports a local modification conflict:

- Keep the applied version unchanged.
- Show the affected relative paths.
- Explain that Flightlog preserved the local files.

Do not provide force overwrite in the first release.

## 11. Synchronization interaction

The `Sync now` action must:

- Show an active synchronization state.
- Prevent another synchronization request.
- Keep read-only page content available when possible.
- Display the final summary.

The summary must include:

- Catalog update result.
- Components updated.
- Components skipped.
- Conflicts.
- New available components.

Do not automatically show a new component as enabled.

## 12. Profiles

The Profiles view must show:

- Profile name.
- Description.
- Version.
- Component states that the profile declares.
- `Apply profile` action.

Before application, show:

- Components that will become enabled.
- Components that will become disabled.
- Dependencies that Flightlog will enable.

Explain that the profile does not lock later changes.

Refresh marketplace state after profile application.

## 13. Activity

The Activity view must show a bounded history.

Show:

- Timestamp.
- Operation.
- Component or profile name.
- Previous version.
- New version.
- Result.
- Conflict count.

Do not show file contents.

Use pagination or incremental loading when the existing Flightlog pattern requires it.

## 14. Conflict presentation

Use consistent conflict presentation for all component types.

Support:

- Unmanaged destination conflict.
- Local modification conflict.
- Target collision.
- Dependency conflict.
- External dependency unavailable.
- Catalog validation failure.
- Projection failure.

Show:

- Stable user-facing title.
- Concise explanation.
- Affected component.
- Relative path when applicable.
- Safe next action.

Do not expose:

- Stack traces.
- Secrets.
- Full home-directory paths.
- Raw backend exceptions.

## 15. Catalog failure state

When the backend reports an invalid catalog:

- Show that the current catalog cannot load.
- Show a concise validation summary.
- Disable mutation actions.
- Keep the last valid data visible when the backend provides it.
- Keep repository synchronization available when it can repair the catalog.

Do not display a partial invalid catalog as valid.

## 16. Initial migration state

When Flightlog requires migration:

- Explain that Flightlog will identify existing matching context files.
- Explain that Flightlog will preserve unmatched files.
- Provide one migration action.
- Show matching, conflicting, and unmanaged counts after migration.

Do not imply that Flightlog owns all existing `~/.copilot` files.

## 17. Responsive behavior

Support Flightlog's current desktop target.

At narrower widths:

- Stack the component detail below or above the list.
- Keep search and filters usable.
- Keep action controls visible.
- Avoid horizontal page scrolling.

Do not require a separate mobile application layout.

## 18. Accessibility

Meet the accessibility level that Flightlog currently requires.

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

## 19. State management

Use the existing Flightlog frontend data layer.

Keep server state authoritative.

After a mutation:

- Use the mutation response when it contains complete refreshed state.
- Otherwise request the marketplace state again.

Do not duplicate dependency or conflict rules in the frontend.

The frontend can format backend data. The backend must make the decision.

## 20. Error handling

Map stable backend error codes to concise user messages.

Provide a general fallback for an unknown error code.

Keep developer diagnostics in existing Flightlog logs.

Do not expose raw response bodies to the user.

## 21. Loading and empty states

Provide:

- Initial loading state.
- Synchronization state.
- Component mutation state.
- Empty catalog state.
- Empty search state.
- No enabled components state.
- No updates state.
- No activity state.

Do not replace the complete page with a spinner for a single component mutation.

## 22. Tests

Use the existing Flightlog frontend test tools.

Test:

- Marketplace loading.
- Component rendering.
- Search.
- Type filters.
- Selection and detail rendering.
- Enable success.
- Enable with dependencies.
- Enable blocked by an unavailable external dependency.
- Enable with unknown external dependency availability.
- Disable success.
- Disable blocked by dependents.
- Update success.
- Update conflict.
- Synchronization success.
- Synchronization failure.
- Profile preview.
- Profile application.
- Activity rendering.
- Catalog validation failure.
- Migration state.
- Empty states.
- Unknown API error.
- Keyboard interaction.
- Accessible labels.

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
- Existing Flightlog frontend tests pass.

## 24. Agent execution instructions

Inspect the existing Flightlog user interface before implementation.

Use the supplied graphical mockup as a design reference.

Follow existing Flightlog components and styles.

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

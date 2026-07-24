# Flightplan Marketplace UI: Actions and Workflows

## Purpose

Connect enable, disable, update, synchronization, profile, and activity
workflows to the stable backend API.

## Prerequisites

- Complete `03a-flightplan-marketplace-browser-spec.md`.
- Read `03-flightplan-marketplace-ui-spec.md` for shared UI invariants.
- Use the backend response as authoritative for every mutation.

Do not duplicate dependency, compatibility, or conflict decisions in the
frontend.

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
- Explain that Flightplan preserved the local files.

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
- Dependencies that Flightplan will enable.

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

Use pagination or incremental loading when the existing Flightplan pattern requires it.

## Focused tests

Test:

- Enable success and dependency preview.
- Required external dependency blocking.
- Unknown external dependency availability.
- Disable success and dependent blocking.
- Update success and update conflict response handling.
- Synchronization success and failure.
- Profile preview and application.
- Activity rendering.
- Mutation controls remaining pending until backend confirmation.

## Completion gate

This slice is complete when every supported marketplace mutation and preview is
wired to the backend and refreshed state appears only after backend
confirmation.

# Flightplan Marketplace UI: Resilience States

## Purpose

Implement consistent conflict, catalog-failure, migration, error, loading, and
empty-state experiences.

## Prerequisites

- Complete 03a and 03b.
- Read `03-flightplan-marketplace-ui-spec.md` for shared UI invariants.
- Consume backend error codes and conflict details without recreating backend
  policy.

## 14. Conflict presentation

Use consistent conflict presentation for all component types.

Support:

- Unmanaged destination conflict.
- Local modification conflict.
- Destination collision.
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

When Flightplan requires migration:

- Explain that Flightplan will identify existing matching context files.
- Explain that Flightplan will preserve unmatched files.
- Provide one migration action.
- Show matching, conflicting, and unmanaged counts after migration.

Do not imply that Flightplan owns all existing `~/.copilot` files.

## 20. Error handling

Map stable backend error codes to concise user messages.

Provide a general fallback for an unknown error code.

Keep developer diagnostics in existing Flightplan logs.

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

## Focused tests

Test:

- Every supported conflict category.
- Catalog validation failure and recovery action.
- Initial migration explanation, action, and result.
- Known and unknown API errors.
- Full-page initial loading versus scoped mutation loading.
- Empty catalog, search, enabled, update, and activity states.

## Completion gate

This slice is complete when all failure and transitional states preserve useful
context, provide an appropriate recovery path, and never imply unsafe file
ownership.

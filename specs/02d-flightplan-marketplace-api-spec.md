# Flightplan Marketplace Backend: API and Integration

## Purpose

Expose the completed marketplace domain through Flightplan's API, enforce
mutation concurrency, and prove the complete backend through integration tests.

## Prerequisites

- Complete 02a, 02b, and 02c in order.
- Read `02-flightplan-marketplace-backend-spec.md` for shared invariants.
- Treat the service behavior from the earlier slices as authoritative; route
  functions must not reimplement it.

## 19. API contract

Follow existing Flightplan API naming and response conventions.

Provide operations equivalent to:

```text
GET  /api/context-marketplace
POST /api/context-marketplace/sync
POST /api/context-marketplace/components/{component_id}/enable
POST /api/context-marketplace/components/{component_id}/disable
POST /api/context-marketplace/components/{component_id}/update
POST /api/context-marketplace/profiles/{profile_id}/apply
GET  /api/context-marketplace/activity
```

### 19.1 Marketplace response

Return:

- Catalog version.
- Source revision.
- Catalog validation status.
- Available component types.
- Profiles.
- Components.
- Enabled count.
- Update count.
- Conflict count.
- Last synchronization summary.

For each component, return:

- ID.
- Type.
- Name.
- Description.
- Available version.
- Applied version.
- Enabled state.
- Update state.
- Conflict state.
- Compatibility.
- Dependencies.
- Dependents.
- External dependencies and their availability status.
- Tags.
- Release summary.

### 19.2 Mutation response

Return:

- Operation result.
- Changed component IDs.
- Automatically enabled dependency IDs.
- Applied versions.
- Conflicts.
- Refreshed summary counts.

### 19.3 Error codes

Use stable codes:

```text
CATALOG_INVALID
CATALOG_SCHEMA_UNSUPPORTED
FLIGHTPLAN_VERSION_UNSUPPORTED
COMPONENT_NOT_FOUND
PROFILE_NOT_FOUND
DEPENDENCY_MISSING
DEPENDENCY_VERSION_MISMATCH
DEPENDENCY_IN_USE
COMPONENT_INCOMPATIBLE
EXTERNAL_DEPENDENCY_UNAVAILABLE
EXTERNAL_DEPENDENCY_VERSION_MISMATCH
DESTINATION_COLLISION
UNMANAGED_FILE_CONFLICT
LOCAL_MODIFICATION_CONFLICT
PROJECTION_FAILED
STATE_INVALID
STATE_WRITE_FAILED
AI_CONTEXT_UPDATE_FAILED
```

Do not expose stack traces.

Do not expose unrestricted home-directory paths.

## 20. Concurrency

Allow only one marketplace mutation at a time.

Protect:

- Repository synchronization.
- State changes.
- Filesystem projection.
- Initial migration.

Return a stable busy or conflict response for a concurrent mutation.

Read-only marketplace requests can continue when safe.

## Focused tests and completion

### 21.5 API tests

Test:

- Marketplace retrieval.
- Enable.
- Disable.
- Update.
- Profile application.
- Synchronization.
- Migration.
- Stable errors.
- Unknown IDs.
- Concurrent mutations.

## 22. Acceptance criteria

The backend is complete when:

- Flightplan loads the validated `ai-context` catalog.
- Flightplan persists marketplace state.
- Flightplan resolves dependencies.
- Flightplan enables every supported component type.
- Flightplan disables every supported component type safely.
- Flightplan detects available updates.
- Flightplan applies safe updates.
- Flightplan preserves unmanaged files.
- Flightplan preserves locally modified managed files.
- Flightplan reports conflicts.
- Flightplan supports profiles.
- Flightplan migrates the existing broad-copy installation.
- Flightplan exposes the required API.
- Flightplan records activity.
- Backend tests pass.
- Existing Flightplan tests pass.

## 23. Agent execution instructions

Inspect Flightplan before selecting modules, routes, models, or persistence.

Follow existing architectural patterns.

Use the supplied catalog templates as contract examples.

Keep domain logic out of route functions.

Keep filesystem logic out of frontend-facing models.

Do not weaken a file-safety requirement.

Do not overwrite unrelated working-tree changes.

Run focused tests after each implementation slice.

Run the complete backend test suite before completion.

Report:

- Modules changed.
- State storage added.
- API operations added.
- Migration behavior.
- Tests run.
- Remaining limitations.

## Completion gate

This slice and the backend sequence are complete only when every acceptance
criterion above is satisfied, the focused suites from 02a through 02d pass, and
the existing Flightplan backend suite remains green.

# Flightplan Marketplace Backend: Lifecycle Operations

## Purpose

Implement repository synchronization, profile application, initial migration,
and bounded activity history using the foundation and projection engine.

## Prerequisites

- Complete `02a-flightplan-marketplace-foundation-spec.md`.
- Complete `02b-flightplan-marketplace-projection-spec.md`.
- Read `02-flightplan-marketplace-backend-spec.md` for shared invariants.

Do not add the public HTTP routes in this slice.

## 15. Repository synchronization

Use the existing Flightplan `ai-context` installation and update mechanism.

The synchronization operation must:

- Update the local checkout.
- Load the new catalog.
- Validate the new catalog.
- Preserve the previous valid catalog when validation fails.
- Calculate component updates.
- Apply safe updates to enabled components.
- Keep disabled components absent from the Copilot home directory.
- Keep new components disabled unless an initial default applies.
- Return updates, skips, and conflicts.

Do not automatically enable a newly added component during normal synchronization.

## 16. Profiles

When Flightplan applies a profile:

- Load the profile from the valid catalog.
- Apply only listed component states.
- Resolve dependencies.
- Validate the complete operation before file writes.
- Project the resulting desired state.
- Record the profile ID and version in activity.

Profiles must not lock later user changes.

## 17. Initial migration

Flightplan currently copies broad `ai-context` content into `~/.copilot`.

Implement a one-time migration:

1. Load the valid catalog.
2. Calculate each component's expected destination files.
3. Compare destination content with current payload content.
4. Mark a component enabled when all expected files match.
5. Record matching hashes.
6. Mark partial matches as conflicts.
7. Leave unmatched files unmanaged.
8. Save migrated state atomically.
9. Record the migration result.

Do not claim ownership from a matching path alone.

Require matching file content before Flightplan records ownership.

Do not delete a file during migration.

## 18. Activity history

Store a bounded activity history.

Each record must include:

- Timestamp.
- Operation.
- Component or profile ID when applicable.
- Previous version.
- New version.
- Result.
- Conflict count.
- Source revision.

Do not record payload contents.

Do not record secrets.

## Focused tests

Test:

- Successful and failed repository synchronization.
- Preservation of the previous valid catalog.
- Safe updates of enabled components after synchronization.
- New components remaining disabled unless an initial default applies.
- Profile preview and merge application.
- Profile dependency and external-dependency handling.
- Successful migration from matching broad-copy files.
- Partial-match migration conflicts.
- Unmatched-file preservation.
- Migration idempotency.
- Activity creation, ordering, and retention bounds.
- Absence of payload contents and secrets in activity records.

## Completion gate

This slice is complete when synchronization, profiles, migration, and activity
operate through the services from 02a and 02b without bypassing projection
safety or corrupting state.

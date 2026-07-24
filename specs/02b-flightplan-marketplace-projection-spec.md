# Flightplan Marketplace Backend: Dependency and Projection Engine

## Purpose

Implement type-independent dependency resolution and safe projection planning
and execution for enable, disable, and update operations.

## Prerequisites

- Complete `02a-flightplan-marketplace-foundation-spec.md`.
- Read `02-flightplan-marketplace-backend-spec.md` for shared invariants.
- Reuse the catalog and state models established in 02a.

Do not add HTTP routes, repository synchronization, profiles, or migration in
this slice.

## 9. Dependency resolution

When the user enables a component:

- Resolve all transitive dependencies.
- Validate dependency version constraints.
- Detect cycles.
- Return the complete dependency plan.
- Enable required dependencies in the same operation.

When the user disables a component:

- Identify enabled dependents.
- Reject the operation when an enabled dependent exists.
- Return the dependent component IDs.

Do not implement automatic cascade disable in the first release.

Use the same dependency behavior for every component type.

For external dependencies:

- Preserve the declared type, ID, name, description, required flag, and version
  constraint in the domain model.
- Determine `available`, `unavailable`, or `unknown` status through an existing
  Flightplan integration when one exists.
- Treat a detected version that does not satisfy the declared constraint as
  unavailable.
- Do not install, configure, or store credentials for an MCP server.
- Reject enable with `EXTERNAL_DEPENDENCY_UNAVAILABLE` when a required external
  dependency is known to be unavailable.
- Use `EXTERNAL_DEPENDENCY_VERSION_MISMATCH` when the dependency is present but
  its detected version does not satisfy the constraint.
- Preserve an `unknown` status when Flightplan cannot determine availability.

Profiles inherit external dependencies through their components. Profile
application must include those requirements in its operation preview and apply
the same enable checks.

## 10. Desired-state calculation

Calculate one desired filesystem state from:

- The valid catalog.
- Enabled component selections.
- Resolved dependencies.
- Component source declarations.
- The active Copilot home directory.

For every source file, derive its destination by appending the unchanged
repository-relative source path to the active Copilot home directory.

Validate all destination collisions before a write.

Return a deterministic operation plan.

The plan must identify:

- Files to create.
- Files to update.
- Files to remove.
- Files to preserve.
- Dependency changes.
- Conflicts.

## 11. Projection safety

The projection service must not overwrite or delete an unmanaged file.

The projection service must not overwrite or delete a locally modified managed file.

For the first release:

- Report the conflict.
- Skip the affected component.
- Preserve the local file.
- Do not provide force overwrite.

Validate every source and destination path before a file operation.

Reject:

- Absolute manifest paths.
- Path traversal.
- A source path outside the checkout.
- A destination path outside the Copilot home directory.
- A source symlink that resolves outside the checkout.
- A destination symlink that resolves outside the Copilot home directory.

Use temporary files and atomic replacement when the operating system supports the operation.

Update marketplace state only after a successful component projection.

## 12. Enable operation

Implement this sequence:

1. Load the valid catalog.
2. Resolve the requested component.
3. Resolve transitive dependencies.
4. Build the desired operation plan.
5. Validate destination paths.
6. Detect collisions.
7. Detect unmanaged destination files.
8. Detect local modifications.
9. Apply safe file writes.
10. Record file hashes.
11. Record applied component versions.
12. Save state atomically.
13. Record activity.
14. Return refreshed marketplace data.

Stop before file writes when a conflict affects the requested operation.

## 13. Disable operation

Implement this sequence:

1. Load the valid catalog.
2. Find enabled dependents.
3. Reject the operation when a dependent exists.
4. Compare each managed file with its installed hash.
5. Remove each unchanged managed file.
6. Preserve each modified managed file.
7. Remove only empty directories that Flightplan created.
8. Preserve directories that contain unmanaged files.
9. Clear the applied version after safe completion.
10. Save state atomically.
11. Record activity.
12. Return refreshed marketplace data.

If a modified managed file remains, return a conflict result.

Do not claim that the component is fully removed while a preserved managed file remains unresolved.

## 14. Update operation

An update exists when the available version is newer than the applied version.

Implement this sequence:

1. Load the current component manifest.
2. Compare the available and applied versions.
3. Calculate source changes and their identically relative destinations.
4. Detect local modifications.
5. Stop when a local modification conflicts with the update.
6. Apply new and changed files.
7. Remove obsolete unchanged managed files.
8. Record new hashes.
9. Record the new applied version.
10. Save state atomically.
11. Record activity.
12. Return refreshed marketplace data.

Do not treat a Git revision change alone as a component update.

## Focused tests

### 21.3 Dependency tests

Test:

- No dependencies.
- Direct dependencies.
- Transitive dependencies.
- Missing dependencies.
- Version mismatch.
- Dependency cycles.
- Blocked disable.
- Available, unavailable, and unknown external dependencies.
- Profile application with an unavailable required external dependency.
- Operation without an MCP installation or configuration attempt.

### 21.4 Projection tests

Use temporary checkout and Copilot home directories.

Test:

- Each supported component type.
- Single-file payloads.
- Directory payloads.
- Multiple file sources.
- New file creation.
- Existing managed file updates.
- Unmanaged file preservation.
- Local modification preservation.
- Safe disable.
- Obsolete file removal.
- Destination collisions.
- Path traversal.
- Unsafe symlinks.
- `COPILOT_HOME`.
- Partial failure.
- State consistency after failure.

## Completion gate

This slice is complete when the dependency and projection services can plan and
apply enable, disable, and update operations atomically while preserving
unmanaged and locally modified files. All dependency and projection tests must
pass before lifecycle orchestration begins.

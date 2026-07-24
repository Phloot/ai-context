# Flightlog Context Marketplace Backend Specification

## 1. Purpose

Implement the Context Marketplace backend in Flightlog.

The backend must consume the versioned catalog from the local `ai-context` checkout.

The backend must manage each developer's enabled components and active Copilot files.

This specification does not define the page layout or visual design.

## 2. Prerequisite

Complete `01-ai-context-catalog-spec.md` before this work.

The installed `ai-context` checkout must contain:

```text
catalog/catalog.yaml
catalog/components/{agents,hooks,instructions,prompts,skills}/*.yaml
catalog/profiles/*.yaml
catalog/schema/*.json
```

The checkout can also contain `catalog/schema/catalog.cue`, which is the
authoring source for the generated JSON Schemas. Flightlog must not require or
execute the CUE CLI. Its runtime contract is the YAML manifests plus the
committed JSON Schemas.

## 3. Required behavior

The backend must:

- Locate the installed `ai-context` checkout.
- Install or update the checkout through the existing Flightlog workflow.
- Load and validate the catalog.
- Store local marketplace state.
- Calculate available updates.
- Resolve component dependencies.
- Enable and disable every supported component type.
- Project enabled payloads into the active Copilot home directory.
- Preserve unmanaged files.
- Detect locally modified managed files.
- Expose a stable FastAPI API.
- Record bounded activity history.

## 4. Architecture

Inspect the existing Flightlog structure before implementation.

Follow existing router, service, model, persistence, configuration, logging, and test patterns.

Keep these responsibilities separate:

- Catalog loading.
- Catalog validation.
- Marketplace state persistence.
- Dependency resolution.
- Desired-state calculation.
- Filesystem projection.
- Repository synchronization.
- Activity recording.
- API routing.

Do not put filesystem operations in FastAPI route functions.

Do not put API response construction in the projection service.

## 5. Catalog loader

Implement a catalog loader that:

- Resolves the configured `ai-context` checkout.
- Loads `catalog/catalog.yaml`.
- Recursively loads all component manifests from the five type directories.
- Loads all profile manifests.
- Validates manifest structure against the committed JSON Schemas.
- Performs the complete semantic catalog validation required by this
  specification.
- Returns typed domain models.
- Caches the most recent valid catalog when appropriate.
- Invalidates its cache after repository synchronization.

If a new catalog is invalid:

- Preserve the previous valid catalog.
- Do not project files from the invalid catalog.
- Return a catalog validation error.
- Record the failed synchronization.

Reject a catalog when:

- Its schema version is unsupported.
- Its minimum Flightlog version is newer than the running Flightlog version.
- Any manifest or semantic validation fails.

## 6. Copilot home resolution

Resolve the active Copilot home directory in this order:

1. Use `COPILOT_HOME` when it has a nonempty value.
2. Use the existing Flightlog Copilot-home configuration when present.
3. Use `~/.copilot`.

Resolve the final path before each synchronization operation.

Do not store an expanded user home path in portable marketplace state.

## 7. Marketplace state

Use Flightlog's existing persistence mechanism when suitable.

Store state outside:

- The `ai-context` checkout.
- Managed Copilot payload directories.
- Any directory that repository synchronization replaces.

Use a model equivalent to:

```json
{
  "schemaVersion": 1,
  "catalogVersion": "2026.07.1",
  "sourceRevision": "<git-revision>",
  "components": {
    "<component-id>": {
      "enabled": true,
      "appliedVersion": "1.2.0",
      "files": {
        "skills/<component>/SKILL.md": {
          "sourceHash": "sha256:<hash>",
          "installedHash": "sha256:<hash>"
        }
      }
    }
  }
}
```

Store destination paths relative to the Copilot home directory.

Use SHA-256 for source and installed hashes.

Save state atomically.

Do not silently discard corrupt state.

Return a recovery error when state cannot load safely.

## 8. Component states

Use these backend states:

- `available`
- `enabled`
- `disabled`
- `update_available`
- `conflict`
- `incompatible`
- `external_dependency_unavailable`

One component can have more than one status attribute.

For example, an enabled component can also have an available update.

Do not infer enabled state only from destination-path existence.

Use marketplace state and file verification together.

Evaluate compatibility against the current operating system and Flightplan's
configured Copilot surface. The supported surface values are `cli`, `intellij`,
and `vscode`.

Mark a component `incompatible` when either compatibility dimension excludes
the current environment. Reject an enable operation when the requested
component or any required component is incompatible.

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
  Flightlog integration when one exists.
- Treat a detected version that does not satisfy the declared constraint as
  unavailable.
- Do not install, configure, or store credentials for an MCP server.
- Reject enable with `EXTERNAL_DEPENDENCY_UNAVAILABLE` when a required external
  dependency is known to be unavailable.
- Use `EXTERNAL_DEPENDENCY_VERSION_MISMATCH` when the dependency is present but
  its detected version does not satisfy the constraint.
- Preserve an `unknown` status when Flightlog cannot determine availability.

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
7. Remove only empty directories that Flightlog created.
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

## 15. Repository synchronization

Use the existing Flightlog `ai-context` installation and update mechanism.

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

When Flightlog applies a profile:

- Load the profile from the valid catalog.
- Apply only listed component states.
- Resolve dependencies.
- Validate the complete operation before file writes.
- Project the resulting desired state.
- Record the profile ID and version in activity.

Profiles must not lock later user changes.

## 17. Initial migration

Flightlog currently copies broad `ai-context` content into `~/.copilot`.

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

Require matching file content before Flightlog records ownership.

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

## 19. API contract

Follow existing Flightlog API naming and response conventions.

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
FLIGHTLOG_VERSION_UNSUPPORTED
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

## 21. Tests

### 21.1 Catalog tests

Test:

- Valid catalog loading.
- Invalid catalog rejection.
- Unsupported schema.
- Catalog loading when the CUE CLI is not installed.
- Unsupported Flightlog version.
- Cache invalidation.
- Previous-catalog preservation.

### 21.2 State tests

Test:

- Empty state.
- Valid state.
- Atomic writes.
- Corrupt state.
- Unsupported state schema.
- State migration.

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
- Target collisions.
- Path traversal.
- Unsafe symlinks.
- `COPILOT_HOME`.
- Partial failure.
- State consistency after failure.

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

- Flightlog loads the validated `ai-context` catalog.
- Flightlog persists marketplace state.
- Flightlog resolves dependencies.
- Flightlog enables every supported component type.
- Flightlog disables every supported component type safely.
- Flightlog detects available updates.
- Flightlog applies safe updates.
- Flightlog preserves unmanaged files.
- Flightlog preserves locally modified managed files.
- Flightlog reports conflicts.
- Flightlog supports profiles.
- Flightlog migrates the existing broad-copy installation.
- Flightlog exposes the required API.
- Flightlog records activity.
- Backend tests pass.
- Existing Flightlog tests pass.

## 23. Agent execution instructions

Inspect Flightlog before selecting modules, routes, models, or persistence.

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

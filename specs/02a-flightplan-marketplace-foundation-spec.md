# Flightplan Marketplace Backend: Foundation

## Purpose

Establish the backend architecture, catalog loader, Copilot-home resolution,
persistent marketplace state, and component-state model.

## Prerequisites

- The `ai-context` repository satisfies `01-ai-context-catalog-spec.md`.
- Read `02-flightplan-marketplace-backend-spec.md` for shared invariants and
  the complete backend delivery sequence.
- Inspect Flightplan before choosing modules, persistence, or configuration.

Do not implement filesystem mutations or HTTP routes in this slice.

## 4. Architecture

Inspect the existing Flightplan structure before implementation.

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
- Its minimum Flightplan version is newer than the running Flightplan version.
- Any manifest or semantic validation fails.

## 6. Copilot home resolution

Resolve the active Copilot home directory in this order:

1. Use `COPILOT_HOME` when it has a nonempty value.
2. Use the existing Flightplan Copilot-home configuration when present.
3. Use `~/.copilot`.

Resolve the final path before each synchronization operation.

Do not store an expanded user home path in portable marketplace state.

## 7. Marketplace state

Use Flightplan's existing persistence mechanism when suitable.

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

## Focused tests

### 21.1 Catalog tests

Test:

- Valid catalog loading.
- Invalid catalog rejection.
- Unsupported schema.
- Catalog loading when the CUE CLI is not installed.
- Unsupported Flightplan version.
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

## Completion gate

This slice is complete when Flightplan can load a valid catalog without CUE,
preserve the previous valid catalog after a failed refresh, resolve the active
Copilot home, persist state atomically, and expose tested domain models for the
next slice.

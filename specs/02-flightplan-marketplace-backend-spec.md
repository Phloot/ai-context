# Flightplan Context Marketplace Backend Plan

## 1. Purpose

Coordinate implementation of the Context Marketplace backend in Flightplan.

The backend consumes the versioned catalog from a local `ai-context` checkout,
manages each developer's enabled components, and safely projects component
payloads into the active Copilot home directory.

This plan defines shared invariants and execution order. The four implementation
specifications contain the detailed requirements and tests.

## 2. Prerequisite contract

Complete `01-ai-context-catalog-spec.md` before backend implementation.

The installed `ai-context` checkout must contain:

```text
catalog/catalog.yaml
catalog/components/{agents,hooks,instructions,prompts,skills}/*.yaml
catalog/profiles/*.yaml
catalog/schema/*.json
```

The checkout can also contain `catalog/schema/catalog.cue`, but Flightplan must
not require or execute CUE. Its runtime contract is the YAML manifests and
committed JSON Schemas.

## 3. Implementation sequence

Implement and review these specifications in order:

1. `02a-flightplan-marketplace-foundation-spec.md`
2. `02b-flightplan-marketplace-projection-spec.md`
3. `02c-flightplan-marketplace-lifecycle-spec.md`
4. `02d-flightplan-marketplace-api-spec.md`

Do not start a later specification until the preceding completion gate and
focused tests pass.

### 3.1 Foundation output

02a establishes:

- Architectural boundaries.
- Catalog loading and validation.
- Copilot-home resolution.
- Persistent marketplace state.
- Component status models.

### 3.2 Projection output

02b establishes:

- Component and external-dependency resolution.
- Deterministic desired-state planning.
- Safe file projection.
- Enable, disable, and update operations.

### 3.3 Lifecycle output

02c establishes:

- Repository synchronization.
- Profile application.
- Initial broad-copy migration.
- Bounded activity history.

### 3.4 API output

02d establishes:

- Stable FastAPI operations and error codes.
- Mutation concurrency.
- Backend integration tests.
- Overall backend acceptance.

The API produced by 02d is the input contract for the user-interface sequence.

## 4. Shared invariants

Every backend slice must preserve these rules:

- Inspect Flightplan and follow its existing router, service, model,
  persistence, configuration, logging, and test patterns.
- Keep domain logic out of route functions.
- Keep filesystem behavior out of frontend-facing response models.
- Treat component IDs as globally unique across component types.
- Use the same dependency behavior for every component type.
- Obtain a dependency's type and source paths from its referenced manifest.
- Treat each component source path as the identical relative destination under
  the active Copilot home.
- Preserve unmanaged files.
- Preserve locally modified managed files.
- Reject absolute paths, traversal, unsafe symlinks, and destination
  collisions.
- Do not infer enabled state only from destination-path existence.
- Do not install or configure external dependencies such as MCP servers.
- Save marketplace state atomically.
- Update state only after successful projection.
- Preserve the previous valid catalog when a synchronized catalog is invalid.
- Do not expose secrets, payload contents, stack traces, or unrestricted home
  paths.
- Do not overwrite unrelated working-tree changes.

## 5. Required end state

After all four specifications:

- Flightplan loads the validated catalog without requiring CUE.
- Flightplan persists and verifies marketplace state.
- Flightplan resolves component and external dependencies.
- Flightplan safely enables, disables, and updates every component type.
- Flightplan synchronizes the catalog without silently enabling new
  components.
- Flightplan applies profiles using merge behavior.
- Flightplan migrates matching files from the previous broad-copy behavior.
- Flightplan records bounded activity without sensitive content.
- Flightplan exposes the stable marketplace API.
- Focused and complete backend tests pass.
- Existing Flightplan tests pass.

## 6. Agent handoff protocol

For each implementation specification:

1. Provide this plan, specs 00 and 01, and only the current detailed slice.
2. Provide the Flightplan repository and the installed or fixture
   `ai-context` checkout.
3. Require the agent to inspect existing architecture before implementation.
4. Require focused tests after each coherent implementation unit.
5. Review the completion gate before starting the next slice.
6. Use a fresh task or context for the next specification.

Each agent must report:

- Modules changed.
- Behavior completed.
- Tests run.
- Remaining limitations or deferred work.

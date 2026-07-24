# Context Marketplace Handoff

Temporary handoff for moving the catalog into the on-premises `ai-context`
repository and implementing the marketplace in Flightplan. Remove this file
with the rest of `specs/` after delivery.

## What is complete

The public `ai-context` repository now contains:

- A versioned marketplace catalog.
- CUE-authored schemas and committed generated JSON Schemas.
- Catalog validation, version-change validation, and tests.
- Contributor guidance in `README.md` and `AGENTS.md`.
- A uv-based development environment and Make targets.
- Sequential implementation plans for the Flightplan backend and UI.

The catalog implementation and granular specification baseline are present by
commit `af5e898`; use the latest `main`.

## Settled architecture

### Catalog concepts

- The **catalog** is the complete versioned marketplace release.
- A **component** is one independently selectable skill, agent, instruction,
  prompt, or hook set.
- A **profile** is a versioned recommendation of enabled or disabled component
  states. It does not own payloads or lock later user changes.

### Component manifests

Component manifests are grouped by type:

```text
catalog/components/
├── agents/
├── hooks/
├── instructions/
├── prompts/
└── skills/
```

The manifest directory must agree with its declared `type`. Component IDs are
globally unique across all directories, and validation rejects duplicates.

### Projection

The repository mirrors the Copilot home layout. Every declared source path is
installed at the identical path relative to the active Copilot home:

```text
<repository>/<source-path> -> <COPILOT_HOME>/<source-path>
```

There is no separate installation target or mapping field.

### Dependencies

- `dependencies` reference another catalog component by globally unique ID and
  optional version constraint.
- Flightplan obtains the dependency's type and source paths from the referenced
  component manifest. Dependency entries do not repeat the type.
- `external_dependencies` describe prerequisites Flightplan cannot install,
  currently MCP servers.
- Flightplan reports external dependency availability but does not configure
  servers, credentials, or secrets.

The maintainability hook depends on the `maintainable-code` skill because its
injected context tells delegated agents to invoke that skill.

### Compatibility and defaults

- Supported operating systems: `macos`, `linux`.
- Supported Copilot surfaces: `cli`, `intellij`, `vscode`.
- Remote cloud execution is intentionally out of scope.
- `default_state: available` means visible but not automatically enabled.
- `default_state: enabled` is reserved for a universal baseline applied on the
  first managed installation. It must not enable new components during normal
  synchronization.
- Profiles are preferred over `enabled` defaults for recommended bundles.

### Schema and tooling

- `catalog/schema/catalog.cue` is authoritative.
- Generated `catalog/schema/*.schema.json` files are committed for Flightplan.
- Flightplan consumes YAML and JSON Schema and must not require CUE at runtime.
- CUE is pinned to v0.17.1.
- Python dependencies and Ruff configuration live in `pyproject.toml`.
- Development commands use uv exclusively.
- `make setup` creates the environment; `make check BASE=<revision>` runs the
  complete non-mutating validation suite.

## Tomorrow: move into on-premises `ai-context`

1. Clone or pull the latest public `main`.
2. Create a working branch in the on-premises `ai-context` repository.
3. Merge the new catalog, schema, validation, CI, documentation, and spec files
   with the on-premises payloads.
4. Preserve existing on-premises payload behavior and unrelated changes.
5. Add a manifest for every independently selectable on-premises payload.
6. Add external MCP requirements where a component depends on an MCP server.
7. Update profiles only for intentional recommended bundles.
8. Increment `catalog_version` for the resulting on-premises catalog release.
9. Run:

   ```shell
   make setup
   make check BASE=<target-branch>
   ```

10. Resolve every ownership, dependency, schema, and versioning error before
    merging.
11. Commit the on-premises catalog foundation.

## Flightplan implementation order

Read the [delivery roadmap](00-context-marketplace-roadmap.md) and
[catalog contract](01-ai-context-catalog-spec.md) first.

### Backend

Read the [backend plan](02-flightplan-marketplace-backend-spec.md), then
implement and review:

1. [02a — foundation](02a-flightplan-marketplace-foundation-spec.md)
2. [02b — dependencies and projection](02b-flightplan-marketplace-projection-spec.md)
3. [02c — lifecycle operations](02c-flightplan-marketplace-lifecycle-spec.md)
4. [02d — API and integration](02d-flightplan-marketplace-api-spec.md)

Do not start a later slice until the preceding completion gate and focused
tests pass.

### User interface

After the complete backend API is stable, read the
[UI plan](03-flightplan-marketplace-ui-spec.md), then implement and review:

1. [03a — browser and read-only state](03a-flightplan-marketplace-browser-spec.md)
2. [03b — actions and workflows](03b-flightplan-marketplace-actions-spec.md)
3. [03c — resilience states](03c-flightplan-marketplace-resilience-spec.md)
4. [03d — quality and acceptance](03d-flightplan-marketplace-ui-quality-spec.md)

## How to brief each implementation agent

The implementation plans are agent-vendor-neutral.

For each slice, give the agent:

- The Flightplan repository.
- The integrated on-premises `ai-context` checkout or representative fixtures.
- Specs 00 and 01.
- The applicable 02 or 03 orchestration plan.
- All sibling slice specifications for forward context.
- A clear instruction to implement only the current slice.

Suggested prompt:

> Read specs 00 and 01, the applicable orchestration plan, and every sibling
> slice so you understand the complete sequence. Implement only the current
> slice. Treat later slices as forward design constraints, not current scope.
> Inspect the existing Flightplan architecture before choosing modules or
> frameworks. Preserve unrelated work, run the focused tests, satisfy the
> completion gate, and stop. Report changed modules, completed behavior, tests,
> and limitations.

Use a fresh task for each slice while retaining the code and commit history from
previous slices. Small interface extensions are expected; later slices should
not replace the architecture established by earlier slices without documenting
a genuine conflict.

## Review checkpoints

Before advancing to the next slice, confirm:

- The current completion gate is satisfied.
- Focused tests and existing relevant tests pass.
- No future slice was implemented prematurely.
- Public interfaces needed by the next slice are clear.
- File safety and server-authoritative decision rules remain intact.
- The slice is committed independently for review and rollback.

After 03d passes final acceptance, remove `specs/` from the production
repositories as planned.

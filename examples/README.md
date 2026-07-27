# Context Marketplace implementation example

This directory is a runnable handoff example for the Flightplan marketplace
specifications in `../specs`. Treat this directory as the example application
package (`<appname>`). It demonstrates integration boundaries and HTTP/UI
behavior; it intentionally does **not** implement production catalog loading,
persistent state, Git synchronization, or safe filesystem projection.

## Why it is structured this way

```text
examples/
├── domains/       # Framework-free marketplace concepts and expected failures
├── schemas/       # Strict Pydantic HTTP contracts
├── services/      # Orchestration and server-authoritative decisions
├── routers/       # Thin FastAPI transport functions
├── static/        # Vanilla JavaScript and small Bootstrap-specific additions
├── templates/     # Marketplace page shell
└── tests/         # API-boundary examples
```

The important dependency direction is `router -> service -> domain/adapters`.
Route functions do not decide dependency, compatibility, conflict, or file
safety policy. The browser formats backend decisions and never marks a mutation
complete before the backend confirms it.

## Run it

From the repository root:

```shell
uv sync --project examples
uv run --project examples uvicorn examples.main:app --reload
```

Open `http://127.0.0.1:8000/marketplace`.

The page links Bootstrap from a CDN only to keep this example small. In
Flightplan, use its existing pinned Bootstrap assets and page shell.

Run the focused checks:

```shell
uv run --project examples pytest examples/tests
uv run --project examples ruff check examples
uv run --project examples ruff format --check examples
```

## Production replacement map

Keep the router and Pydantic contracts stable while replacing
`MarketplaceService.example()` with injected production adapters:

1. `CatalogRepository`: load YAML, validate with committed JSON Schemas, run
   semantic validation, and preserve the last valid catalog.
2. `MarketplaceStateRepository`: read and atomically write versioned state
   outside both the checkout and Copilot home payload directories.
3. `DependencyResolver`: validate transitive component dependencies, versions,
   cycles, dependents, compatibility, and external dependency status.
4. `ProjectionPlanner` and `ProjectionExecutor`: produce deterministic plans;
   reject traversal, unsafe symlinks, collisions, unmanaged files, and locally
   modified managed files; write atomically and update state only after success.
5. `AiContextRepository`: synchronize the existing checkout, invalidate the
   catalog cache, and retain the previous valid catalog after validation errors.
6. `ActivityRepository`: retain a bounded, non-sensitive operation history.

SQLite is not required for the reference UI. If Flightplan's existing
persistence conventions use SQLite, put SQL behind the state and activity
repository interfaces; do not let ORM records become API models.

## Intentional limitations

- Versions are compared for inequality in the demo. Production must use
  Semantic Versioning and enforce dependency constraints.
- Mutation state is in memory and resets on restart.
- Sync and migration return representative results without touching Git or the
  filesystem.
- Browser confirmations demonstrate previews using server-provided dependency
  data. If the production backend adds preview endpoints, prefer those for a
  fully authoritative operation plan.
- The JavaScript test seam is the network boundary. Add the existing Flightplan
  frontend test tooling for search, filters, focus restoration, announcements,
  narrow layouts, conflicts, and every loading/empty state from specs 03a–03d.

## Implementation order for the next agent

Follow the spec slices in order: 02a foundation, 02b projection, 02c lifecycle,
02d API, then 03a–03d UI. After each slice, run its focused tests and stop at its
completion gate. The example spans the final contract for orientation; it is
not permission to skip the safety-focused backend slices.

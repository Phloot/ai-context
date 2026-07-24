# Repository guidance

This repository stores native Copilot payloads and the metadata that Flightplan
uses to publish them in the Context Marketplace.

## Before changing the repository

1. Read `README.md` and the manifests adjacent to the affected payload.
2. Inspect the working tree and preserve unrelated changes.
3. Identify the owning component before editing a payload.
4. Do not change payload behavior as part of metadata-only work.

## Catalog contract

- Keep selectable payloads in `agents/`, `hooks/`, `instructions/`, `prompts/`,
  or `skills/`.
- Keep marketplace metadata under `catalog/`.
- Treat `catalog/schema/catalog.cue` as the schema source of truth.
- Treat `catalog/schema/*.schema.json` as generated, committed artifacts for
  Flightplan and other consumers that do not use CUE.
- Do not edit generated JSON Schemas by hand.
- Keep the YAML manifests as the runtime catalog contract. Flightplan must not
  need the CUE CLI to load a released catalog.
- Give every selectable payload exactly one component owner.
- Keep component IDs stable and lowercase kebab-case.
- Group component manifests under `catalog/components/agents/`, `hooks/`,
  `instructions/`, `prompts/`, or `skills/` according to their declared type.
- Treat every source path as its Copilot-home-relative destination path.

## Adding or changing a component

Follow the contributor checklist in `README.md`.

For every payload change:

- Update the owning component version using Semantic Versioning.
- Update `release.summary`.
- Add new payload files to the existing source declaration or create a new component
  manifest when they are independently selectable.
- Update dependencies and profiles when behavior requires it.
- Declare MCP servers and other non-installable prerequisites under
  `external_dependencies`; do not model them as catalog components.
- Increment `catalog_version` when the released catalog changes.

Do not add marketplace fields to `SKILL.md` frontmatter or payload files.

## Validation

Use CUE v0.17.1.

Run:

```shell
make check BASE=HEAD
```

If GNU Make is unavailable, run:

```shell
uv run python scripts/generate_schemas.py --check
uv run python scripts/validate_catalog.py
uv run python scripts/validate_catalog.py --base HEAD
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
```

Before completion, run the file-growth check described by the
`maintainable-code` skill and report unavailable configured analyzers.

Ruff covers repository tooling under `scripts/` and `tests/`. Versioned payload
code under `hooks/` and `skills/` stays on its component-specific validation so
an unrelated tooling change does not rewrite payload content.

When the catalog wire format or generated JSON Schema contract changes, keep
the CUE source, generated schemas, validator, tests, and README consistent.

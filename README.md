# ai-context

Reusable Copilot context components and their Flightplan marketplace catalog.

## Repository layout

| Path | Purpose |
| --- | --- |
| `agents/` | Selectable Copilot agents. |
| `hooks/` | Selectable hook configurations and their scripts. |
| `instructions/` | Selectable instruction files. |
| `prompts/` | Selectable prompt files. |
| `skills/` | Selectable skills, one component per skill directory. |
| `catalog/components/<type-plural>/` | Component manifests grouped by payload type. |
| `catalog/profiles/` | Versioned recommended component states. |
| `catalog/schema/catalog.cue` | Authoritative catalog schema. |
| `catalog/schema/*.schema.json` | Generated schemas consumed by Flightplan and other non-CUE tools. |

The YAML files under `catalog/` are the runtime wire format. CUE is used to
author and validate the schema; Flightplan does not need CUE to read a released
catalog.

## Key concepts

### Catalog

The catalog is the complete, versioned marketplace release. It consists of:

- `catalog/catalog.yaml`, which declares the schema and catalog release version.
- Every component manifest under `catalog/components/`.
- Every profile manifest under `catalog/profiles/`.

The catalog describes what is available. It does not represent one developer's
enabled state.

### Component

A component is one independently selectable item, such as a skill, instruction,
agent, prompt, or hook set. It combines:

- A native payload under `skills/`, `instructions/`, `agents/`, `prompts/`, or
  `hooks/`.
- One manifest under its matching type directory in `catalog/components/`.
- Its own stable ID and Semantic Version.
- Source paths, compatibility, dependencies, and release summary.

Component dependencies point to other components that Flightplan can enable.
External dependencies describe prerequisites, such as MCP servers, that must be
configured outside the marketplace.

Component IDs are globally unique across every component type directory. The
validator rejects an ID that is reused by an agent, hook, instruction, prompt,
or skill.

A component dependency declares only the referenced component ID and optional
version constraint. Flightplan obtains its type, source paths, and other
metadata from that component's manifest, so dependency entries must not repeat
the component type.

Compatibility declares where a component is expected to work. Supported
Copilot surfaces are `cli`, `intellij`, and `vscode`. Flightplan uses the
operating-system and surface declarations to identify incompatible components;
the declarations do not change where files are installed.

### Profile

A profile is a versioned, named set of recommended enabled or disabled
component states. Applying a profile:

- Changes only the components listed by that profile.
- Uses `merge` behavior.
- Resolves the selected components' dependencies.
- Inherits their external dependencies.
- Does not copy files itself.
- Does not lock later user changes.

Profiles are recommendations over components; they are not components and do
not own payload files.

## Prerequisites

- Python 3.10 or newer.
- [uv](https://docs.astral.sh/uv/getting-started/installation/).
- [CUE v0.17.1](https://cuelang.org/docs/introduction/installation/).

If GNU Make is available, bootstrap and run all checks with:

```shell
make setup
make check BASE=origin/main
```

The Makefile is optional. If GNU Make is unavailable, use the direct commands:

```shell
uv sync
uv run python scripts/validate_catalog.py
```

To enforce component version changes against a target branch:

```shell
uv run python scripts/validate_catalog.py --base origin/main
```

Ruff checks repository tooling. Versioned payload scripts remain on their
component-specific validation so repository-tooling changes do not silently
rewrite component payloads.

Run the complete test suite with:

```shell
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
```

## Add a component

1. Add the native payload without marketplace-specific fields:

   - A skill goes in `skills/<component-id>/`.
   - An agent, instruction, or prompt normally uses one file in its matching
     payload directory.
   - A hook component includes its hook configuration and any scripts it owns.

2. Add `catalog/components/<type-plural>/<component-id>.yaml`.

   - Use a stable lowercase kebab-case `id`.
   - Match the directory to `type`: `agents`, `hooks`, `instructions`,
     `prompts`, or `skills`.
   - Set `type`, display metadata, compatibility, and tags.
   - Use `source.path` for one directory.
   - Use `source.paths` for one or more files.
   - Use only repository-relative source paths.
   - Each source is installed at the same relative path under Copilot home.
   - Declare component dependencies by ID and optional version constraint.
   - Declare non-installable prerequisites such as MCP servers under
     `external_dependencies`.
   - Start at `1.0.0` unless reliable release history supports another version.
   - Explain the current version in `release.summary`.

3. Add the component to a profile only when that profile should explicitly
   enable or disable it.

4. Increment `catalog_version` in `catalog/catalog.yaml`.

5. Run the validation and tests shown above.

Every payload file must have exactly one component owner. Do not create a
manifest for a file that is not independently selectable.

### External dependencies

Use component `dependencies` only for other catalog components that Flightplan
can enable. Use `external_dependencies` for capabilities that must already be
configured outside the marketplace:

```yaml
external_dependencies:
  - type: mcp
    id: intellij
    name: IntelliJ MCP
    description: Provides the IDE search operations required by this skill.
    required: true
```

An optional `version` constraint uses the same syntax as component dependency
constraints. Do not put MCP URLs, credentials, or secrets in a manifest.

Profiles do not repeat these entries; external dependencies are inherited from
the components selected by a profile.

### Walkthrough: add a skill

This example adds a directory-based skill named `api-review`.

1. Create `skills/api-review/SKILL.md`:

   ```markdown
   ---
   name: api-review
   description: Reviews API changes for compatibility. Use when changing an API contract.
   ---

   # API review

   Review compatibility, migration behavior, and consumer impact.
   ```

2. Add any skill-owned scripts or references inside `skills/api-review/`.

3. Create `catalog/components/skills/api-review.yaml`:

   ```yaml
   schema_version: 1

   id: api-review
   type: skill
   name: API Review
   version: 1.0.0
   description: Reviews API changes for compatibility and migration impact.

   source:
     path: skills/api-review

   default_state: available

   compatibility:
     operating_systems: [linux, macos]
     copilot_surfaces: [cli, intellij, vscode]

   dependencies: []
   external_dependencies: []
   tags: [api, compatibility]

   release:
     summary: Initial release of the API review skill.
   ```

4. Optionally add `api-review` to a profile.

5. Increment `catalog_version` in `catalog/catalog.yaml`.

6. Run:

   ```shell
   make check BASE=origin/main
   ```

   Without Make, run the validation, version comparison, tests, and Ruff
   commands from the earlier section.

### Walkthrough: add an instruction

This example adds one file-based instruction named `java-style`.

1. Create `instructions/java-style.instructions.md`. Personal instruction
   payloads use the `*.instructions.md` suffix.

2. Create `catalog/components/instructions/java-style.yaml`:

   ```yaml
   schema_version: 1

   id: java-style
   type: instruction
   name: Java Style
   version: 1.0.0
   description: Applies the organization's Java conventions.

   source:
     paths:
       - instructions/java-style.instructions.md

   default_state: available

   compatibility:
     operating_systems: [linux, macos]
     copilot_surfaces: [cli, intellij, vscode]

   dependencies: []
   external_dependencies: []
   tags: [java, style]

   release:
     summary: Initial release of the Java style instruction.
   ```

3. Optionally add `java-style` to a profile.

4. Increment `catalog_version` in `catalog/catalog.yaml`.

5. Run `make check BASE=origin/main`, or its direct-command equivalent.

## Change a component

When a declared payload or its source declaration changes:

1. Increment the component version.
2. Update `release.summary`.
3. Update dependencies or profile entries when behavior requires it.
4. Increment `catalog_version` for the catalog release.
5. Validate against the target branch:

   ```shell
   uv run python scripts/validate_catalog.py --base origin/main
   ```

Use a patch version for a clarification with no intended behavior change, a
minor version for a compatible behavior or guidance change, and a major version
for an incompatible activation, configuration, rename, or removal.

For an intentional component replacement, keep the new ID stable and declare
the old ID under `replaces`.

## Change the catalog schema

Edit only `catalog/schema/catalog.cue`, then regenerate the committed JSON
Schemas:

```shell
uv run python scripts/generate_schemas.py
uv run python scripts/generate_schemas.py --check
```

The generator requires exactly CUE v0.17.1 because JSON Schema output is pinned
for a stable cross-repository contract. Commit the CUE source and all changed
generated schemas together.

Keep the CUE source, generated schemas, validator, tests, and this contributor
guide consistent whenever the YAML wire format changes.

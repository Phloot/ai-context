# AI Context Catalog Specification

## 1. Purpose

Add a versioned component catalog to the existing `ai-context` repository.

The catalog must describe each selectable context component without changing the native Copilot payload format.

This specification applies only to the `ai-context` repository.

## 2. Current state

The repository currently resembles a local Copilot home directory:

```text
ai-context/
├── agents/
├── hooks/
├── instructions/
├── prompts/
└── skills/
```

Keep these payload directories.

Do not move marketplace metadata into the payload directories.

Do not add marketplace metadata to `.github/`.

Do not add nonstandard version fields to `SKILL.md` frontmatter.

## 3. Required repository structure

Add this metadata structure:

```text
ai-context/
├── cue.mod/
│   └── module.cue
├── catalog/
│   ├── catalog.yaml
│   ├── components/
│   │   ├── agents/
│   │   ├── hooks/
│   │   ├── instructions/
│   │   ├── prompts/
│   │   └── skills/
│   ├── profiles/
│   │   └── <profile-id>.yaml
│   └── schema/
│       ├── catalog.cue
│       ├── catalog.schema.json
│       ├── component.schema.json
│       └── profile.schema.json
├── agents/
├── hooks/
├── instructions/
├── prompts/
└── skills/
```

The `catalog/` directory is metadata for Flightplan and repository validation.

Flightplan must not copy the `catalog/` directory into the Copilot home directory.

## 4. Supported component types

Support these component types:

- `skill`
- `agent`
- `instruction`
- `prompt`
- `hook`

Use one manifest for each independently selectable component.

Use one stable lowercase kebab-case ID for each component.

Component IDs must be globally unique across all component type directories.

Do not use the display name or payload filename as the persistent identity.

## 5. Catalog manifest

Create `catalog/catalog.yaml`.

Use this structure:

```yaml
schema_version: 1
catalog_version: 2026.07.1
```

Use calendar versioning for `catalog_version`.

Increment `catalog_version` when a catalog release changes available components, profiles, or catalog behavior.

Do not use `catalog_version` as a component version.

## 6. Component manifest

Each file under a type directory in `catalog/components/` must describe one
component. The directory must agree with the manifest's `type`.

Use this structure:

```yaml
schema_version: 1

id: <component-id>
type: <skill|agent|instruction|prompt|hook>
name: <display-name>
version: 1.0.0
description: >
  <Concise component description.>

source:
  path: <repository-relative-source-path>

default_state: available

compatibility:
  operating_systems:
    - linux
    - macos
  copilot_surfaces:
    - cli
    - intellij

dependencies: []
external_dependencies: []

tags:
  - <search-tag>

release:
  summary: <Current-version change summary.>
```

The schema must require:

- `schema_version`
- `id`
- `type`
- `name`
- `version`
- `description`
- `source`
- `default_state`
- `compatibility`
- `dependencies`
- `external_dependencies`
- `release.summary`

## 7. Source paths and projection

Support one directory source:

```yaml
source:
  path: skills/<skill-directory>
```

Support multiple file sources:

```yaml
source:
  paths:
    - hooks/<hook-file>.json
    - hooks/scripts/<hook-script>.py
```

Apply these rules:

- Use repository-relative source paths.
- Install each source at the identical path relative to the Copilot home
  directory.
- Reject absolute paths.
- Reject paths that contain `..`.
- Reject a source symlink that resolves outside the repository.
- Reject payload ownership by more than one component.

## 8. Dependencies

### 8.1 Component dependencies

Use component IDs for dependencies that Flightplan can enable from this
catalog:

```yaml
dependencies:
  - id: <required-component-id>
    version: ">=1.0.0,<2.0.0"
```

The `version` field is optional.

Use a standard version constraint syntax that Flightplan can evaluate.

Validation must reject:

- A missing dependency.
- A self-dependency.
- A dependency cycle.
- An invalid version constraint.
- A constraint that the current catalog cannot satisfy.

Use dependencies for all component types.

Do not add type-specific dependency behavior to the catalog.

### 8.2 External dependencies

Declare required capabilities that are not installable catalog components
separately:

```yaml
external_dependencies:
  - type: mcp
    id: intellij
    name: IntelliJ MCP
    description: >
      Provides the IDE search operations required by this skill.
    required: true
    version: ">=1.0.0"
```

The initial external dependency type is `mcp`.

The `version` field is optional. When present, use the same constraint syntax
as component dependencies.

Validation must reject:

- An unsupported external dependency type.
- A duplicate `type` and `id` pair in one component.
- An invalid external dependency ID.
- An invalid version constraint.

External dependencies describe prerequisites; they do not contain connection
URLs, credentials, or secrets.

Profiles must not repeat external dependencies. A profile inherits them from
the components it lists.

Flightplan must not attempt to install or configure an MCP server from this
metadata.

## 9. Compatibility

The manifest must declare supported operating systems and Copilot surfaces.

Use controlled values in the schema.

Initial operating-system values:

- `linux`
- `macos`

Initial Copilot surface values:

- `cli`
- `intellij`
- `vscode`

Compatibility metadata describes availability. It does not enforce organization policy.

## 10. Default state

Support these values:

- `available`
- `enabled`

Use `available` by default.

Use `enabled` only for a component that the organization wants active after the first managed installation.

Flightplan must not automatically enable a new component during a normal catalog update.

The default state applies only when Flightplan creates initial marketplace state.

## 11. Profiles

Store profiles in `catalog/profiles/`.

Use this structure:

```yaml
schema_version: 1

id: <profile-id>
name: <display-name>
version: 1.0.0
description: >
  <Concise profile description.>

mode: merge

components:
  - id: <component-id>
    enabled: true
  - id: <component-id>
    enabled: false
```

Use `merge` as the only supported mode in the first schema version.

A profile must not change components that it does not list.

Validation must reject:

- A duplicate profile ID.
- An invalid profile version.
- An unsupported mode.
- A missing component ID.
- A duplicate component entry.

## 12. Versioning

Use Semantic Versioning for each component.

Apply these rules:

| Change | Required version change |
| --- | --- |
| Typo or clarification with no intended behavior change | Patch |
| Compatible guidance, reference, script, file, or behavior change | Minor |
| Incompatible configuration, activation, rename, or removal | Major |

Treat an intended AI behavior change as a minor change.

Version the complete component payload as one unit.

Do not version files inside a component independently.

Keep component version history in Git.

Use `release.summary` to describe the current version.

## 13. Component replacement

Component IDs must remain stable.

When a component replaces another component, declare the relationship:

```yaml
replaces:
  - id: <old-component-id>
    version: "<2.0.0"
```

Use `replaces` only for an intentional migration.

Do not reuse a retired component ID for a different purpose.

## 14. CUE and JSON Schemas

Use `catalog/schema/catalog.cue` as the authoritative schema definition.

Generate and commit JSON Schemas for:

- `catalog/catalog.yaml`
- Component manifests.
- Profile manifests.

Set `additionalProperties` to `false` where forward compatibility does not require unknown fields.

Define reusable schema definitions for:

- Semantic Version strings.
- Component IDs.
- Relative paths.
- Compatibility values.
- Dependency objects.
- External dependency objects.
- Directory and file source declarations.

Keep the schema version independent from the catalog version.

Pin the CUE language and CLI version used for generation.

The generated JSON Schemas are the portable schema contract for Flightplan and
other consumers that do not use CUE. Do not require those consumers to install
or execute CUE.

Validation must fail when a committed JSON Schema differs from the output
generated from `catalog/schema/catalog.cue`.

## 15. Validation command

Provide one repository validation command.

Use CUE for structural schema authoring and YAML validation.

Use the repository validation command for cross-file, filesystem, dependency,
and Git version-change checks that are outside a single manifest schema.

The command must:

1. Load `catalog/catalog.yaml`.
2. Load all component manifests.
3. Load all profile manifests.
4. Validate the YAML files against the authoritative CUE definitions.
5. Verify that committed JSON Schemas match the CUE-generated output.
6. Validate each file against its generated JSON Schema.
7. Validate source paths.
8. Validate component IDs and type-directory placement.
9. Validate dependency constraints.
10. Detect dependency cycles.
11. Detect payload and destination ownership collisions.
12. Validate profiles.
13. Return a nonzero exit code for any error.

Each error must include:

- Manifest path.
- Field or path when applicable.
- Concise corrective action.

The command must produce deterministic output.

## 16. Version-change validation

Add a validation mode that compares the current branch with a base revision.

The validation must fail when:

- A payload changes without a component version change.
- A component version decreases.
- A source declaration changes without a version change.
- Component dependency, external dependency, compatibility, default-state, or
  replacement metadata changes without a version change.
- A component ID changes without a declared replacement.
- A changed payload has no component owner.

The validation must inspect each component's declared source paths.

The validation must ignore unrelated component changes.

The validation must fail when two components claim the same payload file.

## 17. Continuous integration

Add the catalog checks to the existing continuous integration workflow.

Run:

- CUE schema validation.
- Generated JSON Schema drift validation.
- JSON Schema validation.
- Semantic validation.
- Dependency validation.
- Payload ownership validation.
- Version-change validation.
- Existing component-specific validation.

Do not add a second continuous integration system.

Do not require Flightplan to validate pull requests in `ai-context`.

## 18. Initial catalog migration

Create manifests for all existing selectable payloads.

Apply these rules:

- Treat each skill directory as one component.
- Treat each agent file as one component unless an agent owns adjacent required files.
- Treat each instruction file as one component.
- Treat each prompt file as one component.
- Treat each independently controlled hook set as one component.
- Include a hook script in its owning hook component.
- Declare dependencies when one component requires another component.

Do not change payload content only to complete the catalog migration.

Set the initial version from existing release information when reliable information exists.

Use `1.0.0` when no reliable component version exists.

## 19. Tests

Test:

- A valid catalog.
- Invalid CUE schema.
- Generated JSON Schema drift.
- Invalid YAML.
- Schema violations.
- Duplicate IDs.
- Invalid component IDs.
- Invalid versions.
- Missing source paths.
- Absolute paths.
- Path traversal.
- Unsafe symlinks.
- Payload ownership collisions.
- Missing dependencies.
- Dependency cycles.
- Unsatisfied constraints.
- Invalid profiles.
- Payload changes without version changes.
- Version decreases.
- Valid component updates.

Use temporary repository fixtures.

Do not depend on a developer's `~/.copilot` directory.

## 20. Acceptance criteria

The work is complete when:

- `catalog/catalog.yaml` exists.
- `catalog/schema/catalog.cue` is the authoritative schema.
- Generated JSON Schemas match the pinned CUE output.
- All selectable components have manifests.
- All profiles have manifests.
- All manifests pass their JSON Schemas.
- Component IDs are unique and stable.
- Component versions use Semantic Versioning.
- Source paths exist.
- Target paths are safe.
- Dependencies are valid.
- Dependency cycles do not exist.
- Target collisions do not exist.
- Payload ownership collisions do not exist.
- The validation command returns a nonzero exit code for invalid catalogs.
- Continuous integration runs catalog validation.
- Continuous integration rejects unversioned payload changes.
- Native Copilot payload files remain valid.
- Marketplace metadata remains outside `.github/`.
- `SKILL.md` frontmatter remains standards-compatible.

## 21. Agent execution instructions

Inspect the repository before selecting script locations or test frameworks.

Use the provided template manifests as reference inputs.

Adapt the templates to the actual payload structure.

Do not create manifests for files that are not independently selectable.

Do not change payload behavior unless the task requires that change.

Run focused tests after each implementation slice.

Run the complete catalog validation before completion.

Report:

- Catalog files added.
- Component manifests added.
- Profiles added.
- CUE schema and generated JSON Schemas added.
- Validation commands added.
- Continuous integration changes.
- Tests run.
- Unresolved catalog decisions.

# Context Marketplace Delivery Roadmap

## 1. Purpose

This roadmap divides the Context Marketplace into three implementation stages.

Each stage has one primary repository and one stable output contract.

## 2. Specifications

Implement the specifications in this order:

1. `01-ai-context-catalog-spec.md`
2. `02-flightlog-marketplace-backend-spec.md`
3. `03-flightlog-marketplace-ui-spec.md`

## 3. Ownership

| Area | Repository | Responsibility |
| --- | --- | --- |
| Component payloads | `ai-context` | Store skills, agents, instructions, prompts, hooks, and related files. |
| Catalog metadata | `ai-context` | Describe components, versions, component and external dependencies, compatibility, and profiles. |
| Catalog validation | `ai-context` | Reject invalid metadata and unversioned payload changes. |
| Repository installation | Flightplan | Install and update the local `ai-context` checkout. |
| Marketplace state | Flightplan | Store each developer's enabled components and applied versions. |
| File projection | Flightplan | Copy enabled payloads into the active Copilot home directory. |
| File safety | Flightplan | Preserve unmanaged files and locally modified managed files. |
| Marketplace API | Flightplan | Expose catalog, state, mutation, synchronization, and activity operations. |
| Marketplace user interface | Flightplan | Let developers search, inspect, enable, disable, and update components. |

## 4. Delivery stages

### Stage 1: Catalog foundation

Implement the `ai-context` catalog and validation.

Complete this stage before Flightplan depends on the catalog format.

The stage output must include:

- A versioned catalog format.
- One manifest for each selectable component.
- An authoritative CUE schema.
- Generated JSON Schemas for non-CUE consumers.
- Dependency and collision validation.
- Component version-change validation.
- Continuous integration checks.

### Stage 2: Marketplace backend

Implement the Flightplan marketplace services and API.

The backend must:

- Read the validated catalog.
- Store local component state.
- Resolve dependencies.
- Report external dependency availability without installing external tools.
- Project enabled payloads into `~/.copilot`.
- Detect conflicts.
- Preserve unmanaged and modified files.
- Expose stable API responses.

The backend API is the input contract for the user interface.

### Stage 3: Marketplace user interface

Implement the Flightplan marketplace page after the backend contract is stable.

The user interface must:

- Display all catalog components.
- Display enabled, disabled, update, and conflict states.
- Support search and component-type filters.
- Support enable, disable, update, profile, and synchronization operations.
- Explain dependency actions and file conflicts.

## 5. Shared terms

Use these terms in all three specifications:

| Term | Definition |
| --- | --- |
| Catalog | The validated component metadata from the `ai-context` repository. |
| Component | One selectable skill, agent, instruction, prompt, hook, or supported context item. |
| Payload | The source files that implement a component. |
| Available | The component exists in the current catalog. |
| Enabled | Flightplan projected the component into the active Copilot home directory. |
| Disabled | The component is available but is not projected into the Copilot home directory. |
| Managed file | Flightplan copied the file and recorded its installed hash. |
| Unmanaged file | Marketplace state does not claim ownership of the file. |
| Local modification | A managed file differs from its recorded installed hash. |
| Applied version | The component version currently projected into the Copilot home directory. |
| Available version | The component version in the current catalog. |
| Profile | A versioned set of recommended component states. |

## 6. Cross-repository contract

The `ai-context` repository must provide:

- `catalog/catalog.yaml`
- `catalog/components/{agents,hooks,instructions,prompts,skills}/*.yaml`
- `catalog/profiles/*.yaml`
- `catalog/schema/catalog.cue`
- `catalog/schema/*.json`
- Valid payload paths
- Stable component IDs
- Semantic component versions

Flightplan must not infer missing component metadata from payload filenames.

Flightplan must reject an unsupported catalog schema.

Flightplan must preserve the previous working catalog when a new catalog is invalid.

CUE is an `ai-context` authoring and continuous-integration dependency.
Flightplan must consume the YAML manifests and generated JSON Schemas without
requiring the CUE CLI.

## 7. Release gates

### Catalog gate

Do not start marketplace synchronization work until:

- All existing selectable components have manifests.
- Catalog validation passes.
- Target collisions are resolved.
- Component IDs are stable.

### Backend gate

Do not connect the user interface to mutation operations until:

- Enable and disable operations are safe.
- Local modification detection works.
- API error codes are stable.
- Temporary-directory integration tests pass.

### User-interface gate

Do not release the marketplace page until:

- The page handles loading, empty, error, update, and conflict states.
- The page waits for backend confirmation before it changes enabled state.
- Accessibility checks pass.

## 8. Out of scope

Do not include these features in the first release:

- A public marketplace.
- Third-party component uploads.
- Organization policy enforcement.
- Automatic conflict merging.
- Force overwrite.
- Automatic cascade disable.
- Component ratings or reviews.
- Cloud synchronization of developer selections.
- Per-file versions inside a component.

## 9. Completion criteria

The complete marketplace is ready when:

- The `ai-context` catalog is valid and versioned.
- Flightplan can load the catalog.
- Flightplan can enable and disable each supported component type.
- Flightplan can detect component updates.
- Flightplan preserves unmanaged files.
- Flightplan preserves locally modified managed files.
- Flightplan reports conflicts.
- The user interface exposes all supported operations.
- Automated tests pass in both repositories.

# SL-06: Draft and review coherent slices

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-06` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-05` |
| Acceptance criteria | `AC-013`, `AC-014`, `AC-021`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029`, `AC-030` |

## Outcome

The planner develops each approved outline entry into one detailed, repository-grounded implementation slice.

The user reviews slices individually in dependency order.

## Requires

- Approved outline version from `SL-05`.
- Stable slice identifiers and dependencies.
- Requirement and design decisions.
- Repository evidence ledger.
- Acceptance-criteria coverage map.
- The Slice review presentation rules in the frontend design contract.

## Produces

- Versioned detailed slice artifacts.
- File-level work units supported by repository evidence.
- Slice validation requirements.
- Individual slice approval records.
- Complete requires and produces contracts.

## Repository discovery

Before implementation, find:

- Current plan content storage.
- Current Markdown generation or template behavior.
- Existing plan review and refinement behavior.
- Existing artifact versioning.
- Existing frontend document rendering.
- Tests for plan content and review actions.

Do not make the LLM's Markdown response the only representation of slice state. Keep enough structure to validate identities, dependencies, criteria, and approvals.

## Work units

### Detailed slice model

**Repository path:** Resolve from the plan artifact owner.

Each slice must contain these sections:

- Identity
- Outcome
- Requires
- Produces
- File work units
- Tests and validation
- Risks and recovery
- Non-goals

Each file work unit must contain:

- Exact primary path
- Action: `create`, `modify`, or `delete`
- Relevant symbols
- Current responsibility or behavior
- Required responsibility or behavior
- Important implementation details
- Contracts or data flow
- Dependencies on other work units

Mark each new path as new. Require repository evidence for each existing path and symbol.

### Slice generation sequence

**Repository path:** Keep sequencing rules in the planning domain.

Generate one slice at a time in dependency order.

Before generation, supply the planner with:

- Approved outline entry
- Required earlier-slice contracts
- Applicable decisions
- Applicable acceptance criteria
- Applicable repository evidence
- Current planning budget

Stop after one slice draft. Do not generate the next slice until the user accepts the current slice or explicitly postpones it.

### Slice commands and versions

**Repository path:** Resolve from the planning application owner.

Support:

- Generate slice draft
- Revise slice
- Accept slice
- Reject slice
- Split slice and return to outline review
- Merge adjacent slice and return to outline review
- Return to a prior decision
- Compare slice versions

Preserve stable slice IDs when the outcome does not change.

Store approval against a specific slice version. A later slice revision invalidates only that approval and dependent approvals.

### Planner tools

**Repository path:** Extend the planner-tool owner.

Add typed operations equivalent to:

- Submit slice draft
- Submit slice revision
- Report slice blocker

Reject a slice that:

- Does not match an approved outline entry.
- Contains more than one independent outcome.
- Omits required acceptance criteria.
- References an unapproved dependency.
- Uses an existing path or symbol without evidence.
- Omits focused validation.
- Omits explicit non-goals.

### Slice-review workbench

**Repository path:** Resolve from the center workspace owner.

Display one slice with:

- Identity and version
- Approval status
- Dependencies
- Acceptance criteria
- Outcome
- Requires and Produces
- File work units
- Tests and validation
- Risks and recovery
- Non-goals
- Evidence links

Provide actions for accept, revise, split, merge, and return to decision.

Show the ordered slice list in the phase rail. Distinguish pending, drafting, review, accepted, and stale states.

Keep user feedback attached to the applicable slice and version. Also include the feedback in the planner conversation context.

Render the slice as a technical document. Do not wrap each section in a separate card. Use a table for file work units and compact labels for version, review state, criteria, and evidence.

Keep `Accept slice` as the primary action. Keep revision and return actions secondary.

### Cross-slice consistency

**Repository path:** Keep this policy in the planning domain.

Validate:

- Each dependency is approved or in an allowed prerequisite state.
- Each `requires` item has an earlier source.
- Each promised `produces` item has a later consumer or current outcome.
- Two slices do not own the same behavior.
- A later slice does not redefine an earlier contract without returning to review.

Do not require a separate scaffolding slice when the scaffolding has no independent verification value.

## State and failure behavior

- Preserve the last accepted slice version when a revision is rejected.
- Mark a slice stale when an applicable decision, outline entry, or evidence item changes.
- Mark dependent slices stale when a required contract changes.
- Preserve unaffected accepted slices.
- Stop generation when the budget cannot support an evidence-based slice.
- Do not treat a chat statement as slice approval.

## Tests and validation

Add or change focused tests for:

- Slice generation order.
- One-slice-at-a-time enforcement.
- Required section validation.
- Existing-path evidence validation.
- New-path marking.
- Criterion mapping.
- Requires and Produces validation.
- Slice approval by version.
- Revision invalidation.
- Dependency invalidation.
- Unaffected slice preservation.
- Split and merge return to outline review.
- Slice workbench loading, review, stale, and conflict states.
- Technical-document hierarchy and file-work-unit table accessibility.
- Slice-review conformance to the frontend design contract.

Slice completion evidence:

- The user can generate and approve a one-slice plan.
- The user can review a multi-slice plan in dependency order.
- Changing an earlier contract invalidates only affected slices.
- Each existing file and symbol has repository evidence.
- The user approves the Outline and Slice review visual checkpoint.

## Risks and recovery

- Detailed Markdown can diverge from structured state. Generate Markdown from validated plan data or validate parsed results before storage.
- Slice regeneration can overwrite accepted content. Create a new version and preserve the accepted version.
- Excessive per-file instructions can become line-by-line implementation. Require behavior and contracts, not code transcription.

## Non-goals

- Do not validate the complete plan set.
- Do not grant final plan approval.
- Do not write approved plan files.
- Do not attach content to Agility.
- Do not implement the selected repository changes.

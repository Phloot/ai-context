# SL-05: Create and review the plan outline

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-05` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-04` |
| Acceptance criteria | `AC-011`, `AC-012`, `AC-014`, `AC-021`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029` |

## Outcome

The planner creates an index-level plan outline before it creates detailed slices.

The user can revise and approve the slice structure.

## Requires

- Completed design review from `SL-04`.
- Confirmed requirement and technical decisions.
- Repository evidence ledger.
- Stable acceptance-criteria identifiers.
- No unresolved blocking decision.
- The Outline presentation rules in the frontend design contract.

## Produces

- A versioned plan outline.
- Stable slice identifiers.
- Ordered slice dependencies.
- Cross-slice contracts.
- Acceptance-criteria coverage.
- Explicit outline approval.

## Repository discovery

Before implementation, find:

- Current plan artifact representation.
- Current plan-generation and refinement behavior.
- Existing version or revision models.
- Existing ordering and validation utilities.
- Existing frontend list reordering behavior.
- Current plan preview and review modal behavior.
- Tests for plan generation and update.

Reuse existing plan representations only when they can support an ordered plan set without conflicting semantics.

## Work units

### Plan-outline model

**Repository path:** Resolve from the current plan domain and artifact owner.

Represent:

- Plan-set ID
- Outline version
- Status
- Goal
- Non-goals
- Confirmed assumptions and constraints
- Decision references
- Ordered slice summaries
- Slice dependencies
- Cross-slice contracts
- Acceptance-criteria coverage
- Validation findings

Each slice summary must have:

- Stable slice ID
- Title
- One primary outcome
- Dependency IDs
- Acceptance-criteria IDs
- Status

Do not put detailed file work units in the outline.

### Coherent-slice rules

**Repository path:** Keep these rules in the planning domain and runtime planner instructions.

A slice must contain one observable behavior or one independently verifiable checkpoint.

Split a slice when it:

- Contains more than one independently useful outcome.
- Mixes unrelated responsibilities.
- Has a separate failure or recovery boundary.
- Cannot be reviewed or verified as one change.
- Contains an unresolved decision that does not block other work.

Merge adjacent slices when one slice only creates scaffolding for the next slice. Also merge slices when separate validation has no useful meaning.

Do not divide slices by backend, frontend, database, or test file type when one behavior requires those files together.

### Outline commands

**Repository path:** Resolve from the planning application owner.

Support:

- Create outline draft
- Revise slice summary
- Split slice
- Merge adjacent slices
- Reorder slice
- Change dependency
- Add or remove criterion mapping
- Submit outline approval
- Return to an earlier decision

Each mutation creates a new outline version or a repository-consistent revision record.

Validate dependency changes. Reject cycles, missing dependencies, and invalid order.

### Planner tools

**Repository path:** Extend the planner-tool owner.

Add typed operations equivalent to:

- Submit plan outline
- Submit an outline revision
- Report outline blocker

The planner supplies proposals. The application performs split, merge, order, mapping, version, and approval mutations.

Reject an outline that:

- Omits a confirmed criterion.
- References an unknown decision or evidence item.
- Contains duplicate slice IDs.
- Contains a dependency cycle.
- Contains a slice without one primary outcome.

### Outline workbench

**Repository path:** Resolve from the center workspace owner.

Display:

- Goal and non-goals
- Decision summary
- Ordered slice table
- Dependency information
- Acceptance-criteria coverage
- Cross-slice contracts
- Validation findings
- Outline version

Support explicit actions for revise, split, merge, reorder, and approve.

Use direct manipulation only when accessible keyboard and button alternatives exist. Do not depend only on drag-and-drop.

Keep one primary action visible. Disable approval when validation has a blocking finding.

Use one ordered technical table rather than a slice-card gallery. Show goal and non-goals above the table. Show coverage, dependency-cycle state, and cross-slice contracts below it.

Keep `Approve outline` at the right edge of the workbench action row. Keep reorder, split, merge, regenerate, and revision actions secondary.

### Targeted invalidation

**Repository path:** Keep invalidation policy in the planning domain.

When the outline changes:

- Invalidate the outline approval.
- Invalidate only affected slice drafts and approvals.
- Invalidate downstream slices when their requirements or dependencies changed.
- Preserve unaffected accepted slice versions.
- Record the reason for invalidation.

Returning to a requirement or design decision uses the same dependency-aware invalidation behavior.

## State and failure behavior

- Preserve the last valid outline when a proposed revision fails validation.
- Reject a reorder that violates dependencies.
- Reject a merge that creates more than one independent outcome.
- Require stable IDs for unchanged slice behavior.
- Show stale slice drafts after an outline change.
- Do not generate detailed slices until the current outline version has approval.

## Tests and validation

Add or change focused tests for:

- Outline creation from confirmed inputs.
- Missing criterion coverage.
- Duplicate slice IDs.
- Dependency cycle rejection.
- Split behavior.
- Merge behavior.
- Valid and invalid reordering.
- Criterion mapping changes.
- Outline approval lock.
- Targeted downstream invalidation.
- Preservation of unaffected accepted slices.
- Outline workbench loading, editing, conflict, and approval states.
- Keyboard reorder behavior and accessible dependency errors.
- Outline conformance to the frontend design contract.

Slice completion evidence:

- The user can approve an ordered one-slice outline.
- The user can revise and approve a multi-slice outline.
- Invalid dependency changes do not replace the last valid version.
- Detailed slice generation stays unavailable before outline approval.

## Risks and recovery

- Complex editing can move domain rules into JavaScript. Validate every mutation through the backend planning owner.
- Regenerating the outline can destroy user edits. Create a new version and show the proposed difference.
- Excessive plan versions can accumulate. Define retention separately without deleting approved history.

## Non-goals

- Do not generate detailed file work units.
- Do not approve an individual detailed slice.
- Do not write files to the plans directory.
- Do not attach content to Agility.
- Do not implement a generic graph editor.

# SL-07: Validate and approve the plan set

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-07` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-06` |
| Acceptance criteria | `AC-008`, `AC-009`, `AC-012`, `AC-013`, `AC-014`, `AC-015`, `AC-021`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029` |

## Outcome

Flightlog validates the complete plan set and creates one immutable approved plan version.

Final approval stays unavailable until all blocking findings are resolved.

## Requires

- Approved outline version from `SL-05`.
- Required accepted slice versions from `SL-06`.
- Resolved blocking and high-impact decisions.
- Repository evidence ledger.
- Current repository snapshot.
- The Validate and publish presentation rules in the frontend design contract.

## Produces

- Deterministic validation findings.
- A complete acceptance-criteria coverage result.
- A final approval record.
- An immutable approved plan version.
- Publication-ready artifact references.

## Repository discovery

Before implementation, find:

- Current plan validation behavior.
- Existing approval or status-transition patterns.
- Existing transaction and concurrency conventions.
- Existing plan file rendering.
- Existing frontend validation and confirmation patterns.
- Tests for plan status and persistence.

Keep deterministic validation outside the planner prompt. The planner can explain a finding but cannot waive it directly.

## Work units

### Plan-set validator

**Repository path:** Resolve from the planning domain or add one focused collaborator for this distinct responsibility.

Validate these conditions:

- Each confirmed criterion maps to implementation work.
- Each confirmed criterion maps to validation.
- The index coverage table matches detailed slices.
- Each existing path and symbol has repository evidence.
- Each new path is marked new.
- Each slice has one coherent outcome.
- Each slice states its `requires` and `produces` contracts.
- Each dependency exists and has a valid order.
- No slice duplicates another slice's responsibility.
- Tests cover changed observable behavior and material failure cases.
- The design preserves repository dependency direction.
- The design reuses existing behavior when practical.
- The design does not add speculative abstractions.
- The approved outline matches the detailed slices.
- No unresolved blocking or high-impact decision remains.
- Each required slice version has approval.
- The repository snapshot is not stale.

Return stable finding codes, severity, artifact references, and corrective phase.

### Approval policy

**Repository path:** Keep approval rules in the planning domain.

Final approval requires:

- A successful current validation result.
- Approval for the current outline version.
- Approval for each required current slice version.
- No unresolved blocking or high-impact decision.
- No active planner turn.
- A current repository snapshot or an explicit approved revalidation result.

The user must submit an explicit approval action. A planner message cannot approve the plan.

Create an immutable plan version from the exact approved artifact versions.

### Concurrency and transaction behavior

**Repository path:** Resolve from SQLite transaction and command patterns.

Make validation and approval safe against concurrent changes.

If an artifact changes after validation, reject approval and require validation again.

Use a version, revision, or optimistic concurrency field. Do not rely only on timestamps.

### Planner support

**Repository path:** Extend the planner-tool owner only when needed.

The planner can:

- Explain validation findings.
- Propose a correction.
- Return to the required phase.
- Submit a revised artifact through existing structured tools.

The planner cannot:

- Change finding severity.
- Mark a deterministic finding resolved.
- Grant approval.
- Publish the plan.

### Final-review workbench

**Repository path:** Resolve from the center workspace owner.

Display:

- Goal and scope
- Decision summary
- Ordered slices and approval states
- Acceptance-criteria coverage
- Validation findings
- Repository revision
- Plan version candidate
- Final approval control

Group findings by corrective phase. Provide a direct return action for the affected decision, outline, or slice.

Keep final approval disabled until the backend reports eligibility.

Show findings by corrective phase. Keep plan completeness and repository revision visible. Use the workbench for approval; do not allow chat to approve the plan.

## State and failure behavior

- Invalidate a validation result when a source artifact changes.
- Reject approval when the submitted version is stale.
- Preserve prior approved plan versions.
- Reject a final approval during an active planner turn.
- Preserve validation findings after a browser reload.
- Permit validation retry after repository revalidation.

## Tests and validation

Add or change focused tests for each deterministic validation rule.

Also test:

- Successful one-slice validation.
- Successful multi-slice validation.
- Missing implementation coverage.
- Missing test coverage.
- Evidence failure.
- Duplicate responsibility.
- Dependency-order failure.
- Unresolved decision.
- Stale repository snapshot.
- Stale approval submission.
- Concurrent artifact change.
- Immutable approved version creation.
- Final-review workbench locked and eligible states.
- Keyboard access, focus, and accessible finding status.
- Final-review conformance to the frontend design contract.

Avoid redundant tests for simple data containers. Test rules and state transitions at the closest useful boundary.

Slice completion evidence:

- Flightlog rejects every incomplete plan condition listed above.
- A valid simple plan can receive final approval.
- A valid multi-slice plan can receive final approval.
- An artifact change after validation prevents stale approval.

## Risks and recovery

- Validation logic can be duplicated in the UI. The backend result must remain authoritative.
- A large validator can collect unrelated rules. Group rules by plan invariant and keep one public validation operation.
- Approval and artifact mutation can race. Use transactional version checks.

## Non-goals

- Do not write plan files.
- Do not create the publication ZIP.
- Do not attach content to Agility.
- Do not delete old plan versions.
- Do not let the planner bypass validation.

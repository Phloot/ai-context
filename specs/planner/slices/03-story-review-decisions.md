# SL-03: Review the story and record decisions

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-03` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-02` |
| Acceptance criteria | `AC-007`, `AC-008`, `AC-021`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029` |

## Outcome

The planner reviews the story and acceptance criteria before repository investigation.

The user resolves material requirement questions through structured decision records.

## Requires

- Persistent planner conversation from `SL-02`.
- Verified story content from `SL-01`.
- Structured planner-tool foundation.
- Workflow-phase validation.
- The Story review presentation rules in the frontend design contract.

## Produces

- A reviewed planning brief.
- Stable acceptance-criteria identifiers.
- Classified concerns.
- Confirmed assumptions.
- Persistent decision records.
- A resolved requirement-review phase or an explicit blocker.
- A fast-path eligibility signal.

## Repository discovery

Before implementation, find:

- The current Agility story representation.
- Existing acceptance-criteria parsing or formatting.
- Current plan prompts and additional-comments handling.
- Existing decision, question, or review models.
- Current frontend form and modal patterns for AI questions.
- Tests for story content and AI-generated plan prompts.

Do not introduce a second story model if an existing boundary model can supply the required fields.

## Work units

### Acceptance-criteria identity

**Repository path:** Resolve from the story boundary and planning domain.

Preserve an existing criterion identifier when one exists.

When the story has unnumbered criteria, create stable plan-local identifiers. Do not change those identifiers during later revisions unless the criterion is deleted.

Store the source criterion text or a stable source reference. Do not add technical implementation details to the criterion.

### Requirement-review result

**Repository path:** Resolve from the planning artifact owner.

Represent:

- Confirmed requirements
- Assumptions
- Conflicts
- Unsupported requirements
- Untestable requirements
- Missing information
- Concern severity
- Review completion status

Use these severities:

- `blocking`
- `high-impact`
- `advisory`
- `informational`

Only a blocking concern prevents phase completion automatically. A high-impact concern requires an explicit decision or recorded exception.

### Decision record and transitions

**Repository path:** Resolve from the planning domain and SQLite owner.

A decision record must contain:

- Stable decision ID
- Source phase
- Question
- Severity
- Options when useful
- Planner recommendation when supported
- User answer
- Consequence or exception
- Status
- Created and resolved timestamps
- Affected artifact IDs and versions

The application owns decision state. The planner proposes the question and options through a structured tool.

Batch related questions. Limit one checkpoint to three blocking or high-impact questions.

### Planner tools

**Repository path:** Extend the planner-tool owner from `SL-02`.

Add typed operations equivalent to:

- Submit story review
- Request decisions
- Resolve or supersede a decision
- Mark requirement review complete

Validate criterion and decision identifiers. Reject a completion request with unresolved blocking decisions.

### Story-review workbench

**Repository path:** Resolve from the center workspace owner.

Display:

- Story summary
- Acceptance criteria
- Planner concerns by severity
- Structured decision questions
- Planner recommendation and consequences
- Confirmed assumptions
- Unresolved blocker count
- One primary next action

The user can answer an option or provide free-form input. The saved decision must show the final interpreted answer before the workflow advances.

The conversation rail can explain a concern. It must not become the only record of the answer.

Keep the phase rail and context header visible. Use structured workbench controls for each material question. Show the interpreted decision before the primary continuation action becomes available.

### Automatic fast path

**Repository path:** Keep this policy in the planning domain.

Mark the story eligible for a compressed path when:

- No blocking or high-impact requirement question remains.
- Acceptance criteria are present and testable enough for investigation.
- The user has not requested additional requirement review.

Fast-path eligibility does not bypass repository evidence, outline approval, slice approval, validation, or final approval.

## State and failure behavior

- Preserve a partially completed answer after a transient request failure.
- Reject an unknown decision option unless free-form input is allowed.
- Keep a superseded decision for history.
- Reopen the story-review phase when the source story changes materially.
- Mark downstream artifacts stale when a resolved requirement changes.
- Do not repeat a resolved disagreement unless new evidence invalidates it.

## Tests and validation

Add or change focused tests for:

- Existing criterion identifier preservation.
- Stable identifiers for unnumbered criteria.
- Concern severity validation.
- Maximum question batch size.
- Structured decision creation and resolution.
- Free-form decision input.
- Blocking-decision phase lock.
- High-impact exception recording.
- Source-story change invalidation.
- Fast-path eligibility.
- Story-review workbench loading, decision, error, and completed states.
- Required concern severities, structured decision controls, and primary-action placement.
- Keyboard operation and accessible decision status.

Slice completion evidence:

- The planner cannot begin investigation before story review completes.
- Each material answer exists as a durable decision record.
- Reloading the browser preserves unresolved and resolved decisions.
- A simple story advances without an empty decision ceremony.

## Risks and recovery

- The model can restate a criterion with changed meaning. Preserve the original criterion and separate the planner assessment.
- Free-form answers can be ambiguous. Require the planner to submit the interpreted decision before phase completion.
- Story edits can invalidate decisions. Compare the stored story reference or content version before resumption.

## Non-goals

- Do not inspect repository source.
- Do not create technical design decisions.
- Do not generate a plan outline.
- Do not generate detailed slices.
- Do not approve a plan.

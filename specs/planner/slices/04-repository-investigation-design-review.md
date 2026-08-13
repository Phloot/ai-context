# SL-04: Investigate the repository and review the design

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-04` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-03` |
| Acceptance criteria | `AC-003`, `AC-009`, `AC-010`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029`, `AC-030` |

## Outcome

The planner inspects the smallest relevant repository area and produces an evidence-based design review.

The planner does not modify the selected repository.

## Requires

- Completed story review from `SL-03`.
- Confirmed requirements, assumptions, and decisions.
- Repository snapshot from `SL-01`.
- Persistent planner session and read-only policy from `SL-02`.
- Planning budget.
- The Investigation and Design review presentation rules in the frontend design contract.

## Produces

- Repository evidence references.
- Existing-owner and dependency findings.
- A completed design review or explicit planning blocker.
- Confirmed technical decisions.
- A recorded repository revision and stale status.
- Sufficient evidence for outline generation.

## Repository discovery

This slice implements repository discovery for future plans. Before this slice is implemented, inspect Flightlog itself to find:

- Existing IntelliJ MCP or repository-search integration.
- Skill invocation behavior.
- Repository and branch resolution.
- Current command permissions.
- Existing token, request, and time budgets.
- Existing activity or progress events.
- Existing design-review or AI-review content.
- Tests for MCP tools and repository access.

The Flightlog implementation agent must use repository evidence for these exact owners.

## Work units

### Repository investigation policy

**Repository path:** Resolve from the planning domain and runtime planner resource.

Define the investigation contract:

- Search the smallest relevant repository area.
- Find behavior entry points.
- Find the owner of each affected decision.
- Find similar and reusable behavior.
- Find models, persistence, integrations, and public boundaries.
- Find focused tests and repository quality commands.
- Stop when evidence supports a design.

Require the configured repository-search skill when the planner contract requires it. Report a blocker when the required search capability is unavailable.

Do not allow a silent fallback to broad shell search when the planner contract prohibits that fallback.

### Evidence ledger

**Repository path:** Resolve from the planning artifact and persistence owners.

An evidence reference must contain:

- Stable evidence ID
- Repository snapshot ID
- Exact path
- Symbol when applicable
- Evidence type
- Concise finding
- Source tool or operation
- Created timestamp

Evidence types can include:

- Entry point
- Current owner
- Reusable behavior
- Dependency boundary
- Persistence
- External integration
- Test
- Quality command
- Repository instruction

Do not store complete source files or large search results in SQLite. Store concise references and findings.

### Planning budget

**Repository path:** Resolve from current usage and quota behavior.

Track a planning budget with the units that the current SDK and application can enforce reliably.

The planner must:

- Batch related searches.
- Reuse recorded evidence.
- Stop broad exploration when evidence supports the design.
- Report when the remaining budget cannot support an accurate plan.

The user can increase the budget and continue. A budget blocker must not discard evidence or decisions.

### Design-review artifact

**Repository path:** Resolve from the planning artifact owner.

Represent:

- Repository findings
- Recommended approach
- Important alternatives
- Confirmed assumptions
- Requirement conflicts
- Maintainability concerns
- Blocking decisions
- High-impact decisions
- Repository revision
- Evidence references

Each material technical claim must reference repository evidence.

### Planner tools and transitions

**Repository path:** Extend the planner-tool owner.

Add typed operations equivalent to:

- Record evidence
- Report investigation progress
- Submit design review
- Request technical decisions
- Raise an investigation or budget blocker
- Complete repository investigation

Reject:

- Evidence without a repository snapshot.
- Existing paths without a recorded exact path.
- Completion with unresolved blocking decisions.
- A design review that lacks evidence for material repository claims.

### Investigation and design-review workbench

**Repository path:** Resolve from the center workspace owner.

During investigation, display concise progress groups. Do not display every tool call.

Display:

- Current investigation objective
- Completed evidence categories
- Budget state
- Repository revision
- Stale-revision warning
- Blockers

After investigation, display the design review with:

- Recommendation
- Evidence-backed findings
- Alternatives and consequences
- Maintainability concerns
- Structured decisions
- One primary next action

The user can ask for more evidence through the conversation rail. The workflow advances only after required decisions are recorded.

Use a compact progress summary, structured investigation rows, and an evidence ledger table. Do not show a raw tool-call log.

For Design review, show the recommendation before findings, alternatives, consequences, and maintainability concerns. Use structured workbench decisions for blocking and high-impact choices.

## State and failure behavior

- Deny a source mutation and preserve the investigation state.
- Mark the repository snapshot stale when the selected revision changes.
- Let the user revalidate or restart affected investigation work.
- Preserve evidence after a budget blocker.
- Keep superseded evidence for plan history when a new investigation replaces it.
- Reject evidence that points outside the selected repository unless the plan explicitly includes another approved source.

## Tests and validation

Add or change focused tests for:

- Read-only repository permissions.
- Required search-capability blocker.
- Evidence-reference validation.
- Evidence deduplication or supersession.
- Budget consumption and blocker behavior.
- Budget increase and continuation.
- Design-review evidence requirements.
- Unresolved-decision phase lock.
- Repository revision staleness.
- Investigation progress and design-review UI states.
- Locked next-phase action with a visible reason.
- Evidence-table accessibility and technical-path readability.
- Investigation and Design review conformance to the frontend design contract.

Use a fake repository-search boundary. Do not require a live IntelliJ instance in focused unit tests.

Slice completion evidence:

- The planner produces a design review with exact evidence references.
- A write attempt is rejected.
- A budget blocker can resume without lost evidence.
- A changed repository revision produces a visible stale state.
- The user approves the Investigation and Design review visual checkpoint.

## Risks and recovery

- Tool output can consume excessive context. Store concise evidence and avoid repeated raw results.
- Repository changes can invalidate the design. Record the base revision and require revalidation before final approval.
- Permission filtering can hide required custom tools. Verify the effective tool catalog during session preflight.

## Non-goals

- Do not generate the plan outline.
- Do not write plan files.
- Do not run implementation commands.
- Do not install repository tools or analyzers.
- Do not approve the complete plan.

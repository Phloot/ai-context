# SL-09: Transition legacy plans and retire the old planner

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-09` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-08` |
| Acceptance criteria | `AC-001`, `AC-002`, `AC-020`, `AC-021`, `AC-022` through `AC-030` |

## Outcome

Existing plans remain readable, and Flightlog has one supported planning workflow.

The old modal planner and duplicate AI-refinement behavior are removed after the new workflow passes end-to-end validation.

## Requires

- Working planning inbox and workspace from `SL-01`.
- Complete new workflow through `SL-08`.
- Identified legacy-plan storage formats.
- Existing plan and attachment history.
- Successful end-to-end validation for simple and complex plans.
- Completed frontend visual checkpoints from the design contract.

## Produces

- Read-only legacy-plan access.
- A controlled path from a legacy plan to a new planning session.
- Preserved legacy content and attachment history.
- Removal of the old planner modal.
- Removal of the old refine-plan modal.
- Removal of the rubber-duck toggle.
- One supported planning entry point.

## Repository discovery

Before implementation, find:

- Every legacy plan data shape.
- Current plan status and attachment fields.
- Current review and deletion actions.
- Old planning and refinement endpoints.
- Old planner modal HTML, JavaScript, and CSS.
- Rubber-duck configuration and orchestration.
- Tests and documentation that reference the old planner.
- Installer or migration behavior for existing SQLite data.

Search for callers and references before deleting any symbol.

## Work units

### Legacy-plan reader

**Repository path:** Resolve from current plan persistence and artifact owners.

Read each supported legacy format without rewriting it.

Present:

- Story identity
- Repository when known
- Plan content
- Created and updated timestamps
- Attachment state
- Legacy format label

If a format is incomplete or corrupt, show an unsupported or recovery state. Do not discard the record.

### Continue in planning workspace

**Repository path:** Extend the planning application owner.

Create a new planning session from a supported legacy plan.

Carry forward only verified context:

- Story identity
- Repository identity when valid
- Legacy plan content as reference material
- Existing comments when available
- Prior attachment identity

The new session must perform current capability checks and story review. The legacy plan does not count as an approved new outline or slice.

Record the source legacy-plan identity on the new planning session.

### Planning inbox migration states

**Repository path:** Extend the inbox from `SL-01`.

Distinguish:

- New planning session
- Published plan set
- Supported legacy plan
- Unsupported legacy plan
- Legacy plan continued in the new workflow

Use `View` for legacy content and `Continue in planning workspace` for conversion.

Preserve existing delete behavior only when deletion is safe and already supported. Do not expand deletion scope in this slice.

### Retire old backend behavior

**Repository path:** Resolve from old Plan routers, services, engines, and integrations.

After callers migrate:

- Remove the old plan-generation command.
- Remove the old AI-refinement command.
- Remove rubber-duck orchestration used only by the old planner.
- Remove obsolete request and response models.
- Remove duplicate persistence decisions.
- Remove unused tests and update retained tests.

Preserve shared behavior used by story creation, Marketplace, Bootstrap, or other features.

### Retire old frontend behavior

**Repository path:** Resolve from current Tasks frontend files.

Remove:

- Old setup modal
- Old review and refine modal
- Rubber-duck toggle
- Obsolete event handlers
- Obsolete API calls
- Obsolete modal-specific styles

Keep a compact story and plan inbox. Do not restore the old table as a second planning surface.

Preserve the four-region workspace, petrol and verdigris themes, and technical-workbench hierarchy after old styles and handlers are removed.

### Documentation and labels

**Repository path:** Resolve from user help, release notes, and tests.

Update user-facing labels and help text for:

- Start plan
- Resume
- View published plan
- View legacy plan
- Continue in planning workspace

Add an upgrade note when Flightlog has an existing release-note mechanism.

## State and failure behavior

- A legacy read failure must not block new planning sessions.
- A failed continue operation must not modify the legacy plan.
- Repeating continue must resume the created session or require an explicit new version.
- An unsupported legacy plan must remain visible with recovery guidance.
- Remove old behavior only after the new path passes end-to-end validation.

## Tests and validation

Add or change focused tests for:

- Each supported legacy format.
- Unsupported or corrupt legacy content.
- Read-only legacy display.
- Continue into a new planning session.
- Repeated continue behavior.
- Preservation of legacy attachment identity.
- Inbox status and actions.
- Absence of old modal behavior.
- Absence of old refine-plan calls.
- Absence of the rubber-duck toggle.
- No remaining callers of deleted backend symbols.
- Four-region layout at 1280, 1440, and 1920 CSS pixels after cleanup.
- Light and dark theme conformance after old styles are removed.
- All phase-specific presentation and accessibility requirements.

Run full focused planning tests after deletion. Run affected Tasks, story-creation, Marketplace, Bootstrap, and shared AI tests when removed code was shared.

Slice completion evidence:

- A user can view each supported legacy plan.
- A user can continue a legacy plan without changing the original.
- A user can complete a new simple plan without the old modal.
- A user can complete and publish a complex plan.
- Repository search finds no unsupported caller of removed planner behavior.
- The user approves the final Validation, publication, and legacy visual checkpoint.

## Risks and recovery

- Legacy formats can contain undocumented variations. Add read support only for observed formats and preserve unsupported records.
- Old planner behavior can share an AI engine with another feature. Remove only planner-specific responsibility after caller inspection.
- A migration can create duplicate planning sessions. Use the source legacy ID and active-session rules for idempotency.

## Non-goals

- Do not rewrite legacy plans into the new format automatically.
- Do not delete legacy attachments.
- Do not add bulk migration.
- Do not expand plan deletion behavior.
- Do not change story creation.

# SL-01: Start or resume a planning workspace

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-01` |
| Status | Product-approved; repository mapping required |
| Dependencies | None |
| Acceptance criteria | `AC-001`, `AC-002`, `AC-003`, `AC-004`, `AC-022`, `AC-023`, `AC-026`, `AC-027`, `AC-028`, `AC-029`, `AC-030` |

## Outcome

A user can start or resume a persisted planning workspace for an accessible Agility story.

The user can start from the assigned-story list, a direct story ID, a recent planning session, or a supported legacy plan.

## Requires

- Existing Agility authentication and story access.
- Existing repository selection behavior.
- Existing Tasks navigation.
- Existing SQLite access and migration conventions.
- Existing model and reasoning configuration when available.
- The binding frontend design contract.

## Produces

- A stable planning-session identity.
- A verified story reference.
- A repository snapshot reference.
- A recorded planner configuration and budget.
- A capability-preflight result.
- An initial workflow state.
- A full-page workspace shell.

## Repository discovery

Before implementation, find:

- The Tasks and Plan route entry points.
- The assigned-story query owner.
- The current direct story lookup behavior, if present.
- The repository-selection owner.
- The plan persistence owner and schema migration pattern.
- The current planner modal and row actions.
- The frontend request and error-display conventions.
- Existing design tokens, theme switching, Bootstrap customization, and accessibility conventions.
- Tests for story loading, plan creation, and Tasks navigation.

Record an exact path and symbol for each existing owner. Reuse the owner when the responsibility is cohesive.

## Work units

### Planning-session domain and persistence

**Repository path:** Resolve from current plan and SQLite owners.

Add the minimum state required to identify a planning workflow:

- Planning-session ID
- Story system and story ID
- Story summary snapshot or reference
- Repository identity
- Selected branch
- Base revision
- Planner profile and planner version
- Model and reasoning setting
- Planning budget
- Current workflow phase
- Current plan version
- Created, updated, and last-opened timestamps

Define legal initial states. Reject a planning session without a verified story and repository.

Do not store detailed plan content in SQLite when the existing plan-file owner is suitable.

### Planning application behavior

**Repository path:** Resolve from the current plan service, engine, or domain owner.

Add commands and queries for:

- List assigned stories with planning status.
- Load an accessible story by ID.
- List recent planning sessions.
- Start a planning session.
- Resume a planning session.
- Read the workspace summary.

Starting the same story and repository must not create an accidental duplicate. Let the user resume the active session or explicitly start a new version.

Keep story lookup and repository lookup at integration boundaries. Keep workflow rules in the planning owner.

### Capability preflight

**Repository path:** Resolve from current Copilot, MCP, skill, and repository integrations.

Check the capabilities that the runtime planner requires:

- Packaged runtime planner resource
- Supported Copilot SDK session configuration
- Required structured Flightlog tools
- Agility story-read access
- Repository read and search access
- Plans-directory access
- Required Flightlog-owned implementation-planning capabilities

Return actionable blockers. Do not silently replace a required repository-search workflow.

Do not require the Marketplace implementation-planner for preflight.

Archive attachment capability can remain informational in this slice. `SL-08` makes the final publication decision.

### FastAPI boundary

**Repository path:** Resolve from current Tasks and Plan routers.

Add thin query and command endpoints. Reuse existing request, response, error, and dependency patterns.

The router must not own:

- Story-access policy
- Duplicate-session rules
- Repository snapshot creation
- Workflow transitions
- Capability evaluation

### Planning inbox and workspace shell

**Repository path:** Resolve from current Tasks frontend files.

Replace the current Plan subtab content with a planning inbox that contains:

- Assigned stories
- Direct story-ID input
- Recent planning sessions
- Legacy-plan entries
- Planning status
- One primary action for each item

Use `Start plan`, `Resume`, or `View` according to state.

Open the planner as a full-page application view. Do not open the old setup modal.

Implement the persistent desktop grid from the frontend design contract:

- Existing Flightlog global navigation
- Phase rail
- Center workbench
- Planner conversation rail
- Compact story and repository header

The center workbench must contain the primary action. The conversation rail must not control workflow state in this slice.

Preserve the four-region layout at supported desktop widths. Do not stack the regions or replace the phase rail with tabs.

### Planner themes and shared components

**Repository path:** Resolve from current theme, CSS, and Bootstrap owners.

Implement the light and dark petrol and verdigris tokens from the frontend design contract. Reuse equivalent existing tokens only when the resulting values and roles preserve the contract.

Create or extend the minimum shared frontend behavior for:

- Phase rail states
- Context header
- Workbench action row
- Inline status and alert states
- Bordered technical tables and rows
- Visible keyboard focus
- Supported viewport behavior

Do not create a generic design-system abstraction when existing cohesive CSS and components can own these styles.

### Setup workbench

**Repository path:** Resolve from the workspace frontend owner.

Implement Setup as an integrated two-column form with full-width planning context. Show story, repository, branch, base revision, planner, model, reasoning, budget, and capability preflight.

Keep `Begin story review` locked until required checks pass. Show the blocking check near the action.

Keep the conversation composer disabled before setup completes. Show `Waiting for setup` and explain when conversation becomes available.

## State and failure behavior

- Show an inaccessible story as a lookup error without creating a session.
- Show an unavailable repository as a setup blocker.
- Show a capability failure before the first planner turn.
- Preserve user-entered setup values after a recoverable error.
- Detect an existing active session for the same story and repository.
- Record the selected base revision before repository investigation.

## Tests and validation

Add or change focused tests for:

- Assigned-story planning status.
- Valid direct story lookup.
- Invalid or inaccessible story lookup.
- Planning-session creation.
- Duplicate-session handling.
- Planning-session resume.
- Required setup validation.
- Capability-preflight success and failure.
- Planning inbox loading, empty, and error states.
- Correct `Start plan`, `Resume`, and `View` actions.
- Full-page workspace navigation without the old modal.
- Four-region layout at 1280, 1440, and 1920 CSS pixels.
- Light and dark theme tokens and semantic states.
- Phase-rail completed, active, pending, blocked, and stale states.
- Context-header truncation and accessible full values.
- Keyboard focus and tab order through Setup.
- Setup loading, preflight, blocked, error, and ready states.

Run the existing focused tests for Tasks, Agility story access, repository selection, and SQLite migrations.

Slice completion evidence:

- A user can open a persisted workspace for an assigned story.
- A user can open a persisted workspace from a valid direct story ID.
- Reloading the inbox shows the created planning session.
- A missing required capability prevents planning and explains the blocker.
- The user approves the workspace grid, phase rail, context header, themes, and Setup checkpoint.

## Risks and recovery

- An incomplete migration can make existing plans unavailable. Add the new state without deleting legacy records.
- Duplicate-session rules can hide intentional replanning. Provide an explicit new-version action after the normal resume path.
- Repository revision commands can fail outside a supported repository. Return a setup blocker and preserve the draft session.

## Non-goals

- Do not start the planner conversation.
- Do not review story requirements.
- Do not investigate repository content.
- Do not generate an outline or slice.
- Do not remove legacy planner behavior.
- Do not attach a plan to Agility.

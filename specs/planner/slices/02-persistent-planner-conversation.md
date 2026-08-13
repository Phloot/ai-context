# SL-02: Run a persistent planner conversation

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-02` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-01` |
| Acceptance criteria | `AC-004`, `AC-005`, `AC-006`, `AC-025`, `AC-029`, `AC-030` |

## Outcome

The user can collaborate with the Flightlog runtime planner in a persistent conversation.

The conversation and workflow state survive a browser reload and a Flightlog restart.

## Requires

- Planning-session identity from `SL-01`.
- Verified story and repository references.
- Planner configuration and budget.
- Packaged runtime planner resource.
- Existing Copilot SDK client lifecycle.
- The conversation-rail rules in the frontend design contract.

## Produces

- A stored relationship between the planning session and Copilot session.
- A versioned runtime planner configuration.
- A resumable conversation.
- A structured planner-tool channel.
- Consistent active, idle, canceled, interrupted, and failed turn states.
- A stream or event mechanism for the planner interface.

## Repository discovery

Before implementation, find:

- Copilot client construction and shutdown.
- Session creation and resumption.
- Existing event streaming or polling.
- Existing AI-work serialization.
- Model and reasoning selection.
- Permission handlers, hooks, and available-tool configuration.
- Existing agent or prompt resource loading.
- Existing frontend chat or activity-stream behavior.
- Tests that mock the Copilot SDK.

Confirm the exact SDK behavior for the installed version. Upgrade only when a required supported API is missing or defective.

## Work units

### Runtime planner resource

**Repository path:** New package resource. Select the location from current package-data conventions.

Package a versioned planner instruction resource with the Flightlog wheel.

Do not load this resource from the Marketplace implementation-planner. Do not synchronize the two planner definitions automatically.

The resource must define:

- Critical planning behavior
- Read-only repository behavior
- Workflow-phase boundaries
- Structured tool usage
- Decision severity
- Outline-first generation
- Coherent slice requirements
- Approval restrictions
- Budget behavior
- Blocker reporting

Keep dynamic story, repository, user, and plan content outside this resource.

Record a stable planner version. Keep an active session on its recorded version.

### Planner session owner

**Repository path:** Resolve from the current Copilot engine or session owner.

Create or resume a Copilot session for one planning session.

On creation:

- Load the packaged planner instructions.
- Use system-message append or customize behavior.
- Register structured tools and handlers.
- Apply the read-only permission policy.
- Set the selected model and reasoning level.
- Apply supported session limits or the Flightlog budget.
- Record the Copilot session ID and planner version.

On resume:

- Verify planning-session ownership.
- Re-register required tools, hooks, and handlers.
- Restore event handling.
- Reconcile interrupted Flightlog turn state.

Do not use system-message replacement when replacement removes SDK safety rules.

### Structured tool foundation

**Repository path:** New or existing planner-tool owner. Justify each new file by responsibility.

Define typed host operations for later slices. The initial set should support these concepts:

- Request decisions
- Submit a phase result
- Report progress
- Raise a planning blocker
- Read current workflow context

Do not let the model mutate phase, approval, or version state directly. A tool handler validates each request and calls the planning domain owner.

Return stable identifiers in each structured result.

### Read-only permission policy

**Repository path:** Resolve from current permission handling.

Allow only required read and search operations for repository investigation.

Deny:

- Source-file writes
- Source-file deletion
- Git mutation
- Dependency installation
- Build or deployment actions
- Unapproved shell commands

Enumerate Flightlog custom tools when the SDK tool allowlist applies to both built-in and custom tools.

### Planner-turn coordination

**Repository path:** Resolve from current AI work queue or add a focused planning owner.

Enforce one active planner turn for each planning session.

Support:

- Start turn
- Observe turn events
- Cancel turn
- Mark interrupted turn
- Retry from stable workflow state
- Reject conflicting user commands

Queued free-form messages are optional. The minimum design can disable message submission during an active turn and preserve a user draft.

### Conversation interface

**Repository path:** Resolve from the workspace frontend owner.

Implement the right conversation rail with:

- Message history
- Streaming assistant content
- User input
- Active-turn status
- Cancel action
- Retry action
- Recoverable connection state
- Budget or usage summary
- Active-decision summary with an action that focuses the workbench decision
- A composer fixed at the bottom of the rail

Do not render internal reasoning content. Show concise progress events instead.

Align assistant messages left and user messages right. Keep the conversation visually subordinate to the center workbench.

Use accessible activity states for idle, working, waiting, reconnecting, and interrupted turns. Chat text alone must not confirm a material workflow decision.

## State and failure behavior

- A browser reconnect attaches to the current turn without starting another turn.
- An application restart marks an unfinished turn as interrupted until reconciliation completes.
- A resume failure preserves Flightlog workflow state and offers a safe retry.
- A planner-version mismatch does not silently rewrite an active session.
- A tool-schema validation error does not mutate workflow state.
- A denied repository mutation appears as a planner failure with corrective guidance.

## Tests and validation

Add or change focused tests for:

- Packaged planner-resource loading.
- Planner version persistence.
- Session creation configuration.
- Session resumption with handlers and tools.
- One active turn for each planning session.
- Turn cancellation.
- Browser reconnect during an active turn.
- Flightlog restart with an interrupted turn.
- Invalid structured-tool input.
- Permission denial for source mutation.
- Conversation loading, active, idle, failed, and retry states.
- Conversation-rail width and persistence at supported desktop widths.
- Keyboard and screen-reader behavior for composer, activity, cancel, and retry.
- Active-decision summary and focus behavior without decision confirmation in the conversation rail.

Use an SDK test double at the application boundary. Do not duplicate SDK framework tests.

Slice completion evidence:

- A user can exchange multiple messages with the planner.
- The conversation returns after a browser reload.
- The conversation returns after a Flightlog restart.
- A second concurrent turn is rejected.
- A repository write attempt is denied.
- The user approves the persistent conversation behavior at the Setup and conversation checkpoint.

## Risks and recovery

- Session state can diverge from SQLite after a process failure. Reconcile from the last stable Flightlog state.
- SDK events can arrive more than once. Process events idempotently where they change application state.
- A prompt update can invalidate active sessions. Pin the planner version and migrate only through a new session.

## Non-goals

- Do not perform story review.
- Do not perform repository investigation.
- Do not implement all later planner tools.
- Do not approve any plan artifact.
- Do not expose unrestricted Copilot CLI behavior.

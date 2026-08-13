# Flightlog interactive planner implementation plan

## Plan identity

| Field | Value |
| --- | --- |
| Plan-set ID | `FLLOG-PLANNER-V2` |
| Status | Product-approved; repository mapping required |
| Target application | Flightlog |
| Repository | Resolve during repository inspection |
| Branch | Resolve before implementation |
| Base revision | Record before repository investigation |
| Plan format | Versioned index with coherent slice files |
| Frontend contract | [Binding text-only design contract](design/frontend-design-contract.md) |

## Purpose

Replace the modal planner with one persistent planning workspace. The workspace must support both simple and complex implementation plans.

The planner must act as a critical technical partner. The planner must review requirements, inspect repository evidence, challenge weak decisions, and create coherent implementation slices.

This plan is a product and architecture handoff. It does not contain verified Flightlog paths or symbols. The implementation agent must map each responsibility to repository evidence before implementation.

## Goal

Deliver a story-backed planning workflow that lets a user:

- Start or resume a plan from an Agility story.
- Collaborate with a persistent planner session.
- Resolve requirement and design decisions.
- Review an outline before detailed slice generation.
- Approve each coherent implementation slice.
- Validate and approve the complete plan set.
- Save the approved plan set in the user's Flightlog plans directory.
- Attach an approved ZIP snapshot to the Agility story, or use the approved multiple-file fallback.

Simple stories must use the same workflow. Flightlog can compress phases that have no material content. Required reviews and approvals remain in effect.

## Non-goals

This plan does not:

- Change AI-assisted story creation.
- Implement a plan against the selected repository.
- Permit the planner to modify source code.
- Add storyless or cross-story planning.
- Preserve a separate simple planning workflow.
- Add a mobile-specific planning interface.
- Redesign unrelated Flightlog global navigation.
- Overhaul Marketplace or general agent configuration.
- Add hosted, multi-user Flightlog operation.
- Require a preview-only Copilot SDK feature.
- Generate one combined Markdown publication file.

## Confirmed decisions

| ID | Decision |
| --- | --- |
| `D-001` | Use one planning workflow with an automatically compressed fast path. |
| `D-002` | Require each new plan to reference an accessible Agility story. |
| `D-003` | Support assigned-story selection and direct story-ID loading. |
| `D-004` | Use a persistent full-page workspace instead of a modal sequence. |
| `D-005` | Keep the center workbench authoritative. Use the right rail for planner conversation. |
| `D-006` | Use one resumable Copilot session from story review through approval. |
| `D-007` | Flightlog owns phases, budgets, decisions, versions, validation, approval, and publication. |
| `D-008` | The planner owns critique, investigation, recommendations, and plan content. |
| `D-009` | Store canonical plan content as `index.md` and coherent slice files. |
| `D-010` | Store workflow metadata in SQLite. Do not use conversation history as workflow state. |
| `D-011` | Publish only an explicitly approved plan version. |
| `D-012` | Publish the approved plan set as a ZIP attachment when the Agility MCP supports archive access. |
| `D-013` | If ZIP access is unsupported, attach `index.md`, `manifest.json`, and the slice Markdown files separately. Do not create one combined Markdown file. |
| `D-014` | Present legacy plans as read-only content. Let the user continue a legacy plan in the new workflow. |
| `D-015` | Remove the old modal, refine modal, and rubber-duck toggle after the new workflow is complete. |
| `D-016` | Preserve planner dissent and user-directed exceptions in the decision log. |
| `D-017` | Ship a versioned Flightlog runtime planner with the Python package. |
| `D-018` | Keep the Marketplace implementation-planner independent from the Flightlog runtime planner. |
| `D-019` | Treat the text-only frontend design contract as a binding product requirement. |
| `D-020` | Use a persistent four-region desktop layout: global navigation, phase rail, center workbench, and planner conversation. |
| `D-021` | Use petrol and verdigris as the planner interaction palette in light and dark themes. Keep semantic status colors separate. |
| `D-022` | Keep workflow decisions, approvals, and primary actions in the center workbench. Conversation remains subordinate. |
| `D-023` | Require user visual approval at defined frontend checkpoints. Material deviations require approval. |

## Frontend design authority

The [frontend design contract](design/frontend-design-contract.md) defines the required layout, visual hierarchy, phase composition, theme tokens, component rules, accessibility, and validation checkpoints.

The implementation agent must use the contract as the complete visual specification. No external image asset or visual reference is required. Repository mapping can select existing HTML, JavaScript, CSS, and Bootstrap components. Repository mapping must not weaken the contract silently.

When an existing Flightlog pattern conflicts with the contract, the agent must:

1. Identify the conflict.
2. Explain the effect of each option.
3. Recommend the smallest cohesive implementation.
4. Request approval before a material visual deviation.

## Planner ownership

In this plan, the term planner means the packaged Flightlog runtime planner. The Marketplace implementation-planner is identified by its full name.

Flightlog must package a versioned runtime planner definition inside its Python distribution. The implementation agent must select an exact package-resource location that follows current repository conventions.

When Flightlog creates a Copilot session, Flightlog must:

- Load the packaged planner instructions.
- Append or customize the session system message.
- Preserve the Copilot SDK safety instructions.
- Register Flightlog-owned structured tools.
- Apply a read-only permission policy for repository work.
- Record the planner version on the planning session.

When Flightlog resumes a session, Flightlog must register the required handlers and tools again. An existing planning session keeps its recorded planner version. A new planner version must not silently change an active plan.

The runtime planner must understand the Flightlog workflow contract. It must not contain unnecessary details about Flightlog internals. Flightlog supplies dynamic story, repository, phase, budget, and plan-version context through application state and tool results.

## Acceptance criteria

| ID | Required behavior |
| --- | --- |
| `AC-001` | A user can find an assigned story or load another accessible story by ID. |
| `AC-002` | A user can start, resume, and view planning sessions from the planning inbox. |
| `AC-003` | Setup records the repository, branch or base revision, planning profile, and budget. |
| `AC-004` | Flightlog checks required planner and integration capabilities before planning begins. |
| `AC-005` | The conversation and workflow resume after a browser reload or Flightlog restart. |
| `AC-006` | Only one planner turn runs for a plan at one time. The user can cancel or retry the turn. |
| `AC-007` | The planner reviews the story and acceptance criteria before repository investigation. |
| `AC-008` | Material questions and user answers become structured, persistent decision records. |
| `AC-009` | Repository investigation is read-only, budget-aware, and supported by path and symbol evidence. |
| `AC-010` | A material design decision produces a critical design review with alternatives and consequences. |
| `AC-011` | The user reviews the ordered plan outline before detailed slices are generated. |
| `AC-012` | The user can split, merge, reorder, revise, and approve the outline within dependency constraints. |
| `AC-013` | Flightlog generates and reviews detailed slices individually in dependency order. |
| `AC-014` | An earlier change invalidates only affected approvals and downstream artifacts. |
| `AC-015` | Final approval stays locked until decisions, slices, and deterministic validation are complete. |
| `AC-016` | Approval writes a versioned plan set below the user's Flightlog plans directory. |
| `AC-017` | When the Agility MCP supports archive access, Flightlog creates a deterministic ZIP that contains the approved index, slices, and manifest. |
| `AC-018` | Flightlog attaches the approved snapshot to the Agility story and records the result. |
| `AC-019` | The user can retry attachment failures without duplicate plan versions or attachments. |
| `AC-020` | Existing plans remain accessible and can seed a new planning session without replacement. |
| `AC-021` | A simple story can complete the workflow without empty or unnecessary phases. |
| `AC-022` | The planner uses the required four-region desktop layout at supported widths. |
| `AC-023` | The persistent phase rail and compact context header show current workflow and repository state. |
| `AC-024` | The center workbench contains each material decision, approval, and primary phase action. |
| `AC-025` | The planner conversation rail persists across phases and supports activity, cancel, retry, and reconnect states. |
| `AC-026` | Light and dark themes use the approved petrol and verdigris tokens with accessible semantic states. |
| `AC-027` | The interface uses the approved technical-workbench design language and prohibited-pattern rules. |
| `AC-028` | Each planner phase uses the required phase-specific workbench composition. |
| `AC-029` | The planner supports keyboard interaction, visible focus, accessible status, and WCAG AA contrast. |
| `AC-030` | The user reviews and approves each required frontend visual checkpoint. |

## Ordered slices

| Slice | File | Primary outcome | Depends on |
| --- | --- | --- | --- |
| `SL-01` | [Start or resume a planning workspace](slices/01-start-resume-workspace.md) | A user can enter a persisted workspace for an accessible story. | None |
| `SL-02` | [Run a persistent planner conversation](slices/02-persistent-planner-conversation.md) | Planner conversation and active-turn state survive reconnects. | `SL-01` |
| `SL-03` | [Review the story and record decisions](slices/03-story-review-decisions.md) | The planner resolves material requirement questions before investigation. | `SL-02` |
| `SL-04` | [Investigate the repository and review the design](slices/04-repository-investigation-design-review.md) | The planner produces an evidence-based design review. | `SL-03` |
| `SL-05` | [Create and review the plan outline](slices/05-plan-outline-review.md) | The user approves slice structure before detailed generation. | `SL-04` |
| `SL-06` | [Draft and review coherent slices](slices/06-coherent-slice-review.md) | The user reviews each detailed slice in dependency order. | `SL-05` |
| `SL-07` | [Validate and approve the plan set](slices/07-plan-validation-approval.md) | Flightlog produces one immutable approved plan version. | `SL-06` |
| `SL-08` | [Write and publish the approved plan](slices/08-plan-save-publication.md) | Flightlog saves the plan and publishes an Agility snapshot. | `SL-07` |
| `SL-09` | [Transition legacy plans and retire the old planner](slices/09-legacy-transition.md) | Flightlog has one supported planning workflow. | `SL-08` |

## Acceptance-criteria coverage

| Criterion | Implementation slices | Validation slices |
| --- | --- | --- |
| `AC-001` | `SL-01` | `SL-01`, `SL-09` |
| `AC-002` | `SL-01` | `SL-01`, `SL-09` |
| `AC-003` | `SL-01` | `SL-01`, `SL-04` |
| `AC-004` | `SL-01`, `SL-02` | `SL-01`, `SL-02` |
| `AC-005` | `SL-02` | `SL-02` |
| `AC-006` | `SL-02` | `SL-02` |
| `AC-007` | `SL-03` | `SL-03` |
| `AC-008` | `SL-03` | `SL-03`, `SL-07` |
| `AC-009` | `SL-04` | `SL-04`, `SL-07` |
| `AC-010` | `SL-04` | `SL-04` |
| `AC-011` | `SL-05` | `SL-05` |
| `AC-012` | `SL-05` | `SL-05`, `SL-07` |
| `AC-013` | `SL-06` | `SL-06`, `SL-07` |
| `AC-014` | `SL-05`, `SL-06` | `SL-05`, `SL-06`, `SL-07` |
| `AC-015` | `SL-07` | `SL-07` |
| `AC-016` | `SL-08` | `SL-08` |
| `AC-017` | `SL-08` | `SL-08` |
| `AC-018` | `SL-08` | `SL-08` |
| `AC-019` | `SL-08` | `SL-08` |
| `AC-020` | `SL-09` | `SL-09` |
| `AC-021` | `SL-03` through `SL-07` | `SL-07`, `SL-09` |
| `AC-022` | `SL-01` | `SL-01`, `SL-09` |
| `AC-023` | `SL-01` | `SL-01`, `SL-03` through `SL-09` |
| `AC-024` | `SL-01`, `SL-03` through `SL-08` | `SL-03` through `SL-09` |
| `AC-025` | `SL-02` | `SL-02`, `SL-03` through `SL-09` |
| `AC-026` | `SL-01` | `SL-01`, `SL-09` |
| `AC-027` | `SL-01`, `SL-03` through `SL-09` | `SL-01`, `SL-09` |
| `AC-028` | `SL-01`, `SL-03` through `SL-08` | `SL-01`, `SL-03` through `SL-09` |
| `AC-029` | `SL-01`, `SL-02`, `SL-05` | `SL-01` through `SL-09` |
| `AC-030` | `SL-01`, `SL-04`, `SL-06`, `SL-08`, `SL-09` | `SL-09` |

## Cross-slice contracts

These names describe responsibilities. They are not required Python class names.

| Contract | Required content |
| --- | --- |
| Planning session | Story, repository snapshot, Copilot session, planner version, phase, budget, and current plan version |
| Workflow state | Current phase, legal transitions, blocking conditions, active turn, and recovery state |
| Repository snapshot | Repository identity, selected branch, base revision, working state, and stale status |
| Decision record | Question, severity, options, recommendation, answer, consequence, status, and affected artifacts |
| Evidence reference | Repository path, symbol, evidence summary, revision, and source operation |
| Plan outline | Goal, non-goals, decisions, slice identities, order, dependencies, and criterion coverage |
| Plan slice | Outcome, requirements, products, file work units, validation, risks, and non-goals |
| Approval record | Artifact type, artifact ID, artifact version, user action, and timestamp |
| Plan version | Version identity, source artifact versions, validation result, and immutable approval state |
| Publication record | Local output, archive identity, attachment identity, attempts, status, and error details |

The implementation agent must reuse existing models when those models own the same responsibility. The implementation must not create parallel models only to match these contract names.

## Repository mapping requirements

Before implementation, inspect the smallest relevant repository area. Find exact paths and symbols for:

- Tasks and Plan routers.
- Story listing and story loading.
- Current plan domain behavior.
- SQLite access and schema migrations.
- Copilot client and session lifecycle.
- Agent, model, and reasoning configuration.
- Agility MCP calls and attachment behavior.
- Repository selection and branch discovery.
- The user's Flightlog plans-directory resolution.
- Tasks frontend HTML, JavaScript, and CSS.
- Shared frontend request and state behavior.
- Existing design tokens, theme switching, and Bootstrap customization.
- Existing viewport, accessibility, and frontend test conventions.
- Current planner and legacy-plan tests.

For each existing file, record the exact path and relevant symbol. For each new file, mark the path as new and justify its responsibility.

Do not create a parallel `planner_v2` architecture. Extend or consolidate the current owners when they are cohesive.

## Sequencing constraints

- Keep the old planner available until `SL-08` passes end-to-end validation.
- Do not generate detailed slices before the outline has user approval.
- Do not allow final approval before each required slice has approval.
- Do not write approved files before plan-set validation succeeds.
- Do not attach an archive before the approved local plan version exists.
- Do not retire legacy routes before legacy content is accessible in the new interface.
- Do not silently upgrade the planner definition for an active session.
- Do not implement a material visual deviation without explicit approval.
- Do not continue dependent frontend work after a rejected visual checkpoint.

## Plan-set validation sequence

1. Validate focused backend behavior after each backend change.
2. Validate frontend state transitions after each UI change.
3. Validate browser reload and application restart recovery.
4. Validate planner tool schemas and rejected invalid transitions.
5. Validate outline and slice invalidation behavior.
6. Validate the complete fast path for a one-slice plan.
7. Validate the complete multi-slice path with revised decisions.
8. Validate local publication and deterministic archive contents.
9. Validate successful, failed, retried, and duplicate Agility publication.
10. Validate legacy-plan access before old behavior is removed.
11. Validate the four-region layout at 1280, 1440, and 1920 CSS pixels.
12. Validate light and dark theme tokens, focus states, and WCAG AA contrast.
13. Complete each user visual-review checkpoint in the frontend design contract.
14. Run repository-configured Python and frontend quality commands.
15. Run the repository file-growth check and complete a subtraction review.

## Implementation budget

Repository inspection must replace this provisional budget with an evidence-based estimate.

Use the budget as a growth guard, not as a target. The work agent must explain a material increase.

Expected scope:

- One extended planning domain or application owner.
- One versioned runtime planner resource.
- A small set of structured planner tools.
- SQLite changes for workflow metadata and versions.
- Thin FastAPI endpoints for commands and queries.
- One desktop planning workspace within the existing frontend structure.
- Focused tests at domain, API, integration, and browser-relevant boundaries.

Do not add interfaces, managers, processors, or generic utilities without a current ownership or integration boundary.

## Unresolved technical discoveries

No unresolved product decision remains. The work agent must resolve these technical discoveries:

- Confirm whether the Agility MCP can download and inspect ZIP attachments.
- Determine the exact plan-attachment API and idempotency fields.
- Determine the current legacy-plan storage formats.
- Determine how the current SDK version persists and resumes local sessions.
- Determine which read-only repository tools are available to SDK sessions.
- Determine whether the existing frontend supports streaming events or needs an added transport.
- Determine how the current application serializes concurrent AI work.

If the Agility MCP cannot inspect archives, use the approved multiple-Markdown-attachment fallback.

## Completion definition

The implementation is complete when:

- One supported planner workflow remains.
- Simple and complex plans use the same state model.
- The planner cannot modify the selected repository.
- Planning state survives browser and application restarts.
- The user approves the outline, slices, and final plan explicitly.
- The approved plan exists in the user's Flightlog plans directory.
- The Agility story contains an accessible approved plan snapshot.
- Legacy plans remain readable.
- The planner follows the binding frontend design contract.
- The user approves each frontend visual checkpoint.
- Focused tests and configured quality checks pass.

Reviewed for ASD-STE100 alignment. The official dictionary was not available.

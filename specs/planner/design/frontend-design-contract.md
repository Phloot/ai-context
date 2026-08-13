# Flightlog planner frontend design contract

## Status and authority

This contract defines the required planner layout, visual hierarchy, interaction placement, and theme character.

The implementation agent must preserve this contract while it maps the plan to repository components. Existing Flightlog patterns control implementation details only when those patterns do not conflict with this contract.

The agent must request approval before it makes a material deviation.

A material deviation includes:

- Removing or relocating a primary workspace region.
- Replacing the phase rail with tabs, breadcrumbs, or a step modal.
- Making conversation the primary workflow surface.
- Moving decisions or approvals into chat only.
- Replacing the technical workbench with a card dashboard.
- Changing the petrol and verdigris theme character.
- Stacking the desktop regions into a mobile layout.

## Design intent

The planner must look like a focused technical workbench. It must not look like a generic administration dashboard or consumer chat application.

Use these characteristics:

- Compact information density.
- Strong alignment and clear borders.
- One authoritative work surface.
- Restrained decoration.
- Visible workflow progress.
- Explicit decisions and approvals.
- Persistent but subordinate conversation.
- Consistent light and dark themes.

## Desktop viewport

Design for a desktop viewport from 1440 to 1920 CSS pixels wide.

Support a minimum width of 1280 CSS pixels. Below 1280 pixels, do not stack the primary regions. Show a minimum-width notice or use the repository's approved desktop overflow behavior.

At widths from 1280 to 1439 pixels, use the compact region sizes in the application-grid table. Do not hide a region in compact mode.

The planner workspace uses the full available viewport height. Avoid page-level horizontal scrolling at supported widths.

## Application grid

Use four persistent regions and one context header.

| Region | Required size and behavior |
| --- | --- |
| Global navigation | Preserve the existing Flightlog navigation width and behavior. Use the existing dark neutral treatment in both themes when practical. |
| Phase rail | At 1440 pixels or wider, use a fixed width from 200 to 224 pixels. From 1280 to 1439 pixels, use 184 to 200 pixels. Keep the rail visible during all planner phases. |
| Center workbench | Use all remaining width. Use a minimum width of 640 pixels at 1440 pixels or wider. Use a minimum width of 560 pixels in compact mode. This region owns workflow content and actions. |
| Planner conversation | At 1440 pixels or wider, use a fixed width from 320 to 368 pixels. From 1280 to 1439 pixels, use 288 to 320 pixels. Keep the conversation visible during the workflow. |
| Context header | Use a height from 48 to 56 pixels. Span the center workbench and conversation region. |

Use this conceptual grid:

```text
┌──────────────┬──────────────┬────────────────────────────────────┬───────────────────┐
│              │              │ Story · Repository · Branch · Revision · Planner · Budget · Status │
│ Global nav   │ Phase rail   ├────────────────────────────────────┼───────────────────┤
│              │              │ Authoritative center workbench     │ Planner           │
│              │              │                                    │ conversation      │
└──────────────┴──────────────┴────────────────────────────────────┴───────────────────┘
```

Do not put the planner inside a Bootstrap modal. Do not put the conversation in a floating widget.

## Spacing and shape

Use an 8-pixel spacing rhythm.

Recommended values:

- Center workbench horizontal padding: 24 to 32 pixels.
- Rail padding: 12 to 16 pixels.
- Major section gap: 24 pixels.
- Related control gap: 8 to 12 pixels.
- Standard control height: 36 to 40 pixels.
- Context header horizontal gap: 16 to 20 pixels.
- Border radius: 6 to 8 pixels for controls and bounded panels.
- Border radius: 3 to 5 pixels for compact status labels and identifiers.

Do not use fully rounded pill shapes for ordinary labels or buttons.

Use shadows only when a surface must appear above another surface. Prefer borders and background contrast.

## Typography

Use the existing Flightlog typeface when it is suitable. Otherwise, use a precise system sans-serif typeface comparable to Inter.

Use a restrained monospace typeface for:

- Story IDs
- Slice IDs
- Acceptance-criteria IDs
- Repository paths
- Symbols
- Git revisions
- Plan versions

Use this hierarchy:

- Phase heading: 22 to 26 pixels, medium or semibold.
- Section heading: 15 to 17 pixels, semibold.
- Body and controls: 13 to 15 pixels.
- Compact metadata: 11 to 13 pixels.

Do not use an oversized page title or hero heading.

## Light theme tokens

Use these tokens as the baseline. The implementation can adjust a token only to meet contrast requirements or align with an existing equivalent token.

| Token | Value | Use |
| --- | --- | --- |
| `--planner-canvas` | `#F3F5F2` | Warm mineral-gray workspace canvas |
| `--planner-surface` | `#FFFFFF` | Primary workbench and rail surfaces |
| `--planner-surface-muted` | `#F7F9F7` | Secondary rows and quiet bounded regions |
| `--planner-text` | `#1B2423` | Primary text |
| `--planner-text-muted` | `#66716F` | Secondary text |
| `--planner-border` | `#D8DEDC` | Dividers and control borders |
| `--planner-petrol` | `#0F5B62` | Primary actions and active navigation |
| `--planner-petrol-hover` | `#0B484E` | Primary hover state |
| `--planner-petrol-tint` | `#DCEEEF` | Active phase and selected row background |
| `--planner-verdigris` | `#2E8B78` | Focus, progress, evidence links, and supporting accents |
| `--planner-verdigris-tint` | `#DFF1EA` | Supporting selection and progress backgrounds |

Do not use default Bootstrap administration blue or purple as the planner accent.

## Dark theme tokens

| Token | Value | Use |
| --- | --- | --- |
| `--planner-canvas` | `#111716` | Main canvas |
| `--planner-surface` | `#171E1D` | Primary workbench and rail surfaces |
| `--planner-surface-muted` | `#1D2624` | Secondary rows and bounded regions |
| `--planner-text` | `#E4EAE8` | Primary text |
| `--planner-text-muted` | `#9EAAA6` | Secondary text |
| `--planner-border` | `#33403D` | Dividers and control borders |
| `--planner-petrol` | `#195D61` | Selected backgrounds and deep active surfaces |
| `--planner-petrol-tint` | `#163B3B` | Active phase and selected row background |
| `--planner-verdigris` | `#4FAE96` | Primary actions, focus, progress, and links |
| `--planner-verdigris-hover` | `#69C2AB` | Primary hover state |

Do not use bright cyan glow effects or saturated neon colors.

## Semantic colors

Keep semantic state separate from the petrol and verdigris interaction palette.

- Use a muted green for completed and accepted states.
- Use amber for in-review, stale, and non-blocking warning states.
- Use red only for errors, destructive actions, and blocking failures.
- Use neutral gray for pending, inactive, and unavailable states.

Verify WCAG AA contrast for text, controls, focus, and status indicators in both themes. Do not communicate status through color alone.

## Global navigation

Preserve the existing top-level order:

1. `Usage`
2. `AI Bootstrap`
3. `Marketplace`
4. `Tasks`

Keep `Tasks` active throughout the planner workspace.

Do not redesign unrelated global navigation as part of this work.

## Phase rail

Show these phases in order:

1. `Setup`
2. `Story review`
3. `Investigation`
4. `Design review`
5. `Outline`
6. `Slice review`
7. `Validate & publish`

Use a vertical sequence with numbered circular markers and a restrained connecting line.

Use these states:

- Completed: neutral row with a muted green check.
- Active: petrol-tint row, petrol or verdigris marker, and stronger label weight.
- Pending: neutral text and outlined marker.
- Blocked: amber or red indicator with a short accessible label.
- Stale: amber indicator and `Stale` text.

The rail communicates location and status. It does not replace validation or workflow controls in the center workbench.

During slice review, show the ordered slice list below a divider. Use `Accepted`, `In review`, `Pending`, `Stale`, and `Blocked` states.

During outline review, show a compact outline summary below a divider. Include outline version, review status, slice count, and criterion coverage.

## Context header

Show compact label-value pairs for:

- Story
- Repository
- Branch
- Base revision
- Planner version
- Budget remaining
- Workflow status

Use separators instead of independent cards. Truncate long values with an accessible full-value affordance.

Do not repeat this information in a large banner.

## Center workbench

The center workbench is the authoritative workflow surface.

Each phase must contain:

- One clear phase heading.
- A concise purpose statement when needed.
- Structured phase content.
- Visible blocker or stale state when applicable.
- One primary next action.
- Secondary actions with lower visual emphasis.

Place phase actions in a bottom action row within the workbench. Keep the primary action at the right edge.

Do not require the user to find a workflow action in conversation history.

Use flat document sections, tables, and bordered rows. Use a bounded panel only when the content has one distinct interaction or status boundary.

## Planner conversation rail

Title the rail `Planner`.

Use these regions:

- Header with title and secondary menu.
- Scrollable message history.
- Active-decision summary with an action that focuses the workbench decision.
- Activity state.
- Composer fixed at the bottom of the rail.

Align assistant messages left and user messages right. Use compact bordered message surfaces. Keep message width below approximately 88 percent of the rail.

Show concise activity such as:

- `Planner idle`
- `Planner working`
- `Waiting for setup`
- `Reconnecting`
- `Turn interrupted`

When a planner turn is active, show a `Cancel turn` action near the composer.

Do not show internal reasoning. Summarize tool work as useful progress.

A material decision must appear as structured controls in the center workbench. The conversation can explain or link to the decision. Chat content and conversation-rail controls cannot confirm it.

## Control hierarchy

Use one strong primary action for the current phase.

Examples:

- `Begin story review`
- `Continue to design review`
- `Approve outline`
- `Accept slice`
- `Approve plan`
- `Retry publication`

Use outlined or text buttons for secondary actions. Use red only for destructive actions.

Disable a locked action and show the blocking reason near the action. Do not use a disabled button without an explanation.

## Component rules

### Tables

Use tables for exact mappings, ordered slices, evidence, work units, and criterion coverage.

Keep headers compact. Use horizontal dividers. Avoid placing a separate card around each row.

Provide button and keyboard controls for reorder operations. Drag-and-drop can be an additional interaction but cannot be the only interaction.

### Status labels

Use compact rectangular labels for version, review, stale, and blocked states.

Do not turn every identifier or metadata value into a pill.

### Forms

Use a two-column form at wide desktop widths when fields have short values. Use full-width rows for long context input.

Keep fields inside the workbench surface. Do not place each field group in a separate card.

### Alerts

Use inline alert strips for stale revisions, blockers, and publication failures.

Keep informational alerts restrained. Do not use full-screen warning banners for non-blocking states.

## Phase presentation

### Planning inbox

Use a compact table or structured list for assigned stories, direct story lookup, recent planning sessions, and legacy plans.

Give each row one primary action: `Start plan`, `Resume`, or `View`.

Do not use a gallery of story cards.

### Setup

Use an integrated two-column form.

Show:

- Read-only accessible story.
- Repository selection.
- Branch selection.
- Base revision.
- Planner profile.
- Model and reasoning.
- Planning budget.
- Optional planning context.
- Capability preflight.

Show capability checks as one compact row or list near the bottom. Keep `Begin story review` locked until required checks pass.

Before setup completes, keep the conversation composer disabled. Explain that conversation begins after setup.

### Story review

Show the story and acceptance criteria in the workbench.

Group planner concerns by `blocking`, `high-impact`, `advisory`, and `informational` severity.

Show no more than three material questions in one decision checkpoint. Use structured options and free-form input.

Keep the final interpreted decision visible before the user continues.

### Investigation

Show a compact progress summary with evidence count, completed areas, budget, and blockers.

Use structured rows for investigation categories:

- API entry points
- Current owner
- Persistence
- External integrations
- Focused tests

Show an evidence ledger table with evidence ID, path or symbol, and finding.

Show summarized live activity. Do not show a raw search or tool-call log.

Lock the next-phase action while required investigation is active. Show the reason.

### Design review

Show the recommendation first.

Then show:

- Evidence-backed findings.
- Important alternatives.
- Consequences.
- Maintainability concerns.
- Confirmed assumptions.
- Blocking and high-impact decisions.

Use a comparison table when two or three alternatives have repeated attributes. Put structured decision controls in the workbench or decision region.

### Outline

Show goal and non-goals above one ordered slice table.

The table must show:

- Order
- Slice ID and title
- Primary outcome
- Dependencies
- Acceptance criteria
- Status

Provide accessible reorder, split, merge, revise, and approve actions.

Show criterion coverage, dependency-cycle status, and important cross-slice contracts below the table.

State clearly that detailed slice generation has not begun.

### Slice review

Show one slice at a time as a technical document.

Show:

- Slice ID, title, version, and status.
- Outcome.
- Requires.
- Produces.
- File work units.
- Tests and validation.
- Risks and recovery.
- Non-goals.
- Acceptance criteria and evidence references.

Use a table for file work units. Keep `Accept slice` as the primary action. Provide `Request revision` and `Return to decision` as secondary actions.

### Validate and publish

Show plan completeness before publication controls.

Show:

- Outline and slice approval states.
- Criterion coverage.
- Validation findings grouped by corrective phase.
- Repository revision status.
- Local plan status.
- Agility publication status.

Keep `Approve plan` locked until deterministic validation passes.

After approval, show local writing and Agility publication as separate states. A failed attachment must expose `Retry publication` without regenerating the plan.

## Loading, empty, error, and conflict states

Each frontend owner must implement:

- Initial loading.
- Empty result.
- Recoverable request error.
- Blocking integration error.
- Active planner turn.
- Reconnecting session.
- Interrupted turn.
- Stale repository revision.
- Stale artifact version.
- Optimistic concurrency conflict.
- Publication partial failure.

Preserve the last stable workbench content during a recoverable error when possible.

Do not replace the full workspace with a spinner after initial load.

## Accessibility

- Use semantic landmarks for navigation, phase rail, main workbench, and conversation.
- Give the current phase an accessible current-step state.
- Maintain a visible keyboard focus indicator.
- Give icon-only controls accessible names.
- Do not use color as the only status signal.
- Keep tab order consistent with the visual hierarchy.
- Announce planner activity and validation changes without moving focus unexpectedly.
- Provide keyboard alternatives for reorder operations.
- Verify WCAG AA contrast in light and dark modes.

## Prohibited patterns

Do not use:

- A modal sequence as the main workflow.
- A card for every section, field group, or status.
- Fully rounded pills for most metadata.
- Large gradient backgrounds.
- Glassmorphism or translucent panels.
- Bright cyan glow effects.
- Decorative charts.
- A large empty hero area.
- A floating chat widget.
- Chat-only decisions or approvals.
- A mobile stack at supported desktop widths.
- Default Bootstrap administration blue or purple as the accent.

## Visual validation checkpoints

Pause for user visual review after these checkpoints:

1. Workspace grid, phase rail, context header, and both themes.
2. Setup and persistent conversation behavior.
3. Investigation and design-review states.
4. Outline and slice-review states.
5. Validation, publication, and legacy states.

At each checkpoint:

- Run the frontend at a supported desktop viewport.
- Present the live page or a screenshot to the user.
- Identify any known visual deviation from this contract.
- Record approval or requested changes.
- Correct material deviations before dependent frontend work continues.

If automated image inspection is unavailable, use browser DOM inspection and user visual approval. Do not omit the checkpoint.

## Design completion evidence

The frontend design is complete when:

- The four-region desktop layout remains stable through all phases.
- The phase rail clearly shows completed, active, pending, blocked, and stale states.
- The center workbench owns each workflow action.
- The conversation rail remains available and subordinate.
- Setup, investigation, outline, slice review, and publication follow this contract.
- Light and dark themes use the petrol and verdigris system.
- Supported desktop widths do not create page-level horizontal scrolling.
- Keyboard and contrast checks pass.
- The user approves each required visual checkpoint.

Reviewed for ASD-STE100 alignment. The official dictionary was not available.

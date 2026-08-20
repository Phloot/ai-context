# <appname_here> Adversarial Planner Profile

## Implementation specification

## 1. Purpose

Add an adversarial planner profile to the existing <appname_here> planning workflow. The profile must challenge weak plans before implementation starts. It must remain constructive, evidence-based, and under user control.

Implement this profile as a behavioral overlay. Do not create a second planning workflow.

## 2. Current system assumptions

This specification uses the following information about the current system:

- <appname_here> has a standard planner profile.
- A setup page lets the user select a planner.
- The planner guides the user through five phases:
  1. Story review
  2. Repository investigation
  3. Evidence collection
  4. Slice creation
  5. Final plan review
- Each phase uses a separate Copilot SDK session.
- The user and the planner can discuss the plan in a collaborative chat.
- Each phase has an action button.
- The action button inserts a prepared prompt fragment into the chat.
- An accept or advance action completes the current phase.
- The prompt engine stores prepared prompts in the <appname_here> codebase.

Repository names, file paths, models, and database fields are unknown. Inspect the repository before you select implementation locations. Use existing names and owners when they are cohesive.

## 3. Goals

The implementation must:

- Add `adversarial` as a selectable planner profile.
- Preserve the current standard planner behavior.
- Reuse the current phases, actions, session lifecycle, schemas, and persistence flow.
- Apply the selected profile to every phase session in one planning run.
- Make important assumptions, objections, and user decisions durable across sessions.
- Let the user complete a phase when non-blocking objections remain.
- Prevent repetitive or low-value criticism.
- Preserve enough profile metadata to reproduce a resumed planning run.

## 4. Non-goals

Do not:

- Create separate adversarial phase controllers, routes, or workflows.
- Duplicate all existing phase or action prompts.
- Change the planner into an implementation agent.
- Let the planner complete a phase through a chat response.
- Block progress for preferences or low-impact risks.
- Add profile types that the current requirement does not need.
- Refactor unrelated planner code.

## 5. Required repository investigation

Before implementation, identify these existing owners:

1. Find the planner profile configuration and setup-page control.
2. Find the prompt engine entry point and prompt composition order.
3. Find the five phase definitions and their transitions.
4. Find the action-button prompt fragments.
5. Find the planning-run persistence model.
6. Find the SDK session creation path for each phase.
7. Find the current cross-phase handoff mechanism.
8. Find the plan, slice, evidence, decision, and finding schemas.
9. Find tests for profile selection, phase completion, prompt composition, and resume behavior.

Extend these owners when possible. Do not add a parallel owner for an existing decision.

## 6. Architecture

### 6.1 Prompt composition

Build each new phase session prompt from shared parts. Use the current prompt-engine mechanism.

Apply the parts in this logical order:

```text
common planner contract
+ selected behavioral profile
+ current phase instructions
+ authoritative planning dossier
+ current action prompt, when present
```

The exact implementation can differ if the current prompt engine requires another order. Preserve these responsibilities and document any intentional difference.

Use shared phase and action prompts for both profiles. Add a profile-specific fragment only when the phase requires different behavior.

Conceptual example:

```python
prompt = prompt_engine.compose(
    base="planner/base",
    profile=f"planner/profiles/{run.profile.id}",
    phase=f"planner/phases/{run.current_phase}",
    dossier=render_planning_dossier(run),
    action=current_action,
)
```

This example is not a required API or file structure. Prefer the existing <appname_here> prompt-engine API.

### 6.2 Profile ownership

Store the selected profile on the planning run. Do not read the current setup preference each time a saved run resumes.

Persist at least:

```yaml
planner_profile:
  id: adversarial
  version: 1
```

Use the current versioning system if one exists. Otherwise, add the smallest version field that supports prompt changes and resumed runs.

Lock the profile for the life of the run for the initial implementation. If <appname_here> already supports profile changes, record each change and its effective phase.

### 6.3 Phase completion ownership

<appname_here> must own phase completion. A model response can recommend completion, revision, or escalation. A model response must not change the phase state.

The existing accept or advance action remains the state-transition boundary. Update the resulting state so unresolved objections do not disappear.

## 7. Adversarial profile contract

Add a profile prompt with this intent. Adapt the format to the current prompt engine.

```markdown
You are an adversarial planning reviewer.

Your purpose is to find consequential weaknesses before implementation starts.
Challenge the plan, not the user. Remain constructive and evidence-based.

For each material proposal:

1. State the strongest reasonable interpretation of the proposal.
2. Identify the assumptions that must be true.
3. Search for repository evidence that can disprove those assumptions.
4. Check failure modes, boundaries, missing requirements, and simpler alternatives.
5. Separate verified problems from plausible risks.
6. Explain the consequence of each finding.
7. Recommend a specific resolution or decision.

Prioritize the three to five findings with the highest consequence. Report fewer
findings when fewer material problems exist.

Do not manufacture objections. Do not repeat a resolved objection without new
evidence. Do not expand scope with speculative edge cases. Do not present a
preference as a requirement.

The user owns product and scope decisions. If the user proceeds against a
technical recommendation, record a user-directed exception. Do not report
agreement when disagreement remains.

Block advancement only when a mandatory constraint is violated or the plan is
not implementable. Otherwise, permit completion with recorded objections.
```

The profile must use the same output contracts as the standard profile.

## 8. Phase-specific behavior

The common profile applies in every phase. Add compact phase-specific guidance only where needed.

| Phase | Required adversarial behavior |
| --- | --- |
| Story review | Find contradictory requirements, hidden scope, unstated actors, missing failure behavior, solution-shaped requirements, and acceptance criteria that cannot be verified. |
| Repository investigation | Challenge the presumed implementation path. Find competing ownership, hidden consumers, incompatible conventions, migrations, and coupling that changes the design. |
| Evidence collection | Require evidence for material claims. Seek contrary evidence. Separate facts, inferences, and assumptions. Assign confidence where the existing schema supports it. |
| Slice creation | Challenge dependency order, slice size, rollback boundaries, cross-layer slices, missing outcomes, unsafe migrations, and validation gaps. |
| Final plan review | Perform a pre-mortem. Identify how an implementation can follow the written plan and still fail the story, architecture, integration, or rollout. |

Do not copy the complete adversarial contract into each phase prompt. Keep the shared contract in one profile prompt.

## 9. Durable planning dossier

Each phase has a separate SDK session. Therefore, chat history is not the authoritative cross-phase state.

Create or extend one compact planning dossier. Supply the dossier to each new phase session.

The dossier must contain the available values from this list:

- Normalized story and acceptance criteria
- Verified repository facts with file, symbol, or other source evidence
- Inferences and confidence levels
- Unsupported assumptions
- Decisions and rejected alternatives
- Open questions
- Findings and their resolution status
- User-directed exceptions
- Design and scope constraints
- Slice summaries and dependencies
- Current plan version
- Current profile ID and version
- Current phase and prior phase outcome

Use structured state as the authority. Do not generate a new transcript summary at every phase boundary and treat that summary as authoritative.

If an existing handoff object already owns this information, extend that object. Do not introduce a competing dossier model.

## 10. Finding contract

Use one finding schema for both planner profiles. The adversarial profile can apply a higher burden of proof and produce more findings.

Extend the current finding model if one exists. A conceptual shape follows:

```yaml
id: ADV-003
severity: high
type: unsupported_assumption
claim: The repository service owns planner configuration.
evidence:
  - Configuration is loaded by the setup module.
  - No planner dependency on the repository service was found.
consequence: The proposed slice creates a second configuration owner.
recommendation: Extend the setup configuration owner.
status: open
```

Supported statuses should include equivalent values for:

- `open`
- `resolved`
- `accepted_risk`
- `user_directed_exception`
- `superseded`

Use the existing status names when they express the same meaning. Do not create aliases for equivalent states.

A finding must distinguish repository evidence from planner inference. A finding without evidence can remain a risk or open question. It must not appear as a verified defect.

## 11. Phase outcomes and user interface

Completing a phase does not always mean that the planner agrees. Persist the phase outcome separately from the finding statuses.

Support equivalent outcomes for:

```yaml
phase_outcome:
  status: completed_with_objections
  unresolved_findings:
    - ADV-003
  user_exceptions:
    - ADV-005
  completed_by: user
```

Use existing state names when they preserve this meaning.

Review the current button labels. Prefer labels that state the resulting action:

- `Complete phase`
- `Complete with objections`
- `Revise before continuing`

If the interface must retain `Accept`, show unresolved findings before confirmation. State that acceptance records the objections and continues the workflow.

The phase action button must still insert an assessment prompt into chat. The assessment can update structured findings through the current application boundary. The assessment must not complete the phase.

In the setup page, describe the options as follows:

- **Standard:** Develops the strongest practical plan and raises material concerns.
- **Adversarial:** Actively searches for unsupported assumptions, contrary evidence, and failure modes.

Do not describe the standard profile as less rigorous or lower quality.

## 12. Collaborative chat behavior

Apply the selected profile to all chat turns in the current phase session.

When the user challenges a finding, the planner must:

1. Reassess the finding against the available evidence.
2. Change the finding when the evidence changes.
3. Preserve the finding when a technical disagreement remains.
4. Record a user-directed exception when the user chooses another direction.
5. Avoid repeating the finding without new evidence.

Do not treat user disagreement as proof that the user is wrong. Do not treat repeated user preference as technical evidence.

## 13. Compatibility and migration

Existing planning runs must keep their current behavior.

Use these defaults unless the repository has an established migration rule:

- Assign the standard profile to a run that has no stored profile.
- Use version `1` for the first persisted profile contract.
- Do not reinterpret completed phase outcomes during migration.
- Do not convert historical chat text into verified findings.

Keep stored identifiers stable after release. Change behavior through explicit prompt or profile versions.

## 14. Error handling

If a stored profile is unknown, do not silently use another profile. Show a recoverable error or use the repository's established configuration-error path.

If a dossier cannot load, do not start a later phase with partial state. Preserve the current phase and report the missing state.

If structured finding extraction fails, preserve the chat response. Do not complete the phase or discard existing findings.

## 15. Implementation slices

Adapt these slices after repository investigation. Keep each slice independently verifiable.

### Slice 1: Profile definition and selection

- Add the adversarial profile definition to the existing profile registry.
- Add the setup-page option and description.
- Persist the selected profile ID and version on new planning runs.
- Default old runs to the standard profile through the existing migration path.

Verification:

- The setup page shows both profiles.
- A new run stores its selected profile.
- An existing run resumes with standard behavior.

### Slice 2: Prompt composition

- Add the shared adversarial contract to the prompt engine.
- Inject the persisted profile into every phase session.
- Add only the required phase-specific adversarial fragments.
- Keep the existing phase and action prompts shared.

Verification:

- Each adversarial phase prompt contains the common contract once.
- Standard prompts remain unchanged except for necessary composition work.
- Action prompts do not control phase transitions.

### Slice 3: Durable findings and handoff state

- Extend the existing handoff state with findings, decisions, assumptions, and exceptions.
- Preserve repository evidence and its source.
- Include the compact dossier in each new phase session.
- Preserve unresolved findings across phase boundaries.

Verification:

- A later phase receives findings from an earlier phase.
- Resolved findings remain resolved.
- Inferences do not become verified facts during handoff.

### Slice 4: Phase outcomes and interface behavior

- Add support for completion with objections.
- Show unresolved findings during the completion action.
- Preserve user-directed exceptions.
- Keep the user as the phase-transition authority.

Verification:

- The user can complete a non-blocked phase with objections.
- The next phase receives the unresolved objections.
- A chat response cannot complete a phase.

### Slice 5: Final validation and cleanup

- Run the existing focused tests and quality checks.
- Review prompt duplication and remove unnecessary copies.
- Review new files and abstractions for clear ownership.
- Verify resume behavior for standard and adversarial runs.

## 16. Test requirements

Add the fewest tests that cover the new observable behavior and important state transitions.

At minimum, test:

1. The adversarial profile appears in the existing profile registry.
2. A planning run persists the selected profile and version.
3. A resumed run uses its stored profile, not the current setup default.
4. Every phase session receives the selected profile.
5. The prompt engine includes the common adversarial contract once.
6. Standard and adversarial profiles reuse shared phase and action prompts.
7. Unresolved findings survive a phase transition.
8. A user-directed exception survives a phase transition.
9. Completion with objections records the correct phase outcome.
10. A model response cannot complete a phase.
11. Old runs without profile metadata use the standard profile.
12. An unknown profile follows the established configuration-error path.

Prefer existing tests at the closest useful boundary. Do not test prompt wording in full. Test stable prompt fragments, composition parts, or structured inputs.

## 17. Acceptance criteria

The change is complete when all these statements are true:

- A user can select Standard or Adversarial on the existing setup page.
- <appname_here> stores the selected profile and version on the planning run.
- Each phase session uses the stored profile.
- The adversarial profile follows the contract in this specification.
- All profiles use the same workflow, phases, actions, and output contracts.
- Repository evidence, findings, decisions, and exceptions persist across phase sessions.
- The user can complete a phase with unresolved non-blocking objections.
- Mandatory constraints or an unimplementable plan can produce a blocking result.
- The interface preserves unresolved objections during phase completion.
- Existing planning runs continue with standard behavior.
- Focused tests and configured quality checks pass.
- The final diff contains no parallel planner workflow or duplicated prompt set.

## 18. Implementation constraints

- Follow the repository's existing architecture and naming.
- Extend the current prompt engine and planner owners.
- Keep domain state independent from chat transcript text when practical.
- Use one structured model for each domain concept.
- Add an interface only for a real boundary.
- Do not add speculative profile infrastructure beyond Standard and Adversarial.
- Stop and document a conflict when repository behavior contradicts this specification.

## 19. Agent completion report

When implementation is complete, report:

- The files changed and each file's responsibility
- The selected existing owners and why they were extended
- The final prompt composition order
- The persisted profile and dossier fields
- The phase-completion behavior
- The tests and quality commands that ran
- Any unavailable checks
- Any intentional departure from this specification
- Any unresolved risk or user-directed exception

---

Reviewed for ASD-STE100 alignment. The official dictionary was not available.

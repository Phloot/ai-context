# SL-08: Write and publish the approved plan

## Identity

| Field | Value |
| --- | --- |
| Slice ID | `SL-08` |
| Status | Product-approved; repository mapping required |
| Dependencies | `SL-07` |
| Acceptance criteria | `AC-016`, `AC-017`, `AC-018`, `AC-019`, `AC-023`, `AC-024`, `AC-025`, `AC-027`, `AC-028`, `AC-029`, `AC-030` |

## Outcome

Flightlog writes an approved plan set to the user's plans directory and publishes an accessible snapshot to the Agility story.

Publication can recover from partial failure without duplicate plan versions or attachments.

## Requires

- Immutable approved plan version from `SL-07`.
- Existing plans-directory resolution.
- Agility story and attachment access.
- Confirmed attachment capability.
- Renderable index and slice artifacts.
- The publication-state presentation rules in the frontend design contract.

## Produces

- Canonical local plan-set files.
- A deterministic publication manifest.
- A deterministic ZIP when supported.
- An Agility attachment or approved multiple-file fallback.
- A durable publication record.
- Retry and recovery behavior.

## Repository discovery

Before implementation, find:

- The current plans-directory resolver.
- Existing plan-file writing behavior.
- Current filename and directory conventions.
- Agility MCP attachment operations.
- Attachment lookup, metadata, and duplicate detection.
- Whether the Agility MCP can download and inspect ZIP attachments.
- Existing safe-write or temporary-file behavior.
- Tests for files and Agility attachments.

Treat ZIP readability as a required discovery result. Do not assume that a successful upload makes the archive usable by the MCP.

## Work units

### Plan rendering

**Repository path:** Resolve from the current plan artifact or Markdown owner.

Render the approved plan version into this logical structure:

```text
<plans-directory>/<story-and-plan-identity>/
├── index.md
├── slices/
│   ├── 01-<slice-name>.md
│   └── ...
└── manifest.json
```

Use repository naming conventions after inspection.

Render only approved artifact versions. Include decision and coverage information in `index.md`. Do not create one combined Markdown plan.

### Publication manifest

**Repository path:** Resolve from the publication owner.

The manifest must contain:

- Format version
- Plan-set ID
- Plan version
- Story system and story ID
- Repository identity
- Branch and base revision
- Planner version
- Approval timestamp
- Ordered file inventory
- Content hash for each file

The manifest is generated content. The user and planner do not edit it directly.

### Safe local publication

**Repository path:** Resolve from current filesystem behavior or add one focused artifact writer.

Write the complete plan into a temporary sibling location. Validate the rendered files and manifest. Then publish the directory atomically when the platform supports it.

Do not overwrite an existing approved version. Use a new version identity.

If local publication fails, record the failure and do not attempt the Agility attachment.

### Deterministic ZIP creation

**Repository path:** Keep archive creation with the publication owner.

When the Agility MCP supports archive access:

- Add `index.md` at the archive root.
- Add the `slices/` directory.
- Add `manifest.json` at the archive root.
- Use a stable file order.
- Exclude temporary files and application metadata.
- Use the approved plan version in the archive filename.
- Calculate and record the archive hash.

Equivalent approved content must produce equivalent logical archive contents. Byte-identical ZIP output is preferred when practical but is not required if ZIP metadata prevents it.

### Multiple-file fallback

**Repository path:** Use the same publication owner and Agility boundary.

If the MCP cannot inspect ZIP contents, attach:

- `index.md`
- `manifest.json`
- Each file below `slices/`

Use names that include the plan ID and version when Agility requires globally unique attachment names.

Do not generate a combined Markdown fallback.

### Agility publication boundary

**Repository path:** Resolve from the current Agility MCP adapter or service.

Publish through an idempotent operation based on:

- Story identity
- Plan-set ID
- Plan version
- Archive or manifest hash

Before upload, check for a matching successful attachment when the integration supports lookup.

Record:

- Publication attempt ID
- Artifact type
- Artifact name
- Artifact hash
- External attachment ID
- Attempt count
- Status
- Error category and message
- Created and completed timestamps

Do not create a new plan version only because attachment delivery failed.

### Publication workbench

**Repository path:** Resolve from the final-review workspace owner.

Display separate local and Agility statuses:

- Not started
- Writing local plan
- Local plan ready
- Uploading attachment
- Published
- Publication failed

Provide a retry action for a failed external publication. Do not rerun plan generation or final approval during retry.

Provide links or actions to open the local plan and view the Agility story when current application patterns support them.

Use one inline publication state region in the workbench. Do not replace the workbench with a success card or move retry behavior into chat.

## State and failure behavior

- If rendering fails, do not publish partial local content.
- If local publication succeeds and upload fails, keep the local plan and retry only the upload.
- If the response is lost after upload, reconcile by attachment identity or hash before retry.
- If an attachment with the same identity exists, record success instead of uploading a duplicate.
- If the story becomes inaccessible, preserve the approved local plan and report an external blocker.
- If the ZIP is uploadable but not readable by the MCP, use the approved multiple-file fallback.

## Tests and validation

Add or change focused tests for:

- Approved-version rendering.
- Rejection of unapproved versions.
- Local directory naming.
- Safe-write failure.
- Manifest inventory and hashes.
- Archive root structure.
- Stable archive file ordering.
- ZIP capability success.
- Multiple-file fallback.
- Successful attachment.
- Upload failure after local success.
- Retry without new plan version.
- Lost-response reconciliation.
- Duplicate attachment prevention.
- Publication status interface.
- Publication partial-failure accessibility and focus behavior.
- Validation and publication conformance to the frontend design contract.

Use an isolated temporary plans directory. Use an Agility boundary test double for focused tests.

Complete at least one environment integration test that confirms the Agility MCP can access the published content.

Slice completion evidence:

- An approved plan exists in the expected local structure.
- The manifest matches the plan files.
- The Agility MCP can access the published plan content.
- Repeating publication does not create a duplicate attachment.
- A failed upload can resume without regenerating the plan.
- The user approves the Validation and publication visual checkpoint.

## Risks and recovery

- ZIP support can differ between upload and downstream access. Verify full MCP access before selecting the ZIP path.
- Partial writes can create corrupt local plans. Use temporary output and final publication.
- Duplicate detection can fail when attachment lookup is weak. Include stable identity and hash information in names and records.
- Platform ZIP metadata can prevent byte-identical output. Validate logical file identity through the manifest.

## Non-goals

- Do not change approved plan content during rendering.
- Do not regenerate the plan during publication retry.
- Do not delete earlier approved plan versions.
- Do not publish draft or rejected slices.
- Do not create one combined Markdown attachment.

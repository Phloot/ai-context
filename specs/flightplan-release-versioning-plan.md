# Flightplan Release Versioning and What’s New Plan

## 1. Purpose

Implement a consistent release process for Flightplan. Flightplan is a local FastAPI application with a JavaScript frontend. Jenkins builds the application as a Python wheel and publishes the wheel to Artifactory.

This plan defines the following behavior:

- Assign a unique version to each published Flightplan release.
- Generate a curated changelog from small change fragments.
- Package structured release notes in the wheel.
- Show a What’s New dialog after an installed update.
- Keep version data, changelog data, and packaged release notes consistent.
- Prevent feature branches from publishing production releases.

## 2. Existing delivery workflow

The repository uses this workflow:

1. Create a feature branch from `master`.
2. Push changes to the feature branch.
3. Run Jenkins continuous integration for each push.
4. Submit the feature branch for review.
5. Merge the approved feature branch into `master`.
6. Run the Jenkins `master` pipeline after the merge.

The implementation must preserve this workflow.

## 3. Decisions

### 3.1 Version format

Use `MAJOR.MINOR.PATCH` release versions.

- Increment `MAJOR` for incompatible changes to user configuration, persisted state, command-line behavior, installer behavior, or supported integrations.
- Increment `MINOR` for backward-compatible features.
- Increment `PATCH` for backward-compatible fixes.

Use Python-compatible prerelease versions, such as `1.5.0rc1`, if prereleases become necessary.

### 3.2 Authoritative version source

Use an annotated Git tag as the authoritative release version. Use tags in the form `vMAJOR.MINOR.PATCH`, such as `v1.4.0`.

Configure the Python build to derive the wheel version from the Git tag. Prefer `setuptools-scm` unless the repository already uses a build backend with equivalent source-control version support.

Do not maintain independent version constants in Python, JavaScript, `pyproject.toml`, or the installer.

At runtime, read the installed distribution version with `importlib.metadata.version("flightplan")`. The frontend must obtain the version from the backend.

### 3.3 Release ownership

Feature-branch pipelines must validate release inputs. Feature-branch pipelines must not create release tags or publish production wheels.

The successful `master` pipeline owns release coordination. It calculates the next version, generates release files, creates the tag, builds the wheel, and publishes the wheel.

By default, a merge with a user-visible change fragment produces a release. A merge with only internal changes does not require a release.

If the team later batches several merges into one release, move the release stages to a separately triggered Jenkins release job. Keep the release mechanics unchanged.

### 3.4 Release-note source

Developers must add one small Markdown fragment for each user-visible change. The fragments are the human-authored release-note source.

Generate both `CHANGELOG.md` and the packaged `releases.json` from these fragments. Do not manually edit `releases.json`.

Use Towncrier to assemble the Markdown changelog. Use a small repository-owned Python script to validate fragments and generate the JSON release entry.

### 3.5 Mutable application state

Keep the last acknowledged release version outside the installed wheel. Use `platformdirs` to select the user-specific state directory.

Write the state file atomically. Recover safely when the file is absent or corrupt.

## 4. Change fragment format

Store pending fragments in the repository `changes/` directory.

Use this filename format:

```text
<work-item>.<type>.md
```

Example:

```text
changes/AG-14231.feature.md
```

The fragment contains a concise user-facing description. Do not add a heading or list marker.

```markdown
Added repository readiness scorecards that identify missing or outdated AI instruction files.
```

Support these fragment types:

| Suffix | Changelog section | Minimum version increment | Show in What’s New |
| --- | --- | --- | --- |
| `.breaking.md` | Breaking | Major | Yes |
| `.feature.md` | Added | Minor | Yes |
| `.change.md` | Changed | Patch | Yes |
| `.bugfix.md` | Fixed | Patch | Yes |
| `.security.md` | Security | Patch | Yes |
| `.internal.md` | Internal | None | No |

When a release contains multiple fragment types, use the highest required increment.

Examples:

```text
bugfix + feature = minor
feature + breaking = major
```

CI must reject a fragment when one of these conditions is true:

- The filename does not match the configured work-item and type format.
- The type is not supported.
- The file is empty.
- The content contains raw HTML.
- The content contains a heading.
- The content describes only implementation details.
- The description is not useful to a Flightplan user.

Allow an explicit CI exemption for changes that do not require a release note. Examples include tests, comments, and repository maintenance.

## 5. Generated release files

### 5.1 Changelog

Maintain `CHANGELOG.md` as the permanent human-readable release history. Follow the Keep a Changelog category model.

The release process must add a version and an ISO date:

```markdown
## [1.4.0] - 2026-08-14

### Added

- Added repository readiness scorecards that identify missing or outdated AI instruction files.
```

### 5.2 Packaged release data

Store the generated release data in a package resource. Adapt the path to the existing package structure.

Suggested path:

```text
src/flightplan/resources/releases.json
```

Use a versioned schema:

```json
{
  "schemaVersion": 1,
  "releases": [
    {
      "version": "1.4.0",
      "date": "2026-08-14",
      "summary": "Repository scorecards and marketplace reliability improvements.",
      "showPopup": true,
      "sections": {
        "added": [
          {
            "id": "AG-14231",
            "text": "Added repository readiness scorecards that identify missing or outdated AI instruction files."
          }
        ],
        "changed": [],
        "fixed": [],
        "security": [],
        "breaking": []
      }
    }
  ]
}
```

The `summary` field is optional. The release command can accept it as an argument. If the summary is absent, the frontend must use `What’s new in Flightplan <version>` as the title.

Set `showPopup` to `true` when the release contains at least one user-visible fragment. Set it to `false` for an internal-only release.

## 6. Release preparation command

Add a focused Python command for release preparation. Do not put release policy in the FastAPI application or Jenkinsfile.

Suggested command:

```bash
python scripts/prepare_release.py \
  --version 1.4.0 \
  --summary "Repository scorecards and marketplace reliability improvements."
```

The command must complete these operations:

1. Validate the supplied version.
2. Load all pending fragments.
3. Validate each fragment.
4. Calculate the minimum required increment.
5. Reject an insufficient supplied version.
6. Generate the new JSON release entry.
7. Update `CHANGELOG.md` through Towncrier.
8. Remove the consumed fragments.
9. Validate the generated Markdown and JSON.

The command must fail without partial output. Generate temporary outputs first. Replace tracked outputs only after all validations succeed.

Keep each responsibility separate:

- Fragment parsing owns filename and content extraction.
- Version policy owns increment calculation and validation.
- Release rendering owns Markdown and JSON generation.
- Jenkins owns repository operations and publication.
- FastAPI owns delivery of installed release information.
- The frontend owns presentation and acknowledgment actions.

Do not create generic manager or utility classes for these responsibilities.

## 7. Jenkins behavior

### 7.1 Feature-branch pipeline

For each feature-branch push, Jenkins must:

1. Run the existing tests and quality checks.
2. Validate pending change fragments.
3. Render a draft changelog without changing tracked files.
4. Build an unpublished test wheel.
5. Verify that the wheel contains the frontend assets and release resource.

The feature-branch pipeline must not:

- Create a release tag.
- Commit generated release files.
- Publish a wheel to the production Artifactory repository.

### 7.2 Master release pipeline

After a feature merge, the `master` pipeline must:

1. Ignore a release commit that this pipeline already processed.
2. Acquire an exclusive release lock.
3. Fetch all release tags.
4. Run the full test and quality suite.
5. Read the latest valid release tag.
6. Inspect all pending fragments.
7. Stop without a release when no user-visible fragment exists.
8. Calculate the next version.
9. Run `prepare_release.py`.
10. Create the release commit locally.
11. Create the annotated release tag locally.
12. Build the wheel from the tagged release commit.
13. Install the wheel in a clean environment.
14. Run smoke tests against the installed wheel.
15. Confirm that remote `master` still identifies the tested base commit.
16. Push the release commit and tag.
17. Publish the exact wheel to Artifactory.
18. Verify installation of the exact version from Artifactory.

The pipeline must not force-push. If `master` changes during a release, abort the release and run a new build.

Configure the Jenkins job to prevent concurrent `master` releases. A repository or Jenkins lock is also acceptable when multiple jobs can publish Flightplan.

Use an identifiable release commit message:

```text
chore(release): Flightplan 1.4.0
```

Do not rely only on `[skip ci]`. The pipeline must detect its own release commit and exit without creating another release.

### 7.3 Protected-master alternative

First, determine whether the Jenkins service identity can push release commits and tags under the repository protection rules.

If Jenkins cannot push a release commit to `master`, Jenkins must create a release branch or release pull request. The release branch contains the generated changelog, JSON, and fragment deletions.

After approval and merge, the next `master` pipeline must recognize the prepared release version. It must tag the merged release commit and publish the wheel.

Do not weaken branch protection to implement this feature.

### 7.4 Artifact rules

Publish immutable versioned artifacts, such as:

```text
flightplan-1.4.0-py3-none-any.whl
```

Do not overwrite a published version. Publish a new patch version for every correction.

The installer must request a version from Artifactory. The installer must not contain an independent current-version value.

## 8. Runtime application behavior

### 8.1 Installed version

Read the installed version in the backend:

```python
from importlib.metadata import version

FLIGHTPLAN_VERSION = version("flightplan")
```

Expose the installed version through an existing metadata endpoint or a focused endpoint, such as:

```http
GET /api/application-info
```

The JavaScript frontend must use this backend value. Do not duplicate the version in JavaScript.

### 8.2 What’s New state

Persist a small state document outside the wheel:

```json
{
  "schemaVersion": 1,
  "lastAcknowledgedVersion": "1.3.2"
}
```

Use `packaging.version.Version` for comparisons. Do not compare version strings directly.

### 8.3 What’s New query

Add a backend operation that returns unseen releases. The operation must select releases in this range:

```text
lastAcknowledgedVersion < releaseVersion <= installedVersion
```

Suggested endpoint:

```http
GET /api/whats-new
```

Suggested response:

```json
{
  "currentVersion": "1.4.0",
  "previousVersion": "1.3.2",
  "show": true,
  "releases": []
}
```

Return all unseen releases when a developer skips versions. Order releases from newest to oldest in the response.

### 8.4 Acknowledgment

Persist the installed version only after the frontend acknowledges the dialog:

```http
POST /api/whats-new/acknowledge
Content-Type: application/json

{"version": "1.4.0"}
```

Do not mark the release as acknowledged when the query endpoint returns data. If the browser closes before acknowledgment, show the dialog again.

Do not move `lastAcknowledgedVersion` backward after a downgrade.

### 8.5 Frontend behavior

On application initialization, the frontend must:

1. Request unseen release information.
2. Open the dialog when `show` is `true`.
3. Render structured release text without raw HTML injection.
4. Group changes by release and section.
5. Send acknowledgment after the user closes or confirms the dialog.

For a new installation with no state, show a welcome dialog with the current release highlights.

Do not show a dialog for an internal-only release.

## 9. Proposed responsibility boundaries

Adapt filenames to the established repository structure. Preserve these responsibilities:

| Proposed file or area | Responsibility | Dependency direction |
| --- | --- | --- |
| `scripts/prepare_release.py` | Coordinate deterministic release-file generation | Depends on focused release modules, not FastAPI |
| Release fragment module | Parse and validate change fragments | Independent of Jenkins and FastAPI |
| Release version module | Calculate and validate version increments | Independent of Git transport and FastAPI |
| Release rendering module | Produce changelog and JSON data | Depends on validated release data |
| `src/flightplan/resources/releases.json` | Store generated immutable release history | Consumed by backend release-note behavior |
| Application state component | Persist acknowledgment state atomically | Independent of FastAPI route models |
| Release-note component | Select unseen releases | Depends on release data and state abstractions |
| FastAPI routes | Validate HTTP input and return HTTP responses | Depends on release-note behavior |
| JavaScript dialog | Present releases and send acknowledgment | Depends on backend API only |
| Jenkins pipeline | Coordinate Git, tests, tags, and Artifactory | Invokes release preparation as a boundary command |

Do not add release preparation behavior to the application entry point. Do not add application state behavior to the Jenkinsfile.

## 10. Verification requirements

### 10.1 Release consistency

Verify these values for every release:

- Git tag: `v1.4.0`
- Wheel metadata: `1.4.0`
- Wheel filename: `flightplan-1.4.0-...whl`
- Runtime API version: `1.4.0`
- Latest JSON release entry: `1.4.0`
- Latest changelog heading: `1.4.0`

Fail the release when one value differs.

### 10.2 Release preparation tests

Test these conditions:

- A bug-fix fragment selects a patch increment.
- A feature fragment selects a minor increment.
- A breaking fragment selects a major increment.
- The highest increment wins for mixed fragments.
- An invalid filename fails validation.
- An empty fragment fails validation.
- An insufficient supplied version fails validation.
- A duplicate release version fails validation.
- A failed generation leaves tracked outputs unchanged.
- An internal-only set does not create a popup release.

### 10.3 Runtime tests

Test these conditions:

- A new installation returns the current release.
- An acknowledged version does not return again.
- A multi-version update returns all unseen releases.
- A downgrade does not lower the acknowledgment value.
- A corrupt state file recovers safely.
- An acknowledgment is written atomically.
- Version comparison handles `1.10.0` correctly after `1.9.0`.
- An internal-only release does not show the dialog.

### 10.4 Frontend tests

Test these conditions:

- The dialog opens for unseen release data.
- The dialog does not open when `show` is `false`.
- The dialog renders multiple releases and sections.
- The frontend sends acknowledgment after user confirmation.
- The frontend does not render release text as trusted HTML.

### 10.5 Jenkins tests

Verify these conditions in a safe repository or dry-run mode:

- A feature branch cannot publish a production wheel.
- A master merge calculates the expected version.
- A release commit does not create another release.
- Concurrent release attempts cannot publish the same version.
- A changed remote `master` causes a safe abort.
- An existing tag causes a safe failure.
- An existing Artifactory version causes a safe failure.
- A failed smoke test prevents tag publication and artifact publication.

## 11. Implementation sequence

Implement the work in independently testable slices.

1. Configure tag-derived package versioning.
2. Add runtime version reporting and its tests.
3. Configure fragment validation and draft changelog generation.
4. Implement deterministic JSON release generation.
5. Add generated release data to wheel package data.
6. Implement local acknowledgment state.
7. Implement unseen-release selection.
8. Add the FastAPI endpoints.
9. Add the JavaScript What’s New dialog.
10. Add feature-branch Jenkins validation.
11. Add guarded `master` release coordination.
12. Add clean-install and Artifactory smoke tests.

After each slice, run the repository-configured tests and quality commands. Review changed files for clear ownership and dependency direction.

## 12. Completion criteria

The implementation is complete when all these statements are true:

- A feature PR can add one user-facing fragment without editing release history.
- A successful `master` release calculates one valid next version.
- The tagged source can reproduce the published wheel.
- The wheel, runtime API, changelog, JSON, and tag report the same version.
- Artifactory contains one immutable artifact for the release version.
- A developer sees all unseen user-facing changes after an update.
- The dialog does not return after acknowledgment.
- The release pipeline does not create recursive releases.
- Concurrent builds cannot publish duplicate versions.
- The implementation preserves repository architecture and branch protection.

## 13. Items to confirm during repository inspection

Before implementation, inspect the repository and confirm these items:

- The current Python build backend and package layout.
- The distribution name used by `importlib.metadata`.
- The current Jenkins multibranch and publication stages.
- The repository protection rules for Jenkins commits and tags.
- The available Jenkins locking mechanism.
- The current local-state component and `platformdirs` usage.
- The existing FastAPI metadata or health endpoints.
- The existing modal and frontend state patterns.
- The Artifactory Python repository path and overwrite policy.
- The installer command and restart behavior.

Use existing repository patterns when they satisfy this plan. Do not create a second pattern for the same responsibility.

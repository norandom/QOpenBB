# Native development workflow requirements

## Project description

QOpenBB developers and agents need the existing build and end-to-end verification workflow to run from Windows without entering WSL. The owner supplies Podman Desktop, Docker Compose and native Dagger, and wants Playwright included. This migration preserves application behavior and the meaning of existing checks.

## Scope

Include native local commands, disposable service lifecycle, browser verification, build-tool compatibility, artifact storage and evidence. Preserve Linux CI and image-pull deployment. Exclude new financial features, provider calls unrelated to an approved acceptance case, VM backend changes and replacement of the test framework. Technology choices above are explicit owner constraints; detailed component design follows requirements approval.

### Requirement 1: Native execution

**Objective:** Developers can run the workflow from the repository in a normal Windows shell.

1. When a developer runs a supported local verification or build command, the workflow shall execute without invoking a WSL shell or requiring Linux-host source paths.
2. Before a job starts, the workflow shall validate its required tools and connection and identify missing or incompatible prerequisites in an actionable error.
3. If a job fails, the workflow shall return a nonzero exit code and retain the relevant diagnostic evidence.

### Requirement 2: Isolated application lifecycle

**Objective:** Compose manages disposable verification services without affecting the owner's deployment.

1. When a verification session starts, the workflow shall launch the required service images under a unique owned project with isolated persistent state and loopback-only host access.
2. Before browser verification starts, the workflow shall verify service readiness and record the actual service image identities and reachable application origin.
3. When a test requires recreation, the workflow shall recreate its owned services with the same isolated state and permit verification of retained user data.
4. When cleanup runs, the workflow shall remove only resources proven to belong to that session and preserve unrelated containers and user data.
5. If startup fails or is interrupted, the workflow shall retain useful diagnostics and expose a repeatable owned cleanup command.

### Requirement 3: Browser verification parity

**Objective:** Existing browser journeys retain their coverage in the native workflow.

1. When browser checks run, the workflow shall use an isolated headless browser and fresh contexts without attaching to the user's browser or taking desktop focus.
2. The workflow shall preserve the existing assertions for displayed values, linked parameters, save/reopen, retained state and relevant failure cases in migrated journeys.
3. When a browser check fails, the workflow shall retain sanitized console/network diagnostics and the configured failure artifacts while excluding credentials and token-entry captures.
4. The workflow shall retain the existing worker limits and application login budgets without weakening authentication or rate limits to pass tests.

### Requirement 4: Build and delivery compatibility

**Objective:** Native development remains compatible with reproducible image delivery.

1. Before accepting native image builds, the workflow shall validate and record a compatible pinned CLI, engine and SDK combination together with source and dependency identities.
2. The workflow shall keep image builds separate from verification, publication and deployment.
3. When exercising a packaged acceptance case, the workflow shall identify the exact built or pulled images rather than infer identity from mutable tags.
4. The workflow shall preserve portable Linux CI commands and the server's image-pull installation without introducing an application build at deployment time.

### Requirement 5: Storage and private configuration

**Objective:** Verification leaves controlled artifacts and protects private state.

1. Before a job starts, the workflow shall resolve its working and output paths and reject a drive root as either.
2. The workflow shall route disposable Windows caches, downloads, private test state and generated build outputs under D:/BuildArtifacts in project-specific directories while honoring configured tool cache and temporary paths.
3. The workflow shall keep Linux dependencies and build caches within the Linux filesystem and keep secrets out of tracked files, command logs and public evidence.
4. When reading or deleting private session state, the workflow shall validate its ownership and reject unsafe paths or incompatible descriptors instead of bypassing checks.
5. When creating private credentials or session descriptors, the workflow shall restrict filesystem access to the intended user and fail closed if that protection cannot be established or verified.

### Requirement 6: Bounded migration acceptance

**Objective:** The migration is reviewable without expanding the test suite unnecessarily.

1. Before marking a workflow migrated, the maintainers shall demonstrate its existing meaningful checks on the native environment and record the commands, exit codes, revisions and evidence paths.
2. The maintainers shall map migrated capabilities to their owning criteria and actual checks in the breadth map, distinguishing planned checks from executed results.
3. The maintainers shall document supported native commands, known limitations and Linux CI behavior without relabeling historical WSL evidence as native acceptance.
4. The maintainers shall independently review each implementation task and enforce the existing production size limits before accepting modified production files.

## Requirements review

Requirements gate: numeric groups, EARS criteria, observable failure behavior and explicit exclusions checked. A separate Sol review identified missing private-file access protection; criterion 5.5 addresses it. No application acceptance or implementation approval is implied. Design and executable tasks follow owner approval under the project Kiro flow.

# Requirements Document

## Introduction

The owner of QOpenBB wants to take over the open-source OpenBB Workspace environment for personal development and self-hosting. Development runs on Windows with WSL and Docker; deployment targets a private Linux server. The immediate objective is a reproducible upstream baseline using the Full Workspace variant, its application backend, the open-source OpenBB data API, Financial Modeling Prep (FMP), FRED, and the Excel add-in. Jupyter is an optional research surface.

The owner explicitly deferred a custom data integration backed by their own PostgreSQL database. This feature must establish the baseline before redesigning or extending it.

The first acceptance journey is dashboard construction using ready-made widgets backed by FMP and FRED through the owner's self-hosted open-source OpenBB data API. Both the Workspace application backend and the data API run in this setup; FMP and FRED are the external financial-data providers. Dashboard usability takes priority over optional notebooks and later custom integrations. The Full image variant is selected explicitly; enabling Full does not imply that every hosted AI or catalog service is available.

The owner selected the latest OpenBB data API as the target, with regenerated Workspace widget definitions and Excel functions and provider adaptations where needed. Pin the latest validated release at implementation time rather than tracking a mutable version. Local credentials belong in a gitignored `.env`; `.env.sample` is the public, empty-value template. FMP and FRED are required primary providers; EconDB and AI remain optional extensions.

## Boundary Context

- **In scope:** upstream acquisition and provenance, a single controlling Docker Compose configuration, local development, Dagger builds in GitHub Actions, registry publication and image-pull installation, private-server deployment, baseline persistence, FMP connectivity, Excel baseline verification with small compatibility changes, and optional Jupyter.
- **Out of scope:** custom database connectors, a PostgreSQL data warehouse, changing Workspace's database to PostgreSQL, a new data model, custom financial-model workbooks, replacement frontends, public SaaS, and rebuilding commercial OpenBB services.
- **Compatibility work in scope:** adapt the FMP provider to the latest selected data API as necessary and regenerate consumer schemas. This is separate from the deferred custom PostgreSQL integration. EconDB integration and AI runtime implementation remain optional follow-up scope.
- **Adjacent expectations:** FMP supplies external data under the owner's account; Excel runs on the user's machine. Access to Excel, FMP credentials, server access, DNS, and certificate trust are deployment inputs rather than services supplied by this project.
- **Baseline rule:** retain upstream packaging and behavior where usable. Small Excel compatibility changes are explicitly allowed for self-hosted authentication, URLs, manifest configuration, and API contracts. Preserve existing function signatures; document changes and verify workbook refresh/reopen. Do not silently replace unavailable functionality.
- **Deferred extension:** a later spec can introduce a custom PostgreSQL-backed data service through the supported data-connector interface. It must not be a prerequisite for this baseline.

## Requirements

### Requirement 1: Reproducible upstream baseline
**Objective:** As the owner, I want a recorded upstream baseline so that I can maintain my own environment.

#### Acceptance Criteria
1. When the owner acquires the baseline, the environment shall record the source repositories, exact revisions, dependency versions, and image identifiers used.
2. The environment shall retain the upstream license and notice files for imported components.
3. If a baseline component requires an unavailable package, asset, or hosted service, the setup report shall identify the dependency and the affected capability.
4. When a local adaptation is necessary, the setup report shall distinguish that adaptation from unchanged upstream behavior.

### Requirement 2: One environment control point
**Objective:** As the owner, I want one Compose entry point so that I can operate the baseline consistently.

#### Acceptance Criteria
1. When the owner follows the documented startup procedure with the required configuration, the environment shall start Workspace and the OpenBB data service from one controlling Compose file.
2. When the owner stops and restarts the environment, the environment shall retain saved Workspace state and configuration.
3. If a required component fails to start, the environment shall expose its failed status and diagnostic logs.
4. When the owner requests the optional notebook environment, the environment shall start it without requiring a replacement of the core baseline.

### Requirement 3: Windows/WSL development and private Linux deployment
**Objective:** As the owner, I want to develop locally and deploy the same baseline privately.

#### Acceptance Criteria
1. When the owner follows the development procedure on Windows with WSL Docker, the environment shall provide local access to Workspace and its data service.
2. When the owner changes a supported source component and follows its rebuild procedure, the environment shall run the rebuilt component and identify its source revision.
3. When the owner follows the private Linux deployment procedure, the environment shall use the same recorded component versions as the verified local baseline.
4. The deployment documentation shall identify environment-specific addresses, credentials, storage locations, and certificate requirements.
5. While deployed on the private server, the environment shall restrict access to the intended private network or authenticated access path.

### Requirement 4: Workspace application baseline
**Objective:** As the owner, I want the upstream Workspace experience running independently of the former hosted application.

#### Acceptance Criteria
1. When the owner completes local account setup, Workspace shall allow the owner to sign in to the self-hosted application.
2. When the owner saves a dashboard and restarts the environment, Workspace shall make that dashboard available after sign-in.
3. When the owner registers the self-hosted OpenBB data service, Workspace shall discover and display supported data widgets.
4. If an upstream capability depends on an unavailable external service, the baseline report shall identify that capability as unavailable rather than report the complete hosted product as reproduced.
5. When the owner connects the self-hosted data API, Workspace shall offer its available FMP-backed widget definitions without requiring the owner to author each widget from scratch.
6. When the owner selects available widgets, Workspace shall allow adding, arranging, resizing, and removing them in an owned dashboard.
7. When the owner saves and reopens an FMP-backed dashboard, Workspace shall retain its layout and widget parameters and allow refreshing supported data through the self-hosted API.

### Requirement 5: Open-source data API with FMP and FRED
**Objective:** As the owner, I want FMP and FRED data through a self-hosted OpenBB API so that data access does not depend on OpenBB's hosted API.

#### Acceptance Criteria
1. When the owner configures a valid FMP credential and requests a dataset supported by the installed baseline and the account entitlement, the data service shall return that dataset.
2. If the credential is missing, invalid, rate-limited, or lacks entitlement, the data service shall return an observable failure rather than fabricated or silently substituted data.
3. The environment shall keep the FMP credential out of frontend bundles, committed configuration, and notebook outputs supplied with the baseline.
4. When the owner requests the same supported dataset through Workspace and the data API with equivalent parameters, the environment shall preserve the dataset's financial values and available period, currency, and unit metadata.
5. The environment shall support the baseline data workflow without a custom database or custom data connector.
6. When the owner configures a valid FRED credential and selects a supported economic series, the data service shall return the series through the self-hosted API with its available dates, units, and frequency metadata.
7. When the owner adds a supported FRED widget to a dashboard containing FMP widgets, Workspace shall display and refresh both sources through the self-hosted API.
8. If a FRED request fails because of authentication, throttling, or unavailable data, the environment shall report the failure without silently substituting another source.
9. The environment shall keep the FRED credential out of frontend bundles, committed configuration, and notebook outputs supplied with the baseline.

### Requirement 6: Excel baseline integration
**Objective:** As the owner, I want to use the released Excel add-in with the self-hosted environment.

#### Acceptance Criteria
1. When the owner follows the documented installation procedure in a supported Excel client, Excel shall load the self-hosted add-in assets from a trusted HTTPS address.
2. When the owner signs in through the add-in, the add-in shall authenticate against the self-hosted application backend.
3. When the owner invokes a supported FMP-backed function, the add-in shall retrieve the corresponding data from the self-hosted data service.
4. When the owner reopens a validation workbook and refreshes its supported function, the add-in shall refresh the result without changing its function signature.
5. If the released add-in's authentication, endpoint paths, or response shapes are incompatible with the selected data API, the baseline report shall record the failing contract and the proposed minimal remedy before the integration is declared working.

### Requirement 7: Optional Jupyter research
**Objective:** As the owner, I want an optional notebook environment for investigating the baseline data.

#### Acceptance Criteria
1. When the owner enables Jupyter, the environment shall provide authenticated notebook access.
2. When a notebook calls a supported dataset through the self-hosted data API, the notebook shall receive data without requiring a separate FMP key embedded in the notebook.
3. When the notebook service is recreated, the environment shall retain the owner's saved notebooks.
4. When Jupyter is disabled, Workspace and Excel shall remain usable independently of it.

### Requirement 8: Recovery and baseline verification
**Objective:** As the owner, I want evidence that the baseline works and can be recovered.

#### Acceptance Criteria
1. When the owner runs the documented baseline checks, the report shall distinguish passing, failing, and untested Workspace, data API, Excel, and optional notebook capabilities.
2. When the owner follows the backup and restore procedure, the environment shall recover saved Workspace state and configuration into a clean deployment.
3. When the owner changes the pinned baseline, the environment documentation shall preserve the prior version identifiers and its recovery procedure.
4. If restoring an older application version requires an older data snapshot, the recovery procedure shall state that requirement before rollback.

### Requirement 9: Dagger build and image-pull delivery
**Objective:** As the owner, I want GitHub to build and publish the images using Dagger so that server installation only needs image pulls.

#### Acceptance Criteria
1. When a build runs locally or in GitHub Actions, the pipeline shall execute the same versioned Dagger build and verification definitions.
2. When a release passes its required checks, the pipeline shall publish the selected application images to the configured registry and record their immutable digests with source revisions.
3. If a required build or verification fails, the pipeline shall withhold release promotion and identify the failed check.
4. When the owner installs a published release on the private Linux server, the environment shall pull the recorded images and start without compiling application source on that server.
5. When the owner selects a previous release, the deployment procedure shall identify its exact image set and compatible state-backup requirements.
6. While building, testing, or publishing, the pipeline shall keep registry credentials and provider credentials out of image layers, artifacts, and logs.

### Requirement 10: Background verification and breadth traceability
**Objective:** As the owner, I want the reference project's verification conventions adapted here so that feature coverage and missing evidence remain visible.

#### Acceptance Criteria
1. When browser verification runs during development, the verification environment shall use an isolated project-owned headless browser without moving the desktop pointer, sending system keystrokes, or showing helper windows.
2. When diagnosing a browser failure, the verification workflow shall support Chrome DevTools diagnostics against the project-owned browser and preserve relevant console/network evidence without capturing credentials.
3. When an acceptance-critical browser journey is implemented, the verification workflow shall preserve a reproducible Playwright test of its actual user-visible result and relevant failure/recovery behavior.
4. When tests run concurrently, the verification workflow shall isolate their state, services, output directories, and logs and apply the bounded parallelism policy in testing.md.
5. When a feature is introduced or changed, the breadth map shall link its capability ID to the owning spec criteria, planned or implemented checks, and evidence status.
6. If a required check is missing, skipped, or failing, the verification report shall mark the affected capability unverified rather than complete.

### Requirement 11: Latest API and regenerated consumers
**Objective:** As the owner, I want the latest data API with regenerated consumers so that compatibility does not depend on freezing the environment on an obsolete API generation.

#### Acceptance Criteria
1. When the baseline version is selected, the environment shall record the latest validated OpenBB data API release and pin the complete compatible dependency set.
2. If the selected API no longer supports the released FMP provider package, the baseline shall supply a tested provider adaptation that preserves the required FMP dashboard journey.
3. When the selected API schema changes, the build workflow shall regenerate Workspace widget definitions and Excel functions from that schema and the selected widget inventory.
4. When regenerated functions differ from the prior function contract, the compatibility report shall identify changed paths, arguments, response shapes, and workbook impacts before release.
5. When regenerated artifacts are released, the verification workflow shall exercise a real FMP-backed dashboard and an Excel function against the same self-hosted API version.
6. When the owner configures local keys, the environment shall load them from an untracked `.env` while retaining an empty-value `.env.sample` in source control.
7. While building or publishing images, the workflow shall exclude the local `.env` from source contexts and image layers.

## Workspace AI provider decision

The owner selected Anthropic as the default Workspace AI provider. Store ANTHROPIC_API_KEY only in the local gitignored .env and inject it into the future self-hosted agent service. The model and agent integration remain pending design; dashboard/data access must work independently of AI. A configured credential is not evidence of working AI.

## Review status

Requirements reviewed inline against the local EARS and requirements-review-gate rules: numeric identifiers, observable acceptance criteria, core journeys, error cases, and inclusion/exclusion boundaries checked. Docker Compose, Windows/WSL, Linux, Excel, FMP, and Jupyter are user-requested constraints. Internal service decomposition remains a proposal in research.md.

Core product/tech/structure steering files do not yet exist. testing.md and ci.md adapt the reference project's conventions at the user's explicit request. Human requirements approval is pending. Design, tasks, and runtime implementation are not approved. User amendments added Requirements 9–11, dashboard editing criteria, and explicit permission for Excel/provider compatibility work.

# QOpenBB documentation

Use QOpenBB to work toward a private financial-data workspace with reproducible sources and observable data contracts. The immediate engineering problem is proving that Full Workspace, the latest selected OpenBB API, and FMP/FRED work together. Direct provider access alone does not answer that question.

## Choose your next action

| If you need to... | Read |
| --- | --- |
| Understand the intended financial workflow and its limits | [Goals](goals.md) |
| Find the next dependency gate | [Roadmap](roadmap.md) and [implementation tasks](../.kiro/specs/openbb-self-service/tasks.md) |
| See the path from accepted chart modules to the original application experience | [Completion plan](completion-plan.md) |
| Review the existing-backend persistence repair | [SQLite query design](../.kiro/specs/openbb-self-service/sqlite-repair-design.md) |
| Reproduce SQLite query and storage checks | [SQLite verification](../.kiro/specs/openbb-self-service/sqlite-repair-verification.md) |
| Set up the pinned development tools | [Development toolchain](development.md) |
| Check maintained code size and explicit fork scope | [Complexity checks](complexity.md) |
| Validate source, release and acceptance records | [Evidence contracts](evidence.md) |
| Inspect selected-service inputs and build-source exclusions | [Runtime and source contracts](runtime-contracts.md) |
| Run isolated fixture browser and API checks | [Verification infrastructure](verification.md) |
| Inspect the foundation image workflow and its evidence limits | [Image builds](image-builds.md) |
| Restore the locked data runtime and inspect FRED semantics | [Data runtime](data-runtime.md) |
| Inspect the restored FMP package and installed discovery checks | [FMP adaptation](fmp-adaptation.md) |
| Rebuild the provisional Full frontend from frozen inputs | [Workspace frontend packaging](workspace-build.md) |
| Assess what has actually been tested | [Feasibility report](../.kiro/specs/openbb-self-service/feasibility.md) and [breadth map](../.kiro/breadth.toml) |
| Browse committed screenshots, fixtures and verification records | [Reviewed artifacts](../artifacts/reviewed/README.md) |
| Review acceptance criteria or approve the next phase | [Requirements](../.kiro/specs/openbb-self-service/requirements.md) and [phase status](../.kiro/specs/openbb-self-service/spec.json) |
| Review service contracts, file ownership and acceptance gates | [Technical design](../.kiro/specs/openbb-self-service/design.md) |
| Understand proposed services and compatibility risks | [Research](../.kiro/specs/openbb-self-service/research.md) and [Full versus Lite](../.kiro/specs/openbb-self-service/lite-vs-full.md) |
| Inspect acquired sources, package compatibility and asset constraints | [Compatibility](compatibility.md) and [licenses](licenses.md) |
| Decide the open-source chart and table baseline | [Replacement assessment](chart-replacement-assessment.md) |
| Track features that the renderer replacement must preserve | [Renderer parity audit](renderer-parity-audit.md) |
| Inspect original chart types, controls, flags and required checks | [Renderer capability matrix](renderer-capability-matrix.md) |
| Understand original saved chart settings and the next adapter boundary | [Original option findings](../.kiro/specs/openbb-self-service/chart-option-discovery.md) |
| Review the explicit chart appearance contract | [Explicit appearance design](../.kiro/specs/openbb-self-service/chart-appearance-design.md) |
| Review the next real Workspace chart journey and outstanding contracts | [Application integration draft](../.kiro/specs/openbb-self-service/chart-application-integration-design.md) |
| Inspect original grid selection, range and chart-state inputs | [Grid range source contract](../.kiro/specs/openbb-self-service/chart-grid-range-contract.md) |
| Check explicit appearance implementation and browser evidence | [Appearance verification](../.kiro/specs/openbb-self-service/chart-appearance-verification.md) |
| Inspect original line, title and marker observations | [Line appearance findings](../.kiro/specs/openbb-self-service/chart-line-appearance-findings.md) |
| Check original option-state implementation evidence | [Option-state verification](../.kiro/specs/openbb-self-service/chart-option-state-verification.md) |
| Inspect remaining effective chart styling contracts | [Effective-style discovery](../.kiro/specs/openbb-self-service/chart-effective-style-discovery.md) |
| Inspect observed original dark-theme defaults | [Resolved-theme findings](../.kiro/specs/openbb-self-service/chart-theme-runtime-findings.md) |
| Inspect original light/dark defaults for the three initial chart families | [Stock theme matrix](../.kiro/specs/openbb-self-service/chart-theme-matrix-findings.md) |
| Inspect saved custom palettes and background inheritance | [Custom-theme findings](../.kiro/specs/openbb-self-service/chart-custom-theme-findings.md) |
| Check original numeric, fiscal-date and tooltip formatting rules | [Formatting contract](../.kiro/specs/openbb-self-service/chart-format-control-contract.md) |
| Inspect nested-editor discovery results and remaining gates | [Editor runtime ledger](../.kiro/specs/openbb-self-service/chart-editor-runtime-contract.md) |
| Review the renderer compatibility investigation and parallel work | [Discovery plan](../.kiro/specs/openbb-self-service/parity-plan.md) and [research](../.kiro/specs/openbb-self-service/parity-research.md) |
| Check what the renderer probes actually established | [Discovery results](../.kiro/specs/openbb-self-service/parity-findings.md) |
| Compare original and candidate widget controls | [Paired widget findings](../.kiro/specs/openbb-self-service/parity-widget-findings.md) |
| Inspect the selected ECharts integration boundary and remaining gaps | [ECharts findings](../.kiro/specs/openbb-self-service/echarts-findings.md) |
| Review the proposed chart adapter and original editor scope | [Integration proposal](../.kiro/specs/openbb-self-service/echarts-integration-proposal.md) and [editor contract](../.kiro/specs/openbb-self-service/echarts-editor-contract.md) |
| Review the next isolated chart mapping boundary | [Snapshot design](../.kiro/specs/openbb-self-service/chart-snapshot-design.md) and [grid/SQLite findings](../.kiro/specs/openbb-self-service/chart-next-discovery.md) |
| Verify the isolated ECharts dependency, host and mappings | [Chart foundation](chart-foundation.md) and [snapshot verification](../.kiro/specs/openbb-self-service/chart-snapshot-verification.md) |
| Contribute code, comments, evidence, or documentation | [Contribution guide](contributing.md) |

## Understand the proposed system

| Component | Intended responsibility |
| --- | --- |
| Full Workspace | Dashboard UI, application authentication, saved state, bundled application backend |
| Self-hosted OpenBB data API | Provider requests, financial-data responses, generated widget metadata |
| Anthropic agent | Workspace discovery and streamed answers using selected dashboard data |
| Excel add-in | Functions and authentication adapted to the accepted self-hosted contracts |
| Existing Workspace nginx | One HTTP origin with verified routing to the services |

FMP and FRED remain external providers. Workspace application authentication, data API access, and Cloudflare Access are separate contracts. The owner already manages Cloudflare infrastructure; application and Office behavior through that boundary still require acceptance tests.

The service arrangement and paths in the [Compose proposal](../.kiro/specs/openbb-self-service/compose.proposed.yaml) are proposals. There is no accepted runtime or installation runbook yet. The [README](../README.md#check-the-proposal-syntax) contains the available parser check.

## Find the authoritative detail

Requirements own acceptance criteria. Research and feasibility reports own source findings and experimental evidence. [sources.lock.json](../sources.lock.json) owns acquired revisions; it is not a release manifest. The [breadth map](../.kiro/breadth.toml) connects capabilities to requirements, planned checks, actual test paths, and evidence status.

Project rules live in [AGENTS.md](../AGENTS.md) and steering: [documentation](../.kiro/steering/documentation.md), [complexity](../.kiro/steering/complexity.md), [testing](../.kiro/steering/testing.md), [CI and delivery](../.kiro/steering/ci.md), and [delegation](../.kiro/steering/delegation.md). These pages explain the work; they do not replace the specification or approve its next phase.

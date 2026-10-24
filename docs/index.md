# QOpenBB documentation

Deploy the prototype next, then extend its provider coverage and analyst workflows. Start with the delivery status to see what is implemented, what has been verified and what still prevents release.

## Choose your next action

| Your task | Start here |
| --- | --- |
| Install prebuilt alpha images for development | [Installation guide](install.md) |
| Configure optional remote access | [Tips and Tricks](tips-and-tricks.md) |
| Understand the purpose and operating boundaries | [Goals](goals.md) |
| See the sequence and owning specifications | [Roadmap](roadmap.md) |
| Build, verify and prepare the prototype for installation | [Prototype delivery](prototype-delivery.md) |
| Map FMP, FRED and Yahoo coverage to research needs | [Provider coverage](provider-coverage.md) |
| Check renderer responsibilities and done/todo lists | [ECharts](echarts-status.md), [FINOS Perspective](perspective-status.md) and [Plotly](plotly-status.md) |
| Check which capabilities have actual evidence | [Breadth map](../.kiro/breadth.toml) and [reviewed artifacts](../artifacts/reviewed/README.md) |
| Set up development or contribute | [Development](development.md) and [contribution guide](contributing.md) |
| Keep verification focused and artifacts manageable | [Verification](verification.md) and [artifact retention](artifact-retention.md) |
| Review automated security analysis | [CodeQL coverage and status](security-scanning.md) |

## Current deployment boundary

The prototype combines Full Workspace and the self-hosted OpenBB data API in [root Compose](../compose.yaml). It serves HTTP on port 23003 behind owner-managed Cloudflare Access and cloudflared, with relative bind-mounted state. Dagger builds images; portable commands handle verification and publication. Development installs pull prebuilt latest images; each release manifest also records immutable references.

The [development alpha](https://github.com/norandom/QOpenBB/releases/tag/alpha-40086673952-1) is published with public prebuilt images. Selected candidate-image chart journeys, including Radar Line/Area, are accepted; public image identities and six anonymous pulls are verified separately in the [Radar release evidence](../artifacts/reviewed/chart-radar/verification.md#published-radar-alpha). Assembled Compose and owner-server acceptance remain open. Later stable releases will use pinned versions. [Prototype delivery](prototype-delivery.md) tracks those gates. The older Compose proposal and historical UI plans are reference material, not current installation instructions.

Broader FMP/FRED/Yahoo coverage belongs to market-data-integrations. Reusable widgets, linked research context, commands, theme and renderer completion belong to analyst-workspace. AI, Excel and custom sources have separate specs. Dashboard persistence acceptance is part of the analyst spec; infrastructure recovery verification is deferred. See [spec ownership](../.kiro/spec-ownership.toml) for transferred obligations.

## Technical reference and historical evidence

Earlier findings remain available to explain implementation decisions and reproduce checks. Their next-step language reflects the work at that time. The [agile delivery amendment](../.kiro/steering/delivery-workflow.md) and [current roadmap](roadmap.md) govern sequencing.

<details>
<summary>Browse implementation records and technical guides</summary>

| If you need to... | Read |
| --- | --- |
| Understand the intended financial workflow and its limits | [Goals](goals.md) |
| Map provider coverage to research widgets, commands and linked time views | [Provider coverage](provider-coverage.md) and [widget requirements](../.kiro/specs/openbb-self-service/parameterized-widget-requirements.md) |
| Find the next dependency gate | [Roadmap](roadmap.md) and [implementation tasks](../.kiro/specs/openbb-self-service/tasks.md) |
| Check prototype packaging, CI and remaining release gates | [Prototype delivery](prototype-delivery.md) |
| Track concrete production changes needed for the original UI | [UI parity worklist](../.kiro/specs/openbb-self-service/ui-parity-worklist.md) |
| See the path from accepted chart modules to the original application experience | [Completion plan](completion-plan.md) |
| Inspect the latest original chart appearance and editor contracts | [Runtime findings and next boundary](../.kiro/specs/openbb-self-service/chart-runtime-next-plan.md#appearance-and-editor-follow-up-2026-10-17) |
| Review the next appearance and tooltip implementation boundary | [Appearance/editor design amendment](../.kiro/specs/openbb-self-service/chart-appearance-editor-integration-design.md) |
| Verify saved appearance, derived colors and tooltip state contracts | [Appearance source verification](../.kiro/specs/openbb-self-service/chart-appearance-source-verification.md) |
| Locate the contracts still needed for the original chart/editor journey | [Consuming integration readiness](../.kiro/specs/openbb-self-service/chart-consuming-integration-readiness.md) |
| Inspect concrete appearance/session handoffs and their remaining gates | [Consuming contract draft](../.kiro/specs/openbb-self-service/chart-consuming-contract-draft.md) |
| Check original axis stroke, grid width and dash behavior | [Axis/grid findings](../.kiro/specs/openbb-self-service/chart-axis-grid-findings.md) |
| Reproduce editor close/reopen, theme changes and table return | [UI navigation findings](../.kiro/specs/openbb-self-service/chart-ui-navigation-findings.md) |
| Preserve independent captions, Weight choices and chart padding | [Caption and padding findings](../.kiro/specs/openbb-self-service/chart-caption-padding-findings.md) |
| Preserve color-picker alpha, keyboard behavior and Series Shadow | [Color and Shadow findings](../.kiro/specs/openbb-self-service/chart-color-shadow-findings.md) |
| Review axis controls, type-transition resets and unchanged time-format rendering | [Axis-control findings](../.kiro/specs/openbb-self-service/chart-axis-control-findings.md) |
| Review tooltip content, missing-value behavior and unresolved picked ownership | [Tooltip invocation findings](../.kiro/specs/openbb-self-service/chart-tooltip-invocation-findings.md) |
| Prepare the remaining Legend capture with reviewed measurement limits | [Legend capture plan](../.kiro/specs/openbb-self-service/chart-legend-capture-plan.md) |
| Separate tab resets from chart-family and saved-range changes | [Family navigation plan](../.kiro/specs/openbb-self-service/chart-family-navigation-plan.md) |
| Review the existing-backend persistence repair | [SQLite query design](../.kiro/specs/openbb-self-service/sqlite-repair-design.md) |
| Reproduce SQLite query and storage checks | [SQLite verification](../.kiro/specs/openbb-self-service/sqlite-repair-verification.md) |
| Set up the pinned development tools | [Development toolchain](development.md) |
| Check maintained code size and explicit fork scope | [Complexity checks](complexity.md) |
| Validate source, release and acceptance records | [Evidence contracts](evidence.md) |
| Keep development checks and committed evidence compact | [Artifact retention](artifact-retention.md) |
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
| Review the latest original-runtime captures and next adapter boundary | [Runtime contracts and next steps](../.kiro/specs/openbb-self-service/chart-runtime-next-plan.md) |
| Verify ordinary displayed-grid financial capture | [Grid-capture verification](../.kiro/specs/openbb-self-service/chart-grid-capture-verification.md) |
| Review source-safe chart helpers and remaining runtime joins | [Application helper verification](../.kiro/specs/openbb-self-service/chart-application-source-verification.md) |
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

</details>

## Find the authoritative detail

Requirements own acceptance criteria; spec.json records approval state. Research and verification records describe findings for their stated revisions. [sources.lock.json](../sources.lock.json) pins acquired source revisions, not a published release. The [breadth map](../.kiro/breadth.toml) connects capabilities to criteria, actual test paths and evidence; planned checks do not count as passing tests.

Project rules live in [AGENTS.md](../AGENTS.md) and steering: [documentation](../.kiro/steering/documentation.md), [complexity](../.kiro/steering/complexity.md), [testing](../.kiro/steering/testing.md), [CI](../.kiro/steering/ci.md), [delivery workflow](../.kiro/steering/delivery-workflow.md) and [delegation](../.kiro/steering/delegation.md).

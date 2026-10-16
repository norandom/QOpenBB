# QOpenBB documentation

Use QOpenBB to work toward a private financial-data workspace with reproducible sources and observable data contracts. The immediate engineering problem is proving that Full Workspace, the latest selected OpenBB API, and FMP/FRED work together. Direct provider access alone does not answer that question.

## Choose your next action

| If you need to... | Read |
| --- | --- |
| Understand the intended financial workflow and its limits | [Goals](goals.md) |
| Find the next dependency gate | [Roadmap](roadmap.md) |
| Assess what has actually been tested | [Feasibility report](../.kiro/specs/openbb-self-service/feasibility.md) and [breadth map](../.kiro/breadth.toml) |
| Review acceptance criteria or approve the next phase | [Requirements](../.kiro/specs/openbb-self-service/requirements.md) and [phase status](../.kiro/specs/openbb-self-service/spec.json) |
| Review service contracts, file ownership and acceptance gates | [Technical design](../.kiro/specs/openbb-self-service/design.md) |
| Understand proposed services and compatibility risks | [Research](../.kiro/specs/openbb-self-service/research.md) and [Full versus Lite](../.kiro/specs/openbb-self-service/lite-vs-full.md) |
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

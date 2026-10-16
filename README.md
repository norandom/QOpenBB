# QOpenBB

QOpenBB aims to give financial engineers a self-hosted Full OpenBB Workspace: build dashboards from FMP and FRED data, keep layouts and state under local control, then use Anthropic AI and Excel against the same data API.

The repository currently contains approved requirements and design, an approved implementation task plan, source pins, and feasibility research. Foundation tasks are accepted, including protected tooling, verification and Dagger source-image export. The Full frontend builds from frozen inputs; private bootstrap and session request isolation are verified. Installed FMP profile/income routes and failure handling pass fixture checks against core 2.0.1. Single-origin routing and the locked FMP/FRED runtime pass fixture verification. The provisional Full image now builds, loads and passes independent health/login/private-state checks. The identified data image also passes offline route, readiness and package-origin checks. The Community table boundary and generated three-dataset catalog are accepted. Commercial renderer removal is accepted after independent source, dependency and build review. The standalone Perspective runtime is accepted on isolated browser evidence; financial widget binding is next; no deployable application release is accepted. Start with the [documentation index](docs/index.md), [goals](docs/goals.md), and [roadmap](docs/roadmap.md).

## Current evidence

Direct read-only provider checks returned HTTP 200 for FMP company profile and income statement data and FRED GDP. Anthropic model discovery also returned HTTP 200; inference remains untested. These checks establish limited upstream access, not working Workspace widgets, a compatible OpenBB provider, or a working agent. See the [feasibility report](.kiro/specs/openbb-self-service/feasibility.md) for scope and remaining gaps.

The latest API target requires compatibility work: OpenBB 5 / core 2 excludes the released FMP provider, whose dependency constraint requires core below 2. The maintained FMP profile/income adaptation and provisional Full image packaging are accepted on their recorded checks. Integrated dashboards, live-provider fidelity and release verification remain pending. [Source pins](sources.lock.json) record acquisition snapshots, not validated releases.

## Intended operating contract

- Develop on Windows/WSL Docker and deploy the same Compose topology on a private Linux server.
- Serve plain HTTP at `0.0.0.0:23003`. The owner manages Cloudflare Access and the tunnel for `https://qbb.hanse-hedge.fund`.
- Bind persistent state under `./data`, initially `./data/workspace` to `/data`; use no Docker-managed data volumes.
- Use Dagger only for image builds. Portable repository commands verify and publish; GitHub Actions runs them now, with a later move to Gitea Actions in mind. Deploy by pulling recorded image digests.
- Accept the Full dashboard and FMP/FRED journey first, then Anthropic. Excel implementation waits for Anthropic acceptance.

Jupyter is managed separately. Custom PostgreSQL integration remains deferred.

## Sources and decisions

| Resource | Use |
| --- | --- |
| [Workspace fork](https://github.com/norandom/openbb-workspace) | Frontend, application backend, Full packaging, Excel source |
| [Data API fork](https://github.com/norandom/openbb-data-api) | OpenBB data API and provider adaptation |
| [Requirements](.kiro/specs/openbb-self-service/requirements.md) | Observable acceptance criteria and scope |
| [Research](.kiro/specs/openbb-self-service/research.md) | Source references and proposed integration contracts |
| [Technical design](.kiro/specs/openbb-self-service/design.md) | Approved service contracts, file boundaries and acceptance strategy |
| [Implementation tasks](.kiro/specs/openbb-self-service/tasks.md) | Bounded tasks with exclusive lanes, complexity caps and acceptance joins |
| [Phase status](.kiro/specs/openbb-self-service/spec.json) | Tasks approved; Workspace and data adaptation in progress |
| [Contribution guide](docs/contributing.md) | Evidence, documentation, and code-comment conventions |

Real credentials belong only in the ignored `.env`. The public [.env.sample](.env.sample) has empty values. Never include secrets in builds, images, browser assets, reports, or logs.

## Check the proposal syntax

From this repository root:

```powershell
docker compose --project-directory . --env-file .kiro/specs/openbb-self-service/compose.validation.env -f .kiro/specs/openbb-self-service/compose.proposed.yaml --profile excel config --quiet
```

This command checks the [Compose proposal](.kiro/specs/openbb-self-service/compose.proposed.yaml) with fake fixture values. It does not build or start the application. Requirements, design and tasks are approved. Implementation follows the reviewed task graph with independent review and fresh verification at each acceptance gate.

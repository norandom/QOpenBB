# QOpenBB

A self-hosted research workspace for financial engineers. Build on OpenBB, use FMP as the primary research source, and bring FRED, Yahoo Finance and later custom data into consistent analytical views.

**Available: [development alpha](https://github.com/norandom/QOpenBB/releases/tag/alpha-39415813584-1) with public prebuilt `latest` images.** Provider expansion, the Bloomberg-inspired analyst workspace, AI and Excel have separate specs so they do not hold up this release.

[![Image build and checks](https://github.com/norandom/QOpenBB/actions/workflows/prototype.yml/badge.svg?branch=main)](https://github.com/norandom/QOpenBB/actions/workflows/prototype.yml)

[![Alpha channel](https://img.shields.io/badge/channel-alpha-orange)](docs/install.md) [![Development image tag](https://img.shields.io/badge/dev_images-latest-blue)](docs/install.md) [![Stable images](https://img.shields.io/badge/stable_images-planned-lightgrey)](docs/roadmap.md)

[Install](docs/install.md) · [Documentation](docs/index.md) · [Roadmap](docs/roadmap.md) · [Delivery status](docs/prototype-delivery.md) · [Provider coverage](docs/provider-coverage.md) · [Breadth evidence](.kiro/breadth.toml)

## Status at a glance

Snapshot: 2026-10-20. Follow the CI link for live run status; a green check does not establish deployment acceptance.

| Area | What exists | What remains |
| --- | --- | --- |
| Prototype | Full Workspace, installed data API, two-service Compose, local image builds | Candidate login/dashboard and routing smoke; assembled Compose acceptance |
| CI/CD | Hosted checks and both Dagger builds passed; public images and tagged alpha published | Later stable release pinning and broader runtime acceptance |
| Data | Adapted FMP profile/income routes and FRED series catalog; real-data snapshot dashboard | Broader live FMP coverage, Yahoo adapter, named discovery and consistent provider contracts |
| Visuals | Selected ECharts table-chart journeys, including accepted combination charts with captured FMP data; existing Plotly; Perspective runtime foundation | Perspective dashboard integration, remaining renderer/table functions and shared theme |
| Analyst workflow | Existing dashboard editor and widget foundations | Familiar commands, linked instruments/time, reusable research views and persistence acceptance |
| Extensions | Separate AI, Excel and custom-source specs | Implementation and end-to-end acceptance; Quant plugins later |

Current [combination-chart milestone](.kiro/specs/analyst-workspace/chart-port-milestone.md):

- [x] Accept Column & Line, Area & Column and Custom Combination, including distinct axes and editor controls.
- [x] Verify captured FMP values, save/reopen/export and navigator/theme/refresh retention in the packaged image.
- [x] Publish and verify the updated alpha images, including anonymous pulls of both services.

See the [ECharts checklist](docs/echarts-status.md) for remaining chart families and callers.

Next: [scatter and bubble](.kiro/specs/analyst-workspace/xy-chart-milestone.md).

- [x] Implement and review the inactive X/Y/size field-assignment contract.
- [ ] Connect rendering and editor controls, accept real-FMP application behavior and publish the completed milestone.

## Delivery plan

![Delivery plan: prebuilt alpha, Compose installation, provider coverage and analyst workflows; separate AI-to-Excel lane and later extensions.](docs/assets/delivery-plan.svg)

The diagram shows delivery sequence and the Anthropic-before-Excel dependency, not completed work. Separate workstreams are not alpha release prerequisites. AI is independent of prototype acceptance. Custom sources have their own spec; Quant plugins remain a later extension. Existing persistence code, tests and the `./data/workspace` bind mount stay in place. Dashboard persistence acceptance belongs to the analyst spec; infrastructure recovery verification is deferred. Neither blocks this prototype.

## One analytical experience across providers

An analyst should be able to compare an equity, a commodity and a yield curve without learning each provider's API conventions. The planned workspace uses readable instrument names, familiar commands and linked dates, with consistent tables, charts and controls. Source labels stay visible.

Consistency preserves financial meaning: a spot benchmark is different from a futures contract; a yield curve's horizontal axis is tenor, not time; a filing's publication date differs from its reporting period. The [provider map](docs/provider-coverage.md) separates published coverage from installed and verified functionality.

The [Bloomberg-inspired visual reference](https://github.com/iconicvenom/bloomberg_free) guides the future theme and widget presentation. Existing OpenBB components and our chart work remain the foundation.

## Renderer roles

| Component | Role and current boundary |
| --- | --- |
| Apache ECharts | Implemented chart engine for selected table-to-chart journeys. Full family and caller compatibility remains open. [Done / todo](docs/echarts-status.md) |
| FINOS Perspective | Installed runtime, React host and isolated verification foundation. Pivot/explorer widget integration remains work for `analyst-workspace`. [Done / todo](docs/perspective-status.md) |
| Plotly | Existing endpoint-chart renderer retained. [Done / todo](docs/plotly-status.md) |
| Highcharts | Removed dependency. Legacy Highcharts configurations are not universally translated into ECharts. |

## Operate the prototype

Development uses Windows/WSL Docker; deployment uses the same Compose topology on private Linux. The origin serves HTTP on `0.0.0.0:23003`; the owner manages Cloudflare Access and cloudflared for `qopenbb.example.com`. State uses relative bind directories, not Docker-managed data volumes.

Dagger builds images only. Portable commands run verification and publication; GitHub Actions is the current runner, with Gitea portability retained. Development installation pulls the prebuilt `latest` alpha images; later stable releases use pinned versions. Installation uses these images and runs Compose without compiling source on the server. **The current release is the development alpha.** Use [delivery status](docs/prototype-delivery.md) for the remaining gates rather than treating the historical Compose proposal as an installation guide.

Credentials belong in ignored `.env`; [.env.sample](.env.sample) contains public placeholders. Jupyter is managed separately.

## Find the owning workstream

| Workstream | Scope |
| --- | --- |
| [Prototype delivery](.kiro/specs/openbb-self-service/spec.json) | Current baseline, CI/CD, image publication and installation |
| [Market data](.kiro/specs/market-data-integrations/requirements.md) | FMP horizontal coverage, FRED, Yahoo and future provider adapters |
| [Analyst workspace](.kiro/specs/analyst-workspace/requirements.md) | Reusable widgets, command line, linked context, theme, renderer completion and saved research context |
| [Workspace AI](.kiro/specs/workspace-ai/requirements.md) | Anthropic discovery, grounding and streaming |
| [OpenBB Excel](.kiro/specs/openbb-excel/requirements.md) | Add-in and generated functions; retains the Anthropic-first dependency |
| [Custom data](.kiro/specs/custom-data-source/requirements.md) | Own datasets and later PostgreSQL |

Successor specs are initialized scopes, not completed implementations. [Spec ownership](.kiro/spec-ownership.toml) records the handover. The [breadth map](.kiro/breadth.toml) retains actual tests and evidence; the [contribution guide](docs/contributing.md) explains working conventions.

Sources are owned in the [Workspace fork](https://github.com/norandom/openbb-workspace) and [data API fork](https://github.com/norandom/openbb-data-api), with revisions in [sources.lock.json](sources.lock.json).

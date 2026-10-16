# Lite versus Full

Inspected upstream revision: `be00e95019a55d57af146919ee46b7e1a4859226`, 2026-10-16. This compares the two variants in the released Lite Docker build, not historical hosted subscription tiers. Findings are source-level; no running image was verified.

| Area | Lite variant | Full variant |
| --- | --- | --- |
| Container structure | Workspace SPA + FastAPI application backend + Redis + nginx | Same packaging and backend build |
| Default application storage | SQLite and persistent `/data` | Same default; Full does not imply PostgreSQL |
| Configuration | Strict profile locks many frontend settings into the bundle; changing those requires a rebuild | No Lite lock profile; a broader runtime config renderer exposes those settings |
| Table-generated charts | Column/bar (grouped/stacked), horizontal bar (grouped/stacked), line, scatter, bubble, pie, doughnut, stacked area, histogram, column-line combo | Same shared chart-menu code; no Full-only chart types found there |
| Plotly chart widgets | Shared renderer supports backend-provided figures | Same renderer; data/figure endpoints still required |
| TradingView Advanced Charts | Excluded by the default frontend build | Also excluded by default; Full does not turn on the separate build flag |
| Hosted TradingView widgets | Remain available according to frontend README; external dependency | Same |
| Chart-generation control | Operator-configurable; runtime default on | Operator-configurable; runtime default on |
| Basic Copilot UI and AI enhancements | Configurable; runtime renderer defaults on, OpenBB-hosted Copilot defaults off | Configurable; similar defaults; backend/services still required |
| AI web search, SEC filings, Jina, documentation links, custom-key UI | Locked off | Configurable; supplied Full defaults on. UI availability does not supply the supporting service |
| Registration and password-reset UI | Locked off | Configurable, default off; needs compatible backend/email setup |
| Google/Microsoft/Okta configuration | Locked empty/off | Exposed in runtime config, empty/off by default; setup still required |
| Branding/theme | Fixed Lite branding and dark default in lock profile | Runtime-configurable branding/theme |
| Help/documentation and organization controls | Several controls locked off | Exposed; some enabled in Full defaults |
| `packageDataEnabled` | Locked false | Configurable, default true; this flag is not a grant of data access |
| HTML/JS widgets and MCP companion/default server | Configurable in Lite; runtime defaults on | Configurable; runtime defaults on |
| Telemetry, email, Nixtla, Cloudflare integrations | Locked off in Lite profile | Configurable, default off; infrastructure not supplied by a toggle |
| FMP and other data feeds | Separate data API/provider credentials required | Same; Full does not include a free data subscription |
| Excel / Jupyter | Separate integrations | Separate integrations; Full alone does not resolve Excel auth compatibility |

## Interpretation for QOpenBB

Decision, 2026-10-16: the owner selected **Full**. Build the upstream image with `OPENBB_IMAGE_VARIANT=full`; retain the same combined packaging. FMP and FRED are the required first data sources through the self-hosted API.

Lite is sufficient to evaluate baseline dashboards and the shared chart menu. Full is useful when the owner wants configuration flexibility without rebuilding the lock profile. Both can be built by the same Dagger workflow using the existing `OPENBB_IMAGE_VARIANT` build argument. Do not create parallel implementations of the frontend/backend just to support variants.

The default chart menu is a stronger statement than arbitrary library support: although chart utility code mentions heatmaps, waterfall, treemap and other families, that does not prove they are selectable in the standard menu. Do not advertise those as Full-only features. Third-party chart dependencies/assets need their own distribution and build verification; a root open-source license does not establish the behavior of a clean deployment.

Runtime defaults matter: Lite's frontend.env sets some fallback flags off, but render-frontend-config.sh writes config.js on startup with different defaults. The table uses runtime defaults where applicable.

## Evidence

- [Shared Dockerfile and variant selection](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/Dockerfile)
- [Lite locked profile](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/config-profiles/lite.locked.json)
- [Lite runtime renderer](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/render-frontend-config.sh)
- [Full runtime renderer](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/render-frontend-config.full.sh)
- [Table chart menu](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/src/components/General/Table/AgGridUtils.tsx)
- [Plotly renderer](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/src/components/Charting/PlotlyChart.tsx)
- [TradingView build behavior](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/README.md)

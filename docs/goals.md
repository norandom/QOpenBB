# Goals

Deploy the current QOpenBB prototype next so financial engineers can use the existing Full Workspace and installed data API. Prove authentication, supported widget use, service routing, visible failures and image identity against the candidate images. Broader provider coverage and the analyst experience follow in separate deliveries.

## Outcomes and ownership

| Goal | Observable result | Owner |
| --- | --- | --- |
| Operate the prototype | Authenticate, discover supported widgets, fetch supported data and diagnose failures in the assembled services | [openbb-self-service](../.kiro/specs/openbb-self-service/requirements.md) |
| Broaden financial data | Use FMP as the broad primary provider, yfinance for price gaps and FRED for economic series through consistent controls with labeled provenance | [market-data-integrations](../.kiro/specs/market-data-integrations/requirements.md) |
| Preserve research context | Reopen dashboard layouts, parameters, instruments, linked time ranges and group memberships after container recreation | [analyst-workspace](../.kiro/specs/analyst-workspace/requirements.md) |
| Make analysis consistent | Use reusable widgets, commands and linked instrument/time views with a Bloomberg-inspired theme built on existing work | [analyst-workspace](../.kiro/specs/analyst-workspace/requirements.md) |
| Add Workspace AI | Ground streamed Anthropic responses in selected data and recover from failures while dashboards remain usable | [workspace-ai](../.kiro/specs/workspace-ai/requirements.md) |
| Reuse the API in Excel | Authenticate, run supported functions and refresh after reopening a workbook, after Anthropic acceptance | [openbb-excel](../.kiro/specs/openbb-excel/requirements.md) |
| Add owned datasets | Integrate own sources, with PostgreSQL as later work | [custom-data-source](../.kiro/specs/custom-data-source/requirements.md) |

Persistence acceptance belongs to analyst-workspace. Infrastructure backup/restore and rollback verification remain deferred delivery obligations. Keep the configured bind mount and existing implementation and regressions; deferred acceptance is not a pass. Quant plugins remain later work.

## Financial meaning and analytical tools

A successful HTTP response proves transport and limited account access. Each exercised financial journey also needs a dataset comparison with its provider, endpoint, parameters, observation period and available metadata. Preserve nulls, currency, units, dates and frequency; identify derived values and provider provenance. Provider choice should preserve a consistent interaction pattern, while availability and entitlement limits remain visible.

ECharts supports integrated table charts for selected chart families. Perspective 5.6 packages, a runtime host and isolated tests exist, but production dashboard binding remains open. Plotly widgets remain supported. Highcharts has been removed; this does not establish universal ECharts replacement or full visual parity. Remaining renderer behavior belongs to analyst-workspace and does not block the prototype. See the [roadmap](roadmap.md) for the delivery boundary.

## Operating boundaries

Development uses Windows/WSL with the same service topology on private Linux. The target exposes HTTP on `0.0.0.0:23003`; the owner manages cloudflared at `https://qbb.hanse-hedge.fund`. State uses relative bind directories under `./data`. Dagger builds images. Portable repository commands own verification and publication; GitHub Actions remains replaceable by Gitea Actions. The server pulls immutable images without compiling application source.

Jupyter, notebook images, wheel distribution, custom financial-model workbooks and commercial-service recreation are outside the prototype. Installed adapters do not imply access to every former hosted catalog, premium widget or ready-made dashboard. EconDB is optional follow-up work.

## Evidence needed for release

The prototype is not ready if authentication, supported widget data, service routing, visible failure handling or candidate image identity fails or remains untested. Direct-provider probes and Compose parsing cannot establish the integrated journey. The [breadth map](../.kiro/breadth.toml) records actual checks and evidence; the [roadmap](roadmap.md) separates prototype acceptance from successor work.

# Goals

The first useful outcome is a saved financial dashboard that can refresh FMP and FRED data through the owner's OpenBB API after a restart. Full Workspace is the selected baseline. Anthropic and Excel extend that workflow only after its data and persistence contracts hold.

## Outcomes to prove

| Goal | Observable result | Owning requirements |
| --- | --- | --- |
| Build an owned dashboard | Discover supported widgets, add and arrange them, save, reopen after restart, and refresh | 2, 4 |
| Preserve financial meaning | Equivalent API and widget requests preserve values and available period, currency, unit, date, and frequency metadata | 5 |
| Make failures diagnosable | Missing credentials, entitlement limits, throttling, and unavailable data produce visible failures without fabricated or silently substituted results | 5, 8 |
| Add useful Workspace AI | Discover the agent and receive a streamed Anthropic response using selected dashboard data; recover from failures while dashboards remain usable | 12 |
| Reuse the accepted API in Excel | Load trusted add-in assets, authenticate, run a supported FMP function, and refresh after reopening a workbook | 6, 11 |
| Reproduce and recover the environment | Build from recorded fork revisions, publish immutable images, pull them on Linux, and restore saved state into a clean deployment | 1, 3, 8, 9 |

See the [requirements](../.kiro/specs/openbb-self-service/requirements.md) for the full criteria. Excel implementation is blocked until Anthropic acceptance.

## Financial-data boundaries

A successful HTTP response proves transport and limited account access. Acceptance also requires checking the returned dataset and its presentation. For each exercised financial journey, record the provider, endpoint, parameters, observation period, available metadata, and comparison result. Do not treat a missing value as zero or silently change period, currency, or units to make a chart look complete.

The baseline uses datasets supported by the selected API and the owner's provider entitlements. Full packaging does not establish access to every former hosted catalog, premium widget, or ready-made dashboard. API-discovered widgets must be checked against real supported data.

## Operating boundaries

The target uses Windows/WSL for development and the same service topology on private Linux. It exposes plain HTTP on `0.0.0.0:23003`; the owner supplies the public Cloudflare Access tunnel at `https://qbb.hanse-hedge.fund`. State stays in bind directories under `./data`. Dagger owns builds, checks, and publication; the server pulls images without compiling application source.

Jupyter, notebook images, wheel distribution, custom financial-model workbooks, and commercial-service recreation are outside this baseline. Custom PostgreSQL data integration is deferred to a later specification. EconDB is optional follow-up work.

## What would disprove readiness

The baseline is not ready if a dashboard cannot retain its layout and parameters, if widget data differs materially from the equivalent API response, or if restore cannot recover saved state. Passing direct-provider probes or a Compose parser cannot override a failed or untested user journey. The [roadmap](roadmap.md) and [breadth map](../.kiro/breadth.toml) keep those gates visible.

# Company Research: reuse and remaining input gaps

2026-11-06. Read-only source and acceptance review for IA-A. The next deliverable is an input-readiness decision, followed by an approved quarterly/peer dashboard contract. No new live requests, browser runs, calculations or builds were performed for this research.

## Reuse the published foundation

The [initial provider batch](../../../artifacts/reviewed/financial-input-milestone/accepted.md) is accepted and published, 26/26 tasks. [Company selection](../../../docs/company-selection.md) is accepted and published, 10/10 tasks. The owner confirmed the latest alpha's Linux update, retained dashboards and working autocomplete on 2026-11-06; that report is separate from independent local verification.

The current [catalog](../../../contracts/widgets.json) contains eleven native table definitions:

| Dataset | Reusable input | Remaining readiness question |
| --- | --- | --- |
| Profile | Names, identifiers, exchange, currency, market capitalization and last price | Price/share timing and issuer versus listing identity |
| Income | Revenue, earnings, EPS and weighted-average shares | Discrete-quarter duration and cross-company period alignment |
| Balance | Debt, cash, working-capital balances, minority/lease fields | Comparable quarterly instants and missing claims |
| Cash flow | Operating cash flow, capex, working-capital changes and provider free cash flow | Quarter versus cumulative basis, signs and provider definitions |
| Search | Name/symbol lookup and source-qualified listings | Reuse accepted selector; do not create another search mechanism |
| Peers | Provider candidate names/identifiers and descriptive fields | Analyst rationale and full fundamentals for the selected sample |
| Daily prices | OHLCV with dates and explicit adjustment convention | Match the intended valuation date and share basis |
| Key metrics | Provider ratios, working capital, ROIC and other metrics | Calculation windows and comparability remain provider limitations |
| Ratios | Provider profitability, valuation, leverage and cash-flow ratios | Period, denominator and calculation-basis consistency |
| Enterprise values | Price, shares, capitalization, debt, cash and provider EV | Dates, share basis and a complete bridge are not established |
| FRED series | Generic series observations and metadata | DGS10 is one Treasury benchmark, not a yield curve or issuer cost |

The [live record](../../../artifacts/reviewed/market-live-financial-inputs/accepted.md) covers eleven datasets with fifteen checks and 291 selected field comparisons. Its [query receipt](../../../docs/reference/live-financial-acceptance.json) is narrower than a completed quarterly or peer analysis: MSFT Income has annual and quarter queries; Balance, Cash, Metrics, Ratios and EV have annual queries. AAPL/GOOGL profiles and MSFT peer suggestions do not establish a verified peer financial-history matrix. January 2025 daily prices and DGS10 observations retain their recorded windows; they are not current-account access evidence.

## Keep the existing App and group mechanism

[App definitions](../../../contracts/apps.json) currently supply the QOpenBB starter and FRED App. The starter places eleven tables in a Data tab; this is not the curated Company Research App.

Workspace source was checked at the owned pin `f832a5593223b1e702970c4de8eceda87a17fa5b`, data API at `28423762e8cc3faae978e770899834b41e7cde99`. App schema, template creation, user-App persistence and App-export source are unchanged from the previously inspected Workspace `c652b909` baseline. Reuse their existing layouts, widget definitions, groups and saved state.

The selector binds eight immediate FMP definitions: Profile, Income, Balance, Cash, Prices, Metrics, Ratios and EV. Search, Peers and FRED are intentionally outside that binding. [Packaged acceptance](../../../artifacts/reviewed/company-selector/20261106-acceptance-review.md) establishes Profile/Income linking and independent comparison/FRED preservation, plus saved identity through fresh login and retained-container recreation. It does not certify all eleven complete widget journeys.

Two consumer gaps need explicit later design treatment:

- Financial metadata is available in `extra.results_metadata.__qopenbb_financial__`; [packaged Income acceptance](../../../artifacts/reviewed/market-packaged-financial/accepted.md) adds no financial metadata pane. IA2's full metric inspection remains open.
- Dashboard persistence retains `widget.storage.companySelection`, but the App export storage allowlist does not include it. Export/import of a new research App needs a focused identity check; accepted dashboard reopening does not prove template round-trip behavior.

The Windows vendor Workspace checkout remains at the older `c652b909` baseline. The source review used the authoritative WSL checkout at the locked `f832a559` pin. Future implementation must reconcile the actual checkout identity before making changes; no source pin changed during this research.

## Preserve the financial boundary

Provider metrics retain their supplied definitions and unknown calculation conventions. No quarter-from-YTD, cash-conversion formula, EBITDA adjustment, peer aggregation, EV reconciliation or DCF sensitivity is introduced by this slice. The [separate financial-modeling specification](../financial-modeling/brief.md) owns house methods; its runtime/repository remain queued.

FMP DCF/custom-DCF integration, actual entitlement, response fields and customization behavior remain unverified. The next assessment must distinguish source availability, documentation, observed access and usable assumptions. A blocked or unsupported result can settle a feasibility question; it does not create a valuation feature. This research makes no new claim about the provider's current external offering.

## Next decision

Review the [bounded requirements](research-input-requirements.md), then approve the verification design and tasks. Reuse existing provider/service/catalog checks and `tests/e2e/financial-workspace.spec.mts` where behavior changes. No new harness or infrastructure project is proposed. Any later production changes retain the 400 physical lines/file, 300 logical units/file and 50/function caps, inventory/checker enforcement and independent review.

The proposal is disproved if existing evidence already establishes the missing peer-period/valuation semantics, or if a required field cannot be used under its recorded convention. In either case, update the gap record before approving dashboard scope. IA-A and IA-B remain unchecked until their own evidence passes.

## Design discovery and synthesis, 2026-11-06

The owner approved the bounded requirements. Kiro light discovery applies because this is an extension of verification with no new runtime or dependencies. The design uses the approved input-readiness scope, documentation/complexity/testing/CI/delegation steering, the COBESY conclusion-first and evidence-boundary rules, and the existing house-finance separation. Core `product.md`, `tech.md` and `structure.md` remain absent; the available steering and approved contracts supply context.

**Reuse:** the current live suite calls the installed application through the existing in-process ASGI fixture; no listening service is necessary. It already captures original source callbacks, validates installed models/metadata and checks source/API equality. Annual/quarter queries for the six financial families accept bounded row counts; they do not provide fiscal-date filtering or completeness. Preserve original test node IDs. Dispatch new semantic checks by dataset, not suffixed case name, because current exact-ID dispatch would miss added company/period cases. Added field comparisons must retain missing-versus-null, source ordinals, current/legacy alias precedence and explicit date/year normalization.

**Simplification:** use a fixed MSFT/ORCL/ADBE verification sample, the existing pytest environment and one static assessment. Candidate rationale and business/fiscal differences belong in that assessment; they are not an approved comparables methodology. No provider, schema framework, model engine, Polars acquisition dependency, new browser harness or additional service is needed. The proposed test-only case table separates data from assertions without introducing a second request/capture implementation.

**DCF source finding:** no DCF implementation is present in the inspected current API tree or retained FMP 1.6.1 archive. The exact retained archive hash is `5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517`. This finding does not cover every historical OpenBB release. Generic `get_data_many` transport accepts a complete stable URL, typed errors, provenance, explicit GET, timeout and an API-key header; the legacy URL builder does not construct stable paths. Its proposed call is source-compatible, not execution-verified.

Official [standard DCF](https://site.financialmodelingprep.com/developer/docs/stable/dcf-advanced), [custom DCF](https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced) and [authorization](https://site.financialmodelingprep.com/developer/docs) pages were browsed on 2026-11-06. They document the stable paths and named custom inputs, including beta; no key or account API request was used. Missing currency, valuation dates, financial conventions and response assumptions remain missing. Custom forecast year is not valuation date. Use at most three primary-company probes (standard, default custom, one documented beta binding), retaining observed access and integration as separate dimensions. No local DCF or sensitivity is computed.

**FRED:** retain earlier DGS10 evidence with its actual acquisition and observation dates rather than rerun it merely to update a timestamp. The [official series page](https://fred.stlouisfed.org/series/DGS10), checked on 2026-11-06, supplies benchmark attribution; the installed API's `source=fred` does not by itself establish the underlying release provenance. Any new access claim needs a separately recorded request.

The integration risks are silent skipped assertions, false quarter comparability, source/API normalization mistaken for raw equality, leaked query credentials, and a direct DCF success mistaken for a native widget. The bounded design addresses each through explicit dataset dispatch, semantic findings, normalized-comparison labels, sanitized receipts and native/direct observation kinds. Reuse existing test-only capture and safe failure handling; strict total/time limits need enforcement, not just policy text. No tests or builds ran during design discovery.

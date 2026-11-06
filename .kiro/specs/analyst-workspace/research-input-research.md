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

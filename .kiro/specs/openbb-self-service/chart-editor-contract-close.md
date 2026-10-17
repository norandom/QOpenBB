# Finite tooltip and Set Up contracts

The fresh original runtime closes three specific gaps left by [the nested editor capture](chart-editor-runtime-next.md): exact tooltip modes and visible content, complete numerical transpose/restoration, and settled Sum bar geometry. Full editor, application and renderer acceptance remain blocked by the remaining capability matrix. No implementation task or phase approval is changed.

Evidence dated 2026-10-17 uses original source `38dffc33389aca0e4a87e0e88d42f7067aa220df` and unchanged image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Candidate reference `76edf85a46298f7bc5212ff9944e4b66e9baa4af` was not run. [Report](../../../artifacts/reviewed/parity/editor-contract-close/report.md), [events](../../../artifacts/reviewed/parity/editor-contract-close/event-ledger.json), [30 assertions](../../../artifacts/reviewed/parity/editor-contract-close/verification.json) and [rendered pixel check](../../../artifacts/reviewed/parity/editor-contract-close/pixel-verification.json) own the evidence.

## Observed contract

| Original control | Exact model | Effective / rendered result |
| --- | --- | --- |
| Single tooltip | `bar.tooltip.mode = "single"` in chartOptions | Root effective single; Q1 and Revenue 100 appear for the first bar. |
| Multiple tooltip | `bar.tooltip.mode = "shared"` | Root effective shared; Q1 Revenue 100 and Operating Income 20 both appear. |
| Compact tooltip | `bar.tooltip.mode = "compact"` | Root effective compact; Revenue 100 appears without Q1 heading. |
| Switch Category / Series on | Root flag true | Categories Revenue and Operating Income (USD millions), wrapper IDs 0 and 1; `period:0..3` values [100,120,140,160] and [20,25,30,40]. Four y bindings preserve duplicate Q1 observation identities. |
| Switch off | Root flag false | Original four ordered rows and revenue/operatingIncome bindings restore. |
| Aggregate on/off | Root `aggFunc = "sum"`, then omitted | Q1 100+120=220 and 20+25=45; off restores four observations. Settled six-bar heights match reference values and raster pixels within two pixels in this fixture. |

Tooltip mode belongs to the chart-level family patch, not series.tooltip. Keep UI label Multiple distinct from the stored value shared. Events, model, effective data and visible hover content were separately captured. `waitForUpdate` plus an explicit 1.5-second wait preceded Sum geometry/screenshot capture. The first projection failed on a finite category wrapper; its evidence and successful owned cleanup remain preserved. A fresh corrective runtime then completed seven edits with no action failures, exited 0 and removed its container, state and credentials.

## Proposed next bounded contract

The existing session/reducer should own grouped-column tooltip edits and the captured finite transpose transformation, keeping original namespaces, explicit descriptor identities, original restoration order and existing UI controls. ECharts public tooltip APIs must reproduce the observed single/shared/compact content. The reference geometry/internal chart projection is evidence only and cannot enter production. Scope inventory/checker enforcement and the 400 physical lines/file, 300 logical units/file, 50/function limits apply to future production files. This is a candidate design boundary for independent review, not approval to implement or activate it.

Still unverified: aggregate functions beyond Sum, remaining nested fields and conditional controls, general range/reorder, other families, light/detached/forecast and keyboard paths, candidate visuals/interaction, backend save/reopen/restart. One outgoing final compact-tooltip POST is not backend readback. Original datafeed errors and onboarding-info 404 remain. Requirements 4.8/4.9 continue to prohibit hidden, disabled or inert substitutions; these findings do not narrow the full parity obligation.

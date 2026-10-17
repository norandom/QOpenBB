# Editor tooltip and numerical closure

Seven original UI edits now establish all three tooltip modes, complete category/series transpose and restoration, and settled Sum geometry for this dark grouped-column fixture. This is bounded discovery, not candidate parity or full lane C acceptance.

Observed 2026-10-17 against owned original source `38dffc33389aca0e4a87e0e88d42f7067aa220df`, unchanged Full image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Candidate reference is `76edf85a46298f7bc5212ff9944e4b66e9baa4af`; no candidate runtime was tested. [Fixture](fixture.json) supplies synthetic financials in USD millions; duplicate Q1 rows intentionally distinguish aggregation from observations. Existing table -> chart -> external Chart settings entry points opened the original editor at 1440 by 1000.

## Observed contract

| UI | Original patch / model | Effective and visible outcome |
| --- | --- | --- |
| Tooltip Single | `chartOptions.bar.tooltip.mode = "single"` | Effective root `tooltip.mode = "single"`; hover shows `2024-Q1 Revenue (USD millions) 100`. |
| Tooltip Multiple | `chartOptions.bar.tooltip.mode = "shared"` | Effective root shared; same bar hover adds `Operating Income (USD millions) 20`. |
| Tooltip Compact | `chartOptions.bar.tooltip.mode = "compact"` | Effective root compact; hover shows `Revenue (USD millions) 100`, without the Q1 heading. |
| Aggregate on | Root `aggFunc = "sum"` | Three rows: Q1 220/45, Q3 140/30, Q4 160/40. Both six-bar reference geometry and rendered pixel heights match, after `waitForUpdate` plus 1.5 seconds. |
| Aggregate off | `aggFunc` removed | Four ordered observations restored, including Q1 100/20 and Q1 120/25. |
| Switch Category / Series on | Root `switchCategorySeries = true` | Two category rows with wrapper IDs 0/1, values Revenue/Operating Income (USD millions). `period:0..3` hold [100,120,140,160] and [20,25,30,40]. Four series bind those keys; duplicated Q1 series names remain distinct. |
| Switch off | Root flag false | Original four rows and two numerical series restore. |

[Event ledger](event-ledger.json), [tooltip hover DOM](tooltip-Multiple-hover.json), [transpose projection](setup-Switch-Category-Series-on.json), [Sum geometry](setup-Aggregate-on-geometry.json) and [pixel verification](pixel-verification.json) separate UI actions, event payloads, model patches, numerical data and rendered results. Geometry uses finite original-reference internal projections only; production must use public ECharts APIs. No recursive private-object inspector or arbitrary serialized callback invocation is used.

The Sum screenshot shows bars against a 0..250 axis, with Q1 Revenue at 220 and Operating Income at 45. The offline pixel check independently locates six solid-color bars in the fixed synthetic plot crop and tests height/value scaling and common baseline within two pixels. This fixture-specific pixel check does not certify other chart dimensions or themes.

## Reproduction and failures

Run `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-close/run.sh`. It uses pinned Node 24.22.0, existing Playwright dependencies and an owned headless browser/CDP context. No install or image build was performed. Startup checks image digest and source label, creates a fresh container/port/state/account, and cleanup removes only recorded owned state. [Run statuses](journey-status.json) and [cleanup](cleanup-report.json) record exit 0 and container/state/credential absence.

Attempt 1 failed at the transpose projection because its synthetic category uses an `{id,value,toString}` wrapper rather than a scalar. [Preserved failure](attempt1/journey.log) and cleanup status remain. The corrective run projects only scalar id/value fields and does not call toString; all seven edits passed. A separate shell wrapper around offline verification lost its exit variable after the verifier passed. The direct verifier command was rerun with exit 0; [status](verification-status.json) records both facts.

Offline command `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-close/verify.mjs` passed [30 finite assertions](verification.json). `py artifacts/parity/editor-contract-close/verify_pixels.py` exited 0. The original datafeed HTML-as-JavaScript errors and onboarding-info 404 remain in [diagnostic summary](diagnostic-summary.json). No clean-application claim is made.

One final save generated an [outgoing compact-tooltip model](outgoing-storage-projection.json). This proves a POST body, not backend readback, reopening or intermediate persistence. The fixture uses synthetic dashboard/data overlays.

## Next bounded decision

The observed grouped-column tooltip patch and finite transpose transformation can support a proposed compatibility contract using the existing session/reducer owner, explicit category/series identities and ECharts public tooltip APIs. It must preserve UI labels while mapping Multiple to stored shared, retain duplicate observation identities during transpose, restore original row order on off, and test displayed financial values. A reference-only projection must never become a production dependency. Future production ownership uses the accepted checker/inventory and caps of 400 physical lines/file, 300 logical units/file and 50/function.

Still open: other aggregate functions, nested titles/colors/shadows/remaining axes and legend controls, general range/reorder, other families, light/detached/forecast, keyboard paths, actual candidate interaction/geometry and save/reopen/restart. Sum's visible function dropdown was observed, but no additional aggregation function was exercised. No control may be hidden, disabled or made inert to narrow those obligations. This report does not approve implementation tasks.

[Publication allowlist](publication-allowlist.json) identifies completed synthetic evidence; raw credentials, runtime account/state, request metadata and unfiltered diagnostics are excluded. Installed charts source clues and hash in [source analysis](source-analysis.md) remain separate from original-runtime evidence.

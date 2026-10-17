# Original label and type observations are complete; retain two rendering findings

The one granted original-only attempt completed A05-A09 with full label restoration and intact financial values. Two source predictions were disproved: category-axis style discriminators did not carry across type changes, and the selected Time Format did not change the observed time-axis text. These are findings in the original application, not collector failures or candidate parity results. A01-A04 remain the separately accepted reference package from commit `e1c3013`; their actions were not replayed.

The attempt is [attempt-20261017T1449392-91e1b733](attempt-20261017T1449392-91e1b733/source-manifest.json), dated 2026-10-17. Its copied fifteen-file collector manifest is `ac534d3491e22ddf1873da0fa957a043cb7ee468021c2e0770fa2a887e52e9e4`, reviewed [plan](plan.md) is `1c5ceae2d8dc8f5f8f955b1d961489df89455efed3384beadff980e0e69f41d5`, and [source manifest](source-hashes.json) is `68e0c0e68fd30e3fb1547b1d313a4ef959d5eef0b28e8a4a29116d4cc56f2fa6`. Original Workspace is `38dffc33389aca0e4a87e0e88d42f7067aa220df`; executed image is `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. No candidate, provider, save/reopen, new family or light-theme run occurred.

## Label controls and restoration

| Case | Observed binding and effect | Restoration and boundary |
| --- | --- | --- |
| A05 category labels, 53.115 s | Arial, sans-serif, size 14 and Padding 17 write `label.fontFamily`, `fontSize` and `spacing` to category top/bottom branches. Input 315 gives raw/live -45 degrees and scene 5.497787143782138 radians; input 45 gives +45 degrees and 0.7853981633974483 radians. Auto Rotate on removes the manual rotation; off restores +45. | Font/size/spacing/manual rotation/Auto Rotate all restore through original UI. The final visible state is Verdana, sans-serif, size 11, spacing 11, Auto Rotate on. Formerly absent raw override fields can remain explicit. |
| A06 value labels, 75.703 s | Courier New, monospace, size 16 and Padding 23 write independently to number left/right branches. Input 330 gives raw/live -30 degrees and scene 5.759586531581287 radians. Auto Rotate on/off restores -30. Numeric labels remain 0/50/100/150/200. | Verdana, sans-serif, size 11, spacing 11, Auto Rotate off and visible manual Rotation 0 all restore. The retained explicit manual zero does not claim raw-byte identity with the initial absent/undefined rotation. |

Each role's Font menu had 20 entries and Size had 16, including the initial size 11. The complete observed menus are in [menus.json](attempt-20261017T1449392-91e1b733/menus.json). The other axis's finite style stayed unchanged during each font/size/spacing edit. Every completed transaction retained the four period identifiers and both amount series: Revenue 100/120/140/160 and Operating Income 20/25/30/40, in USD millions.

Scene geometry supports visible layout effects. Horizontal size changed seriesRect height from 251 to 248, then spacing from 248 to 242. Vertical size changed x/width from 51/513 to 59/505, then spacing to 71/493. These are chart logical coordinates from the named finite getters. Parent-space BBoxes, transforms and actual inherited `parentNode` visibility are retained; no canvas transform was inferred. Font-family requests and scene fields do not prove which installed font face supplied the glyphs. The four-label fixture does not prove automatic collision rotation. See [transaction findings](analysis-attempt-20261017T1449392-91e1b733/transaction-findings.json), [vertical rotation raster](attempt-20261017T1449392-91e1b733/019-A-A06-after-57-view18.png), and both [Horizontal](attempt-20261017T1449392-91e1b733/restoration-Horizontal.json) and [Vertical](attempt-20261017T1449392-91e1b733/restoration-Vertical.json) restoration receipts.

The earlier A05 timeout remains immutable in the older package. Completion here does not retrospectively complete it. The offline I/O benchmark and this attempt's timing support further investigation; neither isolates the earlier timeout's cause.

## Type transitions lose the retained discriminator

A07 used the frozen numeric Period fixture: UTC quarter-start milliseconds for 2024-01-01, 2024-04-01, 2024-07-01 and 2024-10-01. These are reporting-period coordinates, not financial amounts. Only the horizontal category role changed type; the vertical financial-value axis remained separate even while both axes were number.

Before the transition, horizontal spacing was 19 with Ticks on and Width 3. Number changed explicit `axes[0].type` and live x type to number, but live spacing/ticks/width became 11/off/1. The old category raw theme still contained spacing 19 and width 3 at that checkpoint; it was not applied to the new numeric role. Time retained the live defaults. Returning to Category kept 11/off/1 and the former category positional spacing/width leaves became absent. The source prediction of applied-style retention is therefore not established and is contradicted by this fixture.

Number selection emitted ordered events 27-29 while the addressed model-theme projection had no changed leaf; Time emitted 30-33; Category exit emitted 36-39. These are accumulated model projections plus distinct explicit/effective/live reads, not sparse option patches. Multiple synchronous events from one action do not imply intermediate settled engines. Numeric x tick strings became `1.70 T` through `1.74 T`: that formatting applies to epoch-millisecond coordinates, not to Revenue or Operating Income values. See [event deltas](analysis-attempt-20261017T1449392-91e1b733/event-deltas.json) and the raw event chunks in the attempt.

## Time Format changes options but leaves the captured strings unchanged

A08 inventoried all 10 Time Format options. Selecting YYYY-MM-DD wrote explicit/effective `%Y-%m-%d` at event 34; DD/MM/YYYY wrote `%d/%m/%Y` at event 35. Time Format was visible only in Time and hidden after Number/Category observations. Category exit made explicit/effective format absent.

The two live text nodes stayed unchanged across both formats: `Sun Jan 01 2023 00:00:00 GMT+0100 (Central European Standard Time)` and `Fri Jan 01 2027 00:00:00 GMT+0100 (Central European Standard Time)`. Their strings are finite scene observations, not the four reporting-quarter values. The [ISO raster](attempt-20261017T1449392-91e1b733/033-B-A08-after-102-view32.png) shows the selected YYYY-MM-DD control together with long, clipped axis text; [European raster](attempt-20261017T1449392-91e1b733/034-B-A08-after-104-view33.png) retains the same scene strings. Parts of those strings fall outside the readable plot area or under the editor. Scene presence is not a claim that every character was visible in pixels.

Diagnostics warn that `axes[0].label.format` and `axes[0].label._formatters` are unknown options and are ignored. This is consistent with the observed rendering failure, but this finite capture does not isolate all formatter/engine precedence. It does not prove all 10 formats or a correct time-domain extent. The original UI request and explicit option string are insufficient evidence of a working date formatter.

A09 used `FY24-Q1` through `FY24-Q4`. In each role's own expanded observation, Axis Type was present but hidden, while Position, Font and Size remained visible. This distinguishes the nonnumeric first datum from accepted A01's parseable-year strings. It does not generalize to empty, grouped, switched or excluded-family cases. Fresh observation DOM, rather than a reused full checkpoint's older DOM, supplies that visibility evidence.

## Verification, limits and cleanup

The [runtime verifier](analysis-attempt-20261017T1449392-91e1b733/runtime-verification.json) passed 1,296 assertions against the immutable attempt and derived findings. It checks source identities, exact financial data, ordered action/event links, fresh settled references, event-emitting-action checkpoint separation, role bindings and scene rotations, original style loss/time-text findings, conditional UI, restoration, actual output budgets and cleanup. It also checks derived axis style/label text/rotation/BBoxes against the underlying raw finite snapshots. A passed verifier means these observations are reproducible; it does not turn the recorded original rendering findings into product success.

The attempt retained 121 actions, 41 field edits, 37 full checkpoints, 37 PNGs and 39 ordered events. Event index, chunks and final counter agree without recovery. Actual retained disk, including the later outer-watchdog receipt, is 152 files and 30,005,260 bytes. Every JSON/PNG and aggregate stayed within the unchanged 2 MiB/4 MiB/160 MiB bounds, 320 files, 240 actions, 80 edits, 96 checkpoints and 64 PNGs. The finalizer reconciled its owned output prefix after cleanup/status receipts; the [actual-disk inventory](analysis-attempt-20261017T1449392-91e1b733/actual-output-inventory.json) additionally includes the outer receipt written afterward.

| Case | Elapsed | Unchanged deadline |
| --- | --- | --- |
| A05 | 53.115 s | 120 s |
| A06 | 75.703 s | 120 s |
| A07 | 27.036 s | 90 s |
| A08 | 21.735 s | 90 s |
| A09 | 9.390 s | 60 s |

The wrapper and 1080-second supervisor exited 0. The [browser cleanup](attempt-20261017T1449392-91e1b733/browser-cleanup.json) records browser/context closure and listener disposal without a close error. The [runtime cleanup](attempt-20261017T1449392-91e1b733/cleanup-report.json) and [fresh read-only absence check](analysis-attempt-20261017T1449392-91e1b733/fresh-owned-absence.json), at 14:54:25 UTC, confirm the owned container, disposable state and credential file were absent. No retry occurred. The heavy lane was released after that check.

This was not a clean-console run. The [safe diagnostic summary](analysis-attempt-20261017T1449392-91e1b733/diagnostic-summary.json) retains syntax/CDP exceptions, 404s, an onboarding tier-update 400, empty AI configuration, an openbb-light theme-list warning and the Time-axis option warnings. Diagnostics did not overflow. Internal editor scroll offsets and complete failed-asset attribution remain unmeasured. No persistence, candidate parity, other-family behavior, installed-font identity or production readiness is certified.

## Reproduce the audit without another runtime

This command reads the closed attempt and existing derived analysis, prints the result and writes no files:

```text
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/ui-parity-axis-followup/verify-runtime.mjs /mnt/d/Source/QOpenBB/artifacts/ui-parity-axis-followup/attempt-20261017T1449392-91e1b733 /mnt/d/Source/QOpenBB/artifacts/ui-parity-axis-followup/analysis-attempt-20261017T1449392-91e1b733 --read-only
```

Without `--read-only`, the verifier writes `runtime-verification.json` and `actual-output-inventory.json` only into the specified analysis directory. `analyze.mjs` similarly writes its two derived analysis files there. Neither changes the raw attempt. `verify-owned-absence.mjs` is a read-only container/filesystem check that writes a dated proof into its analysis destination. The raw attempt was closed before any analysis. Earlier offline checks remain source evidence, not extra application attempts.

The attempt-local copied `plan.md` preserves frozen bytes and its original canonical-source link base. Resolve its relative links from this package root through the [explicit relocation map](analysis-attempt-20261017T1449392-91e1b733/copied-plan-link-map.json), which identifies the canonical source and checked target for each copied-plan link. The canonical plan at this package root retains working relative links; the copied plan is not silently rewritten.

The [publication allowlist](publication-allowlist.json) selects the safe source, fixtures, finite observations/events, synthetic PNGs, reports, verification scripts and derived evidence. Raw action-ledger/diagnostic files, credentials, private runtime metadata, environment files, disposable state, logs, profiles, dependencies and images are excluded. The public ledger removes setup values and DOM and preserves their counts/status; its hash is distinct from the raw input. Independent review must inspect these exact bytes and the original findings before controller publication. Future maintained production work retains the existing inventory/checker foundation and 400 physical lines/file, 300 logical syntax units/file and 50/function limits.

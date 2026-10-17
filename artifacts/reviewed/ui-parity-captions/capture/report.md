# Original captions, Weight and padding capture

The corrected original dark `groupedColumn` capture completed all nine reviewed cases on 2026-10-17. Four captions render independently, all eight Weight bindings preserve weight and style, and asymmetric padding changes the corresponding layout side. This is original-runtime evidence for controller and independent review. It grants no candidate parity, consuming implementation, frozen-contract correction or Kiro phase approval.

The authoritative completed run is [attempt five](runs/attempt-20261017T134459Z-3656a1b9/summary.json): 164 counted UI interactions, 51 field edits, 47 before/after action records, 60 ordered options events, 100 settled snapshots and 53 synthetic screenshots. Browser journey time was 47,593 ms. Its start, journey, cleanup and run exit codes are zero. The browser closed; container, credential and disposable state were absent after cleanup. See [cleanup](runs/attempt-20261017T134459Z-3656a1b9/cleanup-report.json) and [browser closure](runs/attempt-20261017T134459Z-3656a1b9/browser-cleanup.json).

## Reproduce and inspect the evidence

- [Reviewed nine-case plan](../plan.md), SHA256 `a5194d24b08c5e222a4a4ed2d51acd637eae41c8a7689427a5610cff5da86ace`.
- [Runtime/source/fixture/harness hashes and command](runs/attempt-20261017T134459Z-3656a1b9/source-manifest.json). Startup verified image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` and Workspace source `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Candidate `ea02ec15956dee8d2c8a06825387a570757db12d` was not executed.
- [Action ledger](runs/attempt-20261017T134459Z-3656a1b9/action-ledger.json), [per-operation counters](runs/attempt-20261017T134459Z-3656a1b9/operations.json), [event/model deltas](runs/attempt-20261017T134459Z-3656a1b9/event-model-deltas.json), [menu-role matrix](runs/attempt-20261017T134459Z-3656a1b9/menu-role-matrix.json), [geometry measurements](runs/attempt-20261017T134459Z-3656a1b9/measurements.json) and [fresh verification](runs/attempt-20261017T134459Z-3656a1b9/verification.json).
- [Proposed complete publication allowlist](publication-allowlist.json). Raw logs, runtime-private receipts, credentials, state, profiles, environment files and dependency caches are excluded. The controller owns independent publication review and mirroring.

From `/mnt/d/Source/QOpenBB` in WSL, repeat the offline verifier without starting a browser or container:

```sh
CAPTURE_RUN="$PWD/artifacts/ui-parity-captions/capture/runs/attempt-20261017T134459Z-3656a1b9" artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node artifacts/ui-parity-captions/capture/analyze.mjs
```

The fresh command passed 13 assertion groups over all 100 snapshots. The verification record hashes the actual post-run analyzer; runtime scripts are separately frozen in the run's `harness/` directory. Checks cover nine cases, four zero exits, cleanup, budgets/deadlines, fixture/key identity, independent visibility, typed ancestor visibility/opacity, retained details, all eight raw/effective/scene Weight bindings, events and PNG dimensions. Node syntax checks, `bash -n`, the [projection check](offline-check.mjs) and [retained-output checks](offline-output-check.json) also passed. These evidence scripts are excluded from production size caps; future production work retains 400 physical lines/file, 300 logical units/file and 50/function with the existing inventory/checker.

## Caption independence and observed namespaces

The stock state had four unchecked toggles and hidden detail controls. Effective texts were `Title`, `Subtitle`, `Axis Title`, `Axis Title`; the corresponding raw overrides were absent. Enabling Chart Title emitted two ordered events: `bar.title.enabled=true`, then `bar.title.text="Chart Title"`. Distinctive text entry emitted a separate event. Enabling each other caption emitted one event before its separate text edit.

| Real control | Observed raw model and event namespace | Rendered result |
| --- | --- | --- |
| Chart Title | `bar.title.*` | `Financial performance` |
| Subtitle | `bar.subtitle.*` | `USD millions, 2024 quarters` |
| Horizontal Axis Title | Both `bar.axes.category.top.title.*` and `.bottom.title.*` | Bottom category title `Reporting quarter` |
| Vertical Axis Title | Both `bar.axes.number.left.title.*` and `.right.title.*` | Left number title `USD millions`, rotation `-1.5707963267948966` radians |

These observations confirm the plan's predicted namespaces for this fixture. Internal `theme.overrides`, emitted `chartOptions` and raw model overrides remain separate projections. No processed default is inserted into raw evidence.

Compare [all four on](runs/attempt-20261017T134459Z-3656a1b9/019-all-on.png) with [Chart Title off](runs/attempt-20261017T134459Z-3656a1b9/021-disable-chart-title-after.png), [Subtitle off](runs/attempt-20261017T134459Z-3656a1b9/025-disable-subtitle-after.png), [Horizontal Axis Title off](runs/attempt-20261017T134459Z-3656a1b9/029-disable-horizontal-axis-title-after.png) and [Vertical Axis Title off](runs/attempt-20261017T134459Z-3656a1b9/033-disable-vertical-axis-title-after.png). Visual inspection of these actual screenshots found only the selected caption removed; tick labels and the other three captions remained. Source text survived each disabled state and returned after enabling.

At ordinary typography, the all-on series rectangle was `(x=90, y=112, width=474, height=152)` chart units. Chart-title off changed `y` by -24 and height by +24; subtitle off changed them by -25/+25. Horizontal-title off increased height by 40. Vertical-title off changed x by -40 and width by +40. These are measured layout effects, not caption-spacing constants for other themes or dimensions. Chart padding remained 20 on every side through these toggles, matching the original integrated chart's empty toolbar behavior.

## Weight is a pair for every role

Every inventoried menu in this run offered `Predefined`, `Normal`, `Bold`, `Italic`, `Bold Italic`, initially selecting Predefined. This is an observed domain for these eight original roles, not a universal domain. Baseline effective weight was numeric `400`; style was absent. Raw caption overrides for both fields were absent. The collector retains `own`, inherited presence, kind, type and value.

| Chart Title menu choice | Observed raw/effective/scene pair |
| --- | --- |
| Normal | `"normal"`, `"normal"` |
| Bold | `"bold"`, `"normal"` |
| Italic | `"normal"`, `"italic"` |
| Bold Italic | `"bold"`, `"italic"` |
| Predefined | numeric `400`, explicit `"normal"` |

Each selection emitted two events in order, one per property. An event can repeat an already explicit style, so a changed-leaf diff may show only weight while the event count remains two. The ledger preserves both events rather than deduplicating them.

Subtitle and both axis titles independently reached `bold/italic`. The remaining observed bindings were `bar.legend.item.label.*`, `bar.series.label.*`, both category `top/bottom.label.*` branches and both number `left/right.label.*` branches. Effective options and nonempty scene selections confirm each binding; axis labels were projected only during their two named probes. Legend and series labels were projected in their own probes. The final screenshot shows both selected series' eight value labels.

The frozen [RoleTypography proposal](../../consuming-contract-freeze/appearance/proposed-types.ts) omits `fontStyle`. That gap remains open: these events and pixels require both properties. This capture does not edit the frozen shape or replace an absent style with `normal`. The final Chart Title has numeric `400` with newly explicit `normal`; retained-details recovery therefore does not claim byte-identical restoration to baseline absence.

## Asymmetric padding changes geometry

The renderer used DPR 1, a 584x346 CSS/backing canvas and a 260-pixel editor within the fixed 1440x1000 viewport. With the chosen typography and labels enabled, starting seriesRect was `(91,112,473,152)` at padding `(20,20,20,20)` in top/right/bottom/left order. The x coordinate includes axis/title/label occupancy; it does not equal left padding.

| Separate real field action | Effective padding T/R/B/L | Series rectangle x/y/w/h |
| --- | --- | --- |
| Top = 41 | 41/20/20/20 | 91/133/473/131 |
| Right = 67 | 41/67/20/20 | 91/133/426/131 |
| Bottom = 29 | 41/67/29/20 | 91/133/426/122 |
| Left = 13 | 41/67/29/13 | 84/133/433/122 |
| Right = 13 | 41/13/29/13 | 84/133/487/122 |
| Left = 67 | 41/13/29/67 | 138/133/433/122 |

Each action wrote only its expected `bar.padding.side` leaf. Compare [left 13/right 67](runs/attempt-20261017T134459Z-3656a1b9/071-padding-left-13-after.png) with [left 67/right 13](runs/attempt-20261017T134459Z-3656a1b9/075-padding-left-67-after.png): their side sum and series width are equal, while the plot shifts right by 54 units. This discriminates side binding from total-width effects. Restoring the original four values and toggling every caption off/on retained text and Weight pairs; see [final all-on screenshot](runs/attempt-20261017T134459Z-3656a1b9/100-final-all-on.png).

Every snapshot settled after `waitForUpdate`, inactive animation and two identical geometry samples at least 100 ms apart. Caption BBoxes remain labelled in their parent coordinate space. The collector uses the actual named `parentNode` link, retains each parent's identity, inherited visibility/opacity and finite transform fields, and caps chains at eight parents. Title and subtitle have two recorded parents; axis titles have four. Every projected ancestor has actual boolean visibility and finite numeric opacity. No conversion of a local BBox into canvas coordinates is implied. Measured legend bounds and matched screenshots retain its layout obstruction.

## Preserved failures and remaining scope

[Attempt notes](attempt-notes.md) diagnose all earlier captures. Attempts one and two stopped in setup; attempt three stopped on incorrect collector output accounting. Attempt four completed with exit zero but missed mandatory ancestry because it followed `parent` instead of `parentNode`; its [correction receipt](runs/attempt-20261017T133848Z-e6488b85/verification-correction.json) explicitly retracts that measurement closure. All original attempt scripts, partial safe observations, failure/overflow and cleanup receipts remain in the allowlist. No failed attempt was overwritten or promoted into the authoritative run.

The corrected final run retained 13 sanitized diagnostic entries: original HTML-as-JavaScript errors, empty AI URL warnings, onboarding information 404, tier 400 and custom light-theme registration warning. See [diagnostics](runs/attempt-20261017T134459Z-3656a1b9/diagnostics.json). These were preserved, not repaired or described as a clean console. Same-origin routing blocked external requests; no provider account, build, install, candidate renderer, owner browser or persistent owner data was used.

Light had no required discriminator and was not run. Other chart families, theme transitions, font-family/size/color menus, navigation retention, save/reopen and general source inheritance remain separate gaps. Frozen-contract amendment and any production implementation require their own controller review.

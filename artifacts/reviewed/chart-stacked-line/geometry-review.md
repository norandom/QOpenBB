# Stacked Line geometry review

2026-10-26. **Current source verdict: APPROVED for controller atomic integration.** The numerical-axis repair and requested display assertions are resolved. Controller inventory/combined caps, strict typing and joined verification remain pending; this source approval is not final SL2-A task or candidate acceptance.

## Repair re-review

Independently reread the frozen source and final focused assertions. `axisOptions` now limits raw `numberExtent` to ordinary Line, so stacked variants cannot inherit its overflowing interval. The added `applicationAxes` regression checks exact finite endpoints `-MAX_VALUE` / `MAX_VALUE` and an absent interval. Existing Area behavior is unchanged.

The focused test now invokes actual label formatters and checks raw 20, raw zero, missing, hidden and zero-denominator outputs. It checks `connectNulls` both true and false. Additional assertions cover distinct epoch-versus-transformed-Date grouping, empty-row behavior, snapshot immutability and two ECharts SVG SSR cases without NaN/Infinity. These are meaningful bounded source/engine checks; they do not prove browser topology or candidate parity.

Inspected `geometry/focused.log`: 16 tests pass after repair; jsdom canvas notices remain visible. `geometry/biome.log`: seven files checked without fixes. `geometry/caps.json` and parser results put all six whole production files within 400/300/50, with maxima 282 physical, 115 logical and 18 per function. The prior 52 normalized-bar/Area checks remain recorded. `geometry/verification.md` records expected missing-module RED and earlier 109-test GREEN; exact initial RED is described there rather than present as a separate retained log in this directory. The controller must retain execution provenance before final acceptance.

No further blocking source findings. Reviewed source hashes: helper `2360981c39398bb0402d716b67311836df3d4b4553a41fbe3a44e6d51689fc57`, axes `2dccfd5ccb51a182040c7b5df1ffe7b5f6cfb4cd44d911a9875818e8d4cfd620`, series `badec11bccdb414609a7caa7c3354249fe44ca2c208548ccc957285446b72390`. No reviewer tests were launched while the controller verification queue was occupied. Only this report was edited.

## Historical first review (resolved)

Initial verdict: REJECTED pending the numerical-axis repair and verification described below.

## Required repair

**Important:** `cartesianAxes.ts` changes `axisOptions` to run raw `numberExtent` for all line families. For admitted stacked rows `[Number.MAX_VALUE]` and `[-Number.MAX_VALUE]`, each plotted endpoint is finite, but `niceNumberExtent` overflows `max - min` and returns an infinite interval. The later `safeAreaExtent` detects its own unsafe niceness and falls back to `{min,max}`; spreading that fallback does not remove the earlier raw interval. Final axis options therefore retain `interval: Infinity`.

Keep raw `numberExtent` specific to ordinary Line; stacked variants should use their supplied derived extent and its safe niceness policy exclusively. Add a regression through `applicationAxes` asserting finite min/max and any supplied interval for this signed extreme-span example. Preserve ordinary Line and Area behavior.

## Source findings

The new helper otherwise follows the frozen input/output seam: ordinal row identity, continuous serialized keys, selected-series-first/group-row-second accumulation, raw-index preservation, stable-ID visibility, null admission, explicit empty flag and a separate derived snapshot. Signed discriminators, grouped numbers/time, normalized overflow scaling and typed unnormalized failure are implemented. New families use unfilled line series and retain line marker/legend/style behavior. No runtime admission or shared controller files were changed by A.

The helper's finite-input overflow recovery and group denominator require focused tests; the observed test source covers the main signed, duplicate ordinal/number/time, missing/zero, visibility/order and MAX_VALUE cases. Current raw-label test title exceeds its assertions: the test confirms line geometry but does not invoke the label formatter. Before A acceptance, add explicit raw label and null/hidden label assertions, plus true/false `connectMissingData` option checks, to demonstrate the promised line display behavior.

## Evidence inspected and remaining gates

Read the six A production owners, actual diff and new focused test. `geometry/regression.log` records 52 passing existing normalized-bar and Area checks. The worker parser inventory is provisional size evidence, not the controller combined gate. No heavy checks were run by this reviewer while the other lane's verification was active.

Controller must retain the actual focused RED/GREEN output, final nonmutating lint, current whole-file inventory-backed 400/300/50 evidence and strict comparison before task acceptance. Other lanes' working changes were not reviewed or edited. Only this report was written.

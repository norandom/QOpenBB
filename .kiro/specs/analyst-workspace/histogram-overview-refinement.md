# Histogram miniature appearance

The matching FMP captures show that the replacement miniature is too tall, starts left of the main plot, abbreviates its labels and inherits the main axis's rounded upper bound. Correct these within H4. Numerical histogram and lifecycle acceptance on image `a1b1486` remains valid for that image; this correction requires a new candidate.

## Evidence and decision

Original Grid bundle lines 8728-8731 set navigator height to 18, overriding the generic chart miniature height of 40. Original Charts lines 69463 and 69498 reserve that height plus spacing 10; mini-axis padding is additional. The original overview shows raw numeric labels and the full bin extent 40B to 150B, while the main chart rounds to 40B to 160B.

At matching 639px widget width, the replacement main zero baseline is about 24px higher. Its overview starts near widget X31 versus original X54. Installed ECharts `Grid.js` 689-700 confirms that `outerBoundsMode: "same"` contains labels even with `containLabel: false`. A bounded actual-engine probe with an 18px grid produced only 4.5px of plot height under `same`, versus exactly 18px under `none`. The existing helper already reserves label space, so histogram must avoid this second containment step.

Evidence: ignored `artifacts/chart-histogram/reference/navigation/report.md` and `candidate/report.md`. Both original navigation controls visibly show their respective areas. Original wheel/pan/reset effects were unproven in the bounded run; candidate gestures changed the numeric window and reset restored identical full canvas bytes. Do not describe that as verified original gesture equivalence.

## Exact ownership

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

- `echarts/histogramLayout.ts`: export the existing axis-footprint helper without changing its body. Reuse its measurement for the Y-axis side; do not duplicate text measurement.
- `echarts/cartesianNavigator.ts`: add an optional navigation-layout argument for miniature height, left/right offsets and overview outer-bounds mode. Existing callers retain their current defaults. Apply offsets consistently to slider, mask and overview grid; the main grid keeps its existing horizontal containment. Change its vertical reservation only through the selected miniature height.
- `echarts/histogramNavigator.ts`: request 18px miniature height and `outerBoundsMode: "none"`. Offset navigation by the existing Y-axis footprint on the correct side, measuring the complete native tick-label set through ECharts' public scale helper. Endpoint-only measurement is insufficient: a count domain `[0,2]` can contain wider `0.5` labels and leave a 14px alignment gap. Reuse the existing footprint helper for those values rather than duplicating font or tick-generation logic. Supply raw numeric overview labels and the first/last retained calculated-bin boundaries, including empty outer bins. Preserve the main rounded axis, full retained series and numeric navigation behavior. Empty bins keep a finite fallback.
- `application/histogramSessionProjection.ts`: pass the already calculated immutable bins from the existing mapper result to the navigator. No additional binning, aggregation or state owner.

Extend existing histogram navigator/application tests and the shared navigator regression file as needed. Tests must compare actual engine main/overview pixel bounds, 18px overview height, raw label formatting, full bin endpoints including empty outer intervals, right-side axes and finite empty recovery. Retain main-chart rounding and one calculation call. Check ordinary callers retain their defaults.

Navigation alignment measures label containment only. A native-engine probe confirms that enabled axis titles and tick lengths do not enlarge that containment. Use an immutable measurement input with those Y-axis contributions disabled; the actual rendered settings must remain unchanged. Include an enabled-title/tick case alongside fractional labels so the fixture does not conceal this distinction.

Use RED/GREEN and independent review. Every changed production file must pass the explicit inventory checker at 400 physical lines, 300 logical units and 50 units per function. Parent owns inventory, pins, docs, commits and the Dagger candidate. Repeat histogram journeys, the matching FMP miniature capture and affected prior-family image checks after correction; no source test alone closes visual acceptance.

## Source acceptance

Workspace `c1ee9ae9063531b0edd0625eacc6a2725897b5cb` is independently accepted: 40 focused actual-engine/application tests pass, no baseline-relative TypeScript diagnostics are added, and all four production files pass caps. The corrected candidate must still pass the image gates above. See [reviewed evidence](../../../artifacts/reviewed/chart-histogram/verification.md).

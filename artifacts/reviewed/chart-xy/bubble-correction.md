# Bubble range and miniature correction

The rebuilt application passes the reported bubble spread and miniature-clipping checks. Workspace `72bdc113b687f39558ac5284395b4b1252d651c0` preserves the financial observations and EPS diameter mapping. Exact axis-label density remains a separate visual difference shown to the owner.

## Finding and change

The earlier navigator pinned automatic X bounds to raw observation extrema, and zoom/reset pinned Y bounds similarly. ECharts scatter clipping checked marker centers but did not clip marker pixels, allowing the miniature's bubbles to overflow its track.

Original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` was exercised with the same captured AAPL FY2021-FY2025 FMP annual statements. Its main ranges were X 360-420 billion USD and Y 90-120 billion USD; its miniature clipped bubbles within an 18-pixel track. Separate original light-theme capture at a 381×284 canvas confirmed the Y range and clipping.

The correction reuses the existing original-compatible numeric rounding policy, preserves explicit user bounds separately from computed display bounds, retains navigation's four-observation guard, and applies an actual rectangular clip to XY miniature series. Main bubble sizes remain the saved 10-40 pixel linear EPS mapping. No provider request, financial rescaling or widget-state migration was needed.

## Source verification

- Independent Astra review approved the bounded source changes, conditional on packaged application verification.
- 36 independent focused tests passed: miniature clipping/rendering/ranges, shared navigator and XY application integration. Assertions cover actual ECharts SVG geometry, explicit bounds, reset, empty-domain recovery and unaffected series.
- Strict clipping and FMP browser-test typing passed. Expanded range typing reports only the existing `typography.ts:1` unused `@ts-expect-error`; no changed-file diagnostics.
- Combined explicit-scope complexity gate passed with no errors or violations. All five changed production files satisfy 400 physical lines, 300 logical units and 50 units per function.
- Staged whitespace checks passed; the source commit is pushed.

The first image (`8c396e72`, source `e237ee0`) passed displayed main bounds but failed miniature height: label containment reduced the requested 18-pixel track to 4.5 pixels. A diagnostic run confirmed the real clipping rectangle. The follow-up disables outer-bound label containment for this miniature, using the existing histogram layout option. Independent review and nine focused tests passed, including an actual two-grid engine regression proving 18-pixel miniature height and unchanged main geometry.

## Packaged application

Local Dagger image `sha256:02a6530a5a0a41a9450ea1acf19f3211c2a43b07a88e55f21c7972e252785ae4` runs source `72bdc11` without an overlay, at isolated loopback port 55539.

- Captured FMP journey: 1 passed in 30.5 seconds, zero retries/skips. Displayed bounds are X 360-420B and Y 90-120B. Public canvas calls establish an active 18-pixel clipping rectangle while bubble radii cross its edges. Raw coordinates, EPS diameters and units remain checked through zoom/reset, theme, refresh, save/reopen and export; exported pixels include the miniature.
- Scatter regression: 1 passed in 24.7 seconds, zero retries/skips. Shared numeric X, signed Y series, theme, refresh and reopen/export remain covered.
- Commands: `browser.sh final xy-fmp.spec.ts` and `browser.sh scatter xy-charts.spec.ts --grep 'Scatter shares'` under this record's ignored evidence directory. Both exit 0, one isolated browser worker.
- Parent inspected the final exported PNG and opened it beside the original in qView. The replacement retains denser tick labels and a different legend state from the reference; this is not a claim of exact visual parity.
- Independent Astra review accepted the bounded spread/miniature correction against the final result JSON and PNG. It retained the axis-label differences and slight main-marker edge overlap as open visual work.

The corrected chart sample is the actual application export, not a redrawn illustration. Hosted publication remains pending.

Raw source logs, original reference captures and command scripts remain in ignored `artifacts/chart-xy/spread-review/`. Original captures passed with one isolated browser worker and zero retries. Public evidence retains the relevant chart samples and this concise record.

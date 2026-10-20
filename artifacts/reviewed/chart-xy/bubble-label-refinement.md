# Bubble label refinement

The requested closer original label matching passed independent source and packaged-application review. X7 adjusts numeric tick selection and plot clipping; financial observations and explicit user bounds remain unchanged.

## Original comparison and change

The same five captured AAPL FY2021–FY2025 FMP annual statements use revenue and net income in USD, with EPS in USD/share mapped linearly to 10–40 pixel bubble diameters. No new provider request or data transformation was needed.

Original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, with legend and miniature enabled, shows X labels 380/400B at 359×284 pixels and 370/380/390/400/410B at 619×284. Both use Y 80/100/120B and sparse raw-USD miniature labels. The earlier legend-disabled comparison used Y 90–120B: legend space matters to automatic rounding. Both original reference runs passed with one isolated browser worker and no retries.

Workspace `9185c5f12aca4d12b7f731f17d57f7c252fd0452` measures available plot space and formatted label widths, retains calculated intervals, suppresses overflowing horizontal endpoint labels, and preserves the miniature's native domain while restoring raw numeric formatting. The existing XY-owned clip now contains main markers as well as miniature markers. Controls, saved option paths, coordinates and nominal diameters are unchanged.

## Source checks

- Implementer: 46 focused tests passed; independent reviewer: 41 passed. Actual ECharts fixtures use production appearance/layout at both reference widths, plus explicit bounds, rotation, clipping and navigation/reset checks.
- Targeted browser TypeScript check passed. Source typing reports only inherited `typography.ts:1` TS2578; no changed-file diagnostics.
- Explicit-scope complexity gate passed: all six production files meet 400 physical lines, 300 logical units and 50 units per function.
- The browser regression failed on the prior packaged image at the actually cropped right label: 360.68 pixels on a 359-pixel canvas. It observes canvas text bounds and clips, without changing renderer state.
- Independent source review approved the candidate build.

## Packaged application

Local Dagger image `sha256:4c7f0907ed4df0874f0053fff25d55b29317c162880749410995a2d2a18e7ecd` runs production source `9185c5f` without a source overlay on isolated port 55540. Release revision `8aeecf4c1d40a58b0be3fcdcbd3ec7c6e460e8f4` adds only the reviewed browser synchronization fix.

- Captured-FMP journey: 1 passed in 31.4 seconds. It checks actual label bounds, original-like small/wide tick density, raw miniature labels, active main/mini clips, coordinates, EPS diameters, units, theme, refresh, save/reopen and exported pixels.
- Scatter regression: 1 passed in 24.2 seconds. Signed Y series and shared numeric X retain their lifecycle behavior.
- Both runs used one isolated headless worker, zero retries/skips, and passed browser/CDP console/network assertions. Commands: `browser.sh refined xy-fmp.spec.ts` and `browser.sh scatter xy-charts.spec.ts --grep 'Scatter shares'`, both exit 0.
- The initial candidate journey completed the small-chart and export checks but failed the newly added wider-view check because the test sampled the canvas before resize settled. The reviewed test fix waits for the 619-pixel canvas before observing it; renderer code was unchanged. The complete rerun passed.
- Parent and independent reviewer inspected the matched 359×284 original/export and the 619×284 wide view. qView was opened for the matched dark comparison. The published sample is the clean export; the intermediate light screenshot contains a lingering tooltip and is excluded.

Independent Astra review accepted the bounded X7 result. The legend icon and minor spacing still differ; this is closer label matching, not full pixel parity.

Ignored evidence: `artifacts/chart-xy/label-review/`; the initial browser failure is under `artifacts/chart-xy/spread-review/browser-x7-red/`.

## Published refinement

[CI run 39476320841](https://github.com/norandom/QOpenBB/actions/runs/39476320841) passed from root `77035731fca15fb24ac26bfa91a9a4b476937cdc`. [Tagged alpha alpha-39476320841-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39476320841-1) contains Compose, the environment template and image manifest. Both images were rebuilt by Dagger. Six anonymous pulls (digest, alpha tag and latest for each service) matched the manifest's registry/configuration digests, platform and source labels.

- workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:3cd4a18e40b1dbd243671b7a5638924df5d17e6e394dfd147d4ec3b7a0dcd9e0`.
- data-api: `ghcr.io/norandom/qopenbb-data-api@sha256:4f04da112697adeec7241fad4c13a57cb2c8facb46d523544370e9013e1faa39`.

Application checks ran on the identified local candidate; CI publication and image identity were verified separately. Owner-server deployment and exact pixel parity remain unverified.

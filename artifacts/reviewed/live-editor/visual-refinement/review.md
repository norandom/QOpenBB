# Line and gallery visual refinement

The owner accepted the [refined light-theme line view](light-line-refined.png) on 2026-10-18. Line legend samples, category padding, numeric tick spacing and gallery drawings now more closely match the original Workspace reference. Existing controls and saved appearance settings remain in place. This is a bounded visual checkpoint; task 2.77 and deployment acceptance remain open.

The comparison uses the same four-quarter observations, missing second-quarter values, 1440-by-1000 viewport and approximately 864-by-411 widget as the original. The fixture title differs. Small spacing and thumbnail differences remain and were included in the owner's acceptance question.

## Changes and checks

- Gallery: local light/dark colors and line, area, pie and donut silhouettes. Independent Sol review approved the three-file scope and reran all three gallery interaction tests. Every catalog callback and existing conditional item remains available.
- Renderer: line samples replace circular legend icons, ordinal line coordinates reproduce original category edge padding, and generic linear nice ticks use 1/2/5 steps. Original data order, raw values, nulls, labels and native navigator behavior remain covered.
- Independent Astra review approved the bounded renderer change and reran 66 compatibility/geometry/lifecycle tests and 10 native action projection tests. Scoped lint passed. The default unit configuration's four text-metric failures were traced to its canvas mock; the canonical chart configuration passes. The changed production files retain the existing text measurement implementation. TypeScript reports the existing unused directive in `ds/plugins/typography.ts:1`.
- The combined complexity command passed with explicit Workspace/data API change manifests, exit 0. All seven modified production files meet 400 physical lines, 300 logical units and 50 units per callable; the largest is 237/78/21.
- Actual Workspace Playwright capture: `test visual-reference.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts`, one worker, 1/1 passed in 59.4 seconds.
- Actual Workspace join: `test application.spec.ts data-view.spec.ts` with the same config, one worker, 2/2 passed in 81.7 seconds. Checks cover representative edits, save failure/retry, fresh-session and backend-restart persistence, PNG export, table return, sorting and filter Apply/clear with rendered observations. No skips, retries, unexpected or flaky outcomes. Application diagnostics passed their assertions; the join permits the deliberate save-failure 500 and the previously recorded missing TradingView bundle 404. Capture and filter diagnostics are empty.

Raw logs and intermediate images stay local under `artifacts/live-editor/visual-comparison/` and `artifacts/live-editor/runtime/visual-refined*`. The screenshot uses synthetic data. Runtime uses the existing source-overlaid backend image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; it is not a release-image verification.

## Reviewed source identity

Workspace base: `98d05690433634ecbb5a7ed7f60269cfa4bfbd4a`, plus these reviewed files. Gallery and renderer changes retain separate ownership.

| Path within Workspace | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesian.ts` | `e39f55006ce5a3fdae4746f19907a2728d9a71a1166dc81a57e7d4f499be7a7f` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianAxes.ts` | `b7550bf5524f28748f7c292d6e98c428ffa168baf8d850d8319d5f945d1a8d8b` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianLayout.ts` | `02c47ee340be2fe8d60666aa29cacc06dbe8850396ee2947668d40b48ac3cfb4` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianSeries.ts` | `632aea5c68cf009ff8585377c3a91bbdf7e975a68f59aefbbad7625afbaea209` |
| `terminalpro/src/components/General/Table/Chart/editor/ChartTypeThumbnail.tsx` | `dc970508be88a0be5b5c1736e6b4dd52a54f8a8e92af6cae273c44fdeb3ffffc` |
| `terminalpro/src/components/General/Table/Chart/editor/chartEditorDock.css` | `efa9f572795259cf2005b77d2e0ccaa9de553f939e8d9db787fed6cd06597243` |
| `terminalpro/src/components/General/Table/Chart/editor/chartTypeGallery.css` | `9c0c82f8649a0d8eb536204ccad63b1f44345e629b84b95d1ca8d8988c29baf2` |
| `terminalpro/tests/unit/chart-compatibility/cartesian.application.test.ts` | `6688c134b227f8824b8a5cc7be57c9192b34f43d6b36244ce01c25fbd8c52959` |
| `terminalpro/tests/unit/chart-compatibility/cartesian.geometry.test.ts` | `53e34e9cf423fc8c69afa939f7b3b997fae77d385a550404c241ea2d68ac81ac` |

Owner acceptance applies to this default line view. Remaining editor branches, advanced families and release deployment are not certified by this comparison.

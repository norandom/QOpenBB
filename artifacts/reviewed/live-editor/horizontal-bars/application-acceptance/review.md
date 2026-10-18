# Ordinary horizontal bars accepted

Task 2.81 connects groupedBar and stackedBar to ordinary Table/File widgets. Independent Astra review approved the integration. The existing editor, styling, semantic option branches and Widget persistence owner remain in use. Other UI-10 families and release-image deployment remain pending.

The real dashboard journey passed 1/1 in 46.1 seconds with one isolated headless worker and CDP diagnostics. It exercised grouped/stacked label geometry, signed raw-value tooltips, distinct family series selections and restoration, physical titles, numeric-axis styling, structural axis position, return to columns, native numeric-X navigation with category rows retained, the approved horizontal overview, light/dark themes, backend save/fresh-session reopen, current PNG export and table return. Unknown/inactive settings survived. Parent and reviewer inspected the synthetic screenshots and export below.

[Light view](stacked-bar-light.png) | [Dark view](stacked-bar-dark.png) | [Overview](stacked-bar-mini.png) | [Export](saved-ordinary-observations.png)

Affected caller/session/appearance checks passed 43/43; five-file scoped Biome lint passed without fixes. The combined complexity gate includes all 16 production files touched by tasks 2.78-2.81, with no errors or violations against 400 physical / 300 logical / 50 function caps. Earlier separately reviewed lanes passed 60 renderer and 90 control checks. Compatibility TypeScript retains the existing typography TS2578; a full application compiler pass is not claimed.

The first application attempt was obstructed by the original Changelog dialog; the shared fixture now dismisses it via its Close button. The next run exposed two existing three-family guards, now amended to consume the shared horizontal contract; the formatting input type also uses that contract. Subsequent draft assertions were corrected for shared-tooltip HTML and the original numeric-category eligibility predicate. The final check retains strict diagnostics: only the existing missing TradingView bundle 404 and corresponding abort are allowed. No chart or application errors occurred in initial or reopened sessions.

Runtime: owned qopenbb-browser-f4d7fef8292f4847a4ed449e30a7ceb6, base image sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f, backend overlay 23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de (43 files), candidate source served by Vite. This is not release-image verification. The owner-approved miniature repairs the original empty/failed overview; pixel equivalence to that failure is not claimed. Original runtime-only structural-axis restore and numeric-rotation/Auto Rotate limitations remain. Save-failure, restart and aggregation evidence is reused from task 2.77 because those owners did not change.

Workspace base 3f72bc639fbe9322162c4adab90c706cefcbd0dc plus exact changes below. Local detailed evidence: horizontal-bars/join-green.log, join-lint.log, join-complexity.json, join-review.md and runtime/horizontal-join-6/browser-results.json under artifacts/live-editor. Intermediate diagnostics stay local.

| File | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/Chart/AgChartView.tsx` | `65bdc5e3854538a0b141a58c1a30c53df234549f8ceb416189e5e6122ef4aa44` |
| `terminalpro/src/components/General/Table/Chart/application/axisStructure.ts` | `98fdbd98f4c4df1c365a544189a049a6a5a0f69b6fcd73ce5401da922c0ecc44` |
| `terminalpro/src/components/General/Table/Chart/application/effectiveAppearance.ts` | `b667c767c42a5ac21a14a213435b864912307b3c0541a43f4533af86c4f556c7` |
| `terminalpro/src/components/General/Table/Chart/application/types.ts` | `a3419287f4791b22826590d8fd7949a0a75d8b86535f425a2240bb5dabd419b9` |
| `terminalpro/src/components/General/Table/Chart/caller/chartInputs.ts` | `52b42db884b1b0ade048463a873338ea932882b2c18ebb84f3b5c0dfe953391a` |
| `terminalpro/tests/e2e/live-chart/fixtures.ts` | `da5813d9c4f8e62021867dac373db1e6d5798e5a67837a7a5281e63cd379b1d1` |
| `terminalpro/tests/e2e/live-chart/horizontal-bars.spec.ts` | `7d62c158b5d3f97be7bea26317099bef9e9421b432f0b0c340014af27bd7b413` |
| `terminalpro/tests/unit/chart-application/callerHorizontalBars.test.ts` | `894a5c1a19ecdc905476ca140977f8b1c99c2c5b5ffdb26d85030cea857da3ae` |

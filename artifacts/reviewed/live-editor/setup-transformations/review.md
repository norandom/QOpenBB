# Aggregate and category/series switching checkpoint

The ordinary grouped-column chart correctly sums and averages duplicate categories, switches categories and series, and restores the original observations when both transformations are turned off. A transformed state survives a fresh application session read from the backend. No production repair was needed for this bounded journey.

The synthetic input has A=(11,3), A=(7,5), B=(-2,4), and A=(missing,missing). Sum gives A=(18,8), B=(-2,4); Average gives A=(9,4), B=(-2,4). The missing row does not inflate the average denominator. After switching, Revenue/Cost are categories and A/B are series. Actual public canvas text-anchor positions distinguish that change from an inert control that merely writes a saved flag.

## Evidence and review

- The maintained `setup-transformations.spec.ts` uses the actual Full route and existing disposable fixture. It verifies drawn values and label positions, original `aggFunc`/`switchCategorySeries` fields, a fresh-session backend read, restored controls, switching off and aggregation off, and the resulting save payload. The final off state was saved but not reopened a second time.
- Pinned Node 24.22.0 syntax checks passed for both changed test modules. Tests are exempt from production size caps; production files are unchanged.
- `node verification/node_modules/@playwright/test/cli.js test setup-transformations.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts` passed 1/1 in 20.3 seconds with one headless worker, retry 0, no skips or flaky outcomes. Raw result: `artifacts/live-editor/runtime/setup-transformations-diagnostic/browser-results.json`.
- Independent Astra review approved the assertions, financial expectations, diagnostic timeline, fresh browser report and bounded publication. This is bounded functional evidence, not full task 2.77, transport-reliability or deployment acceptance.

## Earlier cancellation remains unresolved

The first run passed initial arithmetic checks but failed strict diagnostics on one CSV request with `net::ERR_ABORTED`. Source inspection found that chart settings and save do not change the CSV query key; it did not establish the precise cancellation trigger. The follow-up run added bounded request timing and stronger orientation assertions. Both observed CSV requests finished, initial diagnostics were empty, and the reopened session had only the previously recorded missing TradingView bundle 404. No diagnostic allowlist was broadened and no production change was presented as a cancellation fix. Retain the first failure under `artifacts/live-editor/runtime/setup-transformations/` for investigation if it recurs.

The runtime remains source-overlaid rather than a verified release image. Existing Auto Rotate and structural-axis restore limitations are unchanged. No screenshot is published because this checkpoint changes verification only.

## Reviewed source identity

Workspace base `e826581bb387a0ce0e39a6a71646d53d5cab4793`, plus:

| Path within Workspace | SHA-256 |
| --- | --- |
| `terminalpro/tests/e2e/live-chart/setup-transformations.spec.ts` | `a7b5807cfcc4c69b4f8c5886c2b6decc9caf9c194896483e596eb35d59999774` |
| `terminalpro/tests/e2e/live-chart/diagnostics.ts` | `10988e1b9a222760d89414161c6ce12c4a3c516dd7025f97be0275e0e5394379` |

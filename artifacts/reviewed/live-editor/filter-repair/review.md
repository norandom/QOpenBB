# Filter restoration repair review

The ordinary-table filter now survives Apply and chart/table changes. This bounded repair is independently approved and has a passing actual Workspace browser regression. Task 2.77 remains pending closer visual matching and coverage of remaining branches; this evidence does not establish full editor parity.

On 2026-10-18, the browser reproduced Category Contains B returning all three rows after Apply. Filter/sort notifications incremented the display revision; sanitizing grid options on every render created new definition objects, causing `newColumnsLoaded` to restore saved state before AG Grid's deferred state update persisted the new filter.

The repair memoizes sanitized column definitions, default column definitions and nested grid options by their caller identities. Genuine definition changes still invalidate the memo. Replacement applies only to keys already present in the original sanitized options: omitted local defaults must preserve the global Apply, Clear, Reset and Cancel actions. Existing restoration and persistence handlers retain ownership.

## Verification and review

- Focused RED tests reproduced definition identity churn and the empty-local-default override. The latter guards the global filter-action contract exposed by actual browser verification.
- Pinned Node 24.22.0: `node node_modules/vitest/vitest.mjs run --config tests/unit/communityBoundary.config.mjs` passed 24/24 tests, exit 0. Independent read-only Biome lint and scoped `git diff --check` passed.
- Independent size measurement passed: 282 physical lines, 114 logical units, largest callable 20, against caps of 400/300/50. The controller's combined complexity check passed with explicit workspace and data API change manifests.
- `node verification/node_modules/@playwright/test/cli.js test data-view.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts` passed 1/1 tests in 52.0 seconds with one worker, no skips, retries or unexpected results. The real journey verifies descending C/B/A order, Apply retaining B after reopening the filter, chart category B with observations 20 and 8, table return, and clearing the filter to restore C/B/A. Application console/network diagnostics passed the journey's assertions. Raw results remain local at `artifacts/live-editor/runtime/data-view-green/browser-results.json`.
- A fresh independent reviewer approved the revised production repair and unit regression after independently rerunning tests, lint and size checks. The same independent reviewer also approved the supporting browser regression source and inspected the completed 1/1 browser report and its empty application-error, HTTP-failure, console-error and request-failure diagnostics.

## Reviewed source identity

Workspace base: `180da6ed94ab65ad3ce4c28f4849dab85ea0e38b`, plus these uncommitted reviewed files (SHA-256):

| File under `vendor/workspace/terminalpro/` | SHA-256 |
| --- | --- |
| `src/components/General/Table/hooks/useTableContext.tsx` | `14dd3b79332187a5c7a9212b519b36264a9f0a06e2317d3c4f808d4554a315a6` |
| `tests/unit/communityMount.test.tsx` | `bc59d9b25661edf0c6bb46611b414968c57043717e9bf95de039f662d2dc6844` |
| `tests/e2e/live-chart/data-view.spec.ts` | `11a6e711a7968639c062846f84d9df6c323404be72d5a34f53efd0e384369f45` |
| `tests/e2e/live-chart/journey.ts` | `d8e4f68fd49d1f9a9d21722a95245803df73b078849c3d769217438f04202f60` |
| `tests/e2e/live-chart/visual-reference.spec.ts` | `3a853baad60fec7d040517f688bf01359d2870a6e35989b6ae516b027b959995` |

The [filtered chart](filtered-chart.png) shows the retained B-only data. Raw RED logs and intermediate browser artifacts are not publication inputs.

## Visible differences and owner direction

The additional `visual-reference.spec.ts` run passed in 15.4 seconds using the original four-quarter fixture, light theme, Chart tab and an 864-by-410 widget (original approximately 864-by-411). Its [comparison capture](light-line-before-parity-fix.png) is evidence of the current appearance, not visual acceptance. The owner compared it with the original `artifacts/reviewed/parity/theme-matrix/light-line-stable.png` and requested closer matching of legend samples, axis spacing/padding and gallery drawings on 2026-10-18. Those repairs remain separate work.

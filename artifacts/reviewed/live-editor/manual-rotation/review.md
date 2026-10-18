# Manual category-label rotation checkpoint

Manual 45-degree rotation works in the ordinary chart editor for grouped column, stacked column and line charts. The actual application check confirms the drawn label angle and the original saved leaves. Line rotation remains effective after a fresh session and backend restart. No production repair was needed.

The existing browser journey now turns Auto Rotate off, enters 45, and observes the public canvas transform when category labels A/B/C are drawn. It resets observations between families and reads the persisted bar/line fields from the backend during reopening. This does not claim an Auto Rotate round trip: the previously documented original numeric-rotation merge limitation remains unchanged.

## Evidence and limits

On 2026-10-18, pinned Node 24.22.0 ran `node verification/node_modules/@playwright/test/cli.js test application.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts`: 1/1 passed in 79.3 seconds, one headless worker, no skips, retries or flaky outcomes. Existing save failure/retry, export and table-return assertions also passed. Diagnostics retain only the deliberate save-failure 500 and the previously recorded missing TradingView bundle 404.

The independent Astra review approved the three test changes, actual browser report, updated UI worklist and sanitized publication. Production code is unchanged; size caps do not apply to these test/documentation edits. The worklist now distinguishes completed integration work from remaining acceptance, instead of describing active chart entry points as disconnected.

Workspace base: `f84879a435f57206788fa57c965c6789404c3520`, plus the following test files:

| Path within Workspace | SHA-256 |
| --- | --- |
| `terminalpro/tests/e2e/live-chart/application.spec.ts` | `f1288c1491e2e3243b6a020efa05ff9983e8092d17921e806be9d1d86e5950a8` |
| `terminalpro/tests/e2e/live-chart/customize.ts` | `3c7bba6f3aa67cadaf809cc628528cfb4927469423ae5349ab23a832f30ea853` |
| `terminalpro/tests/e2e/live-chart/diagnostics.ts` | `f4b3a18089888f8f4eaf09d7e13b75148fca569a41acc61f5609b78505ed8eaf` |

The existing disposable source-overlaid backend and actual Full frontend were used. This is not release-image verification. No new screenshot is published because the change adds a behavioral assertion and does not change the approved appearance. Raw results remain in `artifacts/live-editor/runtime/manual-rotation/`. Task 2.77 and broader renderer/deployment acceptance remain open.

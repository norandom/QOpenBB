# Restore Add a series in Set Up

Set Up again offers the original [Add a series selector](add-series.png) beneath selected series. Removing Cost, saving and reopening now leaves Cost available to select again. Adding it restores its actual values and persists the original selected range. The control also offers eligible numeric columns absent from the saved chart selection.

The original AG Grid 34.1.1 reference uses an unselected-field selector with a plus icon, not another toolbar. The replacement had only remove/reorder pills. Browser RED reproduced the missing selector after removal. The repair supplies the existing panel with current numeric choices and a typed addition event; selected IDs are appended through the original range/model transaction. Empty-string IDs and duplicate labels remain distinguishable.

Fields absent from retained chart data are read from the public grid outside the Widget reducer. A complete stamped snapshot supplies the requested field and current selected values together. Invalid IDs and stale captures cannot commit. This preserves aggregation, category/series switching, range bounds, unknown model fields and the existing persistence owner.

## Verification and scope

- Independent Astra contract and implementation reviews approved the bounded repair and publication set. The implementation reviewer independently reran the 34 session/transition and 10 panel tests, checked all source/publication hashes and inspected the actual browser reports and synthetic screenshot.
- Focused unit checks: 10 panel tests and 34 session/transition tests passed; final transaction rerun passed 7 tests. The panel RED failed for the missing selector before implementation.
- `series-selection.spec.ts` passed in the actual Full Workspace, one headless worker, 1/1 in 76.0 seconds with no skips, retries or flaky outcomes. It removes Cost, checks the remaining plotted observations, saves the reduced original range, opens a fresh session, restores Cost through the selector, checks rendered Revenue/Cost values, saves and opens another fresh session. Raw results remain in `artifacts/live-editor/runtime/series-add-green/`.
- The combined complexity gate passed with explicit Workspace and data API manifests. All seven modified production files meet caps of 400 physical lines, 300 logical units and 50 units per callable; maximums are 195/91/45. Broader session TypeScript compilation remains non-clean in existing imports; changed production files have no reported diagnostics. No full compiler pass is claimed.
- The ordinary three-family application join passed 1/1 in 81.7 seconds, one worker, exit 0, no skips or retries. This preserves manual rotation, save/retry, fresh-session/backend-restart persistence, PNG export and table return. Diagnostics passed their assertions with the deliberate save-failure 500 and previously recorded missing TradingView bundle 404 allowed.

Only one synthetic screenshot and this record are published. The runtime uses the existing disposable source-overlaid backend, not a verified release image. Task 2.77 and broader renderer/deployment acceptance remain open. The original Auto Rotate and structural-axis restoration limitations are unchanged.

## Reviewed source identity

Workspace base `f1e08583a1803136b5b8ef1a5c270df665bb0533`, plus:

| Path within Workspace | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/Chart/application/applicationSessionCapture.ts` | `ccdf65aa50f4a13a6b69eb77d134493d4f0a552aaa9bfbdd00f9c5c4b525e38d` |
| `terminalpro/src/components/General/Table/Chart/application/applicationSessionProjection.ts` | `db40677f8e4b0e6920abf66822398048900085a95fda9a0803f811d3474449d9` |
| `terminalpro/src/components/General/Table/Chart/application/applicationSessionSetup.ts` | `e940578d81d60fe6f60e58afd18b3520c9dbbd7d1907dad9cac65ecf63038e5f` |
| `terminalpro/src/components/General/Table/Chart/application/setupTransitions.ts` | `defa9f37826a401e2f8c9f12eccbdea1535a714fb083fff8e4ff66169b3089f5` |
| `terminalpro/src/components/General/Table/Chart/application/useApplicationChartSession.ts` | `3ab497c8a55d0db987c3686b5e9c377e04b5da5a968e0c85afd067813c30c082` |
| `terminalpro/src/components/General/Table/Chart/editor/setup/ChartSetupPanel.tsx` | `5dbca6ba6aa6503bc23b6b7fac8f7b8b2703f95c27f341fde9c7d0c7382437ee` |
| `terminalpro/src/components/General/Table/Chart/editor/setup/chartSetupPanel.css` | `526709937b976046e89389fa79f77d07b14ec580838624849b8a72986fdd39f7` |
| `terminalpro/tests/unit/chart-application/applicationSession.test.tsx` | `bb838964fcf71e03a3050663e5e7da070d5b34a915f22c26b6490c0d0842d0c9` |
| `terminalpro/tests/unit/chart-application/applicationSessionTransactions.test.ts` | `b89e4e1ac62d929df0d43b8fbdd76464072d928858c55a51a623ef775024b85f` |
| `terminalpro/tests/unit/chart-application/setupTransitions.test.ts` | `d23b3f92278510c91b5fe8d38bb6ddfa5c41263b77ad9537fcab83215fcd892a` |
| `terminalpro/tests/unit/chartSetupPanel.test.tsx` | `ad0b9f8155f9a9160595f04b358f2de4d089474c83be4b5068a68fc03b5bc08f` |
| `terminalpro/tests/e2e/live-chart/series-selection.spec.ts` | `8cf23352167e4409d32a6bb190411c01e32e3a93defb1db28c7ed5793f29dd92` |

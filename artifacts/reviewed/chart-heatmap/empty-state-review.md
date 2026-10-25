# Heatmap empty-selection review

APPROVED for the bounded source correction on 2026-10-25. The independent review inspected the actual two-file diff, original verification outputs and host/export implementation. Packaged browser acceptance remains pending.

Workspace baseline: `c7a7633fd1b864647f55c08dd5ce0d4654fe93a0`. Reviewed working-file SHA-256 values, before commit:

| Path relative to vendor/workspace/terminalpro | SHA-256 |
| --- | --- |
| src/components/General/Table/Chart/AgChartView.tsx | `214310af02e5f9b6cfa95872f0fef710674a8c935ded5feacf4728e4848c6965` |
| tests/unit/chart-application/callerRoute.test.tsx | `0c85bde757ffda2163bbbe5fefe3d6dce5fc84a0f7dc718d524b140c4013f4a4` |

The caller derives both the visible DOM message and host visibility from the same ready Heatmap Setup selection. Zero selected numeric series hides the host with CSS visibility while preserving its mounted lifecycle and dimensions. Selected all-missing observations and selected series with zero displayed rows keep the renderer visible. Other chart families retain their existing condition. No renderer, state-owner or export code changed; no blocking findings or required remediation remain.

The real EChartsHost forwards the style to its container. Lifecycle sizing reads client dimensions and PNG export calls the renderer's getDataURL, independently of DOM capture. This supports retaining the existing export graphic without double-painting the visible message. It is source reasoning, not an executed empty-export acceptance claim.

Verification examined under local `artifacts/chart-heatmap/hm4/empty-overlay/`:

- RED: focused callerRoute Heatmap run failed both Table/File missing-message assertions; two exclusion controls passed, 27 unrelated cases skipped. Exit 1, red.log.
- GREEN: `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/callerRoute.test.tsx --maxWorkers=1`, from the Workspace terminalpro directory: 31/31 passed, exit 0, green.log. Four new cases cover Table/File removal and recovery, selected all-missing coordinates and selected zero-row behavior. The reviewer did not repeat this suite.
- Exact two-file Biome lint passed, exit 0. Full-file test formatting retains pre-existing drift; no clean full-format claim. Diff whitespace, added placeholder and credential-pattern checks were clean.
- Scoped TypeScript baseline/current diagnostic records independently compared unchanged: 390 diagnostics, zero additions. Eight inherited owned diagnostics remain: AgChartView inputs.error TS2339 and seven callerRoute getByRole exact TS2769 diagnostics. This is baseline-relative evidence, not a clean compile.
- Reviewer ran the combined inventory-backed complexity gate with explicit two-file Workspace and empty data-api change manifests: exit 0, no errors, violations or exceptions. AgChartView measures 318 physical lines, 99 logical units and maximum 12 per function against 400/300/50 caps. The test is excluded by inventory policy. Evidence: review-combined-caps.json. An initial shell invocation failed before the checker started because inherited PATH entries contained spaces; the corrected invocation used a fixed Linux toolchain PATH.

This accepts source only. Existing populated-chart appearance acceptance is unchanged. Original empty-state export remains unverified; the rebuilt candidate still requires browser checks for one visible accessible message, recovery, persistence and PNG behavior before application acceptance.

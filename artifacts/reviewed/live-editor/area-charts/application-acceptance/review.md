# Area application join review

APPROVED for task 2.90: ordinary Table/File area, stackedArea and normalizedArea integration. The owner requested original axis scales; the final application now matches them after the independently reviewed axis repair. No broader UI-10 or release-image acceptance is implied.

## Mechanical results

- Tests: PASS. Reviewed RED evidence contains two caller failures and three missing legend callbacks. GREEN evidence contains 17 caller/session checks, 120 initial renderer regressions, 80 affected checks after axis repair, and 19 final representative native area checks.
- Browser: PASS. area-layout-final completed one isolated, single-worker journey in 86.127 seconds with zero skipped, flaky or unexpected results.
- Static checks: scoped Biome passes; targeted placeholder/credential scan and runtime-import inspection are clean. Compatibility TypeScript retains the documented baseline typography.ts TS2578 and is not claimed green.
- Boundary: WITHIN. Three join production files activate the reviewed families, transfer the area axis namespace and reuse the existing native legend callback. Separately reviewed font and axis repairs add no flag, dependency or state owner.
- Caps: PASS. Final explicit combined scope covers 77 files with no errors/violations. Join files remain within 400 physical/300 logical/50 per-function; cartesianAxes.ts measures 229/88/9.

## Findings resolved and observed behavior

The initial application had different area domains and ticks. The owner chose Match original axis scales. The final screenshots show ordinary area -10/0/10, stacked area -5/0/5/10 and normalized area -50%/0%/50%/100%, matching the retained original six-row fixture. The normalized zero category retains the corrected valley. The axis review records the finite-extreme and actual-layout-density corrections required before this approval.

The reviewer inspected all six final images: three defaults, normalized light/dark and the downloaded PNG. The export contains current title, marker sizes, strokes and translucent fills. Browser assertions cover raw signed tooltips, label/marker/stroke/fill controls, native legend reprojection with unchanged full overview, navigation, theme updates, saved options/unknown branches, fresh-context reopen and return to raw table data. Unit checks cover all three callback families, latest data/theme projection, distinct stored ranges and area-axis settings without touching inactive branches. No derived percentages or transient selection enter saved financial observations.

The default screenshot gallery scroll differs from the retained original capture; gallery code and artwork are unchanged, and the browser successfully selects all original area choices. This is a capture-state difference, not a renderer feature removal. Both browser sessions report no application exceptions. The existing allowlisted datafeed bundle 404 and associated console/request events remain; this does not claim globally clean networking.

## Evidence and source identity

Final browser: artifacts/live-editor/runtime/area-layout-final/browser-results.json. Its attachments record actual canvas dimensions 359x284 for every family. The native mapper test uses a separately identified representative 640x300 source-default setup; it is not represented as an exact application-theme reproduction. Earlier stale/runtime and intermediate scale runs do not establish final acceptance.

Commands reuse pinned Node under WSL, existing chart-application/chart-compatibility Vitest configs with one worker, scoped Biome and the explicit complexity manifest. Browser command from QOpenBB root:

```text
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/cli.js test area-charts.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts
```

Reviewed final axis fork commit: 0fc244b, plus the uncommitted three-file application join reviewed independently. SHA-256 identities:

| File | SHA-256 |
| --- | --- |
| application/applicationSessionProjection.ts | d44f30de108e0501f7e67865a607f544fe97e6321ff1c7719e38ccc1c767c612 |
| application/axisStructure.ts | d12e375ac72befaeef5badf7e215c0de51ed9630f5898371098deb9383f2e36f |
| echarts/cartesianTypes.ts | 177b2dfe90aca9fce1ec2328234ee824b437a04d1f9a89b72ba98228825014ce |
| final browser report | f8914acb1f2bb26e6a1057aa51f9006709d9ac620d50f33e86902f391e00118f |
| join-complexity.json | 305188e3e63e462f98c2c3b37089f4f4aa287088e691cfbdf203ea89b1c12b66 |

Publication review: the three final default PNGs contain only the synthetic Area observations fixture and ordinary UI, with no credentials or private account data visible. They are approved for the selective evidence mirror with the concise axis review. Keep raw diagnostics and intermediate runs local. Breadth, source pins, manifest verification and selective delivery remain controller-owned.

No required remediation remains for task 2.90 within this scope. Reuse of accepted persistence-failure/restart evidence is appropriate because this change does not modify persistence ownership.

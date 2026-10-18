# Horizontal renderer acceptance

Task 2.79 implements groupedBar and stackedBar in the existing ECharts mapper. Independent Astra review approved the frozen change. Caller activation and browser acceptance remain task 2.81.

The renderer preserves top-to-bottom categories, raw labels/tooltips, explicit zero versus missing observations and independent positive/negative stacks. Numeric-X navigation crops the main chart without removing rows; the owner-approved horizontal miniature retains all series and their full signed extents. No controls, themes or flags were removed.

Independent verification: pinned Node 24.22.0, compatibility Vitest config, horizontal/application/geometry/grid files: 60/60 passed, exit 0. Scoped Biome: six files passed, no fixes. Whole production files pass 400 physical / 300 logical / 50 function caps; maxima 250/81/21. Compatibility TypeScript retains the existing typography TS2578; no compiler pass is claimed. A preexisting grid test expected obsolete fixed tick counts after the accepted line-spacing refinement; it now verifies exactly two endpoints disappear, retaining independent native coordinate and style comparisons.

Base Workspace 64517dbb941d1080abd3f48cb42f5aecf46e0238 plus the exact files below. Local RED, baseline grid reproduction, final test/lint output and independent review remain under artifacts/live-editor/horizontal-bars/renderer. No image build or release acceptance.

| File | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesian.ts` | `87b25051371e3447ebb3c2491c15593275592b811b4b5c7489b83d8fb8be6b52` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianAxes.ts` | `de8daf631cd9cfb4c8926a9b6a0af3a283d764acee281e691615f09d8fc4194c` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianSeries.ts` | `84ea0f6c0148fd341375e0411ef4bb9c34520682cdccbd4b1c2b2c26c072a357` |
| `terminalpro/src/components/General/Table/Chart/echarts/cartesianNavigator.ts` | `50e2643f6e6e39dc9487a9351d5d7dfb748d9bb1d4c61749db210adac26c3686` |
| `terminalpro/tests/unit/chart-compatibility/cartesian.horizontal.test.ts` | `e7af3f44b5d95f2dc8afa14625147c8ceeb5403738c7828b1df431c47c95266a` |
| `terminalpro/tests/unit/chart-compatibility/cartesian.grid.test.ts` | `8eef9a881dc3692f75b342b1b2e3520ac699a3d486ec2fafadff89f278608f51` |

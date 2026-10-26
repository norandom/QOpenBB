# Stage-label repair independent review

APPROVED for the bounded source repair on 2026-10-26. Actual glyph visibility in a rebuilt image and overall F4 acceptance remain pending.

- TASK: Funnel-family stage-label anchors and Cone endpoint clipping.
- Baseline: Workspace `1fe9178b9d3c0016f912a1c3d85663afdcf88203`.
- Boundary: WITHIN. Only `echarts/funnelLabels.ts` and `tests/unit/chart-compatibility/funnelRenderer.test.ts` change. Reviewed actual diff, surrounding geometry/layout and native retained placement semantics. No source values, plot geometry, padding defaults or session owners change.
- Verified production SHA256: `ae6d158e8be09d8c5d7b94d52bdbb92a9ec7ccbe5da748b45bc78433479f5d29`.
- Verified test SHA256: `0b485c2113f837bafcd7d16a71bcf87f849d7a6233f67e45e0b15a6f6ac2475e`.

Vertical before/after labels now anchor right/middle and left/middle respectively. Horizontal before/after labels anchor center/bottom and center/top. These match native Pyramid placement at retained Enterprise 12.1.1 lines 36424-36432 and 36500-36504; Funnel/Cone use the corresponding category-axis sides through FUNNEL_SERIES_AXES. Optional text-group alignment parameters retain center/middle defaults for numeric labels.

The stage clip expands only along the progression axis by existing seriesAreaPadding. For a nonempty layout, subtracting that padding from the area's start yields common padding plus any enabled caption reservation; adding it to the end yields viewport minus the opposite common padding. Thus the viewport clamp does not broaden the valid clip beyond pre-seriesArea content. The cross-axis strip remains unchanged. Empty areas return before expansion, avoiding invented space when layout is exhausted. The implementation does not mutate geometry or numeric-label output.

Mechanical evidence reviewed:

- Tests PASS: 21 checks in renderer and geometry files, exit 0, 15.06 seconds. `tests.log`, `tests.exit` and `verification.json` retain the command/results. Coverage includes all three families, both directions, both placements, unchanged geometry and numeric defaults, and measured vertical Cone endpoint glyph bounds through actual ECharts text objects.
- Lint PASS: exit 0 for both owned files. `lint.log` reports two formatting fixes; reviewed hashes are the resulting frozen files. Independent changed-file `git diff --check` passes.
- Complexity PASS: matching baseline/head manifest, exit 0, errors and violations empty in `complexity.json`. Production file is 169 physical lines, 81 logical units and maximum function size 15.
- Placeholder/secret spot check CLEAN: no placeholder markers or concrete private-key/API-key patterns found. No new production imports or runtime bindings were introduced.
- RED evidence is the recorded packaged Cone clipping and centered-label discrepancy against native captures. `verification.json` explicitly records that no separate pre-edit failing unit test was run.

No blocking source findings remain. Existing jsdom canvas-measurement warnings limit the glyph test's font-metric evidence; do not substitute it for browser verification. The patch does not promise arbitrary long horizontal label fitting, collision avoidance or additional axial padding. Validate the changed default labels against the matched native captures in the next identified candidate, without expanding this task into a layout rewrite.

REMEDIATION: None for this source task. F4 image, broader controls, theme recovery, refresh, persistence and export acceptance remain separate.

# Independent N3 integration review

## Review Verdict

- VERDICT: APPROVED
- TASK: N3 serialized Table/File Nightingale integration, including the authorized Stroke Width label correction.
- MECHANICAL_RESULTS:
  - Tests: PASS. Fresh independent bounded run on 2026-10-24 at 14:57:22, exit 0: 11 tests across nightingaleSessionOwner.test.tsx (9) and nightingaleEditorControls.test.tsx (2), 37.18 seconds. Command from vendor/workspace/terminalpro: pinned Node 24.22.0 `node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/nightingaleSessionOwner.test.tsx tests/unit/chart-application/nightingaleEditorControls.test.tsx --maxWorkers=1`, through Debian/mc.
  - TBD/TODO grep: CLEAN across all 29 present frozen files, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN targeted credential-pattern scan and actual source inspection.
  - Static checks: PASS fresh scoped Biome lint over all 29 present frozen source/test paths, exit 0, no fixes. Independently compared retained strict diagnostic logs after source-location normalization: 2680 baseline and 2680 current diagnostics, no delta. Current compiler exit 2; initial baseline wrapper exit 0 is unreliable and is not compiler success.
  - Identity: all 29 SHA256 values match frozen-files.json; the thirtieth record's deleted radarCapture.ts is absent. Its polarCapture.ts replacement is identical after the function rename.
  - Complexity: independently recounted all 24 production files against final-identity.json. Maximum 357 physical lines, retained syntax evidence maximum 140 logical units/file and 42/function; within 400/300/50. Controller-owned combined inventory gate remains required before task acceptance.
  - Boundary: WITHIN. Read actual tracked diff and new composition/normalizer files. N4's two E2E files, unrelated Perspective/catalog/inventory work and generated caches are excluded.
  - Boundary audit: CLEAN. Existing capture, setup, reducer, session stamp, theme, transient legend and native ECharts host owners remain authoritative.
  - RED phase: VERIFIED. red.log contains four inactive-routing failures plus the absent composition module. Label RED has exit 1 for the missing Stroke Width control; retained GREEN and this independent run pass.
- FINDINGS: No blocking defects found in the frozen N3 source boundary.
- REMEDIATION: None for source review. Controller must complete the combined inventory gate before marking N3 accepted.
- SUMMARY: The frozen source join preserves Nightingale financial data, control persistence and stale-command protection with passing focused evidence; packaged appearance and real-data acceptance remain N4.

## Contract findings

Read AGENTS.md, applicable delegation/complexity/testing/workspace-experience/documentation steering, kiro-review, the maintained Nightingale contract/milestone and N0/N1/N2 reviews. Review baseline is Workspace 7cffa0894c494ebe59769d4df9a055135a72d65f; root checkpoint supplied by the controller is c4be837. Approval attaches to frozen-files.json hashes, not unrelated working-tree content.

Group Type uses model-root seriesGroupType. Transactions clone the selected complete model, preserve neighboring root and inactive theme options, retain capture, and request a render revision through the existing reducer. Ordinary setup retains that model. Direct family and ordinary setup transactions compare root presence/value; the existing assignment key also contains both. External changes therefore invalidate commands before synchronization and advance generation during synchronization. Internal commits update the key together with storage, avoiding accidental invalidation of subsequent edits. Tests exercise stale family-control and ordinary-setup callbacks both before and after synchronization, plus absent-to-explicit-default root structure changes. Invalid explicit undefined JSON model content remains invalid rather than being treated as a valid stale model; the corrected expectation is justified.

Nightingale has a distinct named observation policy and shares the unchanged polar wrapper normalizer. Setup remains the single aggregation/inversion owner. The integration passes selected snapshots to the accepted mapper without a second aggregation; tests verify raw signed/missing data, duplicate category order, count display without currency, aggregation before inversion, and selected series order. Normalized radial labels remain neutral numerical strings while tooltips retain raw amounts. Legend projections recompute through the same native mapper without persistence writes.

Table/File routing reaches native polar bars, Group Type, Polar Axis and Series controls through existing UI owners. The explicit series branch prevents Pie fallback and excludes markers/shadow/Radar Shape. Existing navigator/mini-chart flags remain saved and reachable without introducing a Nightingale slider. Tests cover ready-empty refresh/recovery, removing/readding all series, resize, retained family settings, and serialization followed by a fresh hook owner. These are source-level persistence and lifecycle checks, not packaged browser claims.

Caller themeInputs uses selected.palette provenance, preserves supplied custom strokes and provides background strokes for absent palettes; same-name light/dark regression inputs disprove a theme-name heuristic. The authorized Line Width to Stroke Width change matches controls.series in retained original observations and is exercised through the accessible input into the saved renderer style. Foreign Nightingale panels reject outside the family, while Nightingale rejects neighboring family controls.

## Retained regression evidence and limits

Inspected actual logs rather than summing handoff claims. join.log reports 50 passing tests in five files. regressions.log reports 150 passing and one failing test in 13 files; the failure was the invalid-versus-stale expectation described above. final-owner.log rechecks all nine owner tests successfully after that expectation correction. label-green.log rechecks both editor tests after the label amendment. polar-setup.log and setup-panel.log add seven and ten passing tests respectively. These runs overlap and must not be presented as one unique combined passing count. The independent 11-test run verifies the final owner/editor bytes. Scoped lint was rerun without invoking the worker's format-write script.

No browser, build, provider call, inventory edit, source modification or commit was performed by this reviewer. Retained caller logs contain jsdom canvas warnings; native SVG checks stub text measurement. Strict TypeScript evidence establishes zero added normalized diagnostics, not a clean application compilation. Real FMP packaged values, light/dark comparison, actual export, browser refresh/fresh-session reopen and owner appearance acceptance remain N4. No N4 result is required or inferred for this source-join approval.

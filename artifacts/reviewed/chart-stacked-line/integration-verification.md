# Stacked Line source integration verification

2026-10-26. The renderer, editor and ordinary Table/File session now admit Stacked Line and 100% Stacked Line through the existing Cartesian owners. This record covers source integration only. Packaged FMP browser acceptance and image publication remain open.

The renderer preserves raw financial values for labels/tooltips and projects signed cumulative coordinates in selected order. Normalized coordinates use maximum cumulative excursion. Missing, hidden and zero-denominator endpoints remain empty; an unrepresentable amount prefix produces a specific diagnostic, including when a legend change removes cancellation. The navigator retains the full selected-series overview while the main plot recalculates visibility.

## Executed gates

Commands ran in WSL with Node 24.22.0 and installed locked dependencies. The combined scripts are local artifacts/chart-stacked-line/join-regressions.sh and join-checks.sh. Every Vitest run used one worker.

- Compatibility: nine files, 178 tests passed (27.90 seconds). Includes new line types/geometry, existing Cartesian, Area, normalized-bar and navigator regressions.
- Application: five files, 53 tests passed (42.48 seconds). Includes both stacked editor variants, session projection, ordinary session state and Area caller/editor regressions.
- Nonmutating scoped Biome: 24 files checked, no fixes, exit 0.
- Whole-file inventory-backed complexity: combined acceptance passed, no errors or violations. Production caps are 400 physical lines, 300 logical units and 50 per function.
- Strict TypeScript comparison uses the same 20-root set against frozen Workspace 0b2190354d2dc5f4175ffb989cf652ac36237c77. Raw result: baseline 2791, candidate 2789, one message mismatch, exit 1. The mismatch is the same app.ts TS2345 at offset 2080/length 26: its truncated enum member display changes order, while the underlying optional Zod key error is unchanged. Raw diagnostics are retained; this is not a clean application compilation. Independent review owns the exact inherited-error adjudication.
- Browser preparation: Playwright lists three tests successfully. Collection is not execution. Source review approves the bounded first run; continuous/duplicate grouping, remaining controls/topology and export content comparisons remain explicitly open.

The retained financial fixture is AAPL FY2025 reported USD: cost of revenue plus gross profit reconciles to each quarter's reported revenue. No fresh provider query ran. Source checks establish arithmetic and integration contracts, not visual parity or a release.

Local evidence: join/compatibility.log, application.log, lint-final.log, complexity.json, typecheck.json, join/typecheck.log, browser/collection.log. Review records: geometry-review.md, editor-review.md, join-review.md and browser/re-review.md. Initial failing checks and fixes remain in local evidence; published documentation summarizes accepted results without copying every raw log.

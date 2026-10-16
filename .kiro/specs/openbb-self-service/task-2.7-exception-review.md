# Task 2.7 narrow exception design review

VERDICT: APPROVED for the seven measured metric exceptions below and the exclusive ChartSettings extraction lane. This is not acceptance of task 2.7 or its final implementation.

Review date: 2026-10-16. Reviewed baseline and current Workspace HEAD: `273c6529571501cb3bc211addb6129e24d91247b`. The three reviewed worktree changes are uncommitted. Review evidence: `artifacts/task-2.7/exception-review-measurements.json`; reproduction: pinned Node 24.22.0 runs `artifacts/task-2.7/exception-review-measure.mjs` from the repository root under WSL Debian. Parser: the existing `tools/quality/syntax_units.ts`, TypeScript 6.0.3.

## Exact scope and measurements

Paths below are relative to inventory repository `workspace`. Baseline and current measurements are identical.

| Path | Physical | Logical | Functions | Functions exceeding 50 units |
| --- | ---: | ---: | ---: | --- |
| terminalpro/src/lib/state/copilot.ts | 1601 | 845 | 162 | `<anonymous>` at line 853, column 22: 52 |
| terminalpro/src/components/types.d.ts | 886 | 581 | 0 | None |
| terminalpro/src/components/General/Table/utils.tsx | 505 | 268 | 47 | `getTableData` at line 86, column 1: 62 |

Approve physical and logical exceptions for copilot.ts, its exact over-limit callable, physical and logical exceptions for types.d.ts, and physical plus the exact over-limit callable for Table/utils.tsx. No logical exception applies to Table/utils.tsx. No other function or file is covered.

Each actual diff is precisely a single type-only module-provider change from `ag-grid-enterprise` to `ag-grid-community`, after newline normalization. The request's reference to `ag-charts` was inaccurate for these three paths. The installed AG Grid Community 34.1.1 declaration entry exports all imported names: BaseCellDataType, ChartModel, ChartType, Column, GridState and IHeaderParams. AG Charts Community 12.1.1 is not the provider of these grid types and is outside this narrow symbol check.

All function names, positions and counts remain identical. TypeScript transpilation with source maps disabled emits byte-identical runtime JavaScript for copilot.ts and Table/utils.tsx; types.d.ts is a declaration file with no runtime output. This is targeted evidence, not a complete frontend typecheck/build or behavioral suite.

## Exception conditions

Each entry must use repository `workspace`, its exact path, one of the seven metrics above, the measured value as `baseline`, this review artifact as `review`, and `expires_on: 2027-01-14`. Function entries require the exact name and one-based line/column above. The `revision` must match the measured Workspace head in the final scope report, as required by `tools/quality/exceptions.py`. Current evidence is tied to HEAD `273c6529571501cb3bc211addb6129e24d91247b` plus the reviewed worktree diff. After a fork commit changes HEAD, rerun the measurement and diff checks, confirm these exact files remain unchanged, and bind the exception to that new scope revision; do not retain a stale revision.

Rationale: task 2.7 removes commercial type dependencies while preserving supported Community contracts. The changes have no runtime output effect, add no syntax units, and change no existing callable or state semantics. Extracting these unrelated store/type/table implementations solely for an import-provider replacement would expand this removal task into an unrelated behavioral refactor. The 90-day expiry bounds that deferral. Any additional behavior change in these paths requires renewed review; any measured growth fails the approved bound. No blanket exclusion, checker weakening, or implicit grandfathering is authorized.

## ChartSettings ownership decision

The proposed second bounded Sol lane is APPROVED after the main lane explicitly releases `ThemeSettings/ChartSettings.tsx`. The second lane owns that file and an explicitly enumerated disjoint set of new helper/test files. Preserve its public exports, props, and state semantics with one state owner. Extract cohesive editor/preview responsibilities; all modified/new maintained files and functions must pass 400 physical, 300 logical, and 50 function-unit caps. This approval grants no exception for ChartSettings because removal of unsupported preview background-image behavior is a behavioral change.

The main lane retains the remaining task 2.7 work. The parent owns shared package/lock, inventory, breadth and spec joins; installs and heavy checks remain serialized. Freeze interfaces and ownership before execution, stop affected lanes on overlap, and independently review joined code and behavior before final acceptance. This is a routine exclusive-file handoff inside the approved Community rendering boundary, not a new feature/phase approval.

## Mechanical result and limitations

Targeted measurement script: PASS, exit 0. Exact-change comparison, function identity, runtime emission identity, and Community type exports: PASS. No added placeholder, credential or runtime expression is possible within the verified single import-provider replacements. Boundary: WITHIN task 2.7 and design's Community rendering boundary. RED phase: not applicable to this narrow design exception review. Full tests/build were intentionally not run against the changing shared fixture; they remain required for task acceptance. No final task acceptance is claimed.

## Committed scope binding

The parent rebound the seven approved exceptions to Workspace revision `0341b12524cb822262be631fa820e2ca851a348a` after the task's independent review approved the frozen 55-path snapshot. The exact import-only diff, callable positions and emission checks were rerun against this commit; evidence is retained in `artifacts/task-2.7/exception-committed-recheck.json`. The original baseline above remains the comparison source.

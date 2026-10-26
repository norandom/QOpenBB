# Repeated-coordinate tooltip source review

2026-10-26. **APPROVED source; verification gates pending.** Reviewed the actual `cartesianTooltip.ts` and `sessionStackedLine.test.ts` changes. No blocker found and no additional scope requested. No execution or production edits by this reviewer.

The implementation retains shared axis triggering, including marker-off behavior. Only shared mode with a drawn admission mask resolves other rows at the same finite continuous coordinate. It reuses category conversion and numeric coercion, handles equivalent time representations, and retains snapshot row order. Ordinal, ordinary Line without the mask, distinct continuous coordinates, single and compact preserve their prior behavior.

Each observation block reads its own raw values, applies its own finite drawn-endpoint admission filter, and includes an escaped category plus observation ordinal. Empty admitted blocks disappear; hidden/missing series do not reappear. No values are summed and no cumulative coordinate replaces a raw amount. The selected-coordinate finite check excludes nonfinite matching groups.

The regression covers both stacked families and both continuous axes with markers and labels disabled, exact separate raw blocks, equivalent timestamps, row-one/row-two axis params, missing and hidden values. The guards check distinct coordinates, duplicate ordinal categories, ordinary Line and single/compact modes. These assertions directly address the reported failure and marker-off design correction. The controller's focused GREEN, scoped static gates and packaged Time rerun remain acceptance evidence to attach after completion; this source approval permits the bounded rebuild workflow.

## Final source gate

**APPROVED with inherited compiler qualification.** Independently compared the current strict report's sole added diagnostic with its baseline counterpart: both are unchanged `src/lib/types/app.ts`, TS2345, offset 2080, length 26, with identical `$ZodRecordKey` / `string | undefined` incompatibility. Only the truncated enum member ordering differs. The file has no diff from the compiler baseline. This is inherited diagnostic rewording, not a new repair defect. Preserve the raw result: baseline 2791, candidate 2789, added 1, exit 1; this is not a clean compile. Candidate diagnostics in all declared owned roots: zero.

Current production and regression-test SHA-256 hashes exactly match the frozen values in `verification.md` (`938190d8…0db8` and `4366ad26…9f0c`). Recorded focused GREEN is 13 tests; the inspected additional Cartesian regression log passes 91 tests. Scoped caps report has no errors or violations; scoped lint is recorded clean. The source repair gate is accepted, with packaged browser hover acceptance remaining separate.

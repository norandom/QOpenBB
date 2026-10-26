# F3a independent helper review

Approve the inactive stock/plain-color Funnel theme helper. Actual source and retained native palette operations agree; focused verification passes. No caller routing or browser acceptance is claimed.

## Review Verdict
- VERDICT: APPROVED
- TASK: F3a-inactive-theme-helper
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent pinned Bun/Vitest, existing chart-compatibility config, funnelThemePaint.test.ts, maxWorkers=1; 19 tests, exit 0. Reproduce with bash artifacts/chart-funnel/f3a/review/tests.sh; output review/tests.log.
  - Static checks: PASS. Independent strict=true, skipLibCheck=true, noEmit=true TypeScript baseline comparison from the actual Terminalpro working directory: baseline 22/candidate 22, no added or owned diagnostics, exit 0 (review/typecheck.json, review/typecheck.log). This is not a clean full application compile.
  - Lint: PASS. Nonmutating Biome check of both owned files, exit 0, no fixes (review/lint.log). Fork git diff --check exit 0.
  - Complexity: PASS. Independent combined inventory gate with f3a workspace/data_api manifests and reviewer output, exit 0 (review/complexity.json). Helper: 124 physical lines, 64 logical units, maximum 16/function; within 400/300/50 caps. Parent corrected only inventory serialization before this run; the worker's earlier inventory-length failure is retained in its report.
  - TBD/TODO/placeholder scan: CLEAN in production helper.
  - Secrets scan: CLEAN in production helper; private.invalid/secret in the test is a deliberate synthetic redaction assertion.
  - Boundary: WITHIN one pure caller helper and its test. Existing projectCallerTheme remains the common color/default owner; no commercial package, host state, storage mutation or routing added.
  - RED phase: VERIFIED. red.log and red.exit record missing-helper import failure, exit 1, before implementation; no assertions ran in RED.
- FINDINGS:
  1. No blocking findings. Native Community 12.1.1 paletteType at 25838-25845 distinguishes named user-full palettes and indexed fills/strokes from inbuilt palettes. Native paletteOperation at 33678-33704 takes circular first-two fills for range2. Enterprise CONE_FUNNEL_SERIES_THEME at 28982 onward uses secondSequentialColors for inbuilt fills/strokes and the same SAFE_RANGE2_OPERATION for both custom arrays. Independently inspected these source ranges; helper matches the approved plain-color semantics, including strokes-only and repeated one-color cases.
  2. Named up/down/neutral entries are validated as fill/stroke objects, not scalar colors. Stock arrays, explicit base-theme selection, Funnel first paints, complete Pyramid arrays and per-family label/drop-off colors have concrete assertions. Retained light OKLCH fixture supplies source identity rather than substituting RGB interpolation.
  3. ValidationResult contains nonthrowing failures for JSON-reachable palette/theme inputs. Advanced objects receive the dedicated unsupported message; malformed colors/arrays receive a distinct invalid message. Errors expose no original asset URL. Returned paint arrays are detached and source input remains unchanged. Deferred advanced palettes are not silently rendered or promoted to acceptance.
  4. Integrated hook diagnostics, external theme recovery, saved-series override precedence, actual browser colors, persistence and export remain F3b/F4 obligations. This helper consumes selected theme defaults; F2 continues to own saved appearance precedence.
- REMEDIATION: None for F3a.
- SUMMARY: The bounded helper satisfies the accepted stock/plain-color design with independent source inspection and fresh verification.

## Source identity

Workspace baseline: a3e1a861f47057f52faf7120b27375419efbfb16. Frozen bytes matched the implementer report:

- caller/funnelThemePaint.ts: 912207102f513c37aa74c44641d80a5d76a3db287ed83f15e653127522800ad2.
- tests/unit/chart-compatibility/funnelThemePaint.test.ts: 321863354d0bb83e0d90a9a3e3592af7adcf1a2d8e66a14eae28f91bfa0a4509.
- Implementer report: 9e175d70f956822f00ad65ae7ed7ee95bb2153df8197a46e8afe03d6d8b9bfa7.

No production files, tests, frozen reports or other lanes were edited by this reviewer. Evidence is ignored under artifacts/chart-funnel/f3a/review/. Verification supports TASK acceptance only, not FEATURE_GO.
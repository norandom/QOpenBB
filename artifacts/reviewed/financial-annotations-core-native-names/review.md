# Canonical native-name correction review

2026-10-29. Approve the bounded core correction. Canonical Python field names now agree with native OpenBB's `response_model_by_alias=False` contract. Projection-mode enforcement and provider adoption retain their separate acceptance gates.

## Review Verdict
- VERDICT: APPROVED
- TASK: Task 1 integration correction, canonical native annotation names
- MECHANICAL_RESULTS:
  - Tests: PASS, independently run 21 tests in 5.17s, exit 0, WSL Debian/Python 3.13.15. Command: `PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_annotations.py -n0 --maxprocesses=2`.
  - TBD/TODO grep: CLEAN, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN; no credentials or new I/O in the diff.
  - Static checks: PASS, exit 0. `verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/core/pyproject.toml --no-fix vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_annotations.py`.
  - Complexity: independently measured with the existing `tools.quality.python_units.measure_python`: 162 physical lines, 100 logical units, maximum function 13. Within 400/300/50; controller inventory gate remains separate.
  - Boundary: WITHIN. Reviewed core module and focused tests; no provider, projection, shared Data, registry or public signature changes in this correction.
  - Boundary audit: CLEAN. Canonical ownership is independent of individual routes; input aliases remain unchanged.
  - RED phase: VERIFIED in `red.log`: native false-mode rendering and canonical aliased-query limit binding failed before the correction, 2 failed/19 passed.
- FINDINGS:
  1. No blocking findings. The diff against `71c9ac04c88` replaces alias selection with nonexcluded `model_fields` names. This resolves the concrete mismatch recorded in [alias-integration.md](../financial-annotations-core/alias-integration.md), without changing accepted runtime rows or metadata names.
  2. FYI: The original class-owned declarations, explicit unknowns, definition resolution, independent deep copies, runtime disclosures and response-cap policies are unchanged and remain covered by the focused suite. The existing aiohttp inheritance deprecation warning persists.
- REMEDIATION: None for this core correction.
- SUMMARY: Approve canonical names as the frozen core interface; complete the controller gate and separate projection/provider reviews before integration acceptance.

## Source identity and scope

Independent SHA256 checks match the frozen production file `08c93215756303d7a6644049314776d8a7616507cc827785f12cb68d8ecffde8` and test file `ef94bce00e4d131796b23934f1d87744a92d1227ab8f4d7d94d7d396a88acfbd`. The abbreviated revision `71c9` was ambiguous; review used the resolved commit `71c9ac04c88`.

The focused regressions verify native false-mode row/template agreement, alias-only key/reference rejection, excluded-field rejection and canonical query-limit lookup despite an input alias. Static inspection confirms all currency/date references use the same canonical field set. Public binding/rendering signatures are unchanged. This review applies the task 1 boundary and requirements 4.1, 4.2, 6.1 and 7.3 with the controller-approved integration correction. The prior isolated review is preserved as historical evidence; it does not override the corrected [interface.md](interface.md).

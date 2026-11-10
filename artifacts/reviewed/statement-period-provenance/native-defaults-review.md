# Native statement default repair review

APPROVED for the bounded provider repair. Task 6 packaged browser acceptance remains open and must use a rebuilt candidate containing this repair.

## Review verdict

- VERDICT: APPROVED
- TASK: Statement period provenance task 6, native optional-limit integration repair only.
- Reviewer: independent financial/native-contract review, 2026-11-10.
- Scope: two FMP adapter query transforms and three affected root test files. No production edits were made by the reviewer.
- Mechanical results: 66 passed, 97 deselected, exit 0. One existing aiohttp inheritance deprecation warning. The worker's broader affected run records 144 passed; its RED records 3 failed and 19 passed before installation of the repair.
- Placeholder and secret review: CLEAN in the added diff. Static checks: SPOT_CHECKED; imports and runtime dependencies are unchanged.
- Boundary: WITHIN the controller-authorized task 6 repair. Boundary audit: CLEAN; no core, generic transport, financial calculation or provenance mutation.
- RED phase: VERIFIED from red.txt, including both direct None cases and native omitted Balance returning 422.
- Findings: no blocking findings.
- Remediation: none for this repair.

## Contract assessment

The installed Balance standard model declares limit=None; Query.execute serializes standard parameters with asdict. The provider declares default 5. Resolving the missing/None sentinel to that declared provider default before strict validation restores the native omitted-control contract. Cash's current standard model already defaults to 5, explaining why its native omitted case was green before the repair; accepting the same optional None sentinel in its provider is coherent with its optional standard type. Direct None is now intentionally accepted in both adapters. This is not an assertion that literal HTTP null is valid.

The change uses an identity check, so zero, False, floats and strings are not mistaken for omission. Existing strict validation still rejects their raw Python representations; native numeric HTTP limit=2 retains the existing conversion and behavior. Native literal null, None, empty and nonnumeric query values fail safely before the mocked acquisition boundary. Tests verify default 5 and explicit 2 are sent to acquisition, clip a six-row payload and agree with effective_query and bounds.

Sorting, paired row/provenance clipping, monetary values, currencies, flow/instant classifications and unknown coverage remain unchanged. The selected provenance regressions passed against the installed packages. This satisfies the repair's preservation obligations under requirements 3.1 and 3.3 and the design's transformation and compatibility sections; browser controls under 4.2 still need controller acceptance.

## Reproduction and identity

Run from the QOpenBB repository with PYTHONPATH pointing only to services/data-api and the isolated provider-venv interpreter:

```text
python -m pytest tests/providers/test_balance_sheet_metadata.py tests/providers/test_cash_flow_metadata.py tests/providers/test_service_financial.py tests/providers/test_statement_provenance.py -q -k "omission_sentinel or statement_native_optional_limit or statement_native_invalid_limit or quarterly_alias_and_strict_limit or invalid_query_fails_before_io or provenance" -o cache_dir=<native-defaults>/review-cache --basetemp=<native-defaults>/review-tmp
```

Exact local output is review-tests.txt. No live provider calls, browser runs, dependency changes or image builds occurred in this review. Independent import inspection confirmed site-packages loading and LF-normalized source equality:

| Adapter | SHA-256 |
| --- | --- |
| Balance | 152eca2460e17b5698f006bbc95b9b27fd9e3ef26079b7151ec126659251951a |
| Cash | 9444c3599a551f377a7c48a5b003c262c87fc403c91683c33ac1fddee1ef6c18 |

Worker size evidence is 154 physical / 57 logical / maximum function 12 for Balance and 137 / 57 / 10 for Cash, within 400 / 300 / 50 caps. The canonical inventory join remains controller-owned; this report does not substitute for it or close the packaged-widget task. Broader financial compatibility and IA-B readiness remain open.

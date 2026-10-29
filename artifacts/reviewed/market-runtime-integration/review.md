# Task 5.2 independent review

- VERDICT: APPROVED
- TASK: 5.2, runtime contract integration.
- SUMMARY: The exact installed candidate exposes the eleven annotated financial datasets, enforces provider selection, and returns safe native API failures while preserving the baseline and gallery contracts.

The review inspected the actual root diff and the data-fork diff from `13e41631bdef0ee98bfa23bda68d329224b56eb1` to `28423762e8cc3faae978e770899834b41e7cde99`. It followed kiro-review and the complexity, testing, delegation, CI and documentation steering. No production or test files were edited by the reviewer. The configured core steering files product.md, tech.md and structure.md are absent; the available task-specific steering and approved specification supplied the review contract.

## Mechanical results

| Check | Observed result |
| --- | --- |
| Installed runtime join | PASS: 193 tests in 38.92 seconds, actual pytest exit 0. Command: `wsl -d Debian -- verification/provider/.venv/bin/python artifacts/market-runtime/run.py review`. Receipt: `artifacts/market-runtime/review.json`; log: `artifacts/market-runtime/review.log`. |
| Packaging and existing gallery contracts | PASS after fixture repair: 84 tests in 8.64 seconds, actual pytest exit 0. `pipeline/.venv/bin/python -m pytest tests/delivery/test_data_image.py tests/contracts/test_gallery_runtime.py -n0 --maxprocesses=2 -q`, with pipeline on PYTHONPATH. Receipt/log: `artifacts/market-runtime-review/packaging-recheck.json` and `.log`. |
| Final gallery fixture cleanup | PASS: the affected gallery test passed in 0.99 seconds, exit 0, after import sorting and equivalent list/dict constructors. Receipt/log: `artifacts/market-runtime-review/gallery-final.json` and `.log`. |
| Owning Ruff configurations | PASS: `verification/provider/.venv/bin/ruff check --no-fix` on all 17 frozen production/test paths from the repository root, exit 0. Receipt/log: `artifacts/market-runtime-review/ruff-root.json` and `.log`. |
| Source identity | PASS: all 15 root-file hashes and both fork-file hashes match final-source.json. Five installed distributions have the candidate's non-editable direct origins; their Python files match the extracted source. All 664 archived files match a newly read immutable Git archive. Details: `artifacts/market-runtime-review/identity.json`. |
| Complexity and inventory | PASS: independently remeasured all ten changed production files against 400 physical lines, 300 logical units and 50 units/function. Measurements equal the frozen record. The retained combined gate covers 83 files with errors and violations empty; changed production paths are inventoried. |
| Placeholder and secret inspection | CLEAN: no TBD/TODO/FIXME/HACK/XXX or private-key/token patterns in the changed Python files. Diff inspection found synthetic test canaries and environment-variable credential reads, with no hardcoded private credentials. |
| Boundary | WITHIN runtime contract integration. Finite image-input changes package the required service modules and coverage index; no root source-pin or consumer snapshot promotion occurred. Foreign renderer and inventory changes were preserved. |
| RED evidence | VERIFIED: runtime RED 15 failed/1 passed; packaging RED 23 failed/13 passed; typed FRED RED 10 failed; binding RED missing the activation function; protocol RED retained verified proofs after a response change. These logs precede the corresponding passing checks. |

The installed join injects only the root service through PYTHONPATH. It does not substitute provider/core source paths. The only runtime-suite warning is the existing aiohttp ClientSession inheritance deprecation.

## Requirements and boundary audit

| Criteria | Verified behavior |
| --- | --- |
| 1.1 | `/datasets.json` returns the eleven annotated installed models, their financial schemas, query definitions, bounds, provider variants and separate coverage states. Its references agree with the served OpenAPI. Account access, real data and widget acceptance remain unknown. Unannotated FRED routes remain in native OpenAPI. |
| 5.1-5.3 | All eight new paths reject omitted providers before transport access. Explicit FMP selection reaches the installed fetcher and stays visible in the result. Baseline defaults remain in their native routes; the wrapper neither dispatches an alternative provider nor substitutes an instrument. |
| 6.2, 6.5 | Actual installed enterprise-value HTTP output agrees with the Python fetcher for rows and financial field semantics, including zero and negative values. Existing profile, income and FRED contracts pass alongside the discovery, policy and error suites. The service uses its installed native commands without a browser or AI service. |
| 7.1, 7.2 | Mounted failures distinguish typed categories, invalid input, invalid provider rows and unexpected exceptions. Secret canaries remain absent from public schema/discovery, error bodies and captured logs. FRED supplies canonical typed categories and discards raw exception chains; its authentication, missing-series and throttling cases retain HTTP 400. |

The service copies the mutable native ASGI shell, router container, handlers and middleware list before activation. Tests exercise a native request, a service request and another factory instance, and confirm that the original native handlers and schema remain unchanged. Pure financial projection retains native response definitions; the separate activation binder describes the installed safe handlers. Response-definition changes now invalidate consumer proofs. The Dagger call boundary passes the actual source revision, coverage file and runtime-input hash and does not manufacture an OCI image digest.

## Findings and remediation

1. Important, resolved: the pre-existing gallery framework test stub exported only configure, so importing the integrated app failed on coverage_index. The independent combined run recorded 1 failed/83 passed in `artifacts/market-runtime-review/packaging.json` and `.log`. The controller extended this explicitly stubbed gallery fixture, retained every original gallery assertion, and added middleware registration coverage. The subsequent 84-test run passed. Genuine native ASGI behavior remains covered by the separate 193-test join.
2. Static-check setup, resolved: the requested pipeline Ruff executable does not exist. The existing provider-environment Ruff was used. Running from pipeline initially produced five import/lambda findings; the gallery fixture was cleaned up and the final owning check from the repository root passed. No production change was needed.

No unresolved findings. Required remediation: none.

## Frozen identity and limits

- Native candidate: `28423762e8cc3faae978e770899834b41e7cde99`.
- Committed archive SHA256: `db6e2a7a71b37953ada4a2860508c415534abaaab9ecac09e9ea58aa5c0e974f`.
- Candidate and retained dependency-lock SHA256: `f3e1026c1d0d23eac2aa85436c8d619577860d6a2cf98dfc4a95618fafb41bd1`.
- Exact file hashes and production measurements are recorded in final-source.json. The final identity receipt includes the seventh root test, tests/contracts/test_gallery_runtime.py. Production hashes remained unchanged throughout review remediation.

Approval is limited to task 5.2 in the installed development environment. Task 5.3 still owns coordinated source/catalog promotion and reusable widget generation. No live provider entitlement, packaged Workspace journey, image build, publication or deployment is established by this review.

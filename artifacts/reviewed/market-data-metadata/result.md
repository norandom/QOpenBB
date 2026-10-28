# Financial metadata task 1.2 evidence

The common schema is frozen for independent review. No provider registration, app wiring, shared fixture, installation or source pin changed in this lane. The controller owns the joined complexity gate and acceptance.

Production: vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_metadata.py SHA256 f09e9e518c6411646fb04921a2ab3aa117b8a3bf9410aca72a4499157c4fd69a.
Test: tests/providers/test_financial_metadata.py SHA256 9dd15a7d8545b991b475e1cc568a91b364b5d72c260228f80fa57abf4940edbf.

## Verification

WSL Debian, repository /mnt/d/Source/QOpenBB:

`PYTHONPATH="$PWD/vendor/data-api/openbb_platform/core" verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_metadata.py -n0 --maxprocesses=2`

RED was run after writing tests and before creating production code: red.log records zero collected and one collection error, ModuleNotFoundError for the absent financial_metadata module, 21.53s. The surrounding shell wrapper incorrectly returned zero; this is a test failure and is not reported as a passing test command. GREEN used pipefail and tee: exit 0, 27 passed, one existing ClientSession deprecation warning, 8.29s, green.log. Python 3.13.15, pytest 9.1.1.

Actual OBBject.from_query processes an AnnotatedResult containing validated metadata. JSON roundtrip preserves legacy GDP metadata, common metadata, actual UTC acquisition, None, zero and signed values. Focused fixtures reject naive acquisition timestamps, source request URLs/query/userinfo, nonallowlisted query keys, nested query objects, URL query values, reserved-key collisions and dishonest completeness. Unknown bases remain nullable; default completeness is unknown. Ordered transformations retain their definition and input basis; FRED source/effective semantics remain distinct. Missing vintage/publication information does not assert point-in-time safety.

Secret canaries are synthetic. Pydantic error text hides supplied values; structured Pydantic errors remain internal inputs and must use the separate safe failure boundary before publication. The model intentionally does not guess whether a valid symbol/name contains a secret. Public source documentation is HTTPS without userinfo, query or fragment; endpoint uses an identifier rather than a request URL. Allowlisted query scalar values reject structural credential assignments and URLs.

Root and fork git diff --check exited 0. Production caps are 400 physical / 300 logical / 50 per function; parent joined executable scope check remains required. No live-provider, service image, application or entitlement acceptance is claimed.

## Independent review remediation

The earlier freeze above is superseded. Independent review identified colon-permitting endpoint identifiers, unconstrained field source and the api-key assignment alias. Added seven focused regressions before fixes. remediation-red.log records exit 1, five failing and 29 passing tests, 15.76s. Tightened identifiers to exclude colon, made field source an identifier and expanded only structural credential-assignment aliases. Ordinary Token Energy Corp and KEY query values remain accepted. remediation-green.log records exit 0, 34 passed, one existing warning, 8.84s, same exact source-override command. Root/fork diff checks exit 0.

Final frozen production SHA256 968e3ffc2d91bb137940bdd2b10f443b3213a6293d2cbe78bc5ffff758b28495.
Final frozen test SHA256 babaf3d39420da80f0ed19c6a855f9960d253aea45cfb1447bd262eecf35eed7.
Parent joined scope/complexity gate and independent re-review remain required.

Final lint-only freeze: production SHA256 b76078803f56c380a1863449dd186b2520031ac2253919fab05a8b1ad2d1d86b supersedes prior production hash. Reviewer requested import ordering and seven rationale docstrings; no behavioral code changes. Scoped owning-fork `verification/provider/.venv/bin/ruff check --no-fix vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_metadata.py` exits 0, All checks passed, ruff.log. Fork diff check exits 0. Test bytes/hash unchanged; prior 34-test behavior evidence retained without unnecessary repeat.

# Income annotation repair 4.1 result

Ready for independent review. Income declarations now own static field semantics; all 17 focused tests and 27 complete baseline comparisons pass. This report does not accept the task or close main task 4.1.

## Contract and scope

Typed query ClassVar declares baseline_default provider selection and income_compatibility response handling, with no fixed clipping cap. The cohesive income_statement_data.py owns the unchanged data class, aliases, validators and explicit canonical field templates. income_statement.py keeps the original public import and fetcher. Runtime renders independent templates and fills actual reporting basis and availability. Acquisition time, bounds, provenance, row currencies and error behavior stay runtime-owned.

Requirements checked: 4.1, 4.2, 4.3, 6.1, 6.2, 6.3. Design checked: Financial metadata contract; Discovery and generated consumer contracts; Financial failures and HTTP compatibility; approved financial-annotations amendment and canonical native-name correction.

## Verification

- RED: instructed WSL provider pytest command on test_income.py before production changes: 14 existing passed, 3 new agreement cases failed with MissingFinancialAnnotation (31.01s), red.log. The initial outer shell masked the child exit status; the recorded pytest failure summary is the RED evidence.
- GREEN: wsl -d Debian -- bash /mnt/d/Source/QOpenBB/artifacts/annotations-income/verify.sh: 17 passed (18.47s), CHILD_RC=0. Same instructed PYTHONPATH, provider venv, pytest config, -n0 --maxprocesses=2.
- preserve.py: 27 complete row and metadata comparisons against frozen 28c31b4 across annual/quarter/ttm, limits None/0/1, original/mixed-currency+null/legacy-current alias fixtures: PASS, PRESERVE_CHILD_RC=0.
- Owning Ruff: verification/provider/.venv/bin/python -m ruff check --no-fix --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml followed by both changed production paths: All checks passed, exit 0.
- Local AST comparison against 28c31b4: data, query and fetcher classes are unchanged after removing added financial annotation attributes.
- Whole-file checker measurement through tools.quality.complexity.measure_file and violations: no cap violations; caps.json records detailed functions and SHA256. Controller still owns combined portable inventory acceptance.

## Frozen files

| File | Physical | Logical | Largest function | SHA256 |
| --- | ---: | ---: | ---: | --- |
| vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/income_statement.py | 133 | 48 | 10 | 6b412528f3962765feecb1cdf9c39a3d2365a3f572e547f23ee1964de91bd71d |
| vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/income_statement_data.py | 262 | 54 | 6 | 6b849fcb43224194d847b000f1695b174694d44eb150b2786c68a3360170cde7 |
| tests/providers/test_income.py | test | excluded | excluded | c3ec45977e94b916690637ac1e6c22077a0954195cf037fe1f9dd7b54a2f0434 |

## Remaining gates

Independent review and controller acceptance remain required. Controller must inventory the new companion, synchronize source pins/breadth and publish reviewed evidence. No commit, source pin, inventory, shared helper or registry edit was made by this lane. No live provider, image or browser verification was performed. The existing aiohttp ClientSession inheritance deprecation warning remains. Missing core steering product.md, tech.md and structure.md was reported; supplied project guidance and applicable existing steering were used.

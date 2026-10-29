# Discovery and peer declaration evidence

Repair task 4.4 is ready for independent review. Source and tests are frozen; controller acceptance, task completion, shared inventory and publication remain separate.

The query classes own explicit-provider policy and clipping by the modeled limit parameter. Existing limits/defaults remain Field-owned; raw search length and trimmed symbol length now read modeled maxima while retaining their prior safety rules. FMPDiscoveryIdentity owns complete identity templates, inherited by search; peers extend copied identity templates with price, market-cap and suggestion provenance. Runtime metadata renders independent copies and fills observed availability. Acquisition time, source, effective query, actual clipping and unavailable dates remain runtime-owned.

Requirements checked: 4.1, 4.2, 5.1, 6.1, 6.2. Design sections checked: Provider fetchers and first-batch surface; Financial metadata contract; Discovery and generated consumer contracts. The accepted financial-annotations amendment and native canonical-name interface apply. Input aliases and emitted names remain unchanged.

## Verification

WSL Debian, repository /mnt/d/Source/QOpenBB; source PYTHONPATH includes owned core, FMP and FRED. Data fork HEAD at evidence recording: 537cf473d4ecd6bc8f24649bebcd720d6aeca93c with concurrent unrelated lanes preserved. Exact owned file SHA256 values are in hashes.json.

- RED: bash artifacts/annotations-discovery/red.sh captured baseline first (actual child rc0), then pytest collected40, returned2 MissingFinancialAnnotation failures and38 passes, actual pytest child rc1. This ran before production edits. See red.log.
- GREEN: bash artifacts/annotations-discovery/green.sh compared30 complete baseline outputs/boundary query/error cases (actual child rc0), then40 tests passed in6.81s (actual child rc0). All37 existing cases remain. See compare.log and green.log.
- Focused pytest command: verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_discovery.py -n0 --maxprocesses=2.
- Owning checks: bash artifacts/annotations-discovery/static.sh ran verification/provider/.venv/bin/ruff check --config vendor/data-api/ruff.toml --no-fix for the three owned models, actual child rc0; existing checker measure_python plus physical caps returned rc0. Initial static run exposed import order and an existing non-imperative docstring; these were corrected manually before final verification.
- Whole-file physical/logical/max-callable counts: equity_search.py88/40/6; equity_peers.py106/44/7; discovery_data.py91/37/7. See caps.json. All pass400/300/50.
- Root and fork scoped git diff --check passed. A trailing blank test line was removed after GREEN; assertions and execution bytes were otherwise unchanged.

Baseline comparisons cover empty, minimal and mixed-exchange/currency/provider-value results across limits1/20/100 for both operations, with preserved complete rows and metadata. Boundary comparisons include raw search length200/201 and leading whitespace, peer length50/51 and surrounding whitespace, allowed prefix/slash rules, comma rejection and newline rejection. New tests verify complete canonical declarations, explicit provider policy, copied-template metadata agreement and template consumption without previous-result mutation.

The only pytest warning was the existing aiohttp ClientSession inheritance deprecation. No live keys, network/provider acceptance, installs, builds or browser sessions were used. This worker does not claim independent approval, installed projection integration or provider guard activation.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: Repair4.4
- TASK_BRIEF: Preserve discovery identities, suggestion semantics and full outputs while sharing static field meaning and clipping policy with declarations.
- FILES_CHANGED: FMP models/equity_search.py, equity_peers.py, discovery_data.py; tests/providers/test_fmp_discovery.py
- REQUIREMENTS_CHECKED: 4.1,4.2,5.1,6.1,6.2
- DESIGN_CHECKED: Provider fetchers and first-batch surface; Financial metadata contract; Discovery and generated consumer contracts; financial-annotations amendment
- RED_PHASE_OUTPUT:40 collected;2 missing declaration failures,38 passed; actual child rc1; red.log
- TESTS_RUN:40 passed;30 complete baseline comparisons; FMP Ruff and three-file caps pass; actual child rc0 for each
- CONCERNS: Independent Astra review and controller acceptance pending; shared inventory/full join remain controller-owned.
- EVIDENCE: brief.md, red.log, green.log, compare.log, baseline.json, compare_baseline.py, caps.json, hashes.json, red.sh, green.sh, static.sh

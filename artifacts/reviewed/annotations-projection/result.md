# Fixture projection ready for independent review

Current freeze includes the native output-name correction reviewed in `artifacts/financial-annotations-core/alias-integration.md`. The original 12-test freeze below is superseded by the evidence and identities recorded here. The accepted core correction is `28c31b4b0ee`.

The projection inspects each required route's actual `response_model_by_alias` attribute and accepts only the literal `False`. Missing, unknown and true-alias modes fail explicitly. Row schemas use `by_alias=False`, matching canonical declarations and native serialization. Query validation schemas retain aliases because native `ProviderInterface._create_field` publishes `Query(alias=field.alias)`. A fixture checks this actual native method with an explicit query alias. Declared query-bound references that cannot resolve against the published query properties fail rather than introducing a name-remapping engine.

Current verification: alias RED had 6 failures / 10 passes, true child return code 1; the row schema emitted `evToEBITDA` instead of `ev_to_ebitda`, unsupported route flags did not fail, and one expected error-text assertion reflected the superseded core wording. Corrected GREEN passed all 17 cases in 6.77 seconds with true child return code 0. Files `alias-red.log` and `alias-green.log` retain that evidence. Owning Ruff passed with return code 0. Production measures 225 physical / 144 logical / maximum function 27; tests measure 272 / 177 / 27. Controller owns the combined inventory gate.

Current frozen SHA-256:

- Production: `f9d910039a9c6695272d42f38ecad796c06ded945dffa1d41d5ad77527a560f2`.
- Tests: `8a0e6c59a1d689dbce882fbc321002d3660ad93cf017d3a609ac2261d5041cc0`.

Repair task 3 implements `project_financial_openapi(document, routes, registry_map, *, required_models)`. The caller supplies advertised model names; every required model must have an actual route association, OpenAPI operation, installed variant and valid declaration. The function returns a copy and leaves unrelated operations and native schemas unchanged.

The descriptor exposes provider policy and installed choices, actual query schemas, serialized row aliases, financial templates including explicit unknowns, procedural bounds, response policy and runtime property disclosures. Namespaced references cover query/row definitions, common metadata, a success-envelope overlay and the public error contract. The overlay preserves the native response schema and identifies `extra.results_metadata.__qopenbb_financial__`; it does not claim that unrestricted `extra` enforces the contract. Error handlers, provider request guards and real-model integration remain separate tasks.

## Initial verification (superseded by correction above)

- RED: focused suite before production module existed failed collection with `ModuleNotFoundError: qopenbb_data.financial_openapi`; true pytest return code 2. An initial inline WSL invocation interpolated the shell result variable through PowerShell; the literal `verify.sh` rerun captured the actual child code before implementation.
- GREEN: `bash artifacts/annotations-projection/verify.sh green` uses the assigned source override and focused pytest command. All 12 tests passed in 5.75 seconds; true pytest return code 0. One existing aiohttp inheritance deprecation warning remains.
- Owning root Ruff discovery: `verification/provider/.venv/bin/ruff check --no-fix services/data-api/qopenbb_data/financial_openapi.py tests/providers/test_financial_openapi.py` passed, return code 0. No root Ruff configuration file exists; discovery resolves root settings. The fork Ruff configuration does not own these root files.
- Existing checker primitives report production 207 physical lines / 129 logical units / maximum function 25; tests 240 / 156 / 22. All satisfy 400 / 300 / 50. Full inventory gate remains controller-owned.

Initial SHA-256 (superseded):

- Production: `141e103a33207c47be5cd4f4739b97d5f804e5f1157c3c2d9adb9a0926c31589`.
- Tests: `b09d37ae4eef2022f2887074eee4cb232de35d67b88ccb82bf339370f6f6c660`.

Local evidence: `red.log`, `green.log`, `static.json`, literal `verify.sh` and `static.py` in this folder. No commits, pins, inventory, provider code, builds, installations or live requests changed in this lane. Foreign renderer and key-metrics lane edits were preserved. Core/default steering `product.md`, `tech.md` and `structure.md` are absent; task-specific steering and approved interface were read.

## Scope limits

Fixture-only projection cannot accept repair task 5 or main task 4.1. The controller must verify accepted real classes, baseline router associations and runtime metadata agreement. This module derives descriptor field keys from the corrected canonical binder/render contract and verifies supported native route mode; it does not implement alias-output remapping. No handlers or production route mounts are installed.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: financial-annotations repair task 3
- TASK_BRIEF: Deterministic nonmutating projection from required native associations and accepted declarations, with resolvable namespaced references and explicit invalid/missing failures.
- FILES_CHANGED: services/data-api/qopenbb_data/financial_openapi.py; tests/providers/test_financial_openapi.py; artifacts/annotations-projection/*
- REQUIREMENTS_CHECKED: 1.1, 4.1, 4.2, 5.1, 5.2, 5.3, 6.1, 6.3
- DESIGN_CHECKED: Discovery and generated consumer contracts; Financial failures and HTTP compatibility; approved financial-annotations amendment minimal contract
- RED_PHASE_OUTPUT: initial missing-module child rc 2; native-mode remediation 6 failed / 10 passed, true child rc 1 before production correction.
- TESTS_RUN: corrected focused pytest 17 passed in 6.77 seconds, child rc 0; owning root Ruff passed, rc 0; existing size checker primitives production 225/144/27.
- CONCERNS: Fixture-only acceptance; runtime wiring and actual-provider class agreement remain controller task 5. Independent review pending.
- EVIDENCE: alias-red.log; alias-green.log; static.json; current source/test hashes above.

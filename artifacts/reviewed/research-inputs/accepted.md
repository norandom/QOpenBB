# Company Research input verification

The bounded IA-A run verified access and source/API preservation for Microsoft, Oracle and Adobe. Financial compatibility and IA-B workflow readiness remain open. Independent financial review accepted the bounded gap assessment on 2026-11-06.

- [Input assessment and next scope](../../../.kiro/specs/analyst-workspace/research-input-assessment.md)
- [Machine-readable coverage and original evidence hashes](../../../docs/reference/research-input-readiness.json)
- [Approved task plan](../../../.kiro/specs/analyst-workspace/research-input-tasks.md)

## Observed execution

On 2026-11-06, source `b597df79007c586a86f2ce7c0004bec8c39baf87` and OpenBB data API `28423762e8cc3faae978e770899834b41e7cde99` completed one serial run: five live journeys passed, 49 upstream attempts, 46 native FMP receipts and three direct DCF receipts. Each source response was HTTP 200. The shared request counter was contiguous from 1 to 49, below the 51-attempt ceiling. There were no automatic retries or fresh FRED calls.

The combined offline check passed 73 tests, with 20 live cases excluded. Live and offline runs each reported the existing aiohttp ClientSession deprecation warning. Independent Astra reviews accepted the helper, both implementation lanes and the live evidence. The initial native review found listing-identity and blocked-prerequisite defects; both were repaired and independently rechecked before the live run.

The canonical entry point was `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml`, with `PYTHONPATH=services/data-api`, `-n0` and `--maxprocesses=2`. The offline join selected the service, native financial and DCF modules with `-m "not live"`. The live run selected the three `test_research_company_inputs` company cases, `test_research_provider_peer_suggestions`, and `test_live_msft_dcf_feasibility` in one process, with explicit live opt-in and privately loaded credentials. Both commands exited 0.

## Evidence boundary

The exact commands, source hashes, query parameters, acquisition dates and individual receipt hashes are indexed in the machine-readable assessment. Original run directory: `artifacts/research-input-readiness/live-20261106T112507Z`. Its `execution.json` SHA256 is `d085d2eb674ca9337ddd0350f1aa16ad9598c3c9c64a564fb1dcbd75985e4fd1`; `pytest.log` SHA256 is `cf25b41cc77df549acf41ffa1b6def3a77cbf86d4484fc1d574e997c1cc62424`. The independent live-review SHA256 is `43afece27987245da7b95a58b3340074650f14ba2cc3e8d1ad4d26f30e3c4f16`. Local receipt paths identify original evidence, not public downloads.

FRED DGS10 evidence retains its original 2026-10-30 scope and acquisition date. Direct DCF access does not establish a native route/widget, house valuation or sensitivity correctness. Period duration, fiscal alignment, currency/share/claim conventions, metadata omissions and financial-method prerequisites remain explicit findings.

This publication contains a sanitized assessment and this concise verification record. Private configuration, raw run logs and intermediate review files are omitted. No production code, dependency, deployment or image changed; no Dagger build was dispatched.

## Final assessment review

Independent Astra review approved the assessment with all 24 requirements covered and no blocking financial findings. Assessment completion is true; IA-B input readiness and workflow implementation remain false. Original review SHA256: `75bd97ac99f853470ed16096c9ec8bb9122f3f50ef37f81211eadb8e55495692`. Publication checks verify the linked records and this exact-byte mirror; no product deployment acceptance is implied.

## Accounting evidence correction, 2026-11-06

The earlier assessment incorrectly attributed three missing exported accounting definitions to the provider. The test sanitizer had removed dictionary keys containing `account`. The [static audit](accounting-source-audit.json) verifies all 50 original receipt hashes; twelve affected receipts retain comparison semantics. Pinned native source separately proves scale and currency-reference annotations. Original exports remain unchanged; this correction does not reconstruct their missing subtrees or claim new live acceptance.

The sanitizer now preserves accounting definitions and selected values while filtering private identity and transport fields. Three regressions failed before the fix; all 35 existing service-suite tests pass with the additions. [Independent Astra review](accounting-correction-review.md) approved the test and assessment correction, including fresh receipt/source checks. The reviewed narrative's sole publication changes are its public audit link and this correction-review reference. IA-B readiness remains false; the genuine Metrics/Ratios periodic-query metadata omission has a separate proposed design. No production code, image or deployment changed.

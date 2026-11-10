# Periodic query provenance

Metrics and Ratios now expose their validated `ttm: exclude` selection, including defaulted requests. Source/native checks and four fresh FMP comparisons passed. Publication and offline packaged checks also passed; independent delivery review passed on 2026-11-10. Owner-server deployment and IA-B analytical readiness remain open.

- [Approved repair and task state](../../../.kiro/specs/market-data-integrations/periodic-query-provenance-tasks.md)
- [Consumer migration](../../../docs/provider-coverage.md#periodic-query-metadata-compatibility)
- [Provider coverage identities](../../../docs/reference/provider-coverage.json)

## Source and verification

Data API commit `2e60c0a7aff039eda5f14a9d494beaec822fb9c4` changes three production lines: the core public-query allowlist and the Metrics/Ratios metadata emitters. Installed core/provider copies matched all three committed module hashes before testing. The older strict Python validator requires the matching updated core/provider pair; metadata remains schema version 1. This adds no TTM acquisition or calculation.

The focused suite reproduced 19 failures before the repair and then passed 125 tests. Independent Astra source review passed, including four fresh identity/schema/empty-result checks. Native/offline integration passed 73 tests with 23 live cases deselected. An initial integration run exposed two test assumptions: stale historical adapter proofs must remain stale, and native responses omit unset/null fields that Python models retain. The corrected assertions preserve both distinctions. The existing aiohttp deprecation warning remains.

The canonical command is `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml`, with `PYTHONPATH=services/data-api`, `-n0` and `--maxprocesses=2`. The focused selection uses the metadata, metrics and ratios test modules; native integration uses service-financial and live-financial with `-m 'not live'`. Both accepted runs exited 0. Source/native schema checked through the accepted clean generator reports no route changes or affected consumers; this is not canonical image-backed catalog generation.

Whole-file physical/logical/maximum-function sizes are 193/115/9, 140/56/10 and 141/59/10. Owning-fork lint and the combined source-pin scope gate pass with no errors or violations. The first pin-join scope attempt rejected an old manifest base against the promoted inventory; the final clean committed-snapshot declaration rechecks maintained controller files and validates the promoted fork identities. The unchanged three fork-file measurements are retained from task 2 and joined by their identical committed/installed hashes. Existing unrelated renderer/inventory work was excluded.

## Four real-provider observations, 2026-11-06

One serial run completed four cases in 34.18 seconds. Each sent one MSFT request with limit 1, returned HTTP 200, preserved source/API values and emitted the validated periodic selection. Run counters are exactly 1 through 4. No retries, FRED calls or repeated IA-A assessment occurred.

| Dataset | Caller selection | Emitted period / TTM | Original receipt SHA256 |
| --- | --- | --- | --- |
| Metrics | Period and TTM omitted | annual / exclude | `95b1832f111c0a358637174c104075028c4edbef3cd822ab76962174e43809f8` |
| Metrics | quarter, exclude | quarter / exclude | `6424d7136736673301ecd804fb8c5ebcd57ba3f7651c901870c186ac02ec48fc` |
| Ratios | Period and TTM omitted | annual / exclude | `6a2aa88f95cb1f5c27dcec10cf765787a8bacf80a48849585821be37969f85dc` |
| Ratios | quarter, exclude | quarter / exclude | `0234c0e16b9e0cc691b17bea484b2f8dda97c531c9523d83828140bb5fc9c885` |

Local original run: `artifacts/periodic-query-provenance/live-20261106T135844Z`. Execution-record SHA256: `6a0c3d4968ea74f03b3e14ed6120934de0c27e808ab7fb46d27d53a0c4f3267d`; pytest-log SHA256: `ea5e4fd6c3a0c25a3965d2279da0b1b8505c27dc8d6c6553c0f355fc335d5abd`. The record identifies controller base `70853da2ac5138a1ce6292c463d6e07243b4d9d4`, the exact then-uncommitted test-file hashes, data commit and four selected node IDs. Raw receipts/logs remain local. The two renewed real-data proofs identify only these adapters and their unchanged contract hashes; all other coverage and historical IA-A receipts remain unchanged.

## Delivery boundary

Native/source acceptance is distinct from image publication, packaged consumer verification and owner-server deployment. The packaged checks below cover the published data API; they do not repeat Workspace browser acceptance or establish owner-server deployment. Actual duration/YTD, restatement, valuation/share/claim conventions and both false IA-B readiness flags remain unresolved. The repair changes query provenance, not financial conclusions.

Independent Astra integration review approved the source/native join on 2026-11-06, with two fresh offline checks and an audit of all four live receipts, the two renewed proofs and 50 unchanged historical receipt hashes. Original review SHA256: `f4b5d9379f42eebbb7b856a27441757a7f1ad08db16eca97c6ca95eae55e5df3`. The published-image checks below follow that source/native acceptance.

## Published alpha and packaged checks

[alpha-42231784072-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-42231784072-1) was built once by [workflow 42231784072](https://github.com/norandom/QOpenBB/actions/runs/42231784072) from controller `b37ec1963e1bc138115b431e3c168e5e48a8bd47`. Both candidate and publication jobs succeeded. Workspace remains at `f832a5593223b1e702970c4de8eceda87a17fa5b`; the data API is the reviewed commit above.

| Image | Immutable public reference |
| --- | --- |
| Workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:6dd6fc83cb46248fdc2e62e582547c3efd25e152640ce931e6bba873d6706ea1` |
| Data API | `ghcr.io/norandom/qopenbb-data-api@sha256:51f28fb741431767dac2385b13ca15faafec3885e7b08af55591cce073e42232` |

Three installation assets passed anonymous HTTP, byte-length and GitHub SHA256 checks. Six anonymous image pulls passed: digest, alpha tag and `latest` for both services. Source labels, manifest/config digests, Linux/AMD64 platform and RepoDigests match the release manifest. Docker's local IDs are manifest digests on this daemon; their Descriptor digests were checked separately. Compose parsed with the immutable pair and parser-only credentials; no deployment was performed.

The canonical clean catalog generator ran against this exact data image and committed provider source, with deterministic repeated upstream generation. Its route hash matches the installed source/native proposal. OpenAPI, routes, widgets, apps, datasets and catalog report are unchanged. Only provenance, hashes and the compatibility comparison record changed; the latter now records no route drift against the preceding accepted catalog. This does not remove the separately documented older strict Python-validator migration requirement.

The existing offline packaged runtime suite passed three tests in 76.48 seconds. A separate ownership-labeled, network-disabled container checked health/readiness, six discovery endpoints, 11 native widgets, source/generation identity and all three installed module hashes. Four deterministic Python/native cases covered Metrics and Ratios with default annual or explicit quarterly queries, unchanged negative/zero/missing values, schema version 1 and `ttm: exclude`. No real provider request, new dependency, host mount or published port was used. All owned probe containers were removed.

Packaged commands: `QOPENBB_DATA_IMAGE=<exact local image ID> QOPENBB_DATA_EVIDENCE=<ignored output> pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/delivery/test_data_runtime_image.py -n0 --maxprocesses=2`, followed by the bounded installed-source/native probe. Both exited 0. Local packaged summary SHA256: `c64083cd69a80f2be7ed071bdcb6ce97625b22f7c884fa724d304446cbe8be0b`; installed-native report SHA256: `88b2ec5bbfdfd6275384116b694aae27a54d7e92934e6ec92170ac8d6c313a88`. Original publication checks remain under `artifacts/periodic-query-provenance/release/run-42231784072/`; packaged checks are under `task4-packaged-evidence/`. Raw logs, temporary containers' details and configuration directories are not public artifacts.

Use the [development install guide](../../../docs/install.md) for the prebuilt alpha. Historical company-selector server confirmation remains tied to its preceding release. This milestone introduces no new dashboard, calculation layer, Anthropic or Excel behavior.

## Final bounded acceptance, 2026-11-10

Independent Astra delivery re-review approved the corrected release links and deployment boundaries. Fresh read-only joins checked the recorded release, catalog and packaged evidence without repeating provider requests, image pulls or runtime tests. Review SHA256: `31ba5d478b681bd198e731e7e7a2870f103ddbf61e62513fe4f0f6d09e14abda`. All four amendment tasks are accepted; broader market-data scope, owner-server deployment of this alpha and IA-B readiness remain open.

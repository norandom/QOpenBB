# QOpenBB handover

Updated 2026-11-10. The native-development-workflow spec is accepted: **15/15 executable tasks**. Native Windows Docker/Compose through Podman, Dagger builds and Playwright have actual application and financial browser evidence. WSL is not required for this path.

## Accepted result

Financial acceptance covers Income, company selection, synthetic failure/recovery and actual retained-state recreation with fresh login. Cumulative attempted sends: 58 FMP / 6 FRED, within 80/16 limits. The owner authorized necessary requests for this verification without repeated prompts. No further run is needed.

Independent Astra review accepted financial and migration technical gates. Task 11.3 commit: `538a822`. See [migration closeout](artifacts/reviewed/native-development-workflow/native-migration-closeout.md) and [financial acceptance](artifacts/reviewed/native-development-workflow/financial-browser-acceptance.md). Linux CI at `e96d0e5`: 459 passed, 12 skipped, one live case deselected; CodeQL passed. Production pins and images were unchanged by the test-only AAP guard correction.

All six owned test sessions are stopped with zero containers/networks. Private state and failed-attempt evidence remain under D:/BuildArtifacts/QOpenBB. The owned Dagger engine/cache and unrelated projects were retained.

## Exact local image pair

- Workspace: `sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053`; source `e1a12c3a031a23598f41166a0f91b8fb24ac2387`.
- Data API: `sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807`; source `2e60c0a7aff039eda5f14a9d494beaec822fb9c4`.

These are locally qualified images. This migration did not publish a release or deploy the Linux server. Do not infer that moving `latest` includes them.

## Resume product work

The next bounded [statement-period provenance contract](.kiro/specs/market-data-integrations/statement-period-provenance-requirements.md) passed independent Astra requirements review. Owner requirements approval is recorded. The [bounded design](.kiro/specs/market-data-integrations/statement-period-provenance-design.md) passed independent Astra review after one repair round; owner design approval is recorded. The [seven-task plan](.kiro/specs/market-data-integrations/statement-period-provenance-tasks.md) passed a fresh independent Astra task-graph review. Owner task/implementation approval is recorded; task 1 source/native baseline is accepted; task 2 core contract is accepted at API b373da3f8d7 with 64 tests and independent review; task 4 consumer compatibility is accepted with 81 independent checks; task 3 FMP integration is accepted at API e78d87b2000 with 102 tests and clean 110-file gate. Task 5 source/native/live integration is next. Root test commits wait for the joined source-pin promotion before pushing, to avoid CI running new tests against the old locked core. Sources and provider-venv are under D:/BuildArtifacts/QOpenBB/statement-period-provenance; refresh installed packages after edits. Graph: preparation, core contract, parallel provider/consumer lanes, installed/live join, packaged widgets, milestone publication. Source review found Income derives classification from the query; Cash already discloses unknown duration. The existing FRED observation_provenance contract is series-specific and must not be repurposed for statement rows. Preserve completed sanitizer and periodic-query work. No provider calls or production changes were made for this contract.

Follow the [roadmap](docs/roadmap.md) and owning analyst/provider specs for the next investment-analysis slice. IA-A assessment and periodic-query provenance repair are accepted; broader IA-B financial compatibility and dashboard/model contracts remain open. Keep provider contracts separate from house modeling. Do not repeat completed infrastructure checks merely to refresh paperwork.

Use [native development guidance](docs/development.md) from the repository. Tool metadata: D:/BuildArtifacts/QOpenBB/native-foundation/resolved-tools.json. Native pipeline Python: that directory's pipeline-venv/Scripts/python.exe. Use `-B` and repository pipeline on PYTHONPATH. Keep builds, dependencies and disposable outputs under D:/BuildArtifacts.

Accepted continuation: D:/BuildArtifacts/QOpenBB/native-financial-remaining. Private raw reports/configuration must not be committed. Current owned Workspace checkout: D:/BuildArtifacts/QOpenBB/native-join/workspace. Root vendor/workspace is historical; do not overwrite the owned fork with it.

Unrelated dirty catalog work was excluded: .kiro/complexity-budgets.json, .kiro/complexity/workspace.json, pipeline/qopenbb_ci/catalog_cli.py, pipeline/qopenbb_ci/catalog_renderers.py and tests/contracts/test_renderers.py. Inspect and assign it before any future selective commit; do not revert it.

# Independent ordinary-grid capture task review

Verdict: **PASS**. Tasks 2.38-2.40 form an executable sequential branch from accepted 1.4 and 2.37. No task-local repair or return to design is required. This verdict approves the task graph for owner review; it grants no implementation approval and certifies no runtime behavior.

Review mode: independent, fresh context. Date: 2026-10-17. Reviewed inputs are frozen by SHA-256 in [mechanical.json](mechanical.json). The approved capture design hash matches the owning entry in spec.json. The reviewer's writable scope was `artifacts/grid-capture-tasks/review/**`; all other inputs were read-only.

## Findings

No blocking findings.

- Prerequisites are explicit. Task 2.38 establishes the finite fixture and actual Community GridApi environment before the adapter exists. Direct inspection confirms the existing `communityRealGrid.test.tsx` exercises real Community registration and filter/sort/value behavior. The application Vitest config already discovers the proposed tests, uses jsdom and one worker, and has no setupFiles. The root setup imports AG mocks and is correctly excluded. The application compiler currently lacks resolveJsonModule; its narrow controller-owned addition is explicitly assigned before fixture consumption. The locked AG Grid Community 34.1.1 installation in Debian exposes getCellValue publicly. No package installation, enterprise registration or new service is hidden in the task graph.
- Ordering and ownership are sound. 2.38 depends on accepted 1.4/2.37; 2.39 depends on 2.38; 2.40 depends on 2.39. Fixture/configuration freeze precedes adapter work. Sequential transfer of the actual-grid test avoids two writers. Shared types remain frozen; the controller owns compiler configuration, maintained inventory, source pins, breadth and evidence joins. No new task claims parallel safety.
- Each leaf has an observable deliverable and a credible 1-3 hour engineering bound within this approved slice: a passing fixture/environment gate; one adapter with deterministic and actual-grid tests; then the controller's combined verification/diff/identity gate. Existing compilers, suites, lint and complexity infrastructure are reused. Unexpected setup or production ownership changes return to controller review instead of silently expanding the leaf.
- Financial capture matches the approved design. Tasks preserve caller-resolved order, stable IDs, duplicate labels, zero/negative/fraction/null values, explicit units/scale and original range provenance. They require unformatted public GridApi values, forbid raw-data fallback and numeric coercion, and retain the accepted snapshot validator. Malformed input, ready-empty versus waiting, unsupported bounds/value modes and bounded failures have named outcomes and tests. Generation arbitration and undetectable caller transformations remain caller responsibilities under the frozen input.
- Integration obligations are preserved. The A1/A2 seam is explicitly tested. All chart-application and compatibility units, both strict compilers, scoped lint, current identities and whole-file complexity remain closing gates. Tasks do not infer application, editor, mapper, image, export or persistence acceptance. Numeric-only/general multiple-category/transformed/remote and unknown or mixed-unit joins remain separately gated. Anthropic-before-Excel remains unchanged.

## Independent checks

Command: `wsl -d Debian-MW -- python3 /mnt/d/Source/QOpenBB/artifacts/grid-capture-tasks/review/check.py`. Exit: 0. [Script](check.py) and [result](mechanical.json) are retained.

The merged preview contains 96 task IDs, including exactly three new unchecked leaves. All 69 numeric requirements remain mapped; there are no duplicate task IDs, unknown requirement references, missing explicit dependency targets or explicit dependency cycles. The three new leaves have boundaries, 1-3 hour bounds and observable completion bullets. Numeric ordering overrides are explicitly documented, so blocked historical renderer entries do not become prerequisites for this helper branch.

The draft appears exactly once in the merged preview. Outside that insertion, the diff changes two lane rows, three downstream blocker sentences and the A2 remaining-contract row. These edits keep 2.12, 3.8, 4.3 and the broader renderer/application joins blocked; no existing accepted checkbox or unrelated task content is altered. The original base and approved-design hashes are retained in the result.

Read-only environment probes initially encountered the Windows Python Store stub and missing Python in the default Debian environment. The explicit Debian-MW Python invocation above completed the mechanical check. A first WSL rg/API-location probe failed; grep against the actual Debian dependency tree confirmed the locked public declarations. These were reviewer tooling/probe failures, not product, implementation or test failures. No implementation tests, browser, build or installation ran. The parent's earlier preparation syntax/quoting corrections likewise do not constitute product-test evidence.

## Publication scope and frozen status

The small proposed publication set was read as text. It contains planning prose, existing task context, deterministic hashes, the preparation/check scripts and this review. No private environment file, credential value, account/database state, browser profile, authentication trace or runtime dump is included. Targeted private-key/token checks pass. The merged preview is a review copy of project task text; it is not a new runtime capture.

Explicit source allowlist for a reviewed evidence mirror:

- `artifacts/grid-capture-tasks/draft.md`
- `artifacts/grid-capture-tasks/merged-preview.md`
- `artifacts/grid-capture-tasks/mechanical.json`
- `artifacts/grid-capture-tasks/prepare.py`
- `artifacts/grid-capture-tasks/review/check.py`
- `artifacts/grid-capture-tasks/review/mechanical.json`
- `artifacts/grid-capture-tasks/review/review.md`

No other artifact is authorized by this review's publication allowlist. The controller must generate and verify the mirror's source/published hashes against final bytes before explicit selective staging. Future tasks.md/spec.json edits remain controller-owned phase records and must retain tasks unapproved and implementation unapproved for this new slice until the owner approves them. Existing unrelated inventory/catalog changes remain outside this review and publication set.

Reviewer edits are frozen after this report. No draft repair occurred; the one permitted task-local repair remains unused. Any later change to the reviewed draft or merge semantics requires checking the changed bytes against this verdict before publication.

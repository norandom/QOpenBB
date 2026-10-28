# Modeling foundation research and decisions

## Summary

2026-10-28. Discovery scope: new model repository with integration-focused inspection of the existing Workspace/data stack. Requirements are owner-approved. No runtime proof, package installation or repository creation accompanies this design.

- Existing custom-backend discovery and widget contracts can be reused; the financial engine need not be an OpenBB provider.
- Current gateway data routes do not establish authenticated Workspace identity for saved model ownership. The design introduces an explicit identity bridge.
- Structural schemas, financial contracts and independent arithmetic verification solve distinct problems and retain distinct evidence.

Consulted Kiro design/discovery/synthesis/review guidance, corporate-finance reference findings already recorded in the house reflection, and project complexity/testing/CI/delegation/documentation policies. Default product/tech/structure steering files remain absent; available project policies and approved requirements govern this design.

## Research Log

### Existing integration seams

Independent Sol explorer inspected these source paths:

- `vendor/workspace/terminalpro/src/lib/utils/validateBackend.ts`: backend-relative `widgets.json`/`apps.json` discovery with connector headers/query parameters.
- `vendor/workspace/terminalpro/src/lib/state/backendConnector.ts`: backend registration and endpoint changes.
- `vendor/workspace/terminalpro/src/components/DataConnectors/common/helpers.ts` and `src/lib/api.tsx`: endpoint resolution and widget transport. OmniWidget POST behavior is not the universal widget protocol.
- `vendor/workspace/lite/qopenbb-routes.conf.template`: existing data/agent proxy patterns, without authenticated identity bridging.
- `vendor/workspace/backend-api/backend/api/auth_helpers.py`: `GetCurrentUser` validates the Workspace session; it does not already issue modeling-service credentials.
- `services/data-api/qopenbb_data/app.py` and `compose.yaml`: no data-service auth wrapper; `OPENBB_API_AUTH=false`.
- `pipeline/qopenbb_ci/configuration.py`, `catalog.py` and `tests/contracts/`: reusable frozen-runtime/catalog checking; the current three GET datasets do not cover model POST execution or ownership.

Implications: add explicit modeling routes and contract checks rather than overloading data discovery. Use the existing session authority through a bounded bridge; do not trust public identity headers. Do not claim current data routes are authenticated merely because the installation sits behind Cloudflare Access.

### Schema and runtime contract foundations

- [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) describes HTTP operations and schema contracts. Use the 3.1 family as an interoperability target, not a claim that it is the latest specification.
- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/) supports schema generation from typed models. Generate structural contracts from authored boundary models; keep semantic definitions and consumer expectations explicit.
- [Python assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) documents removal under optimized execution. Production financial guards use explicit functions and typed outcomes instead.

Exact export dialect and consumer validator compatibility require an implementation check. No complete schema-subsumption algorithm or generated-type-only assurance is assumed.

The signed bridge assertion follows [JWT Best Current Practices, RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html): fixed algorithm, audience/issuer validation, explicit token type and a dedicated high-entropy key. This is a proposed integration, not an existing Workspace credential.

### Dependency candidates

The local data runtime lock contains Pydantic 2.14.1 and FastAPI 0.143.0; its manifest pins Python 3.13.15 and uv 0.12.5. These are candidate reuse baselines only. The new repository resolves its own supported exact lock and verifies packages under the protected install workflow; it does not import OpenBB to obtain framework dependencies. No live package compatibility or performance benchmark was run.

## Architecture Pattern Evaluation

| Option | Decision and rationale |
| --- | --- |
| Put formulas in FMP adapters | Rejected: provider lifecycle would own house methods and scenarios |
| Put formulas in widgets | Rejected: duplicated calculations and inconsistent future AI/Excel consumers |
| Mandatory modeling proxy for every dataset | Rejected: unnecessary coupling and failure propagation |
| Separate repo/service, pure domain modules | Selected: independent changes and releases, shared contracts and offline numerical verification |
| Separate service per financial method | Rejected for now: no demonstrated isolation or scaling need |
| General rule engine, broker and plugin runtime | Rejected for foundation: explicit trusted modules and immutable contract bundles meet the requirements |

## Design Decisions

Generalize the evaluation and check-result envelopes, not the finance formulas. A ratio, DCF and macro method can share validation lifecycle and provenance while retaining method-specific inputs, rules and reference calculations. Retain the user's three-history/five-forecast objective for a later model-specific spec.

Adopt schema libraries and HTTP standards. Build the small domain-specific method descriptors, financial check outcomes and consumer mappings that those standards cannot supply. Reference calculations remain independent from production helpers, even when both use Python.

Keep one model container, a small registry, synchronous bounded execution and atomic run files initially. A short-lived child process bounds expensive calculation without introducing a job queue. Persist exact run inputs and verification rather than relying on a CI badge as proof of arbitrary live results.

Choose immutable release-asset contract bundles pinned by source and hashes. Both repositories test against pinned counterpart contracts. No central broker is needed. Unknown impact broadens relevant checks instead of silently skipping them.

## Risks and Mitigations

- Authentication seam is new: bridge spoofing, expired-session and cross-owner tests precede deployment. The calculation core remains independent of identity implementation.
- Financial notes contain method ambiguities: keep the reflection's corrections ledger and model-specific approval gates; do not encode example values as expected truth.
- Library/schema versions can drift: independent lock and generated-contract drift checks; no dependency change implied by design publication.
- Decimal-to-chart conversion can lose precision: retain authoritative decimal strings and explicit display bounds; test projections separately from financial verification.
- Per-run independent verification costs work: bound execution and measure each method; never silently substitute a CI fixture result for run-specific verification.
- Repo handoff can duplicate ownership: move canonical modeling specs once, record the transfer revision and retain integration pointers in QOpenBB.

## References

The [approved requirements](requirements.md), [house reflection](../analyst-workspace/house-modeling-reflection.md) and [repository blueprint](repository-blueprint.md) establish scope. External references above support technical choices only; they do not prove QOpenBB integration or financial correctness.

## Owner-selected Polars and financial Python amendment

The owner selected Polars for model tables and requested idiomatic Python, finance-domain dataframe/table names and meaningful comments. The [conventions](python-finance-conventions.md) are part of the design and future repository steering. No provider-layer migration or package installation follows from this choice.

Official references checked on 2026-10-28: [expressions and contexts](https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/), [lazy execution](https://docs.pola.rs/user-guide/lazy/using/), [Decimal datatype](https://docs.pola.rs/api/python/stable/reference/api/polars.datatypes.Decimal.html) and [multiprocessing](https://docs.pola.rs/user-guide/misc/multiprocessing/). Use native expressions and explicit materialization; verify exact decimal operations in the pinned version. Spawn-based bounded workers avoid inherited native-thread state. The worker is an execution-limit boundary, not a claim that multiprocessing accelerates Polars.

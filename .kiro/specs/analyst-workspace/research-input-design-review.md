# Input-readiness design review

Decision: APPROVED for owner design review. Independent architecture and financial review completed on 2026-11-06 after one local repair cycle. No unresolved design blocker remains. This approval does not authorize implementation, establish live account access or close IA-A/IA-B.

Reviewed draft: `artifacts/research-input-readiness/design-draft.md`, SHA256 `dc5af3d18c1072437f3e14b240579f81c987129f31771bb00a822212fc2c504b` (193 lines). The decision applies only to these bytes. Requirements are the owner-approved `research-input-requirements.md`; approval metadata, not its older proposal heading, controls phase status.

## Mechanical gate

- All 24 numeric requirement IDs, 1.1 through 6.4, appear in the traceability table. Fresh extraction found no missing IDs.
- Boundary Commitments, Out of Boundary, Allowed Dependencies and Revalidation Triggers are populated. The file plan contains concrete paths with no placeholders.
- Native checks, shared execution support, DCF probes and assessment have explicit file ownership. No orphan component or boundary/file-plan mismatch remains.
- Planned files are test, evidence, documentation and status files. No production, lock, catalog, source-pin, service, model or widget expansion is implied.
- Test/documentation exemptions from production caps are correct. Any production delta requires a reviewed scope amendment and the existing inventory/checker with 400 physical lines/file, 300 logical units/file and 50/function limits.

## Repairs closed

The initial 183-line draft, SHA256 `cd860fb630abc2722a12b1570b74c55c753cdf2cfff20487a1dd38d5e6ebb818`, required two bounded repairs. Neither required a requirements amendment.

R1, shared execution and dependency contract: closed by lines 73 and 103-107, together with the request/error-budget contract. The design now assigns shared research-run state to the existing support layer, requires a common session state across native and direct probes, counts failed and successful attempts before transport, distinguishes provider-wide authentication/throttling stops from endpoint entitlement failures, enforces research timeouts, and separates affected baseline regression budgets. Company journeys resolve identity and obtain EV observations before deriving the bounded price request; they do not depend on pytest case ordering or refetch missing prerequisites. The selected EV receipt and listing remain attached to the date. DCF probes run sequentially within one test, with a usable custom baseline as the local beta prerequisite. The controller freezes this seam before parallel native/DCF work. These are concrete test contracts, not a new runner.

R2, assessment identity and consumer contract: closed by lines 125-133. Company records distinguish trading and reporting currency and retain exchange/source-qualified identity with missing reasons. Observation records bind exact existing widget IDs or a missing-widget reason to evidence and source identities. The next-contract record retains company controls, independent macro identifiers, period meanings, and saved research-context acceptance. Template identity round-trip remains an explicit downstream obligation when an App is packaged. The static record does not become a runtime/widget schema.

## Financial and scope findings

- MSFT, ORCL and ADBE form a bounded verification sample. Candidate peers remain distinct from provider suggestions and a curated comparable set; business/fiscal limitations remain review inputs.
- Annual/quarter labels do not prove discrete-flow duration, YTD treatment, restatement availability or point-in-time safety. Source/API equality is distinct from suitability. Negative, zero, missing and differently defined denominators remain unresolved or unsuitable.
- The DCF call is source-compatible with the inspected `get_data_many`/`get_data` transport. Installed-source absence, documentation, account access, assumption coverage and custom binding remain separate claims. No runtime validation occurred in this review.
- Three DCF probes satisfy the bounded feasibility design: standard, default custom and at most beta=1.0. A second beta scenario is unnecessary. An observed echo/binding of one parameter cannot establish sensitivity support, financial correctness or a native route.
- DCF currency, valuation date, custom forecast year and acquisition time remain distinct. FRED DGS10 is one Treasury benchmark, not issuer borrowing cost, WACC or a curve. Historical reuse preserves original dates and source identity.
- Assessment completion can coexist with IA-B input blockers; this slice cannot implement IA-B. Optional DCF access need not block unrelated raw/provider inputs. House formulas and methodological choices stay with financial-modeling. A raw/provider-data App cannot count as complete IA-B.
- Reusing pytest, the ASGI fixture, original callbacks and existing transport is appropriate. The 51-call ceiling has an explicit enforcement owner rather than relying on per-case counters or timeout defaults. No browser run or image build is justified for this design/test-only scope.

## Task handoff and evidence limits

Tasks must preserve the reviewed shared-state and receipt contracts before fan-out, name the actual selected pytest entry point/node IDs, and retain baseline behavior and source evidence. Implementation review must verify that native and direct cases truly share one state instance; importing fixture names alone is not evidence of that invariant. Every actual attempted upstream request must count, including failures, and dependent cases must record blocked/unexecuted states without recasting a failed required route as a pass. These are verification obligations under the approved design, not outstanding design repairs.

Read the design gate/principles; approved requirements; complexity, delegation, testing, CI, delivery and documentation steering; investment-analysis contract; both source-inventory reports; existing live test/helper source; underlying FMP transport; and prior live financial acceptance records. Core steering `product.md`, `tech.md` and `structure.md` are absent from the current steering inventory. Existing source evidence supports eleven native-table reuse paths and identifies the authoritative Workspace revision; it does not establish new UI acceptance.

This review performed source/document inspection and mechanical ID/hash checks only. No provider/network requests, runtime imports, tests, builds or maintained-file edits occurred. Only this ignored review artifact was written. Requirements/design/tasks/implementation phase approvals and independent implementation acceptance remain required.

# Company Research final integration review



## Validation Report



- DECISION: GO for bounded Company Research implementation and publication. Independent release approval closes criterion 6.4/task 5.3; all 13 executable tasks are supported for closure.

- REVIEWED SOURCE: root `fbd81eaf11d82b47043592f60736009304f198c8`, Workspace `bf180ef506286886da224df9ff184cd1ace2397e`, Data API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`.

- COVERAGE: all 29 original criteria mapped and accepted within the bounded source/runtime/publication scope, with the qualifications below. Criterion 6.4 has actual receipts and independent final release approval. Mapping alone is not acceptance.

- MECHANICAL_RESULTS: existing canonical affected-feature join PASS (Workspace 509/21 files; root 135 passed/1 skipped/3 deselected; separate peer adapter 10 passed); subsequent checked-writer verification 39 passed/1 existing skip plus six independent focused checks. These counts overlap responsibilities and must not be summed as a new suite. No new suite/build/live operation ran in this review.

- FRESH STATIC RESULTS: 41 bounded production/integration files, 3,759 introduced lines inspected mechanically against accepted discovery baselines; zero introduced TBD/TODO/FIXME/HACK/XXX and zero literal password/api_key/secret/token assignment-pattern matches. Exact paths/hashes are in `final-integration-static-evidence.json`. This is a bounded pattern check plus interface inspection, not a repository-wide security audit.

- SMOKE/INTEGRATION: the independently reviewed actual installed initial and retained journeys passed. No fresh runtime was started. Current application source pins match the executed images; later checkpoint-writer changes are separately tested harness work.

- BLOCKED TASKS: none in the bounded milestone. The inspected pre-closure source has twelve checked executable tasks; the final patch records the independently approved thirteenth. Group headings are not additional tasks.

- OWNERSHIP: LOCAL delivery closure for 6.4 is independently approved. Known whole-Workspace compiler/chart/schema/tooling baseline limitations are UPSTREAM/shared baseline; exact historical cellRangeCols ownership remains UNCLEAR beyond unchanged Workspace baseline.



This read-only cross-task audit applies `kiro-validate-impl` and `kiro-verify-completion`. It does not independently approve the documentation derivatives authored by this reviewer; the controller and independent publication reviewer own that final decision. Core product.md/tech.md/structure.md are absent in both inspected steering locations, as already recorded by earlier reviews. Existing testing, complexity, CI, delegation and documentation policies govern the scope. Project testing policy explicitly reuses identical verified inputs rather than rerunning unrelated suites for timestamps. Therefore this report does not claim the generic skill's whole-application full-suite gate is green.



## Evidence freshness and scope



Fresh Git inspection confirms the exact root above and clean working tree, plus the accepted Workspace pin. `workspace-joined.json` binds the canonical 21-file Vitest command to bf180ef and exit 0; its log records 509 passes. `root-contracts-final.json` binds the canonical seven-file pytest group to 2fad74f and exit 0; its log records 135/1skip/3deselected. A fresh restricted diff from that root to fbd81 shows only the separately reviewed checkpoint CLI and its new test in pipeline/contracts/delivery/contracts/tools scope. The original 135-test inputs were not silently changed. The exact three source/test hashes in `task4.2-final-review-hashes.json` still match current bytes, supporting reuse of the independent 10-test real-adapter suite and its separate configuration.



The final checked-writer review binds all four current file hashes, 39/1 author checks, 6 independent checks, strict TypeScript compilation, collection, and the full 741-file inventory with zero errors/violations. The actual financial run remains root 4736c31/browser c9a267, manifest 3e6f45, with the exact d00c17 Workspace/a91d48 API images recorded in `completed-runtime-review.md`. Fresh diff of that browser against current HEAD shows only the checkpoint-write call replacing direct writeFileSync with the checked writer. Financial/capture/state assertions are unchanged; browser 95192 is subsequent offline-tested source, not a second financial run.



The root exclusions remain explicit: platform-gated Linux acquisition skip; historical Linux Node-path fixture; opt-in image-backed catalog capture; Windows symlink/path-escape setup denied by privilege error 1314. The last is unverified, not passed. Whole application TypeScript is not green, and original/candidate app-schema cellRangeCols assertions retain the same established baseline failure. General chart and unrelated checker baselines are outside this bounded feature join. The accepted catalog admission review includes source-preservation, real-schema tests and generator-check evidence; it does not relabel an unexecuted image fixture as passed.



## Cross-task interfaces and dependency direction



1. Catalog → admission → native renderer: fresh inspection of `pipeline/qopenbb_ci/catalog_research.py` confirms exact five FMP widget IDs/endpoints, annual/limit 3 statement defaults, independent dates and an endpointless `company_research` peer declaration. Its five primary items join Symbol; only three statements join period; peers join neither. `backendValidation/nativeWidget.ts` exempts only the known renderer, absent endpoint and successful real schema. The renderer registry agrees. No broad endpoint exemption or dummy transport exists.

2. Selection → table query → evidence: `selectionReconciliation.ts` retains source-qualified saved identities, blocks foreign/unsupported identities and empty symbols, and enables ordinary observed linked changes/default resolution. `useTableData.ts` derives effective transmitted identity from the same group snapshot and gates requests; its context includes widget/dashboard/source/provider/symbol/query. `useEvidenceLifecycle.ts` clears retained evidence on context change and keeps only same-context evidence stale with its own failed-attempt time. Existing widget storage remains the sole persisted choice owner.

3. Peers → adapter → observations: `PeerResearch.tsx` stores validated versioned configuration only. `usePeerObservations.ts` uses the existing authenticated adapter, independent period/limit and `ttm=exclude`; at most two admitted jobs run, no polling, and removed/unmounted jobs cancel. Context/credential changes remount the run; peer reordering does not discard remaining admitted observations. Credentials are transient, not included in query keys or exported state. Schema limits 20 peers/2000-character rationale/limit 1–20 and exact source/provider/symbol duplicate rejection remain intact.

4. Envelope → inspector/peer presentation: `financialEnvelope.ts` validates metadata version/bounds/row attribution and preserves original rows, signed/missing values and source ordinals. Observation dates come from declared evidence, not cache clocks. `eligibility.ts` has no valid-comparable state, does not reconstruct denominators or convert currencies, and reports evidence-only reasons. Current peer UI intentionally remains unverified when applicability/denominators are unknown. Unit-tested conditional conflicts/nonpositive denominators are not presented as separately live-tested financial methodology.

5. Storage → export/import: `researchTemplateState.ts` verifies symbol/identity consistency, then calls the allowlisted `safeResearchExport`; config validation strips unsupported content and refuses credential-dependent source identities. Existing template creation/remapping and widget storage are reused. Neither financial payloads nor authentication state become persisted research configuration. Foreign saved identity requires explicit reselection, including same-symbol recovery local to each affected widget.

6. Runtime checkpoint boundary: new `checkpoint_cli.py` accepts bounded captured stdin, exact same-parent private filenames, ready runtime and matching image/name/container/stage; existing private storage owns exclusive creation. The bridge retains the configured interpreter and finite failure output. This is delivery harness prevention, not a new app database/authentication system. ACL correction did not weaken readers or alter executed frozen source.



The dependency graph remains catalog/declaration → shared identity/config/envelope → consumer controls/presentation → existing adapter/storage. No model service, provider route, house formula, state framework, new package or upstream provider-specific UI workaround was introduced. The shared-schema/backend validation extraction is a reviewed revalidation event: admission-repair-review.md records preserved exports, acyclic schema imports, selective native probing and actual generated-schema agreement. The local-date picker repair was independently reproduced and checked without altering the shared UTC table formatter. Both follow-up changes retain the intended seams rather than silently exempting an oversized owner.



## Original requirement mapping



W paths are relative to Workspace/terminalpro; R paths are relative to root. “Accepted” below means the bounded combined source/runtime evidence, not every case separately live-tested.



| Criterion | Joined implementation and evidence | Status / limit |
| --- | --- | --- |
| 1.1 | R catalog_research; W native admission/registry/PeerResearch; catalog/widget tests; installed six-section journey | Accepted |
| 1.2 | Existing frame/theme/navigation and export path retained; theme journey and template regression | Accepted preservation scope; no broad chart/edit/resize live certification |
| 1.3 | Table lifecycle and per-peer dataset status; frame/request tests; isolated stale 503 recovery | Accepted; not every entitlement variant live |
| 2.1 | Selection reconciliation/selector and primary-only group; actual name/symbol changes | Accepted |
| 2.2 | useTableData context gate and controlled late/clear query tests | Accepted; browser sequential changes are not the late-response test |
| 2.3 | Statement-only period group, original row provenance, quarterly journey | Accepted; labels do not prove duration |
| 2.4 | Separate date/period/peer parameters; real calendar edits and retained choices | Accepted |
| 2.5 | Exact primary whitelist, independent peer config, unrelated-table and peer tests; preserved peers across recovery | Accepted bounded isolation; no live macro request, FRED 0 |
| 3.1 | Financial envelope and observation inspector; metadata/value source matching | Accepted with explicit unknown fields |
| 3.2 | Statement row_index/source_ordinal and coverage parser; inspector/unit/runtime evidence | Accepted; no PIT/restatement inference |
| 3.3 | Original rows/signed/null retention; duplicate unit tests; labelled synthetic raw values | Accepted; duplicate selection need not be relabelled live |
| 3.4 | Provider value-origin/basis presentation and peer response matching | Accepted; no house calculation |
| 3.5 | Explicit missing/conflicting evidence reasons and unknown metadata presentation | Accepted; no inferred compatibility |
| 4.1 | Controlled PeerEditor identity/rationale/order; component and runtime persistence | Accepted; browser removal not separately claimed |
| 4.2 | Shared original-observation selectors and metadata labels across two peers/datasets | Accepted |
| 4.3 | Evidence-only conflict reasons, original inspectability, controlled eligibility tests | Accepted combined evidence; synthetic fiscal mutation is raw display only |
| 4.4 | Referenced-denominator checks with zero/negative/unsupported tests; persistent unverified UI | Accepted; numeric multiple does not establish denominator |
| 4.5 | No valid-comparable enum/aggregation/ranking; persistent peer warnings | Accepted |
| 4.6 | Separate analyst config and source lifecycle; stable job identity tests and runtime edits | Accepted |
| 5.1 | Fresh authenticated context equals saved state and validates current observations | Accepted |
| 5.2 | Retained recreation with checked handoff and restored exact state | Accepted; Workspace identity qualification below |
| 5.3 | Manual refresh retains selections/rationales and replaces current evidence | Accepted |
| 5.4 | Same-context stale/failedAt vs acquisition clocks; lifecycle/request tests and stale recovery | Accepted; exact clock semantics include controlled evidence |
| 5.5 | Configuration-only serialization/export and explicit save guidance | Accepted; not immutable snapshot |
| 5.6 | Actual export/download/import; UUID/group remap; foreign identity preservation/recovery | Accepted |
| 6.1 | Shared schemas/envelope, catalog/admission tests, source-bound contract join and inventory | Accepted bounded affected scope |
| 6.2 | Actual primary plus ORCL/MSFT, source-matched display, fixtures, refresh and financial review | Accepted |
| 6.3 | Separate retained phase and independent custody/content closure | Accepted local retained directory; no backup/restore/server claim |
| 6.4 | Actual CI/assets/six pulls bind source/image identity; independent publication review APPROVED; final mappings prepared | Accepted; controller applies closure record |



## Runtime and custody limits carried forward



Independent initial/reopen acceptance reports 54 required successful captures (45+9), final 291 FMP/0 FRED under 320, all denial categories zero. The accepted run consumed 89 from historical 202 (77+12), exceeding the 87 estimate by 2 but leaving 29. Historical failed attempts remain failed cumulative checkpoints. Nine initial and three reopen requested-only entries were not used by capture assertions; do not claim every observed request terminated.



The exact ACL-only repair and unchanged strict reader closed checkpoint custody/content review at SHA256 461b310e8437a82a8a309502e77c07b7ed88780a2517a42c109001066a4a1557. Preserve historical broader-DACL exposure, no pre-correction payload hash or byte-hash-equality claim, and no independently preserved initial Workspace inventory snapshot. API process identities are independently distinct but belong to a different service; initial Workspace provenance rests on executed runtime-context checkpoint and reopen inequality with current descriptor corroboration. Neither identity class substitutes for the other.



## Verification Result

- STATUS: VERIFIED.
- CLAIM_TYPE: FEATURE_GO.
- CLAIM: The bounded 29-criterion, 13-task Company Research milestone is accepted, including publication criterion 6.4/task 5.3.
- EVIDENCE: Fresh bounded source/interface/diff checks; exact-source canonical affected-feature tests; independent financial/custody/writer reviews; actual successful CI/assets/six anonymous pulls; independent final release approval.
- SCOPE: Bounded-feature GO under project affected-suite policy. Unrelated full-application compiler/chart/schema baselines are not green. Local financial images and public CI rebuilds retain distinct identities.
- CONTROLLER ACTION: Apply reviewed task/breadth/docs reconciliation and exact sanitized evidence entries. At the inspected source the final checkbox is not yet applied; completed evidence supports that administrative closure.

## Final publication evidence

[Independent publication review](publication-review.md) is APPROVED for criterion 6.4/task 5.3, SHA256 `0d6e2258ac66cb03bae66c5190bd31d55103f1b0479136e29ccc36b57782ccd4`. Actual verification receipt SHA256 `88396153f8285eb365fe9e2e98ff49545196a835c33e0d3d9347b05e45e6024d` binds alpha-43604526965-1 to root fbd81eaf11d82b47043592f60736009304f198c8 and accepted Workspace/API pins. Both CI jobs passed. Three anonymous assets match exact sizes/hashes, including default.env.sample. Six digest/tag/latest pulls passed source-label, config identity and linux/amd64 checks; final latest aliases matched at verification time. Independent review reconciled all 28 stages, 60 frozen inputs, empty auth files and parser-only Compose validation. The first failed verifier remains disclosed and preserved.

Published Workspace manifest is 5e456b5f84383f49eb3e9cbda85ec20c9006e31d18619be715e4743c7cc8b570; API manifest is fa113636cfb8a7df948053cfa39b8473e987ad68ab39ec54c0f079fa2909fac9. These differ from local financial-run config identities. No additional financial browser/provider/owner-server operation occurred. A later closure commit does not replace the build source.

No source, task, breadth, mirror, frozen runtime input or private payload was modified by this audit. Independent controller/Astra review owns acceptance of the public derivative and documentation I helped prepare.

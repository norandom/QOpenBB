# Company selector design review

Review date: 2026-10-30. Independent static architecture review, completed after two bounded repair passes. The bounded scope is criteria 1.1-1.5 in `company-selector-requirement.md`, not the analyst-workspace umbrella. No implementation, tests, provider calls, browser checks, build, network access or maintained-file edits were performed.

## Review Verdict

- VERDICT: APPROVED
- The final draft satisfies the bounded design review gate. All findings below are resolved. This is independent design readiness, not owner approval or implementation acceptance. The owner must still approve the design and explicit QueryParams exception before task generation; tasks and implementation remain separate gates.

## Mechanical checks

- Numeric IDs extracted from the confirmed requirement note: 1.1, 1.2, 1.3, 1.4, 1.5. Each appears in the traceability table; no missing IDs.
- Boundary Commitments, Out of Boundary, Allowed Dependencies and Revalidation Triggers are populated.
- File Structure Plan contains six new production paths, two modified production paths and two focused test paths; root E2E reuse is explicit. No TBD placeholders.
- All new responsibilities map to files. Existing DS, GroupDropdown, CompareTermsParam, stores and acquisition helpers are reuse dependencies, not orphan new components. The file boundary is appropriately narrower than the global app/schema/provider layers.
- Final typed ports define selection, request, search state/error, group context/decision and commit outcomes without new `any`. The exact eight widget/native endpoint/multiplicity bindings match the committed catalog. Production paths resolve under `terminalpro/src`; focused unit test paths resolve under `terminalpro/tests/unit` and the existing test runner.

## Criteria coverage

| Criterion | Concrete coverage | Final disposition |
| --- | --- | --- |
| 1.1 | Remote name search, paired UI, alternative identity display | Native envelope, nullable name and bounded alternatives defined |
| 1.2 | One local parameter/metadata update | Same-symbol metadata-only and changed-symbol execution paths defined |
| 1.3 | Symbol search, exact group guard, preserved comparison | Reactive/latest local/shared membership and preview isolation defined |
| 1.4 | Source-qualified identity, no false exchange discriminator | Exact bindings, source identity, private cache generation and ambiguity behavior defined |
| 1.5 | Sibling storage, strict decoder, save/reopen/recreation plan | Forced origin persistence, invalidation and retained-state acceptance defined |

## Resolved findings

The following findings describe the initial draft and the required repairs. The final draft resolves all four; no IMPORTANT finding remains open.

1. **Typed integration contracts.** The final draft adds selection/search/group/commit interfaces and discriminated outcomes, eight concrete bindings, nullable-name behavior and private per-selector authentication/cache generation. Native responses are decoded at `extra.results_metadata.__qopenbb_financial__`. A source-checked correction validates query/limit in `effective_query` and search mode through `source.endpoint` (`search-name` or `search-symbol`); it explicitly avoids requiring the absent `effective_query.is_symbol` field.

2. **Compound commit and execution.** The initial draft did not handle `syncParams` returning early for unchanged symbols or edited manual-run instances. The final design extends the real seam, commits same-symbol metadata without a new financial query/copilot execution, and preserves ordinary updates, refs, draft synchronization and SSRM reset. It explicitly retains the original renderer for manual-run variants. Group commits write once through the existing group writer, then invoke the origin compound update; partial failure does not claim rollback or atomic identity.

3. **Reactive group safety and preview isolation.** The final design requires reactive local/shared widgets and groups, synchronous latest-context validation and all-member competing-binding checks. It avoids the current stable-getter subscription trap. The current override preview caller's `isPreview=true` was verified directly; real dashboard membership is an additional guard, and new override callers require revalidation. Existing update callbacks retain permission/override behavior without an invented capability API or direct store bypass.

4. **Narrow layout.** The final design moves only the eligible Symbol editor/group/comparison controls into a dedicated auto-height below-navbar host with portal results, leaving legacy fixed-height hosts unchanged. This addresses the initial clipping gap without modifying DraggableCard or global layout classes. Its integration delta is included in the revised explicit exception proposal.

## Exception assessment

The final proposed QueryParams-only ceilings are 1000 physical/390 logical/50 per function, against the measured 938/345/max38 baseline. The initial proposal was 970/370/50; the explicit revision adds room for the required auto-height host and compound/unchanged-symbol plumbing. The bounded allowance is 62 physical and 45 logical units; search, decoding, eligibility and safety logic remain in capped modules. The other changed hook is 142/69/max11; all new/other changed production paths remain 400/300/50. A full QueryParams split would pull unrelated execution, endpoint and Period behavior into scope. The exception is a reasonable design proposal, not an automatically accepted counter bypass.

The repaired seam/layout is concrete enough for bounded task generation after owner approval. Actual fit is an implementation acceptance check: require candidate revision and measured source binding, expiry 2026-11-30, real inventory/checker enforcement, and a stop for revised design if integration exceeds the ceiling. No active exception or runtime change is authorized by this review.

## Evidence and limits

Final reviewed draft SHA256: `cc49b22b4276e43ebd39354301cfda7e54f2576a78e975f7164bfc72855baaeb`. The initial draft was `c490f14d409be3eda8d0c56fd267512165d8a95d5b19896af95e834b47acaf2c`; first repair was `6d7c5b0feed14558c4d65d29ce800d1201248b7f3434366153d6877441afc833`. Workspace HEAD is `c652b909627d7634241eee2ed13a561fbb4f177b`; Data API HEAD is `28423762e8cc3faae978e770899834b41e7cde99`. Fresh hashes of both modified-seam source files match the baseline parser receipt at `artifacts/company-selector-design/baseline.json`.

Inspected the draft, requirement/research note, design review gate/principles, delivery/delegation/complexity/testing/documentation steering and retained parser receipt. Source checks included QueryParams, useParamGroupBindings, group store writer/readers, getEndpointParamRequestArgs, GroupDropdown, widget update/subscription persistence, FMP search/discovery models and the committed native widget catalog. The eight catalog definitions all currently have runButton=false; only Profile exposes multiple symbols. The existing local/shared group writer is real and can be reused. Strict sibling storage and guarded display metadata avoid contaminating financial requests.

This is static design evidence only. Real FMP, browser accessibility/layout, stale-response, same-symbol commit, compatible/incompatible local/shared groups and retained-state recreation remain future implementation acceptance.

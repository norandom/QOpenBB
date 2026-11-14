# Company Research amendment review

Verdict: REJECTED. Three Important findings require a focused documentation repair and re-review before task-plan acceptance. This review does not approve implementation.

Reviewed 2026-11-14 by independent agent `/root/amendment_review`, using the evidence and boundary checks from `kiro-review`. Scope is the owner's task-plan and modeling-reflection amendment, not completed implementation. No project files were edited.

## Exact review identity

| Artifact | SHA-256 |
| --- | --- |
| Current `company-research-tasks.md` | `f1667f689f5deb4bf52b7888daa75203d12333ff6abd43d14a10ac3199b749de` |
| Current `house-modeling-reflection.md` | `a79170be93806a57331e0561969e4938770d8c689bc90ed80b6105a03915c4a6` |
| Historical reviewed task draft | `b532b90321cdf83c0b426d58fe31980c0d0620d38ed37c5f90eb753b3ba3a67a` |

Working-tree amendments were compared with Git HEAD `1b31e77fa0293649ce82eefb4f6f023bcbb530a1`. The original `company-research-tasks-review.md` PASS remains valid only for its historical hash. Nested `spec.json.next_workstream.company_research` retains `tasks_approved=false`, `implementation_approved=false`, and `completed_tasks=0`.

## Required repairs

### 1. Important: SBC presentation lacks an explicit supplied-evidence gate

Sources: `house-modeling-reflection.md:117-123`, `company-research-tasks.md:53`, `company-research-tasks.md:113`, and `company-research-tasks.md:123`.

The reflection states that SBC is added back under OCF/FCF and provider or management Adjusted EBITDA, then defines the reported/provider view as SBC added back. That is an unconditional basis claim. The task wording asks the inspector to disclose SBC treatment without explicitly requiring source evidence for that treatment. Taken together, these permit a field-name-based add-back label even when the accepted envelope supplies no such basis. A returned SBC field alone does not establish its treatment within a different reported/provider measure. A downstream subtraction could also count the same cost twice if the starting measure already includes it.

This conflicts with requirements 3.1, 3.4 and 3.5; design lines 97-114 require unavailable basis to remain unknown and eligibility to present supplied evidence only. The reflection itself says at line 147 to review SBC and other add-backs individually.

Minimal repair wording for tasks 2 and 4.1: "Preserve returned SBC and related fields and supplied basis/transformation/limitation metadata. Label SBC as added back only when the source definition or supplied reconciliation establishes that treatment for the selected measure; otherwise show SBC treatment as unknown. Do not infer treatment from a field name, another statement field, or a generic non-cash label. No house adjustment is calculated in this slice."

Minimal reflection repair: make the reported/provider view retain the actual supplied treatment, including unknown treatment; make proposed economic-cost adjustments conditional on a documented starting basis, explicitly preventing double subtraction. Keep the SBC cost/dilution/buyback lens as a future house-method proposal. Add focused cases for evidenced add-back, evidenced retained expense and unknown treatment to task 2/inspector verification.

### 2. Important: currency and EV-bridge rules are broader than the comparison contract

Sources: `company-research-tasks.md:51-52` and `company-research-tasks.md:123`.

Task 2 directs cross-row or trading/reporting currency conflicts to `incompatible`, and directs any numeric multiple missing EV-bridge fields to missing-bridge status. The approved design says incompatibility is "for the stated comparison" (line 110); requirement 4.3 applies only to a required compatibility fact. Currency differences between separate observations are facts to preserve, but do not establish a conflicting numerator/denominator basis for every dimensionless provider ratio. Likewise an equity multiple does not acquire an EV bridge requirement merely because it comes from the same metrics endpoint as EV multiples. All observations still remain unverified for aggregation; this finding concerns truthful reasons, not introducing a valid state.

Minimal repair wording for tasks 2 and 4.2: "Determine which evidence is applicable to the selected measure and stated comparison from supplied definitions. Mark `incompatible` only for explicit conflicting required unit, currency, date, coverage or claim-scope evidence; otherwise retain differences and unknown applicability explicitly. Require EV-bridge evidence only for an EV-based measure/comparison, and name only missing applicable evidence. Do not reconstruct denominators, bridges or currency conversions. Apparently matching observations remain unverified for aggregation."

Add cases distinguishing an explicit currency conflict within a stated monetary comparison from different reporting currencies across dimensionless provider observations, and EV-based versus equity-based evidence reasons. Unknown definitions remain unknown rather than receiving an assumed method classification.

### 3. Important: the shared request predicate has no executable early owner

Sources: task ownership table lines 25-28, suggested dispatch line 36, task 2 line 54, task 3.2 lines 73 and 78, and task 3.3 lines 82-88.

Task 3.2 must synchronously consume a shared identity-reconciliation predicate before selector mount, yet it depends only on task 2, which freezes its interface without naming an implemented predicate location. `selectionReconciliation.ts` belongs to the later task 3.3. The suggested dispatch completes 3.2 before 3.3. This leaves the query lane choosing between an unavailable implementation, out-of-boundary edits or duplicate reconciliation logic. It is exactly the hidden shared dependency disallowed by delegation lines 20-22.

Preferred minimal repair: assign the pure identity classification/request-eligibility predicate and its exact module to task 2, implement and test it there before fan-out, and have both tasks 3.2 and 3.3 consume it. Make task 3.3 own only selector integration and any separately named selector-only helper. Update the ownership table and design file responsibilities for that narrow ownership clarification. Explicitly cover absent versus malformed/unknown/foreign saved metadata, effective-symbol/source agreement and deliberate same-source group changes. An alternative is making 3.2 depend on completed 3.3 and changing the dispatch schedule, while keeping a single predicate owner.

## Checks and nonblocking conclusions

- The 13 executable tasks still cover the 29 requirement IDs; task containers are not executable items. Scope excludes financial calculations, AI/Excel, a model service and owner-server deployment.
- Production completion criteria consistently retain 400 physical lines/file, 300 logical units/file and 50/function. Task 1 establishes measured baselines, executable inventory scope and explicit fork manifests. Query/export extraction and final shared-module audit remain explicit; no implicit size exception was introduced.
- The 1-3 hour work-unit target is conditional on measured scope and a required pre-dispatch split. Expanded task 2 and selector extraction should be re-sized at task 1 against actual logical/function baselines; historical physical counts do not prove compliance.
- Synchronous request gating, malformed-import preservation, explicit export defaults, renderer registration, two-request concurrency, cancellation/retry accounting and native runner/login-budget reuse align with the design in intent. These additions need implementation evidence later, not runtime tests during this document review.
- `git diff --check` passed for the three amended spec files. Placeholder scan found no TBD/TODO/FIXME/HACK/XXX markers. Exact hashes match the handover. No runtime tests, RED-phase evidence, builds, installs, provider requests or browser operations were appropriate or performed; they are N/A for this task-plan amendment review.

Review sources: root `AGENTS.md`; `.kiro/handover.md`; `.kiro/steering/delegation.md`, `documentation.md`, `complexity.md`; `.agents/skills/kiro-review/SKILL.md`; the current Company Research requirements, design, tasks, original task review, reflection and nested Company Research metadata. Financial findings are consistency checks against the approved evidence-only contract, not a new financial-method specification.

Preserve the original review receipt. Record this rejected amendment separately, repair only the affected contracts/wording, and bind the next review to newly computed hashes. Owner task and implementation approval remains pending.

# Task 2 identity decision

Decision: RETRY_TASK after recording the clarification below. No owner decision is required to preserve the explicitly approved existing identity contract. Apply the same identity rule to primary company and peers.

ROOT_CAUSE: The design phrase “absent listing identity” was read as “listingId is null.” Those are different states in the explicitly reused CompanySelectionV1 / ListingChoice contract. Its nullable identifier records missing optional evidence; the connector source, provider and exact single provider symbol retain usable request identity. This does not establish issuer, exchange or cross-source equivalence.
CATEGORY: CONFIG_GAP (contract wording ambiguity, resolvable within approved reuse intent).
CONFIDENCE: HIGH.

## Evidence

Paths below are exact inspected source evidence; tests were read, not executed by this review.

- Canonical requirements `D:/Source/QOpenBB/.kiro/specs/analyst-workspace/company-research-requirements.md:30` asks for available listing/exchange identity; line 50 requires source-qualified peer identity; line 66 requires unavailable identities remain unresolved.
- Canonical design `company-research-design.md:61-69` explicitly declares nullable listingId; line 89 explicitly requires reuse of CompanySelectionV1 / ListingChoice and preservation of nullable listing evidence. Line 91 requires unresolved/foreign/unsupported saved identity protection and retains ordinary same-source resolution behavior.
- Accepted Workspace `terminalpro/src/components/General/Table/NavBar/companySelection.contract.ts:133-155` accepts null listingId and issuerId. Lines 180-185 validate sourceKey, provider and exact symbol, without requiring a non-null listing ID. Lines 188-199 state unknown identifiers establish neither equality nor contradiction, reject known contradictory alternatives and resolve an exact provider symbol.
- `companySearch.ts:64-75` maps absent source listing_id/issuer_id to null and passes that through the existing decoder.
- `useCompanySelection.ts:57-88` accepts a selected current-source result only after contradiction and group checks; `companyGroupSafety.ts:33-48` requires eligible members of the same provider/source. Neither requires a vendor ID.
- `terminalpro/tests/unit/company-selection.test.ts:15-31,49-63,87-90` uses BRK.B with null identifiers as valid saved selection. Lines 190-221 explicitly resolve that symbol, allow nullable identifiers, and reject contradictions across listingId, issuerId, exchange, exchangeShortName and currency.

Accepted Workspace root: `D:/BuildArtifacts/QOpenBB/company-research/workspace`.

Correction to the blocker premise: accepted Data API search does not necessarily emit null listing_id. `D:/BuildArtifacts/QOpenBB/company-research/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_search.py:52,81-88` uses FMPDiscoveryIdentity and validates every result. `discovery_data.py:60-66` constructs a locally qualified identifier from symbol plus exchange, or an explicit unknown exchange suffix. This is a locally derived identity, not proof of a vendor-issued unique listing identifier. Frontend null support remains an intentional accepted contract, independently of that backend behavior.

## Minimal clarification and implementation contract

Replace only the ambiguous sentence at design line 89 with wording equivalent to:

> Source-qualified request identity uses connector source key, provider and exact single provider symbol, retaining provider listing ID and other listing evidence when supplied. A null optional listing ID is allowed by the existing ListingChoice contract and does not itself make the selection unresolved. Missing/invalid source or symbol, unsupported saved identity, or known contradictory listing evidence remains unresolved. Neither null identifiers nor equal symbols establish cross-source, cross-exchange or issuer equivalence. Apply this rule to both primary and peer selections.

Preserve the distinction between schema validity, current-source/request eligibility and financial comparison eligibility. A valid imported identity from a foreign source remains saved and visible but cannot query the current source until explicit recovery. Unknown-version/malformed saved objects remain unresolved; absent metadata is a different state and retains initial-default resolution. Known ambiguous search alternatives remain blocked by the existing contradiction checks. Do not infer ambiguity merely from a null optional ID, and do not claim a saved single record proves that no unseen alternatives exist.

For peer uniqueness, retain all supplied identity evidence. Reject repeated entries that would issue the same source/provider/exact-symbol request instead of silently merging them or treating differing IDs as independently queryable listings: the native financial request cannot discriminate exchanges for one symbol (contract lines 188-194). Describe duplicate rejection as a request/configuration constraint, not proof of security equivalence. Preserve original invalid imported JSON and explain the duplicate or contradiction. Distinct source keys must not be collapsed by matching symbols or IDs; current-source execution checks still apply.

## Task 2 split review

The approved task plan explicitly permits splitting before dispatch (`company-research-tasks.md:9`). A bounded 2a/2b split is consistent with the existing task 2 acceptance boundary, provided the controller first stops/reconciles the original worker and records exclusive ownership before redispatch. No lane 3.x may start until BOTH parts pass independent review and the shared freeze gate.

- 2a: identity/configuration only. Exclusive production ownership `src/lib/companyResearch/config.ts` and `selectionReconciliation.ts`; dedicated config/reconciliation test files. Own source-qualified adapter, configuration limits/duplicates, unresolved vs absent classifier, deliberate linked transitions, and shared request predicate. No financial parser/status implementation.
- 2b: financial evidence only. Exclusive production ownership `src/lib/companyResearch/financialEnvelope.ts` and `eligibility.ts`; dedicated envelope/eligibility test files. Own original rows/ordinals, nullable metadata/date/basis evidence, currency semantics, denominator/EV/SBC reasons and no valid-comparable result. No identity implementation.
- Before parallel execution, controller freezes the few cross-part type signatures and renderer/lifecycle/export declarations. 2b must not edit or await a moving 2a file; if a type import is necessary, freeze that declaration first. No new shared file owned by both workers.
- Controller owns task-plan wording, shared declarations, inventory changes, manifests, commits and join. Keep at most two implementers plus one reviewer. Every production file/function retains 400 physical / 300 logical / 50-function caps. Serialize heavy checks.
- Acceptance of task 2 remains conjunctive: both scoped checks and independent financial/integration review, complete changed-file complexity verification, frozen consumer signatures and a shared regression check of primary/peer identity consistency. Downstream tasks still depend on task 2, not merely 2a or 2b.

## Verification required on retry

Add focused primary AND peer cases for valid same-source null listingId, null names, known contradictory alternatives, duplicate request identity, foreign source, invalid/unknown saved metadata, and no silent import substitution. Verify genuine linked symbol changes separately from first mount/reopen; explicit current-source reselection must recover. Retain existing company-selection/search tests as regressions. Run 2a and 2b focused suites and the existing scoped complexity checker; this source review itself makes no test-pass or implementation-completion claim.

NEXT_ACTION: RETRY_TASK. No source or specification files changed by this review. Report is external; root checkpoint was not overwritten.

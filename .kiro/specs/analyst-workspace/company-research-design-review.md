# Company Research design review

PASS after one local repair. The selector reconciliation seam now preserves unresolved saved identity until explicit reselection. The design is ready for owner review; this does not authorize tasks or implementation.

Reviewed 2026-11-13. Independent architectural and financial review; source inspection only. No runtime, tests, provider calls, builds or source/design edits were performed.

## Reviewed identities

- Requirements SHA-256: `71c0d50c5fdec2247d35543694f478dc531893e88e0357e2db5fde6410ed7df4` (matched).
- Final reviewed draft SHA-256: `2d15e3f309fff9eee00ab964bc91448a414ddee472f2f045f0e120c5358cc291`. Repair count: 1.
- Accepted Workspace: `e1a12c3a031a23598f41166a0f91b8fb24ac2387` at `D:/BuildArtifacts/QOpenBB/native-join/workspace`.
- Accepted data API: `a965f70c164fe477ce9c99654b9be48e2f1bc9fd` at `D:/BuildArtifacts/QOpenBB/statement-period-provenance/data-api`.
- Read the supplied state discovery, approved requirements, delegation/complexity/documentation steering and design-review gate. Targeted accepted-source reads checked selector behavior and the financial metadata contract.

## Mechanical gate

PASS. Extracted all 29 numeric acceptance IDs from requirements; every ID appears in the traceability table. All four boundary sections are populated. The File Structure Plan contains concrete root/Workspace paths, no placeholders, and responsibilities consistent with the stated slice. Proposed components have file owners. Existing APIs, persistence, group helpers and controls are explicitly identified as reused infrastructure.

## Repair history

### R1: High, resolved in repair 1 - automatic selector resolution can replace an unresolved imported identity

Affected criterion: 5.6; related protection: 2.1 and 2.2.

The draft requires explicit reselection when an imported identity no longer resolves, but relies on primary table request gating while retaining the existing selector. That gate does not control selector metadata writes.

In accepted Workspace `terminalpro/src/components/General/Table/NavBar/useCompanySelection.ts`, lines 133-144 discard invalid/current-context-mismatched metadata as the active selection. Lines 205-227 then automatically search the current source by the existing symbol when no active selection remains. Lines 255-271 accept an exact-symbol result for that current source and call `commitLocal(next)`. `QueryParams.tsx` lines 411-425 feeds the stored selection into this hook and persists the replacement through the existing metadata-only path. There is no check preserving the imported identity's original source in this auto-resolution path.

Concrete counterexample: import an App carrying a saved source-A company identity into a widget now bound to source B, with the same symbol available there. A table-level source check can initially disable data, yet the selector can automatically replace A's metadata with B's result. The table then sees a coherent current-source selection and can run without the analyst explicitly reselecting. The stated unavailable-identity guarantee is lost.

Bounded repair: add an explicit reconciliation policy and owner to the design. A focused change to the existing selector hook, optionally with a small helper module, must distinguish ordinary absent metadata and legitimate linked-company changes from unresolved imported/saved identities. Preserve the latter's readable saved identity, suppress automatic replacement and provider execution until explicit reselection, and state how that explicit action clears the unresolved condition. Add these paths to the File Structure Plan and carry the 400 physical / 300 logical / 50-per-function caps. The 311-line hook offers a bounded integration seam; this finding does not require editing oversized QueryParams, generic import/state schemas or the backend.

The planned deterministic/browser cases should include same-symbol source mismatch, malformed saved metadata, absent metadata on a new default App, normal primary group propagation, and explicit reselection recovery. These are later implementation checks, not evidence already obtained.

## Other judgments

PASS. Financial boundaries are appropriate: original rows and nullable facts remain inspectable; signed/duplicate values survive; no inferred denominator, duration, currency conversion or house ratio is introduced; no valid-comparable state is offered. The accepted API contract supplies schema version 1, `retrieved_at`, field metadata and optional `statement_provenance`; absent evidence remains unknown. The original-row inspector avoids pretending transformed grid cells retain one-to-one source attribution.

Configuration ownership, parameter-group separation, price-window independence, request context isolation, two-request peer concurrency, same-context stale presentation and configuration-only saving are sufficiently concrete for bounded tasks. Safe export is an allowlist projection with credential-bearing identity refusal; it does not dump widget storage. The serializer extraction, unchanged oversized import/state files, executable inventory extension and final shared-module audit honor the complexity policy. Role-based lanes freeze shared contracts before fan-out and retain independent financial review.

No additional architecture, provider, financial method, verification framework or runtime prerequisite is requested. Runtime claims remain explicitly pending. Targeted second-pass review confirms the design names both `useCompanySelection.ts` and `selectionReconciliation.ts`, suppresses automatic resolver and metadata commits for unresolved saved identities, preserves raw identity through save/reopen, and permits explicit current-source reselection to clear the condition. Ordinary same-source group changes and initial absent metadata retain current behavior. There is no second persistent selection owner. Whole-file caps and targeted recovery/regression checks are explicit. R1 is closed at design level; implementation behavior remains to be demonstrated.

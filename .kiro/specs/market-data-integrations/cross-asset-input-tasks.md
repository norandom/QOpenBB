# Cross-asset and macro input verification task plan

Status: task plan owner-approved, 2026-11-18, including the 26 planned route calls. Amendment, 2026-11-18: those calls cause 34 provider requests (18 FMP, 16 FRED), because each FRED series call makes two. Follows the [design](cross-asset-input-design.md) and the approved [requirements](cross-asset-input-requirements.md). The owner set no fixed request cap; every send is recorded.

## Execution contract

Work in `D:/BuildArtifacts/QOpenBB/fmp-expansion-b/root`; private evidence goes under `D:/BuildArtifacts/QOpenBB/cross-asset-inputs/evidence`. Tasks run in order. Each task needs independent review, fresh scoped verification, recorded evidence and a selective commit. This slice produces tests, contracts, documentation and evidence, which are excluded from production caps. Any production change stops the task and returns to the owner, and would need fresh 400/300/50 verification.

## Tasks

- [x] 1. Freeze the request matrix and the result-record contract
  - Write the 26-call matrix from the design with exact symbols, series, windows and purposes, and list the provider requests each call causes. Add the JSON schema for `docs/reference/cross-asset-inputs.json` and a contract test that requires all 14 inputs and rejects a copyrighted input marked usable.
  - Seed the record with every input as `unverified`.
  - _Boundary: Controller · matrix, schema, tests/contracts_
  - _Requirements: 4.2, 5.1, 5.5_

- [x] 2. Derive the guarded harness and rehearse it offline
  - Derive the send guard from the reviewed Batch B harness. Count FMP and FRED sends separately, one armed slot per send, with no slot for any other host. Run the matrix inside the published data image with no network and synthetic responses: zero sends, zero denials.
  - Add guard unit tests for unarmed sends, reused slots, wrong host and wrong query.
  - _Boundary: Controller · private harness under evidence_
  - _Depends: 1_
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 3. Write the independent comparison oracle
  - Standard library only. For prices: row-by-row equality with the raw capture, date ordering, duplicates, weekday gaps, earliest and latest dates. For FRED: values, missing observations kept missing, metadata fields. For identity: each attribute a value or unknown.
  - Test it on synthetic captures, including a deliberate mismatch, a gap, a duplicate and a missing observation.
  - _Boundary: Controller · private oracle under evidence_
  - _Depends: 1_
  - _Requirements: 1.1–1.4, 2.1–2.4, 3.1–3.3_

- [x] 4. Review the frozen harness before any live send
  - Independent review of the matrix, guard, rehearsal results and frozen identity. Acceptance binds the image digest, matrix hash and harness hashes. No live request before this approval.
  - _Boundary: Reviewer · read-only_
  - _Depends: 2, 3_
  - _Requirements: 5.1–5.4_

- [x] 5. Run the live matrix once
  - Start the published data image alone with the installation's FMP and FRED keys, server-side only. Execute the 26 calls. Stop an input's remaining calls on an entitlement denial. Record every send, capture and outcome; a rerun needs a recorded reason and a new slot.
  - _Boundary: Controller · live runtime and private evidence_
  - _Depends: 4_
  - _Requirements: 2.3, 3.1–3.4, 4.1, 5.1–5.4_

- [x] 6. Compare results and review the financial meaning
  - Run the oracle on the captures. Fill the result record from its output: identity, price basis, history, display status and verification state per input. Independent financial review checks every statement against the evidence, including that an ETF is not described as a spot price or index.
  - _Boundary: Controller and reviewer · result record_
  - _Depends: 5_
  - _Requirements: 1.1–1.4, 2.1–2.4, 3.1–3.4, 4.1–4.3_

- [ ] 7. Reconcile documentation, breadth and the sanitized mirror
  - Add the cross-asset and macro inputs checkpoint to `docs/provider-coverage.md`, with the FRED notice. Update README, the docs index, the roadmap and `.kiro/breadth.toml` for verified scope only. Mirror the reviews and a sanitized summary; verify hashes and the absence of credentials and raw provider rows.
  - Check-only CI must pass at the final source. No image build.
  - _Boundary: Controller · docs, breadth, reviewed mirror_
  - _Depends: 6_
  - _Requirements: 4.4, 5.4, 5.5_

# Nightingale chart parity

Restore Nightingale in the existing Table/File chart workflow. The owner authorized continuing this milestone after Radar on 2026-10-24. Keep the accepted Radar alpha and the running local Compose installation unchanged during development. Radial Column/Bar and other chart families remain later milestones.

## Acceptance contract

1. Preserve the original Nightingale gallery choice, Set Up/Customize controls, themes, widget framing, flags and saved configurations. Do not add another editor or hide existing actions.
2. Match original field/category selection, displayed order, grouping/stacking/normalization, aggregation, inversion, negative/zero/missing values, duplicates and legend effects. Establish numerical radius/angle semantics from original behavior; the chart name alone does not establish area-proportional encoding.
3. Reuse the existing capture, session, stamp, reducer, persistence, theme and native-host owners. Preserve reachable axis, series, label, tooltip and navigator controls according to observed original behavior.
4. Verify an identified packaged application using retained real FMP records: exact amounts, units and fiscal periods, visible geometry/tooltips, controls, light/dark appearance, refresh, fresh-session reopen and PNG export. Compare matched views with the original; ask the owner about uncertain visible differences in qView.
5. Keep per-task independent review and commits, updated README/docs checkboxes and breadth mapping. Publish selected real-data samples. Dispatch one image pipeline only after the complete milestone is accepted; verify tagged release assets and both public images separately from local browser acceptance.

## Design boundaries and unresolved questions

Original frontend: 38dffc33389aca0e4a87e0e88d42f7067aa220df. N0 Workspace source: 5fd57cf6d22893b5a26510a6ba3f25726a4386d5. Current published alpha: alpha-40086673952-1. The [adapter contract](nightingale-contract.md) and [N0 review](../../../artifacts/reviewed/chart-nightingale/n0-review.md) are accepted. One original browser journey, source semantics and retained FMP reconciliation support the inactive interfaces; replacement application acceptance remains open.

Group Type is stored at model root, with linear radius and separate signed stacks. Normalized geometry uses the larger absolute signed extent while tooltips retain raw values; axis ticks remain plain numbers. The original hides a whole normalized series when one category is missing. On 2026-10-24 the owner approved retaining valid values and omitting only the missing observation. This correction must have a focused regression test.

The retained FMP example is FY2025 quarterly AAPL cost of revenue plus gross profit, reported USD. Four exact sums reconcile to revenue, which is never a third stacked component. No new provider retrieval was needed. The contract distinguishes observed controls/tooltips from source-derived exact geometry and discloses original transport diagnostics. Representative packaged real-data samples remain N4.

## Bounded tasks

- [x] N0. Freeze the original numerical/UI contract and adapter interface.
  - Reuse original-source evidence and one discriminating isolated browser probe; independently reconcile the retained FMP fixture. Distinguish observed, source-derived and unresolved behavior.
  - N0 is controller-owned. A delegated probe worker may edit only the new original probe `terminalpro/tests/e2e/live-chart/nightingale-original.spec.ts` while the controller owns, after semantic freeze, inactive declarations `Chart/compatibility/nightingaleContracts.ts` plus `terminalpro/tests/unit/chart-compatibility/fixtures/nightingaleContract.ts`. Reuse existing browser helpers; any additional helper requires an explicit ownership adjustment. No live application edit belongs to N0.
  - Identify exact N1/N2 new-file lists and shared types before fan-out. Measure modified shared-file baselines. The controller alone edits `.kiro/complexity-budgets.json`, shared interfaces, source locks and the combined change manifests; these writes are serialized. Each lane supplies its scoped measurements and hashes, not competing inventory edits.
  - Done when independent contract/plan review accepts the financial semantics, runtime evidence and executable lane boundaries.
- [ ] N1 (P). Implement the inactive Nightingale renderer and assignments.
  - Depends on N0. Own only the reviewed new Nightingale rendering/assignment files and focused tests, with no shared dispatch or editor edits.
  - Implement original geometry, mode transforms, missing/sign rules, theme/legend/tooltip semantics. Verify meaningful numerical and native rendering results.
  - Done when focused checks, scoped static checks, complete-file complexity and independent review pass. No live activation belongs here.
- [ ] N2 (P). Implement inactive Nightingale control/session adaptation.
  - Depends on N0; independent of N1 only after shared interfaces freeze. Own reviewed new Nightingale editor/session files and focused tests.
  - Map original reachable controls and persisted options through existing owners. Preserve unsupported-neighbor family state and stale-command rules.
  - Done when control-to-option/state effects, saved defaults and rejection behavior pass focused checks, complexity and independent review.
- [ ] N3. Connect the existing Table/File application paths.
  - Depends on N1 and N2. One worker owns shared capture/setup, family unions, editor/caller routing and session integration. Freeze a minimal exact path list and split capture from routing only if review shows a distinct oversized boundary.
  - Preserve prior families, ready-empty recovery, field/mode changes, native legend updates, resize and existing persistence. No alternate state owner or disabled control.
  - Done when real session/editor/caller checks and affected regressions pass, shared-file caps pass and independent review accepts the integration.
- [ ] N4. Accept packaged real-data behavior and visible parity.
  - Depends on N3. Build an identified candidate with Dagger, then reuse the isolated one-worker browser flow and retained FMP fixture. Keep fresh-session reopen as the final operation in each journey.
  - Verify acceptance criteria 2-4; fix concrete defects and rerun affected checks. Retain exact original/candidate identities and selected reviewed samples.
  - Done when independent behavior review and required owner appearance decisions are recorded. Tests and documentation are excluded from production caps; no parallel harness is planned.
- [ ] N5. Publish the accepted milestone.
  - Depends on N4. Reconcile README/docs, owning spec and breadth, sync curated evidence, commit/push, dispatch one image publication and verify release assets plus anonymous digest/tag/latest pulls.
  - Done when publication evidence and final documentation pass independent review. This does not claim remote-server deployment or browser execution of different CI-built bytes.

## Execution limits

Use the existing portable Vitest, scoped Biome, TypeScript baseline comparison, syntax/combined inventory checker and Playwright/CDP helpers. Maintain 400 physical lines/file, 300 logical units/file and 50/function on every new or modified production file. No compressed code or implicit exceptions. Inventory changes and final shared-module checks are part of each source acceptance.

Use at most four agents: controller, two disjoint workers and an independent reviewer. Sol handles bounded implementation; Astra handles numerical/integration contracts and difficult review. Serialize heavy builds and browser runs; at most three independent verification processes, one browser worker. Do not mutate the owner's local Compose data for tests. Preserve unrelated catalog, Perspective and inventory edits.

The [independent plan review](../../../artifacts/reviewed/chart-nightingale/plan-review.md) passed on 2026-10-24. N0 is independently accepted; the contract freezes exact disjoint N1/N2 files, shared interfaces and commands. N1/N2 may proceed without shared live routing edits. This milestone follows the prototype-first steering amendment; it does not mark the full analyst-workspace specification complete.

## FMP samples

Pending N4. No synthetic drawing or generated illustration substitutes for an accepted application capture.

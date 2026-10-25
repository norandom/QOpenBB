# H0 and H1a design review

VERDICT: APPROVED for bounded H0 numerical/capture/control contract closure and inactive H1a type materialization. No remaining design blocker was found. This does not approve implementation acceptance, live hierarchy routing or H4 completion.

Reviewed `.kiro/specs/analyst-workspace/hierarchy-contract.md`, final SHA256 `313bd7bb498a03620c139d85f33d59d3b66dfa07b5fdcf34b19ed0011ba7fdb8`, against original observations, the owner missing-size decision, the controller tooltip decision, and current exported types. The initial reviewed revision was `d5a3e2053eb596e2c268dfa1127daf120e501a44ff77f81752713c001ff8b61f`; the small corrections below were directly reread and rehashed.

- Resolved: numerical and H1a raw scalar types both include boolean. Boolean canonicalization through String is faithful to directly inspected pinned source, but mixed scalar File behavior remains unobserved.
- Resolved: exact type imports are now explicit: ChartSnapshot and SnapshotDiagnostic from `compatibility/snapshotTypes`; GridCaptureInput from `application/types`; SetupAggregation from `echarts/cartesianTypes`. `application/setupTypes` imports SetupAggregation without exporting it.
- Resolved: canonical observed-review link exists. Source and reviewed-mirror SHA256 both equal `0065bcc4857d93365e0e15e280c7ff20a3cf225446f97df6db110e78036c6d70`.

The no-alias HierarchySnapshot deliberately omits scalar category fields and keeps raw values separate from canonical paths. A separate validation-result type and an inactive retained union do not relax ordinary validators or activate the family. The two declaration owners have the correct dependency direction: compatibility types do not import application types. No unreviewed prepared-node/projection signatures are declared.

H1a is confined to two new type declaration files, one compile-only fixture and parent-owned inventory. It changes no runtime, state, capture routing or storage. The fixture proves type shape only. Later live union activation is explicitly atomic in H3, including removal/narrowing of the existing capture casts and guards before flat selectors. This resolves the earlier split-lane propagation risk.

The contract preserves ordered categories, separate size/color roles, duplicates and no-category row identity; distinguishes original missing weight from the owner-approved no-area correction; retains family-root tooltip storage and family mode effects; and records the deliberate working-toggle correction. Diagnostics, exact geometry, provider Table, fresh-session persistence and H4 controls are correctly limited rather than relabeled complete. Future whole-file 400/300/50 caps and inventory checks remain mandatory.

Mechanical review was read-only: canonical/source/type reads, hashes and targeted export searches. No tests, browser or builds ran in this reviewer lane. The proposed strict compiler fixture, formatting and complexity checks remain execution requirements for H1a, not completed verification.

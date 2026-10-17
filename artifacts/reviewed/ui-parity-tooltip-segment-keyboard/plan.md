# Review the segment point and bounded keyboard retention before any run

This is a source-only collector proposal dated 2026-10-17. Independent review and a separate controller grant are required before any runtime attempt. T08's segment-center hypothesis is supported by the approved source diagnosis. T05 remains unexplained; the proposal makes no new cause claim and provides no fix or UI-parity acceptance.

The [diagnosis](../ui-parity-tooltip-geometry-diagnosis/report.md) and [independent review](../ui-parity-tooltip-geometry-review/review.md) bound this work. The exact 12-file executed harness at `artifacts/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1/harness` is copied byte-for-byte into [baseline](baseline). That copy is immutable provenance. The proposed [harness](harness) changes only `collector.mjs`, `journey.mjs` and `io.mjs`, and adds `keyboard-retention.mjs`. The [exact unified diff](collector.diff) includes every changed/new source line. [Source hashes](source-hashes.json) pin the source inputs, baseline, proposed source and offline evidence.

## Coordinate hypothesis and disproof

For `stackedColumn` only, select the already retained finite datum `midPoint.x/y`. Missing, nonnumeric or nonfinite midpoint components stop unresolved. There is no fallback to rectangle center, another series or another coordinate. Grouped rectangle centers and line points remain byte-equivalent in the offline results. All existing DPR, inactive settlement, exact named scene chain, translations, identity transforms, positive envelope, CSS scene and canvas/area bounds guards remain in place. The intended wrapper/ordinal/series/yKey stays distinct from displayed tooltip labels and values. No private picked-state inspection or arbitrary scene walk is added.

The 24 retained pointer probes are recalculated without input. T08.p52 shifts vertically by 28.275 CSS pixels to the income segment midpoint. T05.p17 has zero shift. A future unequal displayed value at the reviewed T08 point would disprove coordinate sufficiency. The T05 disagreement, T04 omission, missing-value semantics, tied-value ambiguity and actual picked identity remain open.

## T06 retention contract

The generic browser `dom()` projection remains unchanged. `observe()` still requires equality of the full raw DOM samples; its optional inspector now checks each T06 sample's finite baseline and projection before that equality test. The settlement projector independently rejects a claimed stable pair if the full raw members are unequal. Both actual pair members, status, sample count and elapsed time are retained separately.

T06's per-input `before`, settled pair members and input-ledger `after` retain the full existing active-element fields and live status. A visible tooltip retains heading, up to three complete label/value rows, up to four compact texts and pagination. Hidden or absent tooltip retains `{visible:false}`. Hidden stale content, tooltip bounds and HTML are omitted from T06. Pointer/escaping evidence retains its existing projection elsewhere. No field is truncated to fit a cap.

Each keyboard mode retains `area` and at most two `swapchain` active projections once. Every subsequent before/settlement sample must equal that baseline before repeated area/swapchain data is dropped. A change stops the case as unresolved, with the prior retained baseline and case reason. Mode setup actions use the compact ledger projection but do not compare against a previous mode's baseline. No baseline change is silently accepted.

## Prospective serialization and stop behavior

The original 131,072-byte case ceiling and 115,072-byte current-case guard remain unchanged. Before every T06 input, and before incrementing its keyboard probe counter, require `serialized current bytes + 32768 <= 115072`. The same reservation runs inside `input()` before action counters, started receipts or emitted input. A reservation failure emits no input and advances neither action nor probe counters in the exercised budget-failure paths.

The finite module caps one projected sample at 4,096 serialized UTF-8 bytes, one mode baseline at 2,048, one complete invocation at 14,336, one ledger entry at 6,144, and one control receipt at 1,024. The reservation covers one invocation, one ledger entry, one baseline, two control receipts and 2,048 bytes of case/scaffold changes: `14336 + 6144 + 2048 + 2048 + 2048 = 26624 < 32768`. The final events/elapsed tail is independently capped at 16,000 bytes before assignment. The writer validates retained T06 entries/invocations/baselines and the hard case ceiling before overwriting an existing file. Existing aggregate JSON/run-byte guards remain intact.

Text caps retain the existing 512-character active name, heading, row label/value and compact text limits, and 2,048-character live status limit. New tag/role/tabindex/id caps are 64/128/32/256 characters. All projected rectangles and settlement counts/times must be finite numbers with absolute value at most one billion. Serialized byte caps are checked in addition to character caps, so Unicode escaping or many individually valid strings cannot borrow unreserved space. More than one heading, three rows, four compact entries or two swapchain elements stops. Unseen states that exceed these caps stop unresolved and preserve already written partial evidence; they do not trigger retries, clipping or a larger budget. A failed after-input projection can leave the already persisted started receipt as the last complete file; it does not retroactively claim that no input occurred.

Offline reprojection of the 27 historical Tabs is 41,342 bytes with their existing ledger untouched. That ledger does not contain compact/pagination fields, so the verifier does not fabricate them. This count differs slightly from the diagnosis because absent tooltip becomes explicit hidden visibility. It is a retained-data calculation only. There is no worst-case promise that 72 Tabs, conditional arrow sequences or all three modes will fit; limits stop future unseen larger states. The 32-KiB reservation is intentionally conservative.

## Unchanged runtime bounds and inherited limitations

The original fixture, source revision `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, eight cases, 396 total actions, 96 probes and 48 PNG ceiling remain unchanged. Pointer cases retain 36 actions/60 seconds; T06 retains 120 actions/120 seconds. Setup remains 24 actions/180 seconds, the shared case lifecycle 600 seconds, input stop 840 seconds and total lifecycle 900 seconds with the existing cleanup reserve. Settlement sample counts/deadlines and per-file/aggregate bytes are unchanged. There are no extra retries. Twenty-four pointer probes plus 72 Tabs exhaust the probe budget; arrow paths remain conditional within the same ceiling.

The original `run.sh`, `start.mjs` and `cleanup.mjs` remain byte-identical. No lifecycle or network improvement is claimed. The [Legend source review's B01](../ui-parity-legend-collector-review/review.md) also applies to the inherited tooltip source: Docker default networking does not deny backend/provider egress; later any-origin specialized routes bypass the generic page-origin handler and `route.fetch()` can follow redirects; routing is page scoped and service workers retain the default. Browser routing therefore does not establish the required denial boundary. Independent review must resolve the traffic-denial prerequisites in a separately owned source revision before a runtime grant; acknowledgement here does not waive the contract.

Cleanup records an owned browser PID/start tick, unlike the older Legend source, but its receipt and fallback do not prove complete descendant-process absence. Shell helper termination uses owned shell variables without a process-start fingerprint; fixed close timeout promises and partial setup/cleanup paths need independent lifecycle review. No process absence, port viability, browser isolation, network denial or 900-second completion has been executed for this proposal. No unreviewed lifecycle changes are borrowed. The inherited `planHash` identifies the earlier executed plan, not approval of this proposal. Historical `static-check.mjs` and `verify.mjs` are preserved for provenance; they depend on their old adjacent files and are not this proposal's verification commands.

## Offline evidence and review handoff

Run from the repository root:

```powershell
node artifacts/ui-parity-tooltip-segment-keyboard/verify.mjs
node artifacts/ui-parity-tooltip-segment-keyboard/freeze-check.mjs
```

The [offline verifier](verify.mjs) launches only Node syntax checks and source/data-only mocks. It writes this package's deterministic [verification receipt](verification.json), with 108 passing checks and exit 0 on the frozen source. Its one injected test fixture initially omitted the Tab cap and was corrected before the passing run. An initial Python alias was unavailable; the installed `py` launcher performed source editing. Neither event was an application/runtime attempt.

Fault cases include T08 midpoint/T05 zero delta; missing, nonnumeric and nonfinite midpoint; outside bounds; broken named chain; missing ordinal; changed area baseline; unequal full DOM that projects identically; hidden stale and full visible tooltip; oversized/extra-row/nonfinite states; prospective budget rejection in the actual extracted input and keyboard functions with counters unchanged; hard-ceiling and ledger prewrite rejection with prior bytes unchanged. The 24 retained probes and 27 historical Tabs are checked. This is verification of source rules and fault stops, not browser reachability or target picking.

The reviewer must independently inspect exact hashes/diff, reservation arithmetic and each added append path; challenge full-DOM-before-projection ordering, baseline changes, hidden/visible semantics, counter preservation, partial-write behavior and inherited lifecycle/network blockers. No reviewer approval has been supplied in this package. The controller owns approval, future source changes, any run grant and publication. The [publication allowlist](publication-allowlist.json) selects only synthetic source, fixture, plans, hashes, diff and offline receipts. It excludes logs, credentials, runtime state, profiles, dependencies, images and historical PNGs. It is compatible with the publisher's sourcePath/hash/bytes contract and does not authorize synchronization itself.

The exact future command is a proposal only, to be reconsidered after independent review resolves the inherited prerequisites and the controller grants this exact source. Create a new empty attempt directory only at that time; never reuse an existing attempt or retry automatically. From WSL at `/mnt/d/Source/QOpenBB`:

```bash
TOOLTIP_HEAVY_GRANTED=yes bash artifacts/ui-parity-tooltip-segment-keyboard/harness/run.sh /mnt/d/Source/QOpenBB/artifacts/ui-parity-tooltip-segment-keyboard/capture/attempt-20261017-tooltip-segment-keyboard-a1
```

The environment flag is an execution guard, not approval evidence. The root must retain the actual independent review and grant beside the exact source hashes. No browser, container, application, image build, installation, provider request, Git operation or runtime command ran for this work.

All writes are confined to the new `artifacts/ui-parity-tooltip-segment-keyboard/` research package. It is excluded from production complexity caps. Future maintained collector/product adoption requires the executable checker/inventory foundation and 400 physical lines/file, 300 logical units/file, 50 logical units/function, plus a final shared-module audit. The new retention module is cohesive by responsibility; the proposal does not use research exclusion as evidence of production conformance. The English owning spec and documentation/testing/delegation/complexity steering were read; core product/tech/structure steering is absent. A plain-language pass kept observations, hypotheses, source checks and runtime prerequisites distinct.

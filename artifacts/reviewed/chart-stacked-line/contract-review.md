# Stacked Line contract review

2026-10-26. **Current verdict: APPROVED for SL1-F, then the disjoint SL2-A/SL2-B lanes after foundation acceptance.** This approves the amended implementation contract, not production changes, runtime admission or replacement acceptance.

## Amended-contract re-review

Reviewed current contract SHA-256: `40e751074fc9370f4c67644ea448174fbc068c59a8439b2f0ac1d2c60f4f397f`. All five blocking findings below are resolved: foundation owns the type-only union widening while runtime guards remain closed; J owns tooltip admission filtering; grouped continuous-x arithmetic and ordinal row identity are explicit; projection supplies an explicit `empty` flag; and the shared named overflow error maps to a specific diagnostic.

Independently read the new grouping assessment and the actual cached Grid `transformCategoryData`, `getDataTransformedData`, `getXAxisType`, `transformTimeData`, plus Charts `toKeyString`. These confirm unique ordinal wrapper IDs, number/time transformation rules and serialized group equality. Together with the previously inspected group accumulation loop, they support the repeated-number discriminator A `[10,30]`, B `[31,33]`, denominator 33. The contract preserves source row indices and raw observations instead of aggregating them away. Its shorthand `C[j]` in rendering sentences refers to the defined `C[j,r]` for grouped input.

The executable dependency boundary is now complete: reviewed controller foundation -> two exclusive inactive implementation lanes -> independent lane review -> atomic controller admission/tooltip/session join -> packaged acceptance. Types are shared before work; neither worker owns runtime admission. The grouping discriminator is part of the frozen helper input. A changed topology or interface requires stopping affected lanes and review. Every maintained file retains inventory-backed 400/300/50 checks; source comparison and focused RED/GREEN evidence remain future obligations.

Mechanical re-review: direct source reads succeeded; Workspace diff remains empty; placeholder scan has no matches. No production edits, tests, typecheck, browser or complexity execution were performed by this reviewer. Missing/zero painted topology, repeated-coordinate native behavior, raw tooltip geometry and identified real-FMP candidate acceptance remain explicitly open in SL3. No further blocking contract findings.

## Historical first review (superseded)

2026-10-26. **Initial verdict: REJECTED pending the bounded amendments below.** The numerical policy for unique projected x values was coherent and financially explicit; the frozen lane interface and repeated-x gate needed correction before fan-out.

Reviewed contract SHA-256: `fb661f1f22cd1bb678163165bb0da8b5afa683bc80ff272830ee5767ad073ec6`. Root source `eac6637cc9f3aaf19e7a6501ed1c3403d0029d06`; Workspace `0b2190354d2dc5f4175ffb989cf652ac36237c77`. Read the milestone, reviewed original-source/native-review/integration-source, current translator/series/axes/tooltip/display/session owners, and original AG Charts 12.1.1 dependency functions directly in the retained WSL cache. This is design review, not runtime acceptance.

## Required amendments

1. **Important: make the frozen types usable by both lanes.** SL1-F creates `LineFamily`, but existing geometry/editor APIs accept `CartesianFamily`, which excludes both new literals. Assign the type-only `CartesianFamily` widening to the controller foundation. Keep `isCartesianFamily` and normalization runtime guards unchanged until SL2-J. This permits independently typed inactive lanes without admitting partially implemented charts.
2. **Important: assign the raw-tooltip admission seam.** Current `cartesianTooltip.ts` shared mode enumerates all raw columns regardless of the supplied engine hits. Null drawn values therefore do not ensure missing, hidden or zero-denominator endpoints disappear from shared output. Assign this file to J and freeze an optional drawn/admission argument, preserving existing callers. Filter by stable series ID and raw row index before formatting raw observations; do not use derived coordinates as financial values. Test all tooltip modes, mixed missing rows, hidden series and zero-denominator rows.
3. **Important: settle repeated-x mathematics before fan-out.** Original `processData` sets `groupByKeys: stacked` even for continuous x; `buildGroupAccFn` iterates series first and each datum index within its key group second. The proposed independent-row formula loses this cross-row accumulation. Freeze group identity and traversal in the contract, including category, numerical and parsed-date keys, and any required grouping/context input to `projectLineStack`. Preserve every raw row/index in output; grouping is a calculation lookup, not permission to merge observations. Define one denominator from all required cumulative values in the x group and independently test repeated-x discriminator vectors. Resolve ambiguous key equivalence through focused original source/diagnostics before freezing this seam. Packaged appearance/lifecycle checks can remain SL3, but runtime parity remains unproved until those checks pass. No silent exclusion or disabled mode is acceptable.
4. **Important: separate empty-domain detection from nice intervals.** Current translator passes `"interval" in extent` to `normalizedDisplay`; that argument suppresses nonzero tick labels for an empty chart. The new line interface allows an interval on nonempty extents. Specify an explicit all-null test for normalized Line and test nonempty percentage ticks with a nice interval. Existing bar/Area policies must remain unchanged.
5. **Important: freeze the overflow diagnostic handoff.** A may raise a local typed error while J must translate it to a specific diagnostic. Name/export that error or a discriminated result in the shared contract before dispatch, so the controller does not infer failure identity from error text. The existing catch-all `invalid-style` diagnostic is insufficient for a numerical overflow.

## Supported decisions and boundary

The signed ordered prefixes and maximum absolute cumulative denominator match the independently read scalar dependency algorithm for unique x. The discriminators distinguish same-sign bar stacking, gross contribution normalization and final-total normalization. Raw observations, unit admission, selected order, stable IDs, full-context overview, explicit zero/missing admission, finite overflow rejection and no forced zero domain are appropriately separated. Saved `line` namespace, host connect-missing default and supported saved false are retained; no invented original control is required.

The dependency graph is sound after these amendments: controller types/inventory -> disjoint geometry and editor lanes -> independent reviews -> controller-only atomic translator/session/tooltip admission -> packaged application acceptance. No new state owner, bar stack property, hidden Area fill, feature flag or reduced native feature set is authorized. Whole-file 400/300/50 checks and inventory/final shared-module audits remain mandatory; existing checker foundation is reused.

## Mechanical results and limits

- Workspace production diff: empty at inspection; unrelated root inventory/CI edits were read as status only and preserved.
- Contract placeholder scan: clean (`rg` exit 1 means no matches). No credential material observed in the reviewed contract.
- Static checks: source/interface spot review only. Tests, typecheck, browser runs and complexity execution: not run, appropriately outside this documentation-only review. RED evidence is N/A before implementation.
- Core steering `product.md`, `tech.md` and `structure.md` are absent; read available delegation, complexity, delivery-workflow and documentation policies. Spec language is English.
- Only this review file was written. Original source evidence does not establish painted geometry or candidate parity. Re-review the amended contract before foundation/worker dispatch.

# Revise the finite observation contract before collector implementation

The eight-case plan is bounded and its source mappings are credible, but its exclusive observation list cannot support every check promised by the cases. Resolve B01 and the getter caveat below, then freeze and rereview the revised plan. This verdict concerns source-only preparation for a collector. It grants no browser execution, runtime capture, production change or UI acceptance.

Reviewed on 2026-10-17 against the frozen [plan](../ui-parity-legend-plan/plan.md) and [source manifest](../ui-parity-legend-plan/source-hashes.json). The supplied SHA256 values match: plan `f62f102b0cc5ed201b1627827a63a80a8ba9059b231fccd07e00bf2d3e3f30ee`; manifest `02c9dae3275292f02bf4bac11b1972164f8fa51e7255f6f82e506a2883794272`. All 29 manifest entries match their stated bytes and hashes, including five files obtained from the pinned original Git revision. See [verification](verification.json).

## B01: promised negative checks exceed the named projection

Plan line 49 requires chart padding to remain observed; line 50 requires series-bar geometry to remain separately measured; line 51 requires live bar stroke to stay observed; line 57 requires live series visibility to remain preserved. Lines 63-68 say to project only the listed paths. That list includes legend nodes, series identities/data, seriesRect and DOM geometry, but excludes chart padding, live series visibility and any bar-node geometry/stroke. A collector following the list cannot honestly report these checks as measured. Plot screenshots support visual comparison, but do not silently add numeric bar geometry to the contract.

The smallest amendment keeps the eight cases and avoids another scene traversal:

1. Add only `chart.padding.top/right/bottom/left`, presence-aware, to the finite chart projection and settlement comparison. Chart padding and the legend/plot gap then have distinct evidence owners.
2. Admit exactly two `chart.series` entries, identity-linked by their stable series IDs and `properties.xKey/yKey` to the two legend data entries and source columns. Add presence-aware `series.visible`, `series.properties.visible`, and `series.contentGroup.visible`. Record both `series.visible` and `properties.visible`: the installed source getter uses legend-manager state before the property fallback, so the property alone does not establish live visibility. A mismatch stops the case; do not search other series or descendants.
3. If L04 keeps a configuration-level stroke comparison, add only `series.properties.strokeWidth` and `series.properties.stroke` for those two series. Explicitly distinguish these from rendered bar-edge evidence. They do not prove the raster stroke.
4. Rewrite L03's promise of separately measured series-bar geometry and L04's live bar stroke comparison as identity-linked comparison of the fixed plot crops, supported by the bounded series state above. Keep numerical geometry claims limited to the already named legend boxes and seriesRect. If numerical measurements of every bar are necessary, provide a separately reviewed exact selection path, eight-node maximum, datum identity mapping and complete updated node/output accounting; do not introduce that traversal during the run.

These changes preserve the financial contract: four quarter wrappers, revenue 100/120/140/160 and operating income 20/25/30/40 USD millions, original field names, two series and original order. They do not authorize a first-series shortcut or accept legend labels as proof that both plotted series remain present.

## C01: describe the permitted getter accurately

The transform formula at plan line 70 is correct for the inspected source. `MatrixTransform.computeBBox` applies the node's own transform (Charts bundle lines 4045-4049); the legend and each item are TranslatableGroup instances. Thus legend group BBox needs no additional legend translation, item BBox receives only legend translation, and label/marker BBoxes receive the item's plus legend's translations. Adding marker translation again would double-count it. `LegendDOMProxy` uses canvas-space bounds and equalizes item DOM heights (35557-35571), so the plan correctly avoids requiring identical DOM and scene heights.

However, `getBBox()` is not a strictly passive scalar read. `Node.getBBox` lazily caches `computeBBox` (1047-1049), and `LegendMarkerLabel.computeBBox` invokes `layout()` on a cache miss (35761-35763). That layout can assign marker x/y and translations (35724-35743); matrix computations also maintain caches. This does not show that settled observations necessarily change pixels, and it does not invalidate the transform formula. It does mean the collector must not describe every permitted getter as side-effect-free.

Clarify that only the named settled `getBBox` calls are permitted, including their source-defined lazy cache/layout work; direct layout, transform, text-measure, update, setter, pick and tooltip calls remain prohibited. Read the named marker x/y/translations and item/legend translations immediately before and after the getter group. Any unexpected change invalidates the sample and yields a bounded observation diagnostic; it must not create a new unrecorded edit, extend the deadline or trigger a repair mutation. Keep these checks within the existing observation and scalar limits. This is a collector-contract clarification, not a new runtime permission.

## Source findings that can be retained

- The installed Grid LegendPanel uses `gradientLegend` for treemap/sunburst/heatmap and `legend` otherwise (48225-48226). Its selected-value-column predicate is greater than one (48289-48291). The plan correctly leaves one-series and other-family behavior unverified.
- Enabled maps to `legend.enabled`; Position, Spacing, Marker Size, Marker Stroke, Item Spacing and both item padding controls map to the paths listed in the plan (48234-48335). The current panel does not provide a Legend Shape selector. The captured default control inventory independently contains the named controls and accessible labels.
- Font and Size inventories are bounded hypotheses with source strings and observed current-value insertion. Fresh popup ownership and exact runtime option names remain necessary. The plan stops on selector ambiguity and does not treat a historical Shape filename as a control contract.
- The inspected source's `getOrientation()` defaults to horizontal (36015-36016); side position alone does not prove a one-column item arrangement. The L06 explicit layout discriminator and unavailable outcome must remain. Keep the maxHeight 50 rule and do not force layout to manufacture a pass.
- The marker -> symbolsGroup -> item -> legend group -> root chain matches the source roles. Scene root and symbolsGroup are plain Groups. The current parent-space correction addresses the earlier double-translation risk; do not replace it with an arbitrary ancestor walk.
- Eight cases, action/event/output ceilings, one isolated context, external-traffic denial, owned-state cleanup and no retry-until-pass are explicit. Budget ceilings may stop a case; they are not evidence that all cases will finish. The source review exercised none of those runtime mechanisms.
- Original Workspace revision `38dffc33389aca0e4a87e0e88d42f7067aa220df` and original image digest `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` remain separate future admission checks. Installed Grid 34.1.1/Charts 12.1.1 bytes are matching-version source clues, not proof of image byte identity.

## Verification and publication boundary

This independent review used filesystem reads, pinned Git object reads, source searches and SHA256/byte comparisons. No application, browser, build, dependency install, collector, provider request or heavy suite ran. An initial `python` launcher command failed because that alias is unavailable; the same offline hash inspection then completed with `py -3`. No failed runtime attempt is being reclassified as success.

The production caps remain 400 physical lines per file, 300 logical units per maintained code file and 50 per function, with inventory/checker foundation and shared-module audit required for future production work. These review documents are research/documentation exclusions; no production complexity pass is claimed. The review preserves the existing session/appearance/mapper/host ownership and does not approve later phase changes.

Only this review and its verification record are proposed for publication through [the explicit allowlist](publication-allowlist.json). They contain source identifiers and sanitized review findings, with no runtime state or secrets. The controller owns mirroring and explicit staging. The frozen planner files were not edited.

# Accept the finite axis/grid evidence; retain the integration gates

The capture supports its bounded original-runtime findings and is suitable for publication through the explicit allowlist. It does not establish candidate parity, complete editor behavior, onboarding acceptance or backend persistence. The separate widget-transaction proposal is coherent research with unresolved design joins; it is not an adopted or implementation-ready contract.

Independent review date: 2026-10-17. Original Workspace: `38dffc33389aca0e4a87e0e88d42f7067aa220df`; original image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Candidate `ea02ec15956dee8d2c8a06825387a570757db12d` was not executed. This reviewer performed source/artifact inspection, offline comparisons and visual inspection of all eight screenshots, without another browser run, build, installation or production edit.

## Findings supported by the capture

The [capture report](../consuming-axis-grid-capture/report.md), case JSON, seven-record action ledger, scene fields and screenshots agree on these distinctions:

| Finding | Independent conclusion |
| --- | --- |
| Axis color field | Both baseline processed axes use `line.stroke = #c1c1c2`; `line.color` is absent. Grid stroke is separately `#515153`. The old missing-color observation resulted from reading the wrong field. |
| Axis enable/width | The disabled baseline left line has scene width zero despite `visible = true`. The real original Thickness action writes enabled/width 3 into left/right model namespaces and produces a visible left line of width 3. |
| Grid width/dash UI | Real controls produce width 4 and dash `[5]`, with corresponding model namespaces, three accumulated options events and all five measured live grid lines updated. The screenshots visibly change; these controls were not no-ops. |
| Unequal widths | Synthetic general/style widths 3/1 and 1/4 remain distinct in processed options, while all measured scene widths are 1 and 4. This supports finite effective-style projection, not arbitrary saved inheritance or UI reachability. |
| Synthetic model versus UI | Proxy updates change the `getChartModels()` projection. They retain the preceding three UI options events and displayed editor values. A changed reference model is not an emitted UI edit or evidence of a backend save. |
| Opacity experiment | `gridLine.style[0].strokeOpacity` is rejected as unknown, absent from processed style, and leaves scene opacity at 1. The 0.25 and 1 PNGs have identical bytes. This is evidence of that unsupported property, not a successful opacity effect. |

The installed source further separates `calculateGridLine`'s stroke/width/dash from `calculateGridFill`'s fill/fillOpacity. Neither the rejected strokeOpacity probe nor the historical fillOpacity observation establishes an ECharts split-line opacity mapping. The updated [findings wrapper](../../../.kiro/specs/openbb-self-service/chart-axis-grid-findings.md) states that limit accurately. It leaves explicit color edits/conflicts, other roles/positions/themes/families, multiple grid styles, hidden-value retention and candidate geometry open.

## Evidence quality, failure and publication

Startup verifies the pinned image and original source label, creates disposable state and generated credentials, and binds a dynamic loopback port. The harness uses an isolated headless browser, rejects other origins, overlays only the synthetic dashboard/data routes and waits for original chart update plus inactive animation before measurement. Reference-only private React/chart inspection is confined to the capture; it does not justify such dependencies in production.

Attempt 1 failed at an onboarding navigation wait. Its failed script and exit-1/failure/cleanup receipts remain selected. The corrected harness waits for the original profile PUT and usable Continue control, then opens the synthetic dashboard. It does not fix or override the onboarding/tier failures. Both attempts record closed browsers and removed containers/state/credential files. The private runtime receipt intentionally remains local and is excluded from publication.

The final diagnostics retain two page errors, two CDP exceptions, original onboarding HTTP failures, the theme registration warning and the unsupported-opacity warning. This is not a clean application run. The sanitized diagnostic derivative identifies its original input hash and excludes raw authentication/request inventories.

The [independent audit](audit.ps1) passed 231 offline checks recorded in [verification.json](verification.json). These are artifact checks, not 231 feature tests. All 51 capture-publication hashes matched; eight final-script hashes, four reused-harness hashes, three installed-dependency hashes and five exact original Git blob hashes also matched. All eight screenshots were inspected. The worker's separate 99-check verification was read, not treated as a substitute for this review.

One initial reviewer check incorrectly expected synthetic model equality. Inspection showed the injected overrides in `getChartModels()` while UI event history stayed unchanged. The reviewer corrected that assumption and now asserts the actual synthetic model values. No runtime retry or worker evidence alteration was needed; the correction is recorded in the audit output.

The reviewed 51-file capture selection includes only synthetic evidence, finite diagnostic derivatives, exact scripts, public source excerpts/license and failure/cleanup receipts. It excludes credentials, private runtime metadata, raw diagnostics, logs, state and caches. The publication helper selects explicit files; no recursive artifact-tree publication is authorized. The combined [safe publication allowlist](safe-publication-allowlist.json) adds only the capture allowlist itself, five new research outputs and this review's outputs. The parent must record the combined allowlist's own hash externally to avoid self-hash recursion.

## Separate widget-transaction research

The [research draft](../widget-transaction-design/draft.md) correctly identifies the six existing setter paths, captured functional-request mutation, passive-effect timing of current widget refs, and boolean event result of `dispatchSaveState`. Source inspection confirms that an awaited save event does not itself await pending React chart writes or backend persistence. All 15 research input/output hashes matched.

Its additive chart port within the existing widget owner is a reviewable hypothesis. The completion journal avoids losing batched receipts or waiting for a widget-value change; it does not introduce another widget store. The draft distinguishes at-most-once effect invocation from successful delivery and does not extend purity guarantees to unaudited legacy callbacks.

Adoption remains blocked on the actual external-fence publication barrier, same-field conflict detection, interaction lifecycle, context-override batching and explicit save barrier. Completion/cancellation ordering and the six-path compatibility matrix need implementation evidence once that design is approved. The 886-line shared declarations file cannot be modified without the stated cohesive extraction or reviewed exception. No production complexity check, TypeScript compilation, React concurrency test or persistence test ran for this research.

These two outputs narrow the next design decisions. They do not reopen or upgrade the earlier frozen contract draft, remove chart guards, approve implementation, or change the full original Workspace acceptance obligation.

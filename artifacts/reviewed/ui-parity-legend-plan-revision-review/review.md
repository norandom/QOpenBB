# Accept the revised plan for collector preparation

The revised eight-case Legend plan closes B01 and C01 without adding a bar-node traversal, fixture variant or runtime attempt. It is accepted as the bounded contract for subsequent collector preparation and independent collector review. This is not permission to execute a browser capture, accept UI parity, change production code or advance a specification phase.

Reviewed on 2026-10-17: [revised plan](../ui-parity-legend-plan-revised/plan.md), [source manifest](../ui-parity-legend-plan-revised/source-hashes.json), and [revision rationale](../ui-parity-legend-plan-revised/revision-notes.md). The original [preflight](../ui-parity-legend-plan-review/review.md) remains preserved. The revised plan hash is `5a33a0237eb351df5a7a6060da2aff5c83379f89999c4a4ca82faa40c92e29ef`; the revised source manifest hash is `199bd6bebb5ced6072a675c6805bd7fc41fc8c76b74bf6c66e7f2fadf9373092`.

## Finding closure

| Finding | Revised contract | Verdict |
| --- | --- | --- |
| B01: observations cannot support promised negative checks | Four presence-aware chart-padding leaves; exactly two source-ordered, ID/key-linked live series; actual visibility, property visibility and content-group visibility; only configuration stroke/strokeWidth. L03/L04 use fixed plot-crop visual comparisons and explicitly disclaim numerical bar-node measurements. | Closed for collector preparation. The finite projection now supports its stated claims. |
| C01: getter may perform lazy work | Seven directly named BBox calls bracketed by the same 14 scalar operands before and after. Operand changes invalidate the sample with a bounded diagnostic. Only existing ten-sample/six-second polling may continue; no repair, extra traversal or deadline extension. Cache equality is not claimed. | Closed for collector preparation. Direct layout/transform/text-measure/update calls remain prohibited. |

The scene count is coherent: root and legend group, two each of item/symbolsGroup/label/marker/line, and two series content groups total 14 unique nodes, below the unchanged 24-node ceiling. Seven BBox calls equal one legend-group call plus three calls for each of two items. Fourteen operands equal two legend translations, four item translations and eight marker coordinates/translations. Their 28 presence-aware before/after records reuse existing identities.

The parent-space geometry remains correct: group BBox already includes legend translation; item BBox receives only legend translation; marker/label BBoxes receive item plus legend translations. Marker translation is not added twice. DOM item-height padding remains a supporting comparison rather than an equality requirement. These are source-supported rules, not fresh runtime geometry evidence.

## Scope retained

All eight case IDs remain L01-L08. The four-quarter fixture, revenue and operating-income identities, USD-million units, four category wrappers and eight numeric values remain unchanged. Live-series identity or visibility mismatch stops a case; neither configuration properties nor legend text alone establish rendered bars.

Control selectors, menu ownership, one-series predicate uncertainty and actual row/column arrangement remain runtime questions. L06 still yields `layout-discriminator-unavailable` if the original fixture cannot discriminate item layout. No shape selector, forced orientation, larger fixture, label renaming or first-series shortcut was introduced. Captions and Color/Shadow retain their existing evidence ownership.

The complete time/output/lifecycle section is unchanged after text decoding. The plan still bounds one original instance, one isolated browser/context, one worker, eight cases, 160 chart input actions, 56 field mutations, 256 events, 24 projected scene nodes, 80 PNGs and 200 MiB total. Hard elapsed limits, diagnostic limits, external-traffic denial and owned cleanup remain fail-closed obligations for later collector review. This source review does not establish that those runtime mechanisms work or that every case will finish within the ceilings.

The original Workspace revision and image digest remain separate runtime admission obligations. Installed Grid 34.1.1 and Charts 12.1.1 bytes remain matching-version source clues; image byte identity is unverified. Candidate execution, provider checks, persistence and broader family/theme coverage remain outside this acceptance.

## Fresh verification and publication

All 34 revised manifest entries match their recorded SHA256 and byte lengths, including the original plan/review inputs, five pinned original Git files, four installed-source clues and two revised outputs. Both supplied revised hashes match. All seven plan links resolve at the intended published depth, mapping the same-directory source manifest to the frozen draft. The original plan and source manifest still match their previously reviewed hashes. [Verification](verification.json) records the exact files and results.

Only offline source reads, Git object reads, text comparison and hashes ran. No browser, application, collector, build, dependency install or heavy suite ran. Research/documentation exclusions apply to this review; no production complexity pass is claimed. Future production work retains the inventory/checker foundation and 400 physical lines per file, 300 logical units per file, 50 logical units per function and final shared-module audit.

The safe revised-plan publication set is the three files explicitly named by its source manifest: plan.md, source-hashes.json and revision-notes.md. The plan's final prose sentence still mentions only plan and source manifest; it is narrower than that explicit list. This review also inspected the rationale and approves it for publication, so the controller should use the exact [reviewed plan allowlist](reviewed-plan-publication-allowlist.json). This delivery wording does not change the collector contract.

The separate [review allowlist](publication-allowlist.json) contains this review and its verification record. Both allowlists use sourcePath, SHA256 and byte lengths. All selected files are source-only documents without runtime state, credentials or private account data. The controller owns mirroring, manifest verification and explicit staging. No frozen planner or prior reviewer file was edited.

# Native Funnel assessment

Original-only reference run 1 completed with 3 tests passed (exit 0, one worker, zero retries). This characterizes observed native behavior; no replacement implementation or acceptance follows from it. Source `38dffc33389aca0e4a87e0e88d42f7067aa220df`, retained image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, readonly backend overlay `23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de`.

Run each via `bash artifacts/chart-funnel/native/run-original.sh /home/mc/qopenbb-work/heatmap-original-private.json http://127.0.0.1:47035 /mnt/d/Source/QOpenBB/artifacts/chart-funnel/native/run-N` in WSL Debian. Each run retains exact command, source hashes/copy, runtime identity, timestamps, exit code, browser JSON and raw diagnostics. Run 1 default grep `bounded native assessment`; runs 2 onward set `QOPENBB_FUNNEL_PROBE_GREP='synthetic effects follow-up'`.

| Behavior | Funnel | Cone Funnel | Pyramid |
| --- | --- | --- | --- |
| Native saved type | funnel | coneFunnel | pyramid |
| FMP default assignments | Stage / Level USD | Stage / Level USD | Stage / Level USD |
| Initial Setup | Aggregate unchecked; Vertical direction | Same | Same |
| Default geometry after inventory toggles restored | Equal-height centered level bars with dim connecting dropoffs | Continuous taper, blue shade progression | Colored triangle segments widening downward |
| Initially expanded Series booleans | Tooltips on; Labels off; Drop-Off on; Stage Labels on; Shadow off | Tooltips on; Labels on; Stage Labels on; no Drop-Off/Shadow | Tooltips on; Labels on; Stage Labels on; Shadow off; no Drop-Off |
| Common visible Customize sections | Chart Style, Titles, Series | Same | Same |
| Axes/Legend/Navigator | No visible sections in captured native editor | Same | Same |
| Five FMP stage tooltips | All five; B formatting | All five; B formatting | All five; raw numeric values |
| Save/export/reload | Save payload captured; valid PNG dimensions/signature; canvas after same-session reload | Same | Same |

Default geometry screenshots follow heading clicks that toggle options and a second click restoring those booleans. Initial Series snapshots, captured before nested heading clicks, establish the initial boolean states. Reload checks in run 1 establish visible chart recovery, not a separately authenticated fresh-context reopening or complete model equality. Chart Style controls were reachable but not inventoried in detail.

All three run-1 diagnostic records contain two `Unexpected token '<'` errors and two failed CSV requests (`net::ERR_FAILED`), with zero recorded HTTP statuses >=400. These are retained original failures, not suppressed or treated as clean diagnostics.

Synthetic follow-up fixture includes ordered First=120, Repeated=90, Repeated=60, Zero=0, Negative=-20, Missing blank, Last=30, plus independent Reserve values. Run 2 failed before chart creation because the harness expected `1007` while the grid displayed `1,007`; the unique textual witness `Last` corrects that assertion. Run 3 reached horizontal Funnel drawing, then failed because a blank-associated public polygon contained nonfinite coordinates and its centroid was passed to CDP pointer dispatch. JSON serializes those coordinates as null. Run 4 filters pointer targets only, preserving the original drawing and invalid target paths.

Remaining effects and limitations are recorded after run 4 below.

## Follow-up outcome

Run 4 exited 1 after recording the full Funnel synthetic journey. The final full-model equality assertion failed because reload regenerated `chartId` and reduced `cellRange.columns` from Stage/Value/Reserve to Stage/Value. The entire `chartOptions` subtree, including the chosen effects, was retained. Cone Funnel and Pyramid synthetic effects were not reached. This is partial original evidence, not a passing lifecycle acceptance result. The controller subsequently authorized the bounded run 5 below.

| Synthetic Funnel observation | Evidence and limit |
| --- | --- |
| Horizontal direction | Saved `chartOptions.funnel.series.direction = horizontal`; image changes stages from top-to-bottom to left-to-right |
| Duplicate labels | Two distinct Repeated tooltips show 90 and 60 with Aggregate off; visible separate bars retain row order |
| Aggregate | UI checked with Sum; Repeated tooltip becomes 150; unchecking restores 90 and 60 |
| Negative | Negative tooltip shows -20 and a centered bar paints with positive absolute span; this is native geometry, not a financial admissibility policy |
| Zero | Stage label Zero remains, no visible level bar; centroid tooltip method did not hit zero, which is inconclusive about tooltip reachability |
| Blank | Table displays dash; Missing stage label remains; public drawing has nonfinite coordinates serialized as null; no claim of null-to-zero normalization |
| Numeric selector | Value and Reserve options are offered. Selecting Reserve appended it alongside Value in the range; chart/tooltips continued to show the first field Value. Replacing Value with Reserve alone was not tested |
| Labels | Checking Labels paints 120/90/60/-20/30; saved `series.label.enabled = true` |
| Stage Labels | Unchecking removes stage text; saved `series.stageLabel.enabled = false` |
| Drop-Off | Unchecking removes dim connectors; saved `series.dropOff.enabled = false` |
| Reload | Chart remains visible and effects' option keys persist; regenerated chart identity/range means whole saved model equality fails |

Run-4 diagnostics again retained two `Unexpected token '<'` errors, two CSV request failures and two associated console errors, with zero HTTP statuses >=400. Native data-state observations do not justify accepting those failures in a replacement.

Pending: alternate numeric field alone, Cone/Pyramid edge and toggle effects, genuine empty/all-zero source behavior, isolated null typing, fresh-context reopening, detailed Chart Style/common cosmetics effects. Run 1 proves reachable controls and representative positive-level rendering/export only; source research and these partial effects should guide a bounded next contract rather than promising untested semantics.

## Cone Funnel and Pyramid bounded completion

Parent authorized a single further run to finish the two previously unreached variants. Run 5 completed one sequential test containing independent Cone Funnel and Pyramid records (one login, one worker, zero retries), exit 0, `1 passed (47.9s)`. This reused the existing test context rather than separate test cases. Its assertions compare `chartOptions` after reload only. Full before/after models remain in `run-5/browser-output/.../effects.json`; run-4 failure is preserved.

| Behavior | Cone Funnel | Pyramid |
| --- | --- | --- |
| Direction | Horizontal saved under `chartOptions['cone-funnel'].series.direction`; visible left-to-right taper | Horizontal under `chartOptions.pyramid.series.direction`; visible wide-left triangle tapering right |
| Duplicate/aggregate | Two Repeated tooltips 90/60; Sum changes to 150 | Two Repeated tooltips 90/60; Sum changes to 150 |
| Zero | Value label 0 at pinch; tooltip Zero/0 observed | 0 text and overlapping labels near apex; no zero tooltip hit |
| Negative | -20 tooltip and painted inverted widening segment after zero | -20 text crowds near triangle apex; no negative tooltip hit; clean positive allocation geometry must not be inferred |
| Blank | Missing stage persists, two nonfinite polygon paths retained | Missing label overlaps at apex; no nonfinite paths recorded by this observer, which does not prove normalized data or valid geometry |
| Labels / Stage Labels | Numeric labels already on; unchecking Stage Labels removes category text | Numeric labels already on; unchecking Stage Labels removes category text |
| Saved options after reload | Entire chartOptions matches, including horizontal and stageLabel=false | Entire chartOptions matches, including horizontal and stageLabel=false |
| Numeric selector | Reserve added to range alongside first field Value; chart continued Value tooltips; alternate field alone not tested | Same multi-field range with Value first; alternate field alone not tested |

Exact reload differences: Cone ID `id-0wc7um7mmfu` to `id-cqb7oolk2cs`; Pyramid ID `id-cqb7oolk2cs` to `id-20svidklngq`. Each range columns reduced Stage/Value/Reserve to Stage/Value. Adding Reserve preserved Value as the first selected field, consistent with the source-observed first-field mapping; removing Value to test Reserve alone was not exercised. These are observed original changes; the passing assertion covers chartOptions only, not full identity/range persistence. Immediately-after-reload drawing.text records were empty. Independent visual inspection of both reloaded PNGs confirms numeric labels are absent, although the before-reload PNGs show them. ChartOptions equality therefore does not prove label appearance persistence; the cause of the disappearance remains unresolved.

Run-5 diagnostics: three `Unexpected token '<'` errors, two failed CSV requests and associated console errors, zero HTTP statuses >=400. Screenshots were visually inspected: Cone negative/blank geometry is discontinuous; Pyramid edge text overlaps near its apex. These are characterization findings, not behavior to endorse in a financial presentation.

This run supersedes the pending Cone/Pyramid edge and Stage Labels observations above. Remaining pending scope: alternate numeric field alone, empty/all-zero input, explicit typed-null distinction, detailed common cosmetics, numeric-label off/on effect in Cone/Pyramid (already on), fresh-context reopening. No candidate acceptance, production edits or commits.

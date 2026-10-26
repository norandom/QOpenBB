# Original Stacked Line characterization review

2026-10-26. **APPROVED to proceed to bounded design.** The retained source assessment and original Table/File observations establish enough behavior to draft the numerical and integration contract. This closes only the bounded original-characterization gate; it does not approve implementation, replacement parity, candidate financial geometry or publication acceptance.

## Evidence checked

All three original runs finished with exit 0: `native-financial-1` (two cases), `native-discriminator-1` (two cases), and `native-controls-1` (two cases, 56.1 seconds). I read the frozen control probe, model/tooltip records, completion log and selected PNGs. No new application tests were run by this reviewer. The probes assert activation, exact model tokens, selected columns and specific persistence/control states; they do not numerically assert full drawn geometry.

Reference frontend is `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Retained identity declares a backend-only overlay and `packaged_image_only:false`; this is an original diagnostic runtime, not an untouched release-image gate. Original HTML-parsing page errors and CSV request failures remain recorded. Empty diagnostics failure arrays do not establish a clean runtime.

## Supported contract boundaries

- Both gallery variants activate on the ordinary native route and preserve `stackedLine` / `normalizedLine`. Financial and discriminator captures retain their selected columns after reload. Controls runs reorder to `[Category, Secondary, Primary]` and preserve that order plus exact chartOptions after reload; chart identity need not remain unchanged.
- Both variants successfully hide and restore Secondary through the visible legend with asserted switch state. Retained normalized screenshots visibly reflow. This supports visibility-dependent projection together with the separately reviewed dependency algorithm; it is not a calibrated endpoint comparison.
- Discriminator and reordered tooltip captures show raw values, including Mixed Secondary -80 / Primary 60 and Missing Secondary 20, for normalized as well as ordinary stacked Line. Financial hover probes have no hits, so financial tooltip equivalence is not claimed. A normalized Zero no-hit does not prove node absence.
- The visible Series panel offers tooltip mode, line width/dash/opacity, markers and labels. Neither control case offers a Connect Missing Data checkbox/switch. Independently inspected original `themes.tsx` confirms `line.series.connectMissingData:true`, overriding the library's false default. Design must preserve this host default and distinguish it from a supported saved override; it must not invent a required original UI control.
- The positive additive FMP picture is consistent with cumulative amounts and normalized cumulative percentages. I initially misread the rendered tool preview; independent `System.Drawing.Bitmap` reads corrected that estimate: both selected and reloaded stacked PNGs have blue y457 and orange y167–168 at x103 in a 640×655 image. Against the retained ticks these are consistent with approximately 66 and 124 billion. There is no established visual discrepancy. These spot readings do not prove every endpoint, and first-canvas public draw calls do not capture complete series geometry.

## Remaining design decisions and acceptance limits

Freeze zero-denominator output, missing raw-point admission versus connected spans, finite-input overflow, series order and visibility-dependent normalization explicitly. Retain raw observations for tooltips/labels and storage, separate from derived cumulative coordinates. The source algorithm, default override and observed raw strings are sufficient inputs to this bounded design; exact zero/missing geometry still needs focused numerical and candidate checks. Duplicate categories and continuous/time axes were not characterized: either exclude them explicitly from this slice or add targeted evidence before accepting them. Do not expand this into an exhaustive caller matrix. Other callers, palettes and export behavior remain outside this original characterization.

No replacement implementation, light/dark parity, refresh/export equivalence, candidate-image checks or release checks pass by implication. Original plot images are reference samples, not candidate success screenshots. Future maintained code retains inventory-backed 400 physical lines/file, 300 logical units/file and 50 units/function caps.

## Selected sample publication review

Inspected the two financial `selected-two-series.png` chart crops. They show public financial field names, quarters, generic chart titles, axes and legends; no credentials, account identity or unrelated desktop content is visible. They are suitable for the already-authorized selected sample publication with explicit original-diagnostic captions and the financial-geometry limit above. Raw observations and authentication state are not included in this approval.

- Normalized sample SHA-256: `1f9d2f7047b63f6efe718d37964553d0850742cee64fd016e3e9e9e57467a5a0`.
- Stacked sample SHA-256, independently rechecked: `e320d82221a6a354c2eb5f2784e4999ef798306dae4013b7dbb1f4f923d22898`.

Only this review file was changed. No production, fixture or browser evidence was modified.

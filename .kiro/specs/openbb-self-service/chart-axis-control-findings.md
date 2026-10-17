# Preserve explicit axis positions and both tick roles

Four original-reference cases establish the axis-control inventory, position changes and independent category/value tick behavior. The [capture report](../../../artifacts/reviewed/ui-parity-axis-controls/capture/report.md) explicitly leaves the partial label case and four unrun cases unverified. This is bounded reference evidence, not candidate parity or a completed nine-case run.

The reference is original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Twenty completed control transactions retain all four reporting periods and both USD-million series: revenue 100/120/140/160 and operating income 20/25/30/40.

| Completed case | Original behavior to preserve |
| --- | --- |
| A01 inventory | Horizontal Axis Type offers Category/Number/Time for this year-prefixed text fixture; Vertical Axis Type is hidden. Both Ticks start off. Labels start in Verdana size 11; Horizontal Auto Rotate is on and Vertical is off. No visible axis-label Enabled toggle was found. |
| A02 positions | Top/Bottom and Right/Left move the addressed explicit, effective and live axis. Each emits an options event without changing an accumulated model-option leaf. A model-only observer misses the addressed change. |
| A03 category ticks | Width 3/Length 11 reach both category-position branches and four live tick lines. Off retains nodes behind hidden ancestors; on restores the visible ticks and details. |
| A04 value ticks | Width 2/Length 7 independently reach both number-position branches and five live tick lines. Numeric labels remain 0/50/100/150/200. Off/on retains details. |

Both tick cases restore the UI values to Width 1/Length 6 and then Ticks off. Grid settings remain unchanged. Restoring a UI value can leave explicit overrides where the untouched model had no field; this is not byte-identical baseline restoration. Opening one top-level axis group collapses the other, so later actions must address the original accordion state.

The fourth attempt timed out during A05 label restoration. Its raw failure and zeroed event counter remain unchanged. A separate recovery index hashes two intact chunks containing 31 ordered events: 20 link to completed A01-A04 and 11 belong to partial A05. Events beyond the last successful projection remain unresolved. The partial verifier checks only the completed cases, recovery provenance and cleanup.

All four attempts have owned-resource cleanup evidence. Only document scroll offsets were measured in this collector; internal editor offsets remain outside its evidence. The [navigation capture](chart-ui-navigation-findings.md) separately records its own scroll-retention observations.

The unfinished label, Number/Time, format and nonnumeric-visibility checks need a bounded follow-up. An offline I/O benchmark supports reducing repeated evidence-file work without increasing deadlines; it does not conclusively explain the runtime timeout. These findings refine the [consuming contract draft](chart-consuming-contract-draft.md), while full editor, persistence and deployment acceptance remain open.

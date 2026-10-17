# Preserve axis controls and distinguish stored options from rendered effects

The first four original-reference cases establish inventory, positions and independent category/value ticks. A separate [follow-up](../../../artifacts/reviewed/ui-parity-axis-followup/report.md) completes the five remaining label/type cases and records two original rendering findings. These two bounded captures supply reference evidence; they do not establish candidate parity. The [earlier report](../../../artifacts/reviewed/ui-parity-axis-controls/capture/report.md) remains unchanged, including its partial label case and unrun work.

The reference is original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. In the earlier A01-A04 capture, twenty completed control transactions retain all four reporting periods and both USD-million series: revenue 100/120/140/160 and operating income 20/25/30/40.

| Completed case | Original behavior to preserve |
| --- | --- |
| A01 inventory | Horizontal Axis Type offers Category/Number/Time for this year-prefixed text fixture; Vertical Axis Type is hidden. Both Ticks start off. Labels start in Verdana size 11; Horizontal Auto Rotate is on and Vertical is off. No visible axis-label Enabled toggle was found. |
| A02 positions | Top/Bottom and Right/Left move the addressed explicit, effective and live axis. Each emits an options event without changing an accumulated model-option leaf. A model-only observer misses the addressed change. |
| A03 category ticks | Width 3/Length 11 reach both category-position branches and four live tick lines. Off retains nodes behind hidden ancestors; on restores the visible ticks and details. |
| A04 value ticks | Width 2/Length 7 independently reach both number-position branches and five live tick lines. Numeric labels remain 0/50/100/150/200. Off/on retains details. |

Both tick cases restore the UI values to Width 1/Length 6 and then Ticks off. Grid settings remain unchanged. Restoring a UI value can leave explicit overrides where the untouched model had no field; this is not byte-identical baseline restoration. Opening one top-level axis group collapses the other, so later actions must address the original accordion state.

The fourth attempt timed out during A05 label restoration. Its raw failure and zeroed event counter remain unchanged. A separate recovery index hashes two intact chunks containing 31 ordered events: 20 link to completed A01-A04 and 11 belong to partial A05. Events beyond the last successful projection remain unresolved. The partial verifier checks only the completed cases, recovery provenance and cleanup.

All four attempts have owned-resource cleanup evidence. Only document scroll offsets were measured in this collector; internal editor offsets remain outside its evidence. The [navigation capture](chart-ui-navigation-findings.md) separately records its own scroll-retention observations.

The follow-up completes A05-A09 in one attempt under unchanged deadlines, without replaying A01-A04. Its 1,296 evidence assertions check 121 actions, 41 field edits, 37 screenshots and 39 ordered events. The [independent review](../../../artifacts/reviewed/ui-parity-axis-followup-runtime-review/review.md) inspected all 37 screenshots and the finite semantic claims. The event index and final counter agree without recovery; owned-resource cleanup passed. Neither its timing nor the offline I/O benchmark isolates the earlier timeout's cause.

| Follow-up case | Observed result and boundary |
| --- | --- |
| A05 horizontal labels | Font, size and spacing change the addressed category branches and plot layout. Manual inputs 315/45 produce -45/+45 degrees, with equivalent scene rotations. Auto Rotate removes manual rotation and restores it when turned off. UI values restore; raw overrides need not return to absence. |
| A06 vertical labels | Independent font/size/spacing changes affect the number branches and layout. Input 330 gives -30 degrees; Auto Rotate toggling restores it. Numeric labels remain 0/50/100/150/200; UI values restore. |
| A07 Number/Time | With UTC quarter-start milliseconds as reporting coordinates, category spacing 19, Ticks on and Width 3 become live defaults 11/off/1 after type changes. Returning to Category removes the old positional overrides. Financial values remain unchanged; epoch-coordinate formatting is separate from amount formatting. |
| A08 Time Format | YYYY-MM-DD and DD/MM/YYYY write distinct explicit/effective formats, but scene date strings stay unchanged and are visibly clipped. Diagnostics warn that the format options are ignored. This disproves the tested rendering effect without establishing a general formatter cause or correct time extent. |
| A09 conditional visibility | For FY24-Q1 through FY24-Q4, Axis Type is attached but hidden in each role's own expanded observation. Position, Font and Size remain visible. Other data/family predicates remain unverified. |

Font menus and scene fields establish requested families, not installed glyph-face identity. Four labels do not prove automatic collision rotation. Internal editor scroll, other themes/families, persistence and the candidate journey remain unverified. These findings refine the [consuming contract draft](chart-consuming-contract-draft.md) without activating a partial editor or changing controls.

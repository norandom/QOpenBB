# Runtime contracts: results and next implementation boundary

The new original-runtime captures support a bounded ordinary grid adapter design and selected nested editor contracts. They do not yet support complete application activation. The implemented adapter boundary is [ordinary grid capture](chart-grid-capture-design.md), using the frozen A2 signature and public Community GridApi values. The owner approved implementation, and tasks 2.38-2.40 are now independently accepted. See [ordinary capture verification](chart-grid-capture-verification.md); the application remains unactivated.

## What this batch established

| Boundary | Evidence | Decision |
| --- | --- | --- |
| Ordinary grid capture | Seven original-runtime cases; 15 independent array/identity/visibility assertions; startup, journey and cleanup exit 0 | Explicit-category flat capture can be designed without guessing category inference. Numeric-only and general multiple-category resolution remain separate. [Findings](chart-grid-runtime-next.md) |
| Nested editor | 18 UI actions, zero focused action failures, 22 offline assertions, captured events and effective leaves | Axis, series, legend, marker and selected Set Up contracts now have concrete namespaces and effects. Tooltip action is UI/event evidence only. [Findings](chart-editor-runtime-next.md) |
| Effective appearance | Eight existing cases, 15 input hashes and 908 finite leaf/container observations independently auditable | The existing style subset is insufficient for complete appearance. Custom backgrounds affect grid/subtitle colors; empty saved options cannot establish conflict precedence. [Audit](chart-appearance-next-audit.md) |

The research batch used Workspace 945e438a9a65c3eeef7073dbce64a03b02f0ff6f without changing production. Subsequent ordinary capture is accepted at 76edf85a46298f7bc5212ff9944e4b66e9baa4af. Original image/source and prior helper acceptance remain intact; controls, flags, dependencies and deployment configuration are unchanged.

## Why the next adapter uses grid values

The original charts a synthetic getter result of 200 when raw revenue is 100. A normalized percentage shown as `20.0 %` remains 0.2 in plotted data. Filtering/sorting precede inclusive row bounds; duplicate category labels retain distinct observation identities. These findings rule out raw-data copying, rendered-text parsing and category-label row IDs as general substitutes.

Reuse the existing public GridApi and snapshot validator. The adapter accepts already resolved category/series descriptors and range, reads unformatted grid values, and returns an immutable validated snapshot. It owns neither category inference nor persistence. The proposed readiness/error rules for unobserved malformed or unsupported inputs are internal design decisions, explicitly distinguished from original runtime behavior.

## Work after this batch

### Appearance and editor follow-up, 2026-10-17

The follow-up captures run the pinned original `38dffc33389aca0e4a87e0e88d42f7067aa220df` image. Candidate revision `76edf85a46298f7bc5212ff9944e4b66e9baa4af` remains untouched. Their findings refine the remaining integration contracts:

- [Derived colors and bounded conflicts](chart-appearance-contract-close.md): isolate background-dependent grid/subtitle colors. Preserve normalized-channel evaluation order; a byte-domain shortcut fails rounding edge cases.
- [Saved-option composition](chart-appearance-saved-composition.md): load nonempty saved models through the original hook and compare saved, combined and effective options for grouped columns and lines. This separates application composition from direct chart-library updates.
- [Tooltip and transpose output](chart-editor-contract-close.md): connect three original tooltip choices to effective state and displayed content, capture complete transposed values and restoration, and check settled Sum geometry.

These are reference contracts, not candidate renderer or persistence acceptance. Keep the next appearance design cohesive: resolved theme inputs, saved-family precedence and explicit mapper fields belong to the same consuming boundary. A standalone color helper would not close that boundary. Editor mapping should reuse the accepted option reducer and financial-formatting policy; transposition remains a separate numeric transformation contract. Do not infer a complete editor, arbitrary custom themes or backend reopen from these finite cases.

Independent Astra reviews accept the bounded [appearance evidence](../../../artifacts/reviewed/parity/appearance-contract-review/review.md), [saved-input composition](../../../artifacts/reviewed/parity/appearance-saved-review/review.md), and [editor evidence](../../../artifacts/reviewed/parity/editor-contract-review/review.md). Fresh checks pass 44 appearance assertions, 262,144 normalized-color comparisons, 99 saved-input assertions, 30 editor assertions and six Sum raster bar checks. The [link addendum](../../../artifacts/reviewed/parity/appearance-contract-review/publication-link-addendum.md) binds the final appearance documentation links. Research is accepted; no new implementation phase is approved.

1. Reuse accepted tasks 2.38-2.40 for ordinary resolved grid capture. Remaining numeric-only/general category and transformed/remote paths still need their own observed contracts before implementation. Existing implementation contracts remain unchanged.
2. In parallel research, close finite appearance collision/derived-color rules and the remaining editor invocation/output gaps. A fresh reviewer checks these contracts before their implementation tasks are dispatched.
3. Join accepted grid, appearance, formatting and editor behavior through the existing application session and entry points. Keep one owner for stored state and one integration lane for control wiring and guard removal.
4. Verify actual table -> chart -> customize -> export -> return -> save/reopen/restart against the original, including light/dark screenshots and financial values. Then complete the remaining capability matrix before image/release acceptance.

No partial helper result permits a hidden control, disabled feature, new flag or reduced product menu. The complete 1:1 product obligation remains unchanged. Dagger-only builds, image-pull deployment, Anthropic-before-Excel, external Jupyter and deferred PostgreSQL remain as planned.

Published evidence: [grid report](../../../artifacts/reviewed/parity/grid-runtime-next/report.md), [editor report](../../../artifacts/reviewed/parity/editor-runtime-next/report.md), and [appearance leaf ledger](../../../artifacts/reviewed/appearance-next-audit/leaf-ledger.json). Historical source-relative artifact paths in lane reports map to these mirrored directories.

## Evidence limits

The earlier editor batch retained its failed attempt separately from the successful focused run. Its immediate aggregate screenshot caught animation in progress and its transpose projection was incomplete. The [follow-up](chart-editor-contract-close.md) supplies settled Sum geometry and complete transposed values for its dark grouped-column fixture. Missing-value transpose semantics, other families and candidate parity remain unverified. An outgoing save payload is not backend persistence proof.

Both browser lanes used isolated disposable state and headless contexts; cleanup removed their containers, state and credentials. The known original datafeed script error remains visible in finite diagnostics. Dashboard fixture overlays do not establish production API or backend save/reopen behavior. Actual user menu reachability is distinguished from public-API filter/sort/visibility operations and the explicitly synthetic getter injection.

The artifact mirror contains only independently reviewed, completed allowlisted files. Raw account/request metadata, credentials, database state and unfiltered diagnostics remain excluded. Any sanitized derivative records its raw source hash separately; it does not claim byte identity with the raw file.

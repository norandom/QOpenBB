# Runtime contracts: results and next implementation boundary

The new original-runtime captures support a bounded ordinary grid adapter design and selected nested editor contracts. They do not yet support complete application activation. The next implementation proposal is [ordinary grid capture](chart-grid-capture-design.md), using the frozen A2 signature and public Community GridApi values. The owner approved the independently reviewed design. Tasks 2.38-2.40 passed independent task-graph review and await implementation approval; no adapter implementation has run.

## What this batch established

| Boundary | Evidence | Decision |
| --- | --- | --- |
| Ordinary grid capture | Seven original-runtime cases; 15 independent array/identity/visibility assertions; startup, journey and cleanup exit 0 | Explicit-category flat capture can be designed without guessing category inference. Numeric-only and general multiple-category resolution remain separate. [Findings](chart-grid-runtime-next.md) |
| Nested editor | 18 UI actions, zero focused action failures, 22 offline assertions, captured events and effective leaves | Axis, series, legend, marker and selected Set Up contracts now have concrete namespaces and effects. Tooltip action is UI/event evidence only. [Findings](chart-editor-runtime-next.md) |
| Effective appearance | Eight existing cases, 15 input hashes and 908 finite leaf/container observations independently auditable | The existing style subset is insufficient for complete appearance. Custom backgrounds affect grid/subtitle colors; empty saved options cannot establish conflict precedence. [Audit](chart-appearance-next-audit.md) |

The original image and source are unchanged. The candidate remains Workspace 945e438a9a65c3eeef7073dbce64a03b02f0ff6f. No production code, dependencies, controls, flags, build or deployment configuration changed. Prior helper acceptance remains intact.

## Why the next adapter uses grid values

The original charts a synthetic getter result of 200 when raw revenue is 100. A normalized percentage shown as `20.0 %` remains 0.2 in plotted data. Filtering/sorting precede inclusive row bounds; duplicate category labels retain distinct observation identities. These findings rule out raw-data copying, rendered-text parsing and category-label row IDs as general substitutes.

Reuse the existing public GridApi and snapshot validator. The adapter accepts already resolved category/series descriptors and range, reads unformatted grid values, and returns an immutable validated snapshot. It owns neither category inference nor persistence. The proposed readiness/error rules for unobserved malformed or unsupported inputs are internal design decisions, explicitly distinguished from original runtime behavior.

## Work after this batch

1. Approve reviewed tasks 2.38-2.40 for the real-grid fixture, adapter and independent joined verification. See the [task review](../../../artifacts/reviewed/grid-capture-tasks/review/review.md). The existing implementation contracts remain unchanged.
2. In parallel research, close finite appearance collision/derived-color rules and the remaining editor invocation/output gaps. A fresh reviewer checks these contracts before their implementation tasks are dispatched.
3. Join accepted grid, appearance, formatting and editor behavior through the existing application session and entry points. Keep one owner for stored state and one integration lane for control wiring and guard removal.
4. Verify actual table -> chart -> customize -> export -> return -> save/reopen/restart against the original, including light/dark screenshots and financial values. Then complete the remaining capability matrix before image/release acceptance.

No partial helper result permits a hidden control, disabled feature, new flag or reduced product menu. The complete 1:1 product obligation remains unchanged. Dagger-only builds, image-pull deployment, Anthropic-before-Excel, external Jupyter and deferred PostgreSQL remain as planned.

Published evidence: [grid report](../../../artifacts/reviewed/parity/grid-runtime-next/report.md), [editor report](../../../artifacts/reviewed/parity/editor-runtime-next/report.md), and [appearance leaf ledger](../../../artifacts/reviewed/appearance-next-audit/leaf-ledger.json). Historical source-relative artifact paths in lane reports map to these mirrored directories.

## Evidence limits

The editor's earlier failed attempt is retained separately from the successful focused run. Its aggregate arrays prove Q1 sums 220/45, while an immediate screenshot caught animation in progress; no settled aggregate geometry is claimed. Switch Category/Series changed model bindings, but complete transposed numerical output remains unverified. An outgoing save payload is not backend persistence proof.

Both browser lanes used isolated disposable state and headless contexts; cleanup removed their containers, state and credentials. The known original datafeed script error remains visible in finite diagnostics. Dashboard fixture overlays do not establish production API or backend save/reopen behavior. Actual user menu reachability is distinguished from public-API filter/sort/visibility operations and the explicitly synthetic getter injection.

The artifact mirror contains only independently reviewed, completed allowlisted files. Raw account/request metadata, credentials, database state and unfiltered diagnostics remain excluded. Any sanitized derivative records its raw source hash separately; it does not claim byte identity with the raw file.

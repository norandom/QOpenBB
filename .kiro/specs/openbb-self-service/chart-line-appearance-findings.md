# Original line appearance findings

The original dark-theme line chart connects an interior missing observation, hides markers by default, and retains title text when its title is disabled. These observations justify explicit fields in the next Cartesian mapper contract. They do not establish complete theme resolution or visual parity.

## Browser evidence, 2026-10-17

A separate Sol lane exercised the original Workspace image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, source label `38dffc33389aca0e4a87e0e88d42f7067aa220df`. One isolated headless Chromium session used Playwright 1.64 and CDP Runtime/Network at 1440x1000. A disposable container and synthetic dashboard kept owner state separate. The runner exited 0, closed its browser and removed its owned container.

The four periods contained revenue 100/null/140/160 and EPS 1.2/null/1.6/1.8. This mixed-unit original UI observation is not a valid single-axis financial acceptance fixture for the new mapper. Candidate fixtures must use matching explicit units and scale.

Five real save actions produced five selected-dashboard POST payloads. Relevant paths under the selected widget's `storage.default.chartModel.chartOptions`:

| Action | Observed state and rendering |
| --- | --- |
| Select line | Chart type becomes line; lines span the null period without point markers. |
| Type title, then disable it | `line.title.text` retains the typed text and `line.title.enabled=false`; no title is drawn. |
| Re-enable title | Only enabled changes to true; retained text is drawn. |
| Enable markers | `line.series.marker.enabled=true`; circles appear at the three non-null observations. The editor displays Circle and Size 7. |

No Connect Missing Data control appeared in the inspected Series panel. The source's explicit `connectMissingData=true` agrees with the default drawing, but a false-state UI action was not observed. Marker colors, inherited fonts, light mode and save/restart/reopen remain unverified.

Local evidence is retained under `artifacts/parity/line-style-capture/`: `report.md`, `widget-writes.json`, `payload-deltas.json`, `observations.json`, runner scripts, DOM snapshots, screenshots and sanitized diagnostics. Artifacts are ignored, not published source. Private disposable state must remain private.

- SHA-256 `widget-writes.json`: `18bc6ff5a2be04cf46d7efb593d18b05f906446f4577f999ebb231f84a0588f7`.
- SHA-256 `payload-deltas.json`: `af278a6d31f4c4a0e75b1a72b1b26eb3d149f4bc1ba1c750650c39485b844634`.

The original application emitted two `Unexpected token '<'` errors with CDP exceptions. Disposable onboarding initially returned 404, then 200. The capture therefore does not claim clean application diagnostics. The controller inspected the default-line and enabled-marker screenshots; numerical and payload evidence remain separate from visual observations.

## Effective-option API investigation

A parallel read-only Sol lane inspected pinned AG Charts 12.1.1 in the original frontend dependencies. Its `AgChartInstance.getOptions()` returns cloned user options, not fully processed defaults. `_Theme.getChartTheme()` exposes palette and theme configuration, but configuration can still contain reference/mix operations. It is not a plain flattened style object.

Internal `ChartOptions.processedOptions` follows user, override and default graph edges. Family overrides are inserted before common overrides; operation resolution and automatic enablement prevent replacement with a guessed object merge. These findings come from `ag-charts-community/dist/package/main.cjs.js` around lines 33718-34258 and `ag-charts-core/dist/package/main.cjs.js` around line 1899.

Constructing private ChartOptions directly in Node would omit the real chart factory's registry initialization and browser defaults. A future effective-options capture should inspect an actual original browser chart instance after its update completes, retaining supplied inputs separately from processed leaves. Private APIs may support reference research; production must not depend on them or copy their resolver.

## Consequence for the next design

Extend the existing resolved-input mapper with independent appearance leaves and explicit provenance. Retain its unit checks, observation values and stable series identities. Adopt ECharts' existing rendering fields; do not introduce another renderer framework. Complete original theme resolution, formatting, layout and application activation remain separate integration work.

These findings supplement [effective-style discovery](chart-effective-style-discovery.md) and the accepted [option-state boundary](chart-option-state-verification.md). They neither approve implementation nor complete requirements 4.8 or 4.9.

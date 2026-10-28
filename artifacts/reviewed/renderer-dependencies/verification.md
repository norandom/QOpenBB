# Highcharts runtime removal and remaining compatibility work

The published Workspace frontend no longer includes Highcharts as a dependency or active renderer. This does not establish complete replacement of every old Highcharts widget, or a comprehensive license audit.

Checked on 2026-10-28 against alpha `40676586728-1`, Workspace source `22180d8ec206e088a384f2a3c7345358b1832c7c`, published image `ghcr.io/norandom/qopenbb-workspace@sha256:ba994b3f22d05cea141d54084d5aae33723669a7f66b690cd579a95cec6f25f9`.

- Current frontend package manifest and Bun lock have no Highcharts, AG Grid Enterprise or AG Charts Enterprise package. Source has no Highcharts import, CDN load or license initialization.
- Read-only inspection of `/usr/share/nginx/html` covered 277 JS, HTML, text, JSON, CSS and source-map files, totaling 31,243,130 bytes. No Highcharts library/API, CDN, license-banner or bundle-filename signatures matched.
- Eleven textual references remain across four bundles: historical changelog text, legacy schema/type identifiers and the unsupported-renderer mapping. They are not evidence that the library ships. AG Enterprise strings in the Community bundle are diagnostic/example text, not an installed Enterprise dependency.
- Legacy `chart-highcharts` maps to `UnsupportedRenderer` in the current widget registry. A saved configuration can therefore be recognized without having a functioning replacement. This remains an open feature gap in the ECharts checklist.

Method: a disposable container with `--rm --network none --entrypoint python`, no mounts and no application startup. The adjacent [scanner](published-asset-scan.py) and [result](published-asset-scan.json) retain the exact artifact checks. Source inspection and signature scanning are bounded evidence; they do not establish the license obligations of every bundled dependency.

Keep package removal, functional parity and deployment acceptance as separate breadth entries. Reuse working ECharts/Plotly/table paths, and identify each remaining former Highcharts caller before implementing a replacement.

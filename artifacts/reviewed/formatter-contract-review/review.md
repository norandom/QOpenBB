# Formatting and custom-theme contract review

Reviewed 2026-10-17 against original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Source discovery is substantially sound. The changed contracts do not yet justify freezing all ordinary-chart runtime tasks: the nested control/event ledger and AG range/formatter invocation behavior remain unresolved. This assessment does not require completing other chart families or the full release before a bounded integration milestone.

## Evidence checked

- Read the application integration design, format-control contract, grid-range contract, editor inventory, custom-theme findings, requirements 4.8-4.9, documentation/workspace/delegation/complexity policies and kiro-validate-design rules. Core product, tech and structure steering files are absent, as the design already reports.
- Checked numbered original extracts for `Chart/utils.tsx:59-87,97-151,225-321`, `Chart/hooks/useChartOptions.tsx:350-489`, and `lib/utils/utils.ts:532-635`. Independently retrieved fiscal and numeric helpers and date regexes with `git show` at the original pin.
- Read custom-theme report, dark/light model and effective-state captures, assertions and cleanup record. No tests, builds, browsers or production edits were performed by this reviewer. Documentation-only work is outside production complexity caps; later production tasks retain 400 physical/300 logical/50 per function limits.

## Source wording corrections, resolved

The controller applied both corrections below. The final format-control contract was reread and agrees with the pinned source.

1. The fiscal shortcut applies only to a recognized datetime string at midnight. Date-only recognized strings continue into quarterly/annual conversion. `AgGridUtils.tsx` recognizes date-only `YYYY-MM-DD` or slash dates separately; its datetime regex requires a space before `HH:mm:ss`. ISO strings using `T` are not recognized by those regexes. The contract must preserve these distinctions rather than imply every date string at midnight bypasses fiscal conversion.
2. Axis and tooltip callbacks invoke `Index.valueFormatter` whenever the Index definition exists, without checking that the formatter is callable (`Chart/utils.tsx:146-151,257-262`). Describe that invocation condition accurately; this is a source assumption, not proof that an absent formatter is handled safely.

These corrections do not undermine the architecture. Numeric threshold strictness, tooltip versus label precision, detached normalized-percent scaling, bar/line namespaces and generated-common replacement are supported by source. Final AG precedence and callback invocation correctly remain unknown.

## Critical remaining design issue

**NO-GO for freezing affected runtime tasks:** the application design's control ledger still lacks complete nested field domains, emitted namespaces and event paths. Its capture contract also leaves AG category/series selection, reorder/aggregation and formatter invocation unresolved. Guessing those seams risks changed financial output or inert controls, contrary to requirements 4.8-4.9. Complete the finite three-family field/event and range/format capture ledger, then freeze only the dependencies exercised by the bounded milestone. Do not require unrelated full-release acceptance before that task freeze.

## Custom-theme scope

The captured `custom-dark` and `custom-light` grouped-column models and passing finite assertions support the two saved palette/background observations. Strokes have effective values but width zero, so they are not visible-outline evidence. The source's exact dark-base selector and palette/params replacement agree with the findings. Fixture GET overlays, successful save requests and local state do not establish independent backend reread/restart persistence or general custom-theme precedence. Keep those limitations explicit.

Final handoff and report distinguish browser Node exit 0 and output assertions exit 0 from shell-wrapper exit 1 caused by a trailing CR line after capture. The saved wrapper was normalized without rerunning it; no passing-wrapper claim is made. Both theme PATCH responses are reported as HTTP 200 JSON. The known HTML-as-JavaScript error remains disclosed. Cleanup reports the owned container absent and no remaining owned state. Independently read manifest SHA256: `529e121864a26864e94fd42e7eb09bf3c915a2d8cc6abbb52fe7a5be0ca189da`. No further heavy run is needed to accept these bounded observations.

## Assessment

The separate display policies and integrated-versus-detached boundary are strong, necessary contracts. **GO for incorporating the corrected source findings and bounded custom-theme observations; NO-GO for the affected runtime task freeze until the explicit nested-control/event and range/formatter seams are closed.** This is neither candidate runtime acceptance nor a request to finish all release capabilities first.

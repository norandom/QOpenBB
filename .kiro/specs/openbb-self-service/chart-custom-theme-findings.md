# Original custom chart theme contract

Saved custom themes are observable through the original admin editor. The bounded run on 2026-10-17 exercises only dark and light grouped-column charts. It is reference discovery for requirements 4.8 and 4.9, not candidate parity or implementation acceptance.

The [committed evidence copy](../../../artifacts/reviewed/parity/custom-theme-contract/report.md) preserves the exact recorded commands, outcomes and case files. The [sync manifest](../../../artifacts/reviewed/sync-manifest.json) maps published bytes to their local sources.

## Source contract

Pinned source `38dffc33389aca0e4a87e0e88d42f7067aa220df`, `terminalpro/src/components/ThemeSettings/ChartSettings.tsx`, provides paired Fill Color and Stroke Color fields, Background Color, Light Mode/Dark Mode editing tabs and Save Theme. Color fields expose `Hex color`; their label order identifies fill/stroke pairs. The editor mode selects which draft is changed; it does not itself change the application's active appearance mode.

Save Theme filters empty/null/undefined parameters and serializes each mode as `chartTheme: {baseTheme, palette: {fills, strokes}, params}`. `lib/state/tableChartThemes.ts` merges those chart settings with existing entity settings, updates its local store, then PATCHes `/admin/theme-settings`. Therefore an outgoing payload or local preview alone cannot establish backend persistence.

`General/Table/Chart/themes.tsx` selects `custom-${activeMode}` when that mode has baseTheme, palette and params, otherwise `openbb-${activeMode}`. `getCustomChartTheme` chooses the OpenBB dark base only for exact `ag-default-dark`; other saved base names select the OpenBB light base. It replaces the base palette and params with saved values, clones base overrides, then applies background image/navigator and item-styler changes. Generated chart defaults and saved chart overrides still have their own later precedence. The ordinary grouped-column fixture does not enable distinct-category fills or background images.

## Runtime evidence

The isolated original image is `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. The disposable admin account could open `/admin/theme-settings`, select Charts, edit both modes and invoke Save Theme. No store mutation was used to create these edits. Original UI edits and exact public PATCH inputs are captured in the ignored local `artifacts/parity/custom-theme-contract/` evidence folder.

| Mode | Saved base | First two fills | First two strokes | Background parameter |
| --- | --- | --- | --- | --- |
| Dark | ag-default-dark | #d12378, #ab34cd | #21dc65, #3ac9ed | #26394a |
| Light | ag-default | #136eab, #81ad32 | #d65123, #9b63d2 | #edf3d7 |

The synthetic table has Revenue 100/null/140/160 and Operating Income 20/null/30/40 in USD millions across 2024-Q1 through Q4. Displayed values are checked before chart entry. Dashboard GET overlays provide fixture provenance and prevent a claim of dashboard backend save/reopen persistence.

The probe reacquires the actual chart proxy and grid for each mode, uses public `waitForUpdate()`, and reads only finite selected leaves from the reference-only private `chart.chartOptions.processedOptions`. `getOptions()` is retained as input-theme evidence; it is not the inherited-default oracle.

## Limits and reproducibility

The first attempt successfully edited and saved both modes, then failed because a reused stock-theme assertion expected `openbb-dark` while the actual model was `custom-dark`. Its evidence and failure log remain in `first-pass/`. One corrected fresh-state remediation uses the custom theme-name assertion. The original bundle route returning HTML and resulting SyntaxError remain diagnostics, so this is not a clean application acceptance result.

Both settled models are groupedColumn with custom-dark/custom-light. Effective fills and strokes exactly match the first two saved palette entries, and effective visible backgrounds exactly match the saved backgroundColor values. Stroke width remains 0, so stroke inheritance is proven in effective options rather than visible outlines. The two Save Theme PATCH responses were HTTP 200 JSON. The independent output assertion command exited 0. Screenshots visibly show both edited palettes/backgrounds and the interior null interval. The browser journey completed, but its shell wrapper exited 1 on a trailing CR-only line after Node had exited 0; the saved wrapper was normalized without another runtime run. The exact commands, exit codes, hashes and verified owned cleanup result are in the local artifact report. This bounded run does not test arbitrary base-theme choices, per-widget color overrides, reset, background images, save failure, environment restart, other chart families, other permissions or candidate rendering. Source observations above must not be represented as runtime proof of those unexercised combinations. No production code or task approval changed.

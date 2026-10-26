# Advanced chart palettes: shared-theme follow-up

Implement image, gradient and pattern palettes as a separate shared-theme task. The owner set this boundary on 2026-10-26 so Funnel, Cone Funnel and Pyramid can proceed with stock themes and plain CSS-color palettes. Advanced palette support remains open; this note records scope and proposed acceptance, not implemented or tested behavior.

## Reachable gap

Persisted API theme settings can contain palette objects: `getEntityThemeSettings` provides a TypeScript generic, the theme store accepts settings without palette-schema validation, and `useAgThemes`/`getCustomChartTheme` pass the palette through. `projectCallerTheme` retains nonempty raw palette arrays at runtime, but shared `effectiveAppearance` rejects nonstring entries. Static string-array annotations do not make this input path unreachable.

Source inspection on 2026-10-26 follows `vendor/workspace/terminalpro/src/api/auth.api.ts` and the theme-settings store into `src/components/General/Table/Chart/themes.tsx`, then `caller/themeInputs.ts`, `application/effectiveAppearanceChrome.ts` and `application/effectiveAppearance.ts` beneath that Chart directory. These paths identify the retained Workspace source; this is source research, not an application or export test.

The [Funnel renderer design](funnel-renderer-design.md) defines the bounded renderer contract. Native expression research distinguishes Cone gradient/pattern fallback from its direct image-object range; it does not establish real-image drawing or export. Heatmap fallback and hierarchy mapping are family-specific and do not establish shared advanced-paint support.

## Current boundary

Until the shared task is accepted, preserve the original advanced-palette payload and report an explicit, accessible unsupported-paint diagnostic. Do not stringify objects, replace them with blue or generic fills, or report native parity. Keep the stored theme available for later recovery and supported-theme selection. Funnel's supported stock/plain-color work does not close this gap.

## Proposed acceptance

- [ ] Define validated shared paint contracts for image, gradient and pattern inputs, including malformed payloads, asset loading failures and renderer-specific limits.
- [ ] Apply the contract across shared theme selection and affected renderers, with explicit diagnostics where a paint cannot be drawn. Preserve financial values, stage/series identity and saved explicit style precedence.
- [ ] Verify original payload retention and effective appearance through save/reopen, theme changes and recovery; no silent coercion or destructive rewrite.
- [ ] Verify supported paints and asset failures in the application and actual export output, including Funnel, Cone Funnel and Pyramid. Record renderer coverage and any remaining unsupported cases separately.
- [ ] Independently review source and identified-image evidence before marking support complete; update capability/breadth records with actual checks and evidence.

Future executable tasks must carry the maintained production caps: 400 physical lines/file, 300 logical units/file and 50/function, with inventory and executable checker evidence. This documentation-only scope changes no production code, so those caps do not apply to this note.

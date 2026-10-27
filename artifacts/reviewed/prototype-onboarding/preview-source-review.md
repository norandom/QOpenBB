# Installed catalog preview repair

Independent Sol review accepted the source and generated assets on 2026-10-27. Runtime acceptance remains open until the rebuilt published pair completes the maintained fresh-account journey.

The existing-account Compose probe loaded actual AAPL annual income and verified the displayed symbol, date, USD revenue and refresh. It then failed strict diagnostics because the bundled FRED preview referenced an unavailable third-party image. This failed run is retained; it is not a passing installation rehearsal.

`catalog.py` now removes only external optional app preview fields (`img`, `img_light`, `img_dark`) and records each omission. Workspace uses its existing fallback. Local previews, layouts, groups, parameters and data remain unchanged. The actual generated app delta removes only FRED's external `img`.

Verification: the new case failed before the change (15 other cases passed); all 16 catalog tests pass afterward. Production size is 219 physical lines, 165 logical units and a largest function of 32, within 400/300/50. Source SHA-256: `8c99cffc43e91a0d56dcac9c598cfcea20e706f9449c59628dc06f356d545d4b`; test SHA-256: `ad51c955e4fc3da0cad8fcd5eb8c8f5ecc9a6026ee04a79b9badd61dd443a813`.

The clean committed CLI/runtime/upstream modules plus the patched catalog regenerated deterministically against the retained schema image, upstream source and matching inventory. Unrelated renderer changes were excluded. Widgets, routes, datasets and OpenAPI remain byte-identical. Five outputs change: apps, catalog report, provenance, hashes and compatibility. Compatibility now compares against the existing installed routes and reports no changes; its former record described initial generation. Independent review checked every output hash and the exact delta.

The supported starter path is Connections → Connect Backend → Apps → QOpenBB starter. Generic widgets inserted without required symbols still produce validation errors; that separate guard remains open. No diagnostic suppression or provider expansion is part of this repair.

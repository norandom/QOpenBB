## Review Verdict

- VERDICT: APPROVED
- TASK: 2.70
- REVIEW: Independent source/specification review and remediation review, 2026-10-18. Workspace HEAD `f4ba1bfb7f6c282485f0e31e2165d6aa1e2b7c08` plus reviewed working-tree resolver files and controller contract amendment.
- MECHANICAL_RESULTS: Fresh focused Vitest 19/19 pass, exit 0; fresh repair lint three files passes, exit 0; earlier six resolver files plus test lint also passed. New placeholder/secret scan clean. Boundary audit clean; the controller owns the reviewed shared-contract addition. RED verified in `appearance/red.log`, `appearance/conditional-red.log` and the concrete failing `appearance/legend-red.log`.
- SIZE: All reviewed production files pass 400/300/50. Final `appearance/complexity.json` has no errors or violations. Physical/logical/largest function: main 255/91/20, Axes 108/35/13, Colors 63/26/7, Defaults 95/9/4, Series 55/7/1, Values 98/57/14; controller-owned appearanceModel 89/72/no functions. Original six-file counts were independently rerun through `tools/quality/syntax_units.ts`; the final report covers the bounded repair.
- FINDINGS: No unresolved blocking findings.
- REMEDIATION: Completed. The legend control and drawn outline now retain their distinct source behavior.

The initial review found that an implicit legend outline was indistinguishable from explicit zero. Source `LegendMarker` leaves its width undefined and rendering inherits the series outline capped at two pixels, while the original control maps undefined to zero. The controller added `legendMarkerStrokeWidth` as separate effective renderer detail; `legend.markerStroke` remains the control value. The repair preserves explicit zero and derives bar/line inheritance from the appropriate resolved series width. The regression first failed with undefined instead of 2, then passed for bar width5 -> drawn2/control0, explicit legend0, and line marker stroke -> drawn1/control0.

Exact source evidence is `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-community/dist/package/main.cjs.js`: LegendMarker 35839, getMarkerStyles 36385, bar legendItemSymbol 41899 and line legendItemSymbol 44179. The enterprise bundle's getDefaultSliderParams 46394 and LegendPanel 48321 establish the separate control default. Line marker style is computed before its enabled flag is attached, so disabled markers retain the same effective outline value.

The canonical selected-theme clarification also resolves a correctness-sensitive ambiguity: the resolver owns stock/conditional defaults; the caller supplies parameter effects and explicit overrides, not blindly expanded defaults. A focused test proves recomputed stroke/title-spacing defaults and explicit width0/spacing20 precedence. Full field retention, selected-family precedence, saved baseline immutability, zero/false values, separate palettes, stable ordered IDs and source color/alpha derivation were reviewed.

The compiler log reports the known pre-existing `src/components/ds/plugins/typography.ts:1` TS2578, exit 2; compiler acceptance is not claimed. No browser, build, install or joined runtime acceptance was attempted. Renderer task 2.72 must consume `legendMarkerStrokeWidth` for drawing. Other lanes were not reviewed or edited.

### Reproduction and source identity

WSL Debian user `mc`, cwd `/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro`, pinned Node `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/effectiveAppearance.test.ts
node node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/application/effectiveAppearance.ts src/components/General/Table/Chart/application/appearanceModel.ts tests/unit/chart-application/effectiveAppearance.test.ts
```

Independent final run at 12:56:32: 19 passed, zero skips, 1.51 seconds, exit 0. Fresh repair lint: three files, no fixes, exit 0.

Final SHA256 identities for `application/effectiveAppearance` files:

- `.ts`: `09DA6B74E297270113A6BFB9A9553E4B0ADA01D24BA8FAA06716D345C6883440`
- `Axes.ts`: `1C18F7BC33E89671ED2EFA3D41F7E5BD5BA4A4911B3C1170B2DF5CE5720366F8`
- `Colors.ts`: `E7EFF3C6EABBD983B7707470021FF1D34E0E41C243E4691B357A8EC451989038`
- `Defaults.ts`: `5040418F6F948E1E3A6A51C32999183E20AD50EBCB71D288CD185A2773A96189`
- `Series.ts`: `27C375FA578032B43E869BB1DF861EF613F4257028C28E74732F855278B0C2BA`
- `Values.ts`: `DFAB74B335B618F08D0064C4A6168187765E05DFFCCA218D2E7FFE52A6D512BF`
- `application/appearanceModel.ts`: `C9574C0760E710AE8D71AAD94AA441CC1C04B77DB4D27CB655DD678C0C525FFF`
- `effectiveAppearance.test.ts`: `CFE0815554F4F2D4EB48F9FBE7B0C733E56A0624EC8860B2BEA67223FC809F5D`

SUMMARY: Task-local appearance resolution is approved after the legend inheritance repair; live rendering and persistence remain later integration gates.

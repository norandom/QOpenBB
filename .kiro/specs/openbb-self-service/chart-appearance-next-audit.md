# Appearance contract readiness audit

The existing evidence supports a typed, finite appearance projection and exact owned-source input composition. It does **not** yet support B2 as a complete application appearance resolver. In particular, custom background changes also change inherited grid and subtitle colors, and all eight baseline models have empty saved chart options. Do not infer general custom inheritance or saved-option collision precedence from these cases.

This independent read-only audit is dated 2026-10-17 and addresses requirements 4.8 and 4.9 and [Effective appearance](chart-application-integration-design.md#effective-appearance-48-49). It changes no production code, shared design, tasks or approval state. The result is a draft for the controller's contract review, not implementation acceptance.

## Evidence and reproduction

Original Workspace revision: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Recorded reference image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. No runtime was started by this audit. The original captures use a synthetic two-series USD-million fixture and reference-only processed options after `waitForUpdate`; their HTML-as-JavaScript baseline defect and overlaid dashboard GET limitation remain in force. These are original observations, not candidate acceptance or backend persistence evidence.

Run `py artifacts/appearance-next-audit/audit.py` from the repository root. Fresh result: exit 0, eight cases, 908 finite leaf/container observations, eight empty `model.chartOptions` objects. The initial Windows `python` attempt failed because it resolved to the unavailable Store alias; `py` ran the audit successfully without installation. No test/build/browser claim is made.

- [Input manifest](../../../artifacts/appearance-next-audit/input-manifest.json) records SHA-256 hashes of every inspected case and five original Git blobs. Git blob bytes are hashed directly, independently of checkout line-ending conversion.
- [Leaf ledger](../../../artifacts/appearance-next-audit/leaf-ledger.json) records each exact JSON pointer, value, runtime provenance, owned-source support where established, and the absence of a competing saved leaf. Empty arrays/objects are retained as finite containers, not interpreted as missing defaults.
- [Custom differences](../../../artifacts/appearance-next-audit/custom-differences.json) records every changed effective leaf against the corresponding stock grouped-column capture.
- Authoritative stock dark stacked/line cases are the `first-pass/` files named by the [stock report](../../../artifacts/reviewed/parity/theme-matrix/report.md). Its later failed Settings selector does not invalidate those earlier settled observations. Other cases use the report's final-pass files. Custom cases follow the [custom report](../../../artifacts/reviewed/parity/custom-theme-contract/report.md).

Core steering `product.md`, `tech.md` and `structure.md` are absent at the documented paths. Documentation, testing, complexity, delegation and CI steering were read. Spec language is English.

## Exact precedence established by owned source

Paths in this table are relative to original `vendor/workspace` at the pinned revision. Source line references describe source behavior only; they do not certify AG's final resolver.

| Responsibility | Source and exact rule | Runtime scope |
| --- | --- | --- |
| Active selection | `terminalpro/src/components/General/Table/Chart/themes.tsx:333-356`: build a custom entry only when baseTheme, palette and params are truthy; select `custom-${mode}` if built, else `openbb-${mode}`. This checks object presence, not palette length or color validity. | Stock/custom names observed for the two normal mode/base combinations. |
| Custom base | `themes.tsx:252-262`: exact `ag-default-dark` selects the OpenBB dark base; every other base name selects the OpenBB light base. Clone overrides; replace palette and params wholesale. | Dark/default dark and light/default combinations only. Other bases and mode/base mismatches lack runtime evidence. |
| Additional effects | `themes.tsx:264-279`: optional enabled image becomes common background image; navigator is navigator OR mini-chart; assign palette-aware itemStyler. `themes.tsx:128-175` defines distinct-color callback. | Effects are off in these captures. Source is not enabled-effect evidence. |
| Generated series/axes | `terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx:378-393`: lodash merge generated series with caller chartSeries, and generated axes with caller chartAxis, before family conversion. | No conflicting caller override cases here. |
| Family namespace | `useChartOptions.tsx:37-71`: line receives options, columns use `bar`; generated bar removes marker/connectMissingData and sets label placement outside-end. | Grouped and stacked both yield bar series; line remains line. Placement is not included by the current runtime projection. |
| Generated common | `useChartOptions.tsx:381-401`: legend comes from OpenBB theme for active mode, with owned fiscal formatter; navigator is regenerated. | Top legend matches the normal-mode cases. Callback invocation is not established by serialized input. |
| Stored composition | `useChartOptions.tsx:406-434`: replace stored `common` with generated `options.common`, then `merge(options, chartOptions)`. Saved family branches participate in that merge. | All eight saved chartOptions are `{}`. No runtime conflict winner is tested here. |
| AG final inheritance | Base theme, theme overrides, generated common, saved family, axis position and palette all feed AG. | Only the final leaves in the ledger are observed. No universal common/family/position priority is established by owned source. |

The source's `themePalette` variable is assigned inside a loop over both mode settings (`themes.tsx:327-359`); it is not a reliable standalone active-mode palette selector. The proposed resolver should consume the explicitly selected theme's palette. This is a typed ownership choice; do not silently reinterpret any legacy consumer of `themePalette`.

## Finite leaf contract

The ledger is authoritative for exact values. The table below groups leaves to make the implementation decision reviewable; it does not turn matching values into inheritance rules.

| Leaves | Observed values and provenance | Existing style consequence |
| --- | --- | --- |
| Background | Stock dark `#151518`, light `#FFFFFF`, visible true. Custom `#26394a` / `#edf3d7`; exactly match saved backgroundColor. Owned stock values: `themes.tsx:218-237`; custom replacement: 252-262. | `background` accepts fill; visibility has no field. |
| Typography | All captured families use `Verdana, sans-serif`, weight 400. Title size 12; legend and axis labels 11. Dark title/axis `#fff`; light title/axis `#181d1f`. Legend dark `#fff`, light `#000`. Owned legend: `themes.tsx:82-102`; title size:214; axis label sizes: `utils.tsx:278-283,311-323`. Other final typography is runtime evidence. | Populate separate title/legend/axis typography explicitly. A single light textColor cannot represent both title/axis and legend. Weight is missing. |
| Title | Disabled, retained text `Title`, spacing 20. | Existing title/titleEnabled preserve text and visibility, not spacing. |
| Legend | Enabled, top, spacing20, maxHeight50; item paddingX32/paddingY8; square marker size11/padding5. | Existing visible/position cover only two leaves. |
| Column colors | Ordered Revenue/Operating Income fills `#5090dc/#ffa03a`; dark strokes `#74a8e6/#ffbe70`, light `#2b5c95/#cc6f10`; width0, fillOpacity1. Custom fills/strokes match first two saved palette entries. | Explicit per-stable-ID fill, stroke and strokeWidth fit. Opacity has no field. Zero width makes stroke observations option-level, not visible-outline proof. |
| Line colors | Line stroke uses stock **fills**, not stock strokes. Marker fill uses fills; marker stroke uses mode-specific strokes; marker strokeWidth0. Line strokeWidth2, strokeOpacity1. | Populate stroke and marker fields independently. Do not assign bar stroke as line stroke. |
| Line behavior | connectMissingData true; disabled circle markers retain size7. Owned marker/connect defaults: `themes.tsx:180`. | Disabled branch of LineMarkerStyle drops shape/size; retain those in the stored baseline, not by resetting on toggle. A future editor-facing effective type needs retained details. |
| Padding/axes/grid/subtitle | Padding20 on all sides; category bottom, number left; axis titles disabled `Axis Title`; category line on, numeric line off; numeric grid on, category grid off. Exact typography, spacing and grid strokes are in the ledger. | These need explicit mapper extensions; existing ResolvedCartesianStyle cannot represent them. |

Custom background changes coincide with additional effective changes: dark subtitle `#7a7a7b` to `#838e98`, grid strokes `#515153` to `#5e6c79`; light subtitle `#707374` to `#696e65`, grid strokes `#e8e8e9` to `#d8dec5`. Both axes carry the changed grid style, even though category grid is disabled. The captures do not isolate which saved parameter causes these changes or establish a color formula. An adapter that substitutes palette/background while retaining stock grid colors fails the existing custom observations.

## Minimal typed proposal

Reuse `OptionBaseline`, `RuntimeOptions`, `SnapshotDiagnostic`, `CartesianFamily`, `ResolvedCartesianStyle` and `ChartDisplayPolicy` from their existing owners. The following describes a draft source-to-style boundary, not a second persistent model. Production must validate JSON before constructing these typed inputs; no saved callback is executed.

```typescript
type AppearanceMode = "dark" | "light";
interface AppearancePalette {
  readonly fills: readonly string[];
  readonly strokes: readonly string[];
}
type AppearanceTheme =
  | { readonly kind: "stock"; readonly name: "openbb-dark" | "openbb-light" }
  | { readonly kind: "custom"; readonly name: "custom-dark" | "custom-light";
      readonly baseTheme: string; readonly palette: AppearancePalette;
      readonly params: RuntimeOptions; readonly backgroundImage?: RuntimeOptions };
interface AppearanceInput {
  readonly mode: AppearanceMode;
  readonly theme: AppearanceTheme;
  readonly baseline: OptionBaseline;
  readonly family: CartesianFamily;
  readonly orderedSeriesIds: readonly string[];
  readonly generated: RuntimeOptions;
  readonly effects: { readonly distinctColors: boolean;
    readonly navigator: boolean; readonly miniChart: boolean };
  readonly precision: number;
}
type AppearanceResult =
  | { readonly status: "resolved"; readonly style: ResolvedCartesianStyle }
  | { readonly status: "invalid" | "unresolved";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
```

`generated` is data-only output of the owned generation/composition layer. Trusted formatting callbacks remain in the separate ChartDisplayPolicy; precision is an explicit compatibility input for the existing mapper and is not evidence of full formatting parity. Family must agree with the validated baseline. Series IDs must be unique, nonempty and supplied in the resolved selected order; labels are not identity. The selected theme name/mode must agree. Unknown saved JSON is preserved in OptionBaseline. A leaf whose effect cannot be resolved reports its original path; it must not be silently discarded.

The smallest useful rule is **direct assignment**, not a lookup of eight whole fixtures: use the selected stock palette or supplied custom palette, assign its entry at each resolved series index to that stable ID, map bar fill/stroke independently, and map line stroke from fills with separate marker strokes. Populate each observed typography role explicitly. For custom grouped columns, take background from the selected params.backgroundColor. This follows owned custom replacement and the two observed palette positions; arbitrary palette cycling, exhausted/empty arrays, reordered selection persistence and custom line/stacked are not established. Do not use the mapper's modulo fallback to invent an upstream allocation rule. These cases need named evidence before claiming general allocation parity.

This rule can produce the existing mapper's finite subset without guessing AG inheritance. Its custom-input generalization is a narrow proposed contract, supported by two concrete examples, not proof of arbitrary themes. For full B2 readiness, the mapper join must represent the remaining observed leaves and resolve derived custom colors; a successful subset must not be exposed as complete application readiness or used to hide unsupported editor controls. Do not add a fixture-ID input or recognize exact screenshots as a product capability gate.

### Explicit mapper extension proposal

Extend the existing style owner through cohesive types for: four-side padding; background visibility; caption enabled/text/font family/size/weight/style/color/spacing; independent category/number axis labels and titles; axis line enabled/width/color; grid enabled/width/style entries; detailed legend spacing/maxHeight/item padding/marker; series opacity and retained marker shape/size even when disabled. Keep line and column style fields distinct. Do not merge arbitrary AG option JSON into ECharts options.

Only observed fields may be required immediately. Absent projected values such as axis line color and legend marker strokeWidth must remain explicitly unresolved until their source property name/presence is checked. Grid style.stroke is available; it does not establish axis-line color. ECharts projection needs its own public-interface mapping and candidate rendering checks. This audit proposes no dependency and does not claim that AG spacing and ECharts spacing have identical semantics.

Any eventual maintained implementation must keep 400 physical lines/file, 300 logical units/file and 50/function, use the existing inventory/checker foundation, and record mapper extension ownership before work. Audit documentation and research artifacts are outside production caps; that exclusion is not production checker acceptance.

## Specific capture changes and disproof conditions

1. Extend the finite probe with a presence record for each selected field (`own`, `undefined`, `null`, or finite value). Existing `pick` plus JSON serialization drops undefined, and the probe does not select fontStyle, series lineDash, label placement, shadow or tooltip settings. Confirm the real property name for axis line color before recording absence. Do not serialize entire internal contexts or callbacks.
2. For each editor mutation, record settled model options, generated data-only chartThemeOverrides, effective leaves and screenshot under one action ID. Change one leaf at a time, retain title/marker details through disable-enable, and capture reset/removal separately. Source input markers are not callback invocation evidence.
3. Exercise actual conflicts for the admitted leaves: generated common versus saved common; common versus bar/line title and legend; family axis versus position-specific axis; custom palette/background versus per-widget saved color. Preserve before/after and the exact action/reopen stage. A direct API-only injection must be labeled synthetic input resolution, not UI reachability or persistence.
4. Isolate custom background-only, palette-only and optional text/grid parameter changes while keeping base/mode fixed. Capture the two derived color leaves above. Either establish a supported finite parameter-to-leaf rule or require explicit effective theme tokens; do not infer a blending formula from two samples.
5. Add a selected-series reorder and a palette-boundary case before accepting index allocation beyond observed positions. Add custom stacked/line separately before admitting their custom behavior. Enabled images, navigator, mini-chart and distinct-datum fills retain their own later contracts.

The current direct assignment hypothesis is disproved if a settled observed case maps the same selected palette entry to a different series position under the stated inputs. A claim that palette/background injection gives full custom parity is already disproved by the existing grid/subtitle differences. A claim of general saved precedence is unverified until conflicting values are exercised. None of these failures should be converted into an unavailable product surface or new feature gate.

## Readiness and publication safety

Ready for controller review: exact source composition, the finite leaf ledger, direct existing-style subset mapping and the named mapper extensions. Not ready: complete B2 resolver acceptance, arbitrary custom inheritance, final conflict precedence, complete editor/candidate parity, or release.

The only new publication candidates from this lane are this document and `artifacts/appearance-next-audit/{audit.py,input-manifest.json,leaf-ledger.json,custom-differences.json,verification.json}`. They contain reviewed synthetic chart values, repository-relative paths, public source hashes and audit results. Do not mirror an entire run directory. No environment, credential, raw browser profile, authentication trace, private account/database state, dependency cache or image archive was read or generated. The controller must independently review this allowlist and synchronize completed files with actual hashes before explicit staging; this audit does not stage or publish them.

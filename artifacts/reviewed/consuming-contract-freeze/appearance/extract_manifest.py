"""Regenerate finite, data-only contract evidence. No browser or dependency writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CHART = "vendor/workspace/terminalpro/src/components/General/Table/Chart/"
DEP = Path("/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/echarts")
LEDGER = "artifacts/reviewed/appearance-next-audit/leaf-ledger.json"
SAVED = "artifacts/reviewed/parity/appearance-saved-composition/cases.json"
CLOSE = "artifacts/reviewed/parity/appearance-contract-close/cases.json"
INPUTS = [LEDGER, SAVED, CLOSE,
          "artifacts/reviewed/appearance-next-audit/input-manifest.json",
          "artifacts/reviewed/parity/appearance-saved-composition/case-inputs.json",
          "artifacts/reviewed/parity/appearance-saved-composition/source-manifest.json",
          "artifacts/reviewed/parity/appearance-contract-close/source-manifest.json",
          "artifacts/reviewed/parity/editor-contract-close/tooltip-Single-hover.json",
          "artifacts/reviewed/parity/editor-contract-close/tooltip-Multiple-hover.json",
          "artifacts/reviewed/parity/editor-contract-close/tooltip-Compact-hover.json",
          "vendor/workspace/terminalpro/package.json",
          "vendor/workspace/terminalpro/bun.lock"]
INPUTS += [CHART + p for p in ["application/types.ts", "application/appearanceContracts.ts",
          "application/appearanceComposition.ts", "application/appearanceColors.ts",
          "application/financialFormatting.ts", "echarts/cartesianTypes.ts",
          "echarts/cartesianStyle.ts", "echarts/cartesian.ts", "themes.tsx",
          "hooks/useChartOptions.tsx"]]
TARGETS = {
    "global": ("types/src/util/types.d.ts", ["backgroundColor?: ZRColor", "interface TextCommonOption", "interface ItemStyleOption", "interface LineStyleOption", "fontWeight?: ZRFontWeight", "fontFamily?: string", "fontSize?: number | string", "ZRLineType ="]),
    "caption": ("types/src/component/title/install.d.ts", ["show?: boolean", "text?: string", "subtext?: string", "itemGap?: number", "padding?: number | number[]", "textStyle?: TitleTextStyleOption", "subtextStyle?: TitleTextStyleOption"]),
    "caption-runtime": ("lib/component/title/install.js", ["if (!titleModel.get('show'))", "textRect.height + titleModel.get('itemGap')"]),
    "axis": ("types/src/coord/axisCommonTypes.d.ts", ["name?: string", "nameTextStyle?: AxisNameTextStyleOption", "nameGap?: number", "axisLine?: AxisLineOption", "splitLine?: SplitLineOption", "margin?: number"]),
    "axis-position": ("types/src/coord/cartesian/AxisModel.d.ts", ["position?: CartesianAxisPosition"]),
    "legend": ("types/src/component/legend/LegendModel.d.ts", ["itemGap?: number", "itemWidth?: number", "itemHeight?: number", "padding?: number | number[]", "orient?: LayoutOrient", "textStyle?: LabelOption"]),
    "grid": ("types/src/coord/cartesian/GridModel.d.ts", ["outerBounds?: BoxLayoutOptionMixin", "outerBoundsMode?", "containLabel?: boolean"]),
    "bar": ("types/src/chart/bar/BarSeries.d.ts", ["interface BarSeriesOption"]),
    "line": ("types/src/chart/line/LineSeries.d.ts", ["lineStyle?: LineStyleOption", "connectNulls?: boolean", "showSymbol?: boolean"]),
    "symbol": ("types/src/util/types.d.ts", ["interface SymbolOptionMixin", "symbolSize?", "symbol?"]),
    "tooltip": ("types/src/component/tooltip/TooltipModel.d.ts", ["trigger?: 'item' | 'axis' | 'none'", "renderMode?: 'auto' | TooltipRenderMode", "TopLevelFormatterParams"]),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def target_evidence():
    assert read("vendor/workspace/terminalpro/package.json")["dependencies"]["echarts"] == "6.0.0"
    assert json.loads((DEP / "package.json").read_text())["version"] == "6.0.0"
    lock = (ROOT / "vendor/workspace/terminalpro/bun.lock").read_text()
    assert 'echarts@6.0.0' in lock
    records = []
    for group, (relative, needles) in TARGETS.items():
        path = DEP / relative
        lines = path.read_text().splitlines()
        matches = []
        for needle in needles:
            hits = [{"line": i + 1, "text": line.strip()} for i, line in enumerate(lines) if needle in line]
            assert hits, (relative, needle)
            matches.append({"needle": needle, "matches": hits[:4]})
        records.append({"id": group, "path": str(path), "sha256": digest(path), "members": matches})
    return {"version": "6.0.0", "claim": "local member existence and declared semantics only; no parity or runtime verification", "files": records}


def typed_field(pointer):
    p = pointer.split("/")[2:]
    if p[0] == "mode":
        return "AppearanceInput.mode", '"dark" | "light"', None, "identity"
    if p[0] == "family":
        return "AppearanceInput.family", '"groupedColumn" | "stackedColumn" | "line"', None, "identity"
    if p[0] == "axes":
        role = "categoryAxis" if p[1] == "0" else "numberAxis"
        tail = p[2:]
        if tail[0] in ("type", "keys"):
            return role + "." + tail[0], "source identity; not a visual field", None, "identity"
        target = "xAxis" if p[1] == "0" else "yAxis"
        if tail[0] == "position":
            return role + ".position", '"top" | "bottom" | "left" | "right"', target + ".position", "axis-position"
        if tail[0] == "title":
            typography = "typography." if tail[-1] in ("color", "fontFamily", "fontSize", "fontWeight") else ""
            return role + ".title." + typography + tail[-1], leaf_type(tail[-1]), target + "." + {"enabled": "name (empty while disabled)", "text": "name", "spacing": "nameGap"}.get(tail[-1], "nameTextStyle." + tail[-1]), "axis"
        if tail[0] == "label":
            return role + ".label." + tail[-1], leaf_type(tail[-1]), target + ".axisLabel." + {"enabled": "show", "spacing": "margin"}.get(tail[-1], tail[-1]), "axis"
        if tail[0] == "line":
            return role + ".line." + tail[-1], leaf_type(tail[-1]), target + ".axisLine." + {"enabled": "show", "width": "lineStyle.width"}.get(tail[-1], "lineStyle.color"), "axis"
        rename = {"stroke": "color", "strokeWidth": "width", "fillOpacity": "opacity", "lineDash": "dash"}
        field = role + ".grid." + ("styles[0]." + rename.get(tail[-1], tail[-1]) if "style" in tail else tail[-1])
        return field, leaf_type(tail[-1]), target + ".splitLine." + {"enabled": "show", "stroke": "lineStyle.color", "strokeWidth": "lineStyle.width", "lineDash": "lineStyle.type", "fillOpacity": "lineStyle.opacity", "width": "lineStyle.width"}[tail[-1]], "axis"
    if p[0] == "series":
        tail = p[2:]
        field = "series[$id]."
        if tail[0] in ("type", "xKey", "yKey", "yName"):
            return "AppearanceInput.series[$sourceKey]." + tail[0], "string", None, "identity"
        if tail[0] == "marker":
            return field + ".".join(tail), "RetainedMarkerStyle (inapplicable for bar null observation)" if len(tail) == 1 else leaf_type(tail[-1]), {"enabled": "series[$id].showSymbol", "shape": "series[$id].symbol", "size": "series[$id].symbolSize", "fill": "series[$id].itemStyle.color", "stroke": "series[$id].itemStyle.borderColor", "strokeWidth": "series[$id].itemStyle.borderWidth"}.get(tail[-1]), "symbol"
        if tail[0] == "label":
            return field + ".".join(tail), leaf_type(tail[-1]), "series[$id].label." + ("show" if tail[-1] == "enabled" else tail[-1]), "global"
        key = tail[-1]
        if key in ("connectMissingData", "strokeOpacity"):
            return "line.connectMissingData" if key == "connectMissingData" else field + key, leaf_type(key), "series[$id]." + {"connectMissingData": "connectNulls", "strokeOpacity": "lineStyle.opacity"}[key], "line"
        channel = field + key
        return channel, leaf_type(key), "series[$id]." + {"fill": "itemStyle.color (bar only)", "stroke": "itemStyle.borderColor (bar) / lineStyle.color (line)", "strokeWidth": "itemStyle.borderWidth (bar) / lineStyle.width (line)", "fillOpacity": "itemStyle.opacity (bar only)"}[key], "global"
    if p[0] in ("title", "subtitle"):
        key = p[-1]
        field = "subtitle." + ("typography." if key in ("color", "fontFamily", "fontSize", "fontWeight") else "") + key
        if p[0] == "title":
            field = {"text": "title", "enabled": "titleEnabled", "spacing": "titleSpacing"}.get(key, "typography.title." + key)
        return field, leaf_type(key), "title[$role]." + {"enabled": "show", "text": "text", "spacing": "top (requires layout)"}.get(key, "textStyle." + key), "caption"
    if p[0] == "legend":
        key = p[-1]
        field = "legendGeometry." + ".".join(p[1:]).replace("item.", "")
        if key in ("enabled", "position"):
            field = "legend.visible" if key == "enabled" else "legend.position"
        elif "label" in p:
            field = "typography.legend." + key
        return field, leaf_type(key), "legend." + {"enabled": "show", "position": "top/bottom/left/right + orient", "spacing": "layout gap (no direct equivalent)", "maxHeight": "height (not equivalent)", "paddingX": "itemGap (not equivalent)", "paddingY": "itemGap (not equivalent)", "shape": "icon", "size": "itemWidth + itemHeight", "padding": "textStyle.padding (not equivalent)"}.get(key, "textStyle." + key), "legend"
    if p[0] == "background":
        return "background" if p[-1] == "fill" else "backgroundVisible", leaf_type(p[-1]), "backgroundColor" if p[-1] == "fill" else "backgroundColor alpha/transparent policy (open)", "global"
    return ".".join(p), "number", "grid.outerBounds." + p[-1] + " + caption/legend layout (not direct chart padding)", "grid"


def leaf_type(key):
    if key in ("enabled", "visible", "connectMissingData"):
        return "boolean"
    if key in ("fontWeight",):
        return 'number | "normal" | "bold" | "bolder" | "lighter"'
    if key == "lineDash":
        return "readonly number[]"
    if key in ("text", "color", "fontFamily", "position", "shape", "fill", "stroke"):
        return "string"
    return "number"


def color_case(item, sha):
    effective = item["effective"]
    result = {key: effective[key] for key in ("background", "title", "subtitle", "legend") if key in effective}
    for key in ("axes", "series"):
        if key in effective:
            result[key] = effective[key]
    def compact(value):
        if isinstance(value, list):
            return [compact(x) for x in value]
        if isinstance(value, dict):
            if value.get("presence") == "absent":
                return {"presence": "absent"}
            return {k: compact(v) for k, v in value.items() if not (isinstance(v, dict) and v.get("presence") == "absent")}
        return value
    return {"referenceCase": item["id"], "path": CLOSE, "sha256": sha, "rawInput": item["input"], "rawEffectivePresentFields": compact(result), "omittedAbsentFields": "See original case; omission is not a default."}


def finite_precedence(pointer):
    if pointer.startswith("/effective/title/") and pointer.rsplit("/", 1)[-1] in ("enabled", "text", "color", "fontSize"):
        return "Saved bar/line family title named leaves survive generated-common replacement in bar-family/line-family; exact rawSaved/rawHookCombined/rawEffective below. Common-only saved title does not survive. Other title collisions remain open."
    if pointer == "/effective/legend/position":
        return "Saved family right wins in four-case comparison; saved common bottom is replaced by generated common top. Other theme/family collisions remain open."
    if pointer == "/effective/axes/1/label/color":
        return "Captured saved number.left.label #abcdef wins over generic number.label #654321 in bar-family/line-family; other positions/leaves remain open."
    if "/series/" in pointer and pointer.rsplit("/", 1)[-1] in ("fill", "stroke", "strokeWidth", "enabled", "shape", "size", "connectMissingData"):
        return "Named saved family channels and disabled marker values are finite observations in savedCompositionCases. Bar fill/stroke/3px and line stroke/5px with independent marker channels are distinct. Supplied line.series.fill is absent effective; common fill does not beat generated colors. General inheritance/allocation remains open."
    return "Captured ledger cases contain no competing saved leaf; use named saved/proxy evidence separately."


def main():
    ledger = read(LEDGER)
    allowed_captures = {x["path"] for x in read("artifacts/reviewed/appearance-next-audit/input-manifest.json") if "case" in x}
    assert {x["path"] for x in ledger} <= allowed_captures
    inputs = sorted(set(INPUTS) | allowed_captures)
    hashes = {p: digest(ROOT / p) for p in inputs}
    groups = {}
    for item in ledger:
        groups.setdefault(item["pointer"], []).append(item)
    rows = []
    for pointer, items in groups.items():
        field, kind, target, target_group = typed_field(pointer)
        rows.append({"id": pointer.removeprefix("/effective/").replace("/", "."),
                     "typedField": field, "typescriptValueType": kind,
                     "observedSourcePaths": sorted(set(x["ownedSourceSupport"] for x in items)),
                     "evidence": [{"referenceCase": items[0]["case"], "path": items[0]["path"], "pointer": pointer, "rawValue": items[0]["value"], "sha256": hashes[items[0]["path"]]}],
                     "allObservedValues": [{"referenceCase": x["case"], "rawValue": x["value"]} for x in items],
                     "precedence": {"known": finite_precedence(pointer), "unresolved": "Arbitrary common/family/theme/position collisions and inherited defaults outside these observations."},
                     "retainedDisabledValues": "Retain raw field and baseline option presence regardless of enabled. Disabled marker circle/7 and captions Title/Subtitle/Axis Title are not erased.",
                     "publicEChartsTarget": target, "lockedTargetEvidence": target_group,
                     "expectedValue": "For each resolved admitted source value, use that evidence row's rawValue; absence/null must not be converted into an invented default.",
                     "optionAssertion": "Assert exact target equality for resolved leaf, source-unit numeric data unchanged, plus unresolved coverage. A member's existence does not establish equivalent geometry.",
                     "visualAssertion": "Matched viewport/mode candidate capture checks this role's visibility/color/typography/geometry independently; no such candidate assertion ran here.",
                     "status": "identity-only" if target_group == "identity" else "projection-shape-defined-original-resolution-open"})
        if pointer == "/effective/mode":
            rows[-1]["transformation"] = "Direct dark/light session mode value. Resolve theme.name separately from actual chartThemes[0]; mode does not distinguish stock/custom. Reject a selected name suffix inconsistent with mode."
            rows[-1]["optionAssertion"] = "Identity assertion only: mode equals source session mode; no ECharts theme name is inferred from this row."
    supplemental = [
        {"id": "axis-line-color", "typedField": "categoryAxis.line.color / numberAxis.line.color", "typescriptValueType": "string", "observedSourcePaths": [], "evidence": [], "precedence": {"known": None, "unresolved": "Ledger does not capture axis-line stroke; gridLine color is a separate channel."}, "retainedDisabledValues": "Retain supplied line color while hidden.", "publicEChartsTarget": "xAxis/yAxis.axisLine.lineStyle.color", "lockedTargetEvidence": "axis", "expectedValue": None, "optionAssertion": "No invented grid-color alias", "visualAssertion": "Capture explicit axis-line color and conflicting grid color", "status": "capture-required"},
        {"id": "background-image", "typedField": "Not frozen: original background image schema/effect capture required", "typescriptValueType": "No runtime image type asserted yet", "observedSourcePaths": [], "evidence": [], "precedence": {"known": None, "unresolved": "Enabled image effect, sizing, positioning and export not captured."}, "retainedDisabledValues": "Preserve disabled source image data in baseline.", "publicEChartsTarget": None, "lockedTargetEvidence": None, "expectedValue": None, "optionAssertion": "Do not pretend backgroundColor renders image", "visualAssertion": "Enabled image/theme/export reference capture", "status": "capture-required"},
        {"id": "series-line-dash", "typedField": "series[$id].lineDash", "typescriptValueType": "readonly number[]", "observedSourcePaths": [], "evidence": [], "precedence": {"known": None, "unresolved": "Nondefault line dash is absent from ledger."}, "retainedDisabledValues": "Retain pattern when stroke hidden.", "publicEChartsTarget": "series[$id].lineStyle.type", "lockedTargetEvidence": "global", "expectedValue": None, "optionAssertion": "Explicit dash array only after source observation", "visualAssertion": "Nondefault dash at known DPR", "status": "capture-required"},
    ]
    tooltip = []
    for label in ("Single", "Multiple", "Compact"):
        path = f"artifacts/reviewed/parity/editor-contract-close/tooltip-{label}-hover.json"
        data = read(path)
        texts = [v["text"] for a in data["attempts"] for v in a["visible"] if v.get("class") == "ag-charts-tooltip-content"]
        tooltip.append({"referenceCase": label, "path": path, "sha256": hashes[path], "rawText": texts})
    supplemental.append({"id": "tooltip-mode", "typedField": "tooltip.mode", "typescriptValueType": '"single" | "shared" | "compact"', "observedSourcePaths": ["composed.bar.tooltip.mode", "compatibility/editorEvents.ts tooltip-mode"], "evidence": tooltip, "precedence": {"known": "Grouped column editor Multiple stores shared; accepted reducer writes bar.tooltip.mode.", "unresolved": "Null/tie/order, keyboard invocation, line/stacked modes; no general common/family tooltip rule."}, "retainedDisabledValues": "Retain stored mode independently of hover visibility.", "publicEChartsTarget": "tooltip.trigger + trusted tooltip.formatter; event bridge retains hovered stable ID", "lockedTargetEvidence": "tooltip", "expectedValue": "single/shared/compact as decoded by accepted event mapper", "optionAssertion": "single resolves hovered ID only; shared/compact content per original finite case", "visualAssertion": "Separate pointer hit/row/series identity and actual rendered content", "status": "content-observed-invocation-open"})
    rows.extend(supplemental)
    write("locked-echarts-targets.json", target_evidence())
    write("field-manifest.json", {"schemaVersion": 1, "date": "2026-10-17", "workspaceRevision": "ea02ec15956dee8d2c8a06825387a570757db12d", "status": "draft contract inputs; no design approval or runtime acceptance", "ledgerRowsReferenced": len(ledger), "observedFieldGroups": len(groups), "supplementalCaptureGates": len(supplemental), "manifestRows": len(rows), "types": "proposed-types.ts", "referenceSources": [{"referenceCase": x["case"], "path": x["path"], "sha256": hashes[x["path"]]} for x in read("artifacts/reviewed/appearance-next-audit/input-manifest.json") if "case" in x], "rows": rows, "savedCompositionCases": [{"referenceCase": x["actionId"], "path": SAVED, "sha256": hashes[SAVED], "rawSaved": x["syntheticSavedFixture"], "rawHookCombined": {family: {k: v for k, v in branches.items() if k in ("title", "legend", "series")} for family, branches in x["hookCombined"].items() if isinstance(branches, dict)}, "rawEffective": x["effective"]} for x in read(SAVED)], "proxyColorAndCollisionCases": [color_case(x, hashes[CLOSE]) for x in read(CLOSE)]})
    write("input-allowlist.json", {"purpose": "Exact finite reviewed inputs and local source hashes; no private runtime/account/diagnostic files", "files": [{"path": p, "sha256": hashes[p]} for p in inputs]})
    outputs = ["draft.md", "proposed-types.ts", "extract_manifest.py", "field-manifest.json", "input-allowlist.json", "locked-echarts-targets.json"]
    write("output-allowlist.json", {"status": "draft local artifacts only", "files": [{"path": str((OUT / p).relative_to(ROOT)).replace("\\", "/"), "sha256": digest(OUT / p)} for p in outputs]})
    print(json.dumps({"observations": len(ledger), "observedFieldGroups": len(groups), "supplementalCaptureGates": len(supplemental), "manifestRows": len(rows), "inputFiles": len(inputs), "targetGroups": len(TARGETS), "runtimeExecuted": False}))


if __name__ == "__main__":
    main()

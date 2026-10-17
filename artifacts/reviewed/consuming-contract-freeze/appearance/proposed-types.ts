// Design artifact: merge these extensions into existing production contracts.
import type { RuntimeOptions } from "../../../../vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/legacyTypes";
import type { OptionBaseline } from "../../../../vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/optionStateTypes";
import type { SnapshotDiagnostic } from "../../../../vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/snapshotTypes";
import type { AppearanceColorTokens } from "../../../../vendor/workspace/terminalpro/src/components/General/Table/Chart/application/appearanceContracts";
import type { CartesianSeriesStyle, ResolvedCartesianStyle as ExistingResolvedCartesianStyle } from "../../../../vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/cartesianTypes";

export type Family = "groupedColumn" | "stackedColumn" | "line";
export interface ThemeSelection {
  readonly name: "openbb-dark" | "openbb-light" | "custom-dark" | "custom-light";
  readonly base: "ag-default" | "ag-default-dark";
  readonly params: RuntimeOptions;
  readonly overrides: RuntimeOptions;
  readonly palette: { readonly fills: readonly string[]; readonly strokes: readonly string[] } | null;
  readonly colorTokens: AppearanceColorTokens;
}
export interface SeriesIdentity {
  readonly id: string;
  readonly sourceKey: string;
  readonly label: string;
}
export interface AppearanceInput {
  readonly mode: "dark" | "light";
  readonly family: Family;
  readonly baseline: OptionBaseline;
  readonly generated: RuntimeOptions;
  readonly theme: ThemeSelection;
  readonly series: readonly SeriesIdentity[];
  readonly categoryColumnId: string;
  readonly chartBarFillEnabled: boolean;
}
export interface RoleTypography {
  readonly color: string;
  readonly fontFamily: string;
  readonly fontSize: number;
  readonly fontWeight: number | "normal" | "bold" | "bolder" | "lighter";
}
export interface CaptionStyle {
  readonly enabled: boolean;
  readonly text: string;
  readonly typography: RoleTypography;
  readonly spacing: number;
}
export interface AxisStyle {
  readonly position: "top" | "bottom" | "left" | "right";
  readonly title: CaptionStyle;
  readonly label: RoleTypography & { readonly enabled: boolean; readonly spacing: number };
  readonly line: { readonly enabled: boolean; readonly width: number; readonly color: string };
  readonly grid: {
    readonly enabled: boolean;
    readonly width: number;
    readonly styles: readonly { readonly color: string; readonly width: number; readonly opacity: number; readonly dash: readonly number[] }[];
  };
}
export interface LegendGeometry {
  readonly spacing: number;
  readonly maxHeight: number;
  readonly paddingX: number;
  readonly paddingY: number;
  readonly marker: { readonly shape: string; readonly size: number; readonly padding: number };
}
export interface RetainedMarkerStyle {
  readonly enabled: boolean;
  readonly shape: string;
  readonly size: number;
  readonly fill: string;
  readonly stroke: string;
  readonly strokeWidth: number;
}
export interface ExtendedSeriesStyle extends Omit<CartesianSeriesStyle,
  "color" | "lineWidth" | "markerFill" | "markerStroke" | "markerStrokeWidth"> {
  readonly fillOpacity?: number;
  readonly strokeOpacity?: number;
  readonly lineDash?: readonly number[];
  readonly marker?: RetainedMarkerStyle;
  readonly label: RoleTypography & { readonly enabled: boolean };
}
// Replace overlapping legacy fields in the same style contract. The existing
// mapper validates legacy or canonical input; mixed representations are invalid.
export interface ResolvedCartesianStyle extends Omit<ExistingResolvedCartesianStyle,
  "textColor" | "fontFamily" | "fontSize" | "precision" | "typography" | "line" | "series"> {
  readonly backgroundVisible: boolean;
  readonly padding: { readonly top: number; readonly right: number; readonly bottom: number; readonly left: number };
  readonly typography: { readonly title: RoleTypography; readonly legend: RoleTypography };
  readonly line?: { readonly connectMissingData: boolean };
  readonly titleSpacing: number;
  readonly subtitle: CaptionStyle;
  readonly categoryAxis: AxisStyle;
  readonly numberAxis: AxisStyle;
  readonly legendGeometry: LegendGeometry;
  readonly series: Readonly<Record<string, ExtendedSeriesStyle>>;
  readonly tooltip: { readonly mode: "single" | "shared" | "compact" };
}
export type AppearanceResult =
  | { readonly status: "resolved"; readonly style: ResolvedCartesianStyle }
  | { readonly status: "invalid" | "unresolved"; readonly diagnostics: readonly SnapshotDiagnostic[] };
export type ResolveApplicationAppearance = (input: AppearanceInput) => AppearanceResult;
export interface TooltipInvocation {
  readonly rowId: string;
  readonly hoveredSeriesId: string;
  readonly source: "pointer" | "keyboard";
}
// Modify existing TranslateCartesian with an optional fourth ChartDisplayPolicy
// parameter during migration. Supplying policy requires canonical role style;
// omitting policy permits only the accepted legacy style. Mixed input is invalid.

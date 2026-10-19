# Frozen ordinary area interfaces

Task 2.86 prepares the three area families for separate numerical and editor implementation. Runtime admission still accepts the seven previously integrated families. This contract does not claim that area charts are integrated or release-ready.

## Ownership and typed seam

`echarts/cartesianAreaTypes.ts` defines AreaFamily, isAreaFamily, immutable AreaProjectionInput and AreaProjection. CartesianFamily includes the type union, but isCartesianFamily and isNormalizedFamily retain their prior behavior until the final application join. This prevents incomplete production branches from activating transitively.

The pure projection receives raw snapshot, selected columns in stored order, area family, connectMissingData and optional native legend selection. It returns per-series marker endpoints and processed labelValues, separate stroke spans, paired lower/upper fill spans and finite extent. Every geometry point carries its original rowIndex; repeated indexes inside a span preserve split boundaries at the same category. Marker arrays retain exactly one slot per raw row. The renderer alone converts row indexes to ordinal/numeric/time coordinates.

Internal native geometry uses isolated transparent baseline/delta stacks with explicit Y-first dimensions/encoding. Internal series never become legend members or financial tooltip rows; public series IDs remain selected column IDs. Separate stroke spans preserve original gap breaks while markers/labels remain row-indexed. Miniature cloning preserves invisible internal baselines and computes full-series geometry independently. All area families use the accepted native legend callback because precomputed endpoints need reprojection after membership changes.

## Original semantics

Pinned original Workspace is 38dffc33389aca0e4a87e0e88d42f7067aa220df, AG Grid Enterprise34.1.1 and AG Charts12.1.1. Exact bundle hashes and finite signed fixtures are in `terminalpro/tests/unit/chart-compatibility/fixtures/area-charts.json` in the Workspace fork.

AreaChartProxy sets category X bottom and numeric Y left. Only stackedArea/normalizedArea stack; normalizedArea sets normalizedTo100 and rounded percentage numeric labels. Original Workspace retains its crosshair magnitude formatter. Ordinary independent areas start at zero. Stacked areas accumulate algebraically in selected-series order; [7,-6,5] ends at [7,1,6]. For complete finite rows normalized extent scans raw scalars and cumulative/window extents: max absolute raw segment or prefix. This gives denominator7 for [7,-6,5], but12 for [7,5,-6]. It is not the bar positive/negative mass formula.

AreaSeries.processData sets processed invalid values to0 when (normalizedTo is defined OR connectMissingData) AND stackCount>1, otherwise null. Hidden series process as0. Zero normalization extent returns null scalar cumulative coordinates, while the original Float64Array stack maps those null results to numeric zero. Preserve that typed-stack coercion for fill/stroke boundaries so an all-zero category remains a valley between valid observations. Nonzero-extent invalid stack entries remain missing. Native marker construction separately coerces cumulative coordinates while checking processed label values. Keep those responsibilities distinct from immutable financial observations. Do not infer a standalone zero-only or all-missing axis domain from these source rules.

Original getSeriesSpans uses neighboring stack arrays, ordered cumulative boundaries and split endpoints; fill spans may fall back to earlier stack phantom spans or the axis, while strokes retain only current valid spans. Implement that source algorithm in the cohesive span helper, not a connectNulls approximation. Reference anchors in the retained Community bundle: processData39915-39969, getSeriesDomain39989-40021, createNodeData40060-40156, getSeriesSpans40184-40273, axis fallback40275-40299 and phantom fills40301-40317. Original normalization source29040-29089 and accumulation29201-29265 supply the numerical rules.

Original normalized area with multiple series visibly labels missing Gamma/First and Delta/Second as0 when labels are enabled. The underlying table still displays missing cells. Preserve this original presentation with a separate labelValues array; do not read those substituted label inputs back into financial data or tooltip values. A raw zero remains a zero and can have an endpoint at0 even when normalized processed extents are null.

## Original editor

All three area model identities read/write the area series namespace; family ranges remain distinct. SeriesPanel48937 lists tooltips, Line Width, Line Dash, Line Opacity, Fill Opacity, Markers, Labels and Shadow. There is no Connect Missing Data control. Preserve a saved/custom connectMissingData leaf without adding a UI control or deleting it.

Area module40722-40755 defaults fill opacity0.8, stroke opacity1, stroke width0 unless supplied stroke then2, disabled circle markers size7, disabled labels, disabled shadow offsets3/3 blur5. Final application composition still applies the original theme/generated/saved precedence. Do not substitute raw property-class defaults or line defaults. Preserve the exact single-date fallback only where original caller derives one date; a one-row non-transposed ordinary chart view does not derive dates and does not trigger it.

Original axis-scale refinement, approved by the owner on 2026-10-19: use the existing source-backed 1/2/5 nice-domain rule over projected area bounds and actual plot length. At the matched six-row reference viewport, ordinary area uses [-10, 10], stacked area [-5, 10], and normalized area [-50, 100] with 50-point percentage steps. Raw financial observations and stack projection remain unchanged. This is an area presentation correction; accepted line/bar behavior retains its existing path.

## Evidence and limits

Native ECharts6.0.0 SVG discriminators independently check endpoints, pixel positions, polygon return edges and null breaks for signed/negative deltas, null termination and duplicate X. They demonstrate the representation, not the production span generator. One source-overlaid original Workspace journey rendered all three area families, lower/middle gaps and normalized legend/miniature behavior. Hiding Second recomputed main geometry and visibly left the orange full overview unchanged. One CSV401 was recorded before the fixture transport rendered the data; this is not clean network or deployment evidence.

Original bar-task save/reopen lifetime evidence uses the same model/legend persistence pipeline; the area application join must still exercise its own fresh-session reopen. Effective custom-theme combinations and standalone zero-only/all-missing displayed domains are not observed. These limitations must not become fabricated source facts or skipped implementation checks.

## Verification commands

Use WSL Debian user mc, pinned Node `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`, Python `/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python`. From Workspace terminalpro, run Node with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.area-contract.test.ts`; editor tests use the existing chart-application config. Scoped Biome uses `node_modules/@biomejs/biome/bin/biome lint` with explicit owned paths. The current compatibility compiler reports baseline typographyTS2578; no full compiler success is claimed.

Use the existing QOpenBB complexity command with explicit workspace/data_api manifests, whole-file400/300/50 caps and inventory registration. Original probes reuse existing isolated Playwright fixtures/config; private runtime descriptors and raw diagnostics stay ignored. Implementation task acceptance requires independent review, focused checks and one joined application journey before area UI acceptance.

Source correction, 2026-10-19: the actual six-row Workspace comparison exposed the zero-category distinction. Original `groupStackAccFn` (around line 29270) constructs a Float64Array, and `normaliseFnBuilder` (around line 29063) maps it; scalar cumulative normalization has a different null result. For Third across Delta/Epsilon/Zeta, the fill upper boundary is [100, 0, 100] and lower boundary [37.5, 0, 50]. This repairs the owning pure projection; native rendering does not fabricate missing boundaries.

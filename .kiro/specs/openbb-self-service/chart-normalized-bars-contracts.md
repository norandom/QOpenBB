# Frozen normalized-family interfaces

Task 2.82 supplies the contracts for tasks 2.83-2.85. Production callers remain on their accepted admission checks until the application join. Independent review accepted these findings and the numerical fixture in task 2.82; tasks 2.83 and 2.84 consume this frozen contract.

## Projection ownership

`CartesianMappingContext.legendSelection` is a read-only map from stable numeric column ID to enabled state; omitted IDs mean enabled. Main ECharts series use that same ID as both `id` and `name`, with display labels supplied only by the legend formatter. Miniature series use the existing `openbb-mini-` namespace and are excluded from native main legend membership.

The renderer owns a pure normalization helper and consumes this optional context. Its internal helper signature is private to task 2.83. The application calls the existing `translateCartesian` API with this context, never the helper. For the overview it projects the same immutable snapshot/style with no legend selection, then supplies those full-series options through a new optional final `overviewOptions: EChartsOption` argument to `cartesianNavigator`. Existing callers omit it and keep their current behavior. The renderer lane owns implementation of that optional argument.

`isCartesianFamily` admits the seven scoped families. `isNormalizedFamily` identifies the two percent-stack families. `isHorizontalCartesianFamily` identifies all three horizontal families. The older `isHorizontalBarFamily` retains its existing two-family meaning during the prerequisite so current caller guards do not accidentally activate normalizedBar. The renderer and application join adopt the new predicates in their owned files. No new chart registry or flag is introduced.

## Native legend request

`ChartRenderRequest` carries optional `legendScope`, `projectLegendSelection` and `onError`; `ApplicationSessionReady` inherits that request contract. A normalized application request supplies scope and projection together. Scope is `JSON.stringify([stateAddress, generation, family])` from the existing session stamp; render/data revisions and viewport/theme changes do not create a new scope.

The callback captures the current immutable projected snapshot, resolved style, display policy, theme, action settings and viewport. It returns complete options, including an independently normalized full overview. If translation fails it throws; it never reads or writes Widget state. The host forwards the paired fields and error callback atomically with options/revision. Native selection is the sole transient owner and is not persisted.

The lifecycle retains only keys present in current main legend data; newly present keys are enabled. It reprojects from the newest accepted callback on a legend event and ordinary accepted update, preserves current navigator extent, and applies selected state without redispatching an event. Scope change/disposal clears selection. An interaction error invalidates export before it is forwarded. Initial/mount/update failure semantics otherwise retain the existing contract.

## Verification commands

Use WSL Debian as user `mc`, with Node `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` and Python `/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python`. No dependency install or Dagger build is required.

From `vendor/workspace/terminalpro`, use the pinned Node executable with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs <owned-test-paths>` or the existing chart-application config. Both use bounded workers. Scoped lint uses `node_modules/@biomejs/biome/bin/biome lint <owned-production-paths>` without fixes. Compatibility type checking uses `node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit`; its known typography TS2578 diagnostic is not a passing compiler result.

From QOpenBB, the existing Python complexity module uses explicit workspace/data_api manifests. Whole modified production files must pass 400 physical / 300 logical / 50 per function. Root metadata and inventory remain controller-owned, including preserving unrelated financial-lane edits. The browser owner uses existing isolated headless fixtures and the private runtime descriptor; credentials never enter committed evidence.

## Original numeric presentation

The pinned AG Grid normalized axis supplies `Math.round(value) + "%"`; AG Charts applies that formatter before a plain label format string. Preserve this precedence. Original Workspace separately supplies a numeric crosshair renderer using `formatNumberMagnitude(value, 0)`, which overrides the default axis text. Therefore the crosshair displays the normalized coordinate with that magnitude formatter, without an added percent suffix. Raw series labels and tooltips continue to display original observations.

Source anchors: AG Grid Enterprise 34.1.1 `main.cjs.js:45429-45448`; Community 12.1.1 `AxisLabel.formatValue:17191-17223`; original Workspace `Chart/utils.tsx:298-310`; Enterprise 12.1.1 `getLabelHtml:14321-14329`. Empty extent propagation has no implicit [0,100] domain: Community `BarSeries.getSeriesDomain:41461-41484`, `normalisedExtentWithMetadata:28727-28744`, and `LinearScale.ticks:30250-30252` produce no numeric ticks for an empty domain. This empty-scale source path does not establish zero-only displayed ticks: the actual original zero-only chart has no bars and a single 0% tick at the numeric zero line. Its exact domain is not inferred. The renderer must preserve that visible result without fabricating normalized observations.

A legitimate normalizedColumn save/reload with miniature disabled restores its canvas/data and resets the hidden Second series to enabled. The exact saved range chart model omits native legend selection. The earlier horizontal-miniature reload remains failed evidence, not the basis of this lifetime conclusion.

An all-missing CSV cannot enter the original ordinary chart flow because no numeric series is inferred. Its displayed chart fallback is therefore unobserved; preserve eligibility and source missing/no-finite-node semantics. If an already admitted series later becomes all-missing, do not claim exact original axis parity for that unobserved state. No more reference harness is required for this boundary.

The original normalizedColumn overview visibly renders full vertical stacks; normalizedBar has no working overview. The owner-approved horizontal overview repair applies. Independent hand-calculated signed segments/endpoints and source/package identities are in `terminalpro/tests/unit/chart-compatibility/fixtures/normalized-bars.json`. Source-backed facts, observed effects and the all-missing limitation are separately labeled there.

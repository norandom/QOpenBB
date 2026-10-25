# H2 design review

Architecture and bounded research direction are accepted. The implementation freeze is not ready; do not dispatch H2 renderer/control workers yet. No owner approval of incomplete types is needed.

Reviewed `h2-design.md` at SHA256 `06ca086e085b1450ead98dfbba357e608f242bdfe575c3cbe4cba2185acd8181`, its renderer/control source reports, accepted H1c outputs and existing appearance/result type owners. This was read-only review: no dependency installation, tests, browser, builds or production edits.

Final readiness-only amendment re-read and rehashed: `572db1d1ec5f8cc58d6f62c7ee98bbbeefcee96ebbfc72b843144f5a597591b5`. Its opening now explicitly records the four items below and withholds implementation freeze/fan-out. The review disposition is unchanged.

Four readiness items remain:

1. Complete the two already scoped original legend observations: equal finite Color, including a value outside [0,1], and selected all-missing Color. Freeze finite legend display separately from paint fallback; no invented measured range or nonfinite ECharts input. Reuse the existing harness without repeating H0.
2. Declare exact editor state, selected-context and intent types with one shared owner. `projectHierarchyEditorState` and `mapHierarchyEditorIntent` currently name undefined public shapes. Freeze applicability, finite field validation and original-path mapping before controls/H3 consume them. Retain the existing composition/layering precedence documented in the controls research.
3. Resolve saved appearance admission before narrowing shared types. The draft admits only never/on-space wrapping and solid paint, while retained source supports additional wrapping policies and advanced fills. Inspect the actual source-valid saved/generated hierarchy inputs and explicitly cover required ones. Retaining an unknown value in storage while rejecting its previously usable rendering is not saved-configuration parity. Do not silently remove functionality or claim unsupported policies work; this is a bounded inventory/contract decision, not permission for a new general styling engine.
4. Assign an implementable gradient hover-indicator/event boundary. The draft acknowledges the original effect but leaves any host callback undecided. Freeze its renderer/H3 ownership and lifecycle behavior before claiming complete gradient behavior; do not silently omit it. A narrow separately reviewed callback is preferable to unplanned edits in the near-cap shared lifecycle.

Native ECharts hierarchy layout remains the right bounded approach. Stable Treemap ordering, original palette identity before zero-weight exclusion, raw tooltip metadata, separate observed/paint domains and H1c-only numerical preparation are coherent. Documented Treemap partition/title-fit and Sunburst inset/label differences require candidate comparison, not a pixel-parity claim or premature custom layout engine.

The Culori-backed conversion plus narrow original interpolation wrapper is a reasonable dependency strategy. Exact package/type release, integrity, protected install command and independent reference samples remain H2.0 gates. Undefined conversions must fail explicitly; no fallback-black, permissive declaration or CDN workaround. A sampled native graphic gradient avoids native visualMap changing explicit per-node colors. Existing host, storage and transaction ownership remain intact.

The proposed disjoint renderer/control modules and whole-file 400/300/50 checks are credible. Two focused numerical/mapping suites and one compact H4 control/FMP lifecycle journey are proportional. No broader test framework or extra user permission flow is warranted. Re-review the completed readiness decisions and exact shared types before materialization/fan-out; this review accepts research direction only, not implementation or rendered acceptance.

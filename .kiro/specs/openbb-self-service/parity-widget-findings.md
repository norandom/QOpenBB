# Original and candidate widget comparison

The current candidate fails the original OpenBB control contract. It displays the synthetic financial rows, but removes the chart toggle and the Advanced, Stats and Formulas settings. This is observed browser behavior, not just a source-code difference. No feature reduction is accepted.

## Comparison scope

The reference is the previously built Full image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, labeled with Workspace source `38dffc33389aca0e4a87e0e88d42f7067aa220df`. The candidate frontend was freshly built from archived commit `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86`, using matching accepted package/lock bytes and the same archived public Full configuration. Build exit was 0; all 464 emitted files were hashed and the copied output matched.

The paired candidate runtime combines that frontend with the original backend image. It is a test fixture, not a built candidate release image. Runtime configuration is written into a disposable asset copy; frozen build output remains unchanged. Release labels differ deliberately to identify the two runs.

At this candidate revision, the isolated Perspective runtime is not integrated into these financial widgets. The comparison establishes gaps in the current implementation; it does not prove that Perspective or another compatible adapter could never reproduce the original behavior.

Both runs use the same synthetic widget definition and rows, default dark initialization, 1440 by 1000 viewport, isolated accounts and localhost containers. Browser routing provides synthetic data and overlays the owned dashboard response while clearing shared/entity-shared entries. Other validation fields are retained. All off-origin requests are blocked. Real provider data and owner state are absent.

## Observed results

| Contract | Original | Candidate |
| --- | --- | --- |
| Two financial rows | Periods 2024-Q1/Q2, revenue 100/120, EPS 1.20/1.40 displayed | Same displayed values |
| Original chart toggle | Present; clicking renders a visible grouped-column chart with period labels and Revenue/EPS legend | Missing: expected one `chart-view-button`, observed zero |
| Settings dialog | Opens with Advanced, Pagination, Stats, Formulas, precision and column controls | Opens, but Advanced, Stats and Formulas are absent; Pagination remains |
| Settings Save and real save/reopen | Unverified | Unverified |
| Full light/dark interaction parity | Unverified | Unverified |

Automated value checks test body-wide text presence; screenshots corroborate row placement. They are not row-scoped cell assertions or financial calculation tests. The original light-theme experiment changed storage/HTML state directly, so it does not prove the real theme control or full chart-theme state. The paired comparison uses default dark only.

Both runs retain a script parse error at `/assets/js/datafeeds/udf/dist/bundle.js`, where HTML is returned instead of JavaScript. The candidate also records an onboarding developer-info 404. No clean-console claim is made.

## Separate persistence blocker

Real dashboard creation was acknowledged, but readback failed. The UI fixture does not establish backend persistence. The implementer reported SQLite `no such function: concat` in the dashboard name projection; initial raw exception output was not retained as a standalone log and its provenance is qualified in the local report.

Independent source tracing found the expression in six `backend-api/backend/api/crud.py` projections for dashboards and user apps. A controller-run, network-disabled container probe using the image's SQLAlchemy 2.0.52 independently reproduced SQLite's rejection of `concat`. A proposed string-concatenation expression passed six isolated SQLite name/null/empty/whitespace cases and compiled with `||` for SQLite and PostgreSQL. Actual CRUD/API recovery and PostgreSQL execution were not tested, and no production repair was made.

The proposed repair preserves the surrounding null-checking CASE and existing trimming. `crud.py` measures 1,599 physical lines and 582 logical units, with functions within the 50-unit limit. Any change needs the project's reviewed narrow size exception or a cohesive extraction; the discovery probe does not waive that gate.

## Evidence and remaining work

Local ignored evidence is in `artifacts/parity/original-widget/`, `candidate-build/`, `candidate-widget/` and `sqlite-projection/`. Authentication storage and container state are private disposable artifacts and must not be published. Owned browsers and probe containers were cleaned up; the controller independently checked that the widget containers were absent.

The original observations and candidate negative findings passed independent Astra review with explicit limitations. The reviewer reran the separate gate over frozen DOM observations: exit 1, with four failures for the missing toggle and three settings. All 13 candidate and 24 original manifest entries matched. All 464 runtime asset entries matched their manifest; only generated `config.js` differed from the frozen build. The collector's exit 0 means evidence collection completed, not parity passed.

Restore the original control/action behavior before any positive parity claim. Preserve these cases as row-scoped, maintained Playwright regressions during the implementation phase; the current artifact-only discovery drivers and recorded-observation gate are not a maintained application test suite. No production, persistence or release acceptance follows from this review.

See the [capability matrix](../../../docs/renderer-capability-matrix.md), [discovery plan](parity-plan.md) and [verification contract](parity-verification.md).

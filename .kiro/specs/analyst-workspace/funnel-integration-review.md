# F3 independent design review

Approve the bounded stock/plain-color preparation and subsequent atomic ordinary-Table integration design. This is source-only design acceptance, not implementation or browser acceptance.

## Review Verdict
- VERDICT: APPROVED
- TASK: F3 bounded ordinary-Table integration proposal
- SOURCE: artifacts/chart-funnel/f3-proposal.md, SHA256 691282732bf53a3614dc4932eaaf8d319e651e76b99ebb15a337c8e15cc39e9b; accepted Workspace a3e1a861f47057f52faf7120b27375419efbfb16.
- MECHANICAL_RESULTS:
  - Tests/build: N/A, design-only review; no production edits or execution claims.
  - Static checks: source inspection against actual session/input/selection/setup/capture/theme/editor/host code and frozen F1/F2 contracts.
  - Boundary: WITHIN. One inactive pure theme helper followed by parent-owned atomic routing; existing capture, aggregation, option reducer and lifecycle remain authoritative.
  - Boundary audit: CLEAN after two concrete corrections below.
  - RED phase: N/A; implementation tasks retain RED/focused verification requirements.
- FINDINGS:
  1. Resolved Important: paint rejection now has an explicit ValidationResult<FunnelThemePaint> contract. Caller validates before generic theme projections and uses a narrow nonthrowing failure envelope retaining chartType. AgChartView forwards that identity to the existing pending surface. Reachable advanced objects receive explicit diagnostics without coercion, fallback colors or payload mutation. Unsupported appearance may disable Set Up/Customize; this does not weaken the separate ready-state requirement for invalid financial data. Existing gallery/table and external theme-administration recovery paths are identified honestly.
  2. Resolved Important: actual gridCapture currently skips undefined only under box/statistical policies. The amended proposal owns the bounded addition of funnel-observations to that branch, preserving absent keys, null and zero through the existing capture owner. Required capture/recapture regressions now exercise an absent middle value before setup/F1 rather than relying solely on handcrafted snapshots.
  3. Recoverable data admission is sound: selection resolves setup/appearance independently of F1 status, ready retains editor/stamp/model/snapshot for expected invalid/empty data, and one extracted chrome builder clears financial geometry. Existing lifecycle uses hideTip and notMerge:true, supporting stale-series/tooltip removal without another host owner. Appearance edits and selecting a correcting first field remain possible.
  4. Dedicated snapshot policy permits empty numeric selection and avoids imposing a numerical-axis unit constraint on unused retained fields. Full ordered selection reaches accepted F1; no transient first-field slice, second aggregation or source normalization is introduced. Existing sessionSetup already masks unsupported switch behavior without requiring saved-model rewriting.
  5. Direction remains a native series option, moves to common Setup composition and does not transpose capture or selection. Runtime appearance fingerprint and both clone sites, transaction dispatch, setup selection, ready/intent unions, caller admission and zero-series exemption are explicitly owned in the atomic join. Existing F2 envelope and family capability rejection remain intact.
  6. Actual theme helper inputs accept unknown persisted objects; TypeScript string arrays are not treated as runtime validation. Stock Cone values are linked to retained source-derived fixtures. The owner-deferred advanced-theme boundary remains explicit and separately tracked; no commercial evaluator dependency is permitted.
  7. Whole-file caps and inventory foundation are retained: 400 physical, 300 logical, 50 per function, with cohesive extraction if shared runtime/view growth exceeds them. Physical inventory is correctly described as planning evidence, not a checker pass. F3 focused source gates and F4 identified-image/browser gates remain distinct.
- REMEDIATION: None remaining for design approval. Implement the specified regressions and collect independent source verification before accepting F3.
- SUMMARY: The amended proposal closes the missing capture and theme-failure boundaries while preserving financial recovery and atomic activation.

Reviewed actual files included applicationSessionTypes, applicationChartSessionTypes, applicationSessionRuntime, applicationSessionSelection, applicationSetupSelection, applicationSessionSetup, setupProjection, histogramCapture, gridCapture, snapshot, heatmapSession, funnelAppearance, appearanceComposition, useCallerSessionInputs, themeInputs, themes.tsx, useCallerDock, AgChartView, ApplicationChartEditor, comboEditorMode, ChartSetupPanel and lifecycle. Reused the previously read Kiro review/completion and applicable steering instructions. Core product/tech/structure steering files remain absent. No frozen reports or other lanes were changed.
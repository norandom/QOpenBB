# Deliver Background and Tooltips controls

Tasks 2.54, 2.55 and 2.56 implement the original Background and Tooltips controls and compose them in the accepted dock preview. Background is committed at f7e2d00, Tooltips at 531848b, and the combined story at 86da20c. Independent task reviews approve each boundary.

## Verification Result
- STATUS: VERIFIED
- CLAIM_TYPE: TASK
- CLAIM: Controlled Background and Tooltips edits preserve values and use the original Chart Style and Series grouping in both themes.
- EVIDENCE: Seven focused panel tests pass, with independent reruns and scoped lint. Isolated Playwright/CDP checks pass with no runtime/network diagnostics, including combined dock and tab retention. Final complexity checks 191 maintained files with no errors or violations. Existing exception source files are unchanged from f34de0a.
- GAPS: Scoped TypeScript reproduces unchanged DS typography.ts TS2578. Remaining Series/axis controls, renderer bindings, storage integration and deployment remain pending. Owner visual approval of these new views is not inferred.

workspace-changes.json, data_api-changes.json and complexity-final.json retain the final scope and measurements. Publication uses explicit reviewed allowlists. Mirror identities and staged bytes are checked with artifacts/appearance-editor-join/hashes.cjs and delivery-audit.py before delivery. Unrelated financial-lane edits are excluded.

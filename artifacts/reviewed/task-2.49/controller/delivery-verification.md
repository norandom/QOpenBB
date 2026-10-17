# Deliver the controlled chart panels

Tasks 2.49 and 2.50 are verified within their approved component boundaries. Set Up is committed at 3bc131666f28fa2cda951c86a921412093d44a1d; Titles and the composed dock preview at 495a08f04c84353ed27adbb556e430928e9b4d36. Independent reviews approved both, and the real light/dark preview preserves controlled edits through navigation. Owner visual judgment remains pending.

## Verification Result
- STATUS: VERIFIED
- CLAIM_TYPE: TASK
- CLAIM: Controlled Set Up and all four Titles sections are implemented and composed in the accepted dock preview.
- EVIDENCE: Six Set Up tests, one independent drag regression and four Titles tests pass. Scoped lint and isolated Playwright/CDP checks pass. Final inventory-aware complexity checks 184 maintained files with zero errors or violations; source manifests and complexity-final.json record the scope. Existing exception files have no diff from a83f711 to 495a08f. Public mirror hashes and staged bytes pass delivery checks.
- GAPS: Known upstream DS typography.ts TS2578 prevents a clean scoped compiler result. Other Customize sections, chart rendering bindings, persistence integration and deployment remain pending. The preview is not the complete application.

The final complexity command uses Debian WSL, the existing pinned Node 24.22.0 and Python environment:

```sh
PATH="$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:$PATH" /home/mc/qopenbb-work/sqlite-runtime/venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/task-2.49/controller/workspace-changes.json --changes data_api=artifacts/task-2.49/controller/data_api-changes.json --output artifacts/task-2.49/controller/complexity-final.json
```

Delivery checks: `node artifacts/appearance-editor-join/hashes.cjs` and `py artifacts/appearance-editor-join/delivery-audit.py`. The initial staged breadth file mixed CRLF and LF; normalizing that metadata file to LF resolved the whitespace gate. Source and reviewed evidence bytes were unchanged. Unrelated financial-lane work remains outside these commits.

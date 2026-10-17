# Original editor evidence is approved within the captured fixture

VERDICT: APPROVED. Independent review dated 2026-10-17 accepts the seven original UI edits, exact tooltip mapping/content, complete finite transpose/restoration and six settled Sum raster bars. It accepts the 57-file publication set by the hashes below. This is research acceptance only: no full lane C, candidate parity, implementation, persistence, application, renderer or release acceptance follows.

The review used kiro-review adapted to frozen research. RED evidence and production suites are not applicable to this discovery review; no production suite, browser or application runtime was started. Research artifacts are outside production complexity caps. Future production work remains subject to the inventory/checker and 400 physical lines/file, 300 logical units/file and 50/function caps.

## Frozen inputs

- Canonical spec: `.kiro/specs/openbb-self-service/chart-editor-contract-close.md`, SHA-256 `7e982b54f722be5aad5e0fc84f37caf6c4be71f36d3ef0ff38efcde060b87d15`. This binds the controller's final link-only change to the reviewed public mirror.
- Evidence report: `artifacts/parity/editor-contract-close/report.md`, SHA-256 `5067c2bb581815800e2a8802fb65c66401e8a14c5beefa998dbcc3752d62f727`.
- Source publication allowlist: `artifacts/parity/editor-contract-close/publication-allowlist.json`, SHA-256 `6f3f829bea21b97d458d34b809a1ebfd953bb9185a4e28bddaeb70fe3cc87943`.
- Original image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; source label `38dffc33389aca0e4a87e0e88d42f7067aa220df`.
- Candidate reference `76edf85a46298f7bc5212ff9944e4b66e9baa4af` was not exercised.

All original evidence inputs remained unchanged. [Hash audit](allowlist-hash-audit.json) enumerates every approved evidence path, byte count and SHA-256. The allowlist itself must accompany those 57 entries when mirrored. [Review audit](audit-results.json) independently checks the claims and binds the final canonical spec hash.

## Mechanical results

Commands ran from `D:/Source/QOpenBB`. Before execution, every allowlisted input was hash/size checked and copied into the review-owned `artifacts/parity/editor-contract-review/scratch/` directory. The supplied verifiers write only their copied outputs there.

| Exact command | Result |
| --- | --- |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-review/scratch/verify.mjs` | Exit 0; 30 assertions pass. |
| `py artifacts/parity/editor-contract-review/scratch/verify_pixels.py` | Exit 0; six actual raster bars satisfy value scaling and common baseline within two pixels. |
| `py artifacts/parity/editor-contract-review/audit.py` | Final exit 0; all 57 hashes/sizes unchanged, exact tooltip UI/event/model/effective checks pass, full numerical transpose and restoration pass, independent Sum recomputation passes, cleanup and derivative-source hashes pass. |
| `wsl -d Debian -u mc -- docker image inspect --format '{{.Id}} {{index .Config.Labels "org.qopenbb.source.workspace"}}' sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` | Exit 0; image ID and source label equal the frozen claims. Read-only inspection. |
| `rg -n -i 'password\|authorization\|bearer\|token\|cookie\|secret\|session\|email\|account\|TBD\|TODO\|FIXME\|HACK\|XXX' artifacts/parity/editor-contract-review/scratch --glob '!*.png'` | Credential-related matches inspected: generated-password code, synthetic example address, file references and scope prose only. No embedded credentials, auth/session values or private account data found. |

The scan above records the search alternatives using escaped pipes for Markdown table rendering; the executed regex used ordinary `|` alternation. No new placeholder markers were found. Static review was scoped to the evidence collector, verifiers, startup/cleanup and publication scripts. No production files were changed.

The first independent audit invocation exited 1 because the reviewer assumed Sum categories were strings. Inspection showed the documented `{id,value}` wrapper. The reviewer corrected only the owned audit to compare `period.value`; the frozen inputs did not change. The subsequent audit and final hash-binding run both exited 0. This was a reviewer schema assumption, not a runtime retry.

[Fresh assertion output](fresh-verification.json) and [fresh pixel output](fresh-pixel-verification.json) equal the frozen result JSON semantically. Runtime identity is preserved in a [finite safe projection](runtime-identity.json).

## Findings and scope

1. Tooltip evidence agrees across the visible control, new `chartOptionsChanged` event, exact `chartOptions.bar.tooltip.mode` patch, root effective tooltip mode and hover DOM/screenshot. Single maps to `single` and displays `2024-Q1 Revenue (USD millions) 100`. Multiple maps to `shared` and adds `Operating Income (USD millions) 20`. Compact maps to `compact` and displays Revenue 100 without the Q1 heading. Series tooltip is not substituted for the chart-level family patch.
2. Complete finite transpose is supported: category wrapper IDs 0/1 label Revenue/Operating Income in USD millions; `period:0..3` preserve `[100,120,140,160]` and `[20,25,30,40]`. The four series retain both Q1 identities. Turning either Sum or transpose off restores every original row, category ID/order, binding and unit-bearing series name.
3. Independent grouping recomputes Q1 220/45, Q3 140/30 and Q4 160/40. The screenshot visibly shows Sum selected and a 0..250 axis. Six connected raster components have heights 221/141/161 and 45/30/40 pixels at a common y=356 baseline, agreeing with the 251-pixel plotting scale within the declared tolerance. Collector ordering places an explicit 1.5-second wait and `waitForUpdate` before capture. This supports the settled fixture; geometry projections alone are not the acceptance basis.
4. Missing-value semantics remain UNVERIFIED. All eight financial observations are finite and present. This fixture establishes no null, undefined, absent, non-finite, zero or negative-value behavior. The accepted result must not be generalized to those cases or mixed financial units.
5. Publication safety passes for the 57 named files. All 12 allowlisted PNGs were visually inspected: synthetic financial chart/editor only, with no login fields, credentials or private account data. Text/JSON fields and script matches were inspected. The preserved first-attempt stack trace contains the finite category-wrapper error and source path, not authentication/request data. Attempt 1 exit 1 and cleanup are retained; the corrective run has seven actions, no failures and exit 0. Both cleanup reports pass; credential and owned state paths are absent.
6. Raw runtime/account identifiers, credentials, state, request metadata, unfiltered diagnostics and raw failure screenshots are excluded from publication. Safe diagnostic and outgoing-storage derivatives have verified source hashes. Original datafeed errors and onboarding 404 remain acknowledged. The single outgoing compact-tooltip POST is not backend readback, reopen or restart evidence.

REMEDIATION: None for this bounded research/publication acceptance. Missing-value cases, additional aggregate functions, remaining controls/families/themes, candidate rendering and persistence remain future evidence obligations. The existing full parity requirements remain unchanged.

Review outputs are frozen after the final audit. Only `artifacts/parity/editor-contract-review/**` was written by this reviewer; unrelated edits were preserved.

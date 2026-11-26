# Commodities versus Technology packaged acceptance

The Ubuntu Workspace candidate opened the catalog story, evaluated real ETF history and restored the saved dashboard after a controlled price revision. The [selection results](story-selection.json) and [persistence results](story-persistence.json) contain the saved-run identifiers and verification measurements. The [breadth map](../../../.kiro/breadth.toml) maps each of the 16 criteria to its test and outcome.

## What the analyst saw

Across the 64 NYSE Arca sessions from August 17 through November 13, 2026, DBC's split-adjusted price return exceeded XLK's by **11.28225 percentage points**. Dividends are excluded. GLD trailed XLK by 1.81099 points and VGT by 3.07018 points. Each comparison matched the exact saved closes and 63 adjacent daily simple returns per leg. The two DFII10 endpoints lacked eligible availability evidence at the cutoff. Workspace identified the dates, withheld the real-yield context and retained the price verdict. Eligible DFII10 charts were verified with controlled inputs. Live chart evidence covers the withheld case.

The January 13 window held only eight scheduled sessions. The story withheld the spread, kept keyboard focus and recovered when the analyst returned to November 13. The catalog card opened by click. Inside the story, Chromium exercised proxy and date selection, inspected evidence and reached the conclusion by keyboard across the light and dark themes.

- [DBC and XLK split-adjusted closes](story-fmp-price-light.png) shows USD per share from August 17 through November 13. The source was FMP history retrieved on November 26, 2026.
- [GLD and VGT daily simple returns](story-fmp-risk-dark.png) shows percent price changes from August 18 through November 13. The values were derived from the GLD/VGT run's saved FMP closes.

## Outage, revision and fresh login

Stopping modeling caused two HTTP 503 responses. The App kept the selection and showed the failure inline. Restoring the service and retrying on the same dashboard recovered the verified spread.

A disposable data API fixture next supplied an ending DBC close of $31.79 in place of $30.79. A second analyst acquired that history through the normal model service. The changed spread was 14.55450 percentage points. A fresh login to the first analyst's dashboard recovered the original 11.28225-point spread, original checks and receipts, and both saved chart configurations. The browser issued zero evaluations and zero direct history requests on reopen. Export before and after reopening matched the full configuration allowlist. A foreign comparison and a deleted macro reference each returned HTTP 404 and an inline unavailable state.

## Reproduce the candidate

The Dagger Workspace build used owned fork revision `eeb11a299978d2de74ade8734fbd18fcb52e469b`. All 29 changed production inputs matched their Git blobs in the stage. The verification harness is recorded in controller commit `4dff622`. Run each suite serially with one worker, the private provider environment and a fresh disposable Compose project. [Packaged runner](../../../verification/modeling-journey/README.md)

```bash
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
mkdir -p artifacts/modeling-journey
for suite in story story-selection story-persistence; do
  pipeline/.venv/bin/python verification/modeling-journey/packaged.py \
    --suite "$suite" --local-images --evidence artifacts/modeling-journey \
    --workspace-image sha256:26e224b495b533fa3b8a3404e31b9676a20281ea8ff4ebbde5a4ea9a3e625ea4 \
    --data-image sha256:1cbb333c1ff5befbafc207786adf04da5adeac13c2f519b3e484d450424cfad6 \
    --modeling-image sha256:090e6646cb2d3d37ac86f2ef10aa61762daa7e78baae2c0b024f1a8db35a7323 || exit 1
done
```

The seven focused Workspace suites passed 49 tests, including saved-state, export-menu, delayed-response and financial evidence cases. The canonical combined complexity gate measured 928 maintained files. The Git-verified Workspace change from `aa1a625` through `eeb11a2`, joined with the controller and unchanged data fork, measured 248 files. Both checks found zero violations. The hosted portable suite passed 1,910 tests, skipped 13 and deselected one. Independent review accepted the joined candidate and rollback record. [CI at the verification revision](https://github.com/norandom/QOpenBB/actions/runs/45873686391)

## Rollback image set

The candidate images above were loaded locally. The prior published deployment remains [modeling-v0.1.0](https://github.com/norandom/QOpenBB/releases/tag/modeling-v0.1.0) at controller revision `5407b3f335d9de413f3d988b7a11fbc2a77e7f62`. Use its deployment bundle and compatible saved-state backup for a rollback. [Published-image verification](../factor-signals/workspace-modeling-release.md)

| Service | Previously published immutable reference |
| --- | --- |
| Workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:49748d9f90d064073187feb8bc1208e1a84d5b08c4b89ad80cea80d24e9f4b01` |
| Data API | `ghcr.io/norandom/qopenbb-data-api@sha256:79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73` |
| Modeling | `ghcr.io/norandom/qopenbb-modeling@sha256:0c19913678b029794eac117a4a58512c826f4779c5e6d77dbdd7a5d5ffa80e43` |

Task group 4 exercised the candidate on disposable Ubuntu state. Registry publication, rollback execution and owner-server deployment are outside this acceptance.

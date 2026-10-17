# Original nested editor probe

The bounded capture did not close any new nested editor contract. It reached the original chart editor with a duplicate-category synthetic fixture, then failed before its first serialized snapshot or any nested edit. See the [contract ledger](../../../.kiro/specs/openbb-self-service/chart-editor-runtime-contract.md).

## Reproduction and attempts

Run `wsl -d Debian -- bash /mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-completion/run.sh` for the preserved launch command. It checks the original source/image identity and starts an isolated loopback service with fresh disposable credentials/state. `run.sh` is a historical failed probe, not a passing acceptance command; cleanup is the separately retained `cleanup.mjs`. Do not rerun without updating its exact owned state cleanup path. No environment file, old credential, operator browser or operator application was read.

The first run failed with `TypeError: Converting circular structure to JSON`, `context.beans`, in the initial `json` snapshot call. Pass 1 removed full getOptions output; pass 2 narrowed series tooltip/label/marker/shadow and legend/axis processed objects. All three stopped at the same initial snapshot before actions. `first-pass/` and `second-pass/` preserve the earlier failures, and the top-level files preserve the final pass. The command status records final exit 1 separately from the wrapper. The 2-remediation bound ended the browser work.

`failure.png` and `table-dark.png` are post-login synthetic screenshots. `failure-ui.txt` records the visible original Chart, Set Up and Customize tabs, family groups, and unaggregated duplicate categories. No event/model ledger exists beyond the explicit unresolved zero-action summary. Planned actions in `journey.mjs` are not executed evidence. Its raw model/options collector needs a stricter finite projection before reuse.

## Diagnostics and cleanup

CDP Runtime and Network domains were enabled on an isolated headless browser. `diagnostics.json` retains `Unexpected token '<'` and original `/assets/js/datafeeds/udf/dist/bundle.js` responses with HTTP 200 and `text/html`. This is not a clean original browser run.

Cleanup exited 0, removed the owned container and the exact bounded disposable state/account paths, and confirmed no owned private path remained. `cleanup-report.json` records the result. All JavaScript/shell probe scripts were checked for CR bytes before execution. They use the existing Debian WSL Node 24.22.0 and Playwright cache; no installs or builds occurred.

No source implementation, phase approval, renderer acceptance or full parity is claimed. Core steering `product.md`, `tech.md` and `structure.md` were absent; applicable testing, delegation, documentation, complexity, CI and Workspace-experience guidance was read.

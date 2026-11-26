# Saved comparison evidence and dashboard state

For the November 13, 2026 observation date, the Workspace decoder reproduced each saved comparison from the packaged preflight. The spread is the commodity proxy's 63-session return less the technology proxy's return, in percentage points. The decoder uses the full saved decimal to determine the sign. The table rounds results for display.

| Commodity | Technology | Spread (pp) | Outcome |
| --- | --- | ---: | --- |
| DBC | XLK | +11.28225 | Commodity outperformed |
| GLD | XLK | −1.81099 | Technology outperformed |
| DBC | VGT | +10.02306 | Commodity outperformed |

Each volatility output exposed 63 daily returns. The separate DFII10 run withheld the November 13 macro assessment. All three comparisons retained their verdicts. See the [packaged preflight](packaged-preflight.json) for the observation window, provider receipts and image identities.

## Reproduce the contract checks

From the controller checkout, run the following command with Node 24.22.1 on the path to generate owner-scoped synthetic run fixtures. Use a fresh temporary directory for each invocation.

```bash
work=$(mktemp -d)
PYTHONPATH=services/data-api pipeline/.venv/bin/python -m pytest \
  -q -c pipeline/pyproject.toml tests/contracts/test_research_story.py \
  --basetemp="$work"
export QOPENBB_STORY_WIRE_FIXTURE="$work/test_synthetic_research_story_0/wire.json"
```

From the matching Workspace revision's `terminalpro` directory, run the decoder and state suites against those fixtures.

```bash
node_modules/.bin/vitest run --maxWorkers=1 \
  src/lib/modeling/storyContract.test.ts src/lib/modeling/storyEvidence.test.ts \
  src/lib/modeling/storyState.test.ts
```

## Verification scope

The [reviewed Workspace candidate](https://github.com/norandom/openbb-workspace/commit/4cc53d7f41725ac2563a5f086151472577a3977b) is on `qopenbb/research-stories`, based on the controller's pinned `aa1a625`. Promotion to the delivery pin is task 4.1. The dashboard renderer and authenticated browser reopen have separate acceptance tasks.

Both controller contract tests passed. The joined Workspace run passed 59 tests across the three suites above, template export and Company Documents integration. Independent review reproduced two defects and verified their fixes:

- A duplicated saved check could mask a missing spread check. Each cited check now resolves exactly once. The malformed spread yields insufficient data while the independently verified leg returns remain visible.
- A template could carry provider rows, response text or credentials beside its story state in a grid entry. Import, save and export now project story configuration and geometry. Regression tests retain the selected series, run references, geometry and minimized state and exercise legacy widgets.

The combined complexity check measured 223 controller and fork files, including eight changed Workspace production files. The largest Workspace file had 397 physical lines. The largest logical file count was 195 and the largest function count was 34. The candidate check used the committed fork range and disabled all Workspace exceptions in a temporary inventory copy because existing exceptions bind to the delivery pin. It found zero violations.

The decoder passed focused strict and non-strict TypeScript checks. The full Workspace typecheck remains open. The installed compiler rejects the checkout's deprecation setting and lacks a built project reference. A separate diagnostic pass also reports existing application errors, including the Sankey chart type in template export.

## Selection, retry and reopen

The [task 3.3 controller](https://github.com/norandom/openbb-workspace/commit/a34dfc6f7f7c9442c6fc6e4d93b72751bc95256e) freezes the selected proxies, observation date, evaluation time and exchange schedule. Changing the selection clears the displayed evidence immediately. The controller waits for an outstanding write before submitting another model and discards obsolete responses, including when the analyst returns to the original pair.

The packaged bridge check used the controller from Node against the [three identified images](packaged-preflight.json) on loopback with an authenticated analyst. The DBC/XLK run returned a spread of +11.28225 percentage points for November 13, 2026. DFII10 was withheld for that date. The table distinguishes the real model calls from the controlled response and saved-reference changes.

| Scenario | Requests observed | Result |
| --- | --- | --- |
| Replace a successful comparison response with a publication error carrying its real run ID | POST, GET, POST | Recovered the persisted comparison by ID, then evaluated the regime. |
| Reopen the two saved references in a new controller | GET, GET | Restored the same references, spread and dated macro result. |
| Substitute the regime ID for the comparison ID | GET, GET | Reported the comparison mismatch and restored the valid regime. |
| Remove the regime reference, reopen and explicitly retry the regime | GET on reopen, POST on retry | Kept the original comparison reference and restored the macro result at the saved cutoff. |

The transport observed at most one active request. The controller suite also exercised delayed success and failure after A → B → A, an uncertain write with no recovery ID, failed-leg replacement, capacity errors and daylight-saving time. Independent review reproduced the missing-reference retry failure before its fix and passed all 14 controller cases afterward. The joined Workspace run passed 49 tests across six suites. Both controller-repository contract tests passed. Strict and non-strict TypeScript checks passed for the controller dependency graph.

To rerun the focused suite, generate the synthetic wire fixture as described above, set `QOPENBB_STORY_WIRE_FIXTURE`, then run `node_modules/.bin/vitest run --maxWorkers=1 src/lib/modeling/storyController.test.ts` from `terminalpro`. The combined complexity gate passed on 227 files using the candidate procedure above. Native widget mounting and keyboard interaction belong to task 3.4.

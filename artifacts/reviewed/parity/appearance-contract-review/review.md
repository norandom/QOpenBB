# Derived-token research is approved after rounding correction

- VERDICT: APPROVED for bounded research evidence and narrow helper design input only.
- TASK: Appearance contract close, independent research review, 2026-10-17.
- Production acceptance, full B2, application activation, UI reachability, persistence and release: NOT ACCEPTED by this review.
- Corrected publication allowlist SHA-256: `60677a94108fe5986ef0d926164670433ea140e705488c9dd9074d05a00f4cbb`.
- Candidate revision: `76edf85a46298f7bc5212ff9944e4b66e9baa4af`.
- Original source: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.
- Reference image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`.

The sole blocker in [the initial rejection](review-initial.md) is resolved. The report and spec now require normalized-channel interpolation followed by clamp, scaling and JavaScript Math.round. The added source utility experiment reproduces the counterexample that invalidates direct byte-domain blending. Narrow design may use explicit resolved opaque-six-digit-hex foreground/background and text/chart-background tokens. No general parameter resolver or production implementation is approved.

## Fresh mechanical evidence

Checks ran offline in review-owned copies; frozen inputs were not overwritten. No browser, install, build, heavy suite, private credential file or owner environment file was used. Production RED and suite requirements are N/A to this research scope.

| Exact command | Result |
| --- | --- |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/corrected/offline/normalized-colors.mjs` | Exit 0; 262,144 channel comparisons, zero normalized mismatches, named #000000/#9b0000 edge produces #8b0000. |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/corrected/offline/assert.py` | Exit 0; 44/44 assertions pass. Generated assertions are byte-identical to frozen assertions. |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/corrected/check.py` | Exit 0; 40/40 checks pass, including 28 publication hashes/sizes and six original/dependency hashes. Output is retained in corrected/check-output.txt. |
| `Get-FileHash` for both normalized-color-evidence.json files | Both SHA-256 `74b1ad224b3fa6008da5050b29ce15920e4e2e752f32aa1bd5b714668e36c45f`. |
| `rg -n 'TBD\|TODO\|FIXME\|HACK\|XXX'` over corrected report/spec/assertion/source-comparison script | No matches; exit 1 is the expected no-match status. |

The original eight runtime cases remain byte-identical, SHA-256 `f429407124be0952217520754aa5c4ea0b682dc4fe16d0a072c94cace999877a`. The added five assertions are source-edge/equivalence checks, not five additional runtime cases. Independent installed-library comparison from the initial review remains preserved in math-check.cjs/json. Its intentional exit 1 documents rejection of the byte shortcut, not failure of the corrected normalized contract.

## Publication and source findings

The [corrected 28-file allowlist](corrected/reviewed-input-allowlist.json) records exact source paths and hashes; [fresh checks](corrected/checks.json) verify actual bytes. This is the approved safe publication set. All eight PNGs were visually inspected during the initial review; unchanged hashes preserve that review. They show synthetic financial data and the original UI, with no exposed credentials. Finite projections and scripts contain no concrete secret values. Raw cases/diagnostics, runtime metadata, account state, credential files and dependency caches remain excluded.

Installed package version/license and six source hashes remain verified. MIT AG Charts Community 12.1.1 supplies the color arithmetic; original package.json pins 12.1.1. The checked source bundle hash is `237912c75d2c7e8219fced7bb79e5ed8fca0f620d6f4d259cdfa58748445fcd1`; license hash is `1cb5ddc0b89c5bf0c5ccdf3a387edc4a1408c922968d633c719265c8ccdd354b`. This verifies inspected source provenance, not a fresh running-image inspection. No enterprise source or general resolver was copied.

Suggestion: the report points to lerp line 1198; the declaration is at 1199. Adjacent context and exact bundle hash make the reference unambiguous, so this is not a blocker.

## Limits retained

Public proxy updates bypass the owned hook's replacement of saved common with generated common. Grouped-bar collisions and derived colors therefore establish neither saved-option reachability nor persistence. Line, stacked and broader namespace behavior remain unresolved. The synthetic light-base case leaves the dashboard dark. Runtime errors and the first callback-clone failure remain disclosed. A follow-up saved-composition lane is separate evidence and is not accepted here.

No production changes occurred. Future helper work requires explicit design/task approval, typed ownership, inventory/checker enforcement and the 400 physical lines/file, 300 logical units/file and 50/function caps. No approval state was edited. The research can support a narrow helper design; full B2 and original application behavior remain open.

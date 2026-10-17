# Correct normalized-channel rounding before closing the token contract

- VERDICT: REJECTED, with one Important numeric-contract blocker.
- TASK: Independent appearance research review, 2026-10-17. This is not production acceptance or full B2 acceptance.
- Reviewed candidate: `76edf85a46298f7bc5212ff9944e4b66e9baa4af`.
- Original source: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.
- Reference image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`.
- Frozen input allowlist SHA-256: `129654e9d227ef23770950128935fec587df57ceb54b73972e8baa41f4f1f967`.

The eight recorded cases remain credible bounded observations. A narrow derived-token helper design is justified after correcting the source arithmetic contract. The current byte-domain equation cannot be accepted as an exact opaque-hex implementation rule.

## Important finding: operation order changes rounding

`appearance-contract-close/assert.py:13` blends byte channels directly. The report's implementation paragraph likewise instructs a [0,255] channel blend. AG Charts 12.1.1 parses hex into normalized channels, mixes those channels, clamps the mixed values to [0,1], multiplies by 255, then uses JavaScript `Math.round`. Floating-point ties make these procedures observably different even for valid opaque six-digit hex values.

The installed library itself returns `#8b0000` for foreground `#000000`, background `#9b0000`, and t=.9; the proposed byte formula returns `#8c0000`. The independent [library comparison](math-check.json) covers every pair of integer channel inputs for four fixed ratios. Direct-byte mixing differs in 0 dark-grid pairs, 1,220 light-grid pairs, 118 dark-subtitle pairs, and 237 light-subtitle pairs. The normalized expression matches actual `Color.mix(...).toString()` for all 262,144 pairs.

Required per-channel order is `Math.round(clamp((fg / 255) * (1 - t) + (bg / 255) * t, 0, 1) * 255)`. Preserve the grid expressions `1 - .257` and `1 - .1` and subtitle literals `.57` and `.38`. This computes encoded-sRGB interpolation; the mix path does not invoke linear-light conversion. Fix the report and offline oracle, add discriminating source-based tie cases, then regenerate the publication hashes. Do not alter recorded runtime observations to fit a corrected oracle.

## Mechanical evidence and publication safety

All commands ran from `D:/Source/QOpenBB`. No browser, install, build, production suite, private credential file, owner environment file or production edit was used. The kiro-review production suite and RED requirements are N/A for this explicitly scoped research review.

| Command | Result |
| --- | --- |
| `git diff -- .kiro/specs/openbb-self-service/chart-appearance-contract-close.md` | Exit 0; no tracked diff. `git status --short --` identifies the spec document as untracked, so the complete document was read directly. |
| `wsl -d Debian -u mc -- bash -c 'cd /mnt/d/Source/QOpenBB && pipeline/.venv/bin/python artifacts/parity/appearance-contract-review/offline/assert.py'` | Exit 0; 39/39 pass. Inputs were copied into the review-owned directory; fresh output is byte-identical to the frozen original assertions. |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/check.py` | Exit 0; 38/38 checks pass, including all 26 publication sizes/hashes, six dependency/original Git blob hashes, finite JSON, eight unique IDs, callback-marker exclusion and targeted secret/path checks. |
| `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/math-check.cjs` | Exit 1, intentionally exposing the byte-formula mismatch; normalized source equivalence passes every channel pair. |
| `rg -n 'TBD\|TODO\|FIXME\|HACK\|XXX'` against the spec, report, assertion and launcher/journey/cleanup scripts | Exit 1 means no matches. |

The exact reviewed publication paths, sizes and hashes are preserved in [the frozen input allowlist](reviewed-input-allowlist.json); [checks.json](checks.json) records the actual measured hashes. This set is safe for a clearly labeled research publication, but the numeric claim must be corrected before publishing it as a closed exact contract. Manual inspection of all eight PNGs found synthetic financial data and UI only. Text review found generated disposable credential handling, not credential values. Excluded private/raw paths must remain excluded. Local filesystem paths and loopback stack URLs in the safe evidence are reproducibility metadata.

Dependency metadata and the actual license text confirm AG Charts Community 12.1.1, MIT. Original `terminalpro/package.json` pins 12.1.1. The checked bundle hash is `237912c75d2c7e8219fced7bb79e5ed8fca0f620d6f4d259cdfa58748445fcd1`; license hash is `1cb5ddc0b89c5bf0c5ccdf3a387edc4a1408c922968d633c719265c8ccdd354b`. These identify the inspected installed community package, not a new image inspection. Source references confirm defaults, text/chart-background aliases, clamp and rounding; the actual lerp declaration is line 1199, one line after the report's pointer.

Two attempted shell source-range reads had quoting errors and supplied no useful source evidence. The Python checker then read the exact bundle ranges successfully. No retries changed a failing behavioral assertion.

## Boundary findings

The report correctly distinguishes public-proxy resolver updates from original UI reachability and persisted saved options. The original `useChartOptions.tsx:406-434` does replace saved `common` with generated `common` before merge. Grouped-bar family/common/position observations therefore do not settle saved-state composition, line namespaces, generated-versus-saved conflicts, or save/reopen. Light-base replacement within the dark dashboard does not prove integrated light-mode behavior. Cleanup and initial callback-clone failure are retained, and known original runtime errors remain visible.

Finite case projections contain only data and explicit presence values. The added source comparison does not copy a general resolver or enterprise code. No production code changed; production caps do not apply to this research. Later helper tasks must carry inventory/checker enforcement and the 400 physical lines/file, 300 logical units/file and 50/function caps.

After arithmetic remediation, the narrow helper design may proceed for explicit resolved opaque-six-digit-hex tokens. Complete B2, original controls, application persistence, renderer acceptance and release remain open. No phase approval is changed by this review.

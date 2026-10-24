# Radar prerequisite verification

RD0 establishes the original Radar contract, retained FMP fixture and inactive interfaces. It does not establish replacement rendering, visual parity or publication. The existing Waterfall alpha remains unchanged.

Independent review approves RD0. Workspace source `d12d0b724e2d70ccccdfdc8274e814762e2425f7` contains the inactive declaration, shared fixture and original-browser characterization tests. Probe files were normalized to LF before commit without changing executable text. The next work is the two inactive implementation lanes.

## Evidence

- Original source: Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Owned isolated Playwright reference runs used one worker. Run4 passed one test in 33.8 seconds; run6 passed its Area-only test in 27.3 seconds. Run5 failed on the original stale Area tooltip and retains the completed Line axis/navigation observations.
- The mixed fixture establishes signed radial geometry, repeated spokes, distinct Line/Area missing-value behavior and observable polar-axis thickness changes. Retained AG Grid 34.1.1 and AG Charts 12.1.1 source supplies capture/aggregation/inversion order, raw domain rules and the polar tick-selection contract. Source-derived facts are distinguished from browser observations in the owning contract.
- FMP fixture: 15 quarterly AAPL revenue amounts for FY2023-2026, all original USD; FY2026 Q4 remains missing. PowerShell derivation and independent Python reconciliation match the 40-record retained provider response, SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. Retrieval was 2026-10-20; no new fetch. Independent review also matched the committed shared TypeScript fixture.
- Inactive declaration `compatibility/radarContracts.ts`: SHA256 `ea9b189b715471059741fa5c1b1eae086f212ccf898b93e691f7987a0b09c820`; 162 physical lines, 103 logical units, no executable functions. Non-mutating Biome checked one file and exited zero. The combined complexity checker exited zero with no violations for the declared scope.
- Pinned TypeScript 6.0.3 with existing Vite declarations: baseline/current each exit one with four byte-identical inherited diagnostics, zero added or owned diagnostics. These are typography TS7031 and three runtimeConfigSchema Zod-type diagnostics. This is scoped non-regression evidence, not a clean application compile.

## Verification commands and scope

The reference wrapper invokes the existing Playwright CLI with `artifacts/chart-radar/original/reference.config.ts` and separate evidence roots. Declaration lint runs from `vendor/workspace/terminalpro` using its existing Biome binary. Type comparisons use the pinned verification TypeScript binary with `artifacts/chart-radar/interfaces/{baseline,current}-tsconfig.json`; exact logs and final exit files remain local.

The root command `pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-radar/workspace-changes.json --changes data_api=artifacts/chart-radar/data-api-changes.json --output artifacts/chart-radar/complexity-final.json` passes with explicit fork identities. The changed production scope is the inactive declaration; unrelated unfinished catalog/Perspective work is not accepted by this milestone.

## Limits and retained failures

The original Area tooltip stayed on the first datum at the tested negative/zero hit coordinates. Some original CSV requests failed after quick actions, so no clean-network claim is made. The original navigator/miniature actions caused no observed drawing or slider change; their visible controls remain part of the original flow. Replacement data correctness is not waived by an original failure.

Initial probe collection failed for missing ESM configuration, and an import-readiness check found two matching cells. Both were corrected without production edits. Run3 was accidentally repeated into the same output directory; its initial log bytes were overwritten, so it is not counted as independent evidence. The retained run4/run5/run6 results above are the relevant observations. The first complexity invocation omitted repository identity in its input manifests; corrected manifests produced the final passing result. None of these failures is concealed as a passing check.

The full shared contract and task ownership are in `.kiro/specs/analyst-workspace/radar-contract.md`. Actual Radar rendering, financial chart screenshots, light/dark comparison, fresh reopen, export and image publication remain open. Dependency excerpts, raw provider captures, browser traces and credentials are excluded from the reviewed mirror.

## RD2: inactive editor/session accepted

Workspace `c8b0561e37e2aebd5011bb8b1ef79b3c7c5f1f66` adds the five owned adapters and three focused test files. Nine tests pass; the independent reviewer reran those tests and eight-file lint. Malformed Polar label fields and coerced enum arrays found during review now have regression coverage. Selection keeps existing source identity and numeric order; appearance retains generated-common replacement and saved-family precedence; edits produce validated patches without storage writes or renderer imports.

All five whole production files pass caps, maxima 132 physical/56 logical/25 per function; the parent combined inventory gate exits zero. Scoped TypeScript diagnostics exactly match the four inherited baseline diagnostics above; a direct parent invocation confirms nonzero compiler exit one with those four errors. This is inactive source acceptance only. Existing original controls are represented, but live control effects, persistence and rendering await RD3/RD4. Detailed local evidence and independent verdict remain under `artifacts/chart-radar/rd2/`.

## RD1: inactive renderer accepted

Workspace `b7a7fcb0899bee0328503aff9a23d8ccd81d35c2` adds five owned renderer/assignment modules and four test/fixture files. Fifteen tests pass, including eight actual ECharts SSR cases; independent review reran the full focused set and nine-file lint. Checks cover retained FMP values, signed affine geometry, zero midpoint, Line gaps versus Area missing-to-center geometry, duplicate spokes, hidden-series bounds, multiple radii and selected appearance/legend/tooltip behavior. Title/subtitle drawing and Radar Line's fill-palette stroke were corrected before acceptance.

Whole-file caps pass, maxima 258 physical/92 logical/22 per function; the parent combined gate exits zero. Pinned TypeScript retains the same four inherited diagnostics with no owned additions; worker recorded nonzero exit two. No live routing, browser pointer interaction, visual parity, reopen, export or new image is accepted here. RD3 joins the two independently reviewed inactive adapters. Detailed local evidence is under `artifacts/chart-radar/rd1/`.

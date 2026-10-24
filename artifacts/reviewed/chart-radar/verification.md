# Radar verification

RD4 is accepted for the bounded Radar Line/Area Table/File journey: independent behavioral review passed, and the owner approved the current appearance on 2026-10-24. Feature/application acceptance and RD5 publication are complete for this scope. Radar is published as alpha-40086673952-1. Earlier sections below record acceptance at each source checkpoint.

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

## RD3a: capture and setup accepted

Workspace `eb74a5e7a0ee48b395efa8cf2a113cfdd5cb5933` registers Radar observation capture and setup projection. Independent review approved the actual diff, reran 11 focused tests and eight direct normalization probes, and inspected the 172 passing tests across nine affected regression files. Non-mutating Biome passes eight files. The named policy preserves original wrapper precedence, finite Dates and own-valueOf values, missing positions, duplicate rows, selected field order, aggregation before inversion and empty selection. Nonfinite aggregate output becomes missing for Radar.

The maintained combined complexity gate passes with zero errors and zero violations; whole-file maxima are 329 physical lines, 140 logical units and 30 per function. Scoped TypeScript retains four unchanged inherited errors against the actual archived pre-change capture/setup import graph; this is non-regression evidence, not a clean compile. Local commands, identities, review and gate reports remain in `artifacts/chart-radar/rd3a/`.

RD3 overall and live session/editor/caller routing (RD3b) remain pending. Packaged FMP, light/dark appearance, refresh/reopen/export acceptance (RD4) and publication (RD5) remain pending. This checkpoint does not activate Radar or change the published Waterfall alpha.

## RD3/RD3b: source integration accepted

Workspace `af226971c53922de5925d9b068fbfbd81df02527` connects Radar Line and Radar Area to the existing Table/File session, editor, caller and ECharts host. Independent review approved the 14 production files, including the narrow Histogram foreign-control guard required by the expanded intent union. Existing baseline, range, setup, stamps, reducers, persistence, legend and resize owners remain in use. Focused hook/editor and mocked-host caller checks cover selection, empty fields, controls, fresh JSON reopen and affected prior-family behavior; they do not establish packaged chart drawing.

Verification passes 88 distinct tests; the independent reviewer reran 14. Non-mutating Biome passes 18 files. All 14 whole production files meet the caps, with maxima 341 physical lines, 104 logical units per file and 38 per function. The maintained combined gate exits zero with zero errors and zero violations. Scoped TypeScript exits two with 2,680 inherited error records unchanged after source-coordinate normalization. The broader caller imports explain the larger diagnostic scope; this is not a clean compile. No pre-implementation failing test run occurred, so historical RED evidence is missing and no TDD claim is made. Exact commands and the independent verdict remain in `artifacts/chart-radar/rd3b/report.md` and `review.md`.

RD3 and RD3b are accepted for source integration. Application and feature acceptance remain false. Packaged FMP values, light/dark visual parity, browser diagnostics, refresh/fresh-session reopen and PNG export remain RD4; publication remains RD5. The published alpha remains Waterfall.

## RD4: application accepted

Independent review approved the retained behavioral evidence on 2026-10-24. Candidate run4 passed both family tests in 2.0 minutes with one worker; original run3 passed its comparison test in 35.1 seconds. Maintained tests are `terminalpro/tests/e2e/live-chart/radar-chart.spec.ts`, `radar-original.spec.ts` and `radar-fixture.ts`, committed at Workspace `194691e589ad75afb74d227574402dfb43ba6aea`.

The Dagger-built, locally loaded candidate image is `sha256:da46760094b602464e9adefa6caae2b100f34307a486076fa9cec4625125a760`, application source `af226971c53922de5925d9b068fbfbd81df02527`. It ran image-only; subsequent changes were tests only. Original source `38dffc33389aca0e4a87e0e88d42f7067aa220df` used image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` with the historical backend overlay. Its actual loopback origin was port 60307, not advertised 55550. This comparison is not an image-only release claim.

The fixture reconciles all 15 exact reported USD amounts and retained raw/CSV/JSON hashes. Complete FY2023-2025 revenue uses Q1-Q4 spokes; FY2026 has three quarters and missing Q4. Both candidate families pass distinct public financial paths on a common center/scale, native tooltip series/category/formatted amount, light/dark captures, marker defaults/size, polar thickness/shape/inner radius, legend hiding and all-hidden domain behavior. Each passes refresh, saved settings, fresh-session reopen and PNG export. Export checks compare the financial region against native drawing; the independent reviewer verified both PNG signatures and hashes. Area also passes aggregate/inverted financial geometry, visible empty-selection recovery and navigator exclusions. Duplicate grouping order remains covered by the earlier capture/setup regressions, not the unique-quarter sample.

Candidate page/CDP/network assertions pass after original-page save/refresh and each fresh reopen/export. Original run3 retains one CSV console ERR_FAILED and its matching request failure, with empty page-error and HTTP-failure arrays; no clean-original-network claim is made. Scoped test typing retains two inherited Canvas overload errors in unchanged histogram-observer.ts and no owned diagnostics. This is non-regression evidence, not a clean application compile.

Earlier failures remain part of the record. Original run1 expected raw digits in an abbreviated grid cell; run2 exposed ambiguous independent path matching. Candidate run1 assumed a tooltip role and targeted overlapping vertices; run2 required explicitly serialized Line marker defaults; run3 reused the invalidated original session after a fresh login. Reviewed test-only corrections use category readiness, distinct jointly matched paths, native scoped tooltip text at separated vertices, resolved defaults and separate family tests with fresh login last. Full field casing follows the displayed labels. Financial values and tolerances did not change.

Exact commands/results remain local under `artifacts/chart-radar/rd4/`, including `candidate-run-4`, `original-run-3` and `behavior-review.md`. Raw browser JSON, logs and runtime descriptors are excluded from the public mirror. Four exact-byte light samples are linked inline in the owning milestone. On 2026-10-24 the owner approved the current Radar Line/Area appearance, including added spokes, right-side radial labels (partly obscured by Area fill), legend symbols/spacing and lower plot placement. The pictured Line circle symbols and Area square symbols differ from the original. This completes bounded RD4 application acceptance; it does not claim pixel identity or general acceptance of other radial families. No UI, source or image changed for this approval. RD5 publication is recorded below.

## Published Radar alpha

Workflow [40086673952](https://github.com/norandom/QOpenBB/actions/runs/40086673952) passed both publication jobs and created [alpha-40086673952-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40086673952-1) from root `2acb5d4660d9a704ae3f8ad626a291f998c650dc`. The release pins Workspace `194691e589ad75afb74d227574402dfb43ba6aea` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. Downloaded compose.yaml, default.env.sample and manifest.json match their release asset hashes. Both services passed six anonymous pulls in total: digest, alpha tag and latest, with matching source labels and manifest/config identities. See the [release manifest](release-manifest.json) and [anonymous pull evidence](anonymous-pulls.json).

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:8f22fdab935ebd7cc6a63bc62d4d2888862fba79ff8c4024ac25e437d04ab44b` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:225f63760084988b8bc9971076eac40b6feb6e1453369451898d35f4f92b56cb` |

Local browser acceptance exercised application `af226971c53922de5925d9b068fbfbd81df02527` in image `sha256:da46760094b602464e9adefa6caae2b100f34307a486076fa9cec4625125a760`. The later Workspace source `194691e589ad75afb74d227574402dfb43ba6aea` changes tests only; CI rebuilt that pin into the separate published bytes above. Publication and pull verification do not establish browser execution of those CI bytes, assembled Compose acceptance or owner-server deployment. RD0-RD5 are complete for the bounded Radar Line/Area milestone; no next milestone is selected here.

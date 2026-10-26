# Funnel packaged progress and visual refinements

F4 remains open. Five candidate browser checks and three original reference checks passed; two visible default/layout mismatches found by comparison have source repairs. Rebuilt-image and owner visual acceptance are still required. No new release is published.

Candidate evidence uses Workspace `490afc974a15099380ff65abf2ad1ab135c55f4c`, image `sha256:dd1fbf41d475a9a9a8aec30be74bb9281f69771c5ca12b73715379e202a720bd`. The source repairs below postdate that image. Browser regressions are committed as `fa3aff173f445faab2e925b5284b079e4938c23e`; label defaults as `1644f09315fecde000ea7ccd4fee56085898d054`; spacing as `1fe9178b9d3c0016f912a1c3d85663afdcf88203`.


---

# F4 browser evidence review progress

Five browser checks pass for the bounded claims below. F4 remains incomplete; these results do not establish native visual parity or the full control/export contract. Review performed 2026-10-26 without executing tests or changing production.

## Identity and evidence

All three reviewed runs identify Workspace `490afc974a15099380ff65abf2ad1ab135c55f4c`, image `sha256:dd1fbf41d475a9a9a8aec30be74bb9281f69771c5ca12b73715379e202a720bd`, loopback origin `http://127.0.0.1:55604` and the same disposable runtime with only its data mount. Each run uses one worker, exits 0, records no skipped/flaky/unexpected tests and passes its post-run source integrity check. Independently hashed frozen test copies all match `bb6f4faedea36ca0dc194ae15a1b8b3db79b2efb2e60b3485b3377a02fe2e2c0`.

- `defaults-2/run.log` (defaults-2): three passing tests, 117.3 seconds. Reviewed results, frozen source, runtime qualification and per-variant defaults observations.
- `recovery-1/run.log` (recovery-1): one passing test, 35.0 seconds. Reviewed pixel counts, prior tooltip point, accessible notices and diagnostics.
- `controls-1/run.log` (controls-1): one passing test, 52.9 seconds. Reviewed frozen assertions, results and diagnostics.

## Verified bounded effects

Defaults use the retained AAPL FY2026 Q2 reported USD CSV, SHA256 `c6b74bd3da1bca8d74438cf441e5b784c40ca27cc4e70d11da42cb34d7b206e8`. The fixture checks exact input values and provenance. Every variant produces all five expected stage/field tooltip pairs in light and dark modes. Displayed values are rounded magnitude strings: 111.18 B, 54.78 B, 35.89 B, 35.83 B and 29.58 B. This verifies formatted financial output, not unrounded tooltip precision. Saved selected columns are Stage/LevelUSD. Native resize actions and PNG download/signature/dimension checks pass.

Recovery begins with actual valid Pyramid paint: 144,236 nonuniform pixels on a 619 by 593 canvas and a demonstrated hit at normalized (0.5, 0.2), displaying `First / Valid USD: 100`. Reordering Invalid USD first enters rejected negative data directly without an intermediate empty selection. The invalid and no-series states both contain zero nonuniform pixels on the same-sized canvas and no tooltip after revisiting the known point with a 600 ms dwell. Corrective removal and re-addition restore stage labels through reachable Set Up controls. The explicit negative and no-series notices are recorded. Saved columns finish as Stage/ValidUSD.

Controls exercise all three gallery variants, Direction selection, Aggregate toggling, eligible Drop-Off/Shadow controls and independent label switches. Stage labels are observed when enabled and absent in numeric-only mode. The final Pyramid numeric-only state survives reload and a separately authenticated reopen. These assertions establish only their stated effects; they do not prove horizontal geometry or every toggled style.

All reviewed chart journeys record empty page-error, HTTP failure, console-error and request-failure arrays. The reopened page also passes the strict diagnostics assertion.

## Corrections and unresolved scope

`defaults-1` remains a failed run (exit 1, three failures): the fixture selected raw IDs as visible labels, whereas the UI exposes Level USD. The explicit display-label map corrects the test; no production repair is implied. Draft recovery checks were corrected before these runs to allow blank canvases, enter invalid data by direct reordering and test a demonstrated prior tooltip coordinate.

`onboarding-1` remains independently failed (exit 1): first-login diagnostics recorded HTTP 404 for `/api/pro/pro-developer-onboarding-info`. Clean subsequent chart journeys do not repair or supersede that first-login failure. No blanket diagnostic exclusion was introduced.

Remaining F4 work includes native matched-image review; meaningful geometry/style effects for Direction, Aggregate, Drop-Off, Shadow and common controls; missing gaps and zero hit targets; zero-total Pyramid; custom palettes and unsupported-theme recovery; source refresh and table/Cartesian round trips. Current label assertions do not establish exact numeric-label contents or numeric absence in stage-only mode. PNG checks prove a valid downloaded image with plausible dimensions, not current chart contents. Reopen coverage applies to the final Pyramid state, not every variant's options. Native matched captures in `visual-1` are outside this progress review and were still running when requested.

Decision: accept these five passing checks as partial F4 evidence only. Do not mark F4, visual parity, onboarding or release readiness complete.


---

# Numeric-label default repair review

APPROVED for the bounded source repair and its per-task commit. This does not accept F4, the packaged candidate, visual parity, or release readiness.

Reviewed independently on 2026-10-26 using the task-local kiro-review protocol. The only production behavior change is the Funnel appearance fallback for numeric labels, from enabled to disabled. Import ordering and equivalent Number constants are formatting changes. The changed scope is limited to `application/funnelAppearance.ts` and `tests/unit/chart-compatibility/funnelControls.test.ts` in Workspace.

The native source at `38dffc33389aca0e4a87e0e88d42f7067aa220df` establishes `createDefaultSeries().label.enabled=false` in `utils.tsx`. `hooks/useChartOptions.tsx` carries that label through its fallback for the three Funnel native scopes. The replacement previously supplied true. I inspected the retained native Funnel image at `../../native/visual-2/browser-output/funnel-visual-reference-or-a7521-al-reference-light-and-dark/default-light.png` and candidate image at `../browser/defaults-2/browser-output/funnel-candidate-Funnel-ca-27361-unnel-retained-USD-defaults/default-light.png`: the native image has stage names without numeric labels; the candidate adds numeric labels such as 111 B. These are observed pre-repair visual failure evidence, not an automated RED test or a failed browser-suite result.

The repair changes the application fallback only. Existing composition still applies selected-theme, generated and saved values above it. The new parameterized assertions cover all three families, preserve stage-label defaults, exercise explicit generated true/false and overriding saved true/false, check editor state, and check native-scoped toggle patches. No financial values, capture, aggregation, persistence schema, geometry or renderer ownership changes appear in the diff. No new placeholders, credentials or runtime imports were introduced.

Mechanical evidence reviewed in `verification.json`: focused controls suite 27 passed, exit 0; bounded Biome check exit 0 with the existing noExportsInTest rule exclusion; diff check exit 0. I did not rerun heavy checks because the controller explicitly requested a read-only review without concurrent heavy verification. The supplied complexity inventory reports 258 physical lines, 81 logical units and maximum 27 per function for the production file, below 400/300/50. Tests are excluded from production caps. The prior inventory baseline was `490afc9`.

I independently verified the reviewed byte identities: production SHA256 `4a9c11f46a00efeadf331d143a5a4cbde2a100d57e1faf1741cde2697b587ebb`; test SHA256 `7056bc46a2d562c9757f285bbcb14e1869c1397b9f6f2d06587b57d1257f43ee`.

Findings: none requiring remediation for this source task. Required remediation: none. A newly packaged candidate still needs the remaining F4 application and visual checks; pre-repair image evidence does not establish post-repair visible behavior.

---

# Funnel spacing repair independent review

APPROVED for the bounded source repair on 2026-10-26. Rebuilt-image endpoint comparison and overall F4 acceptance remain pending.

- TASK: Funnel zero-outer band spacing repair.
- Baseline: Workspace `fa3aff173f445faab2e925b5284b079e4938c23e`.
- Boundary: WITHIN. Only `echarts/funnelGeometry.ts` and `tests/unit/chart-compatibility/funnelGeometry.test.ts` change. Reviewed actual diff against the `../spacing-findings.md` (native-source contract), complete affected functions and new assertions. The reviewer authored that read-only contract, not this implementation.
- Production SHA256: `ff17e2b0896a291bc3238a8fca7ba5fc88592a46beb3b79f66bd637f7abef42d`.
- Test SHA256: `3c8ea02e7015abb60b99358bcf3d12432c22c0e16b582ba5bc08df1a530920f0`.

The implementation uses native n-s denominators for multiple Funnel stages and resets effective spacing to zero for a singleton. It pins the final endpoint to one, updates band centers and connects only immediate numeric neighbors. The empty-stage loop never evaluates the denominator. Admitted spacing endpoints zero and one remain finite, including singleton spacing one. Missing stage indices are retained; no bridge is introduced across a missing endpoint. Signed-magnitude widths, zero-value hit rectangles, Cone, Pyramid, common padding and title handling remain unchanged.

Mechanical results:

- Tests: PASS, 17 checks across geometry and renderer suites, exit 0. `verification.json` records the exact bounded command and `tests.log` retains results. New independent five-stage assertions use bandwidth 3L/19 and gap L/19 in both directions; singleton, touching/full spacing, empty/zero viewport and missing connectors are exercised. Existing zero/extreme, Drop-Off-off, Cone and Pyramid assertions remain.
- Lint: PASS, two files, exit 0, no fixes; command in `verification.json`, result in `lint.log`.
- Complexity: PASS, matching fa3aff1 scope in `workspace-changes.json`, `complexity.exit` 0 and final `complexity.json` errors/violations empty. Whole production file: 188 physical lines, 97 logical units, maximum function 19.
- Independent lightweight checks: changed-file diff whitespace clean; no placeholder or concrete private-key/API-key patterns in the production file. No new imports or runtime bindings require additional dependency validation.
- RED: the pre-repair failure evidence is the retained native/candidate endpoint discrepancy and source-derived formula documented in `spacing-findings.md`. No separate pre-edit failing unit run exists or is claimed. The new assertions directly reject the previous half-gap formula.

No blocking findings remain. Earlier complexity attempts failed on stale inventory metadata and are superseded by the final matching-scope result; no source edits were needed for that issue. Existing jsdom canvas-measurement warnings remain in the test output and do not establish browser pixel parity. Native node rounding can still produce small raster differences; verify the repaired endpoints in the next identified image rather than compensate with common padding.

REMEDIATION: None for this source task. F4 packaged appearance and the broader control, refresh, theme, persistence and export gaps remain independently open.


---

# Funnel browser test source review

APPROVED for the bounded partial-evidence test commit after the two wording corrections below were verified. This does not accept F4 or the packaged candidate.

Independent read-only review on 2026-10-26 covered `funnel-candidate.spec.ts` and `funnel-visual-reference.spec.ts`, the existing `review-progress.md`, defaults-2/recovery-1/controls-1 logs, native visual-2 log and a retained native tooltip/diagnostic record. No tests, browsers, builds or production edits were run.

Resolved wording findings:

- Renamed `Funnel candidate controls persist visible independent labels and direction`. The test sets the Direction combobox to horizontal, checks the control value, then returns it to vertical. It does not assert horizontal geometry or persisted direction. A bounded accurate title is `Funnel candidate controls expose direction and persist final Pyramid numeric-label mode`. Keep the existing broader geometry and persistence gaps open.
- Changed the financial helper's assertion description from `exact retained USD tooltip` to `formatted retained USD tooltip`. `expectedBoxTooltipNumber` expects rounded magnitude strings; exact raw input values are separately checked against the CSV. This wording correction must not be described as new financial precision evidence.

The candidate source hash matches the reviewed five-check evidence: `bb6f4faedea36ca0dc194ae15a1b8b3db79b2efb2e60b3485b3377a02fe2e2c0`. The native visual-reference source hash is `1a073fa74612caf593c696fdc04c8f80c6260100731b8fc9db014945674665b1`. Recorded results are three candidate defaults tests, one recovery test and one controls test passed; three native light/dark reference tests passed. These are prior results for the identified source bytes. Renaming a test or assertion description requires recording new source identity; it does not require treating old evidence as if it ran new bytes.

Candidate diagnostics are collected before login, retained in finally blocks, and checked through `expectApplicationDiagnostics` without adding exclusions. The separately authenticated reopen is also checked. Original diagnostics are retained with an explicit characterization limitation and without a cleanliness claim. The inspected native record contains `Unexpected token '<'` and file-request failures; these remain baseline findings. Native tooltips actually contain the stage and formatted value without a field name, so removing the field-name requirement from this reference test matches observed native behavior and preserves all five stage/value checks. The candidate still requires the field name.

The recovery check demonstrates prior visible paint and a real tooltip point, clears polygons and tooltips in invalid/no-series states, and recovers through reachable Setup controls. The partial review correctly limits controls, PNG, precision and reopen claims. The reference test captures ordinary gallery defaults without opening Customize or injecting options; light/dark changes are explicit. No direct production option replacement or diagnostic suppression is introduced by these files.

I compared the final candidate file directly with the frozen defaults-2 source: the only two differences are the title and assertion-description changes above. Assertions and execution are unchanged. Final candidate SHA256 is `e147eb68a038722b7a4752b7d1c2d90ad8277f800aedf61b49fa662c0f6bd7af`; native reference remains `1a073fa74612caf593c696fdc04c8f80c6260100731b8fc9db014945674665b1`. No new browser run was required solely for these wording changes, and prior run identities remain unchanged. No required remediation remains. The source is suitable for a partial-evidence test commit. F4 remains incomplete: direction/aggregate/drop-off/shadow/common-style effects, exact label-content checks, missing/zero cases, theme recovery, source refresh, broader roundtrips, PNG contents and native matched visual acceptance remain outside these passing checks. The numeric-label fallback repair also needs a newly packaged candidate; these pre-repair browser runs do not validate that repair.
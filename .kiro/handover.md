# QOpenBB session handover

Updated 2026-11-25. The published Company Research dashboard passed its Ubuntu Docker and Playwright journey. Current development extends the existing data API with supplied-input financial methods.

## Where to resume

- **Ubuntu Company Research live acceptance, 2026-11-25.** The canonical Playwright journey passed both phases on the digest-pinned Batch B release at root `91a2ee5`. All required captures matched (45 initial, 9 after container recreation). Coverage includes displayed financial observations, selection changes, peer failure and recovery, export/import and retained state. The owner waived the FMP ceiling; upstream send totals were not measured. The disposable Compose resources were stopped. [Roadmap](steering/roadmap.md)
- **Requirements resumed 2026-11-25.** The owner confirmed the 63-session DFII10 rule and included FCF yield in the first slice. The owner selected the company-level, point-in-time definition. The owner confirmed the 63-session price factors and missing-session rules. Requirements are approved. The [factor design](specs/factor-signals/design.md) is owner-approved. The [15-task plan](specs/factor-signals/tasks.md) is owner-approved. The owner identified the existing `qopenbb-data-api` container as the analytics backend. The factor design and tasks now target the packaged data API. See the [source inventory](specs/factor-signals/research.md) for the source boundary. Foundation tasks 1–7 and factor tasks 1–14 passed. ETF momentum and realized volatility use all 64 required closes, and the DFII10 regime uses the two dated yield endpoints. The methods return calculation candidates with source traces. Company FCF yield now uses the latest complete eligible fiscal year and observation-date issuer equity market value. The ordered ETF comparison calculates percentage-point spreads on matched windows. A missing close on one side preserves the other ETF’s values. The timing study computes benchmark-relative hit rates and slugging by decision-time regime, and drawdown along the exposed path. The foundation now applies financial rules and compares candidates with independent calculations on the supplied inputs. Factor tasks 12–14 now independently recalculate ETF values and spreads, DFII10, issuer FCF yield and timing diagnostics from dated inputs. The data API now runs installed methods in a bounded child process and persists immutable runs for their authenticated owner. A service call now verifies supplied or acquired inputs and saves each evaluation for its owner. Foundation task 8.1 adds signed internal HTTP discovery, evaluation and private saved-run reads. Foundation task 8.2 exposes signed widget and app discovery for an owner-selected saved output. The initial modeling contract bundle and saved-output consumer mapping are pinned (9.1). The compatibility gate checks candidate contracts and exercised success, partial and failure responses (9.2). Changed financial contract IDs now select executable checks (9.3). Next, register the six methods and verify saved evaluations in factor task 15. [Impact evidence](../artifacts/reviewed/factor-signals/modeling-impact.md). [Compatibility evidence](../artifacts/reviewed/factor-signals/modeling-compatibility.md). [Contract evidence](../artifacts/reviewed/factor-signals/modeling-contract-bundle.md). [Projection evidence](../artifacts/reviewed/factor-signals/saved-output-widgets.md). [HTTP contract evidence](../artifacts/reviewed/factor-signals/model-http-routes.md). [Evaluation evidence](../artifacts/reviewed/factor-signals/evaluation-orchestration.md). [Study evidence](../artifacts/reviewed/factor-signals/timing-study.md). [Comparison evidence](../artifacts/reviewed/factor-signals/proxy-comparison.md). Company valuation stays in its own drill-down. [FCF yield evidence](../artifacts/reviewed/factor-signals/issuer-fcf-yield.md). [Method evidence](../artifacts/reviewed/factor-signals/price-and-real-yield-methods.md). [Session evidence](../artifacts/reviewed/factor-signals/session-windows.md). [Registry evidence](../artifacts/reviewed/factor-signals/model-registry.md) and [example evidence](../artifacts/reviewed/factor-signals/dated-examples.md)
- **Published dashboard baseline.** The latest release is alpha-44340458084-1. The modeling changes are source milestones on `main`.
- **Current checkout:** `~/Source/QOpenBB` on Ubuntu. Use the [maintainer Git workflow](steering/delivery-workflow.md#maintainer-git-workflow).
- **Historical Windows checkout:** `D:/BuildArtifacts/QOpenBB/fmp-expansion-b/root`, branch `work/fmp-expansion-b`, pushed as `HEAD:main`. The checkout at `D:/Source/QOpenBB` is behind `main` and holds unrelated uncommitted work; do not overwrite it.
- **Product direction from discovery (owner, 2026-11-18):**
  - regime-based macro and cross-asset stories, shipped as dashboards with changeable inputs
  - finance shown step by step, so it makes sense to quants and portfolio managers
  - simple, transparent factors only: FCF yield, momentum, volatility, sector rotation, FRED macro factors, carry and credit stress
  - the proprietary factor-timing work in `../facdrone` stays out of this repository: do not read, copy or summarise it
- **Parked work, saved before the system switch of 2026-11-25 (not merged, not reviewed):**
  - `backup/source-checkout-2026-11-25` holds the uncommitted state of the old `D:/Source/QOpenBB` checkout, on base `d8a2d28`. Its only work missing from `main` is the unfinished renderer binding of October: `pipeline/qopenbb_ci/catalog_renderers.py`, `tests/contracts/test_renderers.py` and the `--bind-renderers` option in `catalog_cli.py`. It binds three widgets only and predates Company Research and FMP Batches A and B. Owner decision: leave it parked. Reviving it belongs to the `openbb-self-service` spec.
  - `backup/company-research-worktree-2026-11-25` holds older document and spec versions from the Company Research worktree, on base `3b47ead`. `main` supersedes them.
  - Do not merge either branch as is: most files are older copies of files that `main` has since advanced.
- **Not in Git:** the private harness and raw provider evidence under `D:/BuildArtifacts/QOpenBB/cross-asset-inputs`, and the provider keys in `.env`. Copy them by hand to keep them.
- **Live provider usage to date:** 60 FMP and 16 FRED requests, with no guard denial.

## Latest accepted work: cross-asset and macro input verification

- All seven tasks of [the plan](specs/market-data-integrations/cross-asset-input-tasks.md) are accepted on 2026-11-18. No image was built or published.
- Result: [record](../docs/reference/cross-asset-inputs.json) for six ETFs and eight FRED series; [checkpoint](../docs/provider-coverage.md#cross-asset-and-macro-inputs-checkpoint-2026-11-18).
- Owner decisions: FRED data are public; every story chart names its source in the headline; QOpenBB is an academic MIT-licensed project that ships no provider data.
- Private harness and raw evidence: `D:/BuildArtifacts/QOpenBB/cross-asset-inputs`. A rerun needs a new reviewed acceptance.
- Next: the `factor-signals` and `research-stories` specs in the [roadmap](steering/roadmap.md), starting with one thin slice for the commodities-versus-technology story.
- Limits the modeling slice must handle:
  - **Fund prices exclude dividends.** Returns built on them are price returns, so a comparison with SPY understates the dividend payers.
  - **Fund history was requested for two windows only:** 2007 to 2011 and August to November 2026. The start of each fund's history and the years between are not probed.
  - **Energy series have missing days:** Henry Hub about 1,400 across the 2000s, WTI 122 in 2003.
  - **STLFSI4 and NFCI are weekly;** the other six series are daily.
  - **Credit stress rests on those two indexes.** The requirements still exclude the ICE BofA and Moody's spread series, and FRED serves only three years of the ICE series.
- Open contract gaps: the test does not require a rights label or tie the display status to it; WTI has role `oil-spot` but type `unknown`; the mirrored summary shows 74 rows per fund beside a 2007 earliest date, because it counts the recent window only.

## Latest publication: FMP Batch B

- Release: [alpha-44340458084-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-44340458084-1); [CI run 44340458084](https://github.com/norandom/QOpenBB/actions/runs/44340458084), attempt 1. Both jobs passed.
- Released source: root `9dfd5853f42c3b63c2da561cf3ac737c7f26b9ea`; API `5583c958d35282cb59037aae8218cec31d540697`; Workspace `ba03ec72299e1f75d9365bcb8e17925ca1149d58`. Both forks are on GitHub as `qopenbb/fmp-expansion-b`. The later 5.4/5.5 acceptance metadata commits are not the build source.
- Images: Workspace config `sha256:f7346021e3f4883361ae4b170c526d2341c3e5e3cc2035619403c4396e7e889f`, data API config `sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4`. `latest` matches both.
- Verification:
  - three anonymous assets and six anonymous pulls
  - CI provenance equal to the released Git bytes
  - a network-none API check passing 20 synthetic Batch B cases with zero sends
  - an isolated internal-network pair passing health, config, login, wrong-password, state and log checks
- Not verified: Windows host loopback and CI-image browser acceptance. No owner-server deployment is claimed.
- Local acceptance: eight API operations and five representative widgets, at cumulative 42 FMP requests, zero other providers and zero denials. Split history and the dividend and split calendars have API acceptance only.
- A production repair of the document query controls (Workspace `ba03ec7`) shipped with this release.
- [Publication review](../artifacts/reviewed/fmp-expansion-b/5.5-review.md), [release checks](../artifacts/reviewed/fmp-expansion-b/5.4-review.md) and [provider coverage](../docs/provider-coverage.md#batch-b-events-and-documents-checkpoint-2026-11-18).
- Owner direction recorded at publication, since refined by discovery (see "Where to resume"); still not specified or approved:
  - ship curated dashboards as product Apps, starting with an Events & Documents App
  - then Batch C (provider DCF, custom DCF, as-reported statements) with a DCF drill-down App that uses a gated, step-by-step validation flow, aligned with the financial-modeling spec
  - bring the analyst Apps to a professional-terminal standard, reusing the existing widgets and chart library to support hypotheses beyond tables
  - start with `kiro-discovery`.

## FMP expansion status

Batches A and B are complete and published; no FMP expansion batch is in execution.

- **Batch A.** 26/26 tasks accepted. Published in alpha-44132016951-1 from root `32d1140590eac95cd3f4af890249b7ab6d19f832` (see the previous publication below).
- **Batch B.** 25/25 tasks accepted. Published in alpha-44340458084-1 from root `9dfd5853f42c3b63c2da561cf3ac737c7f26b9ea` (see the latest publication above).
- **Batch C.** The five provider DCF, custom DCF and as-reported statement operations remain candidates, without a design or task plan.

The [reviewed plan](specs/market-data-integrations/fmp-expansion-plan.md) names the 24 candidate operations: A11 financial/valuation, B8 events/content, C5 DCF/as-reported. The [inventory](specs/market-data-integrations/fmp-expansion-inventory.md) separates retained-adapter candidates, new-contract candidates and the unchanged ten-model baseline.

Batch B work was done in `D:/BuildArtifacts/QOpenBB/fmp-expansion-b/root` with sibling `data-api` and `workspace` checkouts, all on `work/fmp-expansion-b`. Raw and private evidence is under `D:/BuildArtifacts/QOpenBB/fmp-expansion-b/evidence` and must not be published. The Batch A tree at `D:/BuildArtifacts/QOpenBB/fmp-expansion-a` is historical. Any new batch needs its own approved design, task plan, request allowance and fresh ledger; do not reuse an earlier ledger.

The separate modeling foundation retains its approved 18-task plan. Repository coordinates and selected-method input/definition gates remain open. The proposed repository name, `qopenbb-financial-modeling`, is not an owner decision, and no new repository was created. Full FMP completion, DCF and FRED/WACC are not prerequisites for a narrowly selected historical cash-conversion method.

## Previous publication: FMP Batch A

- Release: [alpha-44132016951-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-44132016951-1); [CI run 44132016951](https://github.com/norandom/QOpenBB/actions/runs/44132016951), attempt 1.
- Released source: root `32d1140590eac95cd3f4af890249b7ab6d19f832`; API `a7c6ae2139b4dcc16571d0c23ade483a114a0068`; Workspace `bf180ef506286886da224df9ff184cd1ace2397e`. Acceptance metadata `8f469a67785fe58abb964e500be966ae1715e164` is later and is not the release build source.
- Three anonymous asset downloads and six public image pulls passed. The network-isolated API check passed three synthetic cases with zero real-provider calls. The published pair passed identity, readiness, full configuration, login, wrong-password rejection and bind-state checks through its isolated internal network; no financial route was called.
- Windows host-loopback transport for this published pair remains unverified after the failed host checks. No CI-image financial browser run or new owner-server deployment is claimed. Local financial acceptance covers eleven API models and four representative widgets under the unchanged 43/48 FMP ledger; seven widgets and future AI remain unknown.
- [Publication review](../artifacts/reviewed/fmp-expansion-a/publication-review.md) owns the final acceptance and immutable image identities. [Provider coverage](../docs/provider-coverage.md) owns the input/UI boundaries. At that time B8/C5, house modeling and AI/Excel were separate work; B8 has since been delivered as Batch B.

## Previously published: Company Research

- Release: [alpha-43604526965-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-43604526965-1).
- CI run: [43604526965, attempt 1](https://github.com/norandom/QOpenBB/actions/runs/43604526965). Both candidate and publish-alpha passed after one dispatch.
- Release source: root `fbd81eaf11d82b47043592f60736009304f198c8`; Workspace `bf180ef506286886da224df9ff184cd1ace2397e`; API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. The later documentation-only closure does not change this build identity.
- Workspace source is available on `qopenbb/company-research`. The unchanged API source remains remotely reachable on `qopenbb/statement-period-provenance`.
- Three public assets and six anonymous digest/tag/latest image pulls passed. The public environment asset is `default.env.sample`; installation instructions save it locally as `.env.sample`.

See [Company Research](../docs/company-research.md), [publication review](../artifacts/reviewed/company-research/publication-review.md) and [final integration review](../artifacts/reviewed/company-research/final-integration-review.md). Publication review SHA-256 is `0d6e2258ac66cb03bae66c5190bd31d55103f1b0479136e29ccc36b57782ccd4`.

## Company Research verification and limits

The local packaged financial journey, export/import, explicit foreign-source recovery, fresh authentication and retained-directory recreation passed at root `4736c31` and browser hash prefix `c9a267`. Its local image pair differs from the CI rebuild. Publication checks establish the public images' identities and accessibility, not a second financial browser run against those bytes.

All 54 required captures matched. Cumulative usage was 291 FMP requests under the reviewed 320 ceiling, zero FRED and zero denials. Twelve additional requested-only entries were not consumed by the required capture assertions. Failed attempts and their cumulative ledgers remain preserved externally.

The checkpoint's ACL/content review is closed. Historical broader access, absence of a pre-correction payload hash and absence of an independent initial Workspace inventory snapshot remain disclosed. Future checkpoint creation now uses the checked private writer; this separate post-run harness change passed 39 tests with one existing platform skip and six independent checks.

Source verification passed 509 joined Workspace tests and 135 supported root checks, with one skip and three deselections; the separate peer-adapter suite passed ten tests. Final complexity covered 741 files with zero violations. Release CI passed 461 tests, with 12 skips and one deselection. Existing unrelated compiler/chart/schema baseline failures are not declared green. Full IA-B, house modeling, validated rankings, live macro coverage, backup/restore and owner-server deployment are outside this milestone.

## Company Research checkout continuity

The clean published implementation checkout is `D:/BuildArtifacts/QOpenBB/company-research/root`; the corresponding Workspace and API checkouts are sibling directories. Release evidence and private failed-run records remain under `D:/BuildArtifacts/QOpenBB/company-research`.

The original `D:/Source/QOpenBB` checkout remains on its prior source commit with pre-existing dirty inventories/catalog work and `.openidea/` preserved. Only reviewed feature metadata, documentation, sanitized evidence and this handover are synchronized there. Do not reset, blanket-checkout, stash or overwrite unrelated work to make it resemble the published checkout. Use the isolated checkout or the tagged release for the accepted implementation.

Company Research requires no further implementation. A follow-on workstream needs its own explicit scope; do not infer authorization to implement house modeling, AI/Excel or server deployment from this completed milestone.

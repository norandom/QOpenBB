# F1 independent source review

Approve the inactive data adapter only. Reviewed on 2026-10-26 against Workspace HEAD `68b1e41d414234c4e191d39207ca6f84347a5bf5`, the approved Funnel contract Data 1-6, frozen `funnel-data-design.md`, and `f1-design-review.md`. The three new files were read in full because they are untracked and absent from `git diff`. All nine entries in `worker/hashes.json` match their actual bytes, including the three source/test hashes and retained evidence.

## Source findings

No blocking defect found. Paths below are relative to `vendor/workspace/terminalpro`.

- `echarts/funnelData.ts:196` follows selected-ID order and never falls back to an unselected descriptor. Lines 18 and 44 preserve duplicate identity, category and missing positions; genuine zero remains a numeric observation. Lines 53-78 reject malformed present values and unsupported numeric provenance with exact paths. The orientation discriminator is checked at line 184.
- `echarts/funnelData.ts:42` detaches source-row arrays; line 201 deep-copies descriptor metadata, including empty-result descriptors. No supplied projection is mutated or frozen. The actual ordinary setup and aggregation owners were read: Count includes missing group rows and preserves original source units separately from the derived count descriptor. The focused assertions at `tests/unit/chart-compatibility/funnelData.test.ts:131` verify these semantics.
- `echarts/funnelData.ts:102` rejects negative Pyramid inputs and zero total. Scaled compensated totals and cumulative boundaries at lines 129-165 avoid raw-total overflow, preserve missing slots, bound axial fractions and retain tiny raw observations even when geometry underflows. Lines 215-221 preserve signed values while normalizing finite magnitudes, including the all-zero domain. The independent expected halves and thirds distinguish axial fractions from equal-area geometry.
- `tests/unit/chart-compatibility/funnelData.test.ts:300` preserves all five retained reported amounts and cites the source hash. The amounts and hash match the independently reviewed financial reconciliation. This proves preservation of overlapping reported levels, not additive revenue decomposition or current issuer/provider authenticity.
- Production reference search finds only the new adapter's own type import and declaration. No capture, aggregation, renderer, persistence or shared-state owner was added; routing remains inactive. Other untracked work was preserved.

## Mechanical evidence

Executed in WSL Debian with PATH `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/bin:/bin`. First two commands use `vendor/workspace/terminalpro` as cwd; complexity uses repository root.

```sh
/mnt/d/Source/QOpenBB/artifacts/task-1.2/bun-linux-x64/bun x vitest run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/funnelData.test.ts --maxWorkers=1
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/compatibility/funnelContracts.ts src/components/General/Table/Chart/echarts/funnelData.ts tests/unit/chart-compatibility/funnelData.test.ts
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-funnel/f1/workspace-changes.json --changes data_api=artifacts/chart-funnel/f1/data_api-changes.json --output artifacts/chart-funnel/f1/review/complexity.json
```

Independent results: focused Vitest exit 0, 21 tests passed; Biome exit 0, all three files clean; combined complexity exit 0, zero errors/violations. Complete production counts are 62 physical/46 logical/max function 1 for contracts and 222/112/max 26 for adapter, below 400/300/50. Current manifests identify the exact two added production paths and current fork revisions.

Read the retained TypeScript 6.0.3 harness and diagnostics, without unnecessarily rerunning it: direct-dependency baseline and candidate each have 33 diagnostics, zero added and zero owned. The harness enables `skipLibCheck`; this is baseline-relative scoped evidence, not a clean full application compile. All referenced evidence hashes matched. RED log is nonempty and task-relevant: the new suite failed because the adapter module did not yet exist, exit 1; assertions had not executed. Fresh GREEN independently confirms implemented behavior.

A targeted `rg -n 'TODO|TBD|FIXME|HACK|XXX|password|secret|api_key|BEGIN PRIVATE'` over the three exact files returned exit 1, no matches; manual reading found no hardcoded credentials. Default product/tech/structure steering files are absent, as previously recorded; available required review steering was read.

## Review Verdict
- VERDICT: APPROVED
- TASK: F1 inactive Funnel data contract and adapter
- MECHANICAL_RESULTS:
  - Tests: PASS (focused command above, exit 0, 21 tests)
  - TBD/TODO grep: CLEAN
  - Secrets grep: CLEAN
  - Static checks: PASS (independent Biome and caps, exit 0; retained scoped typing has no added/owned diagnostics)
  - Boundary: WITHIN (three assigned new files)
  - Boundary audit: CLEAN
  - RED phase: VERIFIED (missing-module failure; no RED assertions ran)
- FINDINGS:
  1. FYI: Frozen finite geometry, identity, provenance and detached-output semantics are implemented at the source lines identified above.
  2. FYI: Full application typing, rendering, browser behavior, integration, persistence and export remain outside this inactive-helper review.
- REMEDIATION: None for F1.
- SUMMARY: F1 satisfies the bounded approved data contract; this approval does not accept the Funnel milestone or any rendered application behavior.

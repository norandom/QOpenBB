# Candidate baseline and compatibility

QOpenBB has acquired owned sources and selected the latest upstream API release as an unvalidated candidate. Continue with locked toolchains, provider adaptation and clean image builds; do not install this acquisition record as an accepted release. [sources.lock.json](../sources.lock.json) remains the source identity record, with no image identifiers or validated release declared.

## Source identities checked on 2026-10-16

| Input | Exact identity | Evidence status |
| --- | --- | --- |
| Owned Workspace, Full | `e5e4170f1a09bdf14339eb760b7ce09e31e5484f` | Task 2.1 frontend packaging accepted; retained notices originate from acquisition `be00e95`; backend/runtime pending |
| Original data API acquisition | `7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2` | Historical develop snapshot; acquisition provenance and notices remain retained |
| Current data API adaptation base | `5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0` | Selected OpenBB 5 release checkout at `vendor/data-api`; provider compatibility and runtime remain unvalidated |
| Latest upstream API release candidate | `openbb-v5.0.0`, commit `5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0` | Official release published 2026-09-30; identical annotated tag available in owned fork; candidate objects acquired |
| FMP source release | `openbb-fmp` 1.6.1 | Published archive hash verified; restoration/adaptation pending |

[API release evidence](../sources/api-release.json) records the tag object and release metadata. GitHub's generic `releases/latest` returns the desktop `ODP` release, so the selection compared published API releases separately. The [official v5 release](https://github.com/openbq-org/OpenBB/releases/tag/openbb-v5.0.0) is the latest API release found. Its source pyprojects declare core/API 2.0.1 even though release prose describes the general 2.0.0 package line. The package inventory records source metadata separately from PyPI observations and the mutable develop branch.

The source lock records the selected adaptation commits; original acquisition identities remain in the provenance records. A future build must explicitly select one source revision plus recorded adaptation commits. It must not silently combine packages from the acquired develop snapshot and the release candidate. A branch name and a candidate label are not executable release pins.

## Adaptation and validation gates

| Finding from exact source inputs | Required change or check | Current status |
| --- | --- | --- |
| FMP 1.6.1 requires core `>=1.6.10,<2.0.0`; candidate contains core 2.0.1 and no FMP provider | Restore FMP with provenance in owned fork, adapt registration/profile/income fetchers, test values and financial metadata, then lock runtime | Incompatible unchanged; not implemented |
| Full frontend uses the retained Bun lock and owned monorepo | Protected frozen install and fresh Full frontend build | Task 2.1 accepted; see [build evidence](workspace-build.md). Backend and image acceptance remain pending |
| Backend Dockerfile runs a lock rewrite | Preserve existing dependency lock; prove clean frozen build | Not implemented |
| Commercial chart dependencies and absent optional TradingView assets | Resolve essential rights/replacements and declare disabled optional renderer | Release constraints open; see [licenses](licenses.md) |
| Full flags include historical hosted capabilities | Verify API-discovered FMP/FRED widgets; disable unsupported hosted AI enhancements and integrate Anthropic | No runtime acceptance |
| API schema, widget contracts and Excel consumer may differ | Regenerate and verify consumers against a single accepted API; begin Excel only after Anthropic acceptance | No generated or Office acceptance evidence |

All acquired application source remains unchanged. These proposed adaptations are distinct from upstream behavior and belong to their owning implementation tasks. No dependency constraint edit alone would establish compatible FMP data. No provider credential or model discovery result would establish dashboard or Anthropic acceptance.

## What is reproducible now

[Required packages and upstream locks](../sources/packages.json) record source paths, declared versions/dependencies and exact SHA256 values for the core, API launcher, equity/economy routers, FRED, Workspace frontend/backend and deferred Excel inputs. Upstream locks are source evidence; they do not yet form the complete compatible QOpenBB runtime lock. The metapackage is inventoried for provenance, not selected as a substitute for explicit required own-source package installation.

Owned checkouts use `core.autocrlf=false` and contain exact Git blob bytes for Linux build inputs. To reacquire, clone each recorded owned repository without checkout, set that local Git option, fetch the recorded SHA, and check out the SHA detached. Fetch the API candidate tag separately and verify its peeled commit against the inventory. Never resolve a mutable branch or import private split repositories during a build.

Task 1.1 verified Git identities/clean source trees, upstream release metadata, retained notice bytes, package/lock hashes and JSON integrity. Ignored `artifacts/task-1.1/` contains captured registry metadata and task-local verification output. It did not install application dependencies, build images, run providers, open dashboards, exercise Anthropic or test Excel. These capabilities remain unverified. Acquisition records, notices and inventories are excluded from production complexity caps; later maintained code requires the executable complexity foundation and its 400 physical lines/file, 300 logical units/file and 50/function limits.

A baseline readiness claim is disproved by a source/hash mismatch, unresolved essential component right, incompatible provider/runtime lock or failed required user journey. Preserve earlier source/image and state-backup references when replacing a validated release; none has yet been validated here.

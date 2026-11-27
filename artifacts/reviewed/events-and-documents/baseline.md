# Events and Documents baseline

The 2026-11-27 baseline confirms the four installed Batch B routes and widgets, the disposable browser login, and source staging for the planned Workspace build. The composed App and live FMP entitlement remain pending.

Root `58463391823a7dd7b75daa9dc0a4b822f8a68fe2` plus the two inventory edits used the clean, owned Workspace commit `eeb11a299978d2de74ade8734fbd18fcb52e469b` and data API commit `5583c958d35282cb59037aae8218cec31d540697`. The browser smoke used the published Batch B Workspace manifest `sha256:c2e9869c5756b689069dfaaac9c53bc17e876d4e2edd1619533ed96927c99fd9`, built from Workspace `ba03ec72299e1f75d9365bcb8e17925ca1149d58`. The paired data image used its current pinned data source and published manifest `sha256:79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73`.

| Check | Observed result | Local evidence |
| --- | --- | --- |
| Inventory ownership assertion using the same `owned` and `exclusion` functions as the checker | The planned catalog generator initially failed ownership resolution. After registration, all 13 planned production paths resolve to Events and Documents. All 16 shared paths and seven sampled test/generated paths resolve through existing inventory entries. | `inventory-red.log`, `check-ownership.py` |
| `python -m tools.quality.complexity --check` with each actual pinned fork commit as both base and head | Exit 0. Both scopes Git-verified, 220 measured files, no issues or exceptions. Root and Workspace inventory files measure 229 and 147 physical lines. | `combined.json` |
| Pipeline pytest quality, catalog snapshot, build and guard suites at one worker | 281 passed, one skipped, including the whole oversized fork rejection regression and actual-send guard tests. | `quality-build-guard.log` |
| Data runtime pytest installed joins and offline statement transport guard | 111 passed against synthetic responses. The join fixtures forbid live transports. | `installed-joins-retry.log` |
| Batch B catalog consumer suite using pipeline pytest plus the local data runtime package and dependencies | 14 passed. The initial separate environments lacked the other environment's packages. | `installed-catalog-combined.log` |
| Published data image under Docker network none, synthetic keys, local OpenAPI and widgets requests | All four GET routes and matching widget IDs are present. The disposable Compose mount independently served all four OpenAPI paths. No live sends. | `packaged-data.json`, `mounted-openapi.json` |
| Disposable loopback Compose and Playwright 1.64.0 | One headless Chromium 156.0.8078.4 worker authenticated into the Workspace shell, read the exact reviver token for `9007199254740993`, observed zero financial browser reads and captured no uncaught browser exceptions through CDP. The successful retry waits for the onboarding entity check before submitting. | `runtime-start.log`, `browser/final.log`, `runtime-stop.json` |
| Portable build entry and Workspace staging | `bash pipeline/ci.sh build --help` and Dagger CLI/SDK 0.21.8 checks passed. Staging from the development checkout rejected dependency symlinks. Fresh detached snapshots from the same verified commits staged successfully under the portable entry point. Image build and export are later work. | `tools-build-preflight.log`, `workspace-stage-diagnostic.log`, `staging-verified.json` |

The complexity report used CPython 3.13.15, Node 24.22.1 and TypeScript 6.0.3. The locally cached Dagger engine reports the digest pinned in `pipeline/tools.lock.json`. No live credentials were used, and the controlled and live feature journeys remain separate acceptance steps.

The Node parser regressions passed 15 tests and the strict no-emit TypeScript check exited 0. Both Compose containers and their network were removed. The portable helper does not support checked state removal on POSIX, so the disposable state remains under the ignored private runtime directory.

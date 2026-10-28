# Python source packaging review

## Combined source acceptance

APPROVED at final Workspace `dfda735c527663dd7ecc2f80af18e25843f575af`, joining the separately reviewed Valkey change. Independent narrow audit confirms the metadata/uv lock hashes below are unchanged and the final Dockerfile hash matches the Valkey review. The explicit combined scope includes all six modified/added/deleted paths. Final joined evidence measures 76 files with zero errors/violations: Dockerfile 188, Supervisor 40, metadata 138 and inventory 399 physical lines. The exact final inventory proposal SHA256 is `28b2f1aad8a60476aea15482b5efcf6049f937f9ca118f2e4219247f2460de98`; it supersedes the earlier proposal identity below. The controller may adopt that proposal and build the candidate. No tests or runtime operations were repeated for this audit.

VERDICT: APPROVED for source acceptance at Workspace commit `dbd3d5c6a66cbc9bbf4faf7f635b0fadd8361cc3`, using the reviewed inventory proposal below. No blocking production-code defect remains. Image/runtime acceptance is separate.

The independent reviewer inspected the maintained Dockerfile, PEP 621 metadata, generated uv lock, historical Poetry lock, focused packaging regression and dependency evidence. No network access, installation, image build or application runtime was performed.

## Verified source behavior

The maintained recipe removes Cython installation, application compilation, source deletion and stripping. It copies `api`, `routers` and `utilities` as owned Python source, preserving entrypoint, migrations, Full frontend selection, runtime paths and service configuration. Dagger assembly includes the backend directory and removes the context ignore file, so the new lock reaches the build context. Authentication source is unchanged.

Protected `uv sync --locked --no-dev --no-install-project` installs into `/opt/.venv` with the pinned CPython interpreter and Python downloads disabled. The non-package root is explicit. Pinned uv and uvx binaries are copied together; no runtime dependency resolution or unpinned uvx tool execution is introduced. Supervisor is now a locked runtime dependency instead of an additional install.

An independent read-only TOML comparison passed: all 151 historical package versions are identical; only virtual root `backend==0.1.0` and `supervisor==4.3.0` are added. Slowapi retains Git commit `d3442b2e1425a9db535732a0a06248470c7f9fd5`. Registry entries use PyPI and wheel records contain SHA256 hashes. The reviewed comparison reports all 136 historical runtime packages reachable plus Supervisor. Metadata keeps the Python 3.13 boundary, equivalent declaration ranges, development markers and Ruff configuration.

Retained logs show protected uv 0.12.5/Safe Chain 1.5.25, lock consistency and a 133-package Linux dry-run plan. These are resolver checks, not installed-package or native import evidence. `git diff --check` passed. Dockerfile and metadata are below the 400-line cap; the generated lock requires the documented exclusion. No new placeholders or secrets were introduced.

## Verification closure

- `checks/red.log` now records the new source-packaging regression failing against the isolated previous Dockerfile at the missing protected uv sync assertion. `checks/green.log` records all three focused packaging tests passing in 0.35 seconds. The prior evidence-only rejection is resolved.
- `checks/inventory-final.json` removes obsolete build-tools ownership/exclusion, owns backend metadata, identifies the protected native uv lock generator and updates the fork revision without importing unrelated working inventory changes. This exact 399-line proposal is approved for controller application: SHA256 `77235BCB4908C49403C7588AA9939E3C33D5BD17D375D8F4554B12A301251864`.
- The retained joined `checks/complexity.json` measures 75 files with zero errors and zero violations. Its explicit fork scope is `22180d8ec206e088a384f2a3c7345358b1832c7c` to `dbd3d5c6a66cbc9bbf4faf7f635b0fadd8361cc3`, including both build-tool deletions. Dockerfile is 178 physical lines, metadata 138 and inventory 399; uv.lock has the generated exclusion. No new complexity exception is needed. The command and empty error log are retained under `checks/`.

## Remaining runtime boundary

PY3 still requires the Dagger image build, actual `.py` module origins, absence of compiled application extensions/Cython, health/login, current/new-password behavior and an existing dashboard journey. Removing the compiler toolchain depends on actual native dependency wheel/build availability; resolver dry-run success cannot prove this. No build-speed claim is supported.

Untouched legacy Poetry Dockerfiles and the historical Poetry lock are outside this maintained Full-image path; their old commands are not compatible-support claims for the migrated metadata.

## Reviewed identities

- Dockerfile: `1447240EC06EFA3A15FEC3DB5C9D3755FF4153D9B238B5E869EC081BB8C15CBE`
- pyproject.toml: `6dbb37165aada23c1dbda763355d5150d2d4d5b0f27bbf76300d5e3d56d3403f`
- uv.lock: `979a61b3621c5edfa127f6b4f76d71485834c6e4a9a2544be790bfd62f9cfd93`
- Historical poetry.lock: `ae615c0d2a7b3b1affb54fa0ae1b17baeca92c751270be06a05daa12142d9633`
- Focused packaging test: `FA804B27CD76BEF48D69AC459354E933516F6DB7BA98E74DB4D6217F507A6B28`

# Task 4.6 SQLite test runtime

The isolated bootstrap and real mapped fixture roundtrip pass on the unchanged backend lock. This closes the task 4.6 test infrastructure boundary; no repaired reads, bulk-save behavior, application restart, renderer or browser acceptance is claimed.

## Reproduce

From WSL Debian as `mc`, execute:

```sh
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-4.6/verify.py
```

`verify.py` runs the maintained `tests_sqlite/run.py` launcher, Ruff checks and formatting checks. `evidence.json` records exact commands, exits, Python identity, installed distributions and SHA256 source manifest. `tests-final.log` preserves the absolute child pytest invocation. The child uses an explicit minimal environment, disables automatic pytest plugins, explicitly loads the locked asyncio plugin and starts in an empty disposable directory. Pytest temporary storage now uses an explicit `--basetemp` beneath the launcher sandbox. The launcher removes that entire sandbox and checks its absence after both successful and nonzero child exits. No service or helper process remains running.

`restore.sh` is the exercised protected restoration: unchanged `poetry.lock` and `pyproject.toml` copied to persistent `/home/mc/qopenbb-work/sqlite-runtime/backend`, exact checked-in `lite/build-tools.txt` restored by Safe Chain uv, Poetry 2.3.2/export plugin 1.10.0 checks/exports the lock with its dev group, and protected uv sync installs that export into the Python 3.13.15 venv with existing build constraints. No lock regeneration, new selected runtime dependency or image build occurred. The source manifest includes the original CRUD hash and Workspace revision. Full distribution identities are retained because a main-only image would lack the test packages.

## Frozen fixture interface

The sibling test directory does not inherit `tests/conftest.py`. Callers import `from tests_sqlite import fixtures` after bootstrap. Builders return real unsaved mapped objects with explicit UUIDs; callers add and flush each FK dependency layer in order:

- `entity_type(**overrides)`, `entity(kind, **overrides)`, `permissions(organization, **overrides)`.
- `user(role, **overrides)`; call separately for owner, creator, recipient and unrelated users. Synthetic passwords use the actual password decorator.
- `dashboard(owner, creator=None, organization=None, **overrides)`, `app(owner, **overrides)`.
- `dashboard_share(item, recipient, **overrides)`, `app_share(item, recipient, **overrides)` default to active view permission; overrides support inactive and other permission cases.
- `dependency_tables()` returns actual `(Base.metadata, dependency_closed_tables)`; original mapped types remain intact.
- Pytest fixture `sqlite_store` yields `(database_path, engine, async_sessionmaker)` for a per-test file with foreign keys enabled. Callers own sessions, explicit rollback after errors and any newly created engines. Bulk commits cannot escape the disposable file boundary.
- `file_engine(path)` in the already-loaded `conftest` enables FKs on every connection, including reopened engines. Do not import it as `tests_sqlite.conftest`: pytest has already imported it as `conftest`; importing twice installs duplicate isolation hooks.

Bootstrap patches `DotEnvSettingsSource._read_env_files`, which executes during source construction. Existing synthetic sentinel files prove interception before the initial production settings import; a Python audit hook independently rejects reads of those filenames and `.env`, rejects network DNS/connect/sendto, and records forbidden read attempts for fixture assertions. Sentinels are removed before application imports, leaving the account-config cwd empty. Direct pytest invocation without the launcher is rejected.

## Fresh evidence and limits

The final recorded run passes two tests, zero skips, exit 0; Ruff check and format checks also exit 0. Tests prove actual compressed bytes, gzip JSON recovery, UUID/creator identities, dates, FK rejection/rollback, app/dashboard shares and a new engine reading the persisted file. Actual query behavior belongs to tasks 4.7 and 4.8.

`first.log` records the initial 2-test setup failure caused by importing conftest twice; `second.log` records the correction. This was an infrastructure failure discovered after writing the bootstrap and tests, not a pre-implementation TDD RED run. No earlier failing-test evidence is claimed. Lint initially failed because the upstream per-file test exemptions cover `tests/*`, not this sibling directory; test-only explicit exemptions retain asserts and the required deferred imports. `lint-first.log` and `lint-fix.log` retain that correction.

Core steering `product.md`, `tech.md` and `structure.md` are absent at the instructed paths; applicable existing complexity, testing, CI, delegation and documentation steering was read. Tests and artifact-only environment restoration are excluded from production caps. Controller owns breadth registration and independent review; task readiness is not acceptance.
## Cleanup review remediation

Independent review rejected the first version because pytest retained three SQLite databases in its default `/tmp/pytest-of-mc` storage. The original cleanup claim was incorrect. The launcher now sets `--basetemp` inside its owned `TemporaryDirectory`, and the storage test asserts its resolved database path remains inside that sandbox.

`cleanup-evidence.json` and `cleanup-{success,nonzero}.log` record fresh normal (exit 0) and deselected-suite (exit 5) child runs; both sandboxes are absent after launcher return. The nonzero check proves cleanup when pytest returns a failure status; it is deliberately not another passing test claim. The launcher prints the removed path and independently rejects a surviving sandbox.

The one-time `cleanup-verify.py` inspected exactly the three reviewer-identified task directories, confirmed each contained only a 180224-byte SQLite database with the SQLite header, removed that database and its now-empty task directory, and recorded each removal. Shared pytest parent directories and all other test state were preserved. That one-time residue cleanup is not a reusable verification command; rerun `verify.py` for ordinary review. Tests and lint/format results in `evidence.json` supersede the pre-remediation source hashes.
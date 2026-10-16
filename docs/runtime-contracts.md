# Validate runtime and source inputs

Use `validate_configuration` with an explicit selected service set before handing inputs to the later runtime controller. This foundation freezes inputs; it does not start Compose, build images, validate installed API schemas or establish image-layer secrecy.

The dashboard checkpoint selects `workspace` and `data-api` without agent or Excel settings. Adding `agent` requires its image, `ANTHROPIC_API_KEY` and explicit `ANTHROPIC_MODEL`. Adding `excel` requires its real image and enables the `excel` profile. Inactive services are absent from validated output: parser-only image defaults must never be pulled, started or published. Production selection requires immutable registry digests. No validator contacts a registry.

`contracts/runtime.json` fixes the single HTTP origin at `0.0.0.0:23003:3000` and the only state bind at `./data/workspace:/data`. Data, agent and Excel remain stateless with internal ports 6900, 7777 and 80. Workspace depends on data availability, independently of agent startup. The runtime controller must reject added databases, tunnel services, Docker sockets and whole-file environment forwarding.

Provider credentials belong only to data-api. The agent receives only its own Anthropic credential and model; Excel receives no credentials. `OPENBB_API_AUTH=false` reflects the owner's single-user origin boundary, not application-session authentication. EconDB and OpenAI sample names remain unwired. Copy the public sample only when a private file does not already exist; all public credential values remain empty. These validators accept mappings and never open the operator's `.env`.

`PUBLIC_URL` is an absolute origin: local loopback HTTP or public HTTPS, with no credentials, query, fragment or path prefix. Advertised application, data and selected optional URLs are absolute. Forwarded protocol comes from this configured scheme. The application retains `/api`; data and agent routes remove their external prefix exactly once. Agent streams require buffering disabled in the later proxy implementation. Excel's route exists only when selected. Incoming forwarded headers cannot choose the advertised scheme.

`contracts/datasets.json` and `contracts/routes.json` are provisional acceptance inputs: AAPL company profile, one annual AAPL income statement and FRED GDP observations. Representative parameters do not limit future user queries. No installed operation identifiers or response schemas are claimed. Task 3.7 must bind actual installed routes and invalidate consumers on mismatch. Preserve financial units, currency, periods, frequency and missing observations during later data verification; quarterly GDP frequency must remain distinct from annualized units.

`select_source` returns sorted relative file paths for one owned source at its exact `sources.lock.json` revision. Workspace includes only `lite`, `terminalpro`, `backend-api`, LICENSE and NOTICE; data includes only `openbb_platform` and LICENSE. Excel is excluded until its separate eligibility gate. This is a file-selection interface for task 1.8, not permission to upload the repository root or all of `vendor`.

Recursive exclusions remove private dotenv files, keys, runtime state, backups, evidence, browser profiles, caches and dependencies. Directory names alone do not identify runtime output: narrowly scoped Python storage/logging modules and TypeScript state modules remain source code. The Workspace state seed and two FMP public lookup JSON files are explicit source-data exceptions. These exceptions bypass only the namespace component at its exact position and only for the declared source types or exact files; private filenames and nested state, evidence or secret directories remain excluded. New ambiguous source namespaces require review before extending this policy. Exact `.env.sample` and `.env.example` names are eligible only when every assignment is empty; `.dockerignore` excludes all dotenv files as additional protection. Symlinks fail closed and require a reviewed materialization rather than following an outside target. Package code, deterministic locks and notices remain eligible. Later builders must consume this filtered set and separately verify image contents and logs.

Offline synthetic-tree and input-validation evidence is retained under ignored `artifacts/task-1.6/`. Run:

```sh
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/contracts/test_configuration.py tests/contracts/test_source_filter.py -n0 --maxprocesses=2
```

A passing result proves these declarative boundaries only. Runtime port/mount inspection, installed-route compatibility and live-provider behavior remain unverified until their owning tasks run.

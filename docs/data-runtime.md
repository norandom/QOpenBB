# Data runtime

Run the selected OpenBB core, equity/economy routers and FMP/FRED extensions from `services/data-api/uv.lock`. The runtime uses core 2.0.1, equity/economy/FRED 2.0.0 and maintained FMP 1.6.1+qopenbb.1 from the owned checkout. It does not install the omnibus OpenBB package. Restore through the [protected toolchain](development.md) with `uv sync --project services/data-api --locked --no-dev --python 3.13.15`.

Set `FMP_API_KEY` and `FRED_API_KEY` in the private service environment, and keep `OPENBB_API_AUTH=false`. Start from `services/data-api` with `uv run --locked --no-dev uvicorn qopenbb_data.app:create_app --factory --host 0.0.0.0 --port 6900 --no-access-log`. The [data image build](image-builds.md#build-the-data-runtime) packages this internal factory entry point. Runtime credentials enter only when starting the container.

Credentials enter the selected core's `UserService` settings interface in memory. No settings file is written. The process disables FRED disk caching and needs no custom database or persistent volume. Provider keys are never schema defaults. Missing keys leave `/healthz` healthy but make `/readyz` return 503 with variable names. Readiness checks configuration and installed routes without provider calls or quota use. Rotate credentials by restarting the process.

The service trusts the owner's protected origin and private service network. It does not validate Workspace sessions or offer API Basic authentication; enabling `OPENBB_API_AUTH` fails initialization. Do not expose port 6900 independently. The owner must enforce Access and prevent clients from bypassing the protected origin. The frozen [runtime contract](../contracts/runtime.json) publishes only the Workspace origin.

Profile, annual income and GDP retain their [dataset paths](../contracts/datasets.json). FRED GDP observations preserve period-start dates and published missing values as null. `extra.results_metadata.GDP` retains frequency, units, seasonal adjustment and available title/notes: quarterly observation frequency is distinct from seasonally adjusted annual-rate units. Authentication, throttling and unavailable data produce explicit sanitized errors without a substitute source.

Task 3.5 fixture checks exercise the installed ASGI routes with deterministic provider transport responses, including missing observations and signed-URL failures. They establish fixture correctness only. Task 3.6 additionally exercises the identified loaded image with networking disabled: health, missing-key and configured-key readiness, installed local provider origins, supported routes and secret exclusion. Live provider entitlement, catalog generation, the protected public client and deployment remain unverified at this checkpoint. Verification uses the separate `dev` dependency group: restore it with `uv sync --project services/data-api --locked --group dev --python 3.13.15` in a disposable verification environment. The runtime restore above excludes pytest, pytest-xdist and pluggy. Run `python -m pytest -c services/data-api/pyproject.toml tests/providers/test_runtime.py tests/providers/test_fred.py -n0` inside the locked environment. The controller owns breadth records, contract freezing and independent acceptance.

## Generate supported consumer proposals

Use `pipeline/.venv/bin/python -m qopenbb_ci.catalog_cli` from WSL/Linux with an explicitly loaded local image ID. The command reads the schema actually served by that image in an owned container with networking disabled. It verifies the upstream widget utilities and bundled FRED app against the accepted source Git blobs, then runs the unchanged upstream `build_json` using the image's installed core. It requires Docker bind paths visible to the local daemon and the [protected pipeline environment](development.md); it installs no extra packages.

```sh
pipeline/.venv/bin/python -m qopenbb_ci.catalog_cli \
  --image sha256:5c23441a269126ebeee5d315caa922993c638d2527d4789684f32d6270cdc7fb \
  --source vendor/data-api --source-lock sources.lock.json \
  --inventory contracts/datasets.json --previous-routes contracts/routes.json \
  --output artifacts/task-3.7/proposed --work /home/mc/qopenbb-work/task37 \
  --allow-contract-change
```

The output preserves the full served schema separately from the three supported widgets. `routes.json` pins operation IDs, exact query parameter definitions, responses and their referenced components. Canonical files use sorted keys, compact UTF-8 JSON and a terminal newline; `hashes.json` hashes those exact bytes. There are no generation timestamps. `provenance.json` records source blobs, generator files and image labels. Two upstream generator runs must agree before proposals are written.

Widget endpoints retain `/api/v1/...`. Workspace combines them with the connector base `PUBLIC_URL/data`; adding `/data` to each endpoint would duplicate the origin prefix. `catalog-report.json` carries the public prefix and the explicit dataset/provider/widget mapping. The FMP company-profile and annual-income defaults use AAPL; the FRED default uses GDP. User-selected symbols and series remain supported route parameters, with provider units, periods, missing values and metadata preserved by the API envelope.

`apps.json` includes a mixed-source starter and the compatible subset of the upstream FRED app. Unsupported widget and group references are omitted with reasons in `catalog-report.json`. Compatible tab layout, parameters, group settings and descriptive metadata remain. Legacy chart/column state waits for the controller's renderer binding, and browser-key instructions are omitted because credentials belong to the data service.

Without `--allow-contract-change`, a changed path, operation ID, parameter or transitive response shape writes a compatibility proposal and exits 2. Stop affected consumer lanes for review. The explicit flag permits generating a review proposal; it does not accept consumer evidence. Compare against the previously accepted `routes.json` on later runs. Generator failures exit nonzero and do not write a new proposal set.

Task 3.7's local checks cover generation and references without using provider quota. Renderer bindings remain pending task 2.9; serving or embedding the final catalog and matching its final image belong to task 3.8. Excel generation remains blocked until Anthropic acceptance. This command does not establish dashboard rendering, live provider entitlement or a deployed catalog.

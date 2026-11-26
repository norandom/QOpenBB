# Run a pull-only Modeling candidate

Use the base Compose file for the Workspace and data API pair. Add the
Modeling override to run the independent image on the Compose network.
Workspace reaches `http://modeling:6901` after authenticating the user's
session. Workspace starts with the data API alone, so provider traffic on
`/data` remains available when Modeling is stopped. [Base Compose](../compose.yaml) ·
[Modeling override](../deploy/compose.modeling.yaml) · [Runtime inventory](../contracts/runtime.json)

## Prepare an isolated Linux deployment

Use Bash, GNU stat and a Docker daemon on the deployment host. Copy the
base Compose file, `.env.sample`, and the override and helper under
`deploy/` into a private deployment directory. Keep the same relative
paths. For a new, disposable deployment, run these commands there.

```bash
umask 077
cp .env.sample candidate.env
mkdir -m 0700 data
sudo install -d -m 0700 -o 10001 -g 10001 data/modeling
```

The image runs as numeric UID:GID `10001:10001`. Its only persistent
mount is `./data/modeling`, used for owner-scoped saved runs. The helper
checks the host owner and mode before pulling. The commands assume a
local, rootful Docker daemon without user namespace remapping.

Edit `candidate.env` in place. Set all three image variables to the
approved `registry/repository@sha256:…` references. Keep the approved
data API digest when evaluating a Workspace and Modeling candidate
against an unchanged data API. For a registry on the Docker daemon
host, use references such as `localhost:5000/qopenbb/modeling@sha256:…`.
Use the registry's manifest digest after the image has been pushed.
Authenticate privately with the registry as needed. Configure the
daemon for the local registry if it uses plain HTTP.

For an isolated run, choose a free host port, set
`WORKSPACE_BIND_IP=127.0.0.1`, and set both `WORKSPACE_HOST_PORT` and
the port in `PUBLIC_URL` to the chosen value. Set disposable
`OPENBB_ADMIN_EMAIL` and `OPENBB_ADMIN_PASSWORD` values. Fill in
`FMP_API_KEY` and `FRED_API_KEY` for the data API and provision one
shared `QFM_IDENTITY_CURRENT_KID` and `QFM_IDENTITY_CURRENT_SECRET`
pair. Generate at least 32 random bytes for the signing secret and use
their encoded text. Leave both previous key variables unset except
during rotation. Use a unique Compose project name and dedicated
deployment directory to isolate the containers and both state paths.

```bash
bash deploy/pull-modeling-candidate.sh qopenbb-modeling-candidate "$PWD/candidate.env"
```

The helper checks the effective image references, including shell
overrides, pulls the three images and starts them with builds and
implicit pulls disabled. Compose waits for container startup and the
configured health checks. The Modeling check confirms the private
authentication challenge and state-directory access. Verify
authenticated access separately by signing into Workspace and listing
models through the same-origin `/modeling/v1/models` endpoint. Evaluate
and reopen a saved run from Workspace to check persisted state. Stop
Modeling and check that an authenticated model request reports
unavailability while the direct-data catalog still responds through
`/data`. [Modeling contract](modeling-contract.md#connect-a-workspace-session)

To inspect, stop or remove this candidate, keep the same project name,
env file and Compose files. For example, stop just the Modeling service
during the availability check.

```bash
docker compose --project-name qopenbb-modeling-candidate --env-file candidate.env \
  -f compose.yaml -f deploy/compose.modeling.yaml stop modeling
```

Use `down` with those same options to remove the candidate containers
and network. The state directories survive container removal.

## Build and exercise the image set

On the build host, use the pinned Dagger CLI, SDK environment and native Docker Engine. From the repository root, choose a fresh output directory.

```bash
bash pipeline/ci.sh build-modeling --output artifacts/modeling-build --dagger-cli "$(command -v dagger)"
```

The command stages the Modeling package and its independent uv lock, exports the Linux AMD64 image, verifies the archive and loads it into Docker. The output directory contains the archive, the SHA-256 of each staged file and the loaded image identity. The model container has no provider credentials. Supply the current Workspace bridge key at deployment time.

For an isolated acceptance run, provide an immutable Workspace image containing the modeling controls, the published data API digest and the independently built modeling image at its registry digest. A loopback registry suffices for locally built candidates. With the repository's Playwright environment installed, run the analyst journey against the pulled images.

```bash
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
mkdir -p artifacts/modeling-acceptance
pipeline/.venv/bin/python verification/modeling-journey/packaged.py \
  --workspace-image "$WORKSPACE_IMAGE" --data-image "$DATA_API_IMAGE" \
  --modeling-image "$MODELING_IMAGE" --evidence artifacts/modeling-acceptance
```

The driver uses a disposable deployment root, two relative state binds, and an isolated loopback port. It runs the application with its packaged frontend, backend and dependencies, checks each running image against its selected reference, then tests authenticated evaluation, recreation, saved reopen and a live provider widget during a modeling outage. Its image inventory and three browser reports identify the set exercised.

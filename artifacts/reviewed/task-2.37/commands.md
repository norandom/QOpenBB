# Reproduce the joined helper checks

The joined runner uses Node 24.22.0 and the accepted dependency tree in an isolated WSL stage. It runs both strict compilers, all application and compatibility tests, and scoped Biome; `check.log` and `check.exit` record the controller run.

```powershell
wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/task-2.37/check.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-2.37/identity.py
```

The first identity attempt used bare `python3`, which Debian could not resolve. The explicit existing virtual-environment interpreter passed. This was an invocation failure before identity execution, not a suppressed check failure.

Whole maintained quality uses the repository checker with the copied exact manifests. Run from the repository root, with the pinned Node binary directory on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/task-2.37/workspace-changes.json --changes data_api=artifacts/task-2.37/data-api-changes.json --output artifacts/task-2.37/complexity-reproduction.json
```

`complexity.json` preserves the completed controller result. Manifests describe the observed current scope, including unrelated dirty files measured but not accepted. Generate fresh manifests if source or inventory changes; do not reuse these as proof for different bytes. `boundary-audit.json` records the accepted committed delta and frozen shared types. `prepare-records.py` copies controller reports and audits the boundary; it requires the ignored local controller scratch paths and is historical evidence, not a standalone setup command.

Public copies retain original paths in commands and script root calculations. Restore the corresponding original artifact layout before rerunning a mirrored script. No installation, browser, provider call, build or runtime activation is performed by these checks.

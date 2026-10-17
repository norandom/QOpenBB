# Joined verification commands

Workspace 76edf85a46298f7bc5212ff9944e4b66e9baa4af. All commands exited 0; no skipped tests.

- `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/task-2.40/check.sh`: both strict compilers, 88 application tests, 260 compatibility tests and scoped Biome. check.log and check.exit retain output.
- `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-2.40/identity.py`: 66 source/config identities match stage, identity.log/exit/json.
- Windows `py artifacts/task-2.40/boundary.py`: exactly five approved changed paths since 945e438; shared types/helpers, mapper, UI and flags unchanged.
- Windows `py artifacts/grid-capture-implementation/scope.py`, then `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/grid-capture-implementation/quality.sh`: current both-fork manifests and full maintained audit, 173 files, no errors or violations; quality.log/exit and copied complexity.json.

Tests/fixture/test-only compiler setup are excluded from production caps. Ordinary capture is 196 physical lines, 92 logical units, largest function 22. Unrelated dirty scope is measured without acceptance or staging. Existing exception target bytes were verified unchanged before source-pin rebinding. No browser, build or product GO.

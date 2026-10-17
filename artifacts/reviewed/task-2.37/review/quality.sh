#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/task-2.37/workspace-changes.json --changes data_api=artifacts/task-2.37/data-api-changes.json --output artifacts/task-2.37/review/complexity.json

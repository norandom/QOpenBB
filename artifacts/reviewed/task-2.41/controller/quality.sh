#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/appearance-editor-implementation/workspace-changes.json --changes data_api=artifacts/appearance-editor-implementation/data-api-changes.json --output artifacts/appearance-editor-implementation/complexity.json

#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
pipeline/.venv/bin/python -m tools.quality.complexity --check \
  --changes workspace=artifacts/task-4.9/workspace-maintained.json \
  --changes data_api=artifacts/task-4.9/data_api-maintained.json \
  --output artifacts/task-4.9/maintained-quality.json

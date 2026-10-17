#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p artifacts/parity/theme-matrix/state-valid
trap 'docker rm -f qopenbb-theme-matrix-20261017-stock > artifacts/parity/theme-matrix/cleanup.log 2>&1; rm -f artifacts/parity/theme-matrix/credential-private.json' EXIT
node artifacts/parity/theme-matrix/start.mjs > artifacts/parity/theme-matrix/start.log 2>&1
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/theme-matrix/journey.mjs > artifacts/parity/theme-matrix/journey.log 2>&1

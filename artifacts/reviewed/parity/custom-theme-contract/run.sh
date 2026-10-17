#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p artifacts/parity/custom-theme-contract
trap 'docker rm -f qopenbb-custom-theme-contract-20261017-stock > artifacts/parity/custom-theme-contract/cleanup.log 2>&1; rm -f artifacts/parity/custom-theme-contract/credential-private.json' EXIT
node artifacts/parity/custom-theme-contract/start.mjs > artifacts/parity/custom-theme-contract/start.log 2>&1
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/custom-theme-contract/journey.mjs > artifacts/parity/custom-theme-contract/journey.log 2>&1

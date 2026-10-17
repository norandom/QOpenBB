#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
node artifacts/parity/editor-contract-completion/start.mjs > artifacts/parity/editor-contract-completion/start.log 2>&1
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-contract-completion/journey.mjs > artifacts/parity/editor-contract-completion/journey.log 2>&1

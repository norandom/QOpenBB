#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-contract-completion/journey.mjs > artifacts/parity/editor-contract-completion/journey.log 2>&1
result=$?
printf '{"exitCode":%s,"command":"PLAYWRIGHT_BROWSERS_PATH=artifacts/playwright-browsers node artifacts/parity/editor-contract-completion/journey.mjs","runtime":"Debian WSL node24.22.0","remediationPass":2}\n' "$result" > artifacts/parity/editor-contract-completion/command-status.json
exit "$result"

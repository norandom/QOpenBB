#!/bin/bash
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-contract-retry/journey.mjs > artifacts/parity/editor-contract-retry/journey.log 2>&1
result=$?
printf '{"exitCode":%s,"remediationPass":2}\n' "$result" > artifacts/parity/editor-contract-retry/command-status.json
exit "$result"

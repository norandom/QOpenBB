#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-runtime-next/journey.mjs > artifacts/parity/editor-runtime-next/journey.log 2>&1
result=$?
printf '{"exitCode":%s}\n' "$result" > artifacts/parity/editor-runtime-next/journey-status.json
exit "$result"

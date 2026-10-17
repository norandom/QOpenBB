#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
node artifacts/parity/editor-runtime-next/start.mjs > artifacts/parity/editor-runtime-next/start.log 2>&1 || exit $?
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-runtime-next/discover.mjs > artifacts/parity/editor-runtime-next/discover.log 2>&1
result=$?
printf '{"exitCode":%s}\n' "$result" > artifacts/parity/editor-runtime-next/discover-status.json
exit "$result"

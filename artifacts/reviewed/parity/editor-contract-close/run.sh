#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
node artifacts/parity/editor-contract-close/start.mjs > artifacts/parity/editor-contract-close/start.log 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > artifacts/parity/editor-contract-close/start-status.json
if [ "$status" != 0 ]; then exit "$status"; fi
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/editor-contract-close/journey.mjs > artifacts/parity/editor-contract-close/journey.log 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > artifacts/parity/editor-contract-close/journey-status.json
node artifacts/parity/editor-contract-close/cleanup.mjs > artifacts/parity/editor-contract-close/cleanup.log 2>&1
cleanup=$?
printf '{"exitCode":%s}\n' "$cleanup" > artifacts/parity/editor-contract-close/cleanup-status.json
if [ "$status" != 0 ]; then exit "$status"; fi
exit "$cleanup"

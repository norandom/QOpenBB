#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
node artifacts/parity/grid-runtime-next/start.mjs > artifacts/parity/grid-runtime-next/start.log 2>&1
start=$?
if [ "$start" -ne 0 ]; then exit "$start"; fi
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/grid-runtime-next/journey.mjs > artifacts/parity/grid-runtime-next/journey.log 2>&1
journey=$?
node artifacts/parity/grid-runtime-next/cleanup.mjs > artifacts/parity/grid-runtime-next/cleanup.log 2>&1
cleanup=$?
printf '{"start":%s,"journey":%s,"cleanup":%s}\n' "$start" "$journey" "$cleanup" > artifacts/parity/grid-runtime-next/command-status.json
if [ "$cleanup" -ne 0 ]; then exit "$cleanup"; fi
exit "$journey"

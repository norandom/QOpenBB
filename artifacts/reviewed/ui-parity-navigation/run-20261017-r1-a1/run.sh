#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
export PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers
capture=artifacts/ui-parity-navigation/run-20261017-r1-a1
cleanup() {
  incoming=$?
  trap - EXIT INT TERM
  timeout --signal=TERM --kill-after=5s 30s node "$capture/cleanup.mjs" > "$capture/cleanup.log" 2>&1
  cleanup_code=$?
  printf '{"exitCode":%s}\n' "$cleanup_code" > "$capture/cleanup-status.json"
  if [ "$incoming" = 0 ] && [ "$cleanup_code" != 0 ]; then incoming=$cleanup_code; fi
  printf '{"exitCode":%s}\n' "$incoming" > "$capture/run-status.json"
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
node "$capture/start.mjs" > "$capture/start.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$capture/start-status.json"
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=10s 380s node "$capture/journey.mjs" > "$capture/journey.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$capture/journey-status.json"
exit "$status"

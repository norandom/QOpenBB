#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
export PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers
test "${AXIS_HEAVY_GRANTED:-}" = "controller-granted" || exit 79
export CAPTURE_ROOT="$1"
harness="$CAPTURE_ROOT/harness"
test -d "$harness" || exit 78
cleanup() {
  incoming=$?
  trap - EXIT INT TERM
  timeout --signal=TERM --kill-after=5s 90s node "$harness/cleanup.mjs" > "$CAPTURE_ROOT/cleanup.log" 2>&1
  cleanup_code=$?
  printf '{"exitCode":%s}\n' "$cleanup_code" > "$CAPTURE_ROOT/cleanup-status.json"
  if [ "$incoming" = 0 ] && [ "$cleanup_code" != 0 ]; then incoming=$cleanup_code; fi
  printf '{"exitCode":%s}\n' "$incoming" > "$CAPTURE_ROOT/run-status.json"
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
timeout --signal=TERM --kill-after=5s 180s node "$harness/start.mjs" > "$CAPTURE_ROOT/start.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_ROOT/start-status.json"
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=5s 900s node "$harness/journey.mjs" > "$CAPTURE_ROOT/journey.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_ROOT/journey-status.json"
exit "$status"

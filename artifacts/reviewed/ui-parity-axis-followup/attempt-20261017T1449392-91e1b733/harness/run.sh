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
  node "$harness/status.mjs" cleanup-status "$cleanup_code" || incoming=1
  if [ "$incoming" = 0 ] && [ "$cleanup_code" != 0 ]; then incoming=$cleanup_code; fi
  node "$harness/status.mjs" run-status 1 || incoming=1
  node "$harness/finalize.mjs" "$incoming" > "$CAPTURE_ROOT/finalize.log" 2>&1 || incoming=1
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
timeout --signal=TERM --kill-after=5s 180s node "$harness/start.mjs" > "$CAPTURE_ROOT/start.log" 2>&1
status=$?
node "$harness/status.mjs" start-status "$status" || exit 1
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=5s 900s node "$harness/journey.mjs" > "$CAPTURE_ROOT/journey.log" 2>&1
status=$?
node "$harness/status.mjs" journey-status "$status" || exit 1
exit "$status"

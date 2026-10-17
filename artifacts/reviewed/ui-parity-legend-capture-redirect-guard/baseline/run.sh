#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
export PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers
test "${LEGEND_HEAVY_GRANTED:-}" = "controller-granted" || exit 79
export CAPTURE_ROOT="$1"
harness="$CAPTURE_ROOT/harness"
test -f "$CAPTURE_ROOT/source-manifest.json" || exit 78
export ATTEMPT_STARTED_MS="$(date +%s%3N)"
cleanup() {
  incoming=$?
  trap - EXIT INT TERM
  now="$(date +%s%3N)"
  remaining=$(( (ATTEMPT_STARTED_MS + 2220000 - now) / 1000 ))
  if [ "$remaining" -gt 119 ]; then remaining=119; fi
  if [ "$remaining" -lt 1 ]; then remaining=1; fi
  timeout --signal=TERM --kill-after=1s "${remaining}s" node "$harness/cleanup.mjs" > "$CAPTURE_ROOT/cleanup.log" 2>&1
  cleanup_code=$?
  node "$harness/status.mjs" cleanup-status "$cleanup_code" || incoming=1
  if [ "$cleanup_code" != 0 ]; then incoming=1; fi
  node "$harness/finalize.mjs" "$incoming" > "$CAPTURE_ROOT/finalize.log" 2>&1 || incoming=1
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
timeout --signal=TERM --kill-after=1s 179s node "$harness/start.mjs" > "$CAPTURE_ROOT/start.log" 2>&1
status=$?
node "$harness/status.mjs" start-status "$status" || exit 1
if [ "$status" != 0 ]; then exit "$status"; fi
now="$(date +%s%3N)"
remaining=$(( (ATTEMPT_STARTED_MS + 2099000 - now) / 1000 ))
if [ "$remaining" -lt 1 ]; then exit 124; fi
timeout --signal=TERM --kill-after=1s "${remaining}s" node "$harness/journey.mjs" > "$CAPTURE_ROOT/journey.log" 2>&1
status=$?
node "$harness/status.mjs" journey-status "$status" || exit 1
exit "$status"

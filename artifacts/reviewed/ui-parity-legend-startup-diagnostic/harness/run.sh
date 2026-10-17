#!/bin/bash
set -u
export CAPTURE_ROOT="$1"
export ATTEMPT_STARTED_MS="$(date +%s%3N)"
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
test "${LEGEND_DIAGNOSTIC_GRANTED:-}" = "controller-granted" || exit 79
cleanup() {
  incoming=$?
  trap - EXIT
  trap '' INT TERM
  timeout --signal=TERM --kill-after=1s 59s node "$CAPTURE_ROOT/harness/cleanup.mjs" > "$CAPTURE_ROOT/cleanup.log" 2>&1
  cleanup_code=$?
  if [ "$cleanup_code" != 0 ]; then incoming=1; fi
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
timeout --signal=TERM --kill-after=1s 84s node "$CAPTURE_ROOT/harness/probe.mjs" > "$CAPTURE_ROOT/probe.log" 2>&1
exit "$?"

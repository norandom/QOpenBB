#!/bin/bash
set -u
test "${LEGEND_DIAGNOSTIC_GRANTED:-}" = "controller-granted" || exit 79
attempt="$1"
case "$attempt" in
  /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-startup-diagnostic/attempt-*) ;;
  *) exit 78 ;;
esac
test -f "$attempt/source-manifest.json" || exit 78
export CAPTURE_ROOT="$attempt"
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
# Conservative sublimits reserve time for the completed watchdog inventory.
timeout --signal=TERM --kill-after=60s 85s bash "$attempt/harness/run.sh" "$attempt" > "$attempt/supervisor.log" 2>&1
status=$?
timeout --signal=KILL 4s node "$attempt/harness/finalize.mjs" "$status" > "$attempt/finalize.log" 2>&1
final=$?
if [ "$final" != 0 ]; then exit "$final"; fi
exit "$status"

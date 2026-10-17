#!/bin/bash
set -u
test "${LEGEND_RELAY_GRANTED:-}" = "controller-granted" || exit 79
attempt="$1"
case "$attempt" in
  /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-relay-mount-source/attempt-*) ;;
  *) exit 78 ;;
esac
test -f "$attempt/source-manifest.json" || exit 78
export CAPTURE_ROOT="$attempt"
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
# Conservative sublimits reserve time for the completed watchdog inventory.
timeout --signal=TERM --kill-after=60s 85s bash "$attempt/harness/run.sh" "$attempt" 2>&1 | node "$attempt/harness/io.mjs" --bounded-log supervisor.log
run_codes=("${PIPESTATUS[@]}")
status=${run_codes[0]}
if [ "${run_codes[1]}" != 0 ]; then status=1; fi
timeout --signal=KILL 4s node "$attempt/harness/finalize.mjs" "$status" 2>&1 | node "$attempt/harness/io.mjs" --bounded-log finalize.log
final_codes=("${PIPESTATUS[@]}")
final=${final_codes[0]}
if [ "${final_codes[1]}" != 0 ]; then final=1; fi
if [ "$final" != 0 ]; then exit "$final"; fi
exit "$status"

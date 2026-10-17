#!/bin/bash
set -u
test "${LEGEND_HEAVY_GRANTED:-}" = "controller-granted" || exit 79
attempt="$1"
case "$attempt" in
  /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-capture-revised/attempt-*) ;;
  *) exit 78 ;;
esac
test -f "$attempt/source-manifest.json" || exit 78
# The independent timeout stops input at 2,100 seconds and kills at 2,220.
timeout --signal=TERM --kill-after=120s 2100s bash "$attempt/harness/run.sh" "$attempt" > "$attempt/watchdog.log" 2>&1
status=$?
printf '{"exitCode":%s,"inputStopSeconds":2100,"cleanupSeconds":120,"hardSeconds":2220}\n' "$status" > "$attempt/watchdog-status.json"
exit "$status"

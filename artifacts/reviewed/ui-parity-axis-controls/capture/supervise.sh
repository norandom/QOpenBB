#!/bin/bash
set -u
test "${AXIS_HEAVY_GRANTED:-}" = "controller-granted" || exit 79
attempt="$1"
case "$attempt" in
  /mnt/d/Source/QOpenBB/artifacts/ui-parity-axis-controls/capture/attempt-*) ;;
  *) exit 78 ;;
esac
test -f "$attempt/source-manifest.json" || exit 78
timeout --signal=TERM --kill-after=90s 1080s bash "$attempt/harness/run.sh" "$attempt" > "$attempt/watchdog.log" 2>&1
status=$?
printf '{"exitCode":%s,"termAfterSeconds":1080,"cleanupGraceSeconds":90,"outerBoundSeconds":1170}\n' "$status" > "$attempt/watchdog-status.json"
exit "$status"

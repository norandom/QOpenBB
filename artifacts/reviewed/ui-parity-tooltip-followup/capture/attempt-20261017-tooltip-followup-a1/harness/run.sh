#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
export PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers
harness="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
test "${TOOLTIP_HEAVY_GRANTED:-}" = "yes" || exit 79
export CAPTURE_ROOT="$1"
test -d "$CAPTURE_ROOT" || exit 78
node -e 'require("fs").writeFileSync(process.env.CAPTURE_ROOT+"/lifecycle-private.json",JSON.stringify({launchedAt:Date.now(),shellPid:Number(process.argv[1])}))' "$$"
active_pid=""
watchdog_pid=""
stop_owned() {
  target_pid="$1"
  kill -TERM "$target_pid" 2>/dev/null || true
  timeout --signal=TERM --kill-after=1s 3s tail --pid="$target_pid" -f /dev/null 2>/dev/null || true
  kill -KILL "$target_pid" 2>/dev/null || true
  wait "$target_pid" 2>/dev/null || true
}
cleanup() {
  incoming=$?
  trap - EXIT INT TERM
  if [ -n "$active_pid" ]; then stop_owned "$active_pid"; fi
  if [ -n "$watchdog_pid" ]; then stop_owned "$watchdog_pid"; fi
  timeout --signal=TERM --kill-after=1s 50s node "$harness/cleanup.mjs" > "$CAPTURE_ROOT/cleanup.log" 2>&1
  cleanup_code=$?
  printf '{"exitCode":%s}\n' "$cleanup_code" > "$CAPTURE_ROOT/cleanup-status.json"
  if [ "$incoming" = 0 ] && [ "$cleanup_code" != 0 ]; then incoming=$cleanup_code; fi
  printf '{"exitCode":%s}\n' "$incoming" > "$CAPTURE_ROOT/run-status.json"
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
owner_pid=$$
node -e 'setTimeout(()=>{try{process.kill(Number(process.argv[1]),"SIGTERM")}catch{}},840000)' "$owner_pid" &
watchdog_pid=$!
timeout --signal=TERM --kill-after=1s 120s node "$harness/start.mjs" > "$CAPTURE_ROOT/start.log" 2>&1 &
active_pid=$!
wait "$active_pid"
status=$?
active_pid=""
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_ROOT/start-status.json"
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=1s 700s node "$harness/journey.mjs" > "$CAPTURE_ROOT/journey.log" 2>&1 &
active_pid=$!
wait "$active_pid"
status=$?
active_pid=""
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_ROOT/journey-status.json"
exit "$status"

#!/bin/bash
set -u
cd /mnt/d/Source/QOpenBB || exit 1
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
export PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers
capture=artifacts/ui-parity-captions/capture
if [ "${QOPENBB_CAPTIONS_HEAVY_GRANT:-}" != "controller-granted" ]; then
  printf '%s\n' 'Explicit controller heavy-lane grant required.' >&2
  exit 77
fi
if [ "${1:-}" != "--owned-inner" ]; then
  exec timeout --signal=TERM --kill-after=95s 1350s bash "$capture/run.sh" --owned-inner
fi
suffix=$(node -e 'process.stdout.write(require("node:crypto").randomBytes(4).toString("hex"))')
export CAPTURE_RUN="/mnt/d/Source/QOpenBB/$capture/runs/attempt-$(date -u +%Y%m%dT%H%M%SZ)-$suffix"
mkdir -p "$capture/runs" || exit 1
mkdir "$CAPTURE_RUN" || exit 1
cleanup() {
  incoming=$?
  trap - EXIT INT TERM
  timeout --signal=TERM --kill-after=5s 90s node "$capture/cleanup.mjs" > "$CAPTURE_RUN/cleanup.log" 2>&1
  cleanup_code=$?
  printf '{"exitCode":%s}\n' "$cleanup_code" > "$CAPTURE_RUN/cleanup-status.json"
  if [ "$incoming" = 0 ] && [ "$cleanup_code" != 0 ]; then incoming=$cleanup_code; fi
  printf '{"exitCode":%s}\n' "$incoming" > "$CAPTURE_RUN/run-status.json"
  printf 'Caption run receipt: %s\n' "$CAPTURE_RUN/run-status.json"
  exit "$incoming"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
node "$capture/manifest.mjs" > "$CAPTURE_RUN/manifest.log" 2>&1
status=$?
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=5s 180s node "$capture/start.mjs" > "$CAPTURE_RUN/start.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_RUN/start-status.json"
if [ "$status" != 0 ]; then exit "$status"; fi
timeout --signal=TERM --kill-after=90s 905s node "$capture/journey.mjs" > "$CAPTURE_RUN/journey.log" 2>&1
status=$?
printf '{"exitCode":%s}\n' "$status" > "$CAPTURE_RUN/journey-status.json"
exit "$status"

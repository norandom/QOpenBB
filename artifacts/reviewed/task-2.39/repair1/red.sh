#!/bin/bash
set -u
root=/mnt/d/Source/QOpenBB
out=$root/artifacts/task-2.39/repair1
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(cat "$out/stage-path.txt")"
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/gridCapture.test.ts > "$out/red.log" 2>&1
printf '%s\n' "$?" > "$out/red.exit"

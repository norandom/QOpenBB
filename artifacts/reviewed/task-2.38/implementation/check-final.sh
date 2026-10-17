#!/bin/bash
set -u
root=/mnt/d/Source/QOpenBB
out=$root/artifacts/task-2.38/implementation
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(cat "$out/stage-path.txt")"
node --version
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/gridCapture.grid.test.ts > "$out/grid-final.log" 2>&1
printf '%s\n' "$?" > "$out/grid-final.exit"
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit > "$out/tsc-final.log" 2>&1
printf '%s\n' "$?" > "$out/tsc-final.exit"
node node_modules/@biomejs/biome/bin/biome check tests/unit/chart-application/gridCapture.grid.test.ts tests/unit/chart-application/gridCapture.fixtures.json > "$out/biome-final.log" 2>&1
printf '%s\n' "$?" > "$out/biome-final.exit"

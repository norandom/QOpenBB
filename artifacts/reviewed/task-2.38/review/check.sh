#!/bin/bash
set -u
root=/mnt/d/Source/QOpenBB
out=$root/artifacts/task-2.38/review
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
cd /home/mc/qopenbb-work/task238-20261017125037/terminalpro
node --version > "$out/runtime.log"
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/gridCapture.grid.test.ts > "$out/grid.log" 2>&1
printf '%s\n' "$?" > "$out/grid.exit"
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit > "$out/tsc.log" 2>&1
printf '%s\n' "$?" > "$out/tsc.exit"
node node_modules/@biomejs/biome/bin/biome check tests/unit/chart-application/gridCapture.grid.test.ts tests/unit/chart-application/gridCapture.fixtures.json tests/unit/chart-application/tsconfig.json > "$out/biome.log" 2>&1
printf '%s\n' "$?" > "$out/biome.exit"
#!/bin/bash
set -u
root=/mnt/d/Source/QOpenBB
out=$root/artifacts/task-2.39/repair1
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(cat "$out/stage-path.txt")"
node node_modules/@biomejs/biome/bin/biome check --write src/components/General/Table/Chart/application/gridCapture.ts tests/unit/chart-application/gridCapture.test.ts tests/unit/chart-application/gridCapture.grid.test.ts > "$out/format.log" 2>&1
cp src/components/General/Table/Chart/application/gridCapture.ts "$root/vendor/workspace/terminalpro/src/components/General/Table/Chart/application/gridCapture.ts"
cp tests/unit/chart-application/gridCapture.test.ts tests/unit/chart-application/gridCapture.grid.test.ts "$root/vendor/workspace/terminalpro/tests/unit/chart-application/"
for suite in chart-application chart-compatibility; do
node node_modules/vitest/vitest.mjs run --config tests/unit/$suite/vitest.config.mjs > "$out/$suite.log" 2>&1
printf '%s\n' "$?" > "$out/$suite.exit"
node node_modules/typescript/bin/tsc --project tests/unit/$suite/tsconfig.json --noEmit > "$out/$suite-tsc.log" 2>&1
printf '%s\n' "$?" > "$out/$suite-tsc.exit"
done
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application > "$out/biome.log" 2>&1
printf '%s\n' "$?" > "$out/biome.exit"

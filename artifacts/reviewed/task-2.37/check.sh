#!/bin/bash
set -eu
root=/mnt/d/Source/QOpenBB
base=/home/mc/qopenbb-work/task237
stage=$base/terminalpro
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p "$base"
if [ ! -d "$stage" ]; then
  git -C "$root/vendor/workspace" archive HEAD terminalpro | tar -x -C "$base"
  ln -s /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules "$stage/node_modules"
fi
for dir in src/components/General/Table/Chart tests/unit/chart-application tests/unit/chart-compatibility tests/e2e/chart-compatibility; do
  mkdir -p "$stage/$dir"
  cp -a "$root/vendor/workspace/terminalpro/$dir/." "$stage/$dir/"
done
cd "$stage"
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application

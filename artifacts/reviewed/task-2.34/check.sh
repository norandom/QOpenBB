set -eu
root=/mnt/d/Source/QOpenBB
stage=/home/mc/qopenbb-work/task234/terminalpro
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
bash "$root/artifacts/task-2.34/stage.sh"
cd "$stage"
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application/types.ts tests/unit/chart-application
printf 'Application runtime suite not executed: task 2.34 declares compile-only contracts; runtime units start in 2.35/2.36.\n'

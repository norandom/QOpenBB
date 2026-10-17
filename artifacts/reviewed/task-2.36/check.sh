set -eu
root=/mnt/d/Source/QOpenBB
base=/home/mc/qopenbb-work/task236
stage=$base/terminalpro
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p "$base"
if [ ! -d "$stage" ]; then
 git -C "$root/vendor/workspace" archive HEAD terminalpro | tar -x -C "$base"
 ln -s /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules "$stage/node_modules"
fi
for dir in src/components/General/Table/Chart/compatibility src/components/General/Table/Chart/echarts tests/unit/chart-compatibility tests/e2e/chart-compatibility; do
 mkdir -p "$stage/$dir"
 cp -a "$root/vendor/workspace/terminalpro/$dir/." "$stage/$dir/"
done
mkdir -p "$stage/src/components/General/Table/Chart/application" "$stage/tests/unit/chart-application"
for file in src/components/General/Table/Chart/application/types.ts src/components/General/Table/Chart/application/financialFormatting.ts tests/unit/chart-application/financialFormatting.sources.json tests/unit/chart-application/contracts.types.ts tests/unit/chart-application/financialFormatting.test.ts tests/unit/chart-application/tsconfig.json tests/unit/chart-application/vitest.config.mjs; do
 cp "$root/vendor/workspace/terminalpro/$file" "$stage/$file"
done
if [ "${RED_MISSING:-0}" = 1 ]; then
 rm -f "$stage/src/components/General/Table/Chart/application/financialFormatting.ts"
fi
cd "$stage"
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application/financialFormatting.ts tests/unit/chart-application/financialFormatting.test.ts tests/unit/chart-application/financialFormatting.sources.json

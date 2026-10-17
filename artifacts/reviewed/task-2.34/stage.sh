set -eu
root=/mnt/d/Source/QOpenBB
base=/home/mc/qopenbb-work/task234
stage=$base/terminalpro
export PATH="$root/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
mkdir -p "$base"
if [ ! -d "$stage" ]; then
  git -C "$root/vendor/workspace" archive HEAD terminalpro | tar -x -C "$base"
  ln -s /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules "$stage/node_modules"
fi
for dir in src/components/General/Table/Chart tests/unit/chart-compatibility tests/e2e/chart-compatibility tests/unit/chart-application; do
  mkdir -p "$stage/$dir"
  cp -a "$root/vendor/workspace/terminalpro/$dir/." "$stage/$dir/"
done
for file in src/lib/utils/utils.ts src/components/General/Table/AgGridUtils.tsx; do
  cp "$root/vendor/workspace/terminalpro/$file" "$stage/$file"
done
cd "$stage"
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit

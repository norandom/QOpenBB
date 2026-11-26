#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 2 ]]; then
  printf 'Usage: %s PROJECT PRIVATE_ENV_FILE\n' "$0" >&2
  exit 2
fi

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
project=$1
env_file=$2
state=$root/data/modeling
compose=(docker compose --project-directory "$root" --project-name "$project"
  --env-file "$env_file" -f "$root/compose.yaml" -f "$root/deploy/compose.modeling.yaml")

if [[ ! -d $state || -L $root/data || -L $state ]] ||
    [[ $(stat -c '%u:%g:%a' -- "$state") != 10001:10001:700 ]]; then
  printf 'Prepare ./data/modeling with owner 10001:10001 and mode 0700.\n' >&2
  exit 2
fi

# Validate the effective references, including shell overrides to the private env file.
resolved=$("${compose[@]}" config --images)
mapfile -t images <<< "$resolved"
reference='^[^/@[:space:]]+/[^:@[:space:]]+@sha256:[0-9a-f]{64}$'
if [[ ${#images[@]} != 3 ]]; then
  printf 'Expected three candidate image references.\n' >&2
  exit 2
fi
for image in "${images[@]}"; do
  registry=${image%%/*}
  if [[ ! $image =~ $reference ||
        ( $registry != localhost && $registry != *.* && $registry != *:* ) ]]; then
    printf 'Every candidate image must use registry/repository@sha256:<digest>.\n' >&2
    exit 2
  fi
done

"${compose[@]}" pull --policy always
"${compose[@]}" up -d --no-build --pull never --wait --wait-timeout 180

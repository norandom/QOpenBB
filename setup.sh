#!/usr/bin/env bash
set +x
set -euo pipefail
umask 077

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
base=(docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env -f compose.yaml)
full=("${base[@]}" -f deploy/setup/compose.full.yaml)

fail() {
    printf '%s\n' "$1" >&2
    exit 1
}

prepare_env() {
    [[ ! -L .env && ( ! -e .env || -f .env ) ]] || fail '.env must be a regular file.'
    if [[ ! -e .env ]]; then
        (set -o noclobber; : > .env) || fail 'Could not create .env.'
    fi
    [[ ! -L .env.setup && ( ! -e .env.setup || -f .env.setup ) ]] || fail '.env.setup must be a regular file.'
    if [[ ! -e .env.setup ]]; then
        (set -o noclobber; : > .env.setup) || fail 'Could not create .env.setup.'
    fi
    chmod 600 .env.setup

    # Let Compose evaluate dotenv quoting and interpolation without emitting values.
    local flags key marker value additions=''
    local -a keys=(FMP_API_KEY FRED_API_KEY)
    [[ -n ${WORKSPACE_BIND_IP:-} ]] || unset WORKSPACE_BIND_IP
    flags=$(
        unset FMP_API_KEY FRED_API_KEY
        docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env -f - config --images 2>/dev/null <<'YAML'
services:
  fmp:
    image: fmp-${FMP_API_KEY:+set}
  fred:
    image: fred-${FRED_API_KEY:+set}
YAML
    ) || fail 'Could not read .env with Docker Compose. Check its syntax privately.'

    for key in "${keys[@]}"; do
        marker=${key%%_*}
        # An empty exported variable would mask the persisted Compose setting.
        [[ -n ${!key:-} ]] || unset "$key"
        if grep -qx "${marker,,}-set" <<< "$flags"; then
            continue
        fi
        value=${!key:-}
        if [[ -z $value ]]; then
            if ! { printf "%s: " "$key" >/dev/tty && read -r -s value </dev/tty; } 2>/dev/null; then
                fail "Supply $key in .env or the environment when there is no interactive terminal."
            fi
            printf '\n' >&2
        fi
        [[ -n $value && $value != *[[:cntrl:]]* && $value != *\\* ]] ||
            fail "$key must be a nonempty single-line key without backslashes."
        value=${value//\'/\\\'}
        additions+=$'\n'"QOPENBB_SETUP_$key='$value'"
    done
    if [[ -n $additions ]]; then
        printf '%s\n' "$additions" >> .env.setup
    fi
}

show_login() {
    local origin
    origin=$("${full[@]}" exec -T workspace printenv PUBLIC_URL)
    printf '\nOpen QOpenBB at %s\n' "$origin"
    if { : >/dev/tty; } 2>/dev/null; then
        printf 'Initial administrator login (private)\n' >/dev/tty
        "${full[@]}" exec -T workspace credentials | sed '/^[[:space:]]*URL:/d' >/dev/tty
    else
        printf 'To display the initial administrator login in a private terminal, run:\n'
        printf '%s\n' "  docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env -f compose.yaml exec -T workspace credentials | sed '/^[[:space:]]*URL:/d'"
    fi
}

docker info --format '{{.ServerVersion}}' >/dev/null 2>&1 || fail 'Start Docker before running setup.'
docker compose version >/dev/null 2>&1 || fail 'Install the Docker Compose plugin before running setup.'
prepare_env
for directory in data data/workspace data/modeling; do
    [[ ! -L $directory && ( ! -e $directory || -d $directory ) ]] ||
        fail "$directory must be a real directory."
done
# Docker creates missing bind directories, including under an existing root-owned data/.
"${base[@]}" config --quiet
"${base[@]}" pull
"${base[@]}" run --rm --no-deps -T --entrypoint python \
    --volume "$PWD/.env.setup:/run/setup.env" \
    --volume "$PWD/services/modeling/pyproject.toml:/run/model.toml:ro" \
    --volume "$PWD/deploy/setup:/opt/qopenbb-setup:ro" \
    --volume "$PWD/data/modeling:/run/setup-model-state" \
    workspace /opt/qopenbb-setup/modeling_env.py --existing-model-bind
"${full[@]}" config --quiet
"${full[@]}" pull modeling
"${full[@]}" up -d --no-build --wait --wait-timeout 240
model_image=$("${full[@]}" images -q modeling)
data_image=$("${full[@]}" images -q data-api)
workspace_container=$("${full[@]}" ps -q workspace)
model_container=$("${full[@]}" ps -q modeling)
[[ -n $model_image && -n $data_image && -n $workspace_container && -n $model_container ]] ||
    fail 'Could not identify the running services for provisioning.'
"${full[@]}" exec -T \
    -e "QOPENBB_SETUP_MODEL_IMAGE=$model_image" \
    -e "QOPENBB_SETUP_DATA_IMAGE=$data_image" \
    -e "QOPENBB_SETUP_WORKSPACE_CONTAINER=$workspace_container" \
    -e "QOPENBB_SETUP_MODEL_CONTAINER=$model_container" workspace python /opt/qopenbb-setup/provision.py
show_login

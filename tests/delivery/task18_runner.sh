#!/bin/sh
# Disposable verification-runner provisioning, outside the Dagger build definition.
set -eu
mkdir -p /work /output /runner-home /fresh-cache
export HOME=/runner-home
export UV_CACHE_DIR=/fresh-cache/uv
export UV_PYTHON_DOWNLOADS=never
export SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48
cp -R /inputs/project/. /work/
cp -R /inputs/tools /tools
chmod +x /tools/bin/* /tools/safe-chain/bin/safe-chain
export PATH=/tools/safe-chain/shims:/tools/safe-chain/bin:/tools/bin:$PATH
cd /work
apt-get update > /output/apt-update.log 2>&1
git_version=$(apt-cache policy git | sed -n 's/ *Candidate: //p')
ca_version=$(apt-cache policy ca-certificates | sed -n 's/ *Candidate: //p')
printf 'git=%s\nca-certificates=%s\n' "$git_version" "$ca_version" > /output/bootstrap-packages.txt
apt-get install -y --no-install-recommends "git=$git_version" "ca-certificates=$ca_version" > /output/apt-install.log 2>&1
dpkg-query -W > /output/installed-packages.txt
cat /etc/apt/sources.list.d/debian.sources > /output/debian.sources
sha256sum /tools/bin/* /tools/safe-chain/bin/safe-chain > /output/bootstrap-binary-sha256.txt
python --version > /output/versions.txt
git --version >> /output/versions.txt
docker version --format '{{.Client.Version}} {{.Server.Version}}' >> /output/versions.txt
dagger version >> /output/versions.txt
uv --version >> /output/versions.txt
safe-chain setup-ci
export PATH=/tools/safe-chain/shims:/tools/safe-chain/bin:/tools/bin:$PATH
hash -r
uv safe-chain-verify
uv sync --project pipeline --locked --python /usr/local/bin/python
uv sync --project .dagger --locked --python /usr/local/bin/python
pipeline/.venv/bin/python -m qopenbb_ci.image_cli acquire --lock sources.lock.json --destination /work/acquired > /output/acquisition.json
mkdir -p /work/acquired/workspace/terminalpro/synthetic
printf SYNTHETIC_TASK18_SECRET_4e71 > /work/acquired/workspace/terminalpro/synthetic/.env
mkdir -p /work/acquired/workspace/terminalpro/secrets
printf SYNTHETIC_TASK18_SECRET_4e71 > /work/acquired/workspace/terminalpro/secrets/credential
pipeline/.venv/bin/python -m qopenbb_ci.image_cli stage --lock sources.lock.json --policy contracts/sources.json --workspace /work/acquired/workspace --data-api /work/acquired/data_api --destination /work/stage > /output/staging.json
pipeline/.venv/bin/python -m qopenbb_ci.image_cli export --stage /work/stage --tools pipeline/tools.lock.json --lock sources.lock.json --policy contracts/sources.json --sdk-python .dagger/.venv/bin/python --archive /output/linux-image.tar --report /output/linux-export.json
pipeline/.venv/bin/python tests/delivery/task18_inspect.py --stage /work/stage --archive /output/linux-image.tar --output /output/linux-inspection.json
pipeline/.venv/bin/python -m qopenbb_ci.image_cli load --archive /output/linux-image.tar --report /output/linux-load.json
image_id=$(pipeline/.venv/bin/python -c 'import json;print(json.load(open("/output/linux-load.json"))["loaded_image_id"])')
docker run --rm --network=none "$image_id" > /output/linux-smoke.txt
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/delivery/test_image_builds.py -n0 > /output/linux-tests.txt
chmod 644 /output/linux-image.tar

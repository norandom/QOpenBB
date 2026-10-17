#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
export PATH="/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/local/bin:/usr/bin:/bin"
trap 'docker rm -f qopenbb-appearance-contract-close-20261017-stock > artifacts/parity/appearance-contract-close/cleanup.log 2>&1; rm -f artifacts/parity/appearance-contract-close/credential-private.json' EXIT
node artifacts/parity/appearance-contract-close/start.mjs > artifacts/parity/appearance-contract-close/start.log 2>&1
echo $? > artifacts/parity/appearance-contract-close/start-exit.txt
set +e
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node artifacts/parity/appearance-contract-close/journey.mjs > artifacts/parity/appearance-contract-close/journey.log 2>&1
result=$?
echo "$result" > artifacts/parity/appearance-contract-close/journey-exit.txt
exit "$result"

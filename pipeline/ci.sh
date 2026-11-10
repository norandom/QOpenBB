#!/bin/sh
# Portable entry point: dependencies are provisioned outside image builds.
set -eu
cd "$(dirname "$0")/.."
case "${1:-}" in
  check)
    export QOPENBB_RUNTIME_READER="$PWD/verification/runtime-descriptor.ts"
    export QOPENBB_RUNTIME_PYTHON="$PWD/pipeline/.venv/bin/python"
    pipeline/.venv/bin/python -m qopenbb_ci.quality_cli --output artifacts/ci-quality.json
    pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml \
      tests/delivery/test_image_builds.py tests/delivery/test_workspace_image.py \
      tests/delivery/test_data_image.py tests/delivery/test_prototype_compose.py \
      tests/delivery/test_publication.py tests/delivery/test_build_cli.py \
      tests/delivery/test_quality_cli.py tests/delivery/test_alpha_cli.py tests/delivery/test_prototype_workflow.py \
      tests/delivery/test_native_environment.py tests/delivery/test_native_actions.py \
      tests/delivery/test_session_files.py tests/delivery/test_runtime_descriptor.py \
      tests/delivery/test_browser_runtime_reader.py tests/delivery/test_compose_runtime.py \
      tests/delivery/test_compose_lifecycle.py tests/delivery/test_workspace_runtime.py \
      tests/delivery/test_workspace_smoke.py tests/delivery/test_verification.py \
      tests/delivery/test_portable_runtime.py tests/delivery/test_financial_budget.py -n0 -m 'not live'
    ;;
  build)
    shift
    pipeline/.venv/bin/python -m qopenbb_ci.build_cli "$@"
    ;;
  *) echo 'usage: pipeline/ci.sh check | build [build_cli arguments]' >&2; exit 2 ;;
esac

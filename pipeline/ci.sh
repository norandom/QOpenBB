#!/bin/sh
# Portable entry point: dependencies are provisioned outside image builds.
set -eu
cd "$(dirname "$0")/.."
case "${1:-}" in
  check)
    pipeline/.venv/bin/python -m qopenbb_ci.quality_cli --output artifacts/ci-quality.json
    pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml \
      tests/delivery/test_image_builds.py tests/delivery/test_workspace_image.py \
      tests/delivery/test_data_image.py tests/delivery/test_prototype_compose.py \
      tests/delivery/test_publication.py tests/delivery/test_build_cli.py \
      tests/delivery/test_quality_cli.py -n0
    ;;
  build)
    shift
    pipeline/.venv/bin/python -m qopenbb_ci.build_cli "$@"
    ;;
  *) echo 'usage: pipeline/ci.sh check | build [build_cli arguments]' >&2; exit 2 ;;
esac

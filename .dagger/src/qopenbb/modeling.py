"""Build the independent modeling runtime from the locked dependency set."""

import hashlib
import json

import dagger
from dagger import dag

from qopenbb.data_api import SAFE_SHA, SAFE_URL, UV_SHA, UV_URL

RUN_DIR = '/data/modeling'
RUN_USER = '10001:10001'
ENTRYPOINT = [
    'uvicorn', 'qopenbb_data.modeling.service.bootstrap:create_app', '--factory',
    '--host', '0.0.0.0', '--port', '6901', '--no-access-log',
]


def modeling_image(context: dagger.Directory, base: str, inputs: dict[str, str]) -> dagger.Container:
    python = dag.container(platform=dagger.Platform('linux/amd64')).from_(base)
    builder = (python
               .with_file('/tmp/uv.tar.gz', dag.http(UV_URL, checksum='sha256:' + UV_SHA))
               .with_exec(['tar', '-xzf', '/tmp/uv.tar.gz', '-C', '/tmp'])
               .with_exec(['cp', '/tmp/uv-x86_64-unknown-linux-gnu/uv', '/usr/local/bin/uv'])
               .with_file('/usr/local/bin/safe-chain', dag.http(SAFE_URL, checksum='sha256:' + SAFE_SHA),
                          permissions=0o755)
               .with_env_variable('SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS', '48')
               .with_env_variable('UV_PROJECT_ENVIRONMENT', '/opt/venv')
               .with_env_variable('UV_PYTHON_DOWNLOADS', 'never')
               .with_directory('/build/modeling', context.directory('services/modeling'))
               .with_workdir('/build/modeling')
               .with_exec(['safe-chain', 'uv', 'safe-chain-verify'])
               .with_exec(['safe-chain', 'uv', 'sync', '--locked', '--no-dev', '--no-install-project',
                           '--no-build', '--python', '/usr/local/bin/python']))

    manifest = json.dumps(inputs, sort_keys=True) + '\n'
    return (python
            .with_directory('/opt/venv', builder.directory('/opt/venv'))
            .with_directory('/app/qopenbb_data', context.directory('services/data-api/qopenbb_data'))
            .with_exec(['install', '-d', '-m', '0700', '-o', '10001', '-g', '10001', RUN_DIR])
            .with_env_variable('PATH', '/opt/venv/bin:/usr/local/bin:/usr/bin:/bin')
            .with_env_variable('HOME', '/tmp')
            .with_env_variable('PYTHONDONTWRITEBYTECODE', '1')
            .with_env_variable('PYTHONUNBUFFERED', '1')
            .with_env_variable('QOPENBB_MODEL_RUN_DIR', RUN_DIR)
            .with_env_variable('QOPENBB_MODEL_DATA_ORIGIN', 'http://data-api:6900')
            .with_workdir('/app')
            .with_user(RUN_USER)
            .with_exposed_port(6901)
            .with_entrypoint(ENTRYPOINT)
            .with_label('org.qopenbb.service', 'modeling')
            .with_label('org.qopenbb.scope', 'modeling-runtime')
            .with_label('org.qopenbb.runtime-inputs.sha256', hashlib.sha256(manifest.encode()).hexdigest())
            .with_label('org.qopenbb.runtime-lock.sha256', inputs['services/modeling/uv.lock']))

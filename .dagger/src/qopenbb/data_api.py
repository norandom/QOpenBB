"""Build the locked local provider packages; retain only production runtime files."""
import hashlib
import json

import dagger
from dagger import dag

UV_URL = 'https://github.com/astral-sh/uv/releases/download/0.12.5/uv-x86_64-unknown-linux-gnu.tar.gz'
UV_SHA = '68a509da24b06b4223a1c0175fb5eb5bc79342b76cbeff0cfe51ac3f5b17b6b2'
SAFE_URL = 'https://github.com/AikidoSec/safe-chain/releases/download/1.5.25/safe-chain-linuxstatic-x64'
SAFE_SHA = '3462a8395f822b392b7c0808c70116ef90e17a5a1479e604cfc41d57bfbd827c'


async def data_image(context: dagger.Directory, base: str, runtime_inputs: dict,
                     source_revision: str) -> dagger.Container:
    builder = (dag.container(platform=dagger.Platform('linux/amd64')).from_(base)
               .with_file('/tmp/uv.tar.gz', dag.http(UV_URL, checksum='sha256:' + UV_SHA))
               .with_exec(['tar', '-xzf', '/tmp/uv.tar.gz', '-C', '/tmp'])
               .with_exec(['cp', '/tmp/uv-x86_64-unknown-linux-gnu/uv', '/usr/local/bin/uv'])
               .with_file('/usr/local/bin/safe-chain', dag.http(SAFE_URL, checksum='sha256:' + SAFE_SHA), permissions=0o755)
               .with_env_variable('SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS', '48')
               .with_env_variable('UV_PROJECT_ENVIRONMENT', '/opt/venv')
               .with_env_variable('UV_PYTHON_DOWNLOADS', 'never')
               .with_directory('/build/vendor/data-api', context.directory('sources/data_api'))
               .with_directory('/build/services/data-api', context.directory('runtime/services/data-api'))
               .with_workdir('/build/services/data-api')
               .with_exec(['safe-chain', 'uv', 'safe-chain-verify'])
               .with_exec(['safe-chain', 'uv', 'sync', '--locked', '--no-dev', '--no-editable',
                           '--python', '/usr/local/bin/python']))
    runtime_hash = hashlib.sha256((json.dumps(runtime_inputs, sort_keys=True) + '\n').encode()).hexdigest()
    return (dag.container(platform=dagger.Platform('linux/amd64')).from_(base)
            .with_directory('/opt/venv', builder.directory('/opt/venv'))
            .with_directory('/app/qopenbb_data', context.directory('runtime/services/data-api/qopenbb_data'))
            .with_directory('/app/qopenbb_data/catalog', context.directory('runtime/contracts'))
            .with_file('/app/qopenbb_data/provider-coverage.json',
                       context.file('runtime/docs/reference/provider-coverage.json'))
            .with_env_variable('QOPENBB_DATA_SOURCE_REVISION', source_revision)
            .with_env_variable('QOPENBB_DATA_GENERATION_REVISION', source_revision)
            .with_env_variable('QOPENBB_DATA_RUNTIME_SHA256', runtime_hash)
            .with_env_variable('PATH', '/opt/venv/bin:/usr/local/bin:/usr/bin:/bin')
            .with_env_variable('PYTHONDONTWRITEBYTECODE', '1')
            .with_env_variable('PYTHONUNBUFFERED', '1')
            .with_env_variable('HOME', '/tmp')
            .with_workdir('/app').with_user('65532:65532')
            .with_exposed_port(6900)
            .with_entrypoint(['uvicorn', 'qopenbb_data.app:create_app', '--factory', '--host',
                              '0.0.0.0', '--port', '6900', '--no-access-log'])
            .with_label('org.qopenbb.runtime-inputs.sha256', runtime_hash)
            .with_label('org.qopenbb.build-assets', json.dumps([
                {'url': UV_URL, 'digest': UV_SHA}, {'url': SAFE_URL, 'digest': SAFE_SHA}], sort_keys=True)))

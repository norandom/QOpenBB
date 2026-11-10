"""Linux runtime inputs, independent of Windows tool metadata and pipe discovery."""
from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import urlsplit

from .container_command import resolve_executable
from .native_environment import (NativeEnvironment, checked_path, child_environment,
                                 resolve_environment as resolve_native, validate_output)


@dataclass(frozen=True)
class LinuxEnvironment(NativeEnvironment):
    storage: Path


def browser_environment(repository, python):
    return {'QOPENBB_RUNTIME_READER': str(repository / 'verification/runtime-descriptor.ts'),
            'QOPENBB_RUNTIME_PYTHON': str(python),
            'PYTHONPATH': str(repository / 'pipeline')}


def output_options(config):
    return {'storage': config.storage} if isinstance(config, LinuxEnvironment) else {}


def linux_endpoint(source, executable):
    if source.get('DOCKER_CONTEXT') or source.get('CONTAINER_CONNECTION'):
        raise ValueError('Portable runtime requires an explicit daemon endpoint, not a named context')
    docker = source.get('DOCKER_HOST')
    container = source.get('CONTAINER_HOST')
    endpoint = container if 'podman' in executable.stem.lower() else docker
    if not endpoint or (container and docker and container != docker):
        raise ValueError('Portable runtime requires one explicit matching daemon endpoint')
    parsed = urlsplit(endpoint)
    if parsed.scheme not in {'unix', 'tcp', 'ssh'} or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Unsupported portable daemon endpoint')
    if parsed.scheme == 'unix':
        if parsed.netloc or not parsed.path.startswith('/') or parsed.path == '/':
            raise ValueError('Explicit Unix daemon socket required')
    elif not parsed.hostname:
        raise ValueError('Explicit daemon hostname required')
    return endpoint


def resolve_linux(repository, source=None):
    source = dict(os.environ if source is None else source)
    repository = checked_path(repository)
    if not (repository / 'pipeline/tools.lock.json').is_file():
        raise ValueError(f'Expected QOpenBB repository: {repository}')
    if not source.get('QOPENBB_STORAGE_ROOT'):
        raise ValueError('Provide QOPENBB_STORAGE_ROOT on the Linux filesystem')
    if not Path(source['QOPENBB_STORAGE_ROOT']).is_absolute():
        raise ValueError('Provide an absolute Linux storage root')
    requested = PurePosixPath(source['QOPENBB_STORAGE_ROOT'])
    if any(requested.is_relative_to(root) for root in ('/mnt/c', '/mnt/d')):
        raise ValueError('Linux outputs and caches must remain on the Linux filesystem')
    storage = checked_path(Path(source['QOPENBB_STORAGE_ROOT']))
    artifacts = validate_output(Path(source.get('QOPENBB_ARTIFACTS', str(storage / 'QOpenBB'))), storage)
    executable = resolve_executable(source.get('QOPENBB_CONTAINER_CLI', 'docker'))
    source['QOPENBB_CONTAINER_CLI'] = str(executable)
    source['DOCKER_HOST'] = linux_endpoint(source, executable)
    environment = child_environment(artifacts, source, storage=storage)
    # A venv's symlink invocation selects its site-packages; its target does not.
    python = Path(sys.executable).absolute()
    if not python.is_file():
        raise ValueError('Current Python interpreter is unavailable')
    environment.update(browser_environment(repository, python))
    return LinuxEnvironment(repository, artifacts, {'python': python, 'container': executable}, environment, storage)


def resolve_environment(repository):
    if sys.platform == 'win32':
        return resolve_native(repository)
    if sys.platform != 'linux':
        raise ValueError('Runtime supported only on Windows and Linux')
    return resolve_linux(repository)

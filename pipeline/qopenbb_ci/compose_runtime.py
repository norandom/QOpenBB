"""Owned native Compose startup; private recovery facts precede resource creation."""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import socket
from uuid import uuid4

from .container_command import compose_command, container_command
from .native_environment import NativeEnvironment, run_command, validate_output
from . import session_files, state_files
from .portable_runtime import output_options
from .runtime_descriptor import RuntimeDescriptor, replace_private
from .compose_checks import validate_config, checked_container, checked_network


@dataclass(frozen=True)
class StartRequest:
    config: NativeEnvironment
    session_path: Path
    workspace_image: str
    data_image: str
    port: int | None = None


class ComposeRuntime:
    def __init__(self, config, path):
        self.config, self.path = config, Path(path)
        self.descriptor = None
        self.stage = 'configuration'
        self.failure_code = 'runtime_check_rejected'

    def command(self, arguments, *, compose=False, timeout=60):
        command = compose_command if compose else container_command
        result = run_command(command(arguments, self.config.environment), self.config.repository,
                             self.config.environment, timeout)
        if result.returncode:
            self.failure_code = 'subprocess_exit'
            if self.descriptor is not None:
                session_files.replace_private(self.path.parent / 'command-failure.txt', result.stderr.encode())
            raise ValueError(f'Owned runtime command failed (exit {result.returncode})')
        return result.stdout

    def invocation(self, *arguments):
        descriptor = self.descriptor
        args = ['--project-name', descriptor.project, '--project-directory', descriptor.compose.project_directory,
                '--env-file', descriptor.compose.environment_file.path]
        for item in descriptor.compose.files:
            args.extend(['--file', item.path])
        return [*args, *arguments]

    def save(self, **updates):
        raw = self.descriptor.model_dump(mode='json')
        raw.update(updates)
        self.descriptor = RuntimeDescriptor.model_validate(raw)
        replace_private(self.path, self.descriptor)

    def discover(self):
        descriptor = self.descriptor
        containers = {}
        for service in ('workspace', 'data-api'):
            ids = self.command(self.invocation('ps', '--all', '--quiet', service), compose=True).split()
            if len(ids) > 1:
                raise ValueError('Unexpected session container count')
            if ids:
                inspected = json.loads(self.command(['inspect', ids[0]]))[0]
                containers[service] = checked_container(inspected, service, descriptor.project,
                                                        descriptor.session_id, descriptor.images[service])
        ids = self.command(['network', 'ls', '--filter', 'label=com.docker.compose.project='+descriptor.project,
                            '--format', '{{.ID}}']).split()
        networks = []
        for identity in ids:
            network = json.loads(self.command(['network', 'inspect', identity]))[0]
            networks.append(checked_network(network, descriptor.project, descriptor.session_id).model_dump())
        self.save(resources={'containers': {k: v.model_dump() for k, v in containers.items()}, 'networks': networks},
                  container=containers['workspace'].id if 'workspace' in containers else None)

    def verify_configuration(self):
        try:
            for item in self.descriptor.compose.files:
                if hashed(Path(item.path))['sha256'] != item.sha256:
                    raise ValueError('changed')
            item = self.descriptor.compose.environment_file
            if hashlib.sha256(session_files.read_private(Path(item.path))).hexdigest() != item.sha256:
                raise ValueError('changed')
        except (OSError, ValueError, AttributeError):
            raise ValueError('Runtime configuration identity mismatch') from None

    def record_failure(self, stage, code):
        stages = {'configuration', 'compose_up', 'resource_discovery', 'service_health',
                  'origin_binding', 'bind_mapping', 'full_configuration', 'disposable_login'}
        diagnostic = {'stage': stage if stage in stages else 'resource_discovery',
                      'code': code if code in {'subprocess_exit', 'runtime_check_rejected'} else 'runtime_check_rejected'}
        session_files.replace_private(self.path.parent / 'failure.json', json.dumps(diagnostic).encode())
        return diagnostic

    def begin(self):
        with state_files.PrivateDirectory.open(self.descriptor.state.host_path) as directory:
            self.state_directory = directory
            try:
                return self._begin()
            finally:
                self.state_directory = None

    def _begin(self):
        self.verify_configuration()
        self.save(phase='starting')
        self.failure_code = 'runtime_check_rejected'
        try:
            self.stage = 'compose_up'
            self.state_directory.verify()
            self.command(self.invocation('up', '-d', '--no-build', '--pull', 'never'), compose=True, timeout=240)
            self.stage = 'resource_discovery'
            self.discover()
            from .compose_readiness import ready
            ready(self)
            self.save(phase='ready')
            return self.descriptor
        except BaseException:
            diagnostic = self.record_failure(self.stage, self.failure_code)
            try:
                self.discover()
            except Exception:
                pass
            self.save(phase='failed')
            raise ValueError(f"Owned Compose startup failed at {diagnostic['stage']} ({diagnostic['code']}); protected recovery descriptor retained") from None


def hashed(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def image_identity(runtime, reference):
    inspected = json.loads(runtime.command(['image', 'inspect', reference]))[0]
    digest = 'sha256:' + inspected['Id'].removeprefix('sha256:')
    manifests = inspected.get('RepoDigests') or []
    return digest, {'config_digest': digest, 'manifest_digest': manifests[0].split('@')[-1] if manifests else None}


def reserve_port(port):
    if port is not None and (type(port) is not int or not 0 < port < 65536):
        raise ValueError('Invalid loopback port')
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', port or 0))
        return reservation.getsockname()[1]


def prepare(request):
    config = request.config
    path = validate_output(Path(request.session_path), **output_options(config))
    if path.exists() or path.parent.exists():
        raise ValueError('A new private session directory is required')
    runtime = ComposeRuntime(config, path)
    images, metadata = {}, {}
    for service, image in [('workspace', request.workspace_image), ('data-api', request.data_image)]:
        images[service], metadata[service] = image_identity(runtime, image)
    info = json.loads(runtime.command(['info', '--format', 'json']))
    identity = info.get('ID') or info.get('host', {}).get('hostname')
    endpoint = config.environment.get('CONTAINER_HOST') or config.environment.get('DOCKER_HOST')
    if not identity or not endpoint:
        raise ValueError('Explicit daemon connection and identity required')
    session = uuid4().hex
    port = reserve_port(request.port)
    with session_files.create_session(path.parent) as directory:
        directory.create_file('command-failure.txt', b'')
        directory.create_file('failure.json', b'{}')
        state = path.parent / 'state'
        with state_files.create_state(state) as state_directory:
            state_directory.create_file('qopenbb-sentinel', session.encode())
        files = [config.repository / 'compose.yaml', config.repository / 'pipeline/compose.runtime.yaml']
        environment = {'WORKSPACE_IMAGE': images['workspace'], 'DATA_API_IMAGE': images['data-api'],
                       'PUBLIC_URL': f'http://127.0.0.1:{port}', 'OPENBB_ADMIN_EMAIL': f'browser-{session}@example.com',
                       'FMP_API_KEY': 'offline-readiness-not-a-provider-key', 'FRED_API_KEY': 'offline-readiness-not-a-provider-key',
                       'QOPENBB_STATE': state.as_posix(), 'QOPENBB_PORT': str(port), 'QOPENBB_SESSION': session}
        env_path = path.parent / 'runtime.env'
        directory.create_file(env_path.name, ''.join(f'{k}={v}\n' for k, v in environment.items()).encode())
        runtime.descriptor = RuntimeDescriptor.model_validate(dict(schema_version=1, session_id=session,
            backend='compose', phase='prepared', name='qopenbb-browser-'+session, project='qopenbb-browser-'+session,
            origin=environment['PUBLIC_URL'], container=None, credentials=None, images=images, image_metadata=metadata,
            packaged_image_only=True, source_overlay=None, release_image_verified=False,
            connection={'endpoint': endpoint, 'identity': identity}, resources={'containers': {}, 'networks': []},
            state={'host_path': str(state), 'daemon_path': None, 'mount_identity': None, 'verified': False},
            compose={'project_directory': str(config.repository), 'files': [hashed(f) for f in files],
                     'environment_file': {'path': str(env_path), 'sha256': hashlib.sha256(session_files.read_private(env_path)).hexdigest()}}))
        directory.create_file(path.name, runtime.descriptor.model_dump_json().encode())
    effective = json.loads(runtime.command(runtime.invocation('config', '--format', 'json'), compose=True))
    validate_config(effective, images, state, port)
    return runtime


def start(request: StartRequest) -> RuntimeDescriptor:
    return prepare(request).begin()

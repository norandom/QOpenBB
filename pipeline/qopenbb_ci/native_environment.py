"""Native preflight and child-process boundaries; no workstation configuration writes."""
import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import urlsplit
from collections.abc import Mapping, Sequence
from .container_command import compose_command, container_command, resolve_executable

ARTIFACTS = Path('D:/BuildArtifacts/QOpenBB')
CACHE_KEYS = ('UV_CACHE_DIR', 'CARGO_HOME', 'CARGO_TARGET_DIR', 'npm_config_cache',
              'PIP_CACHE_DIR', 'PYTHONPYCACHEPREFIX', 'BUN_INSTALL_CACHE_DIR', 'PNPM_HOME', 'PNPM_STORE_DIR',
              'npm_config_store_dir', 'TEMP', 'TMP', 'TMPDIR', 'PLAYWRIGHT_BROWSERS_PATH')
SYSTEM_KEYS = ('SystemRoot', 'WINDIR', 'COMSPEC', 'PATHEXT', 'PATH', 'SYSTEMDRIVE',
               'NUMBER_OF_PROCESSORS', 'PROCESSOR_ARCHITECTURE')
CONNECTION_KEYS = ('DOCKER_HOST', 'DOCKER_CONTEXT', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH',
                   'CONTAINER_HOST', 'CONTAINER_CONNECTION', 'CONTAINER_SSHKEY',
                   'QOPENBB_CONTAINER_CLI', 'PODMAN_COMPOSE_PROVIDER')


def checked_path(path: Path) -> Path:
    path = path.absolute()
    if path == Path(path.anchor):
        raise ValueError(f'Drive/filesystem roots are forbidden: {path}')
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            attrs = part.lstat()
            if part.is_symlink() or getattr(attrs, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError(f'Reparse or symbolic-link paths are forbidden: {part}')
    return path.resolve()


def validate_output(path: Path, storage: Path | None = None) -> Path:
    resolved = checked_path(path)
    if os.name != 'nt' and storage is None:
        raise ValueError('Provide an explicit POSIX storage root on the Linux filesystem')
    allowed = checked_path(Path('D:/BuildArtifacts') if os.name == 'nt' else storage)
    if os.name != 'nt' and (resolved.is_relative_to('/mnt/c') or resolved.is_relative_to('/mnt/d')):
        raise ValueError('Linux outputs and caches must remain on the Linux filesystem')
    if resolved == allowed or not resolved.is_relative_to(allowed):
        raise ValueError(f'Output/cache path must be project-specific beneath {allowed}: {path}')
    return resolved


def child_environment(artifacts: Path, source: Mapping[str, str] | None = None, *, storage: Path | None = None) -> dict[str, str]:
    source = os.environ if source is None else source
    artifacts = validate_output(artifacts, storage)
    keys = (*SYSTEM_KEYS, *CONNECTION_KEYS, *CACHE_KEYS)
    env = {key: value for key, value in source.items() if key.upper() in {item.upper() for item in keys}}
    for key, value in env.items():
        if key.upper() in {item.upper() for item in CACHE_KEYS}:
            validate_output(Path(value), storage)
    home = artifacts / 'home'
    env.update({'HOME': str(home), 'USERPROFILE': str(home),
                'XDG_CONFIG_HOME': str(home / 'config'), 'DOCKER_CONFIG': str(home / 'docker'),
                'FORCE_DARK_MODE': '1', 'PYTHONDONTWRITEBYTECODE': '1'})
    return env


def run_command(argv: Sequence[str], repository: Path, environment: Mapping[str, str], timeout: int = 60) -> subprocess.CompletedProcess:
    cwd = checked_path(repository)
    return subprocess.run(list(argv), cwd=cwd, env=dict(environment), shell=False,
                          capture_output=True, text=True, timeout=timeout,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)


@dataclass(frozen=True)
class NativeEnvironment:
    repository: Path
    artifacts: Path
    tools: dict[str, Path]
    environment: dict[str, str]


def selected_docker_context(repository: Path, source: dict[str, str], executable: Path) -> dict[str, str]:
    if not source.get('DOCKER_CONTEXT') and source.get('DOCKER_HOST'):
        return source
    keys = (*SYSTEM_KEYS, *CONNECTION_KEYS, 'HOME', 'USERPROFILE', 'DOCKER_CONFIG')
    probe_env = {key: value for key, value in source.items() if key.upper() in {item.upper() for item in keys}}
    name = source.get('DOCKER_CONTEXT')
    if not name:
        current = run_command([str(executable), 'context', 'show'], repository, probe_env)
        if current.returncode or not current.stdout.strip():
            raise ValueError('Cannot resolve the effective Docker context')
        name = current.stdout.strip()
    probe = run_command([str(executable), 'context', 'inspect', name], repository, probe_env)
    if probe.returncode:
        raise ValueError('Cannot inspect selected Docker context')
    context = json.loads(probe.stdout)[0]
    endpoint = context['Endpoints']['docker']
    source['DOCKER_HOST'] = endpoint['Host']
    source.pop('DOCKER_CONTEXT', None)
    if context.get('TLSMaterial', {}).get('docker'):
        source['DOCKER_CERT_PATH'] = str(Path(context['Storage']['TLSPath']) / 'docker')
        source['DOCKER_TLS_VERIFY'] = '' if endpoint.get('SkipTLSVerify') else '1'
    return source


def podman_compose_endpoint(repository: Path, source: dict[str, str], executable: Path,
                            selected: dict, probe_env: dict[str, str]) -> dict[str, str]:
    """Map only the selected machine's active rootful/rootless socket to its pipe."""
    machine_name = selected['Name'].removesuffix('-root') if urlsplit(selected['URI']).username == 'root' else selected['Name']
    probe = run_command([str(executable), 'machine', 'inspect', machine_name], repository, probe_env)
    if probe.returncode:
        raise ValueError('Cannot inspect a matching native Podman pipe')
    endpoint = urlsplit(selected['URI'])
    matches = []
    for machine in json.loads(probe.stdout):
        ssh = machine.get('SSHConfig', {})
        rootful = machine.get('Rootful') is True
        name = machine.get('Name', '') + ('-root' if rootful else '')
        socket = endpoint.path == '/run/podman/podman.sock' if rootful else bool(re.fullmatch(r'/run/user/\d+/podman/podman.sock', endpoint.path))
        pipe = machine.get('ConnectionInfo', {}).get('PodmanPipe', {}).get('Path', '')
        if (selected.get('IsMachine') and selected['Name'] == name and machine.get('State') == 'running'
                and endpoint.scheme == 'ssh' and endpoint.hostname in ('127.0.0.1', 'localhost', '::1')
                and endpoint.port == ssh.get('Port') and socket
                and endpoint.username == ('root' if rootful else ssh.get('RemoteUsername'))
                and Path(selected['Identity']).resolve() == Path(ssh.get('IdentityPath', '')).resolve()
                and pipe.startswith('\\\\.\\pipe\\') and len(pipe) > len('\\\\.\\pipe\\')):
            matches.append('npipe://' + pipe.replace('\\', '/'))
    if len(matches) != 1:
        raise ValueError('Selected connection has no unambiguous matching native Podman pipe')
    source['DOCKER_HOST'] = matches[0]
    for key in ('DOCKER_CONTEXT', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH'):
        source.pop(key, None)
    return source


def selected_connection(repository: Path, source: Mapping[str, str]) -> dict[str, str]:
    """Read the operator-selected Podman connection before isolating build homes."""
    result = dict(source)
    executable = resolve_executable(source['QOPENBB_CONTAINER_CLI'])
    if 'podman' not in executable.stem.lower():
        return selected_docker_context(repository, result, executable)
    keys = (*SYSTEM_KEYS, *CONNECTION_KEYS, 'HOME', 'USERPROFILE', 'APPDATA', 'LOCALAPPDATA')
    probe_env = {key: value for key, value in source.items() if key.upper() in {item.upper() for item in keys}}
    probe = run_command([str(executable), 'system', 'connection', 'list', '--format', 'json'], repository, probe_env)
    if probe.returncode:
        raise ValueError('Cannot inspect selected Podman connection')
    connections = json.loads(probe.stdout)
    name = source.get('CONTAINER_CONNECTION')
    host = source.get('CONTAINER_HOST')
    selected = ([item for item in connections if item['URI'] == host] if host else
                [item for item in connections if item['Name'] == name] if name else
                [item for item in connections if item['Default']])
    if len(selected) != 1:
        raise ValueError('Selected Podman connection is missing or ambiguous')
    result.pop('CONTAINER_CONNECTION', None)
    result['CONTAINER_HOST'] = selected[0]['URI']
    identity = source.get('CONTAINER_SSHKEY', selected[0]['Identity'])
    if Path(identity).resolve() != Path(selected[0]['Identity']).resolve():
        raise ValueError('Selected Podman identity does not match its registered connection')
    result['CONTAINER_SSHKEY'] = identity
    return podman_compose_endpoint(repository, result, executable, selected[0], probe_env)


def resolve_environment(repository: Path, artifacts: Path = ARTIFACTS, tools_file: Path | None = None) -> NativeEnvironment:
    if os.name != 'nt':
        raise ValueError('Native tool metadata preflight is Windows-only; use portable Linux CI commands')
    repository = checked_path(repository)
    if not repository.is_dir() or not (repository / 'pipeline/tools.lock.json').is_file():
        raise ValueError(f'Expected QOpenBB repository: {repository}')
    artifacts = validate_output(artifacts)
    metadata = tools_file or ARTIFACTS / 'native-foundation/resolved-tools.json'
    data = json.loads(metadata.read_text(encoding='utf-8-sig'))
    names = ('python', 'node', 'uv', 'pnpm', 'safe_chain', 'dagger_cli', 'podman', 'compose')
    tools = {name: resolve_executable(data[name]['path']) for name in names}
    source = dict(os.environ)
    source.setdefault('QOPENBB_CONTAINER_CLI', str(tools['podman']))
    source.setdefault('PODMAN_COMPOSE_PROVIDER', str(tools['compose']))
    env = child_environment(artifacts, selected_connection(repository, source))
    resolve_executable(env['QOPENBB_CONTAINER_CLI'])
    resolve_executable(env['PODMAN_COMPOSE_PROVIDER'])
    return NativeEnvironment(repository, artifacts, tools, env)


def doctor(config: NativeEnvironment) -> dict:
    lock = json.loads((config.repository / 'pipeline/tools.lock.json').read_text())['tools']
    versions = {}
    for name, tool in config.tools.items():
        result = run_command([str(tool), 'version' if name == 'dagger_cli' else '--version'], config.repository, config.environment)
        expected = lock.get(name, {}).get('version')
        if result.returncode or (expected and not re.search(r'(?<![\d.])' + re.escape(expected) + r'(?![\d.])', result.stdout + result.stderr)):
            raise ValueError(f'{name} version preflight failed; required {expected or "usable executable"}')
        observed = re.search(r'\d+\.\d+\.\d+', result.stdout + result.stderr)
        versions[name] = {'path': str(tool), 'version': observed.group() if observed else expected}
    connection = run_command(container_command(['info', '--format', 'json'], config.environment), config.repository, config.environment)
    if connection.returncode:
        raise ValueError(f'Selected container daemon is unavailable (exit {connection.returncode})')
    daemon = json.loads(connection.stdout)
    compose = run_command(compose_command(['version', '--short'], config.environment), config.repository, config.environment)
    if compose.returncode:
        raise ValueError(f'Explicit Compose provider is unavailable (exit {compose.returncode})')
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', compose.stdout)
    if not match or tuple(map(int, match.groups())) < (2, 24, 4):
        raise ValueError('Compose >= 2.24.4 is required for explicit override semantics')
    access = run_command(compose_command(['ls', '--format', 'json'], config.environment), config.repository, config.environment)
    if access.returncode:
        raise ValueError(f'Compose provider cannot access selected daemon (exit {access.returncode})')
    if not isinstance(json.loads(access.stdout), list):
        raise ValueError('Compose provider returned invalid daemon access evidence')
    return {'status': 'ready', 'repository': str(config.repository), 'artifacts': str(config.artifacts),
            'tools': versions, 'compose_version': compose.stdout.strip(),
            'connection': {'endpoint': config.environment.get('CONTAINER_HOST') or config.environment.get('DOCKER_HOST'),
                           'compose_endpoint': config.environment.get('DOCKER_HOST'),
                           'daemon_id': daemon.get('ID') or daemon.get('host', {}).get('hostname')},
            'scope': 'Native preflight only; build/runtime/browser acceptance remains separate'}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='QOpenBB native workflow')
    parser.add_argument('--action', choices=('doctor', 'build', 'start', 'verify', 'recreate', 'stop'), required=True)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--artifacts', type=Path, default=ARTIFACTS)
    parser.add_argument('--tools-file', type=Path)
    parser.add_argument('--session-path', type=Path)
    parser.add_argument('--workspace-image')
    parser.add_argument('--data-image')
    parser.add_argument('--build-selection', choices=('foundation', 'workspace', 'data-api'))
    args = parser.parse_args(argv)
    allowed = {'doctor': (), 'build': ('build_selection',), 'start': ('session_path', 'workspace_image', 'data_image'),
               'verify': ('session_path',), 'recreate': ('session_path',), 'stop': ('session_path',)}
    for field in ('session_path', 'workspace_image', 'data_image', 'build_selection'):
        if getattr(args, field) is not None and field not in allowed[args.action]:
            parser.error(f'--{field.replace("_", "-")} is irrelevant to {args.action}')
    try:
        config = resolve_environment(args.repository, args.artifacts, args.tools_file)
        if args.action != 'doctor':
            raise ValueError(f'{args.action} is unavailable until its reviewed consumer is integrated (task 11.1)')
        print(json.dumps(doctor(config), indent=2))
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f'Native preflight failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

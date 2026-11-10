"""Fail-closed lifecycle operations on checked, recorded Compose ownership."""
import json
import hashlib
from pathlib import Path

from . import session_files, state_files
from .portable_runtime import output_options
from .compose_checks import checked_container, checked_network
from .compose_runtime import ComposeRuntime
from .native_environment import validate_output
from .runtime_descriptor import read_private, RuntimeDescriptor
from .compose_intent import recreation_intent, create_intent, require_intent, remove_intent


def load(config, path):
    runtime = ComposeRuntime(config, validate_output(Path(path), **output_options(config)))
    runtime.descriptor = read_private(runtime.path)
    descriptor = runtime.descriptor
    endpoint = config.environment.get('CONTAINER_HOST') or config.environment.get('DOCKER_HOST')
    info = json.loads(runtime.command(['info', '--format', 'json']))
    identity = info.get('ID') or info.get('host', {}).get('hostname')
    if endpoint != descriptor.connection.endpoint or identity != descriptor.connection.identity:
        raise ValueError('Runtime daemon identity mismatch')
    runtime.verify_configuration()
    state = Path(descriptor.state.host_path)
    if state != runtime.path.parent / 'state':
        raise ValueError('Runtime state path mismatch')
    if descriptor.phase == 'stopped' and not state.exists():
        return runtime
    if state_files.read_private(state / 'qopenbb-sentinel').decode() != descriptor.session_id:
        raise ValueError('Runtime state ownership mismatch')
    return runtime


def inventory(runtime):
    """List globally, then inspect only exact IDs; missing resources are repeatable."""
    descriptor = runtime.descriptor
    existing = set(runtime.command(['ps', '--all', '--no-trunc', '--quiet']).split())
    containers = {}
    for service, resource in descriptor.resources.containers.items():
        if resource.id in existing:
            observed = json.loads(runtime.command(['inspect', resource.id]))[0]
            checked = checked_container(observed, service, descriptor.project, descriptor.session_id,
                                        descriptor.images[service])
            if checked.id != resource.id or checked.labels != resource.labels:
                raise ValueError('Recorded runtime container identity changed')
            containers[service] = observed
    if containers.get('data-api', {}).get('Mounts'):
        raise ValueError('Unexpected data API mount')
    network_ids = set(runtime.command(['network', 'ls', '--no-trunc', '--format', '{{.ID}}']).split())
    networks = []
    for resource in descriptor.resources.networks:
        if resource.id in network_ids:
            observed = json.loads(runtime.command(['network', 'inspect', resource.id]))[0]
            checked = checked_network(observed, descriptor.project, descriptor.session_id)
            if checked.id != resource.id or checked.labels != resource.labels:
                raise ValueError('Recorded runtime network identity changed')
            networks.append(checked.id)
    project_ids = set(runtime.command(['ps', '--all', '--no-trunc', '--quiet', '--filter',
                        'label=com.docker.compose.project='+descriptor.project]).split())
    project_networks = set(runtime.command(['network', 'ls', '--no-trunc', '--format', '{{.ID}}', '--filter',
                            'label=com.docker.compose.project='+descriptor.project]).split())
    if project_networks - {item.id for item in descriptor.resources.networks}:
        raise ValueError('Unrecorded replacement network refused')
    if project_ids - {item.id for item in descriptor.resources.containers.values()}:
        raise ValueError('Unrecorded replacement resources refused')
    verify_mount(runtime, containers.get('workspace'))
    return containers, networks


def verify_mount(runtime, workspace):
    if workspace is None:
        return
    descriptor = runtime.descriptor
    mounts = workspace.get('Mounts', [])
    if (len(mounts) != 1 or mounts[0].get('Type') != 'bind'
            or mounts[0].get('Destination') != '/data' or mounts[0].get('RW') is not True):
        raise ValueError('Runtime mount identity mismatch')
    if descriptor.state.verified:
        source = mounts[0].get('Source')
        identity = hashlib.sha256(json.dumps({'source': source, 'destination': '/data',
            'type': 'bind', 'sentinel': descriptor.session_id}, sort_keys=True).encode()).hexdigest()
        if source != descriptor.state.daemon_path or identity != descriptor.state.mount_identity:
            raise ValueError('Runtime mount source changed')
    if not descriptor.state.verified:
        if not workspace.get('State', {}).get('Running'):
            raise ValueError('Cannot verify interrupted runtime bind')
        from .compose_readiness import verify_mapping
        verify_mapping(runtime, workspace)


def recover(runtime):
    """Only unrecorded partial startup may adopt resources under both random labels."""
    replacing = runtime.descriptor.phase == 'recreating'
    if replacing:
        require_intent(runtime)
    if replacing or runtime.descriptor.phase in {'prepared', 'starting', 'failed'}:
        recorded = runtime.descriptor.resources
        candidate = rediscover(runtime)
        discovered = candidate.resources
        for service, resource in recorded.containers.items():
            if not replacing and service in discovered.containers and discovered.containers[service].id != resource.id:
                raise ValueError('Replacement runtime container refused')
        old_networks = {item.id for item in recorded.networks}
        if old_networks and {item.id for item in discovered.networks} - old_networks:
            raise ValueError('Replacement runtime network refused')
        runtime.descriptor = validate_candidate(runtime, candidate)
        runtime.save(phase='failed' if replacing else runtime.descriptor.phase)


def remove_resources(runtime, containers, networks):
    # Validate the entire set before the first removal; never remove by name.
    for observed in containers.values():
        runtime.command(['rm', '--force', observed['Id']])
    for identity in networks:
        runtime.command(['network', 'rm', identity])


def status(config, path):
    runtime = load(config, path)
    containers, networks = inventory(runtime)
    return {'phase': runtime.descriptor.phase, 'containers': len(containers), 'networks': len(networks)}


def stop(config, path, remove_state=False):
    runtime = load(config, path)
    recover(runtime)
    containers, networks = inventory(runtime)
    remove_resources(runtime, containers, networks)
    runtime.save(phase='stopped')
    remove_intent(runtime)
    if remove_state:
        remove_state_files(runtime)
    return {'phase': 'stopped', 'state_removed': remove_state}


def recreate(config, path):
    runtime = load(config, path)
    if runtime.descriptor.phase != 'ready':
        raise ValueError('Recreation requires a ready runtime')
    containers, networks = inventory(runtime)
    if set(containers) != {'workspace', 'data-api'} or not networks:
        raise ValueError('Recreation requires the complete recorded runtime')
    create_intent(runtime)
    runtime.save(phase='recreating')
    persist = runtime.save
    runtime.save = lambda **updates: memory_update(runtime, updates)
    try:
        remove_resources(runtime, containers, [])
        with state_files.PrivateDirectory.open(runtime.descriptor.state.host_path) as directory:
            directory.verify()
            runtime.command(runtime.invocation('up', '-d', '--no-build', '--pull', 'never'), compose=True, timeout=240)
            runtime.descriptor = rediscover(runtime)
            from .compose_readiness import ready
            ready(runtime)
        runtime.save = persist
        runtime.save(phase='ready')
        remove_intent(runtime)
        return runtime.descriptor
    except BaseException:
        runtime.save = persist
        try:
            runtime.discover()
        except Exception:
            pass
        runtime.save(phase='failed')
        raise ValueError('Owned recreation failed; protected recovery descriptor retained') from None


def rediscover(runtime):
    original = runtime.save
    descriptor = runtime.descriptor
    runtime.save = lambda **updates: memory_update(runtime, updates)
    try:
        runtime.discover()
        return runtime.descriptor
    finally:
        runtime.save = original
        runtime.descriptor = descriptor


def remove_state_files(runtime):
    state = Path(runtime.descriptor.state.host_path)
    if not state.exists():
        return
    with state_files.PrivateDirectory.open_for_removal(state) as directory:
        names = [item.name for item in state.iterdir()]
        # Preflight every entry before deleting any. Nested or container-owned
        # objects require a separately reviewed removal facility.
        for name in names:
            try:
                with directory.file_handle(name):
                    pass
            except OSError:
                raise ValueError('State retained: nonprivate or nested entries require owner cleanup') from None
        for name in names:
            directory.remove_file(name)
        directory.remove_empty()


def memory_update(runtime, updates):
    raw = runtime.descriptor.model_dump(mode='json')
    raw.update(updates)
    runtime.descriptor = RuntimeDescriptor.model_validate(raw)


def validate_candidate(runtime, candidate):
    descriptor, persist = runtime.descriptor, runtime.save
    runtime.descriptor = candidate
    runtime.save = lambda **updates: memory_update(runtime, updates)
    try:
        inventory(runtime)
        return runtime.descriptor
    finally:
        runtime.descriptor, runtime.save = descriptor, persist

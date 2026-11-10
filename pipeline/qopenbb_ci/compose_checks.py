"""Pure isolation checks for generated Compose and inspected resources."""
from pathlib import Path
from .runtime_descriptor import Resource


def validate_config(config, images, state, port):
    services = config.get('services', {})
    if set(services) != {'workspace', 'data-api'} or config.get('volumes'):
        raise ValueError('Runtime requires only the owned image pair and bind state')
    for name, service in services.items():
        if 'build' in service or service.get('image') != images[name]:
            raise ValueError('Runtime requires immutable images without builds')
        if any(service.get(key) for key in ('network_mode', 'privileged', 'devices', 'external_links', 'volumes_from')):
            raise ValueError('Runtime contains unexpected host access')
    workspace, data = services['workspace'], services['data-api']
    ports = workspace.get('ports', [])
    if len(ports) != 1 or data.get('ports') or data.get('volumes'):
        raise ValueError('Runtime requires one Workspace port and no data host access')
    binding = ports[0]
    if (binding.get('host_ip') != '127.0.0.1' or binding.get('target') != 3000
            or str(binding.get('published')) != str(port) or binding.get('protocol', 'tcp') != 'tcp'):
        raise ValueError('Runtime requires the requested loopback binding')
    mounts = workspace.get('volumes', [])
    if (len(mounts) != 1 or mounts[0].get('type') != 'bind'
            or mounts[0].get('target') != '/data' or mounts[0].get('read_only', False)
            or Path(mounts[0].get('source', '')).resolve() != Path(state).resolve()):
        raise ValueError('Runtime requires exactly its owned /data bind')
    if set(config.get('networks', {})) != {'default'} or config['networks']['default'].get('external'):
        raise ValueError('Runtime requires an owned default network')


def checked_container(inspected, service, project, session, image):
    labels = inspected.get('Config', {}).get('Labels') or {}
    expected = {'com.docker.compose.project': project, 'com.docker.compose.service': service,
                'org.qopenbb.session': session}
    if 'sha256:' + inspected.get('Image', '').removeprefix('sha256:') != image or any(labels.get(k) != v for k, v in expected.items()):
        raise ValueError('Runtime container ownership or image mismatch')
    return Resource(id=inspected['Id'], labels=labels)


def checked_network(inspected, project, session):
    labels = inspected.get('Labels') or inspected.get('labels') or {}
    expected = {'com.docker.compose.project': project, 'org.qopenbb.session': session}
    if any(labels.get(key) != value for key, value in expected.items()):
        raise ValueError('Runtime network ownership mismatch')
    return Resource(id=inspected.get('Id') or inspected.get('ID') or inspected['id'], labels=labels)

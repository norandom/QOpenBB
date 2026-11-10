"""Packaged health, Full configuration and disposable login; no provider queries."""
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import URLError
from urllib.request import Request, urlopen
from . import session_files


def request(origin, path, body=None):
    payload = None if body is None else json.dumps(body).encode()
    with urlopen(Request(origin + path, data=payload, headers={'Content-Type': 'application/json'}), timeout=5) as response:
        return response.status, response.read()


def inspect_pair(runtime):
    from .compose_checks import checked_container
    result = {}
    descriptor = runtime.descriptor
    for service, resource in descriptor.resources.containers.items():
        inspected = json.loads(runtime.command(['inspect', resource.id]))[0]
        checked_container(inspected, service, descriptor.project, descriptor.session_id, descriptor.images[service])
        if not inspected['State'].get('Running'):
            raise ValueError('Owned service exited during startup')
        result[service] = inspected
    if set(result) != {'workspace', 'data-api'}:
        raise ValueError('Both owned services required')
    return result


def verify_mapping(runtime, workspace):
    descriptor = runtime.descriptor
    mounts = workspace.get('Mounts', [])
    if len(mounts) != 1 or mounts[0].get('Type') != 'bind' or mounts[0].get('Destination') != '/data' or mounts[0].get('RW') is not True:
        raise ValueError('Inspected owned /data bind required')
    observed = runtime.command(['exec', descriptor.container, 'cat', '/data/qopenbb-sentinel']).strip()
    expected = session_files.read_private(Path(descriptor.state.host_path) / 'qopenbb-sentinel').decode()
    if observed != expected or observed != descriptor.session_id:
        raise ValueError('Host-to-daemon bind sentinel mismatch')
    source = mounts[0]['Source']
    identity = hashlib.sha256(json.dumps({'source': source, 'destination': '/data', 'type': 'bind',
                                        'sentinel': observed}, sort_keys=True).encode()).hexdigest()
    runtime.save(state={'host_path': descriptor.state.host_path, 'daemon_path': source,
                        'mount_identity': identity, 'verified': True})


def wait_health(runtime):
    for _ in range(90):
        pair = inspect_pair(runtime)
        try:
            status, _ = request(runtime.descriptor.origin, '/api/health')
            healthy = all(item['State'].get('Health', {}).get('Status') == 'healthy' for item in pair.values())
            if status == 200 and healthy:
                runtime.command(['exec', runtime.descriptor.resources.containers['data-api'].id, 'python', '-c',
                    "import urllib.request; urllib.request.urlopen('http://127.0.0.1:6900/readyz',timeout=5).close()"])
                return pair
        except (URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(2)
    raise ValueError('Owned packaged services readiness timeout')


def ready(runtime):
    runtime.stage = 'service_health'
    pair = wait_health(runtime)
    runtime.stage = 'origin_binding'
    descriptor = runtime.descriptor
    bindings = pair['workspace']['NetworkSettings']['Ports']
    if set(bindings) != {'3000/tcp'} or len(bindings['3000/tcp']) != 1:
        raise ValueError('Unexpected inspected host bindings')
    binding = bindings['3000/tcp'][0]
    if binding['HostIp'] != '127.0.0.1' or descriptor.origin != 'http://127.0.0.1:'+binding['HostPort']:
        raise ValueError('Inspected origin mismatch')
    if any(pair['data-api']['NetworkSettings'].get('Ports', {}).values()):
        raise ValueError('Unexpected data API host binding')
    runtime.stage = 'bind_mapping'
    verify_mapping(runtime, pair['workspace'])
    runtime.stage = 'full_configuration'
    _, configuration = request(descriptor.origin, '/config.js')
    text = configuration.decode().strip()
    if not text.startswith('window.__APP_CONFIG__ = '):
        raise ValueError('Packaged Full configuration missing')
    payload = text.removeprefix('window.__APP_CONFIG__ = ').removesuffix(';')
    parsed = json.loads(re.sub(r'(?m)^(\s*)([A-Za-z][A-Za-z0-9]*):', r'\1"\2":', payload))
    if parsed['ui']['isLite'] is not False or parsed['urls']['backend'] != '/api' or parsed['copilot']['openbbCopilot'] is not False:
        raise ValueError('Packaged Full same-origin configuration required')
    runtime.stage = 'disposable_login'
    values = dict(line.split('=', 1) for line in runtime.command(['exec', descriptor.container, 'cat', '/data/secrets.env']).splitlines() if '=' in line)
    credentials = {'email': values['OPENBB_ADMIN_EMAIL'], 'password': values['OPENBB_ADMIN_PASSWORD']}
    status, body = request(descriptor.origin, '/api/pro/login', {**credentials, 'remember': False})
    token = json.loads(body)
    if status != 200 or not token.get('access_token') or token.get('email') != credentials['email']:
        raise ValueError('Disposable login readiness failed')
    runtime.save(credentials=credentials)

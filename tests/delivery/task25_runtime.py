"""Portable packaging smoke against an already loaded image, outside Dagger."""
import argparse
import json
import hashlib
from http.cookies import SimpleCookie
import os
import re
from pathlib import Path
import subprocess
import tempfile
import time
from uuid import uuid4
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def docker(*args):
    return subprocess.check_output(['docker', *args], text=True, stderr=subprocess.PIPE)


def request(origin, path, body=None, private_values=None):
    data = None if body is None else json.dumps(body).encode()
    req = Request(origin + path, data=data, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=5) as response:
        if private_values is not None:
            for header in response.headers.get_all('Set-Cookie', []):
                cookies = SimpleCookie()
                cookies.load(header)
                private_values.extend(cookie.value for cookie in cookies.values() if cookie.value)
        return response.status, response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    name = 'qopenbb-task25-' + uuid4().hex
    image = json.loads(docker('image', 'inspect', args.image))[0]
    report = {'image': image['Id'], 'labels': image['Config'].get('Labels'), 'verified': False}
    private_values = []
    container = None
    with tempfile.TemporaryDirectory(prefix='qopenbb-task25-state-') as state:
        owned_state = Path(state)
        assert not owned_state.is_symlink()
        assert owned_state.resolve().parent == Path(tempfile.gettempdir()).resolve()
        assert owned_state.name.startswith('qopenbb-task25-state-')
        try:
            report['phase'] = 'container_start'
            container = docker('run', '-d', '--name', name, '--mount', f'type=bind,src={state},dst=/data',
                   '-p', '127.0.0.1::3000', '-e', 'PUBLIC_URL=http://localhost',
                   '-e', 'OPENBB_ADMIN_EMAIL=task25@example.com', image['Id']).strip()
            inspected = json.loads(docker('inspect', name))[0]
            assert inspected['Image'] == image['Id'], 'Runtime image identity mismatch'
            assert inspected['NetworkSettings']['Ports']['3000/tcp'][0]['HostIp'] == '127.0.0.1'
            port = inspected['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']
            origin = 'http://127.0.0.1:' + port
            report['phase'] = 'readiness'
            for attempt in range(90):
                try:
                    status, _ = request(origin, '/api/health')
                    observed = json.loads(docker('inspect', name))[0]['State']
                    assert observed['Running'], 'Container exited before readiness'
                    if status == 200 and observed.get('Health', {}).get('Status') == 'healthy':
                        break
                except (URLError, TimeoutError, ConnectionError):
                    pass
                time.sleep(2)
            else:
                raise AssertionError('image health timeout')
            report['phase'] = 'full_configuration'
            _, config = request(origin, '/config.js')
            text = config.decode().strip()
            assert text.startswith('window.__APP_CONFIG__ = ')
            payload = text.removeprefix('window.__APP_CONFIG__ = ').removesuffix(';')
            parsed = json.loads(re.sub(r'(?m)^(\s*)([A-Za-z][A-Za-z0-9]*):', r'\1"\2":', payload))
            assert parsed['ui']['isLite'] is False
            assert parsed['urls']['backend'] == '/api'
            assert parsed['copilot']['openbbCopilot'] is False
            credentials = dict(line.split('=', 1) for line in docker('exec', name, 'cat', '/data/secrets.env').splitlines())
            private_values.extend(value for key, value in credentials.items() if key not in ('OPENBB_ADMIN_EMAIL', 'OKTA_DOMAIN') and value)
            report['phase'] = 'login'
            status, response = request(origin, '/api/pro/login', {
                'email': credentials['OPENBB_ADMIN_EMAIL'], 'password': credentials['OPENBB_ADMIN_PASSWORD'],
                'remember': False}, private_values=private_values)
            token = json.loads(response)
            assert status == 200 and token.get('access_token')
            assert token.get('email') == credentials['OPENBB_ADMIN_EMAIL']
            private_values.append(token['access_token'])
            report['phase'] = 'wrong_password'
            try:
                request(origin, '/api/pro/login', {'email': credentials['OPENBB_ADMIN_EMAIL'],
                                                 'password': 'Incorrect25!Password'})
            except HTTPError as error:
                assert error.code == 401
            else:
                raise AssertionError('invalid password accepted')
            report['phase'] = 'private_state'
            probe = "import json, pathlib, stat; paths=['/data/openbb.db','/data/secrets.env','/opt/code/scripts/cfgs/config.toml','/opt/code/user_create.json']; print(json.dumps({p: {'mode': oct(stat.S_IMODE(pathlib.Path(p).stat().st_mode)), 'bytes': pathlib.Path(p).stat().st_size, 'uid': pathlib.Path(p).stat().st_uid} for p in paths}))"
            metadata = json.loads(docker('exec', name, 'python', '-c', probe))
            assert all(item['mode'] == '0o600' and item['bytes'] > 0 and item['uid'] != 0 for item in metadata.values())
            report.update(verified=True, health=200, full_config=True, login=200,
                          wrong_password=401, bind_state=True, private_state=metadata,
                          config_sha256=hashlib.sha256(config).hexdigest(), container=container,
                          port=port, docker_health='healthy', phase='complete')
        except Exception as error:
            report['failure_type'] = type(error).__name__
        finally:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            if container and not private_values:
                recovered = subprocess.run(['docker', 'exec', container, 'cat', '/data/secrets.env'], capture_output=True, text=True)
                private_values.extend(line.split('=', 1)[1] for line in recovered.stdout.splitlines()
                                      if '=' in line and line.split('=', 1)[0] not in ('OPENBB_ADMIN_EMAIL', 'OKTA_DOMAIN'))
            logs = subprocess.run(['docker', 'logs', container], capture_output=True, text=True) if container else None
            output = logs.stdout + logs.stderr if logs else ''
            report['logs_secret_free'] = not any(value in output for value in private_values)
            for value in private_values:
                output = output.replace(value, '[REDACTED]')
            args.report.with_suffix('.log').write_text(output)
            if container:
                assert not owned_state.is_symlink() and owned_state.resolve() == owned_state
                ownership = subprocess.run(['docker', 'exec', '--user', '0', container,
                                            'chown', '-R', '-h', str(os.getuid()), '/data'], capture_output=True)
                report['state_ownership_restored'] = ownership.returncode == 0
                cleanup = subprocess.run(['docker', 'rm', '-f', container], capture_output=True)
                report['container_removed'] = cleanup.returncode == 0
            report['verified'] = (report['verified'] and report['logs_secret_free']
                                  and report.get('container_removed', False)
                                  and report.get('state_ownership_restored', False))
            args.report.write_text(json.dumps(report, indent=2) + '\n')
    if not report['verified']:
        raise SystemExit('Runtime verification failed; inspect sanitized report (credential bodies withheld)')


if __name__ == '__main__':
    main()

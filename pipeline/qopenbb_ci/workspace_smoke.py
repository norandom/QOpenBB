"""Packaged image-pair smoke through the checked Compose lifecycle, outside Dagger."""
import argparse
import hashlib
from http.cookies import SimpleCookie
import json
import os
from pathlib import Path
import subprocess
from uuid import uuid4
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from qopenbb_ci.compose_runtime import start, StartRequest, ComposeRuntime
from qopenbb_ci.compose_lifecycle import stop
from qopenbb_ci.container_command import container_command
from qopenbb_ci.native_environment import validate_output, run_command
from qopenbb_ci.portable_runtime import resolve_environment, output_options


def docker(*args):
    return subprocess.check_output(container_command(args), text=True, stderr=subprocess.PIPE,
                                   **({'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}))


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


def check_packaged(runtime, report, private_values):
    descriptor = runtime.descriptor
    origin = descriptor.origin
    status, _ = request(origin, '/api/health')
    assert status == 200
    _, config = request(origin, '/config.js')
    report['config_sha256'] = hashlib.sha256(config).hexdigest()
    values = runtime.command(['exec', descriptor.container, 'cat', '/data/secrets.env'])
    private_values.extend(line.split('=', 1)[1] for line in values.splitlines()
                          if '=' in line and line.split('=', 1)[0] not in ('OPENBB_ADMIN_EMAIL', 'OKTA_DOMAIN')
                          and line.split('=', 1)[1])
    credentials = descriptor.credentials.model_dump()
    private_values.append(credentials['password'])
    status, response = request(origin, '/api/pro/login', {**credentials, 'remember': False}, private_values)
    token = json.loads(response)
    assert status == 200 and token.get('access_token') and token.get('email') == credentials['email']
    private_values.append(token['access_token'])
    try:
        request(origin, '/api/pro/login', {'email': credentials['email'], 'password': 'Incorrect25!Password'})
    except HTTPError as error:
        assert error.code == 401
    else:
        raise AssertionError('invalid password accepted')
    probe = "import json,pathlib,stat; paths=['/data/openbb.db','/data/secrets.env','/opt/code/scripts/cfgs/config.toml','/opt/code/user_create.json']; print(json.dumps({p:{'mode':oct(stat.S_IMODE(pathlib.Path(p).stat().st_mode)),'bytes':pathlib.Path(p).stat().st_size,'uid':pathlib.Path(p).stat().st_uid} for p in paths}))"
    metadata = json.loads(runtime.command(['exec', descriptor.container, 'python', '-c', probe]))
    assert all(item['mode'] == '0o600' and item['bytes'] > 0 and item['uid'] != 0 for item in metadata.values())
    report.update(health=200, full_config=True, login=200, wrong_password=401, bind_state=True,
                  private_state=metadata, container=descriptor.container, images=descriptor.images)


def capture_logs(runtime, private_values, path):
    output = ''
    for resource in runtime.descriptor.resources.containers.values():
        result = run_command(container_command(['logs', resource.id], runtime.config.environment),
                             runtime.config.repository, runtime.config.environment)
        if result.returncode:
            raise ValueError('Owned service logs unavailable')
        output += result.stdout + result.stderr
    secret_free = not any(value in output for value in private_values)
    for value in private_values:
        output = output.replace(value, '[REDACTED]')
    path.write_text(output)
    return secret_free


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--data-image', required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--private', type=Path)
    args = parser.parse_args(argv)
    config = resolve_environment(Path(__file__).resolve().parents[2])
    report_path = validate_output(args.report, **output_options(config))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    private_path = args.private or report_path.parent / ('runtime-' + uuid4().hex) / 'descriptor.json'
    runtime = ComposeRuntime(config, private_path)
    report = {'verified': False, 'phase': 'startup'}
    private_values = []
    try:
        runtime.descriptor = start(StartRequest(config, private_path, args.image, args.data_image))
        report['phase'] = 'packaged_checks'
        check_packaged(runtime, report, private_values)
        report['logs_secret_free'] = capture_logs(runtime, private_values, report_path.with_suffix('.log'))
        report['verified'] = report['logs_secret_free']
    except Exception as error:
        report['failure_type'] = type(error).__name__
    finally:
        if private_path.exists():
            try:
                cleanup = stop(config, private_path)
                report.update(container_removed=cleanup['phase'] == 'stopped', state_preserved=True)
            except Exception as error:
                report.update(verified=False, cleanup_failure=type(error).__name__)
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    if not report['verified']:
        raise SystemExit('Runtime verification failed; inspect sanitized report (credential bodies withheld)')


if __name__ == '__main__':
    main()

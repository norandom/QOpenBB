"""Origin runtime contract; all inputs are public, disposable fixture values."""
import json
import sys
from pathlib import Path
import subprocess
import pytest

ROOT = Path(__file__).resolve().parents[2]
LITE = ROOT / 'vendor/workspace/lite'


def test_public_origin_settings():
    result = subprocess.run([sys.executable, str(LITE / 'origin_config.py'), 'https://qbb.hanse-hedge.fund/'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    values = json.loads(result.stdout)
    assert values['SELFURL'] == 'https://qbb.hanse-hedge.fund/api'
    assert values['DATA_API_URL'] == 'https://qbb.hanse-hedge.fund/data'
    assert values['AGENT_API_URL'] == 'https://qbb.hanse-hedge.fund/agent'
    assert values['PUBLIC_SCHEME'] == 'https'


def test_reject_unsafe_origin():
    for value in ['https://user:secret@example.com', 'https://example.com/path', 'https://example.com?x=1', 'https://example.com\n', 'ftp://example.com', 'https://example.com:bad', 'https://example.com:65536', 'https://example.com:-1']:
        result = subprocess.run([sys.executable, str(LITE / 'origin_config.py'), value], capture_output=True)
        assert result.returncode != 0



@pytest.mark.parametrize('agent_available', [False, True])
def test_nginx_real_routes(tmp_path, agent_available):
    import uuid
    import http.server
    import socket
    import threading
    import time
    import urllib.error
    import urllib.request
    from string import Template

    class Upstream(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/stream':
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.end_headers()
                self.wfile.write(b'data: first\n\n')
                self.wfile.flush()
                time.sleep(1)
                self.wfile.write(b'data: second\n\n')
                return
            self.send_response(404 if 'missing' in self.path else 200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'path': self.path, 'scheme': self.headers.get('X-Forwarded-Proto')}).encode())
        def log_message(self, *args):
            pass

    fixture = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Upstream)
    threading.Thread(target=fixture.serve_forever, daemon=True).start()
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    values = {'PORT': str(port), 'PUBLIC_HOST': 'qbb.hanse-hedge.fund', 'PUBLIC_SCHEME': 'https', 'NGINX_RESOLVER': '127.0.0.11'}
    routes = Template((LITE / 'qopenbb-routes.conf.template').read_text()).safe_substitute(values)
    routes = routes.replace('http://data-api:6900', f'http://127.0.0.1:{fixture.server_port}')
    if agent_available:
        routes = routes.replace('http://agent:7777', f'http://127.0.0.1:{fixture.server_port}')
    routes += '\nlocation = /excel { return 404; }\nlocation ^~ /excel/ { return 404; }\n'
    (tmp_path / 'routes.conf').write_text(routes)
    main = Template((LITE / 'nginx.conf.template').read_text()).safe_substitute(values)
    main = main.replace('127.0.0.1:8000', f'127.0.0.1:{fixture.server_port}').replace('/etc/nginx/qopenbb-routes.conf', '/fixture/routes.conf').replace('/usr/share/nginx/html', '/fixture')
    (tmp_path / 'nginx.conf').write_text('events {}\nhttp { access_log off; error_log /dev/stderr warn;\n' + main + '\n}')
    (tmp_path / 'index.html').write_text('fixture SPA')
    tmp_path.chmod(0o755)
    for path in tmp_path.iterdir():
        path.chmod(0o644)
    name = 'qopenbb-origin-' + uuid.uuid4().hex
    command = ['docker', 'run', '--name', name, '--rm', '--network', 'host', '-v', f'{tmp_path}:/fixture:ro', 'sha256:df221db836e1754089190208cee7eeda94f233197056426eda74a43ab1abeac2', 'nginx', '-c', '/fixture/nginx.conf', '-g', 'daemon off;']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def request(path):
        try:
            with urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{port}{path}', headers={'X-Forwarded-Proto': 'http'}), timeout=3) as response:
                return response.status, response.read().decode()
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode()
    try:
        for _ in range(30):
            try:
                assert request('/dashboard')[1] == 'fixture SPA'
                break
            except OSError:
                time.sleep(0.1)
        else:
            raise AssertionError('nginx failed to start')
        import http.client
        connection = http.client.HTTPConnection('127.0.0.1', port, timeout=3)
        connection.request('GET', '/data')
        redirect = connection.getresponse()
        assert redirect.status == 308 and redirect.getheader('Location') == '/data/'
        connection.close()
        assert json.loads(request('/data/widgets.json?x=1')[1]) == {'path': '/widgets.json?x=1', 'scheme': 'https'}
        assert json.loads(request('/api/pro/user')[1])['path'] == '/pro/user'
        status, body = request('/data/missing')
        assert status == 404 and 'fixture SPA' not in body
        assert request('/excel/manifest.xml')[0] == 404
        if agent_available:
            started = time.monotonic()
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/agent/stream', timeout=3) as stream:
                assert stream.readline() == b'data: first\n'
                assert time.monotonic() - started < 0.8
                assert b'data: second' in stream.read()
        else:
            assert request('/agent/query')[0] == 502
        assert request('/dashboard')[1] == 'fixture SPA'
    finally:
        subprocess.run(['docker', 'rm', '-f', name], capture_output=True, check=False)
        process.communicate(timeout=10)
        fixture.shutdown()


def test_actual_frontend_renderer(tmp_path):
    env = dict(__import__('os').environ, CONFIG_OUT=str(tmp_path / 'config.js'), PUBLIC_URL='https://qbb.hanse-hedge.fund', AI_COPILOT_OPENBB_COPILOT='true', AI_COPILOT_AI_ENHANCEMENTS='true')
    subprocess.run(['bash', str(LITE / 'render-frontend-config.full.sh')], env=env, check=True)
    text = (tmp_path / 'config.js').read_text()
    assert 'data: "https://qbb.hanse-hedge.fund/data"' in text
    assert 'agent: "https://qbb.hanse-hedge.fund/agent"' in text
    assert 'openbbCopilot: false' in text
    assert 'aiEnhancements: false' in text
    assert 'webSearch: false' in text
    assert 'ai: ""' in text


@pytest.mark.parametrize('excel_enabled', ['false', 'true'])
def test_origin_boot_configuration(tmp_path, excel_enabled):
    import os
    binary = tmp_path / 'bin'
    binary.mkdir()
    (binary / 'python').symlink_to(sys.executable)
    subst = binary / 'envsubst'
    subst.write_text('#!/bin/bash\nexec docker run --rm -i --entrypoint envsubst -e NGINX_RESOLVER -e PUBLIC_HOST -e PUBLIC_SCHEME sha256:df221db836e1754089190208cee7eeda94f233197056426eda74a43ab1abeac2 "$@"\n')
    subst.chmod(0o755)
    env = dict(os.environ, PATH=str(binary) + ':' + os.environ['PATH'], PUBLIC_URL='https://qbb.hanse-hedge.fund', ORIGIN_HELPERS=str(LITE), ROUTES_OUT=str(tmp_path / 'routes.conf'), EXCEL_ENABLED=excel_enabled)
    command = ['bash', '-c', 'source "$1"; printf "%s\\n" "$FRONTENDURL" "$PROURL" "$SELFURL" "$DATA_API_URL" "$AGENT_API_URL" "$AI_API_URL"', 'fixture', str(LITE / 'configure-origin.sh')]
    result = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
    assert result.stdout.splitlines() == ['https://qbb.hanse-hedge.fund', 'https://qbb.hanse-hedge.fund', 'https://qbb.hanse-hedge.fund/api', 'https://qbb.hanse-hedge.fund/data', 'https://qbb.hanse-hedge.fund/agent', '']
    routes = (tmp_path / 'routes.conf').read_text()
    assert 'proxy_set_header X-Forwarded-Proto https;' in routes
    assert ('http://excel:80' in routes) == (excel_enabled == 'true')

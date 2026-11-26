"""Check the independent Modeling image's build inputs and loaded runtime."""

import hashlib
import json
import os
import subprocess
import time
import tomllib
from pathlib import Path

import pytest
from qopenbb_ci.container_command import container_command
from qopenbb_ci.modeling_image import MODELING_FILES, stage_modeling

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path('services/data-api/qopenbb_data')
PACKAGING = Path('services/modeling')


def test_modeling_stage_copies_exact_source_and_lock(tmp_path):
    inputs = stage_modeling(ROOT, tmp_path)
    sources = (ROOT / PACKAGE / 'modeling').rglob('*.py')
    expected = {path.relative_to(ROOT).as_posix() for path in sources}
    expected.update((str(PACKAGE / '__init__.py'), str(PACKAGING / 'pyproject.toml'),
                     str(PACKAGING / 'uv.lock')))
    assert set(inputs) == expected
    assert {path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob('*') if path.is_file()} == expected
    for file, digest in inputs.items():
        assert (tmp_path / file).read_bytes() == (ROOT / file).read_bytes()
        assert hashlib.sha256((tmp_path / file).read_bytes()).hexdigest() == digest


def test_modeling_stage_excludes_private_inputs_and_rejects_linked_source(tmp_path):
    root = tmp_path / 'root'
    bootstrap = PACKAGE / 'modeling/service/bootstrap.py'
    for relative in MODELING_FILES:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('test source')
    secret = root / PACKAGE / 'modeling/.env'
    secret.write_text('unrelated private input')
    (secret.parent / 'local_credentials.py').write_text('not in the runtime inventory')
    assert set(stage_modeling(root, tmp_path / 'stage')) == MODELING_FILES
    (root / bootstrap).unlink()
    (root / bootstrap).symlink_to(secret)
    with pytest.raises(ValueError, match='symlink'):
        stage_modeling(root, tmp_path / 'rejected')


def test_modeling_lock_uses_only_published_hashed_artifacts():
    lock = tomllib.loads((ROOT / PACKAGING / 'uv.lock').read_text())
    packages = {package['name']: package for package in lock['package']}
    project = packages.pop('qopenbb-modeling-runtime')
    assert set(project['source']) == {'virtual'}
    assert not any(name.startswith(('openbb', 'pytest')) for name in packages)
    for package in packages.values():
        assert package['source'] == {'registry': 'https://pypi.org/simple'}
        assert package['wheels']
        assert all(wheel['hash'].startswith('sha256:') for wheel in package['wheels'])


def docker(*args):
    return subprocess.run(container_command(args), text=True, capture_output=True, check=True,
                          timeout=15, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)


PROBE = '''
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import jwt

url = "http://127.0.0.1:6901/modeling/v1/models"
try:
    urlopen(url, timeout=2)
except HTTPError as error:
    assert error.code == 401
else:
    raise AssertionError("unsigned discovery accepted")

now = int(time.time())
token = jwt.encode(
    {"iss": "qopenbb-workspace", "aud": "qfm", "sub": "image-probe", "iat": now, "exp": now + 30},
    os.environ["QFM_IDENTITY_CURRENT_SECRET"],
    headers={"kid": "smoke", "typ": "qfm-identity"},
)
with urlopen(Request(url, headers={"Authorization": "Bearer " + token}), timeout=2) as response:
    assert len(json.load(response)["models"]) == 6
assert (os.getuid(), os.getgid()) == (10001, 10001)
assert not {"FMP_API_KEY", "FRED_API_KEY"}.intersection(os.environ)
assert os.environ["QOPENBB_MODEL_DATA_ORIGIN"] == "http://data-api:6900"
state = Path(os.environ["QOPENBB_MODEL_RUN_DIR"])
assert state == Path("/data/modeling")
(state / "write-probe").touch()
'''

IMAGE = os.environ.get('QOPENBB_MODELING_IMAGE')


@pytest.mark.skipif(not IMAGE, reason='requires the explicitly identified loaded Modeling image')
def test_loaded_modeling_image_serves_authenticated_discovery():
    config = json.loads(docker('image', 'inspect', IMAGE).stdout)[0]['Config']
    assert config['User'] == '10001:10001'
    assert set(config['ExposedPorts']) == {'6901/tcp'}
    assert config['Labels']['org.qopenbb.runtime-lock.sha256'] == hashlib.sha256(
        (ROOT / PACKAGING / 'uv.lock').read_bytes()).hexdigest()

    cid = docker('run', '-d', '--network', 'none', '-e', 'QFM_IDENTITY_CURRENT_KID=smoke', '-e',
                 'QFM_IDENTITY_CURRENT_SECRET=disposable-modeling-image-check-secret', IMAGE).stdout.strip()
    try:
        deadline = time.monotonic() + 20
        while True:
            try:
                docker('exec', cid, 'python', '-c', PROBE)
                break
            except subprocess.CalledProcessError as error:
                if time.monotonic() >= deadline:
                    pytest.fail(error.stderr + docker('logs', cid).stderr)
                time.sleep(0.25)
    finally:
        docker('rm', '-f', cid)

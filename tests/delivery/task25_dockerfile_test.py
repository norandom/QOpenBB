"""Compatibility translation preserves exact remote asset bytes and permissions."""
import importlib.util
from pathlib import Path
import pytest
spec = importlib.util.spec_from_file_location('dockerfile_adapter', Path(__file__).resolve().parents[2] / '.dagger/src/qopenbb/dockerfile.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
remote_assets = adapter.remote_assets


def test_remote_add_preserves_checksum_and_mode():
    digest = 'a' * 64
    content = f'FROM pinned\nADD --chmod=755 --checksum=sha256:{digest} https://example.invalid/tool /bin/tool\n'
    translated, assets = remote_assets(content)
    assert translated == f'FROM pinned\nCOPY --chmod=755 .qopenbb-build-assets/{digest} /bin/tool\n'
    assert assets == [{'mode': '755', 'digest': digest, 'url': 'https://example.invalid/tool',
                       'target': '/bin/tool', 'path': '.qopenbb-build-assets/' + digest}]


@pytest.mark.parametrize('line', ['ADD https://example.invalid/tool /bin/tool',
    'ADD --checksum=sha256:bad https://example.invalid/tool /bin/tool',
    'ADD local /bin/tool', '  add https://example.invalid/x /x',
    'ADD --checksum=sha256:' + 'a'*64 + ' http://example.invalid/x /x'])
def test_unsupported_add_fails_closed(line):
    with pytest.raises(ValueError):
        remote_assets(line)

"""Explicit root runtime input boundary; no repository-directory uploads."""
import hashlib
import shutil
import stat
from pathlib import Path

RUNTIME_FILES = frozenset('services/data-api/' + name for name in (
    'pyproject.toml', 'uv.lock', 'qopenbb_data/__init__.py',
    'qopenbb_data/config.py', 'qopenbb_data/app.py', 'qopenbb_data/gallery.py',
    'qopenbb_data/financial_openapi.py', 'qopenbb_data/financial_catalog.py',
    'qopenbb_data/financial_policy.py', 'qopenbb_data/financial_errors.py',
    'qopenbb_data/financial_query_policy.py', 'qopenbb_data/financial_http_quarter.py',
    'qopenbb_data/modeling/__init__.py',
    'qopenbb_data/modeling/contracts/__init__.py',
    'qopenbb_data/modeling/contracts/common.py',
    'qopenbb_data/modeling/contracts/inputs.py',
    'qopenbb_data/modeling/contracts/descriptors.py',
    'qopenbb_data/modeling/contracts/checks.py',
    'qopenbb_data/modeling/contracts/trace.py',
    'qopenbb_data/modeling/contracts/results.py',
    'qopenbb_data/modeling/models/__init__.py',
    'qopenbb_data/modeling/models/protocol.py',
    'qopenbb_data/modeling/models/registry.py',
    'qopenbb_data/modeling/models/factors/__init__.py',
    'qopenbb_data/modeling/models/factors/sessions.py',
    'qopenbb_data/modeling/models/factors/method_inputs.py',
    'qopenbb_data/modeling/models/factors/momentum.py',
    'qopenbb_data/modeling/models/factors/volatility.py',
    'qopenbb_data/modeling/models/factors/real_yield.py',
    'qopenbb_data/modeling/verification/__init__.py',
    'qopenbb_data/modeling/verification/factors/__init__.py')) | frozenset({
        'contracts/widgets.json', 'contracts/apps.json',
        'contracts/gallery/data.json', 'contracts/gallery/catalog.json',
        'docs/reference/provider-coverage.json'})


def copy_runtime(root: Path, destination: Path) -> dict[str, str]:
    files = {}
    for name in sorted(RUNTIME_FILES):
        source = root / name
        if any(path.is_symlink() for path in [source, *source.parents]):
            raise ValueError('runtime input symlink rejected')
        if not stat.S_ISREG(source.stat().st_mode):
            raise ValueError('runtime input must be regular')
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target, follow_symlinks=False)
        files[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    return files


def verify_runtime(root: Path, files: dict[str, str]) -> set[str]:
    if set(files) != RUNTIME_FILES:
        raise ValueError('runtime input allowlist differs')
    for name, digest in files.items():
        if hashlib.sha256((root / 'runtime' / name).read_bytes()).hexdigest() != digest:
            raise ValueError('runtime input hash mismatch')
    return {'runtime/' + name for name in files}

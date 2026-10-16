"""Select owned source files before uploading any build context."""

from collections.abc import Iterator
from pathlib import Path, PurePosixPath
import os
import re

BLOCKED = {
    '.git', '.hg', '.svn', '.ssh', '.aws', 'secrets', 'data', 'state', 'storage', 'backups',
    'backup', 'cache', 'logs',
    'artifacts', 'evidence', 'test-results', 'playwright-report', 'browser',
    '.codex', '.cache', '.pytest_cache', '__pycache__', 'node_modules', '.venv',
    'venv', 'dist', 'build', 'htmlcov', 'coverage', '.next', '.turbo',
}
PRIVATE_NAMES = {'id_rsa', 'id_ed25519', 'id_dsa', 'credentials', '.npmrc', '.pypirc'}
ALLOW = {
    'workspace': ['lite', 'terminalpro', 'backend-api', 'LICENSE', 'NOTICE'],
    'data_api': ['openbb_platform', 'LICENSE'],
}


def empty_public_sample(path: Path) -> bool:
    """Public dotenv samples are safe only when every assignment value is empty."""
    if path.name not in {'.env.sample', '.env.example'}:
        return False
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except (UnicodeError, OSError):
        return False
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*\s*=\s*(?:""|\'\')?', line):
            return False
    return True


def excluded(relative: PurePosixPath, path: Path) -> bool:
    parts = [part.lower() for part in relative.parts]
    if any(part in BLOCKED for part in parts):
        return True
    name = parts[-1]
    if name == '.env' or name.startswith('.env.'):
        return not empty_public_sample(path)
    return (name in PRIVATE_NAMES or name.endswith(('.pem', '.key', '.p12', '.pfx', '.pyc', '.db', '.sqlite', '.sqlite3'))
            or name.startswith('.coverage'))


def source_scope(source: str, revision: str, policy: dict, lock: dict) -> list[str]:
    if type(policy.get('schema_version')) is not int or policy['schema_version'] != 1:
        raise ValueError('invalid source policy version')
    if set(policy) != {'schema_version', 'sources'}:
        raise ValueError('invalid source policy')
    if source not in ALLOW or set(policy['sources']) != set(ALLOW):
        raise ValueError('unknown source ownership')
    entry = policy['sources'][source]
    if set(entry) != {'source_lock_key', 'revision', 'allow'}:
        raise ValueError('invalid source entry')
    if entry['source_lock_key'] != source or entry['allow'] != ALLOW[source]:
        raise ValueError('source allowlist differs from frozen ownership')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('exact source revision required')
    if entry['revision'] != revision or lock[source]['revision'] != revision:
        raise ValueError('source revision differs from source lock')
    return entry['allow']


def select_source(root: Path, source: str, revision: str, policy: dict, lock: dict) -> list[str]:
    """Return deterministic root-relative files; symlinks fail closed without reading targets."""
    allow = source_scope(source, revision, policy, lock)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('source root must be a real directory')
    root = root.resolve()
    selected = []
    for owned in allow:
        start = root / owned
        if not start.exists() and not start.is_symlink():
            continue
        for path in walk_owned(start):
            relative = PurePosixPath(path.relative_to(root).as_posix())
            if path.is_symlink():
                raise ValueError('source symlinks require an explicit reviewed materialization')
            if not path.resolve().is_relative_to(root):
                raise ValueError('source path escapes owned root')
            if path.is_file() and not excluded(relative, path):
                selected.append(str(relative))
    return sorted(set(selected))


def scan_error(error: OSError) -> None:
    raise ValueError('cannot completely scan owned source') from None


def walk_owned(start: Path) -> Iterator[Path]:
    yield start
    if not start.is_dir() or start.is_symlink():
        return
    for current, directories, files in os.walk(start, followlinks=False, onerror=scan_error):
        for name in directories + files:
            yield Path(current) / name

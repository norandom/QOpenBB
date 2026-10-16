"""Materialize filtered, hash-addressed inputs before Dagger receives a directory."""

from pathlib import Path
import hashlib
import json
import shutil
import re

from qopenbb_ci.source_filter import excluded, select_source, source_scope, walk_owned
from pathlib import PurePosixPath
from qopenbb_ci.sources import git, identity
from qopenbb_ci.provenance import parse_provenance
from qopenbb_ci.runtime_inputs import copy_runtime, verify_runtime

SMOKE = 'print("QOpenBB foundation smoke; no application services")\n'


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def stage_source(root: Path, destination: Path, source: str, policy: dict, lock: dict) -> dict:
    verified = identity(root, lock[source])
    revision = verified['revision']
    selected = select_source(root, source, revision, policy, lock)
    tracked = set(git(root, 'ls-files', '-z').split('\0'))
    selected = [name for name in selected if name in tracked]
    blobs = {record.split('\t', 1)[1]: record.split()[1]
             for record in git(root, 'ls-files', '--stage', '-z').split('\0') if record}
    for essential in policy['sources'][source]['allow']:
        if not any(name == essential or name.startswith(essential + '/') for name in selected):
            raise ValueError('missing essential source root: ' + essential)
    files = {}
    for name in selected:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target, follow_symlinks=False)
        content = target.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        if blob != blobs[name]:
            raise ValueError('source bytes differ from locked Git blob')
        files[name] = sha256(target)
    identity(root, lock[source])
    return {**verified, 'files': files}


def stage(destination: Path, roots: dict[str, Path], policy: dict, lock: dict,
          service: str = 'foundation-smoke', release_version: str | None = None,
          runtime_root: Path | None = None) -> dict:
    if service not in {'foundation-smoke', 'workspace', 'data-api'}:
        raise ValueError('unsupported build selection')
    if (service == 'data-api') != (runtime_root is not None):
        raise ValueError('runtime inputs require data-api selection')
    if service == 'workspace':
        if not isinstance(release_version, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', release_version):
            raise ValueError('public release identity required')
    elif release_version is not None:
        raise ValueError('foundation has no release identity')
    if destination.exists() or destination.is_symlink():
        raise ValueError('staging requires a fresh destination')
    if set(roots) != {'workspace', 'data_api'}:
        raise ValueError('both owned source snapshots are required')
    destination.mkdir(parents=True)
    try:
        sources = {key: stage_source(root, destination / 'sources' / key, key, policy, lock)
                   for key, root in sorted(roots.items())}
        (destination / 'smoke.py').write_text(SMOKE, encoding='utf-8')
        result = {'schema_version': 1, 'service': service, 'sources': sources,
                  'smoke_sha256': sha256(destination / 'smoke.py')}
        if service == 'workspace':
            result['release_version'] = release_version
        if runtime_root is not None:
            result['runtime_inputs'] = copy_runtime(runtime_root, destination / 'runtime')
        (destination / 'provenance.json').write_text(json.dumps(result, sort_keys=True) + '\n')
        return result
    except Exception:
        shutil.rmtree(destination)
        raise


def staged_files(root: Path) -> set[str]:
    if root.is_symlink():
        raise ValueError('staging root must not be a symlink')
    actual = set()
    for path in walk_owned(root):
        if path.is_symlink():
            raise ValueError('staging symlink rejected')
        if path == root:
            continue
        if not path.is_dir() and not path.is_file():
            raise ValueError('nonregular staged input rejected')
        actual.add(path.relative_to(root).as_posix())
    return actual


def verify_stage(root: Path, policy: dict | None = None, lock: dict | None = None) -> dict:
    actual = staged_files(root)
    result = parse_provenance((root / 'provenance.json').read_text())
    expected = {'provenance.json', 'smoke.py'}
    if result['service'] not in {'foundation-smoke', 'workspace', 'data-api'} or result['schema_version'] != 1:
        raise ValueError('unsupported build selection')
    if set(result['sources']) != {'workspace', 'data_api'}:
        raise ValueError('both owned sources required')
    for key, source in result['sources'].items():
        if policy is not None and lock is not None:
            allow = source_scope(key, source['revision'], policy, lock)
            if source['repository'] != lock[key]['repository']:
                raise ValueError('staged repository differs from source lock')
        else:
            allow = ['lite', 'terminalpro', 'backend-api', 'LICENSE', 'NOTICE'] if key == 'workspace' else ['openbb_platform', 'LICENSE']
        for name, digest in source['files'].items():
            relative_name = PurePosixPath(name)
            if (not relative_name.parts or relative_name.is_absolute() or '..' in relative_name.parts
                    or relative_name.parts[0] not in allow
                    or excluded(relative_name, root / 'sources' / key / name)):
                raise ValueError('staged source violates filtering contract')
            relative = 'sources/' + key + '/' + name
            if not (root / relative).resolve().is_relative_to(root.resolve()):
                raise ValueError('staging path escapes root')
            if sha256(root / relative) != digest:
                raise ValueError('staging source hash mismatch')
            expected.add(relative)
    if result['service'] == 'data-api':
        expected |= verify_runtime(root, result['runtime_inputs'])
    expected |= {str(parent) for name in expected for parent in PurePosixPath(name).parents
                 if str(parent) != '.'}
    if actual != expected or sha256(root / 'smoke.py') != result['smoke_sha256']:
        raise ValueError('staging files differ from provenance')
    if (root / 'smoke.py').read_text() != SMOKE:
        raise ValueError('foundation smoke differs from maintained fixture')
    return result

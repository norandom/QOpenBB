"""Publish an independently reloaded archive using existing Docker authentication."""

import json
from pathlib import Path
import re
import subprocess

from qopenbb_ci.images import inspect_archive, load

DIGEST = r'sha256:[0-9a-f]{64}'


def target_reference(repository: str, tag: str) -> str:
    host, separator, path = repository.partition('/')
    if (not separator or not re.fullmatch(r'[a-z0-9][a-z0-9.-]*(?::[0-9]{1,5})?', host)
            or not ('.' in host or ':' in host or host == 'localhost')
            or not re.fullmatch(r'[a-z0-9]+(?:[._-][a-z0-9]+)*(?:/[a-z0-9]+(?:[._-][a-z0-9]+)*)*', path)):
        raise ValueError('explicit registry repository required')
    if (not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}', tag)
            or tag.lower() in {'latest', 'main', 'master', 'stable', 'dev'}):
        raise ValueError('unique release tag required')
    return repository + ':' + tag


def verify_sources(identity: dict) -> dict:
    labels = identity['labels']
    if labels.get('org.qopenbb.service') not in {'workspace', 'data-api'}:
        raise ValueError('only prototype runtime services may be published')
    sources = {}
    for name in ['workspace', 'data_api']:
        revision = labels.get('org.qopenbb.source.' + name, '')
        repository = labels.get('org.qopenbb.repository.' + name, '')
        if (not re.fullmatch(r'[0-9a-f]{40}', revision)
                or not re.fullmatch(r'https://github.com/norandom/[A-Za-z0-9_.-]+(?:\.git)?', repository)):
            raise ValueError('owned source labels required')
        sources[name] = {'revision': revision, 'repository': repository}
    if not re.fullmatch(r'[0-9a-f]{64}', labels.get('org.qopenbb.provenance.sha256', '')):
        raise ValueError('build provenance label required')
    return sources


def docker(*arguments: str) -> str:
    # Capture output: registry diagnostics must never become published evidence.
    return subprocess.run(['docker', *arguments], check=True, capture_output=True,
                          text=True).stdout


def remote_identity(reference: str) -> dict:
    observed = json.loads(docker('manifest', 'inspect', '--verbose', reference))
    if not isinstance(observed, dict):
        raise ValueError('single remote manifest required')
    descriptor = observed.get('Descriptor', {})
    digest = descriptor.get('digest', observed.get('Digest', ''))
    platform = descriptor.get('platform', observed.get('Platform', {}))
    manifest = observed.get('SchemaV2Manifest') or observed.get('OCIManifest', {})
    config = manifest.get('config', {}).get('digest', '')
    if (not re.fullmatch(DIGEST, digest) or not re.fullmatch(DIGEST, config)
            or manifest.get('schemaVersion') != 2
            or platform.get('architecture') != 'amd64' or platform.get('os') != 'linux'):
        raise ValueError('remote manifest identity or platform invalid')
    return {'manifest_digest': digest, 'config_digest': config, 'os': 'linux', 'architecture': 'amd64'}


def publish(archive: Path, verified_load: dict, repository: str, tag: str) -> dict:
    reference = target_reference(repository, tag)
    identity = inspect_archive(archive)
    if any(verified_load.get(key) != value for key, value in identity.items()):
        raise ValueError('supplied load report differs from archive')
    if (identity['architecture'], identity['os']) != ('amd64', 'linux'):
        raise ValueError('linux/amd64 required')
    sources = verify_sources(identity)
    if not re.fullmatch(DIGEST, verified_load.get('loaded_image_id', '')):
        raise ValueError('verified load identity required')
    reloaded = load(archive, identity)
    if reloaded['loaded_image_id'] != verified_load['loaded_image_id']:
        raise ValueError('reloaded image differs from supplied load report')
    docker('image', 'tag', reloaded['loaded_image_id'], reference)
    output = docker('image', 'push', reference)
    matches = re.findall(r'\bdigest: (' + DIGEST + r')\b', output)
    if len(matches) != 1:
        raise ValueError('push must report exactly one immutable digest')
    remote = remote_identity(reference)
    if remote['manifest_digest'] != matches[0] or remote['config_digest'] != identity['image_config_digest']:
        raise ValueError('remote tag differs from pushed archive')
    immutable = repository + '@' + matches[0]
    if remote_identity(immutable) != remote:
        raise ValueError('immutable remote identity differs from pushed tag')
    return {'schema_version': 1, 'valid': True, 'reference': immutable,
            'tag_reference': reference, 'archive_sha256': identity['archive_sha256'],
            'loaded_image_id': reloaded['loaded_image_id'], 'remote': remote,
            'service': identity['labels']['org.qopenbb.service'], 'sources': sources,
            'labels': identity['labels']}

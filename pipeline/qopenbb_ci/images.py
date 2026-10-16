"""Inspect/load Dagger archives with the portable Docker CLI, without rebuilding."""

from pathlib import Path
import hashlib
import json
import subprocess
import tarfile
import tempfile
import re

from qopenbb_ci.staging import sha256


def manifest_digest(bundle: tarfile.TarFile, config_bytes: bytes) -> str | None:
    if 'index.json' not in bundle.getnames():
        return None
    index = json.load(bundle.extractfile('index.json'))
    if len(index['manifests']) != 1:
        raise ValueError('exactly one archive manifest descriptor required')
    descriptor = index['manifests'][0]['digest']
    manifest_bytes = bundle.extractfile('blobs/sha256/' + descriptor.removeprefix('sha256:')).read()
    if descriptor != 'sha256:' + hashlib.sha256(manifest_bytes).hexdigest():
        raise ValueError('archive manifest descriptor mismatch')
    if json.loads(manifest_bytes)['config']['digest'] != 'sha256:' + hashlib.sha256(config_bytes).hexdigest():
        raise ValueError('archive manifest config mismatch')
    return descriptor


def inspect_archive(archive: Path, sentinel: bytes | None = None) -> dict:
    with tarfile.open(archive, 'r:*') as bundle:
        manifest = json.load(bundle.extractfile('manifest.json'))
        if len(manifest) != 1:
            raise ValueError('exactly one archived image required')
        entry = manifest[0]
        config_bytes = bundle.extractfile(entry['Config']).read()
        config = json.loads(config_bytes)
        descriptor = manifest_digest(bundle, config_bytes)
        for member in bundle.getmembers():
            if member.isfile() and sentinel:
                stream = bundle.extractfile(member)
                previous = b''
                while chunk := stream.read(1024 * 1024):
                    if sentinel in previous + chunk:
                        raise ValueError('synthetic secret found in archive metadata or layer')
                    previous = chunk[-len(sentinel):]
        for layer in entry['Layers']:
            with tarfile.open(fileobj=bundle.extractfile(layer), mode='r|*') as contents:
                for member in contents:
                    if member.name.endswith('/.env') or '/.git/' in member.name:
                        raise ValueError('private path found in image layer')
                    if member.isfile() and sentinel:
                        stream = contents.extractfile(member)
                        previous = b''
                        while chunk := stream.read(1024 * 1024):
                            if sentinel in previous + chunk:
                                raise ValueError('synthetic secret found in decoded layer')
                            previous = chunk[-len(sentinel):]
    return {'archive_sha256': sha256(archive),
            'image_config_digest': 'sha256:' + hashlib.sha256(config_bytes).hexdigest(),
            'image_manifest_digest': descriptor,
            'architecture': config['architecture'], 'os': config['os'],
            'labels': config.get('config', {}).get('Labels', {}), 'layers': entry['Layers']}


def load(archive: Path, expected: dict) -> dict:
    if inspect_archive(archive) != expected:
        raise ValueError('archive differs from inspected identity')
    output = subprocess.check_output(['docker', 'image', 'load', '--input', str(archive)], text=True)
    match = re.search(r'^Loaded image ID: (sha256:[0-9a-f]{64})$', output, re.MULTILINE)
    if not match or match[1] not in {expected['image_config_digest'], expected['image_manifest_digest']}:
        raise ValueError('loaded image ID does not match archive config or manifest')
    image_id = match[1]
    loaded = json.loads(subprocess.check_output(
        ['docker', 'image', 'inspect', image_id], text=True))[0]
    if (loaded['Id'] != image_id or loaded['Architecture'] != expected['architecture']
            or loaded['Os'] != expected['os'] or loaded['Config'].get('Labels', {}) != expected['labels']):
        raise ValueError('loaded image identity differs from archive')
    with tempfile.TemporaryDirectory(prefix='qopenbb-loaded-') as temporary:
        saved = Path(temporary) / 'loaded.tar'
        subprocess.run(['docker', 'image', 'save', '--output', str(saved), image_id], check=True)
        if inspect_archive(saved)['image_config_digest'] != expected['image_config_digest']:
            raise ValueError('loaded image configuration bytes differ from archive')
    return {**expected, 'loaded_image_id': loaded['Id'],
            'repo_digests': loaded.get('RepoDigests', []), 'registry_digest': None}

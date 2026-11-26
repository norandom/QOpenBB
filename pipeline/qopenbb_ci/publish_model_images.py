"""Promote accepted Workspace and modeling image archives with existing Docker authentication."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import tarfile

from qopenbb_ci.publication import DIGEST, publication_inputs, publish, target_reference
from qopenbb_ci.images import sha256

SERVICES = ('workspace', 'modeling')
ASSETS = {f'{service}{suffix}' for service in SERVICES for suffix in ('.tar', '-load.json')}


def verify_transfer(directory: Path, checksum: str) -> None:
    manifest = directory / 'transfer-SHA256SUMS'
    if not re.fullmatch(r'[0-9a-f]{64}', checksum) or sha256(manifest) != checksum:
        raise ValueError('accepted transfer manifest hash differs')
    expected = {}
    for line in manifest.read_text(encoding='ascii').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64}) [ *]([a-z.-]+)', line)
        if not match or match[2] not in ASSETS or match[2] in expected:
            raise ValueError('unexpected transfer manifest entry')
        expected[match[2]] = match[1]
    if expected.keys() != ASSETS:
        raise ValueError('incomplete transfer manifest')
    for name, digest in expected.items():
        if sha256(directory / name) != digest:
            raise ValueError(f'accepted transfer asset hash differs: {name}')


def write_report(path: Path, content: dict) -> None:
    with path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(content, indent=2) + '\n')


def promote(directory: Path, output: Path, namespace: str, tag: str,
            data_api: str, checksum: str) -> dict:
    if not tag.startswith('modeling-'):
        raise ValueError('modeling release tag required')
    data_repo, separator, digest = data_api.partition('@')
    if not separator or not data_repo.endswith('/qopenbb-data-api') or not re.fullmatch(DIGEST, digest):
        raise ValueError('immutable QOpenBB data API reference required')
    target_reference(data_repo, tag)
    repositories = {service: f'{namespace}/qopenbb-{service}' for service in SERVICES}
    for repository in repositories.values():
        target_reference(repository, tag)
    output.mkdir(parents=True)
    verify_transfer(directory, checksum)
    loads = {service: json.loads((directory / f'{service}-load.json').read_text(encoding='utf-8'))
             for service in SERVICES}
    for service in SERVICES:
        publication_inputs(directory / f'{service}.tar', loads[service], expected_service=service)
    images = {'data-api': data_api}
    for service in SERVICES:
        result = publish(directory / f'{service}.tar', loads[service], repositories[service],
                         tag, expected_service=service)
        write_report(output / f'{service}.json', result)
        images[service] = result['reference']
    write_report(output / 'images.json', images)
    return images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--registry-namespace', required=True)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--data-api-image', required=True)
    parser.add_argument('--accepted-inputs-sha256', required=True)
    args = parser.parse_args()
    try:
        promote(args.input, args.output, args.registry_namespace, args.tag,
                args.data_api_image, args.accepted_inputs_sha256)
    except (OSError, ValueError, KeyError, TypeError, IndexError, tarfile.TarError,
            subprocess.SubprocessError) as error:
        print(json.dumps({'valid': False, 'error': type(error).__name__}))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

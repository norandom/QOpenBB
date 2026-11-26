"""Accepted transfer identity gates modeling milestone publication."""

import hashlib
import io
import json
import tarfile

import pytest

from qopenbb_ci import publish_model_images, publication
from qopenbb_ci.staging import sha256

NAMESPACE = 'ghcr.io/norandom'
TAG = 'modeling-v0.1.0'
DATA = NAMESPACE + '/qopenbb-data-api@sha256:' + 'a' * 64


def archive_report(directory, service, labels):
    archive = directory / f'{service}.tar'
    config = {'architecture': 'amd64', 'os': 'linux', 'config': {'Labels': labels}}
    config_bytes = json.dumps(config).encode()
    config_digest = 'sha256:' + hashlib.sha256(config_bytes).hexdigest()
    oci_manifest = json.dumps({'config': {'digest': config_digest}}).encode()
    manifest_hash = hashlib.sha256(oci_manifest).hexdigest()
    with tarfile.open(archive, 'w') as bundle:
        for name, data in {
            'manifest.json': b'[{"Config":"config.json","Layers":[]}]',
            'config.json': config_bytes,
            'index.json': json.dumps({'manifests': [{'digest': 'sha256:' + manifest_hash}]}).encode(),
            f'blobs/sha256/{manifest_hash}': oci_manifest,
        }.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            bundle.addfile(entry, io.BytesIO(data))
    identity = publication.inspect_archive(archive)
    report = {**identity, 'loaded_image_id': identity['image_manifest_digest']}
    (directory / f'{service}-load.json').write_text(json.dumps(report))
    return identity


def checksum(directory):
    manifest = directory / 'transfer-SHA256SUMS'
    manifest.write_text(''.join(f'{sha256(directory / name)}  {name}\n'
                                for name in sorted(publish_model_images.ASSETS)))
    return sha256(manifest)


@pytest.fixture
def transfer(tmp_path, monkeypatch):
    directory = tmp_path / 'transfer'
    directory.mkdir()
    workspace = {'org.qopenbb.service': 'workspace', 'org.qopenbb.provenance.sha256': 'b' * 64}
    for name in ('workspace', 'data_api'):
        workspace[f'org.qopenbb.source.{name}'] = 'c' * 40
        workspace[f'org.qopenbb.repository.{name}'] = f'https://github.com/norandom/{name}.git'
    modeling = {'org.qopenbb.service': 'modeling', 'org.qopenbb.scope': 'modeling-runtime',
                'org.qopenbb.runtime-inputs.sha256': 'd' * 64,
                'org.qopenbb.runtime-lock.sha256': 'e' * 64}
    identities = {service: archive_report(directory, service, labels)
                  for service, labels in [('workspace', workspace), ('modeling', modeling)]}
    commands = []

    def docker(*args):
        commands.append(args)
        return 'digest: sha256:' + 'f' * 64

    def remote(reference):
        service = 'modeling' if '/qopenbb-modeling' in reference else 'workspace'
        return {'manifest_digest': 'sha256:' + 'f' * 64,
                'config_digest': identities[service]['image_config_digest']}

    monkeypatch.setattr(publication, 'docker', docker)
    monkeypatch.setattr(publication, 'remote_identity', remote)
    monkeypatch.setattr(publication, 'load',
                        lambda archive, identity: {'loaded_image_id': identity['image_config_digest']})
    return directory, tmp_path / 'reports', commands


def test_promotion_reuses_shared_publisher_and_retains_data_pin(transfer):
    directory, output, commands = transfer
    images = publish_model_images.promote(directory, output, NAMESPACE, TAG, DATA, checksum(directory))
    assert images['data-api'] == DATA
    assert json.loads((output / 'images.json').read_text()) == images
    assert [args[-1] for args in commands if args[:2] == ('image', 'push')] == [
        f'{NAMESPACE}/qopenbb-workspace:{TAG}', f'{NAMESPACE}/qopenbb-modeling:{TAG}',
    ]
    for service in publish_model_images.SERVICES:
        report = json.loads((output / f'{service}.json').read_text())
        assert report['service'] == service
        assert report['reference'] == images[service]
        assert report['archive_sha256'] == sha256(directory / f'{service}.tar')
        assert report['accepted_load_image_id'] == report['archive_manifest_digest']
        assert report['loaded_image_id'] == report['remote']['config_digest']
        assert report['loaded_image_id'] != report['accepted_load_image_id']


@pytest.mark.parametrize('mutation', ['manifest', 'asset', 'service', 'load-id', 'data-pin'])
def test_invalid_candidate_prevents_both_pushes(transfer, mutation):
    directory, output, commands = transfer
    digest = checksum(directory)
    data = DATA
    if mutation == 'manifest':
        digest = '0' * 64
    elif mutation == 'asset':
        (directory / 'modeling-load.json').write_text('{}')
    elif mutation == 'service':
        archive_report(directory, 'modeling', {'org.qopenbb.service': 'workspace'})
        digest = checksum(directory)
    elif mutation == 'load-id':
        path = directory / 'modeling-load.json'
        content = json.loads(path.read_text())
        content['loaded_image_id'] = 'sha256:' + '0' * 64
        path.write_text(json.dumps(content))
        digest = checksum(directory)
    else:
        data = NAMESPACE + '/qopenbb-data-api:latest'
    with pytest.raises(ValueError):
        publish_model_images.promote(directory, output, NAMESPACE, TAG, data, digest)
    assert commands == []
    assert not (output / 'images.json').exists()


def test_legacy_publication_path_does_not_accept_modeling(transfer):
    directory, _, commands = transfer
    report = json.loads((directory / 'modeling-load.json').read_text())
    with pytest.raises(ValueError, match='prototype runtime'):
        publication.publish(directory / 'modeling.tar', report, NAMESPACE + '/qopenbb-modeling', TAG)
    assert commands == []

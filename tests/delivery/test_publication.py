"""Publication verifies archive, daemon and registry identity before recording success."""

import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

import pytest

from qopenbb_ci import publication, publish_cli
from qopenbb_ci.images import inspect_archive

REMOTE = 'sha256:' + 'a' * 64
REPOSITORY = 'registry.example.invalid/owner/workspace'


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    labels = {'org.qopenbb.service': 'workspace', 'org.qopenbb.provenance.sha256': 'b' * 64}
    for name in ['workspace', 'data_api']:
        labels['org.qopenbb.source.' + name] = 'c' * 40
        labels['org.qopenbb.repository.' + name] = 'https://github.com/norandom/' + name + '.git'
    config = json.dumps({'architecture': 'amd64', 'os': 'linux', 'config': {'Labels': labels}}).encode()
    archive = tmp_path / 'image.tar'
    with tarfile.open(archive, 'w') as bundle:
        for name, content in {'manifest.json': json.dumps([{'Config': 'config.json', 'Layers': []}]).encode(),
                              'config.json': config}.items():
            member = tarfile.TarInfo(name)
            member.size = len(content)
            bundle.addfile(member, io.BytesIO(content))
    identity = inspect_archive(archive)
    state = {'commands': [], 'config': identity['image_config_digest'], 'digest': REMOTE,
             'architecture': 'amd64', 'immutable_digest': REMOTE, 'fail_push': False}

    def execute(command, **kwargs):
        state['commands'].append(command)
        arguments = command[1:]
        output = ''
        if arguments[:2] == ['image', 'load']:
            output = 'Loaded image ID: ' + identity['image_config_digest'] + '\n'
        elif arguments[:2] == ['image', 'inspect']:
            output = json.dumps([{'Id': identity['image_config_digest'], 'Architecture': 'amd64',
                                  'Os': 'linux', 'Config': {'Labels': labels}}])
        elif arguments[:2] == ['image', 'save']:
            shutil.copyfile(archive, arguments[3])
        elif arguments[:2] == ['image', 'push']:
            if state['fail_push']:
                raise subprocess.CalledProcessError(1, command, output='sensitive diagnostic')
            output = 'release-123: digest: ' + REMOTE + ' size: 123\n'
        elif arguments[:3] == ['manifest', 'inspect', '--verbose']:
            digest = state['immutable_digest'] if '@' in arguments[3] else state['digest']
            output = json.dumps({'Descriptor': {'digest': digest, 'platform': {
                'architecture': state['architecture'], 'os': 'linux'}},
                'SchemaV2Manifest': {'schemaVersion': 2, 'config': {'digest': state['config']}}})
        elif arguments[:2] != ['image', 'tag']:
            raise AssertionError(command)
        return subprocess.CompletedProcess(command, 0, stdout=output, stderr='')

    monkeypatch.setattr(subprocess, 'run', execute)
    monkeypatch.setattr(subprocess, 'check_output', lambda command, **kwargs: execute(command, **kwargs).stdout)
    report = {**identity, 'loaded_image_id': identity['image_config_digest']}
    return archive, report, state


def test_publish_reloads_exact_image_and_checks_immutable_remote(fixture):
    archive, report, state = fixture
    result = publication.publish(archive, report, REPOSITORY, 'release-123')
    assert result['reference'] == REPOSITORY + '@' + REMOTE
    assert ['docker', 'image', 'tag', report['loaded_image_id'], REPOSITORY + ':release-123'] in state['commands']
    assert state['commands'][-1][-1] == result['reference']
    assert result['sources']['workspace']['revision'] == 'c' * 40


@pytest.mark.parametrize('field,value', [('config', 'sha256:' + 'd' * 64),
    ('digest', 'sha256:' + 'd' * 64), ('architecture', 'arm64'),
    ('immutable_digest', 'sha256:' + 'e' * 64)])
def test_remote_mismatch_and_tag_race_fail(fixture, field, value):
    archive, report, state = fixture
    state[field] = value
    with pytest.raises(ValueError):
        publication.publish(archive, report, REPOSITORY, 'release-123')


@pytest.mark.parametrize('mutation', ['archive', 'labels', 'loaded_id'])
def test_bad_supplied_report_fails_before_docker(fixture, mutation):
    archive, report, state = fixture
    report = copy.deepcopy(report)
    if mutation == 'archive':
        report['archive_sha256'] = 'f' * 64
    elif mutation == 'labels':
        report['labels']['org.qopenbb.source.workspace'] = 'f' * 40
    else:
        report['loaded_image_id'] = 'invalid'
    with pytest.raises(ValueError):
        publication.publish(archive, report, REPOSITORY, 'release-123')
    assert not state['commands']


@pytest.mark.parametrize('repository,tag', [(REPOSITORY, 'latest'), (REPOSITORY, '../tag'),
    ('owner/image', 'release-123'), ('https://registry.invalid/image', 'release-123'),
    (REPOSITORY + ':old', 'release-123')])
def test_invalid_reference_fails_before_docker(fixture, repository, tag):
    archive, report, state = fixture
    with pytest.raises(ValueError):
        publication.publish(archive, report, repository, tag)
    assert not state['commands']


def test_cli_push_failure_writes_no_report_or_diagnostics(fixture, tmp_path, monkeypatch, capsys):
    archive, report, state = fixture
    state['fail_push'] = True
    loaded, output = tmp_path / 'load.json', tmp_path / 'publication.json'
    loaded.write_text(json.dumps(report))
    monkeypatch.setattr('sys.argv', ['publish', '--archive', str(archive), '--load-report', str(loaded),
        '--repository', REPOSITORY, '--tag', 'release-123', '--report', str(output)])
    assert publish_cli.main() == 2
    assert not output.exists()
    assert 'sensitive' not in capsys.readouterr().out

@pytest.mark.parametrize('schema', ['OCIManifest', 'SchemaV2Manifest'])
def test_remote_supports_observed_docker_schema(monkeypatch, schema):
    response = {'Descriptor': {'digest': REMOTE, 'platform': {'architecture': 'amd64', 'os': 'linux'}},
                schema: {'schemaVersion': 2, 'config': {'digest': 'sha256:' + 'c' * 64}}}
    monkeypatch.setattr(publication, 'docker', lambda *args: json.dumps(response))
    assert publication.remote_identity(REPOSITORY + '@' + REMOTE)['manifest_digest'] == REMOTE


def test_remote_multi_platform_result_rejected(monkeypatch):
    monkeypatch.setattr(publication, 'docker', lambda *args: '[{}]')
    with pytest.raises(ValueError, match='single remote'):
        publication.remote_identity(REPOSITORY + ':release-123')


def test_reloaded_id_mismatch_never_tags_or_pushes(fixture):
    archive, report, state = fixture
    report['loaded_image_id'] = 'sha256:' + 'e' * 64
    with pytest.raises(ValueError, match='reloaded'):
        publication.publish(archive, report, REPOSITORY, 'release-123')
    assert not any(command[1:3] in [['image', 'tag'], ['image', 'push']] for command in state['commands'])


def test_source_label_validation_rejects_placeholder_and_missing_provenance(fixture):
    _, report, _ = fixture
    for label, value in [('org.qopenbb.service', 'foundation-smoke'),
                         ('org.qopenbb.source.workspace', ''),
                         ('org.qopenbb.repository.workspace', 'https://github.com/other/project'),
                         ('org.qopenbb.provenance.sha256', '')]:
        identity = copy.deepcopy(report)
        identity['labels'][label] = value
        with pytest.raises(ValueError):
            publication.verify_sources(identity)

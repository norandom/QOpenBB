"""Resource and private-state fences precede lifecycle side effects."""
import json
import hashlib
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from qopenbb_ci import compose_lifecycle as lifecycle, session_files
from qopenbb_ci.runtime_descriptor import RuntimeDescriptor
from test_runtime_descriptor import valid_descriptor


def runtime(tmp_path):
    raw=valid_descriptor(tmp_path)
    raw['resources']['containers']['data-api']['id']='c'*64
    raw['state']['mount_identity']=hashlib.sha256(json.dumps({'source':'/mnt/state','destination':'/data','type':'bind','sentinel':raw['session_id']},sort_keys=True).encode()).hexdigest()
    descriptor=RuntimeDescriptor.model_validate(raw)
    calls=[]
    def command(args, **kwargs):
        calls.append(args)
        if args[0]=='ps': return '\n'.join(x.id for x in descriptor.resources.containers.values())
        if args[:2]==['network','ls']: return 'd'*64
        if args[:2]==['network','inspect']:
            resource=descriptor.resources.networks[0]
            return json.dumps([{'Id':resource.id,'Labels':resource.labels}])
        if args[0]=='inspect':
            service=next(k for k,v in descriptor.resources.containers.items() if v.id==args[1])
            resource=descriptor.resources.containers[service]
            mounts=[{'Type':'bind','Destination':'/data','RW':True,'Source':'/mnt/state'}] if service=='workspace' else []
            return json.dumps([{'Id':resource.id,'Config':{'Labels':resource.labels},'Image':descriptor.images[service],'Mounts':mounts}])
        raise AssertionError(args)
    return SimpleNamespace(descriptor=descriptor,command=command, calls=calls)


def test_inventory_checks_exact_resources_without_mutation(tmp_path):
    owned=runtime(tmp_path)
    containers,networks=lifecycle.inventory(owned)
    assert set(containers)=={'workspace','data-api'} and networks==['d'*64]
    assert not any(args[0] in {'rm','exec'} for args in owned.calls)


@pytest.mark.parametrize('mutation',['mount','label','image','id','replacement'])
def test_tampered_resources_refuse_before_removal(tmp_path,mutation):
    owned=runtime(tmp_path)
    original=owned.command
    def tamper(args,**kwargs):
        result=original(args,**kwargs)
        if mutation=='replacement' and args[0]=='ps' and '--filter' in args:
            return result+'\n'+'e'*64
        if args[0]!='inspect':return result
        value=json.loads(result)[0]
        if mutation=='mount':value['Mounts']=[]
        if mutation=='label':value['Config']['Labels']['org.qopenbb.session']='other'
        if mutation=='image':value['Image']='sha256:'+'f'*64
        if mutation=='id':value['Id']='e'*64
        return json.dumps([value])
    owned.command=tamper
    with pytest.raises(ValueError):lifecycle.inventory(owned)
    assert not any(args[0]=='rm' for args in owned.calls)


def test_missing_resources_cleanup_is_repeatable(tmp_path):
    owned=runtime(tmp_path)
    owned.command=lambda *args,**kwargs:''
    assert lifecycle.inventory(owned)==({},[])
    lifecycle.remove_resources(owned,{},[])


@pytest.mark.skipif(os.name != 'nt', reason='POSIX checked directory removal fails closed')
def test_private_state_removal_and_repeated_absence(tmp_path):
    state=tmp_path/'private'
    with session_files.create_session(state) as directory:
        directory.create_file('qopenbb-sentinel',b'owned')
        directory.create_file('marker',b'retained')
    owned=SimpleNamespace(descriptor=SimpleNamespace(state=SimpleNamespace(host_path=str(state))))
    lifecycle.remove_state_files(owned)
    assert not state.exists()
    lifecycle.remove_state_files(owned)


def test_nested_state_refused_before_any_file_deleted(tmp_path):
    state=tmp_path/'private'
    with session_files.create_session(state) as directory:
        directory.create_file('qopenbb-sentinel',b'owned')
        directory.create_file('marker',b'retained')
    (state/'nested').mkdir()
    owned=SimpleNamespace(descriptor=SimpleNamespace(state=SimpleNamespace(host_path=str(state))))
    with pytest.raises((OSError,ValueError),match='State retained|not supported'):lifecycle.remove_state_files(owned)
    assert session_files.read_private(state/'marker')==b'retained'
    assert session_files.read_private(state/'qopenbb-sentinel')==b'owned'


def test_wrong_daemon_fails_before_configuration_or_resource_mutation(tmp_path,monkeypatch):
    owned=runtime(tmp_path)
    config=SimpleNamespace(environment={'CONTAINER_HOST':'wrong'})
    monkeypatch.setattr(lifecycle,'validate_output',lambda p:p)
    monkeypatch.setattr(lifecycle,'read_private',lambda p:owned.descriptor)
    monkeypatch.setattr(lifecycle.ComposeRuntime,'command',lambda *a,**k:json.dumps({'ID':'daemon-id'}))
    check=Mock()
    monkeypatch.setattr(lifecycle.ComposeRuntime,'verify_configuration',check)
    with pytest.raises(ValueError,match='daemon identity'):lifecycle.load(config,tmp_path/'descriptor')
    check.assert_not_called()


def test_recreate_commits_new_ids_only_after_readiness(tmp_path,monkeypatch):
    from qopenbb_ci import compose_readiness
    from qopenbb_ci.compose_runtime import ComposeRuntime
    owned=runtime(tmp_path)
    private=tmp_path/'session'
    with session_files.create_session(private):pass
    current=ComposeRuntime(None,private/'descriptor')
    current.descriptor=owned.descriptor
    durable=[]
    def persist(**updates):
        lifecycle.memory_update(current,updates)
        durable.append(current.descriptor.model_copy(deep=True))
    current.save=persist
    current.command=lambda *args,**kwargs:''
    current.invocation=lambda *args:list(args)
    def discover():
        raw=current.descriptor.model_dump(mode='json')
        raw['resources']['containers']['workspace']['id']='f'*64
        raw['resources']['containers']['data-api']['id']='e'*64
        raw['container']='f'*64
        current.save(**raw)
    current.discover=discover
    monkeypatch.setattr(lifecycle,'load',lambda *args:current)
    monkeypatch.setattr(lifecycle,'inventory',lambda value:({'workspace':{'Id':'b'*64},'data-api':{'Id':'c'*64}},['d'*64]))
    monkeypatch.setattr(lifecycle,'remove_resources',lambda *args:None)
    def ready(value):
        assert durable[-1].phase=='recreating'
        assert durable[-1].container=='b'*64
        assert value.descriptor.container=='f'*64
        value.save(credentials=value.descriptor.credentials.model_dump())
        assert len(durable)==1
    monkeypatch.setattr(compose_readiness,'ready',ready)
    result=lifecycle.recreate(None,tmp_path/'descriptor')
    assert [item.phase for item in durable]==['recreating','ready']
    assert result.container=='f'*64
    assert result.origin==owned.descriptor.origin and result.images==owned.descriptor.images
    assert result.state==owned.descriptor.state


def test_partial_recovery_refuses_replacement_without_recording(tmp_path,monkeypatch):
    owned=runtime(tmp_path)
    owned.descriptor=owned.descriptor.model_copy(update={'phase':'failed'})
    raw=owned.descriptor.model_dump(mode='json')
    raw['resources']['containers']['workspace']['id']='e'*64
    raw['container']='e'*64
    candidate=RuntimeDescriptor.model_validate(raw)
    monkeypatch.setattr(lifecycle,'rediscover',lambda value:candidate)
    owned.save=Mock()
    with pytest.raises(ValueError,match='Replacement'):lifecycle.recover(owned)
    owned.save.assert_not_called()
    assert owned.descriptor.container=='b'*64


def test_interrupted_recreation_recovers_only_journaled_replacements(tmp_path, monkeypatch):
    owned=runtime(tmp_path)
    private=tmp_path/'session'
    with session_files.create_session(private):pass
    state=private/'state'
    with session_files.create_session(state):pass
    owned.path=private/'descriptor.json'
    owned.descriptor=owned.descriptor.model_copy(update={'state':owned.descriptor.state.model_copy(update={'host_path':str(state)})})
    owned.descriptor=owned.descriptor.model_copy(update={'phase':'recreating'})
    intent=lifecycle.recreation_intent(owned.descriptor)
    with session_files.PrivateDirectory.open(private) as directory:
        directory.create_file('recreation-intent.json',json.dumps(intent).encode())
    raw=owned.descriptor.model_dump(mode='json')
    raw['resources']['containers']['workspace']['id']='e'*64
    raw['resources']['containers']['data-api']['id']='f'*64
    raw['container']='e'*64
    candidate=RuntimeDescriptor.model_validate(raw)
    monkeypatch.setattr(lifecycle,'rediscover',lambda value:candidate)
    verified=[]
    def inspect_candidate(value):
        verified.append(value.descriptor)
        return ({service:{'Id':resource.id} for service,resource in value.descriptor.resources.containers.items()},['d'*64])
    monkeypatch.setattr(lifecycle,'inventory',inspect_candidate)
    owned.save=lambda **updates:lifecycle.memory_update(owned,updates)
    marker=state/'retained-marker'
    with session_files.PrivateDirectory.open(state) as directory:
        directory.create_file(marker.name,b'retained-state')
    monkeypatch.setattr(lifecycle,'load',lambda *args:owned)
    removed=[]
    monkeypatch.setattr(lifecycle,'remove_resources',lambda *args:removed.append(args))
    result=lifecycle.stop(None,owned.path)
    assert verified[0]==candidate
    assert owned.descriptor.phase=='stopped' and owned.descriptor.container=='e'*64
    assert owned.descriptor.state==candidate.state
    assert result['state_removed'] is False and len(removed)==1
    assert {item['Id'] for item in removed[0][1].values()}=={'e'*64,'f'*64}
    assert session_files.read_private(marker)==b'retained-state'
    assert not (private/'recreation-intent.json').exists()


def test_interrupted_recreation_missing_journal_refuses(tmp_path,monkeypatch):
    owned=runtime(tmp_path)
    owned.path=tmp_path/'descriptor.json'
    owned.descriptor=owned.descriptor.model_copy(update={'phase':'recreating'})
    discovery=Mock()
    monkeypatch.setattr(lifecycle,'rediscover',discovery)
    with pytest.raises(ValueError,match='intent'):lifecycle.recover(owned)
    discovery.assert_not_called()


@pytest.mark.parametrize('mutation', ['stale_session', 'extra_field', 'untyped_version', 'old_ids'])
def test_recreation_journal_must_match_exact_original(tmp_path, monkeypatch, mutation):
    owned=runtime(tmp_path)
    private=tmp_path/'session'
    with session_files.create_session(private):pass
    owned.path=private/'descriptor.json'
    owned.descriptor=owned.descriptor.model_copy(update={'phase':'recreating'})
    intent=lifecycle.recreation_intent(owned.descriptor)
    if mutation=='stale_session':intent['session_id']='c'*32
    if mutation=='extra_field':intent['unexpected']=True
    if mutation=='untyped_version':intent['schema_version']=True
    if mutation=='old_ids':intent['resources']['containers']['workspace']['id']='e'*64
    with session_files.PrivateDirectory.open(private) as directory:
        directory.create_file('recreation-intent.json',json.dumps(intent).encode())
    discovery=Mock()
    monkeypatch.setattr(lifecycle,'rediscover',discovery)
    with pytest.raises(ValueError,match='intent'):lifecycle.recover(owned)
    discovery.assert_not_called()


def test_recovered_mount_failure_never_rewrites_ownership(tmp_path,monkeypatch):
    owned=runtime(tmp_path)
    before=owned.descriptor
    candidate=before.model_copy(update={'phase':'failed'})
    monkeypatch.setattr(lifecycle,'rediscover',lambda value:candidate)
    owned.descriptor=candidate
    owned.save=Mock()
    def reject(value):
        raise ValueError('Runtime mount source changed')
    monkeypatch.setattr(lifecycle,'inventory',reject)
    with pytest.raises(ValueError,match='mount'):lifecycle.recover(owned)
    owned.save.assert_not_called()
    assert owned.descriptor==candidate


@pytest.mark.skipif(os.name == 'nt', reason='POSIX-only fail-closed removal contract')
def test_posix_explicit_removal_preserves_all_entries(tmp_path):
    state=tmp_path/'private'
    with session_files.create_session(state) as directory:
        directory.create_file('qopenbb-sentinel',b'owned')
        directory.create_file('marker',b'retained')
    owned=SimpleNamespace(descriptor=SimpleNamespace(state=SimpleNamespace(host_path=str(state))))
    with pytest.raises(OSError,match='not supported'):lifecycle.remove_state_files(owned)
    assert session_files.read_private(state/'marker')==b'retained'

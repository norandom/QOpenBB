"""Raw selected SDK admission, using native maps and generated public methods."""
import pytest


def test_scoped_frame_is_absent_between_calls():
    from openbb_core.app.static.utils.admission_context import current_frame
    assert current_frame() is None


def test_marker_is_owned_by_exact_selected_class():
    from openbb_core.app.parameter_admission import opted_in
    from fmp_a1_contracts import FMPPriceTargetQueryParams
    class Selected(FMPPriceTargetQueryParams):
        __qopenbb_strict_admission__ = True
        model_config = {'extra': 'forbid'}
    class Inherited(Selected):
        pass
    assert opted_in(Selected, 'fmp')
    assert not opted_in(Inherited, 'fmp')
    assert not opted_in(Selected, 'other')

import inspect
from collections import OrderedDict
from typing import Any, Annotated, Literal, Optional, Union

from openbb_core.app.model.abstract.singleton import SingletonMeta
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.model.system_settings import SystemSettings
from openbb_core.app.model.user_settings import UserSettings
from openbb_core.app.provider_interface import ProviderInterface, ProviderChoices, StandardParams, ExtraParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router, RouterLoader, CommandMap
from openbb_core.app.static.container import Container
from openbb_core.app.static.package_builder.method_definition import MethodDefinition
from openbb_core.app.static.package_builder.path_handler import PathHandler
from openbb_core.app.static.utils.decorators import validate, exception_handler
from openbb_core.app.static.utils.filters import filter_inputs
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.provider import Provider
from openbb_core.provider.registry import Registry
from openbb_core.provider.registry_map import RegistryMap
from fmp_freeze_support import CONTRACTS, describe, standard
from copy import deepcopy
from pydantic import create_model, field_validator, model_validator
from fastapi import Query as FastAPIQuery
from openbb_core.app.model.field import OpenBBField


def fetcher_for(query, row, calls):
    class Dedicated(Fetcher[query, list[row]]):
        require_credentials = False
        @staticmethod
        def transform_query(params):
            return query.model_validate(params)
        @staticmethod
        def extract_data(query, credentials, **kwargs):
            calls.append(query.model_dump(mode='json'))
            return []
        @staticmethod
        def transform_data(query, data, **kwargs):
            return data
    return Dedicated


def registered_query(name, query):
    validators = {}
    for key, decorator in query.__pydantic_decorators__.field_validators.items():
        function = getattr(decorator.func, '__func__', decorator.func)
        validators[key] = field_validator(*decorator.info.fields, mode=decorator.info.mode)(classmethod(function))
    for key, decorator in query.__pydantic_decorators__.model_validators.items():
        function = getattr(decorator.func, '__func__', decorator.func)
        if decorator.info.mode == 'before':
            function = classmethod(function)
        validators[key] = model_validator(mode=decorator.info.mode)(function)
    fields = {key:(info.annotation, deepcopy(info)) for key,info in query.model_fields.items()}
    result = create_model('Dedicated'+name, __base__=standard(name), __module__=__name__,
                          __validators__=validators, **fields)
    result.model_config = dict(query.model_config, title=query.__name__)
    result.__qopenbb_strict_admission__ = True
    result.model_rebuild(force=True)
    return result


@pytest.fixture
def native(monkeypatch):
    calls = []
    registry = Registry()
    models = {}
    descriptors = describe()['adapters']
    for name, (query, row) in CONTRACTS.items():
        selected = registered_query(name, query)
        models[descriptors[name]['model_key']] = fetcher_for(selected, row, calls)
    registry.include_provider(Provider('fmp', 'dedicated offline', fetcher_dict=models))
    registry.include_provider(Provider('other', 'baseline offline', fetcher_dict=models))
    interface = object.__new__(ProviderInterface)
    interface.__init__(RegistryMap(registry))
    monkeypatch.setitem(SingletonMeta._instances, ProviderInterface, interface)
    router = Router()
    paths = {}
    for name, data in descriptors.items():
        async def command(cc: CommandContext, provider_choices: ProviderChoices,
                          standard_params: StandardParams, extra_params: ExtraParams) -> OBBject:
            return await OBBject.from_query(Query(**locals()))
        command.__name__ = name
        router.command(model=data['model_key'], path='/'+name)(command)
        paths[name] = '/'+name
    monkeypatch.setattr(RouterLoader, 'from_extensions', staticmethod(lambda: router))
    from openbb_core.app.command_runner import CommandRunner, ExecutionContext
    monkeypatch.setattr(ExecutionContext, '_route_map', PathHandler.build_route_map())
    runner = CommandRunner(CommandMap(router), SystemSettings(), UserSettings.model_construct())
    methods = {}
    for name, path in paths.items():
        command = runner.command_map.get_command(path)
        formatted = MethodDefinition.format_params(path, dict(inspect.signature(command).parameters), command)
        source = 'class Public(Container):\n' + MethodDefinition.build_command_method_signature('execute', formatted, Any, path)
        source += MethodDefinition.build_command_method_body(path, command, formatted)
        namespace = dict(globals())
        exec(source, namespace)
        methods[name] = namespace['Public'](runner).execute
    return methods, runner, calls


@pytest.mark.parametrize('name', CONTRACTS)
def test_native_generated_all_variants_accept_valid_and_reject_raw(native, name):
    methods, runner, calls = native
    method = methods[name]
    method(symbol='MSFT', provider='fmp')
    assert calls[-1]['symbol'] == 'MSFT'
    method('MSFT', provider='fmp')
    assert calls[-1]['symbol'] == 'MSFT'
    query = CONTRACTS[name][0]
    bad = [{'symbol':'MSFT','chart_params':{}}, {'symbol':'MSFT','RAW_KEY_SENTINEL':False}, {'symbol': True}, {'symbol':None}, {}]
    for field in ('limit', 'page'):
        if field in query.model_fields:
            bad += [dict(symbol='MSFT', **{field:value}) for value in (None, True, False, -1, 10001, 'RAW_VALUE_SENTINEL')]
    before = len(calls)
    for payload in bad:
        with pytest.raises(Exception) as error:
            method(provider='fmp', **payload)
        assert str(error.value) == 'invalid_parameters'
        assert error.value.__cause__ is None
    assert len(calls) == before


def test_native_selected_effective_defaults_preserve_caller_precedence(native):
    methods, runner, calls = native
    runner.user_settings.defaults.commands['price_target'] = {'provider':['fmp'], 'limit':9}
    method = methods['price_target']
    method(symbol='MSFT', limit=4)
    assert calls[-1]['limit'] == 4
    method(symbol='MSFT')
    assert calls[-1]['limit'] == 9
    for value in (True, None, 0, 101, 'RAW_VALUE_SENTINEL'):
        runner.user_settings.defaults.commands['price_target']['limit'] = value
        before = len(calls)
        with pytest.raises(Exception, match='^invalid_parameters$'):
            method(symbol='MSFT')
        assert len(calls) == before


import datetime



@pytest.mark.parametrize('name', CONTRACTS)
def test_registered_query_preserves_frozen_schema_and_validators(name):
    query = CONTRACTS[name][0]
    dedicated = registered_query(name, query)
    for mode in ('validation', 'serialization'):
        assert dedicated.model_json_schema(mode=mode) == query.model_json_schema(mode=mode)
    assert dedicated.model_validate({'symbol':'msft'}).symbol == 'MSFT'


def test_provider_selection_native_priority_and_one_resolution(native, monkeypatch):
    methods, runner, calls = native
    credentials = runner.user_settings.credentials
    monkeypatch.setattr(type(credentials), 'origins', {'fmp':[], 'other':['not_present']})
    checks = []
    original = Container._check_credentials
    def check(self, provider):
        checks.append(provider)
        return original(self, provider)
    monkeypatch.setattr(Container, '_check_credentials', check)
    methods['price_target'](symbol='MSFT')
    assert checks == ['fmp']
    assert calls[-1]['limit'] == 20
    runner.user_settings.defaults.commands['price_target'] = {'provider':['other','fmp']}
    checks.clear()
    methods['price_target'](symbol='MSFT')
    assert checks == ['other','fmp']
    assert calls[-1]['limit'] == 20


def test_other_provider_and_nonopted_class_retain_native_coercion(native, monkeypatch):
    methods, runner, calls = native
    method = methods['price_target']
    method(symbol='MSFT', provider='other', limit=True)
    assert calls[-1]['limit'] == 1
    query = ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    monkeypatch.setattr(query, '__qopenbb_strict_admission__', False)
    method(symbol='MSFT', provider='fmp', limit=True)
    assert calls[-1]['limit'] == 1


@pytest.mark.parametrize('debug', [False, True])
def test_selected_safe_errors_debug_binding_and_input_immutability(native, monkeypatch, debug):
    from openbb_core.env import Env
    from openbb_core.app.static.utils.admission_context import current_frame
    monkeypatch.setitem(Env()._environ, 'OPENBB_DEBUG_MODE', str(debug).lower())
    assert Env().DEBUG_MODE is debug
    methods, runner, calls = native
    method = methods['price_target']
    payload = {'symbol':'MSFT', 'provider':'fmp','RAW_KEY_SENTINEL':{'RAW_VALUE_SENTINEL':True}}
    original = deepcopy(payload)
    before = len(calls)
    for args, kwargs in (((),payload), (('MSFT',),{'symbol':'MSFT','provider':'fmp'}),
                         ((), {'symbol':['MSFT','ORCL'],'provider':'fmp'})):
        with pytest.raises(Exception) as error:
            method(*args, **kwargs)
        assert str(error.value) == 'invalid_parameters'
        assert error.value.__cause__ is None
        assert current_frame() is None
    assert payload == original
    assert len(calls) == before


def test_unsupported_standard_defaults_and_controls(native):
    methods, runner, calls = native
    method = methods['price_target_consensus']
    before = len(calls)
    for kwargs in ({'limit':None}, {'page':0}, {'chart_params':{}}, {'RAW_KEY_SENTINEL':False}):
        with pytest.raises(Exception, match='^invalid_parameters$'):
            method(symbol='MSFT', provider='fmp', **kwargs)
    assert len(calls) == before


def test_positional_and_alias_collision(native, monkeypatch):
    methods, runner, calls = native
    method = methods['price_target']
    assert str(inspect.signature(method)).startswith('(symbol:')
    method('MSFT', limit=7, provider='fmp')
    assert calls[-1]['limit'] == 7
    query = ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    monkeypatch.setattr(query.model_fields['limit'], 'validation_alias', 'cap')
    query.model_rebuild(force=True)
    try:
        with pytest.raises(Exception, match='^invalid_parameters$'):
            method('MSFT', limit=7, cap=7, provider='fmp')
        method('MSFT', cap=7, provider='fmp')
        assert calls[-1]['limit'] == 7
    finally:
        query.model_fields['limit'].validation_alias = None
        query.model_rebuild(force=True)


def test_configured_unknown_and_date_defaults_stop_before_extraction(native):
    methods, runner, calls = native
    for name, defaults in [('price_target', {'RAW_KEY_SENTINEL':False}),
                           ('historical_market_cap', {'start_date':'not-a-date'}),
                           ('historical_market_cap', {'start_date':'2025-02-01','end_date':'2025-01-01'})]:
        runner.user_settings.defaults.commands[name] = defaults
        before = len(calls)
        with pytest.raises(Exception, match='^invalid_parameters$'):
            methods[name](symbol='MSFT', provider='fmp')
        assert len(calls) == before



def test_context_cleanup_nested_calls_and_raw_cleared_before_execution(native, monkeypatch):
    from openbb_core.app.static.utils.admission_context import FRAME, current_frame
    methods, runner, calls = native
    outer = methods['price_target']
    query = ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    original = query.model_validate
    frames = []
    def nested(values, **kwargs):
        frame = current_frame()
        if frame is not None and not frames:
            frames.append(frame)
            methods['price_target_consensus'](symbol='ORCL',provider='fmp')
            assert current_frame() is frame
            methods['price_target_consensus'](symbol='ADBE',provider='other')
            assert current_frame() is frame
        return original(values, **kwargs)
    monkeypatch.setattr(query, 'model_validate', nested)
    original_run = runner.sync_run
    def run(*args, **kwargs):
        assert FRAME.get() is None
        assert all(frame.raw == {} for frame in frames)
        return original_run(*args, **kwargs)
    monkeypatch.setattr(runner, 'sync_run', run)
    outer(symbol='MSFT',provider='fmp')
    assert len(calls) == 3
    assert current_frame() is None
    assert frames[0].consumed and frames[0].executing
    assert frames[0].raw == {}


def test_parallel_public_calls_do_not_share_raw_or_provider(native):
    from concurrent.futures import ThreadPoolExecutor
    from openbb_core.app.static.utils.admission_context import current_frame
    methods, runner, calls = native
    def call(symbol):
        methods['price_target'](symbol=symbol,provider='fmp')
        assert current_frame() is None
    with ThreadPoolExecutor(max_workers=2) as workers:
        list(workers.map(call,['MSFT','ORCL']))
    assert sorted(item['symbol'] for item in calls) == ['MSFT','ORCL']


def test_inherited_child_context_cannot_adopt_frame_and_nested_task_isolated(native):
    import asyncio
    from openbb_core.app.static.utils.admission_context import AdmissionFrame, FRAME, current_frame, consume, InvalidParameters
    methods, runner, calls = native
    container = methods['price_target'].__self__
    query = ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    async def main():
        frame = AdmissionFrame(container,'/price_target','PriceTarget',query,'fmp','fmp',('fmp','other'),{'symbol':'PRIVATE'},frozenset({'provider'}))
        token = FRAME.set(frame)
        async def child():
            assert current_frame() is None
            with pytest.raises(InvalidParameters):
                consume(container,'/price_target','fmp')
            methods['price_target'](symbol='ORCL',provider='fmp')
            assert current_frame() is None
        try:
            await asyncio.create_task(child())
            assert current_frame() is frame
            assert frame.raw == {'symbol':'PRIVATE'}
        finally:
            frame.raw.clear()
            FRAME.reset(token)
    asyncio.run(main())
    assert calls[-1]['symbol'] == 'ORCL'
    assert current_frame() is None


def test_scoped_frame_consume_and_provider_reuse_fail_closed(native):
    from openbb_core.app.static.utils.admission_context import AdmissionFrame, FRAME, matching_selection, consume, InvalidParameters
    methods, runner, calls = native
    container = methods['price_target'].__self__
    query = ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    def frame():
        return AdmissionFrame(container,'/price_target','PriceTarget',query,'fmp',None,('fmp','other'),{},frozenset({'provider'}))
    for mismatch in [(object(),None,'price_target',('fmp','other')), (container,'fmp','price_target',('fmp','other')),
                     (container,None,'wrong',('fmp','other')), (container,None,'price_target',('other','fmp'))]:
        token = FRAME.set(frame())
        try:
            with pytest.raises(InvalidParameters):
                matching_selection(*mismatch)
        finally:
            FRAME.reset(token)
    selected = frame()
    token = FRAME.set(selected)
    try:
        assert matching_selection(container,None,'price_target',('fmp','other')) is selected
        assert consume(container,'/price_target','fmp') is selected
        with pytest.raises(InvalidParameters):
            consume(container,'/price_target','fmp')
        with pytest.raises(InvalidParameters):
            matching_selection(container,None,'price_target',('fmp','other'))
    finally:
        FRAME.reset(token)


def test_actual_async_selected_wrapper_lifecycle(native):
    import asyncio
    from openbb_core.app.static.utils.admission_context import current_frame
    methods, runner, calls = native
    container = methods['price_target'].__self__
    @validate(_command_path='/price_target')
    async def asynchronous(self, symbol: str, provider: str | None = None, **kwargs):
        frame = current_frame()
        assert frame is not None
        await asyncio.sleep(0)
        assert current_frame() is frame
        if symbol == 'FAIL':
            raise ValueError('PRIVATE_SENTINEL')
        return symbol
    async def main():
        first = asynchronous(container,'MSFT','fmp')
        assert current_frame() is None
        task = asyncio.create_task(first)
        assert await asyncio.gather(task, asynchronous(container,'ORCL','fmp')) == ['MSFT','ORCL']
        assert current_frame() is None
        with pytest.raises(Exception, match='^invalid_parameters$'):
            await asynchronous(container,'FAIL','fmp')
        assert current_frame() is None
    asyncio.run(main())


def test_selected_filter_failure_safe_and_transport_failure_not_remapped(native, monkeypatch):
    from openbb_core.app.static.utils.admission_context import current_frame
    methods, runner, calls = native
    method = methods['price_target']
    body = inspect.unwrap(method)
    def bad_filter(**kwargs):
        raise ValueError('RAW_FILTER_SENTINEL')
    original = body.__globals__['filter_inputs']
    monkeypatch.setitem(body.__globals__,'filter_inputs',bad_filter)
    with pytest.raises(Exception, match='^invalid_parameters$'):
        method(symbol='MSFT',provider='fmp')
    assert calls == []
    assert current_frame() is None
    monkeypatch.setitem(body.__globals__,'filter_inputs',original)
    fetcher = ProviderInterface()._registry_map.registry.providers['fmp'].fetcher_dict['PriceTarget']
    def transport(**kwargs):
        raise RuntimeError('TRANSPORT_FAILURE')
    monkeypatch.setattr(fetcher, 'extract_data', staticmethod(transport))
    with pytest.raises(Exception) as error:
        method(symbol='MSFT',provider='fmp')
    assert 'invalid_parameters' not in str(error.value)
    assert 'TRANSPORT_FAILURE' in str(error.value)
    assert current_frame() is None


class DataFrame:
    pass


def test_emitted_metadata_retains_signature_and_arbitrary_types(native):
    params = OrderedDict(data=inspect.Parameter('data',inspect.Parameter.POSITIONAL_OR_KEYWORD,annotation='DataFrame'))
    code = 'class Public:\n' + MethodDefinition.build_command_method_signature('execute',params,Any,'/price_target')
    code += '        return data\n'
    namespace = dict(globals(), DataFrame=DataFrame)
    exec(code,namespace)
    method = namespace['Public']().execute
    frame = DataFrame()
    assert method(frame) is frame
    assert list(inspect.signature(method).parameters) == ['data']





def test_native_validation_failure_is_safe_without_undecorated_rescue(native):
    from openbb_core.app.static.utils.admission_context import current_frame
    methods, runner, calls = native
    container = methods['price_target'].__self__
    bodies = []
    @validate(_command_path='/price_target')
    def mismatched_native(self, symbol: str, limit: str, provider: str, **kwargs):
        bodies.append(True)
    with pytest.raises(Exception) as error:
        mismatched_native(container, symbol='MSFT', limit=7, provider='fmp')
    assert str(error.value) == 'invalid_parameters'
    assert bodies == [] and calls == []
    assert current_frame() is None


def test_selected_filter_cannot_change_resolved_provider(native, monkeypatch):
    methods, runner, calls = native
    body = inspect.unwrap(methods['price_target'])
    original = body.__globals__['filter_inputs']
    def wrong_provider(**kwargs):
        output = original(**kwargs)
        output['provider_choices']['provider'] = 'other'
        return output
    monkeypatch.setitem(body.__globals__, 'filter_inputs', wrong_provider)
    with pytest.raises(Exception, match='^invalid_parameters$'):
        methods['price_target'](symbol='MSFT',provider='fmp')
    assert calls == []


def test_valid_effective_dates_are_iso_and_unknown_defaults_reject(native):
    methods, runner, calls = native
    runner.user_settings.defaults.commands['historical_market_cap'] = {'start_date':'2025-01-01','end_date':'2025-01-03'}
    methods['historical_market_cap'](symbol='MSFT', provider='fmp')
    assert calls[-1]['start_date'] == '2025-01-01'
    assert calls[-1]['end_date'] == '2025-01-03'
    runner.user_settings.defaults.commands['analyst_estimates'] = {'page':True}
    before = len(calls)
    with pytest.raises(Exception, match='^invalid_parameters$'):
        methods['analyst_estimates'](symbol='MSFT',provider='fmp')
    assert len(calls) == before


def test_exact_eleven_native_registered_queries_own_the_opt_in(native):
    from openbb_core.app.parameter_admission import opted_in
    original = ProviderInterface()._registry_map.original_models
    expected = {item['model_key'] for item in describe()['adapters'].values()}
    actual = {model for model, variants in original.items() if opted_in(variants['fmp']['query'],'fmp')}
    assert actual == expected and len(actual) == 11
    assert len({original[model]['fmp']['query'] for model in actual}) == 11


def test_unselected_async_decorator_retains_native_call_timing():
    import asyncio
    from openbb_core.app.static.utils.admission_context import current_frame
    @validate(_command_path='/unregistered')
    async def baseline(value: int):
        return value
    assert not inspect.iscoroutinefunction(baseline)
    coroutine = baseline('7')
    assert inspect.iscoroutine(coroutine)
    assert asyncio.run(coroutine) == 7
    assert current_frame() is None


@pytest.mark.parametrize('name', CONTRACTS)
def test_supplied_pass_allows_absent_required_without_inserting_defaults(native, name):
    from openbb_core.app.parameter_admission import select_frame, supplied
    method = native[0][name]
    func = inspect.unwrap(method)
    args = (method.__self__,)
    frame = select_frame(func, '/'+name, args, {'provider':'fmp'})
    supplied(frame, func, args, {'provider':'fmp'})
    assert frame.raw == {}
    for field in ('limit','page'):
        if field in frame.query.model_fields:
            with pytest.raises(Exception, match='^invalid_parameters$'):
                supplied(frame,func,args,{'provider':'fmp',field:None})


def test_omitted_baseline_provider_resolves_once(native, monkeypatch):
    methods,runner,calls = native
    monkeypatch.setattr(type(runner.user_settings.credentials),'origins',{'other':[],'fmp':[]})
    runner.user_settings.defaults.commands['price_target']={'provider':['other','fmp']}
    checks=[]
    original=Container._check_credentials
    def check(self,provider):
        checks.append(provider)
        return original(self,provider)
    monkeypatch.setattr(Container,'_check_credentials',check)
    methods['price_target'](symbol='MSFT',limit=7)
    assert checks == ['other']
    assert calls[-1]['limit'] == 7


def test_omitted_provider_cannot_drift_into_fmp_after_raw_coercion(native, monkeypatch):
    methods,runner,calls = native
    runner.user_settings.defaults.commands['price_target']={'provider':['other','fmp']}
    checks=[]
    extracted=[]
    providers=ProviderInterface()._registry_map.registry.providers
    base=providers['fmp'].fetcher_dict['PriceTarget']
    original_extract=base.extract_data
    class BaselineFetcher(base):
        @staticmethod
        def extract_data(query,credentials,**kwargs):
            extracted.append('other')
            return original_extract(query,credentials,**kwargs)
    monkeypatch.setattr(providers['other'],'fetcher_dict',dict(providers['other'].fetcher_dict,PriceTarget=BaselineFetcher))
    def forbidden_fmp(**kwargs):
        extracted.append('fmp')
        raise AssertionError('FMP extraction bypassed strict raw admission')
    monkeypatch.setattr(base,'extract_data',staticmethod(forbidden_fmp))
    def changing(self,provider):
        checks.append(provider)
        return len(checks) == 1 or provider == 'fmp'
    monkeypatch.setattr(Container,'_check_credentials',changing)
    methods['price_target'](symbol='MSFT',limit=True)
    assert checks == ['other']
    assert extracted == ['other']
    assert calls[-1]['limit'] == 1


def test_omitted_native_validation_precedes_any_provider_resolution(native, monkeypatch):
    from openbb_core.app.static.utils.admission_context import current_frame
    methods,runner,calls = native
    checks=[]
    def missing(self,provider):
        checks.append(provider)
        return False
    monkeypatch.setattr(Container,'_check_credentials',missing)
    with pytest.raises(Exception) as error:
        methods['price_target'](symbol='MSFT',limit='NATIVE_INVALID_LIMIT')
    assert checks == []
    assert 'Provider fallback failed' not in str(error.value)
    assert 'NATIVE_INVALID_LIMIT' in str(error.value)
    assert current_frame() is None and calls == []


@pytest.mark.parametrize('name,payload', [('price_target',{'symbol':'MSFT','limit':'NATIVE_SENTINEL'}), ('analyst_estimates',{})])
@pytest.mark.parametrize('debug',[False,True])
def test_pending_failure_matches_nonopted_native_error_order(native,monkeypatch,name,payload,debug):
    from openbb_core.env import Env
    from openbb_core.app.static.utils.admission_context import current_frame
    methods,runner,calls=native
    monkeypatch.setitem(Env()._environ,'OPENBB_DEBUG_MODE',str(debug).lower())
    checks=[]
    def unavailable(self,provider):
        checks.append(provider)
        return False
    monkeypatch.setattr(Container,'_check_credentials',unavailable)
    with pytest.raises(Exception) as staged:
        methods[name](**payload)
    assert checks == [] and current_frame() is None
    model=describe()['adapters'][name]['model_key']
    query=ProviderInterface()._registry_map.original_models[model]['fmp']['query']
    monkeypatch.setattr(query,'__qopenbb_strict_admission__',False)
    with pytest.raises(Exception) as baseline:
        methods[name](**payload)
    assert type(staged.value) is type(baseline.value)
    assert str(staged.value) == str(baseline.value)
    assert checks == [] and current_frame() is None and calls == []


def test_selected_omitted_provider_checks_original_boolean_before_filter(native,monkeypatch):
    from openbb_core.app.static.utils.admission_context import current_frame
    methods,runner,calls=native
    runner.user_settings.defaults.commands['price_target']={'provider':['other','fmp']}
    checks=[]
    def available(self,provider):
        checks.append(provider)
        return provider == 'fmp'
    monkeypatch.setattr(Container,'_check_credentials',available)
    with pytest.raises(Exception,match='^invalid_parameters$'):
        methods['price_target'](symbol='MSFT',limit=True)
    assert checks == ['other','fmp'] and calls == []
    assert current_frame() is None


def test_baseline_staged_selection_does_not_apply_strict_query_checks(native,monkeypatch):
    import openbb_core.app.parameter_admission as admission
    from openbb_core.app.static.utils.admission_context import current_frame
    methods,runner,calls=native
    runner.user_settings.defaults.commands['price_target']={'provider':['other','fmp']}
    monkeypatch.setattr(Container,'_check_credentials',lambda self,provider: provider == 'other')
    def forbidden(*args,**kwargs):
        raise AssertionError('strict query admission invoked for baseline')
    monkeypatch.setattr(admission,'supplied_values',forbidden)
    methods['price_target'](symbol='MSFT',limit=True)
    assert calls[-1]['limit'] == 1 and current_frame() is None


def test_noneligible_route_has_no_admission_frame_or_early_resolution(native,monkeypatch):
    from openbb_core.app.static.utils.admission_context import current_frame
    methods,runner,calls=native
    query=ProviderInterface()._registry_map.original_models['PriceTarget']['fmp']['query']
    monkeypatch.setattr(query,'__qopenbb_strict_admission__',False)
    checks=[]
    original=Container._resolve_provider
    def resolve(self,*args):
        assert current_frame() is None
        checks.append(args)
        return original(self,*args)
    monkeypatch.setattr(Container,'_resolve_provider',resolve)
    methods['price_target'](symbol='MSFT',provider='fmp',limit=True)
    assert len(checks)==1 and calls[-1]['limit']==1


def test_nested_baseline_async_await_cannot_adopt_selected_frame(native):
    import asyncio
    from openbb_core.app.static.utils.admission_context import current_frame
    container=native[0]['price_target'].__self__
    @validate
    async def baseline(value: int):
        assert current_frame() is None
        await asyncio.sleep(0)
        assert current_frame() is None
        return value
    @validate(_command_path='/price_target')
    async def selected(self,symbol: str,provider: str,**kwargs):
        frame=current_frame()
        assert await baseline('7') == 7
        assert current_frame() is frame
    asyncio.run(selected(container,'MSFT','fmp'))
    assert current_frame() is None

"""Offline native-source descriptors; provisional until public admission is repaired."""
import ast
import hashlib
import inspect
import json
import tarfile
from collections import OrderedDict
from dataclasses import make_dataclass
from importlib import import_module
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, Query
from openbb_core.app.model.field import OpenBBField
from openbb_core.app.static.package_builder.method_definition import MethodDefinition, Charting
from openbb_core.app.static.package_builder.path_handler import PathHandler
from openbb_core.app.static.utils.decorators import exception_handler, validate
from openbb_core.app.static.utils.filters import filter_inputs
from fmp_a1_contracts import CONTRACTS as A1
from fmp_a2_contracts import CONTRACTS as A2

CONTRACTS = A1 | A2
ROOT = Path(__file__).resolve().parents[2]
API = ROOT / 'vendor/data-api'
PLATFORM = API / 'openbb_platform'
FIXTURES = Path(__file__).parent / 'fixtures/fmp_batch_a'
P = 'openbb_platform/providers/fmp/openbb_fmp/models/'
ROUTES = {
    'analyst_estimates': ('estimates/estimates_router.py','historical','equity/estimates/historical'),
    'price_target': ('estimates/estimates_router.py','price_target','equity/estimates/price_target'),
    'price_target_consensus': ('estimates/estimates_router.py','consensus','equity/estimates/consensus'),
    'revenue_business_line': ('fundamental/fundamental_router.py','revenue_per_segment','equity/fundamental/revenue_per_segment'),
    'revenue_geographic': ('fundamental/fundamental_router.py','revenue_per_geography','equity/fundamental/revenue_per_geography'),
    'historical_market_cap': ('equity_router.py','historical_market_cap','equity/historical_market_cap'),
    'share_statistics': ('ownership/ownership_router.py','share_statistics','equity/ownership/share_statistics'),
    'equity_quote': ('price/price_router.py','quote','equity/price/quote'),
    'income_statement_growth': ('fundamental/fundamental_router.py','income_growth','equity/fundamental/income_growth'),
    'balance_sheet_growth': ('fundamental/fundamental_router.py','balance_growth','equity/fundamental/balance_growth'),
    'cash_flow_growth': ('fundamental/fundamental_router.py','cash_growth','equity/fundamental/cash_growth'),
}


def standard(name):
    module = import_module('openbb_core.provider.standard_models.' + name)
    return next(value for key,value in vars(module).items()
                if key.endswith('QueryParams') and value.__module__ == module.__name__)


def route_node(name):
    filename, function, route = ROUTES[name]
    path = PLATFORM / 'extensions/equity/openbb_equity' / filename
    tree = ast.parse(path.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.AsyncFunctionDef) and n.name == function)
    return path, node, route


def native_controls(name):
    path, node, route = route_node(name)
    arguments = {a.arg:ast.unparse(a.annotation) for a in node.args.args}
    # These concrete commands have no route or parameter dependency controls.
    assert arguments == {'cc':'CommandContext','provider_choices':'ProviderChoices',
                         'standard_params':'StandardParams','extra_params':'ExtraParams'}
    tree = ast.parse(path.read_text())
    router = next(n for n in tree.body if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='router' for t in n.targets))
    assert all(k.arg != 'dependencies' for k in router.value.keywords)
    chart = Charting is not None and route.replace('/','_') in Charting.functions()
    return {'provider':['provider_choices.provider'], 'command_signature':arguments,
            'route_source':path.relative_to(API).as_posix(),
            'route_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'command_dependencies':[], 'chart':bool(chart),'chart_params':False,
            'allowed_public_controls':['provider'] + (['chart'] if chart else []),
            'certification':'source-signature derived; installed eleven-variant join deferred to 4.2'}


def describe():
    adapters = {}
    for name,(query,row) in CONTRACTS.items():
        frozen = json.loads((FIXTURES / 'contracts' / f'{name}.json').read_text())
        fields = {}
        for key,field in query.model_fields.items():
            alias = field.validation_alias
            fields[key] = {'canonical':key, 'validation_alias':alias,
                           'accepted_names':list(dict.fromkeys([key] + ([alias] if isinstance(alias,str) else []))),
                           'required':field.is_required()}
        adapters[name] = {
            'model_key':frozen['model_key'], 'route':ROUTES[name][2],
            'query_class':query.__module__+'.'+query.__name__,
            'strict_opt_in':{'provider':'fmp','query_class':query.__name__,'extra':'forbid',
                             'selection':'native authoritative selected original query class/provider; class namespace owns marker True and extra forbid',
                             'runtime_pair_membership_required':False,
                             'class_owned_marker':'__qopenbb_strict_admission__',
                             'marker_required_value':True, 'implementation_status':'pending_task_2.1; accepted query fixtures unchanged'},
            'canonical_query_fields':fields, 'standard_fields':list(standard(name).model_fields),
            'native_controls':native_controls(name),
            'value_aliases':{'period':{'quarterly':'quarter'}} if 'period' in fields else {},
            'row_aliases_are_not_query_aliases':True,
            'row_contract':f'{name}.json',
            'row_contract_sha256':hashlib.sha256((FIXTURES/'contracts'/f'{name}.json').read_bytes()).hexdigest(),
            'accepted_row_compatibility':frozen.get('compatibility',{}),
            'date_contracts':frozen['date_contracts'],
            'response_policy':frozen['query_annotation']['response_policy'],
        }
    return {'schema_version':1,'status':'proposal_ready_pending_independent_review',
            'surfaces':['HTTP','generated public Python SDK','direct Fetcher raw dictionaries'],
            'supplied_pass':{'before':'validate_call, native filter_inputs and configured defaults',
                             'membership':'only supplied canonical/accepted aliases; unsupported even at native default rejected',
                             'null_bounds':'explicit limit/page null rejected; omission allowed',
                             'boolean_bounds':'reject raw bool before int coercion',
                             'mutates_inputs':False,'inserts_defaults':False},
            'effective_pass':{'after':'configured defaults','before':'sync_run',
                              'validation':'same strict selected query class; resolved dates ISO calendar strings'},
            'direct_fetcher':'transform_query validates untouched dictionary through same strict selected query class',
            'known_defect':'Container._run hooks alone lose standard-field presence and bool type in generated SDK',
            'sdk_mechanism':sdk_mechanism(),
            'repair_verification':{'status':'pending_tasks_2.1_and_2.3','matrix':repair_matrix(),
                                   'final_real_subclass_gate':'tasks_4.1_and_4.2'},
            'adapters':adapters}


def source_inventory(name):
    manifest = json.loads((FIXTURES/'source_manifest.json').read_text())
    member = next(m for m in manifest['members'] if m['member'].endswith('/'+name+'.py'))
    with tarfile.open(ROOT / manifest['archive']['path']) as archive:
        raw = archive.extractfile(member['member']).read()
    source = raw.decode()
    tree = ast.parse(source)
    logical = lambda n: sum(isinstance(x,(ast.stmt,ast.Lambda)) and not (
        isinstance(x,ast.Expr) and isinstance(x.value,ast.Constant) and isinstance(x.value.value,str)) for x in ast.walk(n))
    classes = {n.name:{'physical':n.end_lineno-n.lineno+1,'logical':logical(n)}
               for n in tree.body if isinstance(n,ast.ClassDef)}
    functions = {n.name:logical(n) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    return {'physical':len(source.splitlines()),'logical':logical(tree),
            'classes':classes,'functions':functions,
            'source_sha256':hashlib.sha256(raw).hexdigest()}


def handoffs():
    adapters = {}
    for index,name in enumerate(CONTRACTS,1):
        growth = name in ('income_statement_growth','balance_sheet_growth','cash_flow_growth')
        data_module = P+name+'_data.py' if growth else None
        adapters[name] = {
            'task':f'3.{index}', 'lane':'A1' if name in A1 else 'A2',
            'dispatch':'blocked_until_1.4_and_2.3_accepted',
            'write_paths':['api:'+P+name+'.py', 'root:tests/providers/test_fmp_'+name+'.py',
                           'root:tests/providers/fixtures/fmp_batch_a/'+name+'/**'] + (['api:'+data_module] if growth else []),
            'data_declaration_owner':data_module,
            'source_inventory':source_inventory(name),
            'frozen_contract':'tests/providers/fixtures/fmp_batch_a/contracts/'+name+'.json',
            'compatibility':'Copy exact accepted effective_aliases, accepted_validation_aliases, date_contracts, compatibility and schema overrides; original retained aliases are documentary only.',
            'completion_caps':{'physical':400,'logical':300,'function':50},
            'join':'Actual production strict query and row schemas match frozen validation/serialization; endpoint behavior, direct Fetcher and native public SDK/HTTP re-tested after registration.',
        }
    return {'schema_version':1,'status':'proposal_ready_pending_independent_review',
            'amendment':'.kiro/specs/market-data-integrations/fmp-expansion-a-admission-amendment.md',
            'admission_implementation_paths':sdk_mechanism()['api_write_paths'],
            'repair_acceptance':'pending tasks 2.1 and 2.3; no adapter dispatch before acceptance',
            'read_only':['standards','routers','registry','transport','core','locks','shared fixtures','inventories','other adapters'],
            'controller_inventory_patterns_needed':[P+n+'_data.py' for n in ('income_statement_growth','balance_sheet_growth','cash_flow_growth')],
            'growth_split':'Endpoint-local Data declarations/aliases/schema annotation overrides move to owned *_data.py. Query/admission/acquisition/transform remain adapter-owned; no shared declaration module.',
            'adapters':adapters}


class Capture:
    def _run(self,*args,**kwargs):
        return kwargs


def generated_probe(name, monkeypatch):
    """Characterize the unregistered baseline; strict acceptance uses real Container."""
    # No installed variants exist yet. Suppress only missing route metadata lookups.
    monkeypatch.setattr(MethodDefinition,'is_deprecated_function',staticmethod(lambda path:False))
    monkeypatch.setattr(PathHandler,'get_router_dependencies',staticmethod(lambda path:[]))
    query = standard(name)
    standard_dc = make_dataclass('Standard', [(key,field.annotation,Query(default=field.default,description=field.description))
        for key,field in query.model_fields.items()])
    standard_annotation = Annotated[standard_dc,Depends()]
    def route(standard_params, **kwargs):
        pass
    route.__annotations__={'standard_params':standard_annotation,'return':Any}
    if name == 'analyst_estimates':
        extras = make_dataclass('Extra', [(key,field.annotation,field.default)
            for key,field in CONTRACTS[name][0].model_fields.items() if key not in query.model_fields])
        def route(standard_params, extra_params):
            pass
        route.__annotations__={'standard_params':standard_annotation,'extra_params':Annotated[extras,Depends()],'return':Any}
    path='/'+ROUTES[name][2]
    formatted=MethodDefinition.format_params(path,dict(inspect.signature(route).parameters),route)
    formatted=OrderedDict((k,v) for k,v in formatted.items() if v.kind != inspect.Parameter.VAR_KEYWORD)
    formatted['kwargs']=inspect.Parameter('kwargs',inspect.Parameter.VAR_KEYWORD,annotation=Any)
    code='class Public(Capture):\n'+MethodDefinition.build_command_method_signature('execute',formatted,Any,path)
    code+=MethodDefinition.build_command_method_body(path,route,formatted)
    namespace=dict(globals())
    exec(code,namespace)
    return namespace['Public']().execute


def sdk_mechanism():
    prefix='openbb_platform/core/openbb_core/app/'
    return {
        'route_metadata':'explicit command path on validate before validate_call',
        'authoritative_selection':['CommandMap.commands_model','get_command actual signature/dependencies',
                                   "RegistryMap.original_models[model][provider]['query']"],
        'activation':{'provider':'fmp','query':'authoritative selected original query class',
                      'class_owned_marker':'__qopenbb_strict_admission__','marker_value':True,
                      'class_owned_extra':'forbid','parallel_pair_registry':False,'runtime_fixture_dependency':False},
        'scope_join':{'authority':'native registry/discovery expected-set assertions; not runtime activation',
                      'model_keys':sorted(json.loads((FIXTURES/'contracts'/f'{name}.json').read_text())['model_key'] for name in CONTRACTS),
                      'gates':['2.3','4.2'], 'status':'pending prerequisite/final join tests'},
        'raw_binding':'inspect.signature bind without apply_defaults',
        'caller_state':'copy supplied keys/accepted aliases/raw values; no mutation; no defaults; no absent-field requirements',
        'native_validation':'retained validate_call; private route option consumed; preserve wraps/signature/arbitrary_types configuration; never rescue through raw body',
        'provider_resolution':{
            'resolver':'existing Container._get_provider explicit/default/credential resolution',
            'ordered_choices':'actual Literal descriptor order; never sort',
            'reuse':'matching generated resolver call reuses one preflight selection',
            'matching':['container','authoritative route','original choice','ordered priority descriptor','invocation','thread/task owner'],
            'mismatch':'selected frame fails closed; no matching selected frame preserves ordinary resolution',
            'uncertain_binding':'do not guess selected provider'},
        'lifecycle':{
            'frame':['container identity','authoritative route','model','query class','provider','original provider choice',
                     'ordered provider priorities','supplied keys/raw values','invocation identity','thread/task owner'],
            'token':'ContextVar token reset in finally on every outcome; nested calls restore outer token',
            'consume':'exact matching frame once before async sync_run; clear raw state',
            'child_tasks':'inherited consumed frame cannot be adopted or reused',
            'async_callable':'selected lifecycle surrounds await when actual async wrapper is supported'},
        'effective':'validate selected strict financial query after configured defaults before sync_run; preserve omission/schema defaults; controls separate',
        'safe_errors':{'selected_only':True,'message':'constant safe invalid_parameters OpenBBError or existing equivalent',
                       'scope':['raw input','binding when selection established','native validation','filtering','effective admission'],
                       'excluded':['provider entitlement','transport'],
                       'no_echo':['raw values','user-controlled keys/locations','validator messages/context','URLs','raw cause text'],
                       'debug_mode':'cannot restore raw selected input exceptions','baseline':'native behavior unchanged'},
        'api_write_paths':[prefix+p for p in ['parameter_admission.py','static/utils/admission_context.py',
            'static/utils/decorators.py','static/container.py','static/package_builder/method_definition.py']],
        'approval':'independent architecture/task-local review pending; no runtime repair claimed',
    }


def repair_matrix():
    return {
        'generated_sdk':['all eleven dedicated installed variants','keyword/positional','omission/null/bools',
                         'unsupported standard/extra at native default','alias collisions','required symbol','zero I/O'],
        'selection':['explicit FMP','native omitted provider/default/credentials','ordered priorities','one reused selection',
                     'other provider','non-opted strict/unregistered class','unchanged baseline'],
        'defaults':['valid','null/bool/range/date invalid','unknown configured key','raw invalid before overwrite'],
        'controls':['actual concrete descriptors','chart only exposed','unsupported chart_params','signature/positional duplicates',
                    'native arbitrary_types configuration','no validation bypass'],
        'safe_errors':['pre-body ValidationError','unknown key/value sentinel','malformed list/filter choice',
                       'selected binding/required failures','DEBUG_MODE on/off','no raw cause','no network'],
        'lifecycle':['nested routes/containers','two threads','async tasks','every failure stage','subsequent baseline',
                     'inherited child context','actual async await if supported','finally reset','consume once'],
        'http_fetcher':['repeated symbol/page','unknown/default-valued key','null/bool','invalid provider',
                        'untouched raw dictionary','safe HTTP422','zero extraction'],
        'complexity':['explicit current fork scope','independently reviewed exact final emitter metrics/exception',
                      'all other files400/logical300/functions50'],
    }

"""A2 frozen financial contracts; no provider registration or network access."""
import json
from datetime import date, datetime, timezone
from pathlib import Path
import pytest
from pydantic import ValidationError
from openbb_core.provider.standard_models.financial_annotations import bind_data_annotation, bind_query_annotation, render_field_templates
from fmp_a2_contracts import CONTRACTS, RETAINED_ALIASES, resolve_cap_dates

FIXTURES = Path(__file__).parent / 'fixtures/fmp_batch_a/contracts'
GROWTH = ['income_statement_growth','balance_sheet_growth','cash_flow_growth']

def payload(name):
    return {**{field:None for field,info in CONTRACTS[name][1].model_fields.items() if info.is_required() and field.startswith('growth_')},'symbol':'MSFT', **({'date':'2025-06-30','marketCap':0} if name == 'historical_market_cap' else {'date':'2025-06-30'} if name in GROWTH else {})}

@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_frozen_schema_annotations_aliases(name):
    query,row = CONTRACTS[name]
    frozen=json.loads((FIXTURES/f'{name}.json').read_text())
    for mode in ['validation','serialization']:
        assert query.model_json_schema(mode=mode)==frozen['query'][mode]
        assert row.model_json_schema(mode=mode)==frozen['data'][mode]
    assert bind_data_annotation(row).model_dump(mode='json')==frozen['data_annotation']
    assert bind_query_annotation(query).model_dump(mode='json')==frozen['query_annotation']
    assert set(render_field_templates(row))==set(row.model_fields)
    assert frozen['retained_aliases']==RETAINED_ALIASES[name]
    assert frozen['effective_aliases']==row.__alias_dict__
    for canonical,field in row.model_fields.items():
        assert frozen['accepted_validation_aliases'][canonical]=={'canonical':canonical,'generated_schema_alias':field.validation_alias,'source_aliases':[source for target,source in row.__alias_dict__.items() if target==canonical],'serialization':field.serialization_alias}

@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
@pytest.mark.parametrize('invalid', ['',None,True,'A,B','A&apikey=x','A\x01','A'*51])
def test_symbol_invalid(name,invalid):
    with pytest.raises((ValidationError,ValueError)):
        CONTRACTS[name][0](symbol=invalid)

@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_strict_query(name):
    query=CONTRACTS[name][0]
    assert query(symbol=' brk.b ').symbol=='BRK.B'
    with pytest.raises(ValidationError): query(symbol='MSFT',unsupported=False)
    with pytest.raises(ValidationError): query()

@pytest.mark.parametrize('name', GROWTH)
def test_growth_query(name):
    query=CONTRACTS[name][0]
    assert query(symbol='MSFT').limit==20
    assert query(symbol='MSFT').period=='annual'
    assert query(symbol='MSFT',period='quarterly').period=='quarter'
    for invalid in [None,True,False,0,101,1.5,'20']:
        with pytest.raises(ValidationError): query(symbol='MSFT',limit=invalid)
    for invalid in ['ttm','FY','YTD',None]:
        with pytest.raises(ValidationError): query(symbol='MSFT',period=invalid)


def test_cap_dates_acquisition_resolution():
    query=CONTRACTS['historical_market_cap'][0]
    value=query(symbol='MSFT')
    assert value.start_date is None and value.end_date is None
    assert resolve_cap_dates(value,date(2024,3,1))==(date(2023,3,2),date(2024,3,1))
    assert resolve_cap_dates(query(symbol='MSFT',end_date='2025-06-30'),date(2026,1,1))==(date(2024,6,30),date(2025,6,30))
    assert resolve_cap_dates(query(symbol='MSFT',start_date='2024-01-01',end_date='2025-01-01'),date(2026,1,1))==(date(2024,1,1),date(2025,1,1))
    for start,end in [('2025-06-30','2025-06-29'),('2024-01-01','2025-01-02')]:
        with pytest.raises(ValidationError): query(symbol='MSFT',start_date=start,end_date=end)
    for value in [True,1735689600,'2025-01-01T00:00:00']:
        with pytest.raises(ValidationError): query(symbol='MSFT',start_date=value)
    with pytest.raises(ValueError): resolve_cap_dates(query(symbol='MSFT',start_date='2020-01-01'),date(2026,1,1))

@pytest.mark.parametrize('name', ['historical_market_cap',*GROWTH])
def test_required_facts(name):
    row=CONTRACTS[name][1]
    required=['date','marketCap'] if name=='historical_market_cap' else ['date']
    for field in required:
        for action in ['missing',None,'malformed']:
            data=payload(name)
            if action=='missing': data.pop(field)
            else: data[field]=action
            with pytest.raises(ValidationError): row.model_validate(data)


def test_float_source_percentage_zero_null_and_date():
    row=CONTRACTS['share_statistics'][1]
    for source,expected in [(99.83,.9983),(0,0),(None,None)]:
        result=row.model_validate({'symbol':'MSFT','freeFloat':source,'floatShares':0,'outstandingShares':None,'source':'https://example.org/filing'})
        assert result.free_float==expected
        assert result.float_shares==0 and result.outstanding_shares is None
        assert result.date is None and result.url=='https://example.org/filing'
        assert not result.model_extra
    result=row.model_validate({'symbol':'MSFT','date':'2026-07-30 15:48:00'})
    assert result.date==datetime(2026,7,30,15,48)
    assert result.date.tzinfo is None


def test_quote_epoch_and_price_distinctions():
    row=CONTRACTS['equity_quote'][1]
    value=row.model_validate({'symbol':'MSFT','timestamp':0,'price':0,'dayHigh':12,'dayLow':1,'previousClose':9,'close':8,'bid':7,'ask':10,'changePercentage':0,'marketCap':0})
    assert value.last_timestamp==datetime(1970,1,1,tzinfo=timezone.utc)
    assert (value.last_price,value.high,value.low,value.prev_close,value.close,value.bid,value.ask)==(0,12,1,9,8,7,10)
    assert value.change_percent==0 and value.market_cap==0
    assert row.model_validate({'symbol':'MSFT','timestamp':None}).last_timestamp is None
    value=row.model_validate({'symbol':'MSFT','timestamp':'1785430812','changePercentage':-1.8732})
    assert value.last_timestamp==datetime.fromtimestamp(1785430812,timezone.utc)
    assert value.change_percent==pytest.approx(-.018732)

@pytest.mark.parametrize('name',GROWTH)
def test_growth_fractions_and_fiscal_aliases(name):
    row=CONTRACTS[name][1]
    growth=[field for field in row.model_fields if field.startswith('growth_')]
    for number in [-.25,0,.25,None]:
        value=row.model_validate(payload(name)|{field:number for field in growth}|{'calendarYear':2025,'period':'Q2'})
        assert all(getattr(value,field)==number for field in growth)
        assert str(value.fiscal_year)=='2025' and value.fiscal_period=='Q2'
        assert value.period_ending==date(2025,6,30)
        assert not value.model_extra

@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_every_source_alias_populates_canonical_without_extra(name):
    row=CONTRACTS[name][1]
    for canonical,source in row.__alias_dict__.items():
        probe='https://example.org/filing' if canonical=='url' else '2025-06-30' if canonical=='period_ending' else 2025 if canonical=='fiscal_year' else 'Q2' if canonical=='fiscal_period' else 1785430812 if canonical=='last_timestamp' else 'USD' if canonical in {'currency','reported_currency'} else 7
        value=row.model_validate(payload(name)|{source:probe})
        expected=date(2025,6,30) if canonical=='period_ending' else str(probe) if canonical=='fiscal_year' and isinstance(value.fiscal_year,str) else datetime.fromtimestamp(probe,timezone.utc) if canonical=='last_timestamp' else .07 if canonical=='change_percent' else probe
        assert value.model_dump(by_alias=False)[canonical]==expected,(name,canonical)
        assert not value.model_extra


@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_source_hash_union_notices_and_requiredness(name):
    import ast
    import hashlib
    import tarfile
    from importlib import import_module
    manifest=json.loads((FIXTURES.parent/'source_manifest.json').read_text())
    archive_path=Path(manifest['archive']['path'])
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest()==manifest['archive']['sha256']
    source_info=next(item for item in manifest['members'] if item['member'].endswith(f'/{name}.py'))
    with tarfile.open(archive_path) as archive:
        source=archive.extractfile(source_info['member']).read()
    assert hashlib.sha256(source).hexdigest()==source_info['sha256']
    declaration=next(node for node in ast.parse(source).body if isinstance(node,ast.ClassDef) and node.name.endswith('Data'))
    standard=getattr(import_module(f'openbb_core.provider.standard_models.{name}'),declaration.bases[0].id)
    additions={node.target.id for node in declaration.body if isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name)}
    aliases=next((ast.literal_eval(node.value) for node in declaration.body if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='__alias_dict__' for target in node.targets)),{})
    row=CONTRACTS[name][1]
    assert set(row.model_fields)==set(standard.model_fields)|additions
    assert RETAINED_ALIASES[name]==aliases
    frozen=json.loads((FIXTURES/f'{name}.json').read_text())
    assert frozen['source']['member_sha256']==source_info['sha256']
    api=Path.cwd().parent/'data-api'
    assert hashlib.sha256((api/manifest['notices']['retained_path']).read_bytes()).hexdigest()==manifest['notices']['sha256']
    for field,info in row.model_fields.items():
        assert frozen['field_presence'][field]['required']==info.is_required()
        data=payload(name)
        data.pop('date',None) if field=='period_ending' else None
        data.pop('marketCap',None) if field=='market_cap' else None
        try:
            row.model_validate(data|{field:None})
            nullable=True
        except ValidationError:
            nullable=False
        assert frozen['field_presence'][field]['nullable']==nullable

@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_independent_financial_families(name):
    fields=render_field_templates(CONTRACTS[name][1])
    for field,value in fields.items():
        assert value.currency is None and value.currency_field is None
        assert value.publication_date_field is None and value.valuation_date_field is None
        if name in GROWTH:
            assert value.observation_date_field=='period_ending'
            assert 'denominator periods and restatement unknown' in value.period_basis
            assert ('stock comparison' if name=='balance_sheet_growth' else 'flow growth') in value.period_basis
            if field.startswith('growth_'):
                assert (value.unit,value.scale,value.value_origin)==('ratio',1,'provider_calculation')
        if name=='historical_market_cap' and field=='market_cap':
            assert (value.unit,value.scale,value.value_origin)==('currency',1,'provider_calculation')
            assert value.observation_date_field=='date' and value.financial_basis['share_count'] is None
        if name=='share_statistics':
            assert value.observation_date_field=='date'
            if field in {'outstanding_shares','float_shares'}:
                assert (value.unit,value.scale,value.value_origin)==('shares',1,'provider_observation')
            if field=='free_float':
                assert (value.unit,value.scale,value.value_origin)==('ratio',1,'provider_calculation')
                assert value.source_unit=='percent' and value.requested_transform=='divide_by_100'
        if name=='equity_quote':
            if field in {'last_price','bid','ask','open','high','low','close','prev_close','change','year_high','year_low','ma50','ma200'}:
                assert value.unit=='currency/share' and value.scale==1
                assert value.value_origin==('provider_calculation' if field in {'change','ma50','ma200'} else 'provider_observation')
            if field in {'volume','exchange_volume','last_size'}:
                assert value.unit=='shares' and value.scale==1
            if field=='market_cap':
                assert value.value_origin=='provider_calculation' and value.observation_date_field is None
                assert value.unit=='currency' and value.scale==1


def test_official_float_percentage_evidence():
    frozen=json.loads((FIXTURES/'share_statistics.json').read_text())
    example=frozen['source_evidence']['official_example']
    assert example['freeFloat']==99.83000000136171
    assert example['freeFloat']==pytest.approx(example['floatShares']/example['outstandingShares']*100)
    value=CONTRACTS['share_statistics'][1].model_validate(example)
    assert value.free_float==pytest.approx(.9983000000136171)


def test_balance_currency_source_alias_correction():
    row=CONTRACTS['balance_sheet_growth'][1]
    assert RETAINED_ALIASES['balance_sheet_growth']['currency']=='reportedCurrency'
    assert 'currency' not in row.model_fields
    value=row.model_validate(payload('balance_sheet_growth')|{'reportedCurrency':'USD'})
    assert value.model_dump()['reported_currency']=='USD' and not value.model_extra


def test_cashflow_evidenced_source_spellings_and_conflicts():
    row=CONTRACTS['cash_flow_growth'][1]
    frozen=json.loads((FIXTURES/'cash_flow_growth.json').read_text())
    for canonical,pair in frozen['additional_source_aliases'].items():
        retained,official=pair
        for spelling in pair:
            value=row.model_validate(payload('cash_flow_growth')|{spelling:-.25})
            assert value.model_dump()[canonical]==-.25 and not value.model_extra
        assert row.model_validate(payload('cash_flow_growth')|{retained:0,official:0}).model_dump()[canonical]==0
        with pytest.raises(ValidationError): row.model_validate(payload('cash_flow_growth')|{retained:.2,official:.3})


def test_balance_required_nullable_differs_from_optional():
    row=CONTRACTS['balance_sheet_growth'][1]
    required=[field for field,info in row.model_fields.items() if info.is_required() and field.startswith('growth_')]
    assert len(required)==10
    for field in required:
        value=row.model_validate(payload('balance_sheet_growth'))
        assert value.model_dump()[field] is None
        data=payload('balance_sheet_growth')
        data.pop(field)
        with pytest.raises(ValidationError): row.model_validate(data)
    assert row.model_validate(payload('balance_sheet_growth')).growth_cash_and_cash_equivalents is None


@pytest.mark.parametrize('name', ['share_statistics','equity_quote'])
@pytest.mark.parametrize('key', ['period','limit','page','start_date','end_date'])
def test_singleton_queries_admit_no_extra_financial_options(name,key):
    with pytest.raises(ValidationError): CONTRACTS[name][0](symbol='MSFT',**{key:None})


def test_cap_schema_describes_window_without_unsupported_metadata():
    query=CONTRACTS['historical_market_cap'][0]
    for mode in ['validation','serialization']:
        schema=query.model_json_schema(mode=mode)
        assert schema['required']==['symbol']
        assert schema['additionalProperties'] is False
        assert 'max_days' not in json.dumps(schema)
        for field in ['start_date','end_date']:
            assert '366 days' in schema['properties'][field]['description']
    assert query.financial_query_annotation.response_policy.max_rows==5000


@pytest.mark.parametrize('name', ['historical_market_cap','share_statistics','equity_quote',*GROWTH])
def test_empty_rows_and_optional_null_zero_distinct(name):
    from pydantic import TypeAdapter
    row=CONTRACTS[name][1]
    assert TypeAdapter(list[row]).validate_python([])==[]
    if name=='historical_market_cap':
        assert row.model_validate(payload(name)).market_cap==0
        return
    field='free_float' if name=='share_statistics' else 'last_price' if name=='equity_quote' else next(field for field in row.model_fields if field.startswith('growth_') and not row.model_fields[field].is_required())
    missing=row.model_validate(payload(name))
    explicit_null=row.model_validate(payload(name)|{field:None})
    zero=row.model_validate(payload(name)|{field:0})
    assert getattr(missing,field) is None and getattr(explicit_null,field) is None
    assert field not in missing.model_fields_set and field in explicit_null.model_fields_set
    assert getattr(zero,field)==0


@pytest.mark.parametrize('name', GROWTH)
@pytest.mark.parametrize('mode', ['validation','serialization'])
def test_growth_ratio_schema_and_actual_native_formatter(name,mode):
    import importlib.util
    source=Path.cwd().parent/'data-api/openbb_platform/extensions/platform_api/openbb_platform_api/utils/openapi.py'
    spec=importlib.util.spec_from_file_location('a2_native_widget_openapi',source)
    native=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    schema=CONTRACTS[name][1].model_json_schema(mode=mode)
    document={'paths':{'/growth':{'get':{'operationId':'growth','responses':{'200':{'content':{'application/json':{'schema':schema}}}}}}}}
    columns=native.data_schema_to_columns_defs(document,'growth','fmp')
    by_name={column['field']:column for column in columns}
    for canonical,info in CONTRACTS[name][1].model_fields.items():
        if not canonical.startswith('growth_'):
            continue
        alias=info.validation_alias if mode=='validation' else info.serialization_alias
        prop=schema['properties'][alias]
        assert prop.get('x-unit_measurement')=='ratio',(name,canonical)
        assert 'x-frontend_multiply' not in prop,(name,canonical)
        projected=by_name[canonical]
        assert projected['cellDataType']=='number'
        assert projected['formatterFn'] not in {'percent','normalizedPercent'},(name,canonical,projected)

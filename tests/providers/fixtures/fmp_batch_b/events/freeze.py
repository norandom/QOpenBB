"""Offline contract characterization, not an adapter or installed-route test."""
import ast
import hashlib
import json
import math
import sys
import types
from typing import get_args
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = ROOT.parent
CORE = BASE / 'data-api/openbb_platform/core/openbb_core'
RECOVERED = BASE / 'evidence/foundation/recovered'
NAMES = ['historical_dividends', 'historical_splits', 'calendar_earnings',
         'calendar_dividend', 'calendar_splits']
CLASSES = ['HistoricalDividends', 'HistoricalSplits', 'CalendarEarnings',
           'CalendarDividend', 'CalendarSplits']


def load_models():
    # Avoid provider package initialization and transport dependencies. Execute the
    # exact model declarations and their validators, excluding only Fetcher code.
    for suffix in ['', '.provider', '.provider.abstract', '.provider.utils',
                   '.provider.standard_models']:
        key = 'openbb_core' + suffix
        module = types.ModuleType(key)
        module.__path__ = [str(CORE.joinpath(*suffix.strip('.').split('.')))] if suffix else [str(CORE)]
        sys.modules[key] = module
    result = {}
    for name, stem in zip(NAMES, CLASSES):
        tree = ast.parse((RECOVERED / f'{name}.py').read_text())
        tree.body = [node for node in tree.body if not (
            isinstance(node, ast.ImportFrom) and
            (node.module.endswith('fetcher') or node.module.startswith('openbb_fmp'))
        ) and not (isinstance(node, ast.ClassDef) and node.name.endswith('Fetcher'))]
        namespace = {'__name__': f'fixture_{name}'}
        exec(compile(tree, str(RECOVERED / f'{name}.py'), 'exec'), namespace)
        result[name] = (namespace[f'FMP{stem}QueryParams'], namespace[f'FMP{stem}Data'])
    return result


class Query(BaseModel):
    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='before')
    @classmethod
    def reject_explicit_null(cls, value):
        if any(v is None for v in value.values()):
            raise ValueError('Explicit null is not omission')
        return value

    @model_validator(mode='after')
    def boundaries(self):
        symbol = getattr(self, 'symbol', None)
        if symbol is not None:
            if not symbol.strip() or ',' in symbol or any(c.isspace() for c in symbol):
                raise ValueError('One listing identity required')
            self.symbol = symbol.upper()
        start, end = getattr(self, 'start_date', None), getattr(self, 'end_date', None)
        if start and end and (end < start or (not symbol and (end-start).days > 6)):
            raise ValueError('Invalid inclusive date window')
        return self


def desired_query(name):
    fields = {}
    if name.startswith('historical'):
        fields['symbol'] = (str, Field(..., min_length=1, max_length=50))
    if name != 'historical_splits':
        required = not name.startswith('historical')
        for key in ['start_date', 'end_date']:
            fields[key] = (date if required else date | None, ... if required else None)
    if name == 'historical_dividends':
        fields['limit'] = (int, Field(20, ge=1, le=100, strict=True))
    return create_model('Frozen' + name.title().replace('_', '') + 'Query', __base__=Query, **fields)


def row_fields(name, old):
    result = {}
    for key, field in old.model_fields.items():
        result[key] = {'source': old.__alias_dict__.get(key, key),
                       'required': field.is_required(), 'nullable': type(None) in get_args(field.annotation),
                       'definition': field.description, 'unit': None, 'scale': None,
                       'currency': None, 'period_basis': None,
                       'value_origin': 'provider_observation', 'availability': 'unknown'}
        if 'date' in key or key == 'last_updated':
            result[key]['unit'] = 'civil_date'
        if key in ['amount', 'adjusted_amount', 'eps_actual', 'eps_consensus', 'eps_previous']:
            result[key]['unit'] = 'currency_per_share'
        if key.startswith('revenue'):
            result[key]['unit'] = 'currency'
        if key in ['numerator', 'denominator']:
            result[key]['unit'] = 'shares'
        if key.endswith('consensus'):
            result[key]['value_origin'] = 'estimate'
        if key == 'dividend_yield':
            result[key].update(value_origin='provider_calculation', source_unit='percentage_points',
                               unit='ratio', scale=1, period_basis=None,
                               decision='Divide non-null raw value by 100; preserve zero. Example-level independent unit corroboration; annualization and price basis remain unknown.')
    if name == 'historical_splits':
        result['symbol'] = dict(source='symbol or exact requested listing when absent', required=True,
                                nullable=False, unit=None, scale=None, currency=None, period_basis=None,
                                value_origin='provider_observation', availability='unknown',
                                definition='Company listing identity; reject a foreign supplied symbol.')
    if name.startswith('historical'):
        result['symbol'].update(required=True, nullable=False,
            source='symbol or exact requested listing when absent')
    if 'dividend' in name:
        result['adjusted_amount'].update(required=False, nullable=True,
            decision='Preserve absent/null; retained historical required field is deliberately relaxed.')
    return result


def desired_row(name, old):
    from openbb_core.provider.abstract.data import Data
    fields = {key:(field.annotation, Field(... if field.is_required() else field.default,
                validation_alias=old.__alias_dict__.get(key, key), serialization_alias=key,
                description=field.description, json_schema_extra=field.json_schema_extra))
              for key, field in old.model_fields.items()}
    if 'dividend' in name:
        fields['adjusted_amount'] = (float | None, Field(None,
            validation_alias='adjDividend', serialization_alias='adjusted_amount',
            description='Provider adjusted cash dividend per share; adjustment methodology unknown.'))
    if name.startswith('historical'):
        fields['symbol'] = (str, Field(..., description='Exact company listing identity.'))
    if 'splits' in name:
        for key in ['numerator','denominator']:
            optional = name == 'historical_splits'
            fields[key] = (float | None if optional else float,
                           Field(None if optional else ..., gt=0, allow_inf_nan=False,
                                 description='New shares' if key=='numerator' else 'Old shares'))
    model = create_model('Frozen'+name.title().replace('_','')+'Data', __base__=Data, **fields)
    model.model_config['allow_inf_nan'] = False
    model.model_rebuild(force=True)
    return model


def normalize_fixture_row(name, old, raw, symbol=None):
    row = dict(raw)
    if 'dividend' in name:
        for key in ['declarationDate','recordDate','paymentDate']:
            if row.get(key) == '': row[key] = None
        if row.get('yield') is not None: row['yield'] /= 100
    if symbol:
        if row.get('symbol', symbol).upper() != symbol.upper():
            raise ValueError('Foreign listing')
        row['symbol'] = symbol.upper()
    return desired_row(name, old)(**row).model_dump(mode='json')


def build():
    models = load_models()
    outputs = {}
    for name, (old_query, old_row) in models.items():
        query = desired_query(name)
        calendar = name.startswith('calendar')
        endpoint = {'historical_dividends':'dividends', 'historical_splits':'splits',
                    'calendar_earnings':'earnings-calendar','calendar_dividend':'dividends-calendar',
                    'calendar_splits':'splits-calendar'}[name]
        outputs[name] = {
            'status': 'FROZEN_FOR_REVIEW',
            'endpoint': endpoint, 'source_identity': 'fmp/stable/' + endpoint,
            'query': {mode: query.model_json_schema(mode=mode) for mode in ['validation','serialization']},
            'data': {mode: desired_row(name, old_row).model_json_schema(mode=mode) for mode in ['validation','serialization']},
            'retained_baseline': {
                'query': {mode: old_query.model_json_schema(mode=mode) for mode in ['validation','serialization']},
                'data': {mode: old_row.model_json_schema(mode=mode) for mode in ['validation','serialization']},
                'aliases': old_row.__alias_dict__,
                'sha256': hashlib.sha256((RECOVERED/f'{name}.py').read_bytes()).hexdigest()},
            'fields': row_fields(name, old_row),
            'row_admission': {'dates':'Strict YYYY-MM-DD civil dates; blank optional dates become null; missing/blank event date rejects.',
                'symbols':'Require nonblank market-wide symbol; history binds exact normalized requested symbol, fills absent identity, rejects supplied foreign identity.',
                'duplicates':'Retain separate source rows even on the same event date; no sorting or deduplication.',
                'numbers':'Finite supplied numbers; missing stays null where nullable, zero stays zero.',
                'split_components':'Historical components nullable but positive finite when supplied; calendar components both required; never infer missing values.',
                'yield':'raw percentage points / 100 for non-null values including zero; sample-level unit evidence in unit_evidence.json'},
            'wire': {'method':'GET', 'origin':'https://financialmodelingprep.com', 'path':'/stable/'+endpoint,
                     'parameters': ['from','to'] if calendar else ['symbol','limit'] if 'dividends' in name else ['symbol'],
                     'public_to_wire': {'start_date':'from','end_date':'to'} if calendar else {},
                     'local_only': ['start_date','end_date'] if name=='historical_dividends' else []},
            'procedural_bounds': {'max_calls':1,'pagination':False, 'retries':False,
                'max_inclusive_days':7 if calendar else None,'max_symbols':0 if calendar else 1,
                'required_market_wide':calendar,'reject_unknown_or_repeated_scalar':True,
                'reject_bool_int_and_explicit_null':True,'validate_all_rows_before_clip':True,
                'preserve_source_order':True,'deduplicate':False,
                'row_cap':250 if calendar else 100,
                'clip_order':'validate entire acquisition; preserve source order; clip; local ex-date filter' if name=='historical_dividends' else 'validate entire acquisition; preserve source order; clip',
                'cap_basis':'requested upstream limit, then local defensive limit' if name=='historical_dividends' else 'local product policy'},
            'metadata': {'effective_query':'canonical admitted parameters including defaults; no credentials',
                'retrieved_at':'UTC retrieval timestamp, runtime only', 'field_origin':'per fields entry',
                'bounds':['requested_limit','effective_limit','returned_count','truncated','completeness'],
                'completeness':'unknown; a full page proves no exhaustive history',
                'truncated':'true only when acquired valid rows exceed local cap; otherwise unknown upstream completeness',
                'empty_acquisition':'safe transport empty-data outcome',
                'empty_local_filter':'successful annotated empty results; acquisition was nonempty',
                'malformed':'reject before clipping, including malformed row beyond cap'},
            'transport': {'helper':'get_data with with_provenance=True, typed safe errors; no direct HTTP/chunk loop',
                'allow_empty':False,'error_body':'discard provider text and authenticated URL; preserve typed category only',
                'timeout':'inherit accepted transport configuration, no task-specific override',
                'timeout_and_connection':'typed failures, no retry or stale-success substitution',
                'http_provider':'explicit fmp; no implicit provider fallback',
                'bounds_origin':'one call and product result caps, not documented vendor account maxima'},
            'limitations':['Currency and adjustment methodology unknown.',
                'No confirmed status, fiscal period or timezone inferred.' if name=='calendar_earnings' else 'Civil dates are separate event roles; no timezone inferred.',
                'Product caps do not assert provider maxima or account entitlement.']}
    return outputs, models


def verify(outputs, models):
    checks = 0
    for name, record in outputs.items():
        query = desired_query(name)
        calendar = name.startswith('calendar')
        valid = {'start_date':'2026-01-01','end_date':'2026-01-07'} if calendar else {'symbol':'aapl'}
        assert query(**valid).model_dump(mode='json')['start_date' if calendar else 'symbol'] == ('2026-01-01' if calendar else 'AAPL')
        checks += 1
        invalid = [dict(valid, unknown=True), dict(valid, start_date=None)]
        invalid += [dict(valid,end_date='2026-01-08'),dict(valid,symbol='AAPL')] if calendar else [dict(valid,symbol='AAPL,MSFT')]
        if name=='historical_dividends':
            invalid += [dict(valid,limit=v) for v in [True,0,101,None]]
        for case in invalid:
            try: query(**case)
            except ValueError: checks += 1
            else: raise AssertionError((name,case))
        assert record['procedural_bounds']['validate_all_rows_before_clip']
        assert set(record['retained_baseline']['data']) == {'validation','serialization'}
        checks += 2
    for name in ['historical_dividends','calendar_dividend']:
        row = models[name][1](date='2026-01-01',symbol='AAPL',dividend=0,adjDividend=0,**{'yield':0})
        assert row.dividend_yield is None  # Characterized upstream bug, never accepted semantics.
        assert row.amount == 0
        checks += 2
    row = models['calendar_earnings'][1](date='2026-01-01',symbol='AAPL',epsActual=0,epsEstimated=1,revenueActual=None,revenueEstimated=100)
    assert row.eps_actual == 0 and row.revenue_actual is None and row.eps_consensus == 1
    checks += 1
    for name in ['historical_dividends','calendar_dividend']:
        got = normalize_fixture_row(name, models[name][1], dict(date='2026-01-01',symbol='AAPL',dividend=0,adjDividend=None,**{'yield':0,'declarationDate':''}), 'AAPL')
        assert got['dividend_yield'] == 0 and got['adjusted_amount'] is None and got['declaration_date'] is None
        checks += 1
        for value in [0.27, 0, None]:
            got = normalize_fixture_row(name, models[name][1],
                dict(date='2026-01-01',symbol='AAPL',dividend=1,adjDividend=value), 'AAPL')
            assert got['adjusted_amount'] == value and 'adjDividend' not in got
            checks += 1
    for name in ['historical_splits','calendar_splits']:
        got = normalize_fixture_row(name, models[name][1],dict(date='2026-01-01',symbol='AAPL',numerator=1,denominator=10),'AAPL')
        assert got['numerator'] == 1 and got['denominator'] == 10
        checks += 1
        for value in [0,-1,float('inf'),float('nan')]:
            try: normalize_fixture_row(name,models[name][1],dict(date='2026-01-01',symbol='AAPL',numerator=value,denominator=10),'AAPL')
            except ValueError: checks += 1
            else: raise AssertionError('Invalid ratio accepted')
    units = json.loads((HERE/'unit_evidence.json').read_text())
    historical, calendar = units['historical_dividends'], units['calendar_dividend']
    assert math.isclose(100 * sum(historical['cash_dividends'])/historical['close'], historical['raw_yield'], rel_tol=1e-14)
    assert math.isclose(100 * calendar['adjusted_amount']/calendar['close'], calendar['raw_yield'], rel_tol=1e-14)
    checks += 2
    for sample in json.loads((HERE/'serialization_examples.json').read_text()):
        got = normalize_fixture_row(sample['model'], models[sample['model']][1], sample['raw'], sample.get('requested_symbol'))
        assert got == sample['expected'], sample['model']
        checks += 1
    return checks


if __name__ == '__main__':
    outputs, models = build()
    if '--write' in sys.argv:
        for name, data in outputs.items():
            (HERE/f'{name}.json').write_text(json.dumps(data, indent=2)+'\n',encoding='utf-8')
        examples = []
        for name in NAMES:
            raw = {'date':'2026-01-01','symbol':'AAPL'}
            if 'dividend' in name:
                raw.update(dividend=0,adjDividend=None,declarationDate='',recordDate='2026-01-02',paymentDate='2026-01-10',**{'yield':0})
            elif 'splits' in name:
                raw.update(numerator=1,denominator=10)
            else:
                raw.update(epsActual=0,epsEstimated=1,revenueActual=None,revenueEstimated=100,lastUpdated='2026-01-02')
            symbol = 'AAPL' if name.startswith('historical') else None
            examples.append({'model':name,'raw':raw,'requested_symbol':symbol,
                             'expected':normalize_fixture_row(name,models[name][1],raw,symbol)})
        (HERE/'serialization_examples.json').write_text(json.dumps(examples,indent=2)+'\n',encoding='utf-8')
    else:
        for name, data in outputs.items():
            assert json.loads((HERE/f'{name}.json').read_text()) == data, name
    print(json.dumps({'checks_passed':verify(outputs,models),'authenticated_calls':0,
                      'production_verified':False,'blocked':[]}))

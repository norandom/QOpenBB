"""Shares-float preserves provider counts, nullable dates and percentage basis."""
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import bind_data_annotation, bind_query_annotation
from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.share_statistics import FMPShareStatisticsData as Data, FMPShareStatisticsQueryParams as Query, FMPShareStatisticsFetcher as Fetcher
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, tzinfo=UTC)
ROW = {'symbol': 'ABC', 'freeFloat': 25, 'floatShares': 0, 'outstandingShares': None}


def transformed(rows):
    return Fetcher.transform_data(Fetcher.transform_query({'symbol': ' abc '}), FMPAcquisition(rows, STAMP))


def test_frozen_contract():
    contract = json.loads((Path(__file__).parent / 'fixtures/fmp_batch_a/contracts/share_statistics.json').read_text())
    for model, key in [(Query, 'query'), (Data, 'data')]:
        for mode in ['validation', 'serialization']:
            assert model.model_json_schema(mode=mode) == contract[key][mode]
    assert bind_data_annotation(Data).model_dump(mode='json') == contract['data_annotation']
    assert bind_query_annotation(Query).model_dump(mode='json') == contract['query_annotation']


@pytest.mark.parametrize('params', [{}, {'symbol': None}, {'symbol': True}, {'symbol': 1}, {'symbol': ''}, {'symbol': 'A,B'}, {'symbol': 'A&apikey=x'}, {'symbol': 'A\x7f'}, {'symbol': 'A'*51}, {'symbol': ['A']}, {'symbol': 'ABC', 'limit': 1}])
def test_invalid_zero_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail('invalid query reached transport')
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params))
    assert error.value.code == 'invalid_parameters'


def test_values_metadata():
    result = transformed([ROW])
    row = result.result[0]
    assert row.free_float == .25 and row.float_shares == 0
    assert row.outstanding_shares is None and row.date is None
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(meta['retrieved_at']) == STAMP
    assert meta['effective_query'] == {'symbol': 'ABC'}
    assert meta['provider'] == 'fmp' and meta['point_in_time_safe'] is False
    assert meta['bounds']['completeness'] == 'unknown'
    assert meta['fields']['float_shares']['availability'] == 'available'
    assert meta['fields']['outstanding_shares']['availability'] == 'missing'
    assert meta['fields']['free_float']['requested_transform'] == 'divide_by_100'
    assert meta['fields']['free_float']['unit'] == 'ratio'
    assert urlsplit(meta['source']['documentation']).query == ''
    assert urlsplit(meta['source']['documentation']).fragment == ''


@pytest.mark.parametrize('value,expected', [(0, 0), (None, None), (99.8, .998)])
def test_percent(value, expected):
    assert transformed([{**ROW, 'freeFloat': value}]).result[0].free_float == expected


@pytest.mark.parametrize('date', [None, '2024-01-01', '2024-01-01 15:30:00'])
def test_nullable_source_date(date):
    row = transformed([{**ROW, 'date': date, 'source': 'https://example.com/report'}]).result[0]
    assert (row.date is None) == (date is None)
    assert row.url == 'https://example.com/report'


@pytest.mark.parametrize('rows', [[ROW, ROW], [{**ROW, 'symbol': 'OTHER'}], [{}], [{'symbol': None}], [{**ROW, 'freeFloat': 'bad'}], [{**ROW, 'freeFloat': float('nan')}], [{**ROW, 'floatShares': float('inf')}], [{**ROW, 'outstandingShares': True}], [{**ROW, 'date': True}], [{**ROW, 'date': 0}], [{**ROW, 'date': '0'}]])
def test_invalid_rows(rows):
    with pytest.raises(FinancialError) as error:
        transformed(rows)
    assert error.value.code == 'invalid_response'


class Response:
    status = 200
    def __init__(self, payload):
        self.payload, self.headers = payload, {}
    async def json(self):
        return self.payload


@pytest.mark.parametrize('payload', [[], [ROW]])
def test_real_receipt_and_encoded_request(monkeypatch, payload):
    calls = []
    async def transport(url, **kwargs):
        calls.append(url)
        assert set(kwargs) == {'response_callback'}
        return await kwargs['response_callback'](Response(payload), None)
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', transport)
    before = datetime.now(UTC)
    result = asyncio.run(Fetcher.fetch_data({'symbol': ' brk/b '}, {'fmp_api_key': 'synthetic-secret'})) if not payload else asyncio.run(Fetcher.fetch_data({'symbol': ' abc '}, {'fmp_api_key': 'synthetic-secret'}))
    assert len(calls) == 1
    assert urlsplit(calls[0]).path == '/stable/shares-float'
    assert parse_qs(urlsplit(calls[0]).query) == {'symbol': ['ABC' if payload else 'BRK/B'], 'apikey': ['synthetic-secret']}
    if not payload:
        assert 'BRK%2FB' in calls[0]
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert before <= datetime.fromisoformat(meta['retrieved_at']) <= datetime.now(UTC)
    assert len(result.result) == meta['bounds']['returned_count'] == len(payload)
    assert meta['bounds']['completeness'] == 'unknown'
    assert set(meta['fields']) == set(Data.model_fields)
    if not payload:
        assert all(field['availability'] == 'missing' for field in meta['fields'].values())


@pytest.mark.parametrize('status,code', [(401,'authentication'), (403,'entitlement'), (429,'throttling')])
def test_safe_http(monkeypatch, status, code):
    async def transport(url, **kwargs):
        response = Response({'error': 'synthetic-secret'})
        response.status, response.headers = status, {'Retry-After': '7'}
        return await kwargs['response_callback'](response, None)
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({'symbol': 'ABC'}, {'fmp_api_key': 'synthetic-secret'}))
    envelope = error.value.to_dict()
    assert envelope['code'] == code and 'synthetic-secret' not in str(envelope)
    if status == 429:
        assert envelope['retry_after_seconds'] == 7


@pytest.mark.parametrize('payload', [None, {}, {'data': []}, 'bad', ['bad'], [{'date': 'bad'}]])
def test_malformed_http(monkeypatch, payload):
    async def transport(url, **kwargs):
        return await kwargs['response_callback'](Response(payload), None)
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', transport)
    with pytest.raises(FinancialError):
        asyncio.run(Fetcher.fetch_data({'symbol': 'ABC'}))


def test_timeout(monkeypatch):
    async def transport(url, **kwargs):
        raise TimeoutError('synthetic-secret')
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({'symbol': 'ABC'}))
    assert error.value.code == 'timeout'
    assert 'synthetic-secret' not in str(error.value.to_dict())



def test_exact_import_origins():
    import importlib
    api = Path(__file__).resolve().parents[3] / 'data-api' / 'openbb_platform'
    expected = {
        'openbb_core': 'core/openbb_core/__init__.py',
        'openbb_fmp': 'providers/fmp/openbb_fmp/__init__.py',
        'openbb_fred': 'providers/fred/openbb_fred/__init__.py',
        'openbb_equity': 'extensions/equity/openbb_equity/__init__.py',
        'openbb_economy': 'extensions/economy/openbb_economy/__init__.py',
        'openbb_fmp.models.share_statistics': 'providers/fmp/openbb_fmp/models/share_statistics.py',
    }
    for module, relative in expected.items():
        assert Path(importlib.import_module(module).__file__).resolve() == (api / relative).resolve()


@pytest.mark.parametrize('field,aliases,value,expected', [
    ('free_float', ['free_float', 'freeFloat'], 25, .25),
    ('float_shares', ['float_shares', 'floatShares'], 0, 0),
    ('outstanding_shares', ['outstanding_shares', 'outstandingShares'], 100, 100),
    ('url', ['url', 'source'], 'https://example.com/report', 'https://example.com/report'),
])
def test_all_aliases(field, aliases, value, expected):
    for alias in aliases:
        row = Data.model_validate({'symbol': 'ABC', alias: value})
        assert getattr(row, field) == expected
        assert row.model_dump(by_alias=True)[field] == expected


def test_missing_optional_facts():
    result = transformed([{'symbol': 'ABC'}])
    assert result.result[0].model_dump() == {
        'symbol': 'ABC', 'date': None, 'free_float': None,
        'float_shares': None, 'outstanding_shares': None, 'url': None,
    }
    fields = result.metadata[FINANCIAL_METADATA_KEY]['fields']
    assert fields['symbol']['availability'] == 'available'
    assert all(fields[name]['availability'] == 'missing' for name in fields if name != 'symbol')


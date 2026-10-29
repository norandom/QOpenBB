"""Deterministic provider discovery identities and suggestion provenance."""
import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.equity_search import FMPEquitySearchFetcher as Search
from openbb_fmp.models.equity_peers import FMPEquityPeersFetcher as Peers
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 1, 2, tzinfo=UTC)

@pytest.mark.parametrize('fetcher,params', [(Search, {'query': 'Example'}), (Peers, {'symbol': 'EX'})])
@pytest.mark.parametrize('limit', [0, 101, -1, True, 1.5, '20'])
def test_invalid_limit(fetcher, params, limit):
    with pytest.raises(FinancialError):
        fetcher.transform_query({**params, 'limit': limit})

@pytest.mark.parametrize('query', ['', ' ', 'x\n', 'apikey=SECRET', 'https://secret'])
def test_invalid_search(query):
    with pytest.raises(FinancialError):
        Search.transform_query({'query': query})

@pytest.mark.parametrize('symbol', ['', ' ', 'A,B', 'A&apikey=SECRET', 'A\n'])
def test_invalid_peer_symbol(symbol):
    with pytest.raises(FinancialError):
        Peers.transform_query({'symbol': symbol})

@pytest.mark.parametrize('is_symbol,endpoint', [(False, 'search-name'), (True, 'search-symbol')])
def test_search_transport_and_identity(monkeypatch, is_symbol, endpoint):
    payload = [{'symbol': 'EX', 'name': 'Example', 'exchange': 'NYSE', 'currency': 'USD'},
               {'symbol': 'EX', 'name': 'Example', 'exchange': 'LSE', 'currency': 'GBP', 'cik': '123'}]
    original = deepcopy(payload)
    async def transport(url, **kwargs):
        parsed = urlsplit(url)
        assert parsed.path.endswith('/' + endpoint)
        assert parse_qs(parsed.query)['query'] == ['Example & Co']
        assert kwargs['typed_errors'] and kwargs['with_provenance']
        return FMPAcquisition(payload, STAMP)
    monkeypatch.setattr('openbb_fmp.utils.helpers.get_data_many', transport)
    query = Search.transform_query({'query': 'Example & Co', 'is_symbol': is_symbol})
    receipt = asyncio.run(Search.aextract_data(query, {'fmp_api_key': 'PRIVATE'}))
    result = Search.transform_data(query, receipt)
    assert payload == original and len(result.result) == 2
    assert result.result[0].listing_id != result.result[1].listing_id
    assert result.result[0].issuer_id is None and result.result[1].issuer_id == 'fmp:cik:123'
    assert [r.currency for r in result.result] == ['USD', 'GBP']
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(meta['retrieved_at']) == STAMP
    assert meta['source']['endpoint'] == endpoint
    assert meta['bounds']['completeness'] == 'unknown'
    assert 'PRIVATE' not in result.model_dump_json()
    assert set(meta['fields']) == set(type(result.result[0]).model_fields)


def test_peer_suggestions_and_clipping():
    payload = [{'symbol': 'EX', 'companyName': 'Example', 'price': 0, 'mktCap': 0},
               {'symbol': 'OTHER', 'companyName': 'Other', 'price': None, 'mktCap': None}]
    original = deepcopy(payload)
    query = Peers.transform_query({'symbol': ' src ', 'limit': 1})
    result = Peers.transform_data(query, FMPAcquisition(payload, STAMP))
    row = result.result[0]
    assert query.symbol == 'SRC' and row.price == 0 and row.market_cap == 0
    assert row.candidate_basis == 'provider_suggestion' and row.source_symbol == 'SRC'
    assert row.issuer_id is None and row.exchange is None
    assert payload == original
    assert result.metadata[FINANCIAL_METADATA_KEY]['bounds']['truncated'] is True
    assert result.metadata[FINANCIAL_METADATA_KEY]['bounds']['completeness'] == 'partial'

@pytest.mark.parametrize('fetcher,params', [(Search, {'query': 'Example'}), (Peers, {'symbol': 'EX'})])
def test_empty_and_bad_rows(fetcher, params):
    query = fetcher.transform_query(params)
    assert query.limit == 20
    assert fetcher.transform_data(query, FMPAcquisition([], STAMP)).result == []
    with pytest.raises(FinancialError):
        fetcher.transform_data(query, FMPAcquisition([{'symbol': None}], STAMP))

@pytest.mark.parametrize('fetcher,params', [(Search, {'query': 'Example'}), (Peers, {'symbol': 'EX'})])
@pytest.mark.parametrize('row', ['PRIVATE', 7, None, {'symbol': ' '}])
def test_malformed_rows_are_safe(fetcher, params, row):
    with pytest.raises(FinancialError) as caught:
        fetcher.transform_data(fetcher.transform_query(params), FMPAcquisition([row], STAMP))
    assert 'PRIVATE' not in str(caught.value)


def test_peer_transport_and_unknown_units(monkeypatch):
    async def transport(url, **kwargs):
        parsed = urlsplit(url)
        assert parsed.path.endswith('/stock-peers')
        assert parse_qs(parsed.query)['symbol'] == ['EX']
        assert 'limit' not in parse_qs(parsed.query)
        assert kwargs['typed_errors'] and kwargs['with_provenance']
        return FMPAcquisition([{'symbol': 'PEER', 'companyName': 'Peer', 'mktCap': 0}], STAMP)
    monkeypatch.setattr('openbb_fmp.utils.helpers.get_data_many', transport)
    query = Peers.transform_query({'symbol': 'EX'})
    result = Peers.transform_data(query, asyncio.run(Peers.aextract_data(query, None)))
    row = result.result[0]
    assert row.name == 'Peer' and row.currency is None
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    assert metadata['fields']['price']['unit'] == 'currency/share'
    assert metadata['fields']['market_cap']['value_origin'] == 'provider_calculation'
    assert metadata['fields']['market_cap']['currency_field'] == 'currency'
    assert metadata['transformations'][0]['name'] == 'provider_identity_qualification'
    assert metadata['bounds']['completeness'] == 'unknown'


def test_search_clipping_keeps_duplicates():
    query = Search.transform_query({'query': 'EX', 'limit': 1})
    payload = [{'symbol': 'EX'}, {'symbol': 'EX'}]
    result = Search.transform_data(query, FMPAcquisition(payload, STAMP))
    assert len(result.result) == 1
    assert result.metadata[FINANCIAL_METADATA_KEY]['bounds']['truncated'] is True

@pytest.mark.parametrize('fetcher,params', [(Search, {'query': 'EX'}), (Peers, {'symbol': 'EX'})])
def test_discovery_declarations_drive_metadata(fetcher, params, monkeypatch):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    query = fetcher.transform_query(params)
    model = fetcher.data_type
    declaration = bind_query_annotation(type(query))
    assert declaration.provider_policy == 'explicit'
    assert declaration.response_policy.mode == 'clip'
    assert declaration.response_policy.limit_parameter == 'limit'
    annotation = bind_data_annotation(model)
    assert set(annotation.fields) == set(model.model_fields)
    assert 'fields.availability' in annotation.runtime_properties
    templates = render_field_templates(model)
    result = fetcher.transform_data(query, FMPAcquisition([{'symbol': 'EX'}], STAMP))
    for name, template in templates.items():
        expected = template.model_dump(mode='json')
        expected['availability'] = 'available' if getattr(result.result[0], name) is not None else 'missing'
        assert result.metadata[FINANCIAL_METADATA_KEY]['fields'][name] == expected
    changed = model.financial_data_annotation.model_copy(deep=True)
    changed.fields['symbol'].scale = 7
    monkeypatch.setattr(model, 'financial_data_annotation', changed)
    altered = fetcher.transform_data(query, FMPAcquisition([{'symbol': 'EX'}], STAMP))
    assert altered.metadata[FINANCIAL_METADATA_KEY]['fields']['symbol']['scale'] == 7
    assert templates['symbol'].scale is None
    assert result.metadata[FINANCIAL_METADATA_KEY]['fields']['symbol']['scale'] is None


def test_discovery_length_boundaries():
    assert Search.transform_query({'query': 'x' * 200}).query == 'x' * 200
    assert Peers.transform_query({'symbol': 'x' * 50}).symbol == 'X' * 50
    for fetcher, params in [(Search, {'query': 'x' * 201}),
                            (Search, {'query': ' ' + 'x' * 200}),
                            (Peers, {'symbol': 'x' * 51})]:
        with pytest.raises(FinancialError):
            fetcher.transform_query(params)

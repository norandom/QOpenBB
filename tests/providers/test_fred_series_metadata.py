"""Generic FRED series retain financial meaning and acquisition freshness."""
import asyncio
from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import pytest
from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_fred.models.series import FredSeriesFetcher
from openbb_fred.utils.acquisition import FredAcquisition


@pytest.fixture
def acquisitions(monkeypatch):
    calls = []
    async def request(url, **kwargs):
        calls.append((url, kwargs))
        params = parse_qs(urlparse(url).query)
        series = params['series_id'][0]
        observations = urlparse(url).path.endswith('observations')
        if observations:
            payload = {'observations': [
                {'date': '2024-01-01', 'value': '0', 'realtime_start': '2024-02-01', 'realtime_end': '2024-03-01'},
                {'date': '2024-04-01', 'value': '.', 'realtime_start': '2024-05-01'},
            ]}
        else:
            payload = {'seriess': [{'title': f'{series} economic benchmark', 'units': 'Billions of Dollars', 'frequency': 'Quarterly', 'seasonal_adjustment': 'Seasonally Adjusted Annual Rate', 'notes': 'Source notes'}]}
        day = (4 if observations else 2) if series == 'GDP' else 1
        acquired = FredAcquisition(payload, datetime(2025, 1, day, tzinfo=timezone.utc), 'memory' if observations else 'disk')
        return acquired if kwargs.get('with_provenance') else deepcopy(payload)
    monkeypatch.setattr('openbb_fred.utils.rate_limiter.fred_get', request)
    return calls


def execute(**params):
    query = FredSeriesFetcher.transform_query({'symbol': 'GDP', **params})
    raw = asyncio.run(FredSeriesFetcher.aextract_data(query, {'fred_api_key': 'private-fixture'}))
    return FredSeriesFetcher.transform_data(query, raw)


def test_dynamic_declarations_preserve_modeled_date_and_baseline_policy():
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    from openbb_fred.models.series import FredSeriesData, FredSeriesQueryParams

    query = bind_query_annotation(FredSeriesQueryParams)
    assert query.provider_policy == 'baseline_default'
    assert query.response_policy.model_dump() == {
        'mode': 'provider', 'max_rows': None, 'limit_parameter': None,
    }
    assert FredSeriesQueryParams(symbol='gdp').limit == 100000
    assert FredSeriesQueryParams(symbol='gdp').aggregation_method == 'eop'
    assert FredSeriesQueryParams.__alias_dict__['transform'] == 'units'
    data = bind_data_annotation(FredSeriesData)
    assert data.dynamic_fields is True
    assert set(data.fields) == {'date'}
    date = render_field_templates(FredSeriesData)['date']
    assert date.definition == FredSeriesData.model_fields['date'].description
    assert date.unit is None
    assert date.observation_date_field == 'date'
    assert {'fields', 'fields.unit', 'fields.source_unit', 'fields.source_frequency',
            'fields.effective_frequency', 'fields.seasonal_adjustment',
            'fields.requested_transform', 'fields.aggregation', 'fields.availability',
            'transformations', 'observation_provenance', 'vintage_query_supported',
            'point_in_time_safe'} <= set(data.runtime_properties)


def test_dynamic_resolution_paths_agree_without_adding_static_date_metadata(acquisitions):
    from openbb_core.provider.standard_models.financial_annotations import bind_data_annotation
    from openbb_fred.models.series import FredSeriesData

    declaration = bind_data_annotation(FredSeriesData)
    common = execute(symbol='GDP,CPIAUCSL', transform='pch', frequency='a').metadata[FINANCIAL_METADATA_KEY]
    assert set(common['fields']) == {'GDP', 'CPIAUCSL'}
    for path in declaration.runtime_properties:
        root, *nested = path.split('.')
        assert root in common
        if nested:
            assert all(nested[0] in field for field in common[root].values())
    assert common['fields']['GDP']['unit'] == 'Percent Change'
    assert common['fields']['GDP']['effective_frequency'] == 'Annual'
    assert common['fields']['GDP']['availability'] == 'unknown'
    assert common['point_in_time_safe'] is False


def test_oldest_components_intervals_and_legacy_wide_output(acquisitions):
    result = execute(symbol='GDP,CPIAUCSL', use_cache=False)
    assert [row.model_dump(mode='json') for row in result.result] == [
        {'date': '2024-01-01', 'GDP': 0.0, 'CPIAUCSL': 0.0},
        {'date': '2024-04-01', 'GDP': None, 'CPIAUCSL': None},
    ]
    meta = result.metadata
    assert meta['GDP'] == {'title': 'GDP economic benchmark', 'units': 'Billions of Dollars', 'frequency': 'Quarterly', 'seasonal_adjustment': 'Seasonally Adjusted Annual Rate', 'notes': 'Source notes'}
    common = meta[FINANCIAL_METADATA_KEY]
    assert common['retrieved_at'] == '2025-01-01T00:00:00Z'
    assert common['provider'] == 'fred'
    assert common['point_in_time_safe'] is False
    assert common['vintage_query_supported'] is None
    assert common['observation_provenance']['GDP'] == {
        '2024-01-01': {'realtime_start': '2024-02-01', 'realtime_end': '2024-03-01'},
        '2024-04-01': {'realtime_start': '2024-05-01', 'realtime_end': None},
    }
    assert all(options['with_provenance'] is True for _, options in acquisitions)
    assert all(options['use_cache'] is False for _, options in acquisitions)
    assert 'private-fixture' not in str(common)
    assert common['effective_query']['symbol'] == 'GDP,CPIAUCSL'


@pytest.mark.parametrize('transform,unit', [(None, 'Billions of Dollars'), ('pch', 'Percent Change'), ('pc1', 'Percent Change from Year Ago'), ('log', None)])
def test_source_and_effective_transform_units(acquisitions, transform, unit):
    result = execute(transform=transform)
    common = result.metadata[FINANCIAL_METADATA_KEY]
    field = common['fields']['GDP']
    assert field['source_unit'] == 'Billions of Dollars'
    assert field['unit'] == unit
    assert field['source_frequency'] == field['effective_frequency'] == 'Quarterly'
    assert field['requested_transform'] == transform
    assert field['value_origin'] == ('provider_calculation' if transform else 'provider_observation')
    if transform:
        assert common['transformations']
    if unit is None:
        assert any('effective unit' in text.lower() for text in common['limitations'])
    obs_url = next(url for url, _ in acquisitions if urlparse(url).path.endswith('observations'))
    assert parse_qs(urlparse(obs_url).query).get('units') == ([transform] if transform else None)


@pytest.mark.parametrize('method', ['avg', 'sum', 'eop'])
def test_explicit_aggregation_frequency_preserves_source(acquisitions, method):
    common = execute(frequency='a', aggregation_method=method).metadata[FINANCIAL_METADATA_KEY]
    field = common['fields']['GDP']
    assert field['source_frequency'] == 'Quarterly'
    assert field['effective_frequency'] == 'Annual'
    assert field['aggregation'] == method
    assert any(item['name'] == 'frequency_aggregation' for item in common['transformations'])


def test_reserved_series_rejected_before_transport(acquisitions):
    with pytest.raises(ValueError):
        execute(symbol=f'GDP,{FINANCIAL_METADATA_KEY}')
    assert acquisitions == []


def test_unequal_dates_align_without_interpolation(acquisitions, monkeypatch):
    from openbb_fred.utils import rate_limiter
    original = rate_limiter.fred_get
    async def shifted(url, **kwargs):
        value = await original(url, **kwargs)
        if 'series_id=CPIAUCSL' in url and urlparse(url).path.endswith('observations'):
            value.payload['observations'][0]['date'] = '2024-02-01'
        return value
    monkeypatch.setattr(rate_limiter, 'fred_get', shifted)
    rows = [row.model_dump(mode='json') for row in execute(symbol='GDP,CPIAUCSL').result]
    assert rows == [
        {'date': '2024-01-01', 'GDP': 0.0, 'CPIAUCSL': None},
        {'date': '2024-02-01', 'GDP': None, 'CPIAUCSL': 0.0},
        {'date': '2024-04-01', 'GDP': None, 'CPIAUCSL': None},
    ]


@pytest.mark.parametrize('transform', ['chg', 'ch1', 'pca', 'cch', 'cca', 'log'])
def test_unestablished_units_stay_unknown_and_options_survive(acquisitions, transform):
    common = execute(transform=transform, frequency='a', aggregation_method='sum', limit=2,
                     start_date='2024-01-01', end_date='2024-12-31').metadata[FINANCIAL_METADATA_KEY]
    assert common['fields']['GDP']['unit'] is None
    assert common['fields']['GDP']['requested_transform'] == transform
    assert any('effective unit' in text.lower() for text in common['limitations'])
    url = next(url for url, _ in acquisitions if urlparse(url).path.endswith('observations'))
    params = parse_qs(urlparse(url).query)
    assert params['series_id'] == ['GDP']
    assert params['units'] == [transform]
    assert params['frequency'] == ['a']
    assert params['aggregation_method'] == ['sum']
    assert params['limit'] == ['2']
    assert params['observation_start'] == ['2024-01-01']
    assert params['observation_end'] == ['2024-12-31']

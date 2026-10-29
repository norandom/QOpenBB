"""Periodic metrics preserve provider financial meaning without TTM synthesis."""
import asyncio
from datetime import UTC, datetime
from copy import deepcopy
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.key_metrics import FMPKeyMetricsFetcher as Fetcher
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, tzinfo=UTC)


def fixture(**extra):
    return {"symbol": "ABC", "date": "2023-12-31", "period": "FY",
            "fiscalYear": "2023", "reportedCurrency": "EUR", "marketCap": 100,
            "enterpriseValue": -2, "evToEBITDA": 0, "returnOnEquity": -.2,
            "grahamNetNet": -3, "freeCashFlowToEquity": 5,
            "researchAndDevelopementToRevenue": .15, **extra}


@pytest.mark.parametrize("params", [
    {"symbol": "A,B"}, {"symbol": "A&apikey=secret"}, {"symbol": "A\n"},
    {"symbol": None}, {"symbol": ""}, {"symbol": "A", "period": "ttm"},
    {"symbol": "A", "ttm": "only"}, {"symbol": "A", "ttm": "include"},
    *[{"symbol": "A", "limit": x} for x in [0, 1001, True, "5", 5., None]],
])
def test_invalid_before_io(params):
    with pytest.raises(FinancialError):
        Fetcher.transform_query(params)


@pytest.mark.parametrize("period", ["annual", "quarter", "quarterly"])
def test_periodic_semantics(period):
    query = Fetcher.transform_query({"symbol": " abc ", "period": period})
    payload = [fixture()]
    original = deepcopy(payload)
    result = Fetcher.transform_data(query, FMPAcquisition(payload, STAMP))
    row = result.result[0]
    assert payload == original
    assert row.enterprise_value == -2 and row.ev_to_ebitda == 0
    assert row.return_on_equity == -.2 and row.research_and_development_to_revenue == .15
    assert row.fiscal_year == 2023 and row.currency == "EUR"
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["fields"]["return_on_equity"]["unit"] == "fraction"
    assert meta["fields"]["ev_to_ebitda"]["unit"] == "multiple"
    assert meta["fields"]["graham_net_net"]["unit"] == "currency/share"
    assert meta["fields"]["free_cash_flow_to_equity"]["unit"] == "currency"
    assert meta["fields"]["cash_conversion_cycle"]["unit"] == "days"
    assert meta["fields"]["enterprise_value"]["financial_basis"]["debt"] is None
    assert set(meta["fields"]) == set(type(row).model_fields)


def test_missing_no_fabrication_and_stable_ties():
    query = Fetcher.transform_query({"symbol": "ABC", "limit": 2})
    payload = [{"symbol": "ABC", "enterpriseValue": 1},
               fixture(enterpriseValue=2), fixture(enterpriseValue=3)]
    result = Fetcher.transform_data(query, FMPAcquisition(payload, STAMP))
    assert [r.enterprise_value for r in result.result] == [2, 3]
    assert result.metadata[FINANCIAL_METADATA_KEY]["bounds"]["truncated"] is True
    row = Fetcher.transform_data(query, FMPAcquisition(payload[:1], STAMP)).result[0]
    assert row.period_ending is None and row.fiscal_year is None
    assert row.fiscal_period is None and row.currency is None and row.market_cap is None


@pytest.mark.parametrize("field,value", [("returnOnAssets", "bad"), ("date", "bad"), ("marketCap", float("nan"))])
def test_invalid_rows_safe(field, value):
    with pytest.raises(FinancialError):
        Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                               FMPAcquisition([fixture(**{field: value})], STAMP))


def test_periodic_transport(monkeypatch):
    calls = []
    async def transport(url, **kwargs):
        calls.append((url, kwargs))
        return FMPAcquisition([fixture()], STAMP)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    query = Fetcher.transform_query({"symbol": "abc", "period": "quarterly", "ttm": "exclude"})
    result = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "test"}))
    assert result.retrieved_at == STAMP and len(calls) == 1
    url, kwargs = calls[0]
    assert urlsplit(url).path == "/stable/key-metrics"
    assert parse_qs(urlsplit(url).query) == {"symbol": ["ABC"], "period": ["quarter"], "limit": ["5"], "apikey": ["test"]}
    assert kwargs == {"with_provenance": True, "typed_errors": True}

@pytest.mark.parametrize("key,field,value", [
    ("researchAndDevelopmentToRevenue", "research_and_development_to_revenue", -.3),
    ("researchAndDevelopementToRevenue", "research_and_development_to_revenue", 0),
    ("netDebtToEBITDA", "net_debt_to_ebitda", -2),
    ("freeCashFlowToFirm", "free_cash_flow_to_firm", -10),
    ("capexToDepreciation", "capex_to_depreciation", 1.2),
    ("daysOfInventoryOutstanding", "days_of_inventory_outstanding", 4.5),
])
def test_current_and_retained_aliases(key, field, value):
    payload = {"symbol": "ABC", key: value}
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                                   FMPAcquisition([payload], STAMP))
    assert getattr(result.result[0], field) == value
    assert set(result.result[0].model_dump()) == set(type(result.result[0]).model_fields)


@pytest.mark.parametrize("labels,basis", [(["FY"], "annual"), (["Q1", "Q4"], "discrete_quarter"),
                                         (["FY", "Q4"], None), ([None], None)])
def test_actual_period_basis(labels, basis):
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                                   FMPAcquisition([fixture(period=p) for p in labels], STAMP))
    fields = result.metadata[FINANCIAL_METADATA_KEY]["fields"]
    assert fields["return_on_assets"]["period_basis"] == basis
    assert fields["market_cap"]["valuation_date_field"] is None
    assert fields["market_cap"]["observation_date_field"] is None
    assert fields["market_cap"]["financial_basis"]["market_date"] is None
    assert all(f["unit"] is not None for n, f in fields.items()
               if n not in {"symbol", "period_ending", "fiscal_year", "fiscal_period", "currency"})


def test_unmodeled_provider_amount_omitted():
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                                   FMPAcquisition([fixture(unknownAmount=1234)], STAMP))
    emitted = result.result[0].model_dump()
    assert "unknownAmount" not in emitted and "unknown_amount" not in emitted
    assert set(emitted) == set(result.metadata[FINANCIAL_METADATA_KEY]["fields"])


def test_declarations_cover_runtime_without_mutating_templates():
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    from openbb_fmp.models.key_metrics import FMPKeyMetricsQueryParams
    from openbb_fmp.models.key_metrics_data import FMPKeyMetricsData

    query_annotation = bind_query_annotation(FMPKeyMetricsQueryParams)
    assert query_annotation.provider_policy == "explicit"
    assert query_annotation.response_policy.mode == "clip"
    assert query_annotation.response_policy.limit_parameter == "limit"
    assert query_annotation.response_policy.max_rows is None
    declaration = bind_data_annotation(FMPKeyMetricsData)
    original = deepcopy(FMPKeyMetricsData.financial_data_annotation.model_dump())
    templates = render_field_templates(FMPKeyMetricsData)
    assert set(templates) == set(FMPKeyMetricsData.model_fields)
    assert not declaration.dynamic_fields
    assert {"fields.availability", "fields.period_basis"} <= set(declaration.runtime_properties)
    query = Fetcher.transform_query({"symbol": "ABC", "limit": 1})
    result = Fetcher.transform_data(query, FMPAcquisition([fixture(), fixture()], STAMP))
    fields = result.metadata[FINANCIAL_METADATA_KEY]["fields"]
    for name, template in templates.items():
        expected = template.model_dump(mode="json")
        assert {k: v for k, v in fields[name].items() if k not in {"availability", "period_basis"}} == {
            k: v for k, v in expected.items() if k not in {"availability", "period_basis"}
        }
    assert result.metadata[FINANCIAL_METADATA_KEY]["bounds"]["truncated"] is True
    templates["enterprise_value"].financial_basis["debt"] = "changed"
    assert render_field_templates(FMPKeyMetricsData)["enterprise_value"].financial_basis["debt"] is None
    assert FMPKeyMetricsData.financial_data_annotation.model_dump() == original


def test_runtime_reads_class_owned_templates(monkeypatch):
    from openbb_fmp.models.key_metrics_data import FMPKeyMetricsData

    declaration = FMPKeyMetricsData.financial_data_annotation.model_copy(deep=True)
    declaration.fields["enterprise_value"].financial_basis["debt"] = "test convention"
    monkeypatch.setattr(FMPKeyMetricsData, "financial_data_annotation", declaration)
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                                   FMPAcquisition([fixture()], STAMP))
    assert result.metadata[FINANCIAL_METADATA_KEY]["fields"]["enterprise_value"]["financial_basis"]["debt"] == "test convention"

"""Installed Batch B registry contracts; no acquisition or live entitlement claims."""

import importlib
import json
import tarfile
from datetime import UTC, datetime
from hashlib import sha256
from importlib.metadata import distribution
from inspect import getfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "vendor/data-api/openbb_platform/providers/fmp"
BATCH_B = {
    "HistoricalDividends": ("historical_dividends", "FMPHistoricalDividendsFetcher", "equity/fundamental/dividends"),
    "HistoricalSplits": ("historical_splits", "FMPHistoricalSplitsFetcher", "equity/fundamental/historical_splits"),
    "CalendarEarnings": ("calendar_earnings", "FMPCalendarEarningsFetcher", "equity/calendar/earnings"),
    "CalendarDividend": ("calendar_dividend", "FMPCalendarDividendFetcher", "equity/calendar/dividend"),
    "CalendarSplits": ("calendar_splits", "FMPCalendarSplitsFetcher", "equity/calendar/splits"),
    "CompanyNews": ("company_news", "FMPCompanyNewsFetcher", "news/company"),
    "EarningsCallTranscript": ("earnings_call_transcript", "FMPEarningsCallTranscriptFetcher", "equity/fundamental/transcript"),
    "CompanyFilings": ("company_filings", "FMPCompanyFilingsFetcher", "equity/fundamental/filings"),
}


def test_installed_exact_union_and_module_bytes():
    from openbb_core.app.extension_loader import ExtensionLoader
    from openbb_core.provider.registry_map import RegistryMap
    from test_fmp_batch_a_registration import BASELINE, BATCH_A

    provider = ExtensionLoader().provider_objects["fmp"]
    mapping = RegistryMap().original_models
    original = BASELINE | BATCH_A
    assert len(original) == 21
    assert set(original) <= set(provider.fetcher_dict)
    assert len(provider.fetcher_dict) == 29
    assert set(provider.fetcher_dict) == set(original | BATCH_B)
    assert {key for key, variants in mapping.items() if "fmp" in variants} == set(original | BATCH_B)
    installed = Path(distribution("openbb-fmp").locate_file("openbb_fmp")).resolve()
    assert installed != (PACKAGE / "openbb_fmp").resolve()
    for key, (module_name, class_name, *_) in (original | BATCH_B).items():
        module = importlib.import_module("openbb_fmp.models." + module_name)
        fetcher = getattr(module, class_name)
        path = Path(getfile(fetcher)).resolve()
        assert path.is_relative_to(installed)
        assert path.read_bytes() == (PACKAGE / "openbb_fmp/models" / (module_name + ".py")).read_bytes()
        assert provider.fetcher_dict[key] is fetcher
        assert mapping[key]["fmp"]["query"] is fetcher.query_params_type
        assert mapping[key]["fmp"]["data"] is fetcher.data_type


@pytest.mark.parametrize("model", BATCH_B)
def test_installed_native_provider_binding_and_financial_descriptors(model):
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation,
        bind_query_annotation,
        render_field_templates,
    )

    variant = RegistryMap().original_models[model]["fmp"]
    query, data = variant["query"], variant["data"]
    assert bind_query_annotation(query).provider_policy == "explicit"
    fields = render_field_templates(data)
    assert set(fields) == set(data.model_fields) == set(bind_data_annotation(data).fields)
    for name, field in fields.items():
        assert field.definition == data.model_fields[name].description
        assert field.definition.strip()
    routes = [route for route in iter_api_routes(app)
              if (getattr(route, "openapi_extra", None) or {}).get("model") == model]
    assert len(routes) == 1
    assert routes[0].path == "/api/v1/" + BATCH_B[model][2]
    operation = app.openapi()["paths"][routes[0].path]["get"]
    provider, = [item for item in operation["parameters"] if item["name"] == "provider"]
    assert provider["schema"]["const"] == "fmp"


def test_installed_news_surface_excludes_rss_and_world():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes

    assert {r.path for r in iter_api_routes(app) if "/news/" in r.path} == {"/api/v1/news/company"}


@pytest.mark.parametrize("model", BATCH_B)
def test_selected_registered_metadata_matches_rendered_fields(model):
    from openbb_core.app.extension_loader import ExtensionLoader
    from openbb_core.provider.standard_models.financial_annotations import (
        render_field_templates,
    )
    from openbb_core.provider.standard_models.financial_metadata import (
        FINANCIAL_METADATA_KEY,
        FinancialResultMetadata,
    )
    from openbb_fmp.utils.helpers import FMPAcquisition

    module = BATCH_B[model][0]
    fixtures = ROOT / "tests/providers/fixtures/fmp_batch_b"
    folder = "documents" if model in {"CompanyNews", "CompanyFilings", "EarningsCallTranscript"} else "events"
    examples = json.loads((fixtures / folder / "serialization_examples.json").read_text())
    sample = next(item for item in examples if item["model"] == module)
    handoff = next(item for item in json.loads((fixtures / "handoffs.json").read_text())["widgets"] if item["model"] == model)
    params = sample.get("query", {key: value for key, value in handoff["params"].items() if key != "provider"})
    fetcher = ExtensionLoader().provider_objects["fmp"].fetcher_dict[model]
    query = fetcher.transform_query(params)
    stamp = datetime(2026, 11, 18, tzinfo=UTC)
    result = fetcher.transform_data(query, FMPAcquisition([sample["raw"]], stamp))
    metadata = FinancialResultMetadata.model_validate(result.metadata[FINANCIAL_METADATA_KEY])
    assert metadata.provider == "fmp"
    assert metadata.dataset == BATCH_B[model][2]
    assert metadata.retrieved_at == stamp
    assert metadata.effective_query == query.model_dump(mode="json")
    assert metadata.bounds.returned_count == len(result.result) == 1
    templates = render_field_templates(fetcher.data_type)
    assert set(metadata.fields) == set(templates)
    for name, field in metadata.fields.items():
        assert field.model_dump(exclude={"availability"}) == templates[name].model_dump(exclude={"availability"})


@pytest.mark.parametrize("model", BATCH_B)
def test_selected_registry_schemas_match_frozen_contracts(model):
    from openbb_core.provider.registry_map import RegistryMap

    module = BATCH_B[model][0]
    documents = model in {"CompanyNews", "CompanyFilings", "EarningsCallTranscript"}
    folder = "documents" if documents else "events"
    fixture = ROOT / "tests/providers/fixtures/fmp_batch_b" / folder / (module + ".json")
    contract = json.loads(fixture.read_text())
    variant = RegistryMap().original_models[model]["fmp"]
    for kind in ("query", "data"):
        for mode in ("validation", "serialization"):
            schema = variant[kind].model_json_schema(mode=mode)
            if documents:
                expected = contract["expected"][f"{'row' if kind == 'data' else kind}_{mode}"]
                if kind == "data":
                    for name, field in schema["properties"].items():
                        assert field.pop("description") == variant[kind].model_fields[name].description
            else:
                expected = contract[kind][mode]
                schema.pop("description", None)
                schema["title"] = expected["title"]
            assert schema == expected


def test_batch_b_archive_lineage_and_installed_candidate_identity():
    provenance = json.loads((PACKAGE / "provenance.json").read_text())
    archive = ROOT / provenance["artifact"]["retained_path"]
    assert sha256(archive.read_bytes()).hexdigest() == provenance["artifact"]["sha256"] == "5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517"
    installed = Path(distribution("openbb-fmp").locate_file("openbb_fmp"))
    with tarfile.open(archive) as source:
        for module, _, _ in BATCH_B.values():
            path = "openbb_fmp/models/" + module + ".py"
            entry = provenance["adapted_files"][path]
            assert entry["archive_member"] == "openbb_fmp-1.6.1/" + path
            original = source.extractfile(entry["archive_member"]).read()
            assert sha256(original).hexdigest() == entry["archive_sha256"]
            assert entry["batch"] == "B"
            assert sha256((PACKAGE / path).read_bytes()).hexdigest() == sha256((installed / "models" / (module + ".py")).read_bytes()).hexdigest()

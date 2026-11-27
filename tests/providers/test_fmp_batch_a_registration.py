"""Installed registration and retained-source provenance, offline only."""

import importlib
import json
import tarfile
from hashlib import sha256
from importlib.metadata import distribution
from inspect import getfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = (ROOT / "vendor/data-api").resolve()
PACKAGE = API / "openbb_platform/providers/fmp"
BASELINE = {
    "EquityInfo": ("equity_profile", "FMPEquityProfileFetcher"),
    "IncomeStatement": ("income_statement", "FMPIncomeStatementFetcher"),
    "BalanceSheet": ("balance_sheet", "FMPBalanceSheetFetcher"),
    "CashFlowStatement": ("cash_flow", "FMPCashFlowStatementFetcher"),
    "EquitySearch": ("equity_search", "FMPEquitySearchFetcher"),
    "EquityPeers": ("equity_peers", "FMPEquityPeersFetcher"),
    "EquityHistorical": ("equity_historical", "FMPEquityHistoricalFetcher"),
    "KeyMetrics": ("key_metrics", "FMPKeyMetricsFetcher"),
    "FinancialRatios": ("financial_ratios", "FMPFinancialRatiosFetcher"),
    "EnterpriseValues": ("enterprise_values", "FMPEnterpriseValuesFetcher"),
}
BATCH_A = {
    "AnalystEstimates": ("analyst_estimates", "FMPAnalystEstimatesFetcher", "estimates/historical"),
    "PriceTarget": ("price_target", "FMPPriceTargetFetcher", "estimates/price_target"),
    "PriceTargetConsensus": ("price_target_consensus", "FMPPriceTargetConsensusFetcher", "estimates/consensus"),
    "RevenueBusinessLine": ("revenue_business_line", "FMPRevenueBusinessLineFetcher", "fundamental/revenue_per_segment"),
    "RevenueGeographic": ("revenue_geographic", "FMPRevenueGeographicFetcher", "fundamental/revenue_per_geography"),
    "HistoricalMarketCap": ("historical_market_cap", "FmpHistoricalMarketCapFetcher", "historical_market_cap"),
    "ShareStatistics": ("share_statistics", "FMPShareStatisticsFetcher", "ownership/share_statistics"),
    "EquityQuote": ("equity_quote", "FMPEquityQuoteFetcher", "price/quote"),
    "IncomeStatementGrowth": ("income_statement_growth", "FMPIncomeStatementGrowthFetcher", "fundamental/income_growth"),
    "BalanceSheetGrowth": ("balance_sheet_growth", "FMPBalanceSheetGrowthFetcher", "fundamental/balance_growth"),
    "CashFlowStatementGrowth": ("cash_flow_growth", "FMPCashFlowStatementGrowthFetcher", "fundamental/cash_growth"),
}


def test_actual_registry_exact_keys_fetcher_identity_and_source_origins():
    from openbb_core.app.extension_loader import ExtensionLoader
    from openbb_core.provider.registry_map import RegistryMap

    registry = RegistryMap()
    provider = ExtensionLoader().provider_objects["fmp"]
    from test_fmp_batch_b_registration import BATCH_B

    expected = BASELINE | BATCH_A | BATCH_B
    assert set(provider.fetcher_dict) == set(expected)
    assert {key for key, variants in registry.original_models.items() if "fmp" in variants} == set(expected)
    assert registry.registry.providers["fmp"] is provider
    assert provider.credentials == ["fmp_api_key"]
    for key, (module_name, class_name, *_) in expected.items():
        module = importlib.import_module("openbb_fmp.models." + module_name)
        fetcher = getattr(module, class_name)
        assert provider.fetcher_dict[key] is fetcher
        assert Path(getfile(fetcher)).resolve() == Path(distribution("openbb-fmp").locate_file("openbb_fmp/models/" + module_name + ".py")).resolve()
        assert registry.original_models[key]["fmp"]["query"] is fetcher.query_params_type
        assert registry.original_models[key]["fmp"]["data"] is fetcher.data_type
    for namespace in ("openbb_core", "openbb_equity", "openbb_economy", "openbb_fmp", "openbb_fred"):
        module = importlib.import_module(namespace)
        assert Path(module.__file__).resolve().is_relative_to(Path(distribution(namespace.replace("_", "-")).locate_file(namespace)).resolve())


def test_actual_native_batch_a_route_associations():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes

    routes = [route for route in iter_api_routes(app)
              if (getattr(route, "openapi_extra", None) or {}).get("model") in BATCH_A]
    assert len(routes) == 11
    assert {route.openapi_extra["model"]: route.path for route in routes} == {
        key: "/api/v1/equity/" + value[2] for key, value in BATCH_A.items()
    }


def test_original_archive_hashes_notices_and_extracted_growth_lineage():
    manifest = json.loads((ROOT / "tests/providers/fixtures/fmp_batch_a/source_manifest.json").read_text())
    provenance = json.loads((PACKAGE / "provenance.json").read_text())
    archive = ROOT / manifest["archive"]["path"]
    assert sha256(archive.read_bytes()).hexdigest() == manifest["archive"]["sha256"] == provenance["artifact"]["sha256"]
    assert provenance["license"]["sha256"] == manifest["notices"]["sha256"]
    assert sha256((PACKAGE / "LICENSE").read_bytes()).hexdigest() == manifest["notices"]["sha256"]
    assert b"GNU AFFERO GENERAL PUBLIC LICENSE" in (PACKAGE / "LICENSE").read_bytes()
    assert "offline" in provenance["runtime_compatibility"].lower()
    assert "live" in provenance["runtime_compatibility"].lower()
    with tarfile.open(archive) as source:
        notices = [m.name for m in source.getmembers() if m.isfile() and Path(m.name).name.lower().startswith(("license", "notice"))]
        assert notices == manifest["notices"]["archive_standalone_notices"]
        for item in manifest["members"]:
            path = item["member"].split("/", 1)[1]
            entry = provenance["adapted_files"][path]
            assert entry["archive_member"] == item["member"]
            assert entry["archive_sha256"] == item["sha256"] == sha256(source.extractfile(item["member"]).read()).hexdigest()
            assert entry["task"].startswith("3.")
            if path.endswith(("income_statement_growth.py", "balance_sheet_growth.py", "cash_flow_growth.py")):
                derived = provenance["adapted_files"][path.removesuffix(".py") + "_data.py"]
                assert derived["archive_member"] == item["member"]
                assert derived["archive_sha256"] == item["sha256"]
                assert derived["derived_from"] == path
        for path, digest in provenance["unchanged_files"].items():
            assert sha256((PACKAGE / path).read_bytes()).hexdigest() == digest
            assert (PACKAGE / path).read_bytes() == source.extractfile("openbb_fmp-1.6.1/" + path).read()

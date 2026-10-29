"""Installed FMP discovery, without financial-provider network requests."""

import io
import json
import subprocess
import tarfile
import tomllib
from hashlib import sha256
from importlib.metadata import distribution, distributions
from inspect import getfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "vendor/data-api/openbb_platform/providers/fmp"
FMP_MODELS = {
    "EquityInfo", "IncomeStatement", "BalanceSheet", "CashFlowStatement",
    "EquitySearch", "EquityPeers", "EquityHistorical", "KeyMetrics",
    "FinancialRatios", "EnterpriseValues",
}


def test_installed_fmp_entry_point_and_core_loader():
    dist = distribution("openbb-fmp")
    entries = [ep for ep in dist.entry_points if ep.group == "openbb_provider_extension"]
    assert [(ep.name, ep.value) for ep in entries] == [("fmp", "openbb_fmp:fmp_provider")]
    from openbb_core.app.extension_loader import ExtensionLoader

    loader = ExtensionLoader()
    provider = loader.provider_objects["fmp"]
    assert provider is entries[0].load()
    assert set(provider.fetcher_dict) == FMP_MODELS
    assert provider.credentials == ["fmp_api_key"]
    assert distribution("openbb-core").version == "2.0.1"
    assert distribution("openbb-equity").version == "2.0.0"
    assert distribution("openbb-economy").version == "2.0.0"
    assert distribution("openbb-fred").version == "2.0.0"
    assert dist.version == "1.6.1+qopenbb.1"
    assert {"equity", "economy"} <= {ep.name for ep in loader.core_entry_points}


def test_registered_models_are_installed_packages():
    from openbb_core.app.extension_loader import ExtensionLoader

    for name in ("fmp", "fred"):
        package = Path(distribution("openbb-" + name).locate_file("openbb_" + name)).resolve()
        provider = ExtensionLoader().provider_objects[name]
        assert package.is_dir()
        for fetcher in provider.fetcher_dict.values():
            assert Path(getfile(fetcher)).resolve().is_relative_to(package)


def test_first_batch_native_routes_and_model_associations():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap

    expected = {
        "EquityInfo": "/equity/profile",
        "EquitySearch": "/equity/search",
        "EquityPeers": "/equity/compare/peers",
        "IncomeStatement": "/equity/fundamental/income",
        "BalanceSheet": "/equity/fundamental/balance",
        "CashFlowStatement": "/equity/fundamental/cash",
        "KeyMetrics": "/equity/fundamental/metrics",
        "FinancialRatios": "/equity/fundamental/ratios",
        "EnterpriseValues": "/equity/fundamental/enterprise_values",
        "EquityHistorical": "/equity/price/historical",
        "FredSeries": "/economy/fred_series",
    }
    mapping = RegistryMap().original_models
    # FRED's existing broader registration stays available outside this batch.
    assert set(expected) <= set(mapping)
    routes = [route for route in iter_api_routes(app)
              if (getattr(route, "openapi_extra", None) or {}).get("model") in expected]
    assert len(routes) == len(expected)
    assert {route.openapi_extra["model"]: route.path for route in routes} == {
        model: "/api/v1" + path for model, path in expected.items()
    }
    schema = app.openapi()
    ids = [schema["paths"][route.path]["get"]["operationId"] for route in routes]
    assert len(ids) == len(set(ids))
    for model in expected:
        providers = mapping[model]
        assert set(providers) == ({"fred"} if model == "FredSeries" else {"fmp"})


def installed_code_identity():
    """Compare wheel code with committed bytes, independent of checkout line endings."""
    packages = {
        "openbb-core": "openbb_platform/core",
        "openbb-equity": "openbb_platform/extensions/equity",
        "openbb-economy": "openbb_platform/extensions/economy",
        "openbb-fmp": "openbb_platform/providers/fmp",
        "openbb-fred": "openbb_platform/providers/fred",
    }
    command = ["git", "-C", str(ROOT / "vendor/data-api"), "archive", "HEAD", "--", *packages.values()]
    archive = subprocess.check_output(command)
    result = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        revision = source.pax_headers["comment"]
        members = {item.name: item for item in source.getmembers() if item.isfile()}
        for name, directory in packages.items():
            namespace = name.replace("-", "_")
            prefix = directory + "/"
            expected = {path.removeprefix(prefix): sha256(source.extractfile(item).read()).hexdigest()
                        for path, item in members.items()
                        if path.startswith(prefix + namespace + "/") and path.endswith(".py")}
            package = Path(distribution(name).locate_file(namespace)).resolve()
            actual = {namespace + "/" + path.relative_to(package).as_posix(): sha256(path.read_bytes()).hexdigest()
                      for path in package.rglob("*.py") if "__pycache__" not in path.parts}
            assert actual == expected, name
            result[name] = {"python_files": len(actual), "sha256": sha256(
                json.dumps(actual, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
    return {"source_revision": revision, "packages": result}


def test_installed_code_matches_committed_candidate():
    identity = installed_code_identity()
    assert len(identity["source_revision"]) == 40
    assert all(item["python_files"] > 0 for item in identity["packages"].values())


def test_installed_versions_match_frozen_dependency_graph():
    lock = tomllib.loads((ROOT / "verification/provider/uv.lock").read_text())
    versions = {}
    for package in lock["package"]:
        versions.setdefault(package["name"].replace("_", "-"), set()).add(package["version"])
    for installed in distributions():
        name = installed.metadata["Name"].lower().replace("_", "-")
        assert installed.version in versions.get(name, set()), name


def test_import_provenance_and_license():
    provenance = json.loads((PACKAGE / "provenance.json").read_text())
    archive = ROOT / provenance["artifact"]["retained_path"]
    assert sha256(archive.read_bytes()).hexdigest() == provenance["artifact"]["sha256"]
    assert provenance["api_base"] == "5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0"
    license_bytes = (PACKAGE / "LICENSE").read_bytes()
    assert sha256(license_bytes).hexdigest() == provenance["license"]["sha256"]
    assert b"GNU AFFERO GENERAL PUBLIC LICENSE" in license_bytes
    with tarfile.open(archive) as source:
        for path, digest in provenance["unchanged_files"].items():
            data = (PACKAGE / path).read_bytes()
            assert sha256(data).hexdigest() == digest
            assert data == source.extractfile(f"openbb_fmp-1.6.1/{path}").read()

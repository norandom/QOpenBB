"""Installed FMP discovery, without financial-provider network requests."""

from hashlib import sha256
from importlib.metadata import distribution
import json
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "vendor/data-api/openbb_platform/providers/fmp"


def test_installed_fmp_entry_point_and_core_loader():
    dist = distribution("openbb-fmp")
    entries = [ep for ep in dist.entry_points if ep.group == "openbb_provider_extension"]
    assert [(ep.name, ep.value) for ep in entries] == [("fmp", "openbb_fmp:fmp_provider")]
    from openbb_core.app.extension_loader import ExtensionLoader

    loader = ExtensionLoader()
    provider = loader.provider_objects["fmp"]
    assert provider is entries[0].load()
    assert set(provider.fetcher_dict) == {"EquityInfo", "IncomeStatement"}
    assert provider.credentials == ["fmp_api_key"]
    assert distribution("openbb-core").version == "2.0.1"
    assert distribution("openbb-equity").version == "2.0.0"
    assert distribution("openbb-economy").version == "2.0.0"
    assert distribution("openbb-fred").version == "2.0.0"
    assert dist.version == "1.6.1+qopenbb.1"
    assert {"equity", "economy"} <= {ep.name for ep in loader.core_entry_points}


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

"""Runtime settings, route readiness and secret boundaries."""
import asyncio
import json
import os
import sys
from importlib import metadata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / "services/data-api"))


@pytest.fixture(autouse=True)
def packaged_catalog(monkeypatch):
    import qopenbb_data.app as application
    import qopenbb_data.config as configuration
    monkeypatch.setattr(application, "CATALOG", Path(__file__).parents[2] / "contracts")
    monkeypatch.setattr(configuration, "COVERAGE", Path(__file__).parents[2] /
                        "docs/reference/provider-coverage.json", raising=False)
    for name in ("SOURCE", "GENERATION"):
        variable = f"QOPENBB_DATA_{name}_REVISION"
        monkeypatch.setenv(variable, os.environ.get(variable, "1" * 40))


@pytest.fixture
def runtime(monkeypatch):
    monkeypatch.setenv("FMP_API_KEY", "fixture-runtime-fmp")
    monkeypatch.setenv("FRED_API_KEY", "fixture-runtime-fred")
    monkeypatch.setenv("OPENBB_API_AUTH", "false")
    from qopenbb_data.app import create_app
    return create_app()


async def get(app, path, query=b"", method="GET", raw=False):
    messages = []
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    async def send(message):
        messages.append(message)
    await app({"type": "http", "asgi": {"version": "3.0", "spec_version": "2.4"},
               "http_version": "1.1", "method": method, "scheme": "http",
               "path": path, "raw_path": path.encode(), "root_path": "",
               "query_string": query, "headers": [],
               "client": ("127.0.0.1", 1234), "server": ("test", 80)}, receive, send)
    status = next(m["status"] for m in messages if m["type"] == "http.response.start")
    text = b"".join(m.get("body", b"") for m in messages).decode()
    return status, text.encode() if raw else json.loads(text)


@pytest.mark.parametrize("name", ["widgets.json", "apps.json"])
def test_catalog_composition_is_served_without_provider_calls(runtime, monkeypatch, name):
    contracts = Path(__file__).parents[2] / "contracts"
    canonical = json.loads((contracts / name).read_text())
    gallery = json.loads((contracts / "gallery/catalog.json").read_text())[name.removesuffix(".json")]
    expected = {**canonical, **gallery} if name == "widgets.json" else canonical + gallery
    async def forbidden(*args, **kwargs):
        raise AssertionError("catalog discovery must not call a provider")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    status, body = asyncio.run(get(runtime, "/" + name))
    assert status == 200
    assert body == expected


@pytest.mark.parametrize("name", ["widgets.json", "apps.json"])
def test_catalog_routes_are_read_only(runtime, name):
    status, body = asyncio.run(get(runtime, "/" + name, method="POST"))
    assert status in {404, 405}
    assert body == {"detail": "Not Found"} or body == {"detail": "Method Not Allowed"}


def test_data_only_runtime_advertises_no_agents(runtime, monkeypatch):
    async def forbidden(*args, **kwargs):
        raise AssertionError("agent discovery must not call a provider")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    assert asyncio.run(get(runtime, "/agents.json")) == (200, [])
    assert "/agents.json" not in runtime.openapi()["paths"]


def test_routes_credentials_and_no_quota_readiness(runtime, monkeypatch):
    from openbb_core.app.service.user_service import UserService
    settings = UserService.read_from_file()
    assert settings.credentials.fmp_api_key.get_secret_value() == "fixture-runtime-fmp"
    assert settings.credentials.fred_api_key.get_secret_value() == "fixture-runtime-fred"
    async def forbidden(*args, **kwargs):
        raise AssertionError("health must not call a provider")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    for path in ("/healthz", "/readyz"):
        status, body = asyncio.run(get(runtime, path))
        assert status == 200 and body["status"] in ("ok", "ready")
    schema = runtime.openapi()
    for path in ("/api/v1/equity/profile", "/api/v1/equity/fundamental/income", "/api/v1/economy/fred_series"):
        assert "get" in schema["paths"][path]
    assert "fixture-runtime" not in json.dumps(schema)
    assert metadata.version("openbb-core") == "2.0.1"
    assert metadata.version("openbb-fmp") == "1.6.1+qopenbb.1"


def test_missing_configuration_is_unready(monkeypatch):
    from qopenbb_data.app import create_app
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    monkeypatch.delenv("FMP_API_KEY", raising=False)
    monkeypatch.setenv("OPENBB_API_AUTH", "false")
    app = create_app()
    status, body = asyncio.run(get(app, "/readyz"))
    assert status == 503
    assert body["missing"] == ["FMP_API_KEY", "FRED_API_KEY"]
    assert asyncio.run(get(app, "/healthz"))[0] == 200


def test_basic_auth_is_rejected(monkeypatch):
    from qopenbb_data.app import create_app
    monkeypatch.setenv("OPENBB_API_AUTH", "true")
    with pytest.raises(ValueError, match="OPENBB_API_AUTH"):
        create_app()

def test_no_disk_cache_or_credential_file(runtime, monkeypatch):
    import os

    from openbb_core.app.service.user_service import UserService
    from openbb_fred.utils.cache import enabled
    assert os.environ["OPENBB_FRED_DISK_CACHE"] == "0"
    assert not enabled()
    def forbidden(*args, **kwargs):
        raise AssertionError("runtime must never persist credentials")
    monkeypatch.setattr(UserService, "write_to_file", forbidden)
    from qopenbb_data.app import create_app
    assert asyncio.run(get(create_app(), "/readyz"))[0] == 200

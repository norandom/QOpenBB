"""The owned news package exposes company news without global/RSS composition."""
import ast
import importlib.metadata as metadata
import json
import tomllib
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import url2pathname

ROOT = Path(__file__).resolve().parents[2]
NEWS = ROOT / "vendor/data-api/openbb_platform/extensions/news"


def test_news_entry_point_composes_company_only():
    source = (NEWS / "openbb_news/__init__.py").read_text()
    tree = ast.parse(source)
    commands = [node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
    assert [node.name for node in commands] == ["company"]
    assert 'model="CompanyNews"' in source
    assert "openbb_news.rss" not in source
    assert "openbb_news.news_router" not in source
    manifest = tomllib.loads((NEWS / "pyproject.toml").read_text())
    assert manifest["project"]["entry-points"]["openbb_core_extension"]["news"] == "openbb_news:router"


def test_news_is_owned_locked_dependency_in_runtime_and_verification():
    for project in ("services/data-api", "verification/provider"):
        path = ROOT / project
        manifest = tomllib.loads((path / "pyproject.toml").read_text())
        assert "openbb-news==2.0.0" in manifest["project"]["dependencies"]
        assert manifest["tool"]["uv"]["sources"]["openbb-news"]["path"] == "../../vendor/data-api/openbb_platform/extensions/news"
        lock = tomllib.loads((path / "uv.lock").read_text())
        news = next(p for p in lock["package"] if p["name"] == "openbb-news")
        assert news["version"] == "2.0.0"
        assert news["source"] == {"directory": "../../vendor/data-api/openbb_platform/extensions/news"}


def test_installed_news_entry_point_and_origin():
    dist = metadata.distribution("openbb-news")
    assert dist.version == "2.0.0"
    entry, = [ep for ep in dist.entry_points if ep.group == "openbb_core_extension"]
    assert (entry.name, entry.value) == ("news", "openbb_news:router")
    origin = json.loads(dist.read_text("direct_url.json"))
    assert Path(url2pathname(urlsplit(origin["url"]).path)).resolve() == NEWS.resolve()
    assert entry.load() is __import__("openbb_news").router
    package = Path(dist.locate_file("openbb_news"))
    for source in (NEWS / "openbb_news").rglob("*.py"):
        assert (package / source.relative_to(NEWS / "openbb_news")).read_text() == source.read_text()


def test_isolated_fixture_registry_discovers_company_without_world_or_rss(tmp_path):
    import subprocess
    import sys

    script = tmp_path / "fixture_registry.py"
    script.write_text('''from openbb_core.app.extension_loader import ExtensionLoader
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.company_news import CompanyNewsQueryParams, CompanyNewsData
class FixtureQuery(CompanyNewsQueryParams):
    pass
class FixtureData(CompanyNewsData):
    pass
class FixtureFetcher(Fetcher[FixtureQuery, list[FixtureData]]):
    @staticmethod
    def transform_query(params):
        return FixtureQuery(**params)
    @staticmethod
    async def aextract_data(query, credentials, **kwargs):
        raise AssertionError("Fixture registration must never acquire data")
    @staticmethod
    def transform_data(query, data, **kwargs):
        return data
provider = ExtensionLoader().provider_objects["fmp"]
assert len(provider.fetcher_dict) == 21
provider.fetcher_dict = {**provider.fetcher_dict, "CompanyNews": FixtureFetcher}
from openbb_core.api.rest_api import app
from openbb_core.app.route_iter import iter_api_routes
routes = {r.path: (r.openapi_extra or {}).get("model") for r in iter_api_routes(app)}
assert routes["/api/v1/news/company"] == "CompanyNews"
assert not any("/news/world" in p or "/news/rss" in p for p in routes)
import sys
assert "openbb_news.rss" not in sys.modules
assert "openbb_news.news_router" not in sys.modules
print("isolated fixture company route discovered; no acquisition")
''')
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr



def test_all_existing_fmp_native_routes_remain_registered():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from test_discovery import FMP_MODELS

    models = [(r.openapi_extra or {}).get("model") for r in iter_api_routes(app)]
    assert {model for model in models if model in FMP_MODELS} == FMP_MODELS
    assert all(models.count(model) == 1 for model in FMP_MODELS)
    assert not any("/news/world" in r.path or "/news/rss" in r.path for r in iter_api_routes(app))

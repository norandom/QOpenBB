"""Factory for the internal data process behind the owner-managed origin."""
from copy import copy
from datetime import UTC, datetime
from hashlib import sha256
from inspect import getfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from qopenbb_data.config import configure, coverage_index, financial_identity
from qopenbb_data.gallery import load_gallery

CATALOG = Path(__file__).with_name("catalog")

REQUIRED_ROUTES = (
    "/api/v1/equity/profile",
    "/api/v1/equity/fundamental/income",
    "/api/v1/economy/fred_series",
)


def _annotated_models(registry) -> set[str]:
    from openbb_core.provider.standard_models.financial_annotations import (
        DATA_ANNOTATION_ATTRIBUTE,
        QUERY_ANNOTATION_ATTRIBUTE,
    )

    # Partial declarations must reach the authoritative projection and fail there;
    # unannotated legacy FRED models keep their existing native behavior.
    return {dataset for dataset, variants in registry.original_models.items()
            if any(getattr(models[kind], attribute, None) is not None
                   for models in variants.values() for kind, attribute in (
                       ("query", QUERY_ANNOTATION_ATTRIBUTE), ("data", DATA_ANNOTATION_ATTRIBUTE)))}


def _source_hashes(registry, required: set[str]) -> dict:
    from openbb_core.app.extension_loader import ExtensionLoader

    providers = ExtensionLoader().provider_objects
    return {dataset: {provider: sha256(Path(getfile(
        providers[provider].fetcher_dict[dataset])).read_bytes()).hexdigest()
        for provider in registry.original_models[dataset]} for dataset in sorted(required)}


def _financial_runtime(template):
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap

    from qopenbb_data.financial_catalog import build_financial_catalog
    from qopenbb_data.financial_errors import install_financial_error_handlers
    from qopenbb_data.financial_openapi import (
        financial_error_responses,
        project_financial_openapi,
    )

    registry = RegistryMap()
    required = _annotated_models(registry)
    document = project_financial_openapi(template.openapi(), iter_api_routes(template),
                                        registry, required_models=required)
    document = financial_error_responses(document)
    # The upstream template is process-global and may already have served requests.
    # Isolate its mutable ASGI shell while retaining native routes and middleware.
    native = copy(template)
    native.router = copy(template.router)
    native.router.routes = list(template.router.routes)
    native.exception_handlers = dict(template.exception_handlers)
    native.user_middleware = list(template.user_middleware)
    native.middleware_stack = None
    native.openapi_schema = document
    native.openapi = lambda: document
    install_financial_error_handlers(native, document)
    identity = financial_identity()
    runtime_hash = identity.pop("runtime_inputs_sha256")
    discovery = build_financial_catalog(
        document, coverage_index(), **identity, generated_at=datetime.now(UTC).isoformat(),
        source_hashes=_source_hashes(registry, required))
    discovery["identity"]["runtime_inputs_sha256"] = runtime_hash
    return native, document, discovery


def create_app() -> FastAPI:
    gallery = load_gallery(CATALOG)
    missing = configure()
    from openbb_core.api.rest_api import app as upstream

    from qopenbb_data.financial_policy import FinancialProviderPolicy

    native, document, discovery = _financial_runtime(upstream)
    app = FastAPI(title="QOpenBB data runtime", docs_url=None, redoc_url=None)
    app.add_middleware(FinancialProviderPolicy, document=document)

    @app.get("/healthz", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz", include_in_schema=False)
    async def ready() -> JSONResponse:
        paths = document["paths"]
        required = set(REQUIRED_ROUTES) | {item["command"]["path"] for item in discovery["datasets"]}
        absent = sorted(path for path in required if path not in paths)
        failed = bool(missing or absent)
        return JSONResponse(status_code=503 if failed else 200, content={
            "status": "unready" if failed else "ready",
            "missing": missing, "missing_routes": absent,
        })

    @app.get("/widgets.json", include_in_schema=False)
    async def widgets() -> dict:
        return gallery.widgets()

    @app.get("/apps.json", include_in_schema=False)
    async def apps() -> list:
        return gallery.apps()

    @app.get("/datasets.json", include_in_schema=False)
    async def datasets() -> dict:
        return discovery

    @app.get("/gallery/data/{dataset_id}", include_in_schema=False)
    async def gallery_data(dataset_id: str):
        try:
            return gallery.dataset(dataset_id)
        except KeyError:
            return JSONResponse(status_code=404, content={"detail": "Not Found"})

    @app.get("/agents.json", include_in_schema=False)
    async def agents() -> list[dict[str, object]]:
        return []

    app.mount("/", native)
    app.openapi = native.openapi
    return app

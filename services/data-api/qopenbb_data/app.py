"""Factory for the internal data process behind the owner-managed origin."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from qopenbb_data.config import configure
from qopenbb_data.gallery import load_gallery

CATALOG = Path(__file__).with_name("catalog")

REQUIRED_ROUTES = (
    "/api/v1/equity/profile",
    "/api/v1/equity/fundamental/income",
    "/api/v1/economy/fred_series",
)


def create_app() -> FastAPI:
    gallery = load_gallery(CATALOG)
    missing = configure()
    from openbb_core.api.rest_api import app as upstream

    app = FastAPI(title="QOpenBB data runtime", docs_url=None, redoc_url=None)

    @app.get("/healthz", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz", include_in_schema=False)
    async def ready() -> JSONResponse:
        paths = upstream.openapi()["paths"]
        absent = [path for path in REQUIRED_ROUTES if path not in paths]
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

    @app.get("/gallery/data/{dataset_id}", include_in_schema=False)
    async def gallery_data(dataset_id: str):
        try:
            return gallery.dataset(dataset_id)
        except KeyError:
            return JSONResponse(status_code=404, content={"detail": "Not Found"})

    @app.get("/agents.json", include_in_schema=False)
    async def agents() -> list[dict[str, object]]:
        return []

    app.mount("/", upstream)
    app.openapi = upstream.openapi
    return app

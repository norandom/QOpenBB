"""Factory for the internal data process behind the owner-managed origin."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from qopenbb_data.config import configure

CATALOG = Path(__file__).with_name("catalog")

REQUIRED_ROUTES = (
    "/api/v1/equity/profile",
    "/api/v1/equity/fundamental/income",
    "/api/v1/economy/fred_series",
)


def create_app() -> FastAPI:
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
    async def widgets() -> FileResponse:
        return FileResponse(CATALOG / "widgets.json", media_type="application/json")

    @app.get("/apps.json", include_in_schema=False)
    async def apps() -> FileResponse:
        return FileResponse(CATALOG / "apps.json", media_type="application/json")

    app.mount("/", upstream)
    app.openapi = upstream.openapi
    return app

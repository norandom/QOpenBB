"""Internal ASGI entry point packaged in the analytics runtime."""

import os

from fastapi import FastAPI

from ..models.registry import ModelRegistry
from .acquisition import DataApiSnapshotSource
from .http import create_model_app
from .identity import IdentityVerifier
from .orchestrator import Orchestrator
from .run_store import FileRunStore


def create_app() -> FastAPI:
    """Serve installed methods on a listener reserved for the Workspace bridge."""
    registry = ModelRegistry()
    store = FileRunStore(os.environ.get("QOPENBB_MODEL_RUN_DIR", "./data/modeling"))
    source = DataApiSnapshotSource(os.environ.get("QOPENBB_MODEL_DATA_ORIGIN", "http://data-api:6900"))
    service = Orchestrator(registry, {}, store, snapshot_source=source)
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    app.mount("/modeling/v1", create_model_app(service, registry, IdentityVerifier.from_env()))
    return app

"""Internal ASGI entry point packaged in the analytics runtime."""

import os

from fastapi import FastAPI

from ..models.protocol import Model
from ..models.registry import ModelRegistry
from .acquisition import DataApiSnapshotSource
from .http import create_model_app
from .identity import IdentityVerifier
from .orchestrator import MethodBinding, Orchestrator
from .run_store import FileRunStore

_INSTALLED_METHODS: tuple[tuple[Model, MethodBinding], ...] = ()


def installed_methods() -> tuple[ModelRegistry, dict[tuple[str, str], MethodBinding]]:
    """Use one registration list for execution, discovery and contract export."""
    registry = ModelRegistry(model for model, _ in _INSTALLED_METHODS)
    bindings = {}
    for model, binding in _INSTALLED_METHODS:
        descriptor = model.describe()
        bindings[descriptor.model_id, descriptor.method_version] = binding
    return registry, bindings


def create_app() -> FastAPI:
    """Serve installed methods on a listener reserved for the Workspace bridge."""
    registry, bindings = installed_methods()
    store = FileRunStore(os.environ.get("QOPENBB_MODEL_RUN_DIR", "./data/modeling"))
    source = DataApiSnapshotSource(
        os.environ.get("QOPENBB_MODEL_DATA_ORIGIN", "http://data-api:6900")
    )
    service = Orchestrator(registry, bindings, store, snapshot_source=source)
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    app.mount(
        "/modeling/v1", create_model_app(service, registry, IdentityVerifier.from_env())
    )
    return app

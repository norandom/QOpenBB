"""Explicit registry of installed supplied-input model methods."""

from collections.abc import Iterable

from ..contracts.descriptors import ModelDescriptor
from .protocol import Model


class ModelRegistry:
    def __init__(self, models: Iterable[Model] = ()) -> None:
        self._models: dict[tuple[str, str], Model] = {}
        for model in models:
            self.register(model)

    def register(self, model: Model) -> None:
        # Revalidate even typed descriptors because Pydantic permits unchecked copies.
        descriptor = ModelDescriptor.model_validate(model.describe())
        key = (descriptor.model_id, descriptor.method_version)
        if key in self._models:
            raise ValueError(f"model {key[0]!r} version {key[1]!r} is already installed")
        self._models[key] = model

    def resolve(self, model_id: str, method_version: str) -> Model:
        try:
            return self._models[model_id, method_version]
        except KeyError:
            raise LookupError(f"model {model_id!r} version {method_version!r} is not installed") from None

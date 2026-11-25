"""Service contracts for authenticated model-run persistence."""

from threading import Event
from typing import Protocol

from ..contracts import EvaluationCutoff, InputSnapshot, ModelRun
from ..contracts.common import Contract, Description, Identifier


class Principal(Contract):
    """Exact authenticated subject supplied by the service identity boundary."""

    subject: Identifier


class RunStore(Protocol):
    """Append complete runs and retrieve them under their authenticated owner."""

    def save(self, run: ModelRun, principal: Principal) -> str:
        """Assign a fresh run ID and commit a run owned by the principal.

        A post-publication failure raises RunPublishedError with the original
        run_id. Use get with that ID and principal to recover before retrying.
        """
        ...

    def get(self, run_id: str, principal: Principal) -> ModelRun:
        """Load a saved run scoped to the exact principal."""
        ...


class AcquisitionRequest(Contract):
    """Select a configured dataset and its observation cutoff."""

    dataset_id: Identifier
    parameters: tuple[tuple[Identifier, Description], ...] = ()
    cutoff: EvaluationCutoff


class SnapshotSource(Protocol):
    """Acquire service-owned snapshot evidence for a dataset request."""

    def acquire(
        self, request: AcquisitionRequest, *, deadline: float | None = None, cancel: Event | None = None,
    ) -> InputSnapshot:
        """Retrieve and map data within the absolute monotonic evaluation deadline."""
        ...

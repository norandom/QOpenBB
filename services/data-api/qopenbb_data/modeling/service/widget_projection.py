"""Read-only widget representation of an authorized saved model output."""

from decimal import Decimal
from urllib.parse import quote

from ..contracts import ModelRun
from ..contracts.common import Scalar
from .run_store import RunNotFound


def _display_number(value: Scalar | None) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        return None
    number = float(value)
    # Conversion back to Decimal exposes binary64 rounding without applying
    # the active Decimal context. Only lossless values enter the numeric field.
    return number if Decimal.from_float(number) == value else None


def _display_text(value: str | int | bool | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def project_output(
    run: ModelRun, output_id: str, *, expected_run_id: str | None = None
) -> dict:
    """Project saved evidence after the caller has authorized access to the run."""
    output = next((item for item in run.outputs if item.output_id == output_id), None)
    if output is None:
        raise RunNotFound()
    freshness = "saved"
    if expected_run_id is not None:
        freshness = "matched" if expected_run_id == run.run_id else "stale"
    checks = [check for check in run.checks if check.rule_id in output.check_ids]
    check_explanations = "\n".join(
        f"{check.rule_id}: {check.explanation}"
        for check in checks
        if check.explanation is not None
    )
    run_detail_href = f"runs/{quote(run.run_id, safe='')}"
    result = output.model_dump(mode="json")
    result.update(
        display_value=_display_number(output.value),
        display_text=_display_text(result["value"]),
        freshness=freshness,
        run_detail_href=run_detail_href,
        check_explanations=check_explanations or None,
        display_numeric={"transform": "exact_binary64", "max_absolute_error": "0"},
    )
    return {
        "run_id": run.run_id,
        "results": [result],
        "checks": [check.model_dump(mode="json") for check in checks],
        "trace": [
            entry.model_dump(mode="json")
            for entry in run.trace
            if entry.trace_id in output.trace_ids
        ],
        "verification": [
            entry.model_dump(mode="json")
            for entry in run.verification
            if entry.output_id == output_id
        ],
        "run_detail_href": run_detail_href,
        "exceptions": [
            item.model_dump(mode="json")
            for item in run.exceptions
            if item.exception_id in output.exception_ids
        ],
    }

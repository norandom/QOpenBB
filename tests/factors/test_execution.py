import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path
from time import monotonic, sleep
from typing import ClassVar

import pytest
from qopenbb_data.modeling.contracts.inputs import Assumption, AssumptionSet
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.models.registry import ModelRegistry
from qopenbb_data.modeling.service import execution
from qopenbb_data.modeling.service.execution import (
    ExecutionError,
    ExecutionLimits,
    ModelExecutor,
)
from qopenbb_data.modeling.service.execution_decimal import require_exact_decimal
from qopenbb_data.modeling.service.execution_transport import InputWriter
from test_model_registry import SuppliedValueFixture
from test_model_registry import inputs as shared_snapshot_fixture

supplied_inputs = shared_snapshot_fixture


class OfflinePolarsModel(SuppliedValueFixture):
    """Test-only selection of an exact nullable decimal from supplied observations."""

    def __init__(self, started=None, helper_output=None):
        super().__init__()
        self.started = started
        self.helper_output = helper_output

    def calculate(self, inputs, assumptions):
        import polars as pl

        assert pl.thread_pool_size() == 2
        assert os.getpid() != self.parent_pid
        should_block = (
            self.started is not None and inputs.tables[0].rows[0].value is not None
        )
        if self.helper_output is not None and (self.started is None or should_block):
            subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    (
                        "import sys, time; from pathlib import Path; "
                        "time.sleep(2); Path(sys.argv[1]).touch()"
                    ),
                    str(self.helper_output),
                ]
            )
        if should_block:
            marker = self.started.with_suffix(".pending")
            marker.write_text(str(os.getpid()))
            marker.replace(self.started)
            while True:
                # Keep executing native Polars work until the service stops this child.
                pl.int_range(0, 10_000, eager=True).sum()
        values = [row.value for row in inputs.tables[0].rows]
        for value in values:
            if value is not None:
                require_exact_decimal(value, precision=18, scale=4)
        observations = pl.LazyFrame(
            {"amount": values}, schema={"amount": pl.Decimal(precision=18, scale=4)}
        ).select(pl.col("amount").first())
        amount = observations.collect().item()
        return CandidateResult(
            outputs=(CandidateOutput(output_id="value", value=amount),)
        )


def measure_test_dimensions(inputs, assumptions):
    dimensions = {
        assumption.assumption_id: assumption.value
        for assumption in assumptions.assumptions
    }
    return dimensions.get("horizon", 1), dimensions.get("scenarios", 1)


class SlowSizing:
    def __init__(self, marker):
        self.marker = marker

    def __call__(self, inputs, assumptions):
        horizon, scenarios = measure_test_dimensions(inputs, assumptions)
        if horizon == 3:
            marker = self.marker.with_suffix(".pending")
            marker.write_text(str(os.getpid()))
            marker.replace(self.marker)
            sleep(3)
        return horizon, scenarios


def declared_limits(max_rows, max_horizon, max_scenarios, timeout_seconds=None):
    return ExecutionLimits(
        max_rows,
        max_horizon,
        max_scenarios,
        timeout_seconds,
        measure_dimensions=measure_test_dimensions,
    )


def supplied_dimension(name, value):
    return Assumption(
        assumption_id=name,
        value_type="boolean" if type(value) is bool else "integer",
        value=value,
        origin="method_default",
        rationale="Synthetic execution dimension",
    )


@pytest.fixture
def setup_executor(monkeypatch):
    helper_path = str(Path(__file__).resolve().parent)
    child_paths = [helper_path]
    if python_path := os.environ.get("PYTHONPATH"):
        child_paths.append(python_path)
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(child_paths))

    def setup(
        *, started=None, timeout_seconds=10, method_limits=None, helper_output=None
    ):
        method = OfflinePolarsModel(started, helper_output)
        method.parent_pid = os.getpid()
        return ModelExecutor(
            ModelRegistry((method,)),
            {
                ("test-only-supplied-value", "1"): method_limits
                or declared_limits(2, 3, 1)
            },
            polars_threads=2,
            timeout_seconds=timeout_seconds,
        )

    return setup


def evaluate(executor, inputs, *, horizon=3, scenarios=1, cancel=None, version="1"):
    return executor.evaluate(
        "test-only-supplied-value",
        version,
        inputs,
        AssumptionSet(
            version="1",
            effective_date=inputs.tables[0].rows[0].observation_date,
            assumptions=(
                supplied_dimension("horizon", horizon),
                supplied_dimension("scenarios", scenarios),
            ),
        ),
        cancel=cancel,
    )


def test_spawned_polars_uses_child_budget_and_preserves_decimal(
    supplied_inputs, setup_executor, monkeypatch
):
    monkeypatch.setenv("POLARS_MAX_THREADS", "7")
    outcome = evaluate(setup_executor(), supplied_inputs)
    assert outcome.outputs[0].value == Decimal("12345678901234.0025")
    missing_first = supplied_inputs.tables[0].model_copy(
        update={"rows": supplied_inputs.tables[0].rows[::-1]}
    )
    assert (
        evaluate(
            setup_executor(),
            supplied_inputs.model_copy(update={"tables": (missing_first,)}),
        )
        .outputs[0]
        .value
        is None
    )
    assert os.environ["POLARS_MAX_THREADS"] == "7"


@pytest.mark.parametrize(
    ("limits", "horizon", "scenarios", "code"),
    [
        (declared_limits(1, 3, 1), 3, 1, "row_limit"),
        (declared_limits(2, 3, 1), 4, 1, "horizon_limit"),
        (declared_limits(2, 3, 1), 0, 1, "horizon_limit"),
        (declared_limits(2, 3, 1), 3, 2, "scenario_limit"),
        (declared_limits(2, 3, 1), 3, True, "scenario_limit"),
    ],
)
def test_limits_reject_before_calculation(
    supplied_inputs, setup_executor, tmp_path, limits, horizon, scenarios, code
):
    started = tmp_path / "calculation-started"
    executor = setup_executor(started=started, method_limits=limits)
    with pytest.raises(ExecutionError) as error:
        evaluate(executor, supplied_inputs, horizon=horizon, scenarios=scenarios)
    assert error.value.code == code
    assert not started.exists()


def test_unknown_version_rejected(supplied_inputs, setup_executor):
    with pytest.raises(LookupError):
        evaluate(setup_executor(), supplied_inputs, version="latest")


@pytest.mark.parametrize("value", ["12345678901234.00251", "123456789012345"])
def test_decimal_conversion_rejects_scale_loss_and_overflow(
    supplied_inputs, setup_executor, value
):
    table = supplied_inputs.tables[0]
    changed = table.rows[0].model_copy(update={"value": Decimal(value)})
    snapshot = supplied_inputs.model_copy(
        update={
            "tables": (table.model_copy(update={"rows": (changed, table.rows[1])}),)
        }
    )
    with pytest.raises(ExecutionError) as error:
        evaluate(setup_executor(), snapshot)
    assert error.value.code == "unsupported_numeric_conversion"


def test_timeout_reaps_child_and_releases_capacity(
    supplied_inputs, setup_executor, tmp_path
):
    started = tmp_path / "started"
    executor = setup_executor(
        started=started, timeout_seconds=10, method_limits=declared_limits(2, 3, 1, 2)
    )
    with pytest.raises(ExecutionError) as error:
        evaluate(executor, supplied_inputs)
    assert error.value.code == "timeout"
    with pytest.raises(ProcessLookupError):
        os.kill(int(started.read_text()), 0)
    cancelled = threading.Event()
    cancelled.set()
    with pytest.raises(ExecutionError) as error:
        evaluate(executor, supplied_inputs, cancel=cancelled)
    assert error.value.code == "cancelled"


def test_running_child_rejects_extra_request_and_is_reaped_on_cancel(
    supplied_inputs, setup_executor, tmp_path
):
    started = tmp_path / "started"
    cancel = threading.Event()
    helper_output = tmp_path / "helper-finished"
    executor = setup_executor(
        started=started, helper_output=helper_output if os.name == "posix" else None
    )
    with ThreadPoolExecutor(max_workers=1) as callers:
        running = callers.submit(evaluate, executor, supplied_inputs, cancel=cancel)
        try:
            deadline = monotonic() + 5
            while (
                not started.exists() and not running.done() and monotonic() < deadline
            ):
                sleep(0.01)
            assert started.exists()
            with pytest.raises(ExecutionError) as error:
                evaluate(executor, supplied_inputs)
            assert error.value.code == "capacity"
        finally:
            cancel.set()
        with pytest.raises(ExecutionError) as error:
            running.result(timeout=5)
        assert error.value.code == "cancelled"
    with pytest.raises(ProcessLookupError):
        os.kill(int(started.read_text()), 0)

    table = supplied_inputs.tables[0]
    retry = supplied_inputs.model_copy(
        update={"tables": (table.model_copy(update={"rows": table.rows[::-1]}),)}
    )
    assert evaluate(executor, retry).outputs[0].value is None

    if os.name == "posix":
        deadline = monotonic() + 2.5
        while not helper_output.exists() and monotonic() < deadline:
            sleep(0.02)
        assert not helper_output.exists(), "helper continued after cancellation"


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX process groups")
def test_successful_worker_stops_its_helper(supplied_inputs, setup_executor, tmp_path):
    helper_output = tmp_path / "helper-finished"
    executor = setup_executor(helper_output=helper_output)
    assert evaluate(executor, supplied_inputs).outputs[0].value == Decimal(
        "12345678901234.0025"
    )
    deadline = monotonic() + 2.5
    while not helper_output.exists() and monotonic() < deadline:
        sleep(0.02)
    assert not helper_output.exists(), "helper continued after successful worker exit"


@pytest.mark.parametrize(
    ("change", "code"),
    [
        ("schema_id", "input_schema_mismatch"),
        ("schema_version", "input_schema_mismatch"),
        ("unchecked_row", "invalid_input_snapshot"),
        ("unchecked_assumption", "invalid_assumptions"),
    ],
)
def test_executor_validates_supplied_contracts_before_calculation(
    supplied_inputs, setup_executor, change, code
):
    setup_executor()
    method = SuppliedValueFixture()
    snapshot = supplied_inputs
    assumptions = AssumptionSet(
        version="1", effective_date=snapshot.tables[0].rows[0].observation_date
    )
    # This fixture reads the first value and ignores metadata and assumptions.
    if change == "schema_id":
        snapshot = snapshot.model_copy(update={"schema_id": "other-observations"})
    elif change == "schema_version":
        method.descriptor = method.descriptor.model_copy(
            update={"input_schema_version": "2"}
        )
    elif change == "unchecked_row":
        table = snapshot.tables[0]
        bad_row = table.rows[1].model_copy(update={"category": "unknown"})
        snapshot = snapshot.model_copy(
            update={
                "tables": (table.model_copy(update={"rows": (table.rows[0], bad_row)}),)
            }
        )
    elif change == "unchecked_assumption":
        assumptions = assumptions.model_copy(update={"effective_date": "invalid"})
    executor = ModelExecutor(
        ModelRegistry((method,)),
        {("test-only-supplied-value", "1"): declared_limits(2, 3, 1)},
    )
    with pytest.raises(ExecutionError) as error:
        executor.evaluate(
            "test-only-supplied-value",
            "1",
            snapshot,
            assumptions,
        )
    assert error.value.code == code


@pytest.mark.parametrize("stop_code", ["cancelled", "timeout"])
def test_admission_and_deadline_cover_sizing(
    supplied_inputs, setup_executor, tmp_path, stop_code
):
    sizing_started = tmp_path / "sizing-started"
    calculation_started = tmp_path / "calculation-started"
    limits = ExecutionLimits(2, 3, 1, measure_dimensions=SlowSizing(sizing_started))
    executor = setup_executor(
        started=calculation_started,
        method_limits=limits,
        timeout_seconds=1.8 if stop_code == "timeout" else 10,
    )
    cancel = threading.Event()
    with ThreadPoolExecutor(max_workers=1) as callers:
        running = callers.submit(evaluate, executor, supplied_inputs, cancel=cancel)
        try:
            deadline = monotonic() + 5
            while (
                not sizing_started.exists()
                and not running.done()
                and monotonic() < deadline
            ):
                sleep(0.01)
            assert sizing_started.exists()
            with pytest.raises(ExecutionError, match="^capacity$"):
                evaluate(executor, supplied_inputs.model_copy(update={"schema_id": ""}))
            if stop_code == "cancelled":
                cancel.set()
            with pytest.raises(ExecutionError, match=f"^{stop_code}$"):
                running.result(timeout=2.5)
        finally:
            cancel.set()
    with pytest.raises(ProcessLookupError):
        os.kill(int(sizing_started.read_text()), 0)
    assert not calculation_started.exists()
    table = supplied_inputs.tables[0]
    retry = supplied_inputs.model_copy(
        update={"tables": (table.model_copy(update={"rows": table.rows[::-1]}),)}
    )
    assert evaluate(executor, retry, horizon=1).outputs[0].value is None


class SerializationProbeModel(OfflinePolarsModel):
    serialized_at: ClassVar[list[int]] = []

    def __getstate__(self):
        self.serialized_at.append(os.getpid())
        return vars(self)


class SerializationProbeSizing:
    serialized_at: ClassVar[list[int]] = []

    def __getstate__(self):
        self.serialized_at.append(os.getpid())
        return {}

    def __call__(self, inputs, assumptions):
        return measure_test_dimensions(inputs, assumptions)


def test_configuration_serialization_happens_only_at_construction(
    supplied_inputs, setup_executor
):
    SerializationProbeModel.serialized_at.clear()
    SerializationProbeSizing.serialized_at.clear()
    model = SerializationProbeModel()
    model.parent_pid = os.getpid()
    executor = ModelExecutor(
        ModelRegistry((model,)),
        {
            ("test-only-supplied-value", "1"): ExecutionLimits(
                2, 3, 1, measure_dimensions=SerializationProbeSizing()
            )
        },
        polars_threads=2,
    )
    observed_at_construction = (
        list(model.serialized_at),
        list(SerializationProbeSizing.serialized_at),
    )
    for _ in range(2):
        assert evaluate(executor, supplied_inputs).outputs[0].value is not None
    assert observed_at_construction == ([os.getpid()], [os.getpid()])
    assert (
        model.serialized_at == SerializationProbeSizing.serialized_at == [os.getpid()]
    )


class CallerSerializationProbe:
    invoked = False

    def __reduce__(self):
        type(self).invoked = True
        return str, ("test-observations",)


def test_unchecked_caller_objects_cannot_run_serialization_hooks(
    supplied_inputs, setup_executor
):
    CallerSerializationProbe.invoked = False
    snapshot = supplied_inputs.model_copy(
        update={"schema_id": CallerSerializationProbe()}
    )
    with pytest.raises(ExecutionError, match="^invalid_input_snapshot$"):
        evaluate(setup_executor(), snapshot)
    assert not CallerSerializationProbe.invoked


@pytest.mark.parametrize("stop_code", ["cancelled", "timeout"])
def test_input_transfer_can_stop_and_release_capacity(
    supplied_inputs, setup_executor, monkeypatch, stop_code
):
    executor = setup_executor(timeout_seconds=1.5)
    transfer_started = threading.Event()
    cancel = threading.Event()
    original_write = InputWriter._write

    def slow_write(writer, chunk):
        transfer_started.set()
        sleep(0.02)
        original_write(writer, chunk)

    def unexpected_worker(*args, **kwargs):
        pytest.fail("interrupted transfer launched a worker")

    with monkeypatch.context() as during_transfer:
        during_transfer.setattr(InputWriter, "_write", slow_write)
        during_transfer.setattr(ModelExecutor, "_run_child", unexpected_worker)
        with ThreadPoolExecutor(max_workers=1) as callers:
            running = callers.submit(evaluate, executor, supplied_inputs, cancel=cancel)
            try:
                assert transfer_started.wait(1)
                if stop_code == "cancelled":
                    cancel.set()
                with pytest.raises(ExecutionError, match=f"^{stop_code}$"):
                    running.result(timeout=2.5)
            finally:
                cancel.set()

    assert evaluate(executor, supplied_inputs).outputs[0].value == Decimal(
        "12345678901234.0025"
    )


def test_parent_bounds_response_transfer(supplied_inputs, setup_executor, monkeypatch):
    executor = setup_executor()
    with monkeypatch.context() as limited_parent:
        limited_parent.setattr(execution, "MAX_RESULT_BYTES", 8)
        with pytest.raises(ExecutionError, match="^result_limit$"):
            evaluate(executor, supplied_inputs)
    assert evaluate(executor, supplied_inputs).outputs[0].value is not None

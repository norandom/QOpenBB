from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError
from qopenbb_data.modeling.contracts.descriptors import (
    ModelDescriptor,
    OutputDescriptor,
)
from qopenbb_data.modeling.contracts.inputs import AssumptionSet, InputSnapshot
from qopenbb_data.modeling.models.protocol import (
    CandidateOutput,
    CandidateResult,
    Model,
)
from qopenbb_data.modeling.models.registry import ModelRegistry


class SuppliedValueFixture:
    """Test-only passthrough for an already validated supplied value."""

    def __init__(self, method_version: str = "1") -> None:
        self.descriptor = ModelDescriptor(
            model_id="test-only-supplied-value",
            method_version=method_version,
            input_schema_id="test-observations",
            output_schema_id="test-result",
            rule_set_version="1",
            reference_version="1",
            entity_types=("test-entity",),
            period_types=("date",),
            input_ids=("observations",),
            outputs=(
                OutputDescriptor(
                    output_id="value",
                    semantic_definition="Supplied test observation",
                    unit="amount",
                    required_input_ids=("observations",),
                ),
            ),
        )

    def describe(self) -> ModelDescriptor:
        return self.descriptor

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        return CandidateResult(
            outputs=(CandidateOutput(output_id="value", value=inputs.tables[0].rows[0].value),),
        )


@pytest.fixture
def inputs() -> InputSnapshot:
    day = date(2024, 1, 2)
    return InputSnapshot.model_validate({
        "schema_id": "test-observations",
        "provenance": {
            "origin": "user_supplied", "source": "test-fixture", "query": (),
            "retrieved_at": datetime(2024, 1, 3, tzinfo=UTC),
        },
        "tables": ({
            "table_id": "observations",
            "grain": "one test value per entity and observation date",
            "keys": ("entity_id", "observation_date"),
            "nullable": True,
            "rows": tuple(
                {
                    "record_id": record_id, "entity_id": record_id, "metric_id": "test-value",
                    "observation_date": day, "context": {"unit": "amount", "currency": "USD"},
                    "value": value, "category": "raw",
                }
                for record_id, value in (("present", "12345678901234.0025"), ("missing", None))
            ),
        },),
    })


def test_resolved_method_calculates_offline(inputs: InputSnapshot) -> None:
    installed: Model = SuppliedValueFixture()
    registry = ModelRegistry((installed,))
    model = registry.resolve("test-only-supplied-value", "1")
    assert model is installed
    result = model.calculate(inputs, AssumptionSet(version="1", effective_date=date(2024, 1, 2)))
    assert result.outputs[0].value == Decimal("12345678901234.0025")
    assert result.trace == ()


def test_registry_resolves_exact_installed_versions() -> None:
    first, second = SuppliedValueFixture("1"), SuppliedValueFixture("2")
    registry = ModelRegistry((first, second))
    assert registry.resolve(first.describe().model_id, "1") is first
    assert registry.resolve(second.describe().model_id, "2") is second
    for model_id, version in (
        (first.describe().model_id, "01"),
        (first.describe().model_id, "latest"),
        (first.describe().model_id.upper(), "1"),
        ("unknown", "1"),
    ):
        with pytest.raises(LookupError, match="not installed"):
            registry.resolve(model_id, version)


def test_duplicate_registration_preserves_installed_method() -> None:
    installed = SuppliedValueFixture()
    registry = ModelRegistry((installed,))
    with pytest.raises(ValueError, match="already installed"):
        registry.register(SuppliedValueFixture())
    assert registry.resolve(installed.describe().model_id, "1") is installed


@pytest.mark.parametrize(("dependency", "reference", "message"), [
    ("required_input_ids", "missing", "unknown input dependencies"),
    ("required_check_ids", "missing", "unknown check dependencies"),
    ("required_output_ids", "missing", "unknown output dependencies"),
    ("required_output_ids", "value", "cyclic output dependencies"),
])
def test_registration_revalidates_unchecked_descriptor(
    dependency: str, reference: str, message: str
) -> None:
    method = SuppliedValueFixture()
    output = method.descriptor.outputs[0].model_copy(update={dependency: (reference,)})
    method.descriptor = method.descriptor.model_copy(update={"outputs": (output,)})
    registry = ModelRegistry()
    with pytest.raises(ValidationError, match=message):
        registry.register(method)
    with pytest.raises(LookupError, match="not installed"):
        registry.resolve(method.descriptor.model_id, "1")


def test_registry_accepts_acyclic_output_dependencies() -> None:
    method = SuppliedValueFixture()
    source = method.descriptor.outputs[0]
    derived = source.model_copy(update={"output_id": "downstream", "required_output_ids": ("value",)})
    method.descriptor = method.descriptor.model_copy(update={"outputs": (derived, source)})
    assert ModelRegistry((method,)).resolve(method.descriptor.model_id, "1") is method


def test_registry_rejects_cycle_between_outputs() -> None:
    method = SuppliedValueFixture()
    source = method.descriptor.outputs[0].model_copy(update={"required_output_ids": ("downstream",)})
    derived = source.model_copy(update={"output_id": "downstream", "required_output_ids": ("value",)})
    method.descriptor = method.descriptor.model_copy(update={"outputs": (source, derived)})
    with pytest.raises(ValidationError, match="cyclic output dependencies"):
        ModelRegistry((method,))


def test_candidate_rejects_duplicate_outputs_and_float_decimals() -> None:
    output = CandidateOutput(output_id="value", value=Decimal("1.25"))
    with pytest.raises(ValidationError, match="duplicate candidate output ID"):
        CandidateResult(outputs=(output, output))
    with pytest.raises(ValidationError, match="finite Decimal"):
        CandidateOutput.model_validate({"output_id": "value", "value": 1.25})


def test_polars_materializes_bounded_nullable_decimal_input(inputs: InputSnapshot) -> None:
    pl = pytest.importorskip("polars")

    class PolarsSuppliedValuesFixture(SuppliedValueFixture):
        """Test-only materialization of the two supplied observations."""

        def __init__(self) -> None:
            super().__init__()
            output = self.descriptor.outputs[0]
            self.descriptor = self.descriptor.model_copy(update={
                "model_id": "test-only-polars-supplied-values",
                "outputs": tuple(
                    output.model_copy(update={"output_id": output_id})
                    for output_id in ("present", "missing")
                ),
            })

        def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
            table = inputs.tables[0]
            assert table.nullable and len(table.rows) == 2
            schema = pl.Schema({"record_id": pl.String, "value": pl.Decimal(precision=18, scale=4)})
            plan = pl.LazyFrame(
                [(row.record_id, row.value) for row in table.rows], schema=schema, orient="row"
            ).select("record_id", "value")
            assert plan.collect_schema() == schema
            materialized = plan.limit(2).collect()
            assert materialized.schema == schema
            return CandidateResult(outputs=tuple(
                CandidateOutput(output_id=record_id, value=value)
                for record_id, value in materialized.iter_rows()
            ))

    registry = ModelRegistry((PolarsSuppliedValuesFixture(),))
    model = registry.resolve("test-only-polars-supplied-values", "1")
    result = model.calculate(inputs, AssumptionSet(version="1", effective_date=date(2024, 1, 2)))
    present, missing = result.outputs
    assert present.output_id == "present"
    assert isinstance(present.value, Decimal)
    assert present.value == Decimal("12345678901234.0025")
    assert missing.output_id == "missing"
    assert missing.value is None


def test_discovery_lists_all_exact_versions_in_stable_order():
    registry = ModelRegistry((SuppliedValueFixture("2"), SuppliedValueFixture("1")))
    assert [method.method_version for method in registry.descriptors()] == ["1", "2"]
    assert ModelRegistry().descriptors() == ()

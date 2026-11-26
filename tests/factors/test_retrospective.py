"""Verify the acquired ETF price history separately from historical trading eligibility."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, build_run, text_assumption
from qopenbb_data.modeling.models.factors.comparison import ProxyComparisonModel
from qopenbb_data.modeling.models.factors.retrospective import (
    RetrospectiveComparisonModel,
)
from qopenbb_data.modeling.verification.factors.etf import comparison_reference
from qopenbb_data.modeling.verification.factors.retrospective_reference import (
    retrospective_reference,
)


@pytest.fixture
def history():
    fixture = build_run(EXAMPLES["proxy_comparison"], missing=False)
    calendar = "NYSE_ARCA"
    symbols = {"fixture_left": "DBC", "fixture_right": "XLK"}
    assumptions = fixture.assumptions.model_copy(
        update={
            "assumptions": (
                *(
                    item.model_copy(update={"value": symbols.get(item.value, item.value)})
                    for item in fixture.assumptions.assumptions
                ),
                *(
                    text_assumption(key, calendar, "Bind the synthetic session calendar")
                    for key in ("calendar_id", "left_calendar", "right_calendar")
                ),
            )
        }
    )
    times = {"left_retrieved_at": "2024-05-06T14:07:00Z", "right_retrieved_at": "2024-05-07T15:01:00Z"}
    query = dict(
        dataset_id="story.etf_pair",
        calendar_id=calendar,
        schedule_revision="fixture_us_listing.2024r1",
        left_proxy="DBC",
        right_proxy="XLK",
        **times,
    )
    provenance = fixture.inputs.provenance.model_copy(
        update={
            "origin": "service_acquired",
            "source": "fmp",
            "acquisition_id": "synthetic_receipt",
            "query": tuple(query.items()),
            "retrieved_at": datetime.fromisoformat(times["right_retrieved_at"]),
        }
    )
    sessions, *prices = fixture.inputs.tables
    tables = [
        sessions.model_copy(
            update={"rows": tuple(row.model_copy(update={"entity_id": calendar}) for row in sessions.rows)}
        )
    ]
    for table in prices:
        rows = tuple(
            row.model_copy(
                update={
                    "entity_id": symbols[row.entity_id],
                    "source_record_id": row.record_id,
                    "category": "provider",
                    "published_at": None,
                    "vintage_at": None,
                    "context": row.context.model_copy(update={"vintage_coverage": "unknown"}),
                }
            )
            for row in table.rows
        )
        tables.append(table.model_copy(update={"rows": rows}))
    return fixture.inputs.model_copy(update={"provenance": provenance, "tables": tuple(tables)}), assumptions


def test_retrieved_history_is_exact_and_historical_eligibility_remains_strict(history):
    inputs, assumptions = history
    reference = retrospective_reference()
    result = RetrospectiveComparisonModel().calculate(inputs, assumptions)
    assert [item.value for item in result.outputs] == list(map(Decimal, (20, 10, 10, 40, 20, 20)))
    for item, trace in zip(result.outputs, result.trace, strict=True):
        assert reference.calculations[item.output_id](inputs, assumptions) == item.value
        assert trace.formula_version == "2"
        assert all(
            "Retrospective FMP history retrieved at" in step.description for step in trace.transformations
        )
        assert comparison_reference().calculations[item.output_id](inputs, assumptions) is None
    assert all(item.value is None for item in ProxyComparisonModel().calculate(inputs, assumptions).outputs)


@pytest.mark.parametrize(
    "change",
    [
        "user_supplied",
        "wrong_dataset",
        "wrong_source",
        "wrong_proxy",
        "missing_receipt",
        "invalid_latest",
        "future_receipt",
        "early_receipt",
    ],
)
def test_receipt_eligibility(history, change):
    inputs, assumptions = history
    provenance = inputs.provenance
    query = dict(provenance.query)
    updates = {}
    if change == "user_supplied":
        updates.update(origin="user_supplied", acquisition_id=None)
    elif change == "wrong_dataset":
        query["dataset_id"] = "story.other"
    elif change == "wrong_source":
        updates["source"] = "fred"
    elif change == "wrong_proxy":
        query["left_proxy"] = "other"
    elif change == "missing_receipt":
        del query["left_retrieved_at"]
    elif change == "invalid_latest":
        updates["retrieved_at"] = datetime.fromisoformat(query["left_retrieved_at"])
    elif change == "future_receipt":
        updates["retrieved_at"] = datetime.now(UTC) + timedelta(days=30)
        query["left_retrieved_at"] = updates["retrieved_at"].isoformat()
    else:
        query["left_retrieved_at"] = "2024-04-02T13:00:00Z"
    updates["query"] = tuple(query.items())
    inputs = inputs.model_copy(update={"provenance": provenance.model_copy(update=updates)})
    assert all(
        item.value is None for item in RetrospectiveComparisonModel().calculate(inputs, assumptions).outputs
    )
    assert all(fn(inputs, assumptions) is None for fn in retrospective_reference().calculations.values())


@pytest.mark.parametrize(
    "change",
    [
        "future_close",
        "future_vintage",
        "dividend_adjusted",
        "estimate",
        "missing_source",
        "future_schedule",
        "volatility_overflow",
    ],
)
def test_invalid_evidence_withholds_only_affected_outputs(history, change):
    inputs, assumptions = history
    tables = list(inputs.tables)
    index = 0 if change == "future_schedule" else 2
    rows = list(tables[index].rows)
    updates = {
        "future_close": {"observation_date": inputs.cutoff.observation_date + timedelta(days=1)},
        "dividend_adjusted": {"context": rows[-1].context.model_copy(update={"basis": "total_return"})},
        "future_vintage": {"vintage_at": inputs.provenance.retrieved_at + timedelta(days=1)},
        "future_schedule": {"published_at": inputs.cutoff.decision_at + timedelta(days=1)},
        "estimate": {"category": "estimate"},
        "missing_source": {"source_record_id": None},
        "volatility_overflow": {"value": Decimal("1e-38")},
    }[change]
    row_index = 1 if change == "volatility_overflow" else -1
    rows[row_index] = rows[row_index].model_copy(update=updates)
    tables[index] = tables[index].model_copy(update={"rows": tuple(rows)})
    inputs = inputs.model_copy(update={"tables": tuple(tables)})
    result = RetrospectiveComparisonModel().calculate(inputs, assumptions)
    allowed = {"left_momentum", "left_volatility"} if change != "future_schedule" else set()
    if change == "volatility_overflow":
        allowed.update(("right_momentum", "momentum_spread"))
    for item in result.outputs:
        assert (item.value is not None) == (item.output_id in allowed)
        assert retrospective_reference().calculations[item.output_id](inputs, assumptions) == item.value


@pytest.mark.parametrize("reason", ["missing_data", "upstream", "entitlement", "invalid_response"])
def test_failed_transport_preserves_opposite_receipt_and_values(history, reason):
    inputs, assumptions = history
    sessions, left, right = inputs.tables
    query = dict(inputs.provenance.query)
    del query["right_retrieved_at"]
    query["right_error"] = reason
    provenance = inputs.provenance.model_copy(
        update={
            "query": tuple(query.items()),
            "retrieved_at": datetime.fromisoformat(query["left_retrieved_at"]),
        }
    )
    inputs = inputs.model_copy(
        update={
            "provenance": provenance,
            "tables": (
                sessions,
                left,
                right.model_copy(update={"rows": ()}),
            ),
        }
    )
    model = RetrospectiveComparisonModel()
    issues = model.input_issues(inputs, assumptions)
    for item in model.calculate(inputs, assumptions).outputs:
        assert (item.value is not None) == item.output_id.startswith("left_")
        if item.value is None:
            assert reason in issues[item.output_id] and "XLK" in issues[item.output_id]
        assert retrospective_reference().calculations[item.output_id](inputs, assumptions) == item.value


def test_saved_run_replays_exact_original_prices_after_provider_revision(history, tmp_path):
    from qopenbb_data.modeling.service.bootstrap import installed_methods
    from qopenbb_data.modeling.service.evaluation import EvaluationRequest
    from qopenbb_data.modeling.service.orchestrator import Orchestrator
    from qopenbb_data.modeling.service.ports import AcquisitionRequest, Principal
    from qopenbb_data.modeling.service.run_store import FileRunStore

    inputs, assumptions = history

    class AcquiredHistory:
        snapshot = inputs

        def acquire(self, request, *, deadline, cancel):
            return self.snapshot

    registry, bindings = installed_methods()
    provider = AcquiredHistory()
    store = FileRunStore(tmp_path)
    service = Orchestrator(registry, bindings, store, snapshot_source=provider)
    owner = Principal(subject="story_analyst")
    acquisition = AcquisitionRequest(
        dataset_id="story.etf_pair",
        cutoff=inputs.cutoff,
        parameters=tuple(
            (key, value)
            for key, value in inputs.provenance.query
            if key
            in {
                "left_proxy",
                "right_proxy",
                "calendar_id",
                "schedule_revision",
            }
        ),
    )
    request = EvaluationRequest(
        model_id="proxy_comparison", method_version="2", assumptions=assumptions, acquisition=acquisition
    )
    first = service.evaluate(request, owner)
    sessions, left, right = inputs.tables
    revised = left.rows[-1].model_copy(update={"value": Decimal(130)})
    provider.snapshot = inputs.model_copy(
        update={
            "tables": (
                sessions,
                left.model_copy(update={"rows": (*left.rows[:-1], revised)}),
                right,
            )
        }
    )
    second = service.evaluate(request, owner)
    assert second.outputs[0].value == 30 and first.outputs[0].value == 20
    original = FileRunStore(tmp_path).get(first.run_id, owner)
    assert original == first
    verifier = bindings["proxy_comparison", "2"].reference
    for item in original.outputs:
        assert item.status == "verified"
        assert verifier.calculations[item.output_id](original.inputs, original.assumptions) == item.value
    supplied = EvaluationRequest(
        model_id="proxy_comparison", method_version="2", assumptions=assumptions, inputs=inputs
    )
    assert all(item.status == "withheld" for item in service.evaluate(supplied, owner).outputs)


@pytest.mark.parametrize(("basis", "stamp", "eligible"), [
    ("regular_session", "2024-04-03T19:59:59Z", False),
    ("regular_session", "2024-04-03T20:00:00Z", True),
    ("early_close_1300_eastern", "2024-04-03T16:59:59Z", False),
    ("early_close_1300_eastern", "2024-04-03T17:00:00Z", True),
])
def test_same_day_receipt_uses_exchange_close(history, basis, stamp, eligible):
    inputs, assumptions = history
    schedule, *prices = inputs.tables
    rows = tuple(row.model_copy(update={"context": row.context.model_copy(update={"basis": basis})})
                 if row.observation_date == inputs.cutoff.observation_date else row for row in schedule.rows)
    query = dict(inputs.provenance.query, left_retrieved_at=stamp)
    inputs = inputs.model_copy(update={
        "tables": (schedule.model_copy(update={"rows": rows}), *prices),
        "provenance": inputs.provenance.model_copy(update={"query": tuple(query.items())}),
    })
    results = RetrospectiveComparisonModel().calculate(inputs, assumptions)
    by_id = {item.output_id: item.value for item in results.outputs}
    assert by_id["right_momentum"] is not None
    assert (by_id["momentum_spread"] is not None) == eligible
    assert retrospective_reference().calculations["momentum_spread"](inputs, assumptions) == by_id["momentum_spread"]

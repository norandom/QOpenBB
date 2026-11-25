"""Bind factor snapshots to the dated observations used in a calculation."""

from decimal import Context, Decimal, localcontext

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    ModelDescriptor,
    Observation,
    OutputDescriptor,
    RuleDescriptor,
    ScalarKind,
    TraceEntry,
    TraceValue,
)
from .sessions import (
    PRICE_BASIS,
    PriceWindow,
    SessionWindow,
    resolve_price_window,
    resolve_session_window,
)


def input_rows(inputs: InputSnapshot, table_id: str) -> tuple[Observation, ...]:
    for table in inputs.tables:
        if table.table_id == table_id:
            return table.rows
    raise ValueError(f"Missing required input table {table_id}")


def text_assumption(assumptions: AssumptionSet, key: str) -> str:
    for item in assumptions.assumptions:
        if item.assumption_id == key and item.value_type == "text" and isinstance(item.value, str):
            return item.value
    raise ValueError(f"Missing required text assumption {key}")


def _entity(rows: tuple[Observation, ...], metric: str) -> str:
    entities = {row.entity_id for row in rows if row.metric_id == metric}
    if len(entities) != 1:
        raise ValueError(f"Expected one entity with {metric} observations, found {len(entities)}")
    return entities.pop()


def evaluation_cutoff(inputs: InputSnapshot, assumptions: AssumptionSet, model_id: str) -> EvaluationCutoff:
    if inputs.schema_id != f"{model_id}.inputs":
        raise ValueError(f"Expected the input schema for {model_id}")
    if inputs.cutoff is None:
        raise ValueError("Missing historical evaluation cutoff")
    if assumptions.effective_date > inputs.cutoff.observation_date:
        raise ValueError(f"Assumptions are not effective on {inputs.cutoff.observation_date}")
    return inputs.cutoff


def session_window(inputs: InputSnapshot, assumptions: AssumptionSet, model_id: str) -> SessionWindow:
    cutoff = evaluation_cutoff(inputs, assumptions, model_id)
    rows = input_rows(inputs, "sessions")
    return resolve_session_window(
        rows, calendar_id=_entity(rows, "session"), cutoff=cutoff,
        schedule_revision=text_assumption(assumptions, "schedule_revision"),
    )


def price_window(inputs: InputSnapshot, assumptions: AssumptionSet, model_id: str) -> PriceWindow:
    window = session_window(inputs, assumptions, model_id)
    if text_assumption(assumptions, "price_basis") != PRICE_BASIS:
        raise ValueError(f"{window.endpoints[-1]} requires {PRICE_BASIS}")
    rows = input_rows(inputs, "closes")
    if not any(row.metric_id == "close" for row in rows):
        raise ValueError(f"Missing close history through {window.endpoints[-1]}")
    return resolve_price_window(window, rows, proxy_id=_entity(rows, "close"))


def substitution(row: Observation) -> TraceValue:
    return TraceValue(name=row.record_id, value=row.value, unit=row.context.unit,
                      currency=row.context.currency, scale=row.context.scale,
                      period_start=row.context.period_start,
                      period_end=row.context.period_end or row.observation_date)


def price_trace(window: PriceWindow, output_id: str, expression: str, intermediates: tuple[TraceValue, ...]) -> TraceEntry:
    return TraceEntry(
        trace_id=output_id, formula_id=output_id, formula_version="1", expression=expression,
        output_id=output_id, check_ids=(f"eligible_inputs.{output_id}",),
        source_record_ids=window.window.source_record_ids + tuple(row.record_id for row in window.closes),
        input_ids=("sessions", "closes"), assumption_ids=("schedule_revision", "price_basis"),
        substitutions=(substitution(window.closes[0]), substitution(window.closes[-1])),
        intermediate_values=intermediates,
    )


def factor_descriptor(model_id: str, entity_type: str, input_ids: tuple[str, ...],
                      outputs: tuple[tuple[str, str, str, ScalarKind], ...], *,
                      period_type: str = "session") -> ModelDescriptor:
    rules = tuple(RuleDescriptor(rule_id=f"eligible_inputs.{name}", version="1",
                                 stage="precondition", severity="blocking")
                  for name, _, _, _ in outputs)
    return ModelDescriptor(
        model_id=model_id, method_version="1", input_schema_id=f"{model_id}.inputs",
        output_schema_id=f"{model_id}.outputs", rule_set_version="1", reference_version="1",
        entity_types=(entity_type,), period_types=(period_type,), input_ids=input_ids, rules=rules,
        outputs=tuple(OutputDescriptor(output_id=name, semantic_definition=expression, unit=unit,
                                       value_type=kind, required_input_ids=input_ids,
                                       required_check_ids=(rule.rule_id,))
                      for (name, expression, unit, kind), rule in zip(outputs, rules, strict=True)),
    )


def result_decimal(value: Decimal) -> Decimal:
    """Round once to wire precision and preserve a nonzero result's sign and magnitude."""
    if value.is_zero():
        return Decimal(0)
    if not value.is_finite() or not -38 <= value.adjusted() <= 37:
        raise ValueError("value exceeds financial decimal range")
    exponent = max(value.adjusted() - 37, -38)
    with localcontext(Context(prec=39)):
        rounded = value.quantize(Decimal((0, (1,), exponent)))
    if rounded.adjusted() > 37:
        raise ValueError("value exceeds financial decimal range")
    return rounded

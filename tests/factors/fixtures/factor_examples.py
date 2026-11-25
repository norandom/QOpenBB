"""Reviewable factor descriptors and expected runs for the offline contract suite."""

import itertools
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import date

from qopenbb_data.modeling.contracts import (
    Assumption,
    AssumptionSet,
    CheckOutcome,
    InputSnapshot,
    ModelDescriptor,
    ModelRun,
    ObservationTable,
    OutputDescriptor,
    OutputResult,
    RuleDescriptor,
    Tolerance,
    TraceEntry,
    TraceValue,
)

from .factor_inputs import (
    END,
    SESSIONS,
    START,
    STUDY_DATES,
    company_inputs,
    cutoff,
    prices,
    schedule,
    study_inputs,
    yields,
)


@dataclass(frozen=True)
class ExpectedOutput:
    output_id: str
    expression: str
    unit: str
    value: str
    input_ids: tuple[str, ...]
    absolute_tolerance: str | None
    depends_on: tuple[str, ...] = ()

    @property
    def value_type(self):
        return "text" if self.absolute_tolerance is None else "decimal"

    @property
    def rule_id(self):
        return f"eligible_inputs.{self.output_id}"


@dataclass(frozen=True)
class Example:
    model_id: str
    entity_type: str
    period_type: str
    input_ids: tuple[str, ...]
    outputs: tuple[ExpectedOutput, ...]
    tables: Callable[[bool], tuple[ObservationTable, ...]]
    withheld: dict[str, str]
    observation_date: date = END
    partial_values: dict[str, str] = field(default_factory=dict)
    variant: str = "missing"

    def descriptor(self):
        return ModelDescriptor(
            model_id=self.model_id, method_version="1", rule_set_version="1",
            reference_version="1", input_schema_id=f"{self.model_id}.inputs",
            output_schema_id=f"{self.model_id}.outputs", entity_types=(self.entity_type,),
            period_types=(self.period_type,), input_ids=self.input_ids,
            rules=tuple(RuleDescriptor(rule_id=item.rule_id, version="1",
                                       stage="precondition", severity="blocking")
                        for item in self.outputs),
            outputs=tuple(OutputDescriptor(
                output_id=item.output_id, semantic_definition=item.expression,
                value_type=item.value_type, unit=item.unit, required_input_ids=item.input_ids,
                required_check_ids=(item.rule_id,), required_output_ids=item.depends_on,
            ) for item in self.outputs),
        )


MOMENTUM = "100 × (last close / first close − 1), excluding dividends"
VOLATILITY = "100 × √252 × sample standard deviation of 63 adjacent simple returns (divisor 62)"
PERCENT_TOLERANCE = "0.00000001"
POINTS_TOLERANCE = "0.00000002"
RATIO_TOLERANCE = "0.000000001"
PRICE_INPUTS = ("sessions", "closes")
LEFT = ("sessions", "left_closes")
RIGHT = ("sessions", "right_closes")
PAIR = ("sessions", "left_closes", "right_closes")
STUDY = ("dated_signals", "dated_regimes", "forward_returns")
MISSING_CLOSE = "Missing required split-adjusted close on 2024-04-03"


EXAMPLES = {example.model_id: example for example in (
    Example(
        "etf_momentum", "etf", "session", PRICE_INPUTS,
        (ExpectedOutput("momentum", MOMENTUM, "percent", "20", PRICE_INPUTS, PERCENT_TOLERANCE),),
        lambda missing: (schedule(), prices("closes", "fixture_left", "120", missing)),
        {"momentum": MISSING_CLOSE},
    ),
    Example(
        "etf_realized_volatility", "etf", "session", PRICE_INPUTS,
        (ExpectedOutput("realized_volatility", VOLATILITY, "percent", "40",
                        PRICE_INPUTS, PERCENT_TOLERANCE),),
        lambda missing: (schedule(), prices("closes", "fixture_left", "120", missing)),
        {"realized_volatility": MISSING_CLOSE},
    ),
    Example(
        "real_yield_regime", "macro_series", "session", ("sessions", "dfii10"),
        (
            ExpectedOutput("regime", "Sign of exact DFII10 endpoint change", "classification",
                           "rising", ("sessions", "dfii10"), None),
            ExpectedOutput("change", "End DFII10 level minus start level", "percentage_points",
                           "0.25", ("sessions", "dfii10"), POINTS_TOLERANCE),
        ),
        lambda missing: (schedule(), yields(missing)),
        {"regime": "Missing DFII10 endpoint on 2024-04-03",
         "change": "Missing DFII10 endpoint on 2024-04-03"},
    ),
    Example(
        "issuer_fcf_yield", "company", "trailing_fiscal_year", ("cash_flows", "market_value"),
        (ExpectedOutput("fcf_yield", "100 × (operating cash flow − capex spending) / equity market value",
                        "percent", "5", ("cash_flows", "market_value"), PERCENT_TOLERANCE),),
        company_inputs, {"fcf_yield": "Missing issuer equity market value on 2024-04-03"},
    ),
    Example(
        "proxy_comparison", "ordered_etf_pair", "session", PAIR,
        (
            ExpectedOutput("left_momentum", MOMENTUM, "percent", "20", LEFT, PERCENT_TOLERANCE),
            ExpectedOutput("right_momentum", MOMENTUM, "percent", "10", RIGHT, PERCENT_TOLERANCE),
            ExpectedOutput("momentum_spread", "Left minus right momentum", "percentage_points",
                           "10", PAIR, POINTS_TOLERANCE, ("left_momentum", "right_momentum")),
            ExpectedOutput("left_volatility", VOLATILITY, "percent", "40", LEFT, PERCENT_TOLERANCE),
            ExpectedOutput("right_volatility", VOLATILITY, "percent", "20", RIGHT, PERCENT_TOLERANCE),
            ExpectedOutput("volatility_spread", "Left minus right volatility", "percentage_points",
                           "20", PAIR, POINTS_TOLERANCE, ("left_volatility", "right_volatility")),
        ),
        lambda missing: (schedule(), prices("left_closes", "fixture_left", "120", False),
                         prices("right_closes", "fixture_right", "110", missing)),
        {"right_momentum": MISSING_CLOSE, "right_volatility": MISSING_CLOSE,
         "momentum_spread": "Right momentum withheld", "volatility_spread": "Right volatility withheld"},
    ),
    Example(
        "timing_study", "etf_study", "study_interval", STUDY,
        (
            ExpectedOutput("rising_hit_rate", "Rising group winners / eligible outcomes including ties",
                           "ratio", "0.3333333333333333333333333333", STUDY, RATIO_TOLERANCE),
            ExpectedOutput("rising_slugging", "Rising group mean winner / absolute mean loser",
                           "ratio", "2", STUDY, RATIO_TOLERANCE),
            ExpectedOutput("falling_hit_rate", "Falling group winners / eligible outcomes including ties",
                           "ratio", "0.5", STUDY, RATIO_TOLERANCE),
            ExpectedOutput("falling_slugging", "Falling group mean winner / absolute mean loser",
                           "ratio", "3", STUDY, RATIO_TOLERANCE),
            ExpectedOutput("study_drawdown", "Maximum peak-to-trough loss on the full exposed wealth path",
                           "percent", "8.8", ("dated_signals", "forward_returns"), PERCENT_TOLERANCE),
        ),
        study_inputs,
        {"rising_slugging": "No eligible rising-group loser after the missing benchmark return"},
        STUDY_DATES[-1], {"rising_hit_rate": "0.5"},
    ),
)}


UNKNOWN_DFII10_AVAILABILITY = replace(
    EXAMPLES["real_yield_regime"],
    tables=lambda missing: (schedule(), yields(False, unknown_availability=missing)),
    withheld={
        "regime": "Unknown historical availability for DFII10 endpoint on 2024-04-03",
        "change": "Unknown historical availability for DFII10 endpoint on 2024-04-03",
    },
    variant="unknown_availability",
)


def text_assumption(name, value, rationale):
    return Assumption(assumption_id=name, value_type="text", value=value,
                      origin="method_default", rationale=rationale)


def example_assumptions(example):
    assumptions = []
    if "sessions" in example.input_ids:
        assumptions.extend((
            text_assumption("schedule_revision", "fixture_us_listing.2024r1",
                            "Synthetic listing schedule shared by both proxies"),
        ))
    if "sessions" in example.input_ids and "dfii10" not in example.input_ids:
        assumptions.append(text_assumption("price_basis", "split_adjusted_dividends_excluded",
                                           "Price metrics exclude distributions"))
    if example.model_id == "proxy_comparison":
        assumptions.extend((
            text_assumption("left_proxy", "fixture_left", "Minuend in the ordered comparison"),
            text_assumption("right_proxy", "fixture_right", "Subtrahend in the ordered comparison"),
            text_assumption("leg_methods", "etf_momentum@1, etf_realized_volatility@1",
                            "Both legs use the same versioned price-return methods"),
        ))
    if example.model_id == "issuer_fcf_yield":
        assumptions.append(text_assumption("capex_sign", "cash_outflow_negative",
                                           "Convert negative filing cash outflow to positive spending"))
    if example.model_id == "timing_study":
        assumptions.extend((
            text_assumption("schedule_revision", "fixture_us_listing.2024r1", "Synthetic NY sessions"),
            text_assumption("study_schedule", ";".join(
                f"{day}T14:00:00+00:00/{day}T22:00:00+00:00" for day in STUDY_DATES
            ), "Supplied session opens and decision cutoffs for the study"),
            text_assumption("position_rule", "long_when_momentum_positive.v1", "Use prior-session signal"),
            text_assumption("horizon", "one_session_open_to_open", "Outcome intervals do not overlap"),
            text_assumption("benchmark", "fixture_benchmark", "Use matched benchmark return"),
            text_assumption("partition", "out_of_sample", "All outcomes belong to the held-out partition"),
            text_assumption("study_dates", "2024-06-04/2024-06-11", "Inclusive outcome path dates"),
            text_assumption("universe", "fixture_left", "Study universe contains one ETF"),
            text_assumption("drawdown_basis", "full_study_exposed_returns", "Compound chronological returns"),
        ))
    return AssumptionSet(version="1", effective_date=START, assumptions=assumptions)


def build_run(example, missing):
    descriptor = example.descriptor()
    evaluation = cutoff(example.observation_date)
    inputs = InputSnapshot(
        schema_id=descriptor.input_schema_id, cutoff=evaluation, tables=example.tables(missing),
        provenance={"origin": "user_supplied", "source": "synthetic_factor_examples",
                        "query": (), "retrieved_at": evaluation.evaluated_at},
    )
    assumptions = example_assumptions(example)
    outputs, checks, trace = [], [], []
    overrides = example.partial_values if missing else {}
    for expected in example.outputs:
        reason = example.withheld.get(expected.output_id) if missing else None
        value = overrides.get(expected.output_id, expected.value)
        result, check = output_and_check(expected, value, reason)
        outputs.append(result)
        checks.append(check)
        if reason is None:
            trace.append(build_trace(expected, inputs, assumptions, missing))
    return ModelRun(
        run_id=f"{example.model_id}.{example.variant if missing else 'valid'}",
        owner_id="fixture_analyst", created_at=evaluation.evaluated_at, descriptor=descriptor,
        inputs=inputs, assumptions=assumptions, outputs=outputs, trace=trace, checks=checks,
    )


def output_and_check(expected, value, reason):
    numeric = reason is None and expected.absolute_tolerance is not None
    # The expected scalar illustrates the wire contract. Independent verifiers are separate tasks.
    output = OutputResult(
        output_id=expected.output_id, semantic_definition=expected.expression, unit=expected.unit,
        value_type=expected.value_type, value=None if reason else value,
        status="withheld" if reason else "unverified",
        reason=reason or "Draft synthetic expected value awaits independent verification",
        trace_ids=() if reason else (expected.output_id,), check_ids=(expected.rule_id,),
    )
    check = CheckOutcome(
        rule_id=expected.rule_id, rule_version="1", severity="blocking",
        status="fail" if reason else "pass", explanation=reason,
        input_ids=expected.input_ids, output_ids=(expected.output_id,),
        observed_value=value if numeric else None, expected_value=value if numeric else None,
        tolerance=Tolerance(unit=expected.unit, absolute=expected.absolute_tolerance) if numeric else None,
    )
    return output, check


def build_trace(expected, inputs, assumptions, missing):
    tables = [table for table in inputs.tables if table.table_id in expected.input_ids]
    rows = [row for table in tables for row in table.rows]
    if expected.output_id.startswith(("rising_", "falling_")):
        # Group outcome dates follow decisions by two session positions.
        positions = slice(0, 3) if expected.output_id.startswith("rising_") else slice(3, 5)
        decisions = STUDY_DATES[:-2][positions]
        ends = STUDY_DATES[2:][positions]
        rows = [
            row for row in rows
            if row.observation_date in (ends if row.metric_id == "forward_return" else decisions)
        ]
    if expected.output_id == "study_drawdown":
        rows = [row for row in rows if row.entity_id == "fixture_left"]
    substitutions = tuple(
        TraceValue(name=row.record_id, value=row.value, unit=row.context.unit,
                   currency=row.context.currency, scale=row.context.scale,
                   period_start=row.context.period_start, period_end=row.context.period_end or row.observation_date)
        for row in rows if row.metric_id != "session"
        if row.metric_id != "close" or row.observation_date in {START, END}
    )
    return TraceEntry(
        trace_id=expected.output_id, formula_id=expected.output_id, formula_version="1",
        expression=expected.expression, output_id=expected.output_id, check_ids=(expected.rule_id,),
        source_record_ids=tuple(row.record_id for row in rows), input_ids=expected.input_ids,
        assumption_ids=tuple(item.assumption_id for item in assumptions.assumptions),
        substitutions=substitutions, intermediate_values=intermediates(expected.output_id, missing),
    )


def intermediates(output_id, missing):
    if output_id == "fcf_yield":
        return (
            TraceValue(name="capex_spending", value="20", unit="currency", currency="USD", scale=6),
            TraceValue(name="free_cash_flow", value="40", unit="currency", currency="USD", scale=6),
        )
    if output_id in {"realized_volatility", "left_volatility", "right_volatility"}:
        first_return = "0.1" if output_id == "right_volatility" else "0.2"
        dated_returns = tuple(
            TraceValue(name=f"simple_return.{end}", value=first_return if index == 0 else "0",
                       unit="ratio", period_start=start, period_end=end)
            for index, (start, end) in enumerate(itertools.pairwise(SESSIONS))
        )
        return dated_returns + (
            TraceValue(name="return_count", value="63", unit="count"),
            TraceValue(name="sample_divisor", value="62", unit="count"),
            TraceValue(name="annualization_sessions", value="252", unit="count"),
        )
    if output_id in {"momentum", "left_momentum", "right_momentum"}:
        return (TraceValue(name="observation_count", value="64", unit="count",
                           period_start=START, period_end=END),)
    if output_id.startswith(("rising_", "falling_")):
        rising = output_id.startswith("rising_")
        return (
            TraceValue(name="eligible_count", value="3" if rising and not missing else "2", unit="count"),
            TraceValue(name="excluded_count", value="1" if rising and missing else "0", unit="count"),
            TraceValue(name="mean_winner", value="10" if rising else "12", unit="percentage_points"),
        ) + (() if rising and missing else (
            TraceValue(name="absolute_mean_loser", value="5" if rising else "4", unit="percentage_points"),
        ))
    return ()

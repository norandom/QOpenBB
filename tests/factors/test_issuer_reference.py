"""Independent issuer FCF yield comparison against dated filings."""

import itertools
from datetime import date, timedelta
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.contracts import CheckOutcome
from qopenbb_data.modeling.models.factors.fcf_yield import FcfYieldModel
from qopenbb_data.modeling.validation.outputs import resolve_outputs
from qopenbb_data.modeling.validation.rules import Rule, RuleContext, evaluate_stage
from qopenbb_data.modeling.verification.factors.issuer_reference import issuer_reference
from qopenbb_data.modeling.verification.reference import verify_outputs

EXAMPLE = EXAMPLES["issuer_fcf_yield"]


def with_rows(run, *, flows=None, equity=None):
    tables = tuple(table.model_copy(update={"rows": rows}) if rows is not None else table
                   for table, rows in zip(run.inputs.tables, (flows, equity), strict=True))
    return run.model_copy(update={"inputs": run.inputs.model_copy(update={"tables": tables})})


def candidate_for(run):
    return FcfYieldModel().calculate(run.inputs, run.assumptions)


def verify(run, value, *, trace=None, check_status="pass", reason=None):
    output = run.outputs[0].model_copy(update={
        "value": value, "status": "withheld" if value is None else "unverified",
        "reason": reason or "Awaiting comparison",
        "trace_ids": () if value is None else run.outputs[0].trace_ids,
    })
    check = run.checks[0]
    if check_status != check.status:
        check = check.model_copy(update={
            "status": check_status, "explanation": reason,
            "observed_value": None, "expected_value": None, "tolerance": None,
        })
    outputs, evidence, _ = verify_outputs(run.descriptor, run.inputs, run.assumptions,
                                         (output,), run.trace if trace is None else trace,
                                         (check,), issuer_reference())
    return outputs[0].status, evidence[0].status


@pytest.mark.parametrize(("ocf", "expected", "mutant"), [
    ("60", "5", "10"), ("20", "0", "5"), ("-60", "-10", "10"),
])
@pytest.mark.parametrize("positive_spending", [False, True])
def test_filing_sign_and_zero_negative_numerators(ocf, expected, mutant, positive_spending):
    run = build_run(EXAMPLE, False)
    cash, capex = run.inputs.tables[0].rows
    cash = cash.model_copy(update={"value": Decimal(ocf)})
    if positive_spending:
        basis = "spending_positive"
        item, = run.assumptions.assumptions
        run = run.model_copy(update={"assumptions": run.assumptions.model_copy(
            update={"assumptions": (item.model_copy(update={"value": basis}),)})})
        capex = capex.model_copy(update={"value": Decimal(20), "context": capex.context.model_copy(
            update={"basis": basis})})
    run = with_rows(run, flows=(cash, capex))
    candidate = candidate_for(run)
    value = candidate.outputs[0].value
    assert value == Decimal(expected)
    assert verify(run, value, trace=candidate.trace) == ("verified", "match")
    assert verify(run, Decimal(mutant)) == ("withheld", "mismatch")
    assert verify(run, value, check_status="unknown", reason="Check unavailable") == ("unverified", "match")
    if value <= 0:
        assert verify(run, None, check_status="fail", reason="Nonpositive numerator incorrectly withheld") == (
            "withheld", "unavailable")
        assert issuer_reference().calculations["fcf_yield"](run.inputs, run.assumptions) == value


@pytest.mark.parametrize("overlap", [False, True])
def test_rolling_fiscal_year_and_late_amendment(overlap):
    run = build_run(EXAMPLE, False)
    annual = run.inputs.tables[0].rows
    ends = [date(2023, 3, 31), date(2023, 6, 30), date(2023, 9, 30),
            date(2023, 12, 31), date(2024, 3, 31)]
    quarters = tuple(source.model_copy(update={
        "record_id": f"{source.metric_id}.quarter.{end}", "source_record_id": f"filing.{end}",
        "observation_date": end, "published_at": run.inputs.cutoff.decision_at,
        "value": amount, "context": source.context.model_copy(update={
            "period_start": start + timedelta(days=1), "period_end": end, "frequency": "standalone_quarter",
        }),
    }) for start, end in itertools.pairwise(ends)
        for source, amount in zip(annual, (Decimal(19), Decimal(-3)), strict=True))
    late = tuple(row.model_copy(update={
        "record_id": f"{row.record_id}.late", "published_at": row.published_at + timedelta(seconds=1),
        "vintage_at": row.published_at + timedelta(seconds=1),
        "value": row.value * 2,
    }) for row in quarters[-2:])
    if overlap:
        # An overlapping quarter cannot be counted in addition to its predecessor.
        quarters = (*quarters[:-2], *(row.model_copy(update={"context": row.context.model_copy(
            update={"period_start": row.context.period_start - timedelta(days=4)})})
            for row in quarters[-2:]))
        run = with_rows(run, flows=(*late, *reversed(quarters)))
        output, = candidate_for(run).outputs
        assert issuer_reference().calculations["fcf_yield"](run.inputs, run.assumptions) is output.value is None
        assert verify(run, output.value, check_status="fail", reason=output.reason) == ("withheld", "unavailable")
        return
    run = with_rows(run, flows=(*late, *reversed(quarters), *annual))
    candidate = candidate_for(run)
    assert candidate.outputs[0].value == Decimal(8)
    assert candidate.trace[0].source_record_ids[:-1] == tuple(row.record_id for row in quarters)
    assert [(item.period_start, item.period_end) for item in candidate.trace[0].substitutions[:-1]] == [
        (row.context.period_start, row.context.period_end) for row in quarters
    ]
    assert verify(run, candidate.outputs[0].value, trace=candidate.trace) == ("verified", "match")
    assert verify(run, Decimal(10)) == ("withheld", "mismatch")


@pytest.mark.parametrize("case", ["missing", "zero", "negative", "sign", "unit", "currency", "scale",
                                  "scope", "stale", "ytd", "unknown", "premature", "unpublished"])
def test_issuer_unavailable_matches_production(case):
    run = build_run(EXAMPLE, case == "missing")
    cash, capex = run.inputs.tables[0].rows
    if case in {"sign", "ytd", "unknown", "premature", "unpublished"}:
        if case in {"ytd", "unknown"}:
            change = {"fiscal_period": "FY_YTD"} if case == "ytd" else {"vintage_coverage": "unknown"}
            flows = tuple(row.model_copy(update={"context": row.context.model_copy(update=change)})
                          for row in (cash, capex))
        elif case == "premature":
            flows = tuple(row.model_copy(update={"published_at": row.published_at - timedelta(days=90)})
                          for row in (cash, capex))
        elif case == "unpublished":
            flows = tuple(row.model_copy(update={"published_at": None}) for row in (cash, capex))
        else:
            flows = (cash, capex.model_copy(update={"value": Decimal(20)}))
        run = with_rows(run, flows=flows)
    elif case != "missing":
        market, = run.inputs.tables[1].rows
        changes = {"unit": {"unit": "price"}, "currency": {"currency": "EUR"},
                   "scale": {"scale": 3}, "scope": {"consolidation_scope": "share_class"},
                   "stale": {"period_end": market.observation_date - timedelta(days=1)}}
        updates = ({"value": Decimal(0 if case == "zero" else -1)} if case in {"zero", "negative"}
                   else {"context": market.context.model_copy(update=changes[case])})
        run = with_rows(run, equity=(market.model_copy(update=updates),))
    output, = candidate_for(run).outputs
    assert issuer_reference().calculations["fcf_yield"](run.inputs, run.assumptions) is output.value is None
    assert output.reason
    if case == "missing":
        assert run.checks[0].status == "fail"
        assert output.reason == run.checks[0].explanation
    assert verify(run, output.value, check_status="fail", reason=output.reason) == ("withheld", "unavailable")


@pytest.mark.parametrize(("offset", "comparison"), [
    ("0.00000001", ("verified", "match")), ("0.000000011", ("withheld", "mismatch")),
])
def test_frozen_issuer_tolerance(offset, comparison):
    run = build_run(EXAMPLE, False)
    assert verify(run, Decimal(5) + Decimal(offset)) == comparison


@pytest.mark.parametrize("field", ["version", "effective_date", "assumptions", "convention", "type"])
def test_issuer_requires_versioned_dated_assumptions(field):
    run = build_run(EXAMPLE, False)
    item, = run.assumptions.assumptions
    changes = {
        "version": {"version": "2"},
        "effective_date": {"effective_date": run.inputs.cutoff.observation_date + timedelta(days=1)},
        "assumptions": {"assumptions": ()},
        "convention": {"assumptions": (item.model_copy(update={"value": "unknown"}),)},
        "type": {"assumptions": (item.model_copy(update={"value_type": "integer", "value": 1}),)},
    }
    assumptions = run.assumptions.model_copy(update=changes[field])
    assert issuer_reference().calculations["fcf_yield"](run.inputs, assumptions) is None


def evaluate_reference(run, candidate):
    reference = issuer_reference()

    def bind(output):
        rule_id, = output.required_check_ids

        def evaluate(context):
            value = reference.calculations[output.output_id](context.inputs, context.assumptions)
            return CheckOutcome(
                rule_id=rule_id, rule_version="1", severity="blocking",
                input_ids=output.required_input_ids, output_ids=(output.output_id,),
                status="fail" if value is None else "pass",
                observed="insufficient evidence" if value is None else "eligible dated inputs",
                expected="eligible dated inputs",
                explanation="Independent calculation has insufficient evidence" if value is None else None,
            )

        return Rule(rule_id, output.required_input_ids, (output.output_id,), evaluate)

    rules = tuple(bind(output) for output in run.descriptor.outputs)
    checks = evaluate_stage(run.descriptor, rules, "precondition", RuleContext(run.inputs, run.assumptions))
    outputs = resolve_outputs(run.descriptor, candidate, checks, inputs=run.inputs)
    outputs, evidence, _ = verify_outputs(run.descriptor, run.inputs, run.assumptions, outputs,
                                         candidate.trace, checks, reference)
    return checks, outputs, evidence


@pytest.mark.parametrize(("case", "check_status", "explanation", "output_reason"), [
    ("missing_table", "unknown", "Required input table is absent", "A required input table is absent"),
    ("wrong_unit", "fail", "Independent calculation has insufficient evidence", "A blocking financial rule failed"),
    ("valid", "pass", "Observed condition met the expectation: eligible dated inputs", None),
])
def test_issuer_reference_preconditions(case, check_status, explanation, output_reason):
    run = build_run(EXAMPLE, False)
    original, measured = run.inputs.tables
    tables = (original, measured)
    if case == "missing_table":
        tables = (original,)
    elif case == "wrong_unit":
        row = measured.rows[-1]
        wrong_unit = row.model_copy(update={"context": row.context.model_copy(update={"unit": "ratio"})})
        tables = (original, measured.model_copy(update={"rows": (*measured.rows[:-1], wrong_unit)}))
    run = run.model_copy(update={"inputs": run.inputs.model_copy(update={"tables": tables})})
    candidate = FcfYieldModel().calculate(run.inputs, run.assumptions)
    reference = issuer_reference()
    values = tuple(reference.calculations[item.output_id](run.inputs, run.assumptions)
                   for item in candidate.outputs)
    assert values == tuple(item.value for item in candidate.outputs)
    checks, outputs, evidence = evaluate_reference(run, candidate)
    assert [(check.rule_id, check.status, check.explanation) for check in checks] == [
        (definition.rule_id, check_status, explanation) for definition in run.descriptor.rules
    ]
    verified = case == "valid"
    assert [(item.status, item.value, item.reason, item.check_ids) for item in outputs] == [
        ("verified" if verified else "withheld", value, output_reason, definition.required_check_ids)
        for value, definition in zip(values, run.descriptor.outputs, strict=True)
    ]
    assert [item.status for item in evidence] == ["match" if verified else "unavailable"] * len(values)


@pytest.mark.parametrize("conflict", [False, True])
def test_same_period_annual_reconciles_with_quarters(conflict):
    run = build_run(EXAMPLE, False)
    annual = run.inputs.tables[0].rows
    assert tuple(row.value for row in annual) == (Decimal(60), Decimal(-20))
    boundaries = [date(2022, 12, 31), date(2023, 3, 31), date(2023, 6, 30),
                  date(2023, 9, 30), date(2023, 12, 31)]
    quarters = tuple(source.model_copy(update={
        "record_id": f"{source.metric_id}.quarter.{end}", "source_record_id": f"filing.{end}",
        "observation_date": end, "value": amount, "context": source.context.model_copy(update={
            "period_start": start + timedelta(days=1), "period_end": end, "frequency": "quarterly",
        }),
    }) for start, end in itertools.pairwise(boundaries)
        for source, amount in zip(annual, (Decimal(15), Decimal(-5)), strict=True))
    if conflict:
        quarters = (quarters[0].model_copy(update={"value": Decimal(16)}), *quarters[1:])
    run = with_rows(run, flows=(*annual, *quarters))
    candidate = candidate_for(run)
    independently_calculated = issuer_reference().calculations["fcf_yield"](run.inputs, run.assumptions)
    assert candidate.outputs[0].value == independently_calculated == (None if conflict else Decimal(5))
    if conflict:
        assert "conflict" in candidate.outputs[0].reason.lower()
    checks, outputs, evidence = evaluate_reference(run, candidate)
    assert checks[0].status == ("fail" if conflict else "pass")
    assert outputs[0].status == ("withheld" if conflict else "verified")
    assert evidence[0].status == ("unavailable" if conflict else "match")

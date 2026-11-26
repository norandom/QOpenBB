"""Signed evaluation and saved evidence through the installed modeling listener."""

from decimal import Decimal
from json import dumps
from urllib.parse import urlencode

import pytest
from fixtures.factor_examples import EXAMPLES, UNKNOWN_DFII10_AVAILABILITY, build_run
from test_model_identity import assertion
from test_model_listener import exchange, internal_listener


@pytest.fixture(scope="module")
def modeling_url(tmp_path_factory):
    with internal_listener(tmp_path_factory.mktemp("installed-factor-runs")) as origin:
        yield origin + "/modeling/v1"


@pytest.fixture
def owner():
    return assertion(claims={"sub": "fixture_analyst"})


def evaluate(url, owner, fixture_run, inputs=None):
    payload = {
        "model_id": fixture_run.descriptor.model_id,
        "method_version": "1",
        "inputs": fixture_run.inputs.model_dump(mode="json")
        if inputs is None
        else inputs,
        "assumptions": fixture_run.assumptions.model_dump(mode="json"),
    }
    status, saved = exchange(
        url + "/evaluations", owner, payload=dumps(payload).encode()
    )
    assert status == 200, saved
    assert saved["owner_id"] == "fixture_analyst"
    assert saved["inputs"] == payload["inputs"]
    return saved


def run_url(url, run):
    return url + "/runs/" + run["run_id"]


def assert_trace(run, output):
    traces = [
        entry for entry in run["trace"] if entry["trace_id"] in output["trace_ids"]
    ]
    assert traces
    records = {
        row["record_id"] for table in run["inputs"]["tables"] for row in table["rows"]
    }
    cited = {record_id for trace in traces for record_id in trace["source_record_ids"]}
    assert cited and cited <= records
    for trace in traces:
        assert trace["output_id"] == output["output_id"]
        assert trace["formula_version"] == "1"
        assert trace["expression"]


def assert_projection(url, owner, run, output, widget):
    output_id = output["output_id"]
    params = urlencode({"run_id": run["run_id"], "output_id": output_id})
    status, projection = exchange(url + "/" + widget["endpoint"] + "?" + params, owner)
    assert status == 200
    assert exchange(run_url(url, run) + "/outputs/" + output_id, owner) == (
        200,
        projection,
    )
    (row,) = projection[widget["data"]["dataKey"]]
    assert {key: row[key] for key in output} == output
    assert row["freshness"] == "saved"
    assert row["display_text"] == output["value"]
    assert url + "/" + row["run_detail_href"] == run_url(url, run)
    assert projection["run_id"] == run["run_id"]
    assert projection["trace"] == [
        trace for trace in run["trace"] if trace["trace_id"] in output["trace_ids"]
    ]
    assert projection["checks"] == [
        check for check in run["checks"] if check["rule_id"] in output["check_ids"]
    ]
    assert projection["verification"] == [
        entry for entry in run["verification"] if entry["output_id"] == output_id
    ]


def test_signed_catalog_installs_six_exact_versions(modeling_url, owner):
    url = modeling_url + "/models"
    assert exchange(url, headers={"X-User-Id": "fixture_analyst"})[0] == 401
    status, catalog = exchange(url, owner)
    assert status == 200
    assert sorted(
        (
            item["model_id"],
            item["method_version"],
            item["rule_set_version"],
            item["reference_version"],
        )
        for item in catalog["models"]
    ) == [(model_id, "1", "1", "1") for model_id in sorted(EXAMPLES)]
    sample = build_run(EXAMPLES["etf_momentum"], missing=False)
    payload = dumps(
        {
            "model_id": "etf_momentum",
            "method_version": "2",
            "inputs": sample.inputs.model_dump(mode="json"),
            "assumptions": sample.assumptions.model_dump(mode="json"),
        }
    ).encode()
    status, failure = exchange(modeling_url + "/evaluations", owner, payload=payload)
    assert status == 422 and failure["code"] == "unsupported_method"


@pytest.mark.parametrize(
    ("model_id", "variant"),
    [(model_id, "verified") for model_id in EXAMPLES]
    + [
        ("proxy_comparison", "partial"),
        ("timing_study", "partial"),
        ("real_yield_regime", "withheld"),
    ],
    ids=lambda value: value,
)
def test_save_installed_factor_and_project_evidence(
    modeling_url, owner, model_id, variant
):
    example = (
        UNKNOWN_DFII10_AVAILABILITY if variant == "withheld" else EXAMPLES[model_id]
    )
    run = evaluate(
        modeling_url, owner, build_run(example, missing=variant != "verified")
    )
    assert exchange(run_url(modeling_url, run), owner) == (200, run)
    assert (
        exchange(run_url(modeling_url, run), assertion(claims={"sub": "other"}))[0]
        == 404
    )

    status, catalog = exchange(modeling_url + "/models", owner)
    assert status == 200
    assert run["descriptor"] in catalog["models"]
    status, widgets = exchange(modeling_url + "/widgets.json", owner)
    assert status == 200
    (widget,) = widgets.values()
    expected = {item.output_id: item for item in example.outputs}
    evidence = {entry["output_id"]: entry for entry in run["verification"]}
    checks = {entry["rule_id"]: entry for entry in run["checks"]}
    assert {item["output_id"] for item in run["outputs"]} == expected.keys()
    for output in run["outputs"]:
        output_id = output["output_id"]
        item = expected[output_id]
        assert output["unit"] == item.unit
        assert evidence[output_id]["reference_version"] == "1"
        check = checks[item.rule_id]
        assert check["rule_version"] == "1"
        assert check["output_ids"] == [output_id]
        if variant != "verified" and output_id in example.withheld:
            assert output["status"] == "withheld"
            assert output["value"] is None and output["reason"]
            assert evidence[output_id]["status"] == "unavailable"
            assert check["status"] in ("fail", "unknown")
            assert check["explanation"]
        else:
            assert output["status"] == "verified"
            assert evidence[output_id]["status"] == "match"
            assert check["status"] == "pass"
            target = (
                example.partial_values.get(output_id, item.value)
                if variant == "partial"
                else item.value
            )
            if item.absolute_tolerance is None:
                assert output["value"] == target
            else:
                assert abs(Decimal(output["value"]) - Decimal(target)) <= Decimal(
                    item.absolute_tolerance
                )
            assert_trace(run, output)
        assert_projection(modeling_url, owner, run, output, widget)


def test_timing_study_withholds_unsupported_return_tenor(modeling_url, owner):
    fixture_run = build_run(EXAMPLES["timing_study"], missing=False)
    items = tuple(
        item.model_copy(update={"value": "two_session_open_to_open"})
        if item.assumption_id == "horizon"
        else item
        for item in fixture_run.assumptions.assumptions
    )
    assumptions = fixture_run.assumptions.model_copy(update={"assumptions": items})
    run = evaluate(
        modeling_url, owner, fixture_run.model_copy(update={"assumptions": assumptions})
    )
    assert exchange(run_url(modeling_url, run), owner) == (200, run)
    assert all(
        item["status"] == "withheld" and item["value"] is None
        for item in run["outputs"]
    )
    assert all(item["status"] == "unavailable" for item in run["verification"])
    assert run["checks"]
    for check in run["checks"]:
        assert check["status"] in ("fail", "unknown")
        assert "one_session_open_to_open" in check["explanation"]


def test_saved_fcf_snapshot_survives_filing_revision(tmp_path, owner):
    example = build_run(EXAMPLES["issuer_fcf_yield"], missing=False)
    directory = tmp_path / "runs"
    with internal_listener(directory) as origin:
        first = evaluate(origin + "/modeling/v1", owner, example)
    revised_inputs = example.inputs.model_dump(mode="json")
    cash, capex = revised_inputs["tables"][0]["rows"]
    # The amended filing changes operating cash flow and preserves the capex convention.
    cash["value"] = "-60"
    for row in (cash, capex):
        row["source_record_id"] = "synthetic_amended_filing_2023"
    with internal_listener(directory) as origin:
        url = origin + "/modeling/v1"
        revised = evaluate(url, owner, example, revised_inputs)
        assert revised["run_id"] != first["run_id"]
        assert exchange(run_url(url, first), owner) == (200, first)
        assert exchange(run_url(url, revised), owner) == (200, revised)
        status, widgets = exchange(url + "/widgets.json", owner)
        assert status == 200
        (widget,) = widgets.values()
        for run in (first, revised):
            (output,) = run["outputs"]
            assert_projection(url, owner, run, output, widget)
        older_result = urlencode(
            {
                "run_id": first["run_id"],
                "output_id": "fcf_yield",
                "expected_run_id": revised["run_id"],
            }
        )
        status, stale = exchange(
            url + "/" + widget["endpoint"] + "?" + older_result, owner
        )
        assert status == 200
        (row,) = stale["results"]
        assert row["freshness"] == "stale"
        assert Decimal(row["display_text"]) == 5
        assert stale["verification"] == first["verification"]
    for run, value in ((first, Decimal(5)), (revised, Decimal(-10))):
        (output,) = run["outputs"]
        (verification,) = run["verification"]
        assert output["status"] == "verified"
        assert Decimal(output["value"]) == value
        assert verification["status"] == "match"
        assert_trace(run, output)
        (trace,) = run["trace"]
        intermediates = {item["name"]: item for item in trace["intermediate_values"]}
        free_cash_flow = intermediates["free_cash_flow"]
        assert Decimal(free_cash_flow["value"]) == value * 8
        assert (free_cash_flow["currency"], free_cash_flow["scale"]) == ("USD", 6)
        assert Decimal(intermediates["capex_spending"]["value"]) == 20
    assert (
        first["verification"][0]["input_fingerprint"]
        != revised["verification"][0]["input_fingerprint"]
    )
    assert (
        first["inputs"]["tables"][0]["rows"][0]["source_record_id"]
        == "synthetic_annual_filing_2023"
    )

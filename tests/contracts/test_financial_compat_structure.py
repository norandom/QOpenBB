import json
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WIDGET = "qopenbb_saved_model_output"


@pytest.fixture
def contracts():
    bundle = {
        path.name: json.loads(path.read_text())
        for path in (ROOT / "contracts/modeling/v1").glob("*.json")
        if path.name != "manifest.json"
    }
    consumer = json.loads(
        (
            ROOT / "contracts/consumers/financial-modeling/saved-output.v1.json"
        ).read_text()
    )
    return bundle, deepcopy(bundle), consumer, deepcopy(consumer)


def compare(contracts):
    from qopenbb_ci.financial_compat_structure import compare_structure

    return compare_structure(*contracts)


def operation(bundle):
    return bundle["openapi.json"]["paths"]["/widget-results"]["get"]


def projection_rows(bundle):
    for projection in (
        bundle["widget-projection.schema.json"],
        bundle["openapi.json"]["components"]["schemas"]["WidgetProjection"],
    ):
        yield projection["$defs"]["ProjectedOutput"]


def test_pinned_contract_and_schema_annotations(contracts):
    _, candidate, _, _ = contracts
    candidate["widget-projection.schema.json"]["examples"] = [{"results": []}]
    operation(candidate)["responses"]["200"]["description"] = "Saved result"
    assert compare(contracts) == []


@pytest.mark.parametrize("copy", ["standalone", "embedded"])
def test_either_projection_copy_must_preserve_nonnullable_units(contracts, copy):
    _, candidate, _, _ = contracts
    document = candidate["widget-projection.schema.json"]
    if copy == "embedded":
        document = candidate["openapi.json"]["components"]["schemas"][
            "WidgetProjection"
        ]
    document["$defs"]["ProjectedOutput"]["properties"]["unit"]["type"] = [
        "string",
        "null",
    ]
    assert any(
        "incompatible:" in issue and "unit" in issue for issue in compare(contracts)
    )


@pytest.mark.parametrize("required", [False, True])
def test_query_parameter_addition_depends_on_requiredness(contracts, required):
    _, candidate, _, _ = contracts
    operation(candidate)["parameters"].append(
        {
            "in": "query",
            "name": "view",
            "required": required,
            "schema": {"type": "string"},
        }
    )
    assert bool(compare(contracts)) is required


def test_candidate_consumer_semantics_cannot_replace_the_pin(contracts):
    _, _, _, candidate = contracts
    candidate["response"]["row_fields"][4]["semantic_id"] = "currency-converted"
    assert any(
        "incompatible:" in issue and "semantic_id" in issue
        for issue in compare(contracts)
    )


def test_widget_binding_changes_block_even_with_unchanged_schemas(contracts):
    _, candidate, _, _ = contracts
    candidate["widgets.json"][WIDGET]["data"]["dataKey"] = "other"
    assert any(
        "widgets.json" in issue and "dataKey" in issue for issue in compare(contracts)
    )


def test_unknown_keyword_change_blocks(contracts):
    _, candidate, _, _ = contracts
    candidate["input-snapshot.schema.json"]["x-unreviewed"] = True
    assert any(issue.startswith("unknown:") for issue in compare(contracts))


@pytest.mark.parametrize(
    ("before", "after", "compatible"),
    [
        (["a"], ["a", "b"], True),
        (["a", "b"], ["a"], False),
        (["a"], [True, "a"], True),
    ],
)
def test_input_enum_direction(contracts, before, after, compatible):
    baseline, candidate, _, _ = contracts
    for bundle, values in ((baseline, before), (candidate, after)):
        operation(bundle)["parameters"].append(
            {"in": "query", "name": "view", "schema": {"enum": values}}
        )
    assert (compare(contracts) == []) is compatible


@pytest.mark.parametrize(
    ("states", "compatible"),
    [
        (["verified", "withheld"], True),
        (["verified", "unverified", "withheld", "estimated"], False),
    ],
)
def test_status_enum_direction(contracts, states, compatible):
    _, candidate, _, _ = contracts
    for row in projection_rows(candidate):
        row["properties"]["status"]["enum"] = states
    assert (compare(contracts) == []) is compatible


@pytest.mark.parametrize("retained", [True, False])
def test_original_api_version_must_remain_bound(contracts, retained):
    _, candidate, _, _ = contracts
    servers = candidate["openapi.json"]["servers"]
    if not retained:
        servers.clear()
    servers.append({"url": "/modeling/v2"})
    assert (compare(contracts) == []) is retained


def method():
    return {
        "model_id": "model",
        "method_version": "1",
        "input_schema_id": "input",
        "input_schema_version": "1",
        "output_schema_id": "output",
        "output_schema_version": "1",
        "rule_set_version": "1",
        "reference_version": "1",
        "entity_types": ["company"],
        "period_types": ["annual"],
        "input_ids": [],
        "parameters": [],
        "rules": [],
        "outputs": [
            {
                "output_id": "cash-flow",
                "semantic_definition": "Cash flow",
                "unit": "USD",
                "value_type": "decimal",
                "required_input_ids": [],
                "required_check_ids": [],
                "required_output_ids": [],
            }
        ],
    }


@pytest.mark.parametrize("change", ["addition", "replaced", "units", "period", "rules"])
def test_method_and_rule_versions_are_immutable(contracts, change):
    baseline, candidate, _, _ = contracts
    baseline["descriptors.json"]["models"] = [method()]
    edited = method()
    candidate["descriptors.json"]["models"] = [edited]
    if change in {"addition", "replaced"}:
        edited["method_version"] = "2"
    if change == "addition":
        candidate["descriptors.json"]["models"].append(method())
    elif change == "units":
        edited["outputs"][0]["unit"] = "EUR"
    elif change == "period":
        edited["period_types"] = ["quarterly"]
    elif change == "rules":
        edited["rule_set_version"] = "2"
    assert (compare(contracts) == []) is (change == "addition")


@pytest.mark.parametrize(("closed", "compatible"), [(False, True), (True, False)])
def test_optional_output_addition_needs_open_schema_and_consumer(
    contracts, closed, compatible
):
    baseline, candidate, consumer, candidate_consumer = contracts
    for manifest in (consumer, candidate_consumer):
        manifest["response"]["closed"] = closed
    names = {field["name"] for field in consumer["response"]["row_fields"]}
    for bundle in (baseline, candidate):
        for row in projection_rows(bundle):
            row["additionalProperties"] = not closed
            del row["allOf"]
            if closed:
                row["properties"] = {name: row["properties"][name] for name in names}
                row["required"] = sorted(names)
    assert compare(contracts) == []
    for row in projection_rows(candidate):
        row["properties"]["extra"] = {"type": "string"}
    assert (compare(contracts) == []) is compatible


def test_unknown_change_in_output_conditions_blocks(contracts):
    _, candidate, _, _ = contracts
    row = candidate["widget-projection.schema.json"]["$defs"]["ProjectedOutput"]
    row["allOf"][-1]["if"]["properties"]["status"]["const"] = "unverified"
    assert any(
        issue.startswith("unknown:") and "allOf" in issue
        for issue in compare(contracts)
    )


def test_invalid_openapi_path_requiredness_blocks(contracts):
    _, candidate, _, _ = contracts
    endpoint = candidate["openapi.json"]["paths"]["/runs/{run_id}"]["get"]
    endpoint["parameters"][0]["required"] = False
    assert any("path/run_id/required" in issue for issue in compare(contracts))


def test_nested_schema_description_inside_condition_is_descriptive(contracts):
    _, candidate, _, _ = contracts
    row = candidate["widget-projection.schema.json"]["$defs"]["ProjectedOutput"]
    row["allOf"][-1]["then"]["properties"]["trace_ids"]["description"] = (
        "Source trace IDs"
    )
    assert compare(contracts) == []


def test_removing_safe_error_response_is_incompatible(contracts):
    _, candidate, _, _ = contracts
    del operation(candidate)["responses"]["422"]
    assert any(
        issue.startswith("incompatible:") and "/responses/422" in issue
        for issue in compare(contracts)
    )


def test_schema_financial_extension_requires_review(contracts):
    _, candidate, _, _ = contracts
    unit = candidate["widget-projection.schema.json"]["$defs"]["ProjectedOutput"][
        "properties"
    ]["unit"]
    unit["x-currency-basis"] = "constant-2025-USD"
    assert any(
        issue.startswith("unknown:") and "x-currency-basis" in issue
        for issue in compare(contracts)
    )


def test_compatible_wire_change_requires_matching_export_copies(contracts):
    _, candidate, _, _ = contracts
    schema = candidate["input-snapshot.schema.json"]
    schema["properties"]["optional_note"] = {"type": "string"}
    assert any(
        "embedded" in issue and "InputSnapshot" in issue for issue in compare(contracts)
    )


def test_method_must_validate_against_both_releases(contracts):
    _, candidate, _, _ = contracts
    candidate["descriptors.json"]["models"] = [method()]
    for schema in (
        candidate["model-descriptor.schema.json"],
        candidate["openapi.json"]["components"]["schemas"]["ModelDescriptor"],
    ):
        schema["$defs"]["OutputDescriptor"]["properties"]["value_type"]["enum"].remove(
            "decimal"
        )
    assert any("descriptors.json" in issue for issue in compare(contracts))


@pytest.mark.parametrize("edit", ["same", "rule", "rule_set"])
def test_new_method_preserves_reused_rule_and_rule_set_identities(contracts, edit):
    baseline, candidate, _, _ = contracts
    original = method()
    original["rules"] = [
        {
            "rule_id": "coverage",
            "version": "1",
            "stage": "precondition",
            "severity": "blocking",
            "exception_policy_version": None,
        }
    ]
    edited = deepcopy(original)
    edited["method_version"] = "2"
    if edit == "rule":
        edited["rule_set_version"] = "2"
        edited["rules"][0]["severity"] = "warning"
    elif edit == "rule_set":
        edited["rules"][0]["version"] = "2"
    baseline["descriptors.json"]["models"] = [original]
    candidate["descriptors.json"]["models"] = [original, edited]
    issues = compare(contracts)
    if edit == "rule":
        assert any("coverage/1/severity" in issue for issue in issues)
    elif edit == "rule_set":
        assert any("rule_set_version/1" in issue for issue in issues)
    else:
        assert issues == []


def test_closed_consumer_rejects_extra_fields_in_retained_projection(contracts):
    _, _, consumer, candidate_consumer = contracts
    for manifest in (consumer, candidate_consumer):
        manifest["response"]["closed"] = True
    issues = compare(contracts)
    assert any(
        "openapi.json" in issue and "closed consumer" in issue for issue in issues
    )
    assert any(
        "widget-projection.schema.json" in issue and "closed consumer" in issue
        for issue in issues
    )


def test_malformed_openapi_parameter_requiredness_blocks(contracts):
    _, candidate, _, _ = contracts
    operation(candidate)["parameters"][0]["required"] = "yes"
    assert any("query/run_id/required" in issue for issue in compare(contracts))


def test_widget_input_type_must_match_query_manifest(contracts):
    baseline, candidate, _, _ = contracts
    for bundle in (baseline, candidate):
        bundle["widgets.json"][WIDGET]["params"][0]["type"] = "number"
    assert any(
        "widgets.json" in issue and "run_id" in issue for issue in compare(contracts)
    )


@pytest.mark.parametrize("bad_version", [None, "", "  ", 2, True, ["2.0.0"]])
@pytest.mark.parametrize("side", [0, 1])
def test_openapi_info_version_is_required_nonempty_text(contracts, side, bad_version):
    info = contracts[side]["openapi.json"]["info"]
    if bad_version is None:
        del info["version"]
    else:
        info["version"] = bad_version
    assert any(
        issue.startswith("unknown:") and "info/version" in issue
        for issue in compare(contracts)
    )


def test_openapi_document_version_can_change_with_api_binding_retained(contracts):
    _, candidate, _, _ = contracts
    candidate["openapi.json"]["info"]["version"] = "1.1.0"
    assert compare(contracts) == []


@pytest.mark.parametrize("side", [0, 1])
@pytest.mark.parametrize("value", ["missing", None, True, [], 3])
@pytest.mark.parametrize(
    "location", ["info/title", "responses/200/description", "responses/422/description"]
)
def test_required_openapi_documentation_fields(contracts, side, value, location):
    bundle = contracts[side]
    if location.startswith("info"):
        document, field = bundle["openapi.json"]["info"], "title"
    else:
        document, field = (
            operation(bundle)["responses"][location.split("/")[1]],
            "description",
        )
    if value == "missing":
        del document[field]
    else:
        document[field] = value
    assert any(
        issue.startswith("unknown:") and location in issue
        for issue in compare(contracts)
    )


@pytest.mark.parametrize("copies_agree", [False, True])
def test_published_input_snapshot_agrees_with_evaluation_request(
    contracts, copies_agree
):
    _, candidate, _, _ = contracts
    components = candidate["openapi.json"]["components"]["schemas"]
    snapshots = [candidate["input-snapshot.schema.json"], components["InputSnapshot"]]
    if copies_agree:
        snapshots.extend(
            (
                candidate["evaluation-request.schema.json"]["$defs"]["InputSnapshot"],
                components["EvaluationRequest"]["$defs"]["InputSnapshot"],
            )
        )
    for schema in snapshots:
        schema["properties"]["optional_note"] = {"type": "string"}
    issues = compare(contracts)
    if copies_agree:
        assert issues == []
    else:
        assert any(
            "evaluation" in issue and "InputSnapshot" in issue for issue in issues
        )

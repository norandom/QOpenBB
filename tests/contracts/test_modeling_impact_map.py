import json
import subprocess
from pathlib import Path

import pytest
import tomllib
from qopenbb_ci.financial_impact_manifest import load_mapping, matches
from qopenbb_ci.financial_impact_map import select


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def commit(root):
    git(root, "add", ".")
    git(
        root,
        "-c",
        "user.name=Impact",
        "-c",
        "user.email=impact@example.test",
        "commit",
        "--quiet",
        "--allow-empty",
        "-m",
        "impact fixture",
    )
    return git(root, "rev-parse", "HEAD")


def write(root, path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


MAP = ".kiro/modeling-impact.toml"
MODEL = "services/data-api/qopenbb_data/modeling/models/factors/momentum.py"
OTHER = "services/data-api/qopenbb_data/modeling/models/factors/new.py"
API = "contracts/modeling/v1/openapi.json"
NODE = "tests/factors/test_example.py::test_calculation"
MAPPING = f"""
version = 1
[[mapping]]
ids = ["model:etf_momentum@1"]
criteria = ["5.1", "5.2"]
paths = ["{MODEL}"]
selectors = ["{NODE}"]

[[mapping]]
ids = ["operation:evaluateModel"]
criteria = ["5.3", "5.4"]
paths = ["{API}"]
selectors = ["tests/contracts/test_example.py::test_api"]
"""


def api(*ids):
    return json.dumps(
        {"paths": {f"/{name}": {"get": {"operationId": name}} for name in ids}}
    )


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "--quiet")
    write(tmp_path, MAP, MAPPING)
    write(tmp_path, MODEL, "method = 1\n")
    write(tmp_path, API, api("evaluateModel"))
    write(tmp_path, NODE.split("::")[0], "def test_calculation(): pass\n")
    write(tmp_path, "tests/contracts/test_example.py", "def test_api(): pass\n")
    return tmp_path, commit(tmp_path)


def test_selects_only_affected_nodes_and_reads_pinned_map(repo):
    root, base = repo
    write(root, MODEL, "method = 2\n")
    head = commit(root)
    write(root, MAP, "working tree can be dirty")
    assert select(base, head, root) == {
        "changed_ids": ["model:etf_momentum@1"],
        "criteria": ["5.1", "5.2"],
        "selectors": [NODE],
        "gaps": [],
        "affected_mappings": {
            "model:etf_momentum@1": {
                "criteria": ["5.1", "5.2"],
                "selectors": [NODE],
                "paths": [MODEL],
            },
        },
    }


def test_unrelated_change_has_no_impact(repo):
    root, base = repo
    write(root, "README.md", "unrelated")
    assert select(base, commit(root), root) == {
        "changed_ids": [],
        "criteria": [],
        "selectors": [],
        "gaps": [],
        "affected_mappings": {},
    }


def test_unmapped_model_and_renamed_operation_trigger_broader_checks(repo):
    root, base = repo
    write(root, OTHER, "method = 1\n")
    write(root, API, api("newOperation"))
    result = select(base, commit(root), root)
    assert result["changed_ids"] == [
        "operation:evaluateModel",
        "operation:newOperation",
    ]
    assert any(OTHER in gap for gap in result["gaps"])
    assert any("operation:newOperation" in gap for gap in result["gaps"])
    assert {"tests/factors", "tests/contracts/test_example.py::test_api"} <= set(
        result["selectors"]
    )


@pytest.mark.parametrize(
    "change",
    [
        lambda mapping: mapping.replace("version = 1", "version = true"),
        lambda mapping: mapping.replace('"5.1"', '"99.1"'),
        lambda mapping: mapping.replace("::test_calculation", "::test_missing"),
        lambda mapping: mapping.replace(MODEL, "../outside.py"),
        lambda mapping: mapping.replace(MODEL, MODEL + ".missing"),
        lambda mapping: mapping.replace(
            'selectors = ["' + NODE + '"]', "selectors = []"
        ),
    ],
)
def test_invalid_map_blocks_even_for_identical_revisions(repo, change):
    root, _ = repo
    write(root, MAP, change(MAPPING))
    head = commit(root)
    result = select(head, head, root)
    assert result["gaps"]
    assert "tests/factors" in result["selectors"]


def test_invalid_revision_blocks(repo):
    root, base = repo
    assert select(base, "--all", root)["gaps"]


def test_map_change_rechecks_all_mappings(repo):
    root, base = repo
    write(root, MAP, MAPPING + "\n# Mapping review\n")
    result = select(base, commit(root), root)
    assert result["gaps"] == []
    assert result["criteria"] == ["5.1", "5.2", "5.3", "5.4"]
    assert NODE in result["selectors"]


@pytest.mark.parametrize(
    "narrow",
    [
        lambda mapping: mapping.replace('"5.1", "5.2"', '"5.1"'),
        lambda mapping: mapping.replace("::test_calculation", "::test_retargeted"),
        lambda mapping: mapping.replace(MODEL, OTHER),
        lambda mapping: mapping.replace("model:etf_momentum@1", "model:replacement@1"),
    ],
)
def test_candidate_cannot_remove_base_obligations(repo, narrow):
    root, base = repo
    write(root, OTHER, "method = 2\n")
    write(
        root,
        NODE.split("::")[0],
        "def test_calculation(): pass\ndef test_retargeted(): pass\n",
    )
    write(root, MAP, narrow(MAPPING))
    result = select(base, commit(root), root)
    assert any("removed mapping obligation" in gap for gap in result["gaps"])
    assert "tests/factors" in result["selectors"]


def test_maintained_map_covers_source_descriptors():
    from qopenbb_data.modeling.models.factors.comparison import ProxyComparisonModel
    from qopenbb_data.modeling.models.factors.diagnostics import TimingStudyModel
    from qopenbb_data.modeling.models.factors.fcf_yield import FcfYieldModel
    from qopenbb_data.modeling.models.factors.momentum import MomentumModel
    from qopenbb_data.modeling.models.factors.real_yield import RealYieldModel
    from qopenbb_data.modeling.models.factors.volatility import VolatilityModel
    from qopenbb_data.modeling.service.bootstrap import installed_methods

    root = Path(__file__).resolve().parents[2]
    paths = set(
        git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(
            "\0"
        )
    )
    rows = load_mapping(paths, lambda path: (root / path).read_text(encoding="utf-8"))
    registry, _ = installed_methods()
    descriptors = [
        cls().describe()
        for cls in (
            MomentumModel,
            VolatilityModel,
            RealYieldModel,
            FcfYieldModel,
            ProxyComparisonModel,
            TimingStudyModel,
        )
    ] + list(registry.descriptors())
    for descriptor in descriptors:
        method = f"model:{descriptor.model_id}@{descriptor.method_version}"
        rules = {f"rule:{rule.rule_id}@{rule.version}" for rule in descriptor.rules}
        assert any({method, *rules}.issubset(row.ids) for row in rows)


@pytest.fixture(scope="module")
def maintained_repo(tmp_path_factory):
    root = Path(__file__).resolve().parents[2]
    repo = tmp_path_factory.mktemp("maintained_impact")
    git(repo, "init", "--quiet")
    rows = tomllib.loads((root / MAP).read_text(encoding="utf-8"))["mapping"]
    patterns = tuple(path for row in rows for path in row["paths"])
    selectors = {
        selector.split("::")[0] for row in rows for selector in row["selectors"]
    }
    for path in git(
        root, "ls-files", "--cached", "--others", "--exclude-standard", "-z"
    ).split("\0"):
        if path in selectors or (path and matches(path, patterns)):
            write(repo, path, (root / path).read_text(encoding="utf-8"))
    return repo, commit(repo)


@pytest.mark.parametrize(
    "dependency",
    [
        "services/data-api/qopenbb_data/modeling/models/factors/method_inputs.py",
        "services/data-api/qopenbb_data/modeling/models/factors/sessions.py",
        "services/data-api/qopenbb_data/modeling/contracts/common.py",
        "services/data-api/qopenbb_data/modeling/verification/reference.py",
        "tests/factors/fixtures/factor_inputs.py",
    ],
)
def test_shared_changes_select_numeric_checks_for_dependent_methods(
    maintained_repo, dependency
):
    root, base = maintained_repo
    git(root, "checkout", "--quiet", "--detach", base)
    path = root / dependency
    path.write_text(
        path.read_text(encoding="utf-8") + "\n# shared change\n", encoding="utf-8"
    )
    result = select(base, commit(root), root)
    assert result["gaps"] == []
    for model, rule, check in (
        (
            "etf_momentum",
            "momentum",
            "momentum.py::test_varying_prices_match_frozen_result_and_trace",
        ),
        (
            "etf_realized_volatility",
            "realized_volatility",
            "volatility.py::test_varying_prices_match_frozen_trace_and_sample_volatility",
        ),
        (
            "real_yield_regime",
            "regime",
            "real_yield.py::test_only_exact_endpoints_are_needed_and_match_frozen_trace",
        ),
        (
            "issuer_fcf_yield",
            "fcf_yield",
            "fcf_yield.py::test_frozen_issuer_yield_descriptor_and_trace",
        ),
        (
            "timing_study",
            "rising_hit_rate",
            "diagnostics.py::test_frozen_results_and_trace",
        ),
        (
            "proxy_comparison",
            "left_momentum",
            "comparison.py::test_ordered_comparison_and_reversed_pair",
        ),
    ):
        model_id, rule_id = f"model:{model}@1", f"rule:eligible_inputs.{rule}@1"
        assert {model_id, rule_id}.issubset(result["changed_ids"])
        for identity in (model_id, rule_id):
            assert (
                f"tests/factors/test_{check}"
                in result["affected_mappings"][identity]["selectors"]
            )


@pytest.mark.parametrize(
    ("path", "identity", "check"),
    [
        (
            "pipeline/qopenbb_ci/financial_impact.py",
            "capability:source-impact-gate",
            "tests/contracts/test_modeling_impact_gate.py::test_integration_preserves_selection_and_evidence",
        ),
        (
            "pipeline/qopenbb_ci/financial_impact_run_worker.py",
            "capability:source-impact-gate",
            "tests/contracts/test_modeling_impact_run.py::test_unevaluated_node_fails_even_when_pytest_exits_zero",
        ),
        (
            ".github/workflows/prototype.yml",
            "capability:source-impact-gate",
            "tests/delivery/test_prototype_workflow.py::test_release_trigger_checkout_and_unique_build_identity",
        ),
        (
            "sources.lock.json",
            "capability:modeling-source-runtime",
            "tests/delivery/test_data_image.py::test_staged_modeling_modules_are_importable",
        ),
    ],
)
def test_integration_inputs_select_source_checks(
    maintained_repo, path, identity, check
):
    root, base = maintained_repo
    git(root, "checkout", "--quiet", "--detach", base)
    target = root / path
    target.write_bytes(target.read_bytes() + b"\n")
    result = select(base, commit(root), root)
    assert result["gaps"] == []
    assert identity in result["changed_ids"]
    assert check in result["affected_mappings"][identity]["selectors"]
    assert not any("test_data_runtime_image" in node for node in result["selectors"])


def test_descriptor_discovery_reports_model_and_rule_changes(repo):
    root, base = repo
    path = "contracts/modeling/v1/descriptors.json"
    old = {
        "model_id": "etf_momentum",
        "method_version": "1",
        "rules": [{"rule_id": "eligible_inputs.momentum", "version": "1"}],
    }
    write(root, path, json.dumps({"models": [old]}))
    write(
        root,
        MAP,
        MAPPING.replace(
            '"model:etf_momentum@1"',
            '"model:etf_momentum@1", "rule:eligible_inputs.momentum@1"',
        ),
    )
    base = commit(root)
    new = old | {"rules": [{"rule_id": "eligible_inputs.momentum", "version": "2"}]}
    write(root, path, json.dumps({"models": [new]}))
    result = select(base, commit(root), root)
    assert result["changed_ids"] == [
        "model:etf_momentum@1",
        "rule:eligible_inputs.momentum@1",
        "rule:eligible_inputs.momentum@2",
    ]
    assert (
        "unmapped contract identity: rule:eligible_inputs.momentum@2" in result["gaps"]
    )
    assert (
        NODE
        in result["affected_mappings"]["rule:eligible_inputs.momentum@1"]["selectors"]
    )

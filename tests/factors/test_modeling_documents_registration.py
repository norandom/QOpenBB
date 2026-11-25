import asyncio

from qopenbb_ci.modeling_documents import documents
from qopenbb_data.modeling.contracts.checks import RuleDescriptor
from qopenbb_data.modeling.service import bootstrap
from qopenbb_data.modeling.service.execution import ExecutionLimits
from qopenbb_data.modeling.service.orchestrator import MethodBinding
from test_model_http import Verifier, call
from test_model_registry import SuppliedValueFixture


def measure_dimensions(inputs, assumptions):
    return 1, 1


def test_export_and_listener_share_installed_methods_and_rule_descriptors(
    monkeypatch, tmp_path
):
    method = SuppliedValueFixture()
    rule = RuleDescriptor(
        rule_id="coverage",
        version="2",
        stage="postcondition",
        severity="blocking",
    )
    method.descriptor = method.descriptor.model_copy(update={"rules": (rule,)})
    binding = MethodBinding(
        ExecutionLimits(1, 1, 1, measure_dimensions=measure_dimensions)
    )
    monkeypatch.setattr(bootstrap, "_INSTALLED_METHODS", ((method, binding),))
    monkeypatch.setattr(bootstrap.IdentityVerifier, "from_env", Verifier)
    monkeypatch.setenv("QOPENBB_MODEL_RUN_DIR", str(tmp_path))
    app = bootstrap.create_app()
    status, payload = asyncio.run(call(app, "/modeling/v1/models"))
    assert status == 200
    assert payload == documents()["descriptors.json"]
    assert payload["models"][0]["rules"] == [rule.model_dump(mode="json")]

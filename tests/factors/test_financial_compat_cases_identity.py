"""Exercise runtime source binding with the same exported contract bytes."""

from functools import partial

import pytest
import test_financial_compat_cases as cases
from test_modeling_bundle import source_repo as source_repo_fixture

source_repo = source_repo_fixture


def test_unchanged_export_cannot_bind_drifted_runtime(
    source_repo, tmp_path, monkeypatch
):
    module, revision, consumer, checkout = source_repo
    candidate = tmp_path / "candidate"
    expected = module._expected("check", revision, consumer)
    module._bundle("write", candidate, expected)
    monkeypatch.setattr(cases, "ROOT", checkout)
    monkeypatch.setattr(
        cases,
        "_verify_source",
        partial(module._verify_source, root=checkout),
        raising=False,
    )
    cases.verify_candidate_for_exercise(candidate, consumer)

    route = checkout / module.DATA_API / "modeling/service/http.py"
    route.parent.mkdir(parents=True)
    route.write_text("# A runtime-only module absent from the candidate source.\n")
    assert (
        module.main(
            [
                "check",
                "--revision",
                revision,
                "--output",
                str(candidate),
                "--consumer",
                str(consumer),
            ]
        )
        == 0
    )
    with pytest.raises(
        ValueError, match="source input differs from revision: .*http.py"
    ):
        cases.verify_candidate_for_exercise(candidate, consumer)

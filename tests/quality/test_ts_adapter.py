"""The subprocess response is validated before any record reaches the gate."""

import copy
from types import SimpleNamespace

import pytest


VALID = [{"path": "/fixture.ts", "logical": 2,
          "functions": [{"name": "f", "line": 1, "column": 9, "logical": 1}]}]


@pytest.mark.parametrize("mutate", [
    lambda rows: rows.clear(),
    lambda rows: rows.append(copy.deepcopy(rows[0])),
    lambda rows: rows[0].update(path="/unexpected.ts"),
    lambda rows: rows[0].pop("functions"),
    lambda rows: rows[0].update(logical=True),
    lambda rows: rows[0].update(logical=-1),
    lambda rows: rows[0].update(logical=1.5),
    lambda rows: rows[0].update(functions={}),
    lambda rows: rows[0]["functions"][0].update(line=0),
    lambda rows: rows[0]["functions"][0].update(column=False),
    lambda rows: rows[0]["functions"][0].update(logical=-1),
    lambda rows: rows[0]["functions"][0].update(name=None),
    lambda rows: rows[0]["functions"][0].pop("column"),
])
def test_invalid_parser_records_are_rejected(mutate):
    from tools.quality.ts_adapter import validate_records

    rows = copy.deepcopy(VALID)
    mutate(rows)
    with pytest.raises(ValueError, match="parser"):
        validate_records(rows, ["/fixture.ts"])


def test_valid_parser_records_and_empty_input():
    from tools.quality.ts_adapter import validate_records

    assert validate_records(VALID, ["/fixture.ts"]) == {"/fixture.ts": VALID[0]}
    assert validate_records([], []) == {}
    with pytest.raises(ValueError, match="parser"):
        validate_records({}, [])
    with pytest.raises(ValueError, match="parser"):
        validate_records(VALID, ["/fixture.ts", "/fixture.ts"])


@pytest.mark.parametrize("result", [
    SimpleNamespace(returncode=2, stdout='[{"path":"partial.ts"}]', stderr="fixture.ts: syntax failed"),
    SimpleNamespace(returncode=0, stdout="not JSON", stderr=""),
])
def test_parser_process_failures_reject_partial_output(monkeypatch, result):
    from tools.quality import ts_adapter

    monkeypatch.setattr(ts_adapter, "runtime", lambda: ("node", {"node": "24.22.1", "typescript": "6.0.3"}))
    monkeypatch.setattr(ts_adapter, "execute", lambda *args, **kwargs: result)
    with pytest.raises(ValueError, match="parser"):
        ts_adapter.measure_typescript(["/fixture.ts"])


def test_wrong_node_version_fails_before_parsing(monkeypatch):
    from tools.quality import ts_adapter

    monkeypatch.setattr(ts_adapter, "execute", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout="v22.0.0\n", stderr=""))
    with pytest.raises(ValueError, match="Node.*24.22.1"):
        ts_adapter.runtime()

"""Python metric boundary and syntax fixtures."""

import pytest

@pytest.mark.parametrize("size", [400, 401])
def test_physical_boundary(size):
    from tools.quality.complexity import physical_lines, violations

    item = {"path": "fixture.py", "physical": physical_lines("# x\n" * size), "functions": []}
    assert bool(violations(item, LIMITS)) == (size == 401)


LIMITS = {"physical": 400, "logical": 300, "function": 50}


@pytest.mark.parametrize("size", [300, 301])
def test_python_file_boundary(size):
    from tools.quality.complexity import violations
    from tools.quality.python_units import measure_python

    assert bool(violations(measure_python("x=1;" * size), LIMITS)) == (size == 301)


@pytest.mark.parametrize("size", [50, 51])
def test_python_function_boundary(size):
    from tools.quality.complexity import violations
    from tools.quality.python_units import measure_python

    item = measure_python("async def f():\n" + " x=1\n" * size)
    assert item["functions"][0]["logical"] == size
    assert bool(violations(item, LIMITS)) == (size == 51)


def test_docstrings_nested_bodies_and_lambda():
    from tools.quality.python_units import measure_python

    source = ('"module docs"\n# comment\ndef outer():\n "docs"\n'
              ' def inner():\n  "docs"\n  a()\n  b()\n'
              ' class Nested:\n  def method(self):\n   c()\n'
              ' "not a docstring"\n return lambda: (lambda: 42)\n')
    item = measure_python(source)
    assert item["logical"] == 11
    assert [(f["name"], f["logical"]) for f in item["functions"]] == [
        ("outer", 5), ("inner", 2), ("method", 1), ("<lambda>", 1), ("<lambda>", 1)]


@pytest.mark.parametrize("source, expected", [
    ("", 0), ("a\r\nb\rc\n", 3), ("a\n\n", 2),
    ("x=1\f\v\u2028\u2029\n", 1), ("a", 1)])
def test_physical_newlines(source, expected):
    from tools.quality.complexity import physical_lines

    assert physical_lines(source) == expected


def test_invalid_python_rejected():
    from tools.quality.python_units import measure_python

    with pytest.raises(SyntaxError):
        measure_python("def broken(")

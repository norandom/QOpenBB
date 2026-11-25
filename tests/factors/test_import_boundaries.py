import ast
from importlib.util import resolve_name
from pathlib import Path

import pytest

DOMAIN = Path(__file__).resolve().parents[2] / "services/data-api/qopenbb_data/modeling"
PACKAGE = "qopenbb_data.modeling"
LAYERS = ("contracts", "models", "validation", "verification")
DOMAIN_DEPENDENCIES = {
    "__future__", "abc", "bisect", "calendar", "collections", "copy", "dataclasses",
    "datetime", "decimal", "enum", "fractions", "functools", "graphlib", "hashlib", "itertools",
    "json", "math", "numbers", "operator", "polars", "pydantic", "re", "statistics",
    "types", "typing", "uuid", "zoneinfo",
}


def imported_names(tree, package):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom):
            source = "." * node.level + (node.module or "")
            try:
                module = resolve_name(source, package)
            except ImportError:
                module = source
            for alias in node.names:
                yield node.lineno, f"{module}.{alias.name}"


def boundary_violations(root):
    initializer = root / "__init__.py"
    paths = [initializer] if initializer.is_file() else []
    for layer in LAYERS:
        paths.extend((root / layer).rglob("*.py"))

    violations = []
    for path in sorted(paths):
        relative = path.relative_to(root)
        package = ".".join((PACKAGE, *relative.parent.parts))
        # Contracts and the package initializer cannot re-export production formulas.
        allowed_layers = {"contracts", relative.parts[0]} & set(LAYERS)
        allowed_prefixes = {f"{PACKAGE}.{layer}" for layer in allowed_layers}
        if relative.parts[0] == "validation":
            allowed_prefixes.add(f"{PACKAGE}.models.protocol")
        if relative.as_posix() == "validation/lifecycle.py":
            allowed_prefixes.add(f"{PACKAGE}.verification.reference")
        if relative.as_posix() == "verification/reference.py":
            allowed_prefixes.update({
                f"{PACKAGE}.validation.outputs.ordered_outputs",
                f"{PACKAGE}.validation.tolerance.within_tolerance",
            })
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for line, name in imported_names(tree, package):
            if name.partition(".")[0] in DOMAIN_DEPENDENCIES:
                continue
            if any(name == prefix or name.startswith(prefix + ".") for prefix in allowed_prefixes):
                continue
            violations.append(f"{relative.as_posix()}:{line}: {name}")
    return violations


def test_production_modeling_import_boundaries():
    for package in (DOMAIN, *(DOMAIN / layer for layer in LAYERS)):
        assert (package / "__init__.py").is_file(), package
    violations = boundary_violations(DOMAIN)
    assert not violations, "\n".join(violations)


@pytest.mark.parametrize("layer", LAYERS)
@pytest.mark.parametrize(("statement", "dependency"), [
    pytest.param("import httpx as client", "httpx", id="http"),
    pytest.param("from openbb_fmp import utils", "openbb_fmp.utils", id="provider"),
    pytest.param("from openbb_platform import api", "openbb_platform.api", id="openbb"),
    pytest.param("from openbb_platform_api import auth", "openbb_platform_api.auth", id="workspace"),
    pytest.param("import sqlite3", "sqlite3", id="storage"),
    pytest.param("from ... import config", "qopenbb_data.config", id="credentials"),
    pytest.param("from os import environ", "os.environ", id="environment"),
    pytest.param("from ..service import run_store", "qopenbb_data.modeling.service.run_store",
                 id="run-store"),
])
def test_domain_layers_reject_adapter_imports(tmp_path, layer, statement, dependency):
    path = tmp_path / layer / "example.py"
    path.parent.mkdir()
    path.write_text(statement, encoding="utf-8")
    assert boundary_violations(tmp_path) == [f"{layer}/example.py:1: {dependency}"]


@pytest.mark.parametrize("statement", [
    "import qopenbb_data.modeling.models.factors.momentum as formula",
    "from qopenbb_data.modeling.models.factors import momentum",
    "from ...models.factors import momentum",
    "from ... import models",
])
def test_references_reject_production_formula_imports(tmp_path, statement):
    path = tmp_path / "verification/factors/reference.py"
    path.parent.mkdir(parents=True)
    path.write_text(statement, encoding="utf-8")
    findings = boundary_violations(tmp_path)
    assert len(findings) == 1
    assert findings[0].startswith(f"verification/factors/reference.py:1: {PACKAGE}.models")


@pytest.mark.parametrize("module", ["__init__.py", "contracts/__init__.py"])
def test_shared_packages_cannot_reexport_production_formulas(tmp_path, module):
    path = tmp_path / module
    path.parent.mkdir(exist_ok=True)
    path.write_text(f"from {PACKAGE}.models.factors import momentum\n", encoding="utf-8")
    assert boundary_violations(tmp_path) == [f"{module}:1: {PACKAGE}.models.factors.momentum"]


def test_references_accept_shared_contracts_and_numerical_dependencies(tmp_path):
    path = tmp_path / "verification/factors/reference.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "from decimal import Decimal\n"
        "import polars as pl\n"
        "from pydantic import BaseModel\n"
        "from ...contracts import inputs\n"
        "from . import scalar\n",
        encoding="utf-8",
    )
    assert not boundary_violations(tmp_path)

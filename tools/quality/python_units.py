"""CPython AST implementation of project-syntax-units-v1 (Python 3.13)."""

import ast


CALLABLES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
BOUNDARIES = (*CALLABLES, ast.ClassDef)


def measure_python(source: str, path: str = "fixture.py") -> dict:
    tree = ast.parse(source, filename=path)
    docs = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(node, (ast.Module, ast.ClassDef, *CALLABLES[:2])) and body:
            first = body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                if isinstance(first.value.value, str):
                    docs.add(id(first))

    def count(node: ast.AST, own: bool = False) -> int:
        value = int((isinstance(node, ast.stmt) and id(node) not in docs)
                    or isinstance(node, ast.Lambda))
        if own and isinstance(node, BOUNDARIES):
            return value
        return value + sum(count(child, own) for child in ast.iter_child_nodes(node))

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, CALLABLES):
            logical = (1 if isinstance(node, ast.Lambda)
                       else sum(count(child, True) for child in node.body))
            functions.append({"name": getattr(node, "name", "<lambda>"),
                              "line": node.lineno, "column": node.col_offset + 1,
                              "logical": logical})
    return {"path": path, "logical": count(tree), "functions": functions}

"""Validate impact ownership and exact pytest entry points against the candidate tree."""

import ast
import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from glob import translate

import tomllib

MAP_PATH = ".kiro/modeling-impact.toml"
_CRITERION = re.compile(r"(?:1\.[1-4]|2\.[1-7]|3\.[1-6]|4\.[1-5]|5\.[1-4]|6\.[1-5])")
_IDENTITY = re.compile(
    r"(?:(?:model|rule):[\w.-]+@[\w.-]+|(?:operation|widget|consumer|capability):[\w.-]+)",
    re.ASCII,
)
_PATH = re.compile(r"[\w./*-]+", re.ASCII)
_NODE = re.compile(r"(tests/[^:]+/test_[\w]+\.py)::(test_[\w]+)", re.ASCII)


@dataclass(frozen=True)
class Mapping:
    ids: tuple[str, ...]
    criteria: tuple[str, ...]
    paths: tuple[str, ...]
    selectors: tuple[str, ...]

    def preserves(self, identity: str, base: "Mapping") -> bool:
        return (
            identity in self.ids
            and set(base.criteria).issubset(self.criteria)
            and set(base.paths).issubset(self.paths)
            and set(base.selectors).issubset(self.selectors)
        )


@lru_cache(maxsize=256)
def _path_pattern(pattern: str) -> re.Pattern:
    return re.compile(translate(pattern, recursive=True, include_hidden=True, seps="/"))


def matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(_path_pattern(pattern).fullmatch(path) for pattern in patterns)


def _values(row: dict, key: str, pattern: re.Pattern | None = None) -> tuple[str, ...]:
    values = row[key]
    if (
        not isinstance(values, list)
        or not values
        or any(
            not isinstance(value, str)
            or not value
            or (pattern and not pattern.fullmatch(value))
            for value in values
        )
    ):
        raise ValueError(f"invalid mapping {key}")
    if len(set(values)) != len(values):
        raise ValueError(f"duplicate mapping {key}")
    return tuple(values)


def _path_is_safe(path: str) -> bool:
    return all(part not in {"", ".", ".."} for part in path.split("/"))


def _validate_selector(
    selector: str, paths: set[str], read: Callable, cache: dict
) -> None:
    match = _NODE.fullmatch(selector)
    if match is None:
        raise ValueError(f"invalid pytest node: {selector}")
    path, name = match.groups()
    if not _path_is_safe(path) or path not in paths:
        raise ValueError(f"missing pytest file: {path}")
    if path not in cache:
        try:
            cache[path] = {
                node.name
                for node in ast.parse(read(path)).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
        except SyntaxError as exc:
            raise ValueError(f"invalid pytest source: {path}") from exc
    if name not in cache[path]:
        raise ValueError(f"missing pytest node: {selector}")


def load_mapping(paths: set[str], read: Callable[[str], str]) -> list[Mapping]:
    if MAP_PATH not in paths:
        raise ValueError(f"missing impact map: {MAP_PATH}")
    try:
        document = tomllib.loads(read(MAP_PATH))
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f"invalid TOML: {MAP_PATH}") from exc
    if (
        document.keys() != {"version", "mapping"}
        or type(document["version"]) is not int
        or document["version"] != 1
        or not isinstance(document["mapping"], list)
        or not document["mapping"]
    ):
        raise ValueError("invalid impact map schema")
    result = []
    cache: dict[str, set[str]] = {}
    for record in document["mapping"]:
        if not isinstance(record, dict) or record.keys() != {
            "ids",
            "criteria",
            "paths",
            "selectors",
        }:
            raise ValueError("invalid impact map row")
        row = Mapping(
            _values(record, "ids", _IDENTITY),
            _values(record, "criteria", _CRITERION),
            _values(record, "paths", _PATH),
            _values(record, "selectors"),
        )
        for pattern in row.paths:
            if not _path_is_safe(pattern) or pattern.startswith("*"):
                raise ValueError(f"unsafe mapped path: {pattern}")
            if not any(matches(path, (pattern,)) for path in paths):
                raise ValueError(f"stale mapped path: {pattern}")
        for selector in row.selectors:
            _validate_selector(selector, paths, read, cache)
        if row in result:
            raise ValueError("duplicate impact map row")
        result.append(row)
    return result

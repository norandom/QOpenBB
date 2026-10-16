"""Export public JSON schemas from the authoritative Python boundary models."""

import argparse
import json
from pathlib import Path

from .contracts import Acceptance, Backup, ExpectedContext, Release
from .source_contract import SourceLock


MODELS = {"source": SourceLock, "release": Release, "acceptance": Acceptance,
          "backup": Backup, "expected": ExpectedContext}


def schema_text(model: type[SourceLock | Release | Acceptance | Backup | ExpectedContext]) -> str:
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", **model.model_json_schema()}
    return json.dumps(schema, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name, model in MODELS.items():
        (args.output / f"{name}.schema.json").write_text(schema_text(model), encoding="utf-8")


if __name__ == "__main__":
    main()

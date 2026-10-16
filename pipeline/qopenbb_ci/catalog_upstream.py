"""Execute unchanged upstream widget utilities using the image's installed core."""
import importlib
import json
from pathlib import Path
import sys
import types


def main() -> None:
    # A namespace loads only the two accepted utilities, without launcher extras.
    package = types.ModuleType("qopenbb_upstream")
    package.__path__ = ["/generator"]
    sys.modules[package.__name__] = package
    module = importlib.import_module("qopenbb_upstream.widgets")
    schema = json.loads(Path("/input/schema.json").read_text())
    result = module.build_json(schema, [])
    print("QOPENBB_CATALOG=" + json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()

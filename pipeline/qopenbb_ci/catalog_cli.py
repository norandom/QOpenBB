"""Generate canonical consumer proposals without builds, publication or Excel."""
import argparse
import hashlib
import json
from pathlib import Path

from qopenbb_ci.catalog import canonical, compatibility, digest, freeze_routes, generate
from qopenbb_ci.catalog_runtime import ASSET, capture_schema, upstream_widgets, verified_sources


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--image", required=True)
    result.add_argument("--source", required=True, type=Path)
    result.add_argument("--source-lock", required=True, type=Path)
    result.add_argument("--inventory", required=True, type=Path)
    result.add_argument("--previous-routes", type=Path)
    result.add_argument("--allow-contract-change", action="store_true",
                        help="Write review proposals despite drift; never accepts downstream evidence")
    result.add_argument("--public-prefix", default="/data")
    result.add_argument("--output", required=True, type=Path)
    result.add_argument("--work", required=True, type=Path)
    return result


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(args: argparse.Namespace) -> dict:
    revision = read(args.source_lock)["data_api"]["revision"]
    provenance = verified_sources(args.source, revision)
    schema, identity = capture_schema(args.image)
    if identity["Config"]["Labels"].get("org.qopenbb.source.data_api") != revision:
        raise ValueError("image/source revision mismatch")
    inventory = read(args.inventory)
    freeze_routes(schema, inventory)
    args.work.mkdir(parents=True, exist_ok=True)
    raw = upstream_widgets(args.image, args.source, schema, inventory, args.work)
    outputs = generate(schema, inventory, raw, read(args.source / ASSET), args.public_prefix)
    second = upstream_widgets(args.image, args.source, schema, inventory, args.work)
    if canonical(outputs) != canonical(generate(schema, inventory, second, read(args.source / ASSET), args.public_prefix)):
        raise ValueError("upstream generation is not deterministic")
    prior = read(args.previous_routes) if args.previous_routes else None
    outputs["compatibility.json"] = compatibility(prior, outputs["routes.json"])
    outputs["provenance.json"] = {**provenance, "image": args.image, "image_labels": identity["Config"]["Labels"],
                                  "inventory_sha256": digest(inventory), "repeat_identical": True,
                                  "maintained_generator_sha256": generator_hashes()}
    hashes = {name: digest(value) for name, value in outputs.items()}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, value in {**outputs, "hashes.json": hashes}.items():
        (args.output / name).write_bytes(canonical(value))
    return {"output": str(args.output), "hashes": hashes,
            "requires_revalidation": outputs["compatibility.json"]["requires_revalidation"]}


def generator_hashes() -> dict:
    return {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ("catalog.py", "catalog_runtime.py", "catalog_upstream.py", "catalog_cli.py")}


def main() -> int:
    args = parser().parse_args()
    try:
        report = run(args)
        print(json.dumps(report, sort_keys=True))
        if report["requires_revalidation"] and not args.allow_contract_change:
            return 2
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

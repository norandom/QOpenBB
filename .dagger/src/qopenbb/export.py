"""SDK build/export entry point; no tests, publication or deployment."""

import argparse
import asyncio
import json
from pathlib import Path

import dagger
from dagger import dag

from qopenbb.images import build


async def export(args: argparse.Namespace) -> None:
    provenance = json.loads((args.stage / 'provenance.json').read_text())
    async with dagger.Connection():
        context = dag.host().directory(str(args.stage))
        image = build(args.service, context, args.base, provenance)
        await image.export(str(args.archive), media_types=dagger.ImageMediaTypes.DockerMediaTypes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--service', required=True)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--base', required=True)
    parser.add_argument('--archive', type=Path, required=True)
    asyncio.run(export(parser.parse_args()))


if __name__ == '__main__':
    main()

"""Export the independently staged Modeling runtime using the Dagger SDK."""

import argparse
import asyncio
import json
from pathlib import Path

import dagger
from dagger import dag

from qopenbb.modeling import modeling_image


async def export(stage: Path, archive: Path) -> None:
    manifest = json.loads((stage / 'inputs.json').read_bytes())
    async with dagger.Connection():
        await dag.version()
        image = modeling_image(dag.host().directory(str(stage)), manifest['base'], manifest['runtime_inputs'])
        await image.export(str(archive), media_types=dagger.ImageMediaTypes.DockerMediaTypes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    asyncio.run(export(args.stage.resolve(), args.archive.resolve()))


if __name__ == '__main__':
    main()

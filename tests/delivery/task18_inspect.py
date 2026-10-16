"""Task-local evidence checks; all archive/layer inspection runs outside Dagger."""

import argparse
import json
from pathlib import Path
from pathlib import PurePosixPath

from qopenbb_ci.images import inspect_archive
from qopenbb_ci.staging import verify_stage
from qopenbb_ci.source_filter import source_namespace_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    provenance = verify_stage(args.stage)
    sentinel = b'SYNTHETIC_TASK18_SECRET_4e71'
    count = 0
    for path in args.stage.rglob('*'):
        if path.is_file():
            assert sentinel not in path.read_bytes(), path
            count += 1
    expected = [
        'sources/workspace/terminalpro/src/lib/state/main.json',
        'sources/workspace/terminalpro/public/assets/data/indices_fmp.json',
        'sources/workspace/terminalpro/public/assets/data/tickers_fmp.json',
    ]
    # Source names are checked against the locked inventory, not assumed by directory labels.
    for path in expected:
        assert (args.stage / path).is_file(), path
    result = inspect_archive(args.archive, sentinel)
    preserved = {key: [name for name in source['files']
                       if source_namespace_index(PurePosixPath(name)) is not None]
                 for key, source in provenance['sources'].items()}
    assert {key: len(names) for key, names in preserved.items()} == {'workspace': 32, 'data_api': 7}
    result['preserved_source_namespaces'] = preserved
    result['staged_files'] = count
    result['source_revisions'] = {key: value['revision'] for key, value in provenance['sources'].items()}
    result['sentinel_absent_from_stage_metadata_and_all_layers'] = True
    args.output.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()

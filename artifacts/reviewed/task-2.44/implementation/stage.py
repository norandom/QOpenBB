"""Snapshot current source and owned tests into the isolated accepted runtime."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
SOURCE = ROOT / 'vendor/workspace/terminalpro'
STAGE = Path('/home/mc/qopenbb-work/task244-20261017140641/terminalpro')
OUTPUT = ROOT / 'artifacts/task-2.44/implementation'
FOLDERS = [
    'src/components/General/Table/Chart',
    'tests/unit/chart-application',
    'tests/unit/chart-compatibility',
    'tests/e2e/chart-compatibility',
]
FILES = ['biome.json', 'tsconfig.json', 'package.json', 'package-lock.json']
SIBLING_PENDING = {
    'src/components/General/Table/Chart/application/appearanceComposition.ts',
    'src/components/General/Table/Chart/application/appearanceColors.ts',
    'tests/unit/chart-application/appearanceComposition.test.ts',
    'tests/unit/chart-application/appearanceColors.test.ts',
}

def snapshot(label):
    entries = []
    # These sibling-lane files were absent at accepted task 2.41. The join owns them.
    for relative in SIBLING_PENDING:
        (STAGE / relative).unlink(missing_ok=True)
    for folder in FOLDERS:
        for source in sorted((SOURCE / folder).rglob('*')):
            if source.is_file():
                relative = source.relative_to(SOURCE)
                if relative.as_posix() in SIBLING_PENDING:
                    continue
                target = STAGE / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                entries.append({'path': str(relative), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    for relative in FILES:
        source = SOURCE / relative
        if source.exists():
            shutil.copyfile(source, STAGE / relative)
            entries.append({'path': relative, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    for entry in entries:
        assert hashlib.sha256((STAGE / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    (OUTPUT / f'{label}-stage-manifest.json').write_text(json.dumps({'stage': str(STAGE), 'files': entries}, indent=2) + '\n')

if __name__ == '__main__':
    import sys
    snapshot(sys.argv[1])

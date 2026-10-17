from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[2]
for name in ('complexity.json','workspace-changes.json','data-api-changes.json','owned-source-hashes.json'):
 shutil.copyfile(root/'artifacts/grid-capture-implementation'/name, root/'artifacts/task-2.40'/name)

import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))
from tools.quality.complexity import physical_lines
from tools.quality.python_units import measure_python

out = Path(__file__).parent
workspace = root / 'vendor/workspace'
base = '693954f43aac8af888cfe6e7bfed6d9dcb72d2f5'
key = 'vendor/workspace/backend-api/backend/api/crud.py'
old = subprocess.check_output(['git', '-C', str(workspace), 'show', base + ':backend-api/backend/api/crud.py'], text=True)
new = (root / key).read_text()
expected = old.replace('func.concat(User.first_name, " ", User.last_name)', 'User.first_name + " " + User.last_name')
expected = expected.replace(').where(DashboardItem.uuid.in_(shared_uuids))', ').join(User, User.uuid == DashboardItem.creator_uuid).where(DashboardItem.uuid.in_(shared_uuids))')
assert expected == new
red = json.loads((out.parent / 'red-final.json').read_text())
green = json.loads((out / 'fresh.json').read_text())
assert red['exit'] == 1 and green['exit'] == 0
assert red['distributions'] == green['distributions']
assert red['sqlite'] == green['sqlite'] and red['python'] == green['python']
assert {k: v for k, v in red['sources'].items() if k != key} == {k: v for k, v in green['sources'].items() if k != key}
assert hashlib.sha256(old.encode()).hexdigest() == red['sources'][key]
for name, digest in green['sources'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
baseline_format = subprocess.run([sys.executable, '-m', 'ruff', 'format', '--check', '--stdin-filename', str(root / key), '-'], input=old, text=True, capture_output=True)
(out / 'baseline-format.log').write_text(baseline_format.stdout + baseline_format.stderr)
record = {'exact_seven_sites': True, 'runtime_and_test_manifests_identical': True, 'current_manifest_matches': True, 'baseline_format_exit': baseline_format.returncode, 'sizes': {}}
for label, text in [('baseline', old), ('patched', new)]:
    units = measure_python(text, key)
    record['sizes'][label] = {'physical': physical_lines(text), 'logical': units['logical'], 'max_function': max(f['logical'] for f in units['functions']), 'sha256': hashlib.sha256(text.encode()).hexdigest()}
assert baseline_format.returncode == 1
(out / 'independent.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))

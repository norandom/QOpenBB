import json
from pathlib import Path
import subprocess
import sys

out = Path(__file__).parent
success = (out / 'tests-final.log').read_text()
success_path = Path(success.split('Removed sandbox: ')[1].strip())
assert not success_path.exists()
command = [sys.executable, '/mnt/d/Source/QOpenBB/vendor/workspace/backend-api/backend/tests_sqlite/run.py', '-k', 'review_cleanup_no_matching_test']
result = subprocess.run(command, text=True, capture_output=True)
(out / 'cleanup-nonzero.log').write_text(result.stdout + result.stderr)
assert result.returncode == 5
nonzero_path = Path(result.stdout.split('Removed sandbox: ')[1].strip())
assert not nonzero_path.exists()
prior = [Path(f'/tmp/pytest-of-mc/pytest-{i}/test_real_fixture_roundtrip0/workspace.db') for i in range(3)]
assert all(not path.exists() for path in prior)
record = {'success_path': str(success_path), 'success_removed': True, 'nonzero_command': command, 'nonzero_exit': result.returncode, 'nonzero_path': str(nonzero_path), 'nonzero_removed': True, 'prior_database_paths_absent': [str(path) for path in prior]}
(out / 'cleanup.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))

from pathlib import Path
import importlib.util
import json
import os
import pytest

@pytest.mark.fixture
@pytest.mark.parametrize('case', range(4))
def test_synthetic_provider_observation(tmp_path, case):
    datum = json.loads(Path('tests/providers/fixtures/observation.json').read_text())
    assert (datum['value'], datum['unit'], datum['provider']) == (123.45, 'USD', 'synthetic')
    worker = os.environ.get('PYTEST_XDIST_WORKER', 'master')
    assert worker in ('master', 'gw0', 'gw1')
    (tmp_path / 'worker.json').write_text(json.dumps({'worker': worker, 'case': case}))

@pytest.mark.fixture
@pytest.mark.parametrize('workers', [-1, 3, 100])
def test_runner_refuses_unbounded_workers(workers):
    spec = importlib.util.spec_from_file_location('verification_runner', 'verification/runner.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match='workers'):
        module.run_pytest(['tests/delivery/test_verification.py'], workers)

@pytest.mark.live
def test_live_provider_requires_separate_authorization():
    pytest.skip('live provider acceptance is unverified; no credentials loaded')

@pytest.mark.fixture
def test_failed_python_evidence_discards_exception_and_stdout(tmp_path):
    spec = importlib.util.spec_from_file_location('verification_runner', 'verification/runner.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    failing = tmp_path / 'test_failure.py'
    sentinel = 'SYNTHETIC_SECRET_DO_NOT_RETAIN'
    failing.write_text('import pytest\n@pytest.mark.fixture\ndef test_failure():\n    print("' + sentinel + '")\n    raise ValueError("' + sentinel + '")\n')
    code, output = module.run_pytest([str(failing)], workers=0)
    assert code == 1
    evidence = json.loads((output / 'evidence.json').read_text())
    assert evidence['counts']['failed'] == 1
    for artifact in output.rglob('*'):
        if artifact.is_file():
            assert sentinel.encode() not in artifact.read_bytes()

@pytest.mark.fixture
def test_owned_python_timeout_is_reaped(tmp_path):
    import sys
    spec = importlib.util.spec_from_file_location('verification_runner', 'verification/runner.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pid_file = tmp_path / 'owned.pid'
    script = 'import os,time,pathlib; pathlib.Path(' + repr(str(pid_file)) + ').write_text(str(os.getpid())); time.sleep(60)'
    code, stdout = module.execute([sys.executable, '-c', script], {}, timeout=1)
    assert code == 124
    assert stdout == ''
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)

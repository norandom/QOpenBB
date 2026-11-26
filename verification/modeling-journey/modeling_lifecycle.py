"""Apply the modeling service lifecycle requested by one Playwright session."""

import subprocess
import time


def run_browser(command, env, change_service, evidence, *, timeout, cwd=None):
    directory = evidence / "service-control"
    directory.mkdir(mode=0o700)
    env = {**env, "JOURNEY_SERVICE_CONTROL": str(directory)}
    deadline = time.monotonic() + timeout
    with subprocess.Popen(command, env=env, cwd=cwd) as process:
        try:
            for action in ("stop", "start"):
                wait_for_request(directory / action, process, deadline)
                change_service(action)
                (directory / f"{action}.done").touch(exist_ok=False)
            status = process.wait(timeout=max(0, deadline - time.monotonic()))
            if status:
                raise subprocess.CalledProcessError(status, command)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


def wait_for_request(path, process, deadline):
    while not path.is_file():
        status = process.poll()
        if status:
            raise subprocess.CalledProcessError(status, process.args)
        if status == 0:
            raise RuntimeError(f"Missing modeling lifecycle request: {path.name}")
        if time.monotonic() >= deadline:
            raise subprocess.TimeoutExpired(process.args, 0)
        time.sleep(0.1)

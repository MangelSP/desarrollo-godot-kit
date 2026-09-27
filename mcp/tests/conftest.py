import json
import stat
import sys

import pytest

STUB = """#!/usr/bin/env python3
import json, os, sys, time
log = os.environ.get("STUB_LOG")
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(sys.argv[1:]) + "\\n")
out = os.environ.get("STUB_PRINT", "")
if out:
    print(out, flush=True)
time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
sys.exit(int(os.environ.get("STUB_EXIT", "0")))
"""

needs_posix = pytest.mark.skipif(sys.platform == "win32", reason="stub executables use a shebang")


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "game"
    root.mkdir()
    (root / "project.godot").write_text("config_version=5\n", encoding="utf-8")
    return root


@pytest.fixture
def make_stub(tmp_path, monkeypatch):
    monkeypatch.setenv("STUB_LOG", str(tmp_path / "stub.log"))

    def _make(name: str, env_var: str):
        path = tmp_path / "bin" / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(STUB, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv(env_var, str(path))
        return path

    return _make


@pytest.fixture
def stub_calls(tmp_path):
    def _calls() -> list[list[str]]:
        log = tmp_path / "stub.log"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    return _calls

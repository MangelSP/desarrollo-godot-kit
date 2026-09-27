import sys
import time

from godot_kit_mcp.proc import run


def test_run_captures_merged_output():
    r = run([sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"], 30)
    assert r.code == 0 and not r.timed_out
    assert "out" in r.output and "err" in r.output


def test_run_times_out_and_kills():
    start = time.monotonic()
    r = run([sys.executable, "-c", "import time; print('started', flush=True); time.sleep(30)"], 1)
    assert r.timed_out and r.code is None
    assert time.monotonic() - start < 10


def test_run_missing_executable():
    r = run(["/definitely/not/here/godot"], 5)
    assert r.code is None and not r.timed_out
    assert r.output.startswith("cannot run")


def test_run_path_with_spaces_and_unicode(tmp_path):
    folder = tmp_path / "Program Files" / "Godot 4与C"
    folder.mkdir(parents=True)
    script = folder / "say.py"
    script.write_text("print('hola')", encoding="utf-8")
    r = run([sys.executable, str(script)], 30, cwd=folder)
    assert r.code == 0 and "hola" in r.output

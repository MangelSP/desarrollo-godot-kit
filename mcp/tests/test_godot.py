import shutil
from pathlib import Path

import pytest

from conftest import needs_posix
from godot_kit_mcp import config, godot
from godot_kit_mcp.png import decode_png

FIXTURE = Path(__file__).parent / "fixtures" / "min_project"

GUT_OUTPUT = """\x1b[0mres://tests/unit/test_a.gd
* test_ok
* test_bad
    [Failed]:  expected 1 got 2
Totals
------
Scripts               1
Tests                 2
Passing Tests         1
Failing Tests         1
Asserts               2
"""


def test_parse_log_splits_errors_and_warnings():
    log = godot.parse_log("ok line\nERROR: boom\n  WARNING: careful\nSCRIPT ERROR: Parse Error\n")
    assert log["errors"] == ["ERROR: boom", "SCRIPT ERROR: Parse Error"]
    assert log["warnings"] == ["WARNING: careful"]


def test_parse_gut_totals_and_failures():
    g = godot.parse_gut(GUT_OUTPUT)
    assert g["totals"]["tests"] == 2 and g["totals"]["failing_tests"] == 1
    assert g["failures"] == ["test_bad: [Failed]:  expected 1 got 2"]
    assert g["all_passed"] is False


def test_find_reports_missing_godot(project, monkeypatch):
    monkeypatch.setattr(config, "resolve_tool", lambda tool, root: config.ToolPath(None, "missing"))
    r = godot.find(project)
    assert r["ok"] is False and "Godot not found" in r["summary"]


@needs_posix
def test_import_flags_errors_in_log(project, make_stub, monkeypatch, stub_calls):
    make_stub("godot", "GODOT_BIN")
    monkeypatch.setenv("STUB_PRINT", "ERROR: broken script")
    r = godot.import_project(project)
    assert r["ok"] is False and r["errors"] == ["ERROR: broken script"]
    assert stub_calls()[0] == ["--headless", "--editor", "--quit", "--path", str(project)]


@needs_posix
def test_run_scene_times_out_instead_of_hanging(project, make_stub, monkeypatch):
    make_stub("godot", "GODOT_BIN")
    monkeypatch.setenv("STUB_SLEEP", "30")
    r = godot.run_scene(project, "res://main.tscn", frames=10, timeout_s=1)
    assert r["ok"] is False and r["timed_out"] is True and "timed out" in r["summary"]


def test_run_tests_requires_gut(project):
    r = godot.run_tests(project)
    assert r["ok"] is False and "GUT is not installed" in r["summary"]


def test_export_requires_presets(project):
    r = godot.export(project, "Android", "build/game.apk")
    assert r["ok"] is False and "export_presets.cfg" in r["summary"]


# --- integration: real Godot -------------------------------------------------

def _real_godot():
    t = config.resolve_tool("godot", None)
    return t.path if t.path and t.path.exists() else None


real = pytest.mark.skipif(_real_godot() is None, reason="no Godot executable found")


@pytest.fixture
def min_project(tmp_path):
    root = tmp_path / "min_project"
    shutil.copytree(FIXTURE, root)
    return root


@pytest.mark.godot
@real
def test_real_find_and_import(min_project):
    found = godot.find(min_project)
    assert found["ok"] and found["version"].startswith("4.")
    r = godot.import_project(min_project, timeout_s=180)
    assert r["ok"], r


@pytest.mark.godot
@real
def test_real_screenshot(min_project):
    r = godot.screenshot(min_project, "res://main.tscn", frames=10, out="shot.png", width=320, height=240)
    assert r["ok"], r
    w, h, rgba = decode_png(Path(r["path"]).read_bytes())
    assert (w, h) == (320, 240)
    assert rgba[:4] == bytes([255, 0, 0, 255])  # top-left pixel is the red box

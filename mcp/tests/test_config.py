import os
import stat

import pytest

from godot_kit_mcp import config


def test_find_project_root_walks_up(project):
    sub = project / "scenes" / "ui"
    sub.mkdir(parents=True)
    assert config.find_project_root(sub) == project.resolve()


def test_find_project_root_names_the_folder(tmp_path):
    with pytest.raises(config.ProjectNotFound, match=str(tmp_path.resolve())):
        config.find_project_root(tmp_path)


def test_config_beats_env(project, monkeypatch, tmp_path):
    (project / ".godot-kit.toml").write_text('[tools]\ngodot = "/opt/from-config"\n', encoding="utf-8")
    monkeypatch.setenv("GODOT_BIN", "/opt/from-env")
    t = config.resolve_tool("godot", project)
    assert (str(t.path), t.source) == ("/opt/from-config", "config")


def test_env_beats_path(project, monkeypatch, tmp_path):
    bindir = tmp_path / "pathbin"
    bindir.mkdir()
    exe = bindir / "godot"
    exe.write_text("#!/bin/sh\n")
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", str(bindir))
    monkeypatch.setenv("GODOT_BIN", "/opt/from-env")
    assert config.resolve_tool("godot", project).source == "env"
    monkeypatch.delenv("GODOT_BIN")
    t = config.resolve_tool("godot", project)
    assert t.source == "path" and t.path.name.startswith("godot")


def test_missing_when_nothing_found(project, monkeypatch, tmp_path):
    monkeypatch.delenv("TILED_BIN", raising=False)
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.setattr(config, "os_default_candidates", lambda tool: [])
    t = config.resolve_tool("tiled", project)
    assert t.path is None and t.source == "missing"


def test_resolve_inside(project):
    assert config.resolve_inside(project, "assets/a.png") == (project / "assets/a.png").resolve()
    assert config.resolve_inside(project, "res://assets/a.png") == (project / "assets/a.png").resolve()
    with pytest.raises(ValueError):
        config.resolve_inside(project, "../outside.png")


def test_reserve_credits_default_and_config(project):
    assert config.reserve_credits(project) == 1500
    (project / ".godot-kit.toml").write_text("[elevenlabs]\nreserve_credits = 900\n", encoding="utf-8")
    assert config.reserve_credits(project) == 900


def test_kit_root_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("GODOT_KIT_ROOT", str(tmp_path))
    assert config.kit_root() == tmp_path

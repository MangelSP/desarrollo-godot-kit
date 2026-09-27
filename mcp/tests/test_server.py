import asyncio
import json

from godot_kit_mcp.server import server

EXPECTED = {
    "godot_find", "godot_import", "godot_test", "godot_run_scene", "godot_screenshot", "godot_export",
    "tiled_export", "greybox_tileset", "greybox_sprite", "pixelorama_open",
    "elevenlabs_balance", "elevenlabs_sfx", "elevenlabs_music",
    "plan_status", "plan_next_task", "plan_mark", "checkpoint_record",
    "intake_questions", "project_scaffold", "knowledge_search", "knowledge_get",
}

PLAN = "## Milestone 0: Base\r\n\r\n- [ ] **T0.1 · game-architect**: Architecture.\r\n"


def call(name, args):
    result = asyncio.run(server.call_tool(name, args))
    return json.loads(result.content[0].text)


def test_exactly_the_spec_tools():
    tools = asyncio.run(server.list_tools())
    assert {t.name for t in tools} == EXPECTED
    assert all(t.description for t in tools)


def test_plan_tools_round_trip_crlf(project):
    (project / "docs").mkdir()
    plan_file = project / "docs/mvp-plan.md"
    plan_file.write_bytes(PLAN.encode())
    nxt = call("plan_next_task", {"project_dir": str(project)})
    assert nxt["ok"] and nxt["task"]["id"] == "T0.1" and nxt["reason"] == "ok"
    marked = call("plan_mark", {"project_dir": str(project), "task_id": "T0.1", "state": "done", "note": "wrote it"})
    assert marked["ok"], marked
    assert plan_file.read_bytes().decode() == (
        "## Milestone 0: Base\r\n\r\n- [x] **T0.1 · game-architect**: Architecture.\r\n  Done: wrote it\r\n"
    )
    status = call("plan_status", {"project_dir": str(project)})
    assert status["milestones"]["Milestone 0: Base"]["done"] == 1


def test_errors_come_back_as_fail(tmp_path):
    r = call("plan_status", {"project_dir": str(tmp_path)})
    assert r["ok"] is False and "project.godot" in r["summary"]
    r = call("plan_mark", {"project_dir": str(tmp_path), "task_id": "T1", "state": "done"})
    assert r["ok"] is False


def test_intake_questions():
    r = call("intake_questions", {})
    assert r["ok"] and len(r["questions"]) == 12


def test_elevenlabs_without_key(project, monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    r = call("elevenlabs_sfx", {"project_dir": str(project), "out": "a.mp3", "prompt": "horn", "seconds": 1.0})
    assert r["ok"] is False and "ELEVENLABS_API_KEY" in r["summary"]

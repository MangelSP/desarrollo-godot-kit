import io
import json
import zipfile

import pytest

from godot_kit_mcp import intake

RELEASES = [
    {"tag_name": "v9.8.0", "target_commitish": "main", "prerelease": False, "draft": False},
    {"tag_name": "v9.7.1", "target_commitish": "godot_4_7", "prerelease": False, "draft": False},
    {"tag_name": "v9.6.0", "target_commitish": "godot_4_6", "prerelease": False, "draft": False},
]


def _zip(members: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in members.items():
            z.writestr(name, data)
    return buf.getvalue()


def _fetch(zip_bytes):
    def fetch(url):
        return json.dumps(RELEASES).encode() if "api.github.com" in url else zip_bytes
    return fetch


def test_questions_cover_spec():
    ids = [q["id"] for q in intake.QUESTIONS]
    assert ids == ["pitch", "genre", "core_loop", "platforms", "session_length", "art_direction",
                   "narrative", "maps", "audio", "languages", "out_of_scope", "first_checkpoint"]


def test_pick_gut_release():
    assert intake.pick_gut_release(RELEASES, "4.7.stable.mono.official")[0]["tag_name"] == "v9.7.1"
    release, exact = intake.pick_gut_release(RELEASES, "4.9.0")
    assert release["tag_name"] == "v9.8.0" and exact is False


def test_install_gut_extracts_only_addons(tmp_path):
    z = _zip({"Gut-9.7.1/addons/gut/gut_cmdln.gd": b"extends SceneTree", "Gut-9.7.1/README.md": b"x"})
    r = intake.install_gut(tmp_path, "4.7", fetch=_fetch(z))
    assert r["ok"] and r["tag"] == "v9.7.1"
    assert (tmp_path / "addons/gut/gut_cmdln.gd").read_bytes() == b"extends SceneTree"
    assert not (tmp_path / "README.md").exists()


def test_install_gut_blocks_zip_slip(tmp_path):
    z = _zip({"Gut/addons/gut/../../../evil.gd": b"x"})
    r = intake.install_gut(tmp_path / "game", "4.7", fetch=_fetch(z))
    assert r["ok"] is False and not (tmp_path / "evil.gd").exists()


@pytest.fixture
def template(tmp_path):
    t = tmp_path / "template"
    (t / "docs").mkdir(parents=True)
    (t / "project.godot").write_text('config/name="{{game_name}}"\n', encoding="utf-8")
    (t / "docs/gdd.md").write_text("# {{game_name}}\n\n{{pitch}}\n{{mystery}}\n", encoding="utf-8")
    (t / "icon.png").write_bytes(b"\x89PNG{{game_name}}")
    return t


def test_scaffold_fills_placeholders(tmp_path, template):
    z = _zip({"Gut/addons/gut/gut_cmdln.gd": b"x"})
    target = tmp_path / "new_game"
    r = intake.scaffold(target, {"game_name": "Motoconcho", "pitch": "Deliver on a scooter"}, template, "4.7",
                        fetch=_fetch(z))
    assert r["ok"], r
    assert (target / "project.godot").read_text(encoding="utf-8") == 'config/name="Motoconcho"\n'
    assert "Deliver on a scooter" in (target / "docs/gdd.md").read_text(encoding="utf-8")
    assert r["unfilled"] == ["mystery"]
    assert (target / "icon.png").read_bytes() == b"\x89PNG{{game_name}}"  # binary untouched
    assert (target / "addons/gut/gut_cmdln.gd").exists()


def test_scaffold_refuses_non_empty_target(tmp_path, template):
    target = tmp_path / "existing"
    target.mkdir()
    (target / "keep.txt").write_text("mine", encoding="utf-8")
    r = intake.scaffold(target, {"game_name": "X"}, template, "4.7", fetch=_fetch(b""))
    assert r["ok"] is False and (target / "keep.txt").read_text(encoding="utf-8") == "mine"

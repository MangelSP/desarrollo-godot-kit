import time

from conftest import needs_posix
from godot_kit_mcp import assets
from godot_kit_mcp.png import decode_png


def test_greybox_tileset_layout(project):
    tiles = [{"name": "street", "color": "#5C5F66"}, {"name": "alley", "color": "#8B6B4A"},
             {"name": "building", "color": "#2B2D42"}]
    r = assets.greybox_tileset(project, "assets/tiles.png", tiles, tile_size=4, columns=2)
    assert r["ok"] and r["atlas"] == {"street": [0, 0], "alley": [1, 0], "building": [0, 1]}
    w, h, rgba = decode_png((project / "assets/tiles.png").read_bytes())
    assert (w, h) == (8, 8)
    assert rgba[:4] == bytes([92, 95, 102, 255])


def test_greybox_tileset_rejects_duplicates_and_escape(project):
    dup = [{"name": "a", "color": "#000000"}, {"name": "a", "color": "#FFFFFF"}]
    assert assets.greybox_tileset(project, "t.png", dup)["ok"] is False
    r = assets.greybox_tileset(project, "../t.png", [{"name": "a", "color": "#000000"}])
    assert r["ok"] is False and "outside the project" in r["summary"]


def test_greybox_sprite(project):
    r = assets.greybox_sprite(project, "res://assets/sprites/bike.png", "triangle", "#FFD23F", 24, 16, outline="#000000")
    assert r["ok"]
    w, h, _ = decode_png((project / "assets/sprites/bike.png").read_bytes())
    assert (w, h) == (24, 16)


def test_tiled_export_needs_converter(project):
    r = assets.tiled_export(project, "res://maps/a.tmx", "res://scenes/world/generated/AMap.tscn", "res://t.tres")
    assert r["ok"] is False and "tools/tiled_to_godot.gd" in r["summary"]


@needs_posix
def test_tiled_export_runs_import_then_converter(project, make_stub, stub_calls):
    (project / "tools").mkdir()
    (project / "tools/tiled_to_godot.gd").write_text("extends SceneTree\n", encoding="utf-8")
    make_stub("godot", "GODOT_BIN")
    r = assets.tiled_export(project, "res://maps/a.tmx", "res://gen/AMap.tscn", "res://t.tres")
    assert r["ok"], r
    calls = stub_calls()
    assert calls[0] == ["--headless", "--path", str(project), "--import"]
    assert calls[1] == ["--headless", "--path", str(project), "-s", "res://tools/tiled_to_godot.gd",
                        "--", "res://maps/a.tmx", "res://gen/AMap.tscn", "res://t.tres"]
    assert not any("--export-map" in arg for call in calls for arg in call)


@needs_posix
def test_pixelorama_open_starts_detached(project, make_stub, stub_calls):
    (project / "a.png").write_bytes(b"x")
    make_stub("pixelorama", "PIXELORAMA_BIN")
    r = assets.pixelorama_open(project, "a.png")
    assert r["ok"], r
    for _ in range(50):
        if stub_calls():
            break
        time.sleep(0.1)
    assert stub_calls() == [[str((project / "a.png").resolve())]]


def test_pixelorama_open_missing_file(project):
    assert assets.pixelorama_open(project, "nope.png")["ok"] is False

"""Greybox art, Tiled map conversion and Pixelorama hand-off."""

import subprocess
from pathlib import Path

from . import config, godot
from .raster import Canvas, parse_color
from .result import fail, ok

CONVERTER = "tools/tiled_to_godot.gd"


def greybox_tileset(root: Path, out: str, tiles: list[dict], tile_size: int = 32, columns: int = 8) -> dict:
    names = [t["name"] for t in tiles]
    if not tiles or len(set(names)) != len(names):
        return fail("tiles must be a non-empty list with unique names")
    try:
        target = config.resolve_inside(root, out)
    except ValueError as exc:
        return fail(str(exc))
    rows = -(-len(tiles) // columns)
    width = min(columns, len(tiles)) * tile_size
    canvas = Canvas(width, rows * tile_size)
    atlas: dict[str, list[int]] = {}
    for index, tile in enumerate(tiles):
        col, row = index % columns, index // columns
        canvas.fill_rect(col * tile_size, row * tile_size, tile_size, tile_size, parse_color(tile["color"]))
        atlas[tile["name"]] = [col, row]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canvas.png())
    return ok(f"Tileset with {len(tiles)} tiles saved to {target}", path=str(target), atlas=atlas)


def greybox_sprite(root: Path, out: str, shape: str, color: str, width: int, height: int, outline: str = "") -> dict:
    try:
        target = config.resolve_inside(root, out)
    except ValueError as exc:
        return fail(str(exc))
    canvas = Canvas(width, height)
    canvas.fill_shape(shape, 0, 0, width, height, parse_color(color))
    if outline:
        canvas.outline(parse_color(outline))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canvas.png())
    return ok(f"{shape} sprite {width}x{height} saved to {target}", path=str(target))


def tiled_export(root: Path, tmx: str, out: str, tileset: str, timeout_s: float = 180) -> dict:
    if not (root / CONVERTER).is_file():
        return fail(f"This project has no {CONVERTER}. The kit's project template provides one; "
                    "Tiled's own --export-map tscn is not used because it crashes on Tiled 1.12.2.")
    r, err = godot._run(root, ["--headless", "--path", str(root), "--import"], timeout_s)
    if err:
        return err
    if r.timed_out or r.code != 0:
        return fail("Godot import before the conversion failed", log_tail=godot.tail(r.output))
    args = ["--headless", "--path", str(root), "-s", f"res://{CONVERTER}", "--", tmx, out, tileset]
    r, err = godot._run(root, args, timeout_s)
    if err:
        return err
    if r.timed_out:
        return fail(f"Map conversion timed out after {timeout_s:g}s", timed_out=True, log_tail=godot.tail(r.output))
    if r.code != 0:
        return fail(f"Map conversion of {tmx} failed; the previous scene is unchanged", log_tail=godot.tail(r.output))
    return ok(f"Converted {tmx} into {out}", scene=out, log_tail=godot.tail(r.output, 20))


def pixelorama_open(root: Path | None, path: str) -> dict:
    target = config.resolve_inside(root, path) if root else Path(path).expanduser().resolve()
    if not target.is_file():
        return fail(f"file not found: {target}")
    t = config.resolve_tool("pixelorama", root)
    if t.path is None or not t.path.exists():
        return fail("Pixelorama not found. Install it, or set [tools].pixelorama in .godot-kit.toml, or PIXELORAMA_BIN.")
    subprocess.Popen([str(t.path), str(target)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    return ok(f"Opened {target} in Pixelorama", path=str(target))

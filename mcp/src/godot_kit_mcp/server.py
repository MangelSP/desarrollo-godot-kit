"""MCP entry point. Tool logic lives in the other modules; this file only wires it."""

import os
from dataclasses import asdict
from datetime import date
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from . import assets, config, elevenlabs, godot, intake, knowledge, plan
from .result import fail, ok, safe

server = MCPServer(
    "godot-kit",
    instructions=(
        "Tools for building 2D Godot 4 games with GDScript, Tiled and Pixelorama: "
        "run Godot headless, test with GUT, take screenshots, convert Tiled maps, "
        "make greybox art, track the MVP plan, scaffold projects and search game-dev knowledge. "
        "Every tool returns {ok, summary, ...}; read summary first."
    ),
)


def _root(project_dir: str) -> Path:
    return config.find_project_root(project_dir)


def _plan_file(project_dir: str, plan_path: str) -> Path:
    return config.resolve_inside(_root(project_dir), plan_path)


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _write(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


# --- Godot -------------------------------------------------------------------

@server.tool()
@safe
def godot_find(project_dir: str = ".") -> dict:
    """Find the Godot 4 executable (.godot-kit.toml, GODOT_BIN, PATH, OS defaults) and report its version."""
    try:
        root = _root(project_dir)
    except config.ProjectNotFound:
        root = None
    return godot.find(root)


@server.tool()
@safe
def godot_import(project_dir: str = ".", timeout_s: float = 300) -> dict:
    """Import the project headless (--editor --quit) and return parsed errors and warnings."""
    return godot.import_project(_root(project_dir), timeout_s)


@server.tool()
@safe
def godot_test(project_dir: str = ".", test_dir: str = "res://tests", timeout_s: float = 600) -> dict:
    """Run the GUT test suite headless; returns totals and failing tests."""
    return godot.run_tests(_root(project_dir), test_dir, timeout_s)


@server.tool()
@safe
def godot_run_scene(scene: str, project_dir: str = ".", frames: int = 120, timeout_s: float = 120) -> dict:
    """Run a scene headless for N frames and return errors, warnings and the end of the log."""
    return godot.run_scene(_root(project_dir), scene, frames, timeout_s)


@server.tool()
@safe
def godot_screenshot(scene: str, project_dir: str = ".", frames: int = 30, out: str = "",
                     width: int = 1280, height: int = 720, timeout_s: float = 120) -> dict:
    """Render a scene for N frames and save the window as PNG so you can look at the result."""
    return godot.screenshot(_root(project_dir), scene, frames, out, width, height, timeout_s)


@server.tool()
@safe
def godot_export(preset: str, out_path: str, project_dir: str = ".", release: bool = False,
                 timeout_s: float = 900) -> dict:
    """Export an existing preset from export_presets.cfg (debug by default)."""
    return godot.export(_root(project_dir), preset, out_path, release, timeout_s)


# --- Assets ------------------------------------------------------------------

@server.tool()
@safe
def tiled_export(tmx: str, out: str, tileset: str, project_dir: str = ".", timeout_s: float = 180) -> dict:
    """Convert a Tiled .tmx into a TileMapLayer scene with the project's tools/tiled_to_godot.gd."""
    return assets.tiled_export(_root(project_dir), tmx, out, tileset, timeout_s)


@server.tool()
@safe
def greybox_tileset(out: str, tiles: list[dict], project_dir: str = ".", tile_size: int = 32,
                    columns: int = 8) -> dict:
    """Write a solid-color tileset PNG. tiles = [{"name": "street", "color": "#5C5F66"}, ...]."""
    return assets.greybox_tileset(_root(project_dir), out, tiles, tile_size, columns)


@server.tool()
@safe
def greybox_sprite(out: str, shape: str, color: str, width: int, height: int, project_dir: str = ".",
                   outline: str = "") -> dict:
    """Write a greybox sprite PNG: shape is rect, circle, triangle (points right) or hexagon."""
    return assets.greybox_sprite(_root(project_dir), out, shape, color, width, height, outline)


@server.tool()
@safe
def pixelorama_open(path: str, project_dir: str = ".") -> dict:
    """Open an image in Pixelorama so the human can touch it up."""
    try:
        root = _root(project_dir)
    except config.ProjectNotFound:
        root = None
    return assets.pixelorama_open(root, path)


# --- ElevenLabs --------------------------------------------------------------

@server.tool()
@safe
def elevenlabs_balance() -> dict:
    """Real ElevenLabs credit balance (needs ELEVENLABS_API_KEY with user_read)."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return fail("Set the ELEVENLABS_API_KEY environment variable (never put the key in a file).")
    left = elevenlabs.balance(key)
    return ok(f"{left} credits left", credits=left)


@server.tool()
@safe
def elevenlabs_sfx(out: str, prompt: str, seconds: float, project_dir: str = ".", loop: bool = False) -> dict:
    """Generate one sound effect (0.5-30 s, ~40 credits/s) only if the reserve in .godot-kit.toml stays intact."""
    root = _root(project_dir)
    return elevenlabs.generate("sfx", root=root, out=out, prompt=prompt, seconds=seconds, loop=loop,
                               reserve=config.reserve_credits(root), api_key=os.environ.get("ELEVENLABS_API_KEY"))


@server.tool()
@safe
def elevenlabs_music(out: str, prompt: str, seconds: float, project_dir: str = ".") -> dict:
    """Generate one instrumental music track (3-300 s, ~7 credits/s) only if the reserve stays intact."""
    root = _root(project_dir)
    return elevenlabs.generate("music", root=root, out=out, prompt=prompt, seconds=seconds,
                               reserve=config.reserve_credits(root), api_key=os.environ.get("ELEVENLABS_API_KEY"))


# --- Plan --------------------------------------------------------------------

@server.tool()
@safe
def plan_status(project_dir: str = ".", plan_path: str = "docs/mvp-plan.md") -> dict:
    """Count tasks per milestone and state (todo, in_progress, done, blocked)."""
    counts = plan.status(plan.parse(_read(_plan_file(project_dir, plan_path))))
    done = sum(c["done"] for c in counts.values())
    total = sum(sum(c.values()) for c in counts.values())
    return ok(f"{done}/{total} tasks done", milestones=counts)


@server.tool()
@safe
def plan_next_task(project_dir: str = ".", plan_path: str = "docs/mvp-plan.md") -> dict:
    """Next task to work on. reason: ok, checkpoint, blocked:<id>, waiting_on:<id> or complete."""
    task, reason = plan.next_task(plan.parse(_read(_plan_file(project_dir, plan_path))))
    if task is None:
        return ok(f"No task to run ({reason})", task=None, reason=reason)
    return ok(f"{task.id} · {task.owner}: {task.title} ({reason})", task=asdict(task), reason=reason)


@server.tool()
@safe
def plan_mark(task_id: str, state: str, note: str = "", project_dir: str = ".",
              plan_path: str = "docs/mvp-plan.md") -> dict:
    """Set a task's state (todo, in_progress, done, blocked) and optionally its Done: note."""
    path = _plan_file(project_dir, plan_path)
    _write(path, plan.mark(_read(path), task_id, state, note or None))
    return ok(f"{task_id} is now {state}")


@server.tool()
@safe
def checkpoint_record(task_id: str, feedback: str, project_dir: str = ".",
                      plan_path: str = "docs/mvp-plan.md") -> dict:
    """Store the human's feedback under a checkpoint task (does not change its state)."""
    path = _plan_file(project_dir, plan_path)
    _write(path, plan.record_checkpoint(_read(path), task_id, feedback, date.today().isoformat()))
    return ok(f"Feedback recorded under {task_id}")


# --- Intake ------------------------------------------------------------------

@server.tool()
@safe
def intake_questions() -> dict:
    """The /new-game questionnaire: ask one question at a time, recommended option first."""
    return ok(f"{len(intake.QUESTIONS)} questions", questions=intake.QUESTIONS)


@server.tool()
@safe
def project_scaffold(target_dir: str, answers: dict[str, str], godot_version: str = "") -> dict:
    """Create a new game from the kit template in an empty folder and install the matching GUT."""
    kit = config.kit_root()
    if kit is None:
        return fail("GODOT_KIT_ROOT is not set and the kit checkout was not found")
    version = godot_version or godot.find(None).get("version", "")
    if not version:
        return fail("Could not detect the Godot version; pass godot_version, e.g. '4.7'")
    return intake.scaffold(Path(target_dir).expanduser(), answers, kit / "templates" / "project", version)


# --- Knowledge ---------------------------------------------------------------

def _cards() -> list[knowledge.Card]:
    root = knowledge.default_root()
    return knowledge.load_cards(root) if root else []


@server.tool()
@safe
def knowledge_search(query: str, topic: str = "", limit: int = 10) -> dict:
    """Search the kit's reviewed game-dev knowledge cards (pixel art, design, feel, UX, Godot)."""
    hits = knowledge.search(_cards(), query, topic, limit)
    return ok(f"{len(hits)} cards match", hits=hits)


@server.tool()
@safe
def knowledge_get(name: str) -> dict:
    """Return one knowledge card by name."""
    card = knowledge.get(_cards(), name)
    if card is None:
        return fail(f"no card named {name!r}")
    return ok(card.name, topic=card.topic, confidence=card.confidence, body=card.body)


def main() -> None:
    server.run()

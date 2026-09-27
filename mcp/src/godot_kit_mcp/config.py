"""Project root, .godot-kit.toml, and where the external tools live."""

import os
import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = ".godot-kit.toml"
ENV_VARS = {"godot": "GODOT_BIN", "tiled": "TILED_BIN", "pixelorama": "PIXELORAMA_BIN"}
PATH_NAMES = {
    "godot": ["godot", "godot4", "Godot"],
    "tiled": ["tiled", "Tiled"],
    "pixelorama": ["pixelorama", "Pixelorama"],
}
DEFAULT_RESERVE = 1500


class ProjectNotFound(Exception):
    pass


@dataclass
class ToolPath:
    path: Path | None
    source: str


def find_project_root(start: str | Path) -> Path:
    here = Path(start).expanduser().resolve()
    for folder in [here, *here.parents]:
        if (folder / "project.godot").is_file():
            return folder
    raise ProjectNotFound(f"no project.godot in {here} or any parent folder")


def load_config(root: Path | None) -> dict:
    if root is None or not (root / CONFIG_NAME).is_file():
        return {}
    with (root / CONFIG_NAME).open("rb") as fh:
        return tomllib.load(fh)


def os_default_candidates(tool: str) -> list[Path]:
    home = Path.home()
    if sys.platform == "darwin":
        pattern = {
            "godot": "Godot*.app/Contents/MacOS/Godot",
            "tiled": "Tiled.app/Contents/MacOS/Tiled",
            "pixelorama": "Pixelorama.app/Contents/MacOS/Pixelorama",
        }[tool]
        found = [p for base in (Path("/Applications"), home / "Applications") for p in base.glob(pattern)]
        return sorted(found)
    if sys.platform == "win32":
        pattern = {
            "godot": "Godot*/Godot*.exe",
            "tiled": "Tiled/tiled.exe",
            "pixelorama": "Pixelorama/Pixelorama.exe",
        }[tool]
        bases = [os.environ.get(v, "") for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
        found = [p for base in bases if base for p in Path(base).glob(pattern)]
        # The _console.exe build prints to stdout, which is what we capture.
        return sorted(found, key=lambda p: ("console" not in p.name.lower(), str(p)))
    patterns = {
        "godot": ["godot*", "org.godotengine.Godot"],
        "tiled": ["tiled", "org.mapeditor.Tiled"],
        "pixelorama": ["pixelorama", "com.orama_interactive.Pixelorama"],
    }[tool]
    bases = [
        home / ".local/bin",
        Path("/usr/local/bin"),
        Path("/var/lib/flatpak/exports/bin"),
        home / ".local/share/flatpak/exports/bin",
    ]
    return sorted(p for base in bases for pat in patterns for p in base.glob(pat))


def resolve_tool(tool: str, root: Path | None) -> ToolPath:
    configured = str(load_config(root).get("tools", {}).get(tool, "")).strip()
    if configured:
        return ToolPath(Path(configured).expanduser(), "config")
    from_env = os.environ.get(ENV_VARS[tool], "").strip()
    if from_env:
        return ToolPath(Path(from_env).expanduser(), "env")
    for name in PATH_NAMES[tool]:
        found = shutil.which(name)
        if found:
            return ToolPath(Path(found), "path")
    candidates = os_default_candidates(tool)
    if candidates:
        return ToolPath(candidates[0], "os-default")
    return ToolPath(None, "missing")


def resolve_inside(root: Path, path: str) -> Path:
    rel = path[len("res://"):] if path.startswith("res://") else path
    target = (root / rel).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"{path} is outside the project {root}")
    return target


def kit_root() -> Path | None:
    from_env = os.environ.get("GODOT_KIT_ROOT", "").strip()
    if from_env:
        return Path(from_env).expanduser()
    checkout = Path(__file__).resolve().parents[3]  # mcp/src/godot_kit_mcp/config.py -> repo root
    return checkout if (checkout / ".claude-plugin").is_dir() else None


def reserve_credits(root: Path | None) -> int:
    return int(load_config(root).get("elevenlabs", {}).get("reserve_credits", DEFAULT_RESERVE))

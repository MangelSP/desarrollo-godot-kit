"""The /new-game questionnaire and the project scaffold."""

import io
import json
import re
import shutil
import urllib.request
import zipfile
from collections.abc import Callable
from pathlib import Path

from .result import fail, ok

QUESTIONS: list[dict] = [
    {"id": "pitch", "question": "Describe the game in one sentence.", "options": [], "recommended": ""},
    {"id": "genre", "question": "Genre and camera?",
     "options": ["Top-down arcade", "Side-scroller / platformer", "Puzzle", "Other"], "recommended": "Top-down arcade"},
    {"id": "core_loop", "question": "Core loop in three verbs (e.g. find, haggle, deliver)?", "options": [], "recommended": ""},
    {"id": "platforms", "question": "Target platforms and orientation?",
     "options": ["Android landscape + PC", "PC only", "Android portrait", "Web + PC"], "recommended": "Android landscape + PC"},
    {"id": "session_length", "question": "How long is one play session?",
     "options": ["3-5 minutes", "8-10 minutes", "20+ minutes"], "recommended": "8-10 minutes"},
    {"id": "art_direction", "question": "Art direction for the MVP?",
     "options": ["Greybox shapes only", "Greybox now, pixel art 16x16 later", "Pixel art 32x32 from the start"],
     "recommended": "Greybox now, pixel art 16x16 later"},
    {"id": "narrative", "question": "Does the game need story, scripts or dialogue?",
     "options": ["No", "Light (short texts)", "Yes (story and dialogue)"], "recommended": "No"},
    {"id": "maps", "question": "Build maps with Tiled?", "options": ["Yes", "No, Godot TileMapLayer only"], "recommended": "Yes"},
    {"id": "audio", "question": "Audio source?",
     "options": ["Procedural placeholders", "ElevenLabs with a credit budget"], "recommended": "Procedural placeholders"},
    {"id": "languages", "question": "Player-facing language(s)?", "options": [], "recommended": "English"},
    {"id": "out_of_scope", "question": "What is explicitly out of the MVP?", "options": [], "recommended": ""},
    {"id": "first_checkpoint", "question": "What should you be able to try first?", "options": [],
     "recommended": "Move the main character around a test map"},
]

TEXT_SUFFIXES = {".md", ".godot", ".gd", ".cfg", ".json", ".toml", ".tscn", ".tres", ".txt", ".sh", ".csv"}
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")
GUT_RELEASES = "https://api.github.com/repos/bitwes/Gut/releases?per_page=30"
GUT_ZIP = "https://github.com/bitwes/Gut/archive/refs/tags/{tag}.zip"

Fetch = Callable[[str], bytes]


def default_fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "godot-kit-mcp"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def pick_gut_release(releases: list[dict], godot_version: str) -> tuple[dict, bool]:
    stable = [r for r in releases if not r.get("prerelease") and not r.get("draft")]
    if not stable:
        raise ValueError("no stable GUT release found")
    m = re.match(r"(\d+)\.(\d+)", godot_version)
    if m:
        wanted = f"godot_{m[1]}_{m[2]}"
        for release in stable:
            if release.get("target_commitish") == wanted:
                return release, True
    return stable[0], False


def install_gut(target: Path, godot_version: str, fetch: Fetch = default_fetch) -> dict:
    release, exact = pick_gut_release(json.loads(fetch(GUT_RELEASES)), godot_version)
    tag = release["tag_name"]
    base = target.resolve()
    written = 0
    with zipfile.ZipFile(io.BytesIO(fetch(GUT_ZIP.format(tag=tag)))) as archive:
        for member in archive.infolist():
            idx = member.filename.find("addons/gut/")
            if idx < 0 or member.is_dir():
                continue
            dest = (base / member.filename[idx:]).resolve()
            if not dest.is_relative_to(base / "addons" / "gut"):
                return fail(f"GUT archive has an unsafe path: {member.filename}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(archive.read(member))
            written += 1
    note = "" if exact else f" (no release targets Godot {godot_version}; used the latest)"
    return ok(f"Installed GUT {tag}{note}", tag=tag, exact_match=exact, files=written)


def scaffold(target: Path, answers: dict[str, str], template_dir: Path, godot_version: str,
             fetch: Fetch = default_fetch) -> dict:
    if not template_dir.is_dir():
        return fail(f"template folder not found: {template_dir}")
    if target.exists() and any(target.iterdir()):
        return fail(f"{target} is not empty; choose a new folder so nothing gets overwritten")
    shutil.copytree(template_dir, target, dirs_exist_ok=True)
    unfilled: set[str] = set()
    for path in target.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")

        def fill(m: re.Match) -> str:
            if m[1] in answers:
                return str(answers[m[1]])
            unfilled.add(m[1])
            return m[0]

        path.write_text(PLACEHOLDER_RE.sub(fill, text), encoding="utf-8")
    gut = install_gut(target, godot_version, fetch)
    if not gut["ok"]:
        return fail(f"Project created in {target}, but GUT failed: {gut['summary']}", unfilled=sorted(unfilled))
    return ok(f"Project created in {target}; {gut['summary']}", path=str(target), unfilled=sorted(unfilled),
              gut_tag=gut["tag"])

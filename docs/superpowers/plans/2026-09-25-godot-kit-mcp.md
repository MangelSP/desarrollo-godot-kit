# Godot Kit MCP Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `godot-kit-mcp`, the Python MCP server of the Godot Kit, with the 21 tools from spec §6 (Godot, assets, plan, intake, knowledge), installable from the plugin with `uvx`.

**Architecture:** Every tool's logic lives in a plain, testable module (`config`, `proc`, `plan`, `godot`, `png`, `assets`, `elevenlabs`, `intake`, `knowledge`). `server.py` only wraps those functions as MCP tools, resolves the project root and converts every exception into `{"ok": false, "summary": ...}`. External programs (Godot, Pixelorama) always run through `proc.run` with an argument list and a hard timeout; network calls (ElevenLabs, GitHub) go through an injectable function so tests never touch the network.

**Tech Stack:** Python ≥ 3.11 (stdlib `tomllib`, `zlib`, `urllib`), `mcp` 2.2.x (`from mcp.server.mcpserver import MCPServer`, the 2.x name of FastMCP), `pytest`, `uv`/`uvx`, hatchling. GDScript (Godot 4.4+) for the bundled screenshot script.

**Spec:** `docs/specs/2026-09-25-godot-kit-design.md`

## Global Constraints

- Python `>=3.11`; the only runtime dependency is `mcp>=2.2,<3`.
- In mcp 2.x FastMCP is `MCPServer`: `from mcp.server.mcpserver import MCPServer`. `mcp.server.fastmcp` does not exist.
- Stdio transport. Plugin launch command: `uvx --from ${CLAUDE_PLUGIN_ROOT}/mcp godot-kit-mcp`.
- Every tool returns a JSON object with `ok`, a short `summary`, and data. Tools never raise raw exceptions.
- Every subprocess has a hard timeout (Godot can hang).
- Tool path lookup order: `.godot-kit.toml` in the project root → env var (`GODOT_BIN`, `TILED_BIN`, `PIXELORAMA_BIN`) → `PATH` → OS defaults.
- Secrets only from env (`ELEVENLABS_API_KEY`). Never write a key to a file, a log line or a tool result.
- `.godot-kit.toml` has `[tools] godot/tiled/pixelorama` and `[elevenlabs] reserve_credits = 1500`.
- ElevenLabs: generate only if `balance - estimate ≥ reserve_credits`; log every generation to `docs/audio-ledger.md`.
- SFX cost: 40 credits per second with fixed duration (0.5–30 s). Music: measured ~288 credits per ~42 s track (use 7 credits/s).
- Never call Tiled's `--export-map tscn` (segfaults on Tiled 1.12.2). `tiled_export` runs the project's own `res://tools/tiled_to_godot.gd`.
- Plan format: task lines `- [ ] **T1.2 · owner**: title`, states `[ ]` todo, `[~]` in progress, `[x]` done, `[!]` blocked, notes on a `Done:` line under the task. Motoconcho's Spanish labels (`*Depende de:*`, `Hecho:`, "Punto de control") must parse too.
- English for code, docs and tool descriptions. MIT license.
- Works on macOS, Windows and Linux. No personal paths in code.

## Review Focus

1. **Godot never exits** (a script error before `quit()`): the tool must return `timed_out` within its timeout, never block the agent. Pinned in Task 2 (`proc` timeout) and Task 6 (`run_scene` with a sleeping stub).
2. **Paths with spaces or non-ASCII characters** (`Program Files`, `Godot_mono.app`, `Godot 4与C`): commands run as argument lists, never through a shell. Pinned in Task 2.
3. **A plan edited by hand**: CRLF line endings, Spanish labels, extra spaces. Parsing must tolerate them and `plan_mark` must change only the target lines, byte for byte. Pinned in Task 4 and Task 11 (the tool reads and writes bytes).
4. **ElevenLabs balance lag** (the balance takes ~60 s to show a charge): two quick generations must not both pass the reserve check. Pinned in Task 8 (pending estimates from the last 120 s count against the balance).
5. **`project_scaffold` pointed at a non-empty folder, or a GUT zip with `../` paths**: never overwrite existing work, never write outside the target. Pinned in Task 9.

---

## File map

```text
mcp/
├── pyproject.toml
├── src/godot_kit_mcp/
│   ├── __init__.py
│   ├── result.py        # ok(), fail(), @safe
│   ├── proc.py          # run(cmd, timeout_s, cwd) -> ProcResult
│   ├── config.py        # find_project_root, load_config, resolve_tool, resolve_inside, kit_root
│   ├── plan.py          # parse, next_task, mark, record_checkpoint, status
│   ├── png.py           # encode_png, decode_png (stdlib)
│   ├── raster.py        # Canvas, parse_color, shapes
│   ├── godot.py         # find, import_project, run_tests, run_scene, screenshot, export
│   ├── gdscript/screenshot.gd
│   ├── assets.py        # greybox_tileset, greybox_sprite, tiled_export, pixelorama_open
│   ├── elevenlabs.py    # balance, estimates, ledger, generate
│   ├── intake.py        # QUESTIONS, pick_gut_release, install_gut, scaffold
│   ├── knowledge.py     # parse_card, load_cards, search, get
│   └── server.py        # MCPServer + 21 tools, main()
└── tests/
    ├── conftest.py      # project fixture, stub executables
    ├── fixtures/min_project/{project.godot, main.tscn}
    └── test_*.py
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

All commands below run from `mcp/` unless stated otherwise. Test command: `uv run pytest -q`.

---

### Task 1: Package scaffold and result helpers

**Files:**
- Create: `mcp/pyproject.toml`, `mcp/src/godot_kit_mcp/__init__.py`, `mcp/src/godot_kit_mcp/result.py`, `mcp/src/godot_kit_mcp/server.py`
- Test: `mcp/tests/test_result.py`

**Interfaces:**
- Produces: `ok(summary: str, **data) -> dict`, `fail(summary: str, **data) -> dict`, `safe(fn) -> fn` (decorator: exceptions become `fail("<Type>: <msg>")`, keeps the signature via `functools.wraps`), `server: MCPServer`, `main() -> None`.

- [ ] **Step 1: Create `mcp/pyproject.toml`**

```toml
[project]
name = "godot-kit-mcp"
version = "0.1.0"
description = "MCP server for the Godot Kit: Godot, Tiled, Pixelorama, plan, intake and knowledge tools"
requires-python = ">=3.11"
license = "MIT"
dependencies = ["mcp>=2.2,<3"]

[project.scripts]
godot-kit-mcp = "godot_kit_mcp.server:main"

[dependency-groups]
dev = ["pytest>=8"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/godot_kit_mcp"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["godot: needs a real Godot 4 executable (skipped when none is found)"]
```

- [ ] **Step 2: Write the failing test** `mcp/tests/test_result.py`

```python
from godot_kit_mcp.result import fail, ok, safe


def test_ok_and_fail_shape():
    assert ok("done", n=1) == {"ok": True, "summary": "done", "n": 1}
    assert fail("nope") == {"ok": False, "summary": "nope"}


def test_safe_turns_exceptions_into_fail():
    @safe
    def boom(x: int) -> dict:
        raise ValueError(f"bad {x}")

    assert boom(3) == {"ok": False, "summary": "ValueError: bad 3"}


def test_safe_keeps_signature_and_doc():
    @safe
    def tool(a: int, b: str = "x") -> dict:
        """Doc."""
        return ok("fine")

    import inspect

    assert list(inspect.signature(tool).parameters) == ["a", "b"]
    assert tool.__doc__ == "Doc."
    assert tool(1)["ok"] is True
```

- [ ] **Step 3: Run it and see it fail**

Run: `uv run pytest -q tests/test_result.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'godot_kit_mcp'`.

- [ ] **Step 4: Implement**

`mcp/src/godot_kit_mcp/__init__.py`:

```python
"""Godot Kit MCP server."""

__version__ = "0.1.0"
```

`mcp/src/godot_kit_mcp/result.py`:

```python
"""Uniform tool results. Every tool returns ok(...) or fail(...), never raises."""

import functools
from collections.abc import Callable
from typing import Any


def ok(summary: str, **data: Any) -> dict[str, Any]:
    return {"ok": True, "summary": summary, **data}


def fail(summary: str, **data: Any) -> dict[str, Any]:
    return {"ok": False, "summary": summary, **data}


def safe(fn: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # tools must never raise to the client
            return fail(f"{type(exc).__name__}: {exc}")

    return wrapper
```

`mcp/src/godot_kit_mcp/server.py` (tools are added in Task 11):

```python
"""MCP entry point. Tool logic lives in the other modules; this file only wires it."""

from mcp.server.mcpserver import MCPServer

server = MCPServer(
    "godot-kit",
    instructions=(
        "Tools for building 2D Godot 4 games with GDScript, Tiled and Pixelorama: "
        "run Godot headless, test with GUT, take screenshots, convert Tiled maps, "
        "make greybox art, track the MVP plan, scaffold projects and search game-dev knowledge."
    ),
)


def main() -> None:
    server.run()
```

- [ ] **Step 5: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_result.py`
Expected: `3 passed`.

- [ ] **Step 6: Commit**

```bash
git add mcp/pyproject.toml mcp/uv.lock mcp/src mcp/tests
git commit -m "feat(mcp): package scaffold and result helpers"
```

---

### Task 2: Subprocess runner with hard timeouts

**Files:**
- Create: `mcp/src/godot_kit_mcp/proc.py`
- Test: `mcp/tests/test_proc.py`

**Interfaces:**
- Produces: `ProcResult(code: int | None, output: str, timed_out: bool)`; `run(cmd: list[str], timeout_s: float, cwd: str | Path | None = None) -> ProcResult`. stdout and stderr are merged in order; output is decoded as UTF-8 with replacement; a missing executable gives `code=None` and an output starting with `cannot run`.

- [ ] **Step 1: Write the failing test** `mcp/tests/test_proc.py`

```python
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
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_proc.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'godot_kit_mcp.proc'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/proc.py`

```python
"""Run external programs with an argument list (never a shell) and a hard timeout."""

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProcResult:
    code: int | None
    output: str
    timed_out: bool


def _text(data: bytes | str | None) -> str:
    if data is None:
        return ""
    return data.decode("utf-8", "replace") if isinstance(data, bytes) else data


def run(cmd: list[str], timeout_s: float, cwd: str | Path | None = None) -> ProcResult:
    try:
        done = subprocess.run(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout_s
        )
    except subprocess.TimeoutExpired as exc:  # subprocess.run already killed the child
        return ProcResult(None, _text(exc.output), True)
    except OSError as exc:
        return ProcResult(None, f"cannot run {cmd[0]}: {exc}", False)
    return ProcResult(done.returncode, _text(done.stdout), False)
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_proc.py`
Expected: `4 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/proc.py mcp/tests/test_proc.py
git commit -m "feat(mcp): subprocess runner with hard timeouts"
```

---

### Task 3: Configuration and tool resolution

**Files:**
- Create: `mcp/src/godot_kit_mcp/config.py`, `mcp/tests/conftest.py`
- Test: `mcp/tests/test_config.py`

**Interfaces:**
- Produces:
  - `class ProjectNotFound(Exception)`
  - `find_project_root(start: str | Path) -> Path` (walks up to the first folder with `project.godot`; raises `ProjectNotFound` naming the start folder)
  - `load_config(root: Path | None) -> dict` (`{}` if no `.godot-kit.toml`)
  - `ToolPath(path: Path | None, source: str)`; `source` is `"config" | "env" | "path" | "os-default" | "missing"`
  - `resolve_tool(tool: str, root: Path | None) -> ToolPath` for `"godot" | "tiled" | "pixelorama"`
  - `os_default_candidates(tool: str) -> list[Path]`
  - `resolve_inside(root: Path, path: str) -> Path` (relative paths are joined to `root`; `res://x` maps to `root/x`; raises `ValueError` if the result escapes `root`)
  - `kit_root() -> Path | None` (env `GODOT_KIT_ROOT`, else the repo root when running from a checkout, else `None`)
  - `reserve_credits(root: Path | None) -> int` (`[elevenlabs].reserve_credits`, default 1500)
- Test fixtures produced in `conftest.py`: `project` (a temp folder with `project.godot`), `make_stub(name, env_var)` (writes an executable Python stub that logs its argv as JSON lines to `$STUB_LOG`, prints `$STUB_PRINT`, sleeps `$STUB_SLEEP` s and exits with `$STUB_EXIT`), `stub_calls()`.

- [ ] **Step 1: Write the test fixtures** `mcp/tests/conftest.py`

```python
import json
import stat
import sys

import pytest

STUB = """#!/usr/bin/env python3
import json, os, sys, time
log = os.environ.get("STUB_LOG")
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(sys.argv[1:]) + "\\n")
out = os.environ.get("STUB_PRINT", "")
if out:
    print(out, flush=True)
time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
sys.exit(int(os.environ.get("STUB_EXIT", "0")))
"""

needs_posix = pytest.mark.skipif(sys.platform == "win32", reason="stub executables use a shebang")


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "game"
    root.mkdir()
    (root / "project.godot").write_text("config_version=5\n", encoding="utf-8")
    return root


@pytest.fixture
def make_stub(tmp_path, monkeypatch):
    monkeypatch.setenv("STUB_LOG", str(tmp_path / "stub.log"))

    def _make(name: str, env_var: str):
        path = tmp_path / "bin" / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(STUB, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv(env_var, str(path))
        return path

    return _make


@pytest.fixture
def stub_calls(tmp_path):
    def _calls() -> list[list[str]]:
        log = tmp_path / "stub.log"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]

    return _calls
```

- [ ] **Step 2: Write the failing test** `mcp/tests/test_config.py`

```python
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
```

- [ ] **Step 3: Run it and see it fail**

Run: `uv run pytest -q tests/test_config.py`
Expected: FAIL with `ImportError: cannot import name 'config'`.

- [ ] **Step 4: Implement** `mcp/src/godot_kit_mcp/config.py`

```python
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
```

- [ ] **Step 5: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_config.py`
Expected: `8 passed`.

- [ ] **Step 6: Commit**

```bash
git add mcp/src/godot_kit_mcp/config.py mcp/tests/conftest.py mcp/tests/test_config.py
git commit -m "feat(mcp): project config and tool resolution"
```

---

### Task 4: Plan parser and editor

**Files:**
- Create: `mcp/src/godot_kit_mcp/plan.py`
- Test: `mcp/tests/test_plan.py`

**Interfaces:**
- Produces:
  - `Task(id: str, owner: str, title: str, state: str, milestone: str, checkpoint: bool, depends: list[str], line: int)`; `state` is `"todo" | "in_progress" | "done" | "blocked"`
  - `parse(text: str) -> list[Task]`
  - `next_task(tasks: list[Task]) -> tuple[Task | None, str]`; the reason is `"ok"`, `"checkpoint"`, `"blocked:<id>"`, `"waiting_on:<id>"` or `"complete"`
  - `mark(text: str, task_id: str, state: str, note: str | None = None) -> str` (raises `KeyError` for an unknown id and `ValueError` for an unknown state)
  - `record_checkpoint(text: str, task_id: str, feedback: str, date: str) -> str`
  - `status(tasks: list[Task]) -> dict[str, dict[str, int]]` (milestone → counts per state)
- All text functions preserve the text's line endings (`\n` or `\r\n`) and leave every other line unchanged.

- [ ] **Step 1: Write the failing test** `mcp/tests/test_plan.py`

```python
import pytest

from godot_kit_mcp import plan

PLAN = """# MVP plan

## Milestone 0: Base

- [x] **T0.1 · game-architect**: Architecture doc.
  *Accept:* every system has an owner.
  Done: wrote docs/architecture.md.
- [ ] **T0.2 · game-designer**: Resources.
  *Depends on:* T0.1.

## Milestone 1: Driving

- [ ] **T1.1 · gameplay-programmer**: Moto scene.
  *Depends on:* T0.2, T0.1.
- [ ] **T1.2 · producer** CHECKPOINT: Human playtests the driving.
"""

SPANISH = """## Hito 1: Manejo

- [x] **T1.5 · qa-tester**: tests.
  Hecho: listo.
- [ ] **T1.6 · producer**: pedirle al usuario que pruebe. **Punto de control: no se sigue sin su visto bueno.**
  *Depende de:* T1.5.
"""


def test_parse_reads_tasks_and_milestones():
    tasks = plan.parse(PLAN)
    assert [t.id for t in tasks] == ["T0.1", "T0.2", "T1.1", "T1.2"]
    t = tasks[2]
    assert (t.owner, t.title, t.state, t.milestone) == (
        "gameplay-programmer", "Moto scene.", "todo", "Milestone 1: Driving"
    )
    assert t.depends == ["T0.2", "T0.1"]
    assert tasks[3].checkpoint and not tasks[2].checkpoint


def test_parse_spanish_labels_and_checkpoint():
    tasks = plan.parse(SPANISH)
    assert tasks[1].checkpoint and tasks[1].depends == ["T1.5"]
    assert tasks[0].state == "done"


def test_next_task_order_and_reasons():
    tasks = plan.parse(PLAN)
    task, reason = plan.next_task(tasks)
    assert (task.id, reason) == ("T0.2", "ok")

    text = plan.mark(PLAN, "T0.2", "done")
    text = plan.mark(text, "T1.1", "done")
    task, reason = plan.next_task(plan.parse(text))
    assert (task.id, reason) == ("T1.2", "checkpoint")

    blocked = plan.mark(PLAN, "T0.2", "blocked")
    assert plan.next_task(plan.parse(blocked)) == (None, "blocked:T0.2")

    done = PLAN.replace("- [ ]", "- [x]")
    assert plan.next_task(plan.parse(done)) == (None, "complete")


def test_next_task_waits_on_unfinished_dependency():
    text = PLAN.replace("*Depends on:* T0.1.", "*Depends on:* T1.1.")
    task, reason = plan.next_task(plan.parse(text))
    assert task.id == "T0.2" and reason == "waiting_on:T1.1"


def test_in_progress_task_comes_first():
    text = plan.mark(PLAN, "T1.1", "in_progress")
    assert plan.next_task(plan.parse(text))[0].id == "T1.1"


def test_mark_changes_only_target_lines():
    new = plan.mark(PLAN, "T0.2", "done", "created data/*.tres")
    old_lines, new_lines = PLAN.splitlines(), new.splitlines()
    assert new_lines[8] == "- [x] **T0.2 · game-designer**: Resources."
    assert new_lines[10] == "  Done: created data/*.tres"
    assert new_lines[:8] == old_lines[:8] and new_lines[11:] == old_lines[10:]


def test_mark_replaces_existing_done_line():
    new = plan.mark(PLAN, "T0.1", "done", "rewritten")
    assert "  Done: rewritten" in new and "wrote docs/architecture.md" not in new


def test_mark_preserves_crlf():
    crlf = PLAN.replace("\n", "\r\n")
    new = plan.mark(crlf, "T0.2", "in_progress", "started")
    assert "\r\n" in new and "\n" not in new.replace("\r\n", "")
    assert "- [~] **T0.2" in new


def test_mark_errors():
    with pytest.raises(KeyError):
        plan.mark(PLAN, "T9.9", "done")
    with pytest.raises(ValueError):
        plan.mark(PLAN, "T0.2", "finished")


def test_record_checkpoint_appends_feedback():
    new = plan.record_checkpoint(PLAN, "T1.2", "feels sharp, keep it", "2026-09-25")
    assert new.rstrip().endswith("  Feedback (2026-09-25): feels sharp, keep it")
    assert "- [ ] **T1.2" in new  # state untouched


def test_status_counts_per_milestone():
    counts = plan.status(plan.parse(PLAN))
    assert counts["Milestone 0: Base"] == {"todo": 1, "in_progress": 0, "done": 1, "blocked": 0}
    assert counts["Milestone 1: Driving"]["todo"] == 2
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_plan.py`
Expected: FAIL with `ImportError: cannot import name 'plan'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/plan.py`

```python
"""Read and edit docs/mvp-plan.md without disturbing hand-written lines."""

import re
from dataclasses import dataclass, field

TASK_RE = re.compile(
    r"^- \[(?P<mark>[ ~x!])\] \*\*(?P<id>T\d+(?:\.\d+)*)\s*[·:\-]\s*(?P<owner>[\w-]+)\*\*(?P<rest>.*)$"
)
DEPS_RE = re.compile(r"^\s+\*(?:Depends on|Depende de):\*\s*(?P<deps>.+)$", re.IGNORECASE)
NOTE_RE = re.compile(r"^\s+(?:Done|Hecho):", re.IGNORECASE)
ID_RE = re.compile(r"T\d+(?:\.\d+)*")
CHECKPOINT_RE = re.compile(r"CHECKPOINT|punto de control", re.IGNORECASE)
STATES = {" ": "todo", "~": "in_progress", "x": "done", "!": "blocked"}
MARKS = {state: mark for mark, state in STATES.items()}


@dataclass
class Task:
    id: str
    owner: str
    title: str
    state: str
    milestone: str
    checkpoint: bool
    depends: list[str] = field(default_factory=list)
    line: int = 0


def _eol(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _title(rest: str) -> str:
    rest = rest.strip()
    return rest.split(":", 1)[1].strip() if ":" in rest else rest


def parse(text: str) -> list[Task]:
    tasks: list[Task] = []
    milestone = ""
    current: Task | None = None
    for i, line in enumerate(text.splitlines()):
        if line.startswith("## "):
            milestone, current = line[3:].strip(), None
            continue
        m = TASK_RE.match(line)
        if m:
            current = Task(
                id=m["id"],
                owner=m["owner"],
                title=_title(m["rest"]),
                state=STATES[m["mark"]],
                milestone=milestone,
                checkpoint=bool(CHECKPOINT_RE.search(m["rest"])),
                line=i,
            )
            tasks.append(current)
            continue
        if current and line[:1] in (" ", "\t"):
            deps = DEPS_RE.match(line)
            if deps:
                current.depends.extend(ID_RE.findall(deps["deps"]))
        elif line.strip():
            current = None
    return tasks


def next_task(tasks: list[Task]) -> tuple[Task | None, str]:
    states = {t.id: t.state for t in tasks}
    pending = [t for t in tasks if t.state != "done"]
    if not pending:
        return None, "complete"
    started = [t for t in pending if t.state == "in_progress"]
    task = started[0] if started else pending[0]
    if task.state == "blocked":
        return None, f"blocked:{task.id}"
    for dep in task.depends:
        if states.get(dep) != "done":
            return task, f"waiting_on:{dep}"
    return task, "checkpoint" if task.checkpoint else "ok"


def _block_end(lines: list[str], start: int) -> int:
    """Index just after the task's indented continuation lines."""
    end = start + 1
    while end < len(lines) and lines[end][:1] in (" ", "\t") and lines[end].strip():
        end += 1
    return end


def _find(lines: list[str], task_id: str) -> int:
    for i, line in enumerate(lines):
        m = TASK_RE.match(line.rstrip("\r\n"))
        if m and m["id"] == task_id:
            return i
    raise KeyError(f"task {task_id} not found in the plan")


def mark(text: str, task_id: str, state: str, note: str | None = None) -> str:
    if state not in MARKS:
        raise ValueError(f"unknown state {state!r}; use one of {sorted(MARKS)}")
    eol = _eol(text)
    lines = text.splitlines(keepends=True)
    i = _find(lines, task_id)
    lines[i] = lines[i][:3] + MARKS[state] + lines[i][4:]
    if note:
        end = _block_end(lines, i)
        new_line = f"  Done: {note}{eol}"
        existing = [j for j in range(i + 1, end) if NOTE_RE.match(lines[j])]
        if existing:
            lines[existing[0]] = new_line
        else:
            if not lines[end - 1].endswith(("\n", "\r")):
                lines[end - 1] += eol
            lines.insert(end, new_line)
    return "".join(lines)


def record_checkpoint(text: str, task_id: str, feedback: str, date: str) -> str:
    eol = _eol(text)
    lines = text.splitlines(keepends=True)
    i = _find(lines, task_id)
    end = _block_end(lines, i)
    if not lines[end - 1].endswith(("\n", "\r")):
        lines[end - 1] += eol
    lines.insert(end, f"  Feedback ({date}): {feedback}{eol}")
    return "".join(lines)


def status(tasks: list[Task]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for t in tasks:
        bucket = counts.setdefault(t.milestone, {s: 0 for s in MARKS})
        bucket[t.state] += 1
    return counts
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_plan.py`
Expected: `11 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/plan.py mcp/tests/test_plan.py
git commit -m "feat(mcp): MVP plan parser and editor"
```

---

### Task 5: PNG writer and greybox rasterizer

**Files:**
- Create: `mcp/src/godot_kit_mcp/png.py`, `mcp/src/godot_kit_mcp/raster.py`
- Test: `mcp/tests/test_png_raster.py`

**Interfaces:**
- Produces:
  - `encode_png(width: int, height: int, rgba: bytes | bytearray) -> bytes` (8-bit RGBA, raises `ValueError` if the buffer size is wrong)
  - `decode_png(data: bytes) -> tuple[int, int, bytes]` (reads back files written by `encode_png`: filter type 0 only)
  - `parse_color(value: str) -> tuple[int, int, int, int]` (`#RRGGBB` or `#RRGGBBAA`, raises `ValueError`)
  - `Canvas(width, height)` with `.fill_rect(x, y, w, h, color)`, `.fill_shape(shape, x, y, w, h, color)` (`shape` is `"rect" | "circle" | "triangle" | "hexagon"`; the triangle points right, like the player bike), `.outline(color)` (1 px border on the shape's edge), `.get(x, y) -> tuple`, `.png() -> bytes`

- [ ] **Step 1: Write the failing test** `mcp/tests/test_png_raster.py`

```python
import pytest

from godot_kit_mcp.png import decode_png, encode_png
from godot_kit_mcp.raster import Canvas, parse_color


def test_png_round_trip():
    rgba = bytes([255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 0, 0, 0, 0])
    data = encode_png(2, 2, rgba)
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert decode_png(data) == (2, 2, rgba)


def test_png_rejects_bad_buffer():
    with pytest.raises(ValueError):
        encode_png(2, 2, b"\x00" * 3)


def test_parse_color():
    assert parse_color("#FFD23F") == (255, 210, 63, 255)
    assert parse_color("#11223380") == (17, 34, 51, 128)
    with pytest.raises(ValueError):
        parse_color("yellow")


def test_triangle_points_right():
    c = Canvas(24, 16)
    c.fill_shape("triangle", 0, 0, 24, 16, parse_color("#FFD23F"))
    assert c.get(2, 8)[3] == 255      # base, middle
    assert c.get(22, 8)[3] == 255     # tip
    assert c.get(22, 1)[3] == 0       # outside near the tip
    assert c.get(0, 0)[3] == 0 or c.get(0, 0)[3] == 255  # corner is on the edge, either is fine


def test_circle_and_outline():
    c = Canvas(10, 10)
    c.fill_shape("circle", 0, 0, 10, 10, parse_color("#111111"))
    assert c.get(5, 5) == (17, 17, 17, 255)
    assert c.get(0, 0)[3] == 0
    c.outline(parse_color("#FFFFFF"))
    assert c.get(5, 0) == (255, 255, 255, 255)  # top edge becomes outline
    assert c.get(5, 5) == (17, 17, 17, 255)     # inside unchanged


def test_canvas_png_has_size():
    c = Canvas(3, 5)
    c.fill_rect(0, 0, 3, 5, parse_color("#5C5F66"))
    w, h, rgba = decode_png(c.png())
    assert (w, h) == (3, 5) and rgba[:4] == bytes([92, 95, 102, 255])
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_png_raster.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'godot_kit_mcp.png'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/png.py`

```python
"""Minimal RGBA PNG encoder/decoder (stdlib only). Enough for greybox art."""

import struct
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def encode_png(width: int, height: int, rgba: bytes | bytearray) -> bytes:
    if len(rgba) != width * height * 4:
        raise ValueError(f"expected {width * height * 4} bytes of RGBA, got {len(rgba)}")
    stride = width * 4
    raw = b"".join(b"\x00" + bytes(rgba[y * stride:(y + 1) * stride]) for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return SIGNATURE + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b"")


def decode_png(data: bytes) -> tuple[int, int, bytes]:
    if not data.startswith(SIGNATURE):
        raise ValueError("not a PNG")
    pos, width, height, idat = len(SIGNATURE), 0, 0, b""
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        tag, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
        if tag == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif tag == b"IDAT":
            idat += body
        pos += 12 + length
    raw, stride, out = zlib.decompress(idat), width * 4, bytearray()
    for y in range(height):
        row = raw[y * (stride + 1):(y + 1) * (stride + 1)]
        if row[0] != 0:
            raise ValueError("only filter type 0 is supported")
        out += row[1:]
    return width, height, bytes(out)
```

`mcp/src/godot_kit_mcp/raster.py`:

```python
"""Tiny rasterizer for greybox shapes (spec: gdd.md visual language tables)."""

import math

from .png import encode_png

Color = tuple[int, int, int, int]


def parse_color(value: str) -> Color:
    v = value.strip().lstrip("#")
    if len(v) not in (6, 8) or any(ch not in "0123456789abcdefABCDEF" for ch in v):
        raise ValueError(f"color must be #RRGGBB or #RRGGBBAA, got {value!r}")
    r, g, b = (int(v[i:i + 2], 16) for i in (0, 2, 4))
    a = int(v[6:8], 16) if len(v) == 8 else 255
    return r, g, b, a


def _inside_polygon(px: float, py: float, pts: list[tuple[float, float]]) -> bool:
    inside, j = False, len(pts) - 1
    for i, (xi, yi) in enumerate(pts):
        xj, yj = pts[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


class Canvas:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.buf = bytearray(width * height * 4)

    def get(self, x: int, y: int) -> Color:
        i = (y * self.width + x) * 4
        return tuple(self.buf[i:i + 4])  # type: ignore[return-value]

    def _set(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 4
            self.buf[i:i + 4] = bytes(color)

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color) -> None:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._set(xx, yy, color)

    def fill_shape(self, shape: str, x: int, y: int, w: int, h: int, color: Color) -> None:
        if shape == "rect":
            self.fill_rect(x, y, w, h, color)
            return
        if shape == "circle":
            cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
            test = lambda px, py: ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1.0  # noqa: E731
        elif shape == "triangle":
            pts = [(x, y), (x + w, y + h / 2), (x, y + h)]
            test = lambda px, py: _inside_polygon(px, py, pts)  # noqa: E731
        elif shape == "hexagon":
            cx, cy = x + w / 2, y + h / 2
            pts = [(cx + w / 2 * math.cos(a), cy + h / 2 * math.sin(a)) for a in (k * math.pi / 3 for k in range(6))]
            test = lambda px, py: _inside_polygon(px, py, pts)  # noqa: E731
        else:
            raise ValueError(f"unknown shape {shape!r}; use rect, circle, triangle or hexagon")
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if test(xx + 0.5, yy + 0.5):
                    self._set(xx, yy, color)

    def outline(self, color: Color) -> None:
        edge = []
        for yy in range(self.height):
            for xx in range(self.width):
                if self.get(xx, yy)[3] == 0:
                    continue
                around = [(xx + 1, yy), (xx - 1, yy), (xx, yy + 1), (xx, yy - 1)]
                if any(not (0 <= a < self.width and 0 <= b < self.height) or self.get(a, b)[3] == 0 for a, b in around):
                    edge.append((xx, yy))
        for xx, yy in edge:
            self._set(xx, yy, color)

    def png(self) -> bytes:
        return encode_png(self.width, self.height, self.buf)
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_png_raster.py`
Expected: `6 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/png.py mcp/src/godot_kit_mcp/raster.py mcp/tests/test_png_raster.py
git commit -m "feat(mcp): stdlib PNG writer and greybox rasterizer"
```

---

### Task 6: Godot tools (find, import, tests, run scene, screenshot, export)

**Files:**
- Create: `mcp/src/godot_kit_mcp/godot.py`, `mcp/src/godot_kit_mcp/gdscript/screenshot.gd`, `mcp/tests/fixtures/min_project/project.godot`, `mcp/tests/fixtures/min_project/main.tscn`
- Test: `mcp/tests/test_godot.py`

**Interfaces:**
- Consumes: `config.resolve_tool`, `config.resolve_inside`, `proc.run`, `result.ok/fail`.
- Produces (all return `ok`/`fail` dicts):
  - `find(root: Path | None) -> dict` with `path`, `version`, `source`
  - `import_project(root: Path, timeout_s: float = 300) -> dict` with `errors`, `warnings`, `exit_code`
  - `run_tests(root: Path, test_dir: str = "res://tests", timeout_s: float = 600) -> dict` with `totals` (keys `scripts`, `tests`, `passing_tests`, `failing_tests`, `asserts` …), `failures`, `all_passed`
  - `run_scene(root: Path, scene: str, frames: int = 120, timeout_s: float = 120) -> dict` with `errors`, `warnings`, `log_tail`
  - `screenshot(root: Path, scene: str, frames: int = 30, out: str = "", width: int = 1280, height: int = 720, timeout_s: float = 120) -> dict` with `path`
  - `export(root: Path, preset: str, out_path: str, release: bool = False, timeout_s: float = 900) -> dict` with `path`
  - `parse_log(output: str) -> dict`, `parse_gut(output: str) -> dict`
  - On timeout every function returns `fail(...)` with `timed_out=True` and `log_tail`.

- [ ] **Step 1: Create the fixture project**

`mcp/tests/fixtures/min_project/project.godot`:

```ini
config_version=5

[application]

config/name="min"
config/features=PackedStringArray("4.4")
```

`mcp/tests/fixtures/min_project/main.tscn`:

```ini
[gd_scene format=3]

[node name="Main" type="Node2D"]

[node name="Box" type="ColorRect" parent="."]
offset_right = 100.0
offset_bottom = 100.0
color = Color(1, 0, 0, 1)
```

- [ ] **Step 2: Write the failing test** `mcp/tests/test_godot.py`

```python
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
```

- [ ] **Step 3: Run it and see it fail**

Run: `uv run pytest -q tests/test_godot.py`
Expected: FAIL with `ImportError: cannot import name 'godot'`.

- [ ] **Step 4: Write** `mcp/src/godot_kit_mcp/gdscript/screenshot.gd`

```gdscript
extends SceneTree
## Bundled with godot-kit-mcp. Loads a scene, waits N frames and saves the window as PNG.
##   godot --path <project> --windowed --resolution WxH -s screenshot.gd -- <res://scene.tscn> <frames> <out.png>
## Needs a display: on headless Linux run it under xvfb-run.

var _frames_left: int = 0
var _out: String = ""


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.size() < 3:
		printerr("usage: -- <res://scene.tscn> <frames> <out.png>")
		quit(2)
		return
	var packed: PackedScene = load(args[0]) as PackedScene
	if packed == null:
		printerr("cannot load scene: ", args[0])
		quit(1)
		return
	_frames_left = maxi(1, args[1].to_int())
	_out = args[2]
	root.add_child(packed.instantiate())


func _process(_delta: float) -> bool:
	if _out.is_empty():
		return false
	_frames_left -= 1
	if _frames_left > 0:
		return false
	var err: Error = root.get_texture().get_image().save_png(_out)
	if err != OK:
		printerr("cannot save png: ", error_string(err))
		quit(1)
	else:
		quit(0)
	_out = ""
	return false
```

- [ ] **Step 5: Implement** `mcp/src/godot_kit_mcp/godot.py`

```python
"""Godot 4 from the command line: find, import, GUT tests, run, screenshot, export."""

import re
import time
from importlib.resources import as_file, files
from pathlib import Path

from . import config, proc
from .result import fail, ok

ANSI = re.compile(r"\x1b\[[0-9;]*m")
ERROR_RE = re.compile(r"^\s*(SCRIPT ERROR|USER ERROR|ERROR):")
WARNING_RE = re.compile(r"^\s*(USER WARNING|WARNING):")
GUT_TOTAL_RE = re.compile(r"^(Scripts|Tests|Passing Tests|Failing Tests|Pending|Risky/Pending|Asserts)\s+(\d+)$")
MISSING = "Godot not found. Install Godot 4, or set [tools].godot in .godot-kit.toml, or GODOT_BIN."


def clean(output: str) -> str:
    return ANSI.sub("", output)


def tail(output: str, lines: int = 60) -> str:
    return "\n".join(clean(output).splitlines()[-lines:])


def parse_log(output: str) -> dict:
    lines = clean(output).splitlines()
    return {
        "errors": [line.strip() for line in lines if ERROR_RE.match(line)],
        "warnings": [line.strip() for line in lines if WARNING_RE.match(line)],
    }


def parse_gut(output: str) -> dict:
    text = clean(output)
    totals: dict[str, int] = {}
    failures: list[str] = []
    current = ""
    for raw in text.splitlines():
        line = raw.strip()
        m = GUT_TOTAL_RE.match(line)
        if m:
            totals[m[1].lower().replace(" ", "_").replace("/", "_")] = int(m[2])
        elif line.startswith("* "):
            current = line[2:]
        elif "[Failed]" in line:
            failures.append(f"{current}: {line}")
    return {"totals": totals, "failures": failures, "all_passed": "All tests passed" in text}


def _exe(root: Path | None) -> tuple[config.ToolPath, dict | None]:
    t = config.resolve_tool("godot", root)
    if t.path is None:
        return t, fail(MISSING)
    if not t.path.exists():
        return t, fail(f"Godot path from {t.source} does not exist: {t.path}")
    return t, None


def _run(root: Path, args: list[str], timeout_s: float) -> tuple[proc.ProcResult | None, dict | None]:
    t, err = _exe(root)
    if err:
        return None, err
    return proc.run([str(t.path), *args], timeout_s, cwd=root), None


def _timed_out(r: proc.ProcResult, what: str, timeout_s: float) -> dict:
    return fail(
        f"{what} timed out after {timeout_s:g}s (Godot may be stuck on a script error)",
        timed_out=True,
        log_tail=tail(r.output),
    )


def find(root: Path | None) -> dict:
    t, err = _exe(root)
    if err:
        return err
    r = proc.run([str(t.path), "--version"], 30)
    lines = clean(r.output).strip().splitlines()
    version = lines[-1].strip() if lines else ""
    return ok(f"Godot {version} at {t.path}", path=str(t.path), version=version, source=t.source)


def import_project(root: Path, timeout_s: float = 300) -> dict:
    r, err = _run(root, ["--headless", "--editor", "--quit", "--path", str(root)], timeout_s)
    if err:
        return err
    if r.timed_out:
        return _timed_out(r, "Import", timeout_s)
    log = parse_log(r.output)
    good = r.code == 0 and not log["errors"]
    summary = f"Import {'clean' if good else 'failed'}: {len(log['errors'])} errors, {len(log['warnings'])} warnings"
    return (ok if good else fail)(summary, exit_code=r.code, **log)


def run_tests(root: Path, test_dir: str = "res://tests", timeout_s: float = 600) -> dict:
    if not (root / "addons/gut/gut_cmdln.gd").is_file():
        return fail("GUT is not installed (addons/gut/gut_cmdln.gd is missing)")
    args = ["--headless", "--path", str(root), "-s", "addons/gut/gut_cmdln.gd",
            f"-gdir={test_dir}", "-ginclude_subdirs", "-gexit"]
    r, err = _run(root, args, timeout_s)
    if err:
        return err
    if r.timed_out:
        return _timed_out(r, "Tests", timeout_s)
    g = parse_gut(r.output)
    t = g["totals"]
    good = r.code == 0 and g["all_passed"]
    summary = f"{t.get('passing_tests', 0)}/{t.get('tests', 0)} tests passed"
    extra = {} if good else {"log_tail": tail(r.output)}
    return (ok if good else fail)(summary, exit_code=r.code, **g, **extra)


def run_scene(root: Path, scene: str, frames: int = 120, timeout_s: float = 120) -> dict:
    r, err = _run(root, ["--headless", "--path", str(root), scene, "--quit-after", str(frames)], timeout_s)
    if err:
        return err
    if r.timed_out:
        return _timed_out(r, f"Scene {scene}", timeout_s)
    log = parse_log(r.output)
    good = r.code == 0 and not log["errors"]
    summary = f"Ran {scene} for {frames} frames: {len(log['errors'])} errors, {len(log['warnings'])} warnings"
    return (ok if good else fail)(summary, exit_code=r.code, log_tail=tail(r.output), **log)


def screenshot(root: Path, scene: str, frames: int = 30, out: str = "", width: int = 1280,
               height: int = 720, timeout_s: float = 120) -> dict:
    if out:
        target = config.resolve_inside(root, out)
    else:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        target = root / ".godot-kit" / "screenshots" / f"{Path(scene).stem}-{stamp}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.unlink(missing_ok=True)
    with as_file(files("godot_kit_mcp") / "gdscript" / "screenshot.gd") as script:
        args = ["--path", str(root), "--windowed", "--resolution", f"{width}x{height}",
                "-s", str(script), "--", scene, str(frames), str(target)]
        r, err = _run(root, args, timeout_s)
    if err:
        return err
    if r.timed_out:
        return _timed_out(r, "Screenshot", timeout_s)
    if r.code != 0 or not target.is_file():
        return fail("Screenshot failed. It needs a display (on headless Linux use xvfb-run).",
                    log_tail=tail(r.output))
    return ok(f"Screenshot saved to {target}", path=str(target))


def export(root: Path, preset: str, out_path: str, release: bool = False, timeout_s: float = 900) -> dict:
    if not (root / "export_presets.cfg").is_file():
        return fail("No export_presets.cfg: create the preset in the Godot editor first (Project > Export).")
    target = config.resolve_inside(root, out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    flag = "--export-release" if release else "--export-debug"
    r, err = _run(root, ["--headless", "--path", str(root), flag, preset, str(target)], timeout_s)
    if err:
        return err
    if r.timed_out:
        return _timed_out(r, "Export", timeout_s)
    if r.code != 0 or not target.exists():
        return fail(f"Export of preset {preset!r} failed", log_tail=tail(r.output))
    return ok(f"Exported {preset!r} to {target}", path=str(target))
```

- [ ] **Step 6: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_godot.py`
Expected: all pass. With Godot installed, the two `godot` integration tests run (a window opens briefly for the screenshot); without it they are skipped.

- [ ] **Step 7: Commit**

```bash
git add mcp/src/godot_kit_mcp/godot.py mcp/src/godot_kit_mcp/gdscript mcp/tests/test_godot.py mcp/tests/fixtures
git commit -m "feat(mcp): Godot tools with timeouts, GUT parsing and screenshots"
```

---

### Task 7: Asset tools (greybox art, Tiled export, Pixelorama)

**Files:**
- Create: `mcp/src/godot_kit_mcp/assets.py`
- Test: `mcp/tests/test_assets.py`

**Interfaces:**
- Consumes: `raster.Canvas`, `raster.parse_color`, `config.resolve_inside`, `config.resolve_tool`, `proc.run`, `godot._run`, `godot.tail`.
- Produces:
  - `greybox_tileset(root: Path, out: str, tiles: list[dict], tile_size: int = 32, columns: int = 8) -> dict`; `tiles` items are `{"name": str, "color": "#RRGGBB"}`; the result has `path` and `atlas` (`{name: [col, row]}`)
  - `greybox_sprite(root: Path, out: str, shape: str, color: str, width: int, height: int, outline: str = "") -> dict` with `path`
  - `tiled_export(root: Path, tmx: str, out: str, tileset: str, timeout_s: float = 180) -> dict` (runs `godot --headless --path <root> --import`, then `godot --headless --path <root> -s res://tools/tiled_to_godot.gd -- <tmx> <out> <tileset>`; fails clearly when the project has no converter)
  - `pixelorama_open(root: Path | None, path: str) -> dict` (starts Pixelorama detached with the file)

- [ ] **Step 1: Write the failing test** `mcp/tests/test_assets.py`

```python
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
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_assets.py`
Expected: FAIL with `ImportError: cannot import name 'assets'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/assets.py`

```python
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
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_assets.py`
Expected: `7 passed` (the two stub tests are skipped on Windows).

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/assets.py mcp/tests/test_assets.py
git commit -m "feat(mcp): greybox art, Tiled export and Pixelorama tools"
```

---

### Task 8: ElevenLabs with a hard credit reserve

**Files:**
- Create: `mcp/src/godot_kit_mcp/elevenlabs.py`
- Test: `mcp/tests/test_elevenlabs.py`

**Interfaces:**
- Consumes: `config.resolve_inside`, `result.ok/fail`.
- Produces:
  - `Http = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]` (method, url, headers, body) → (status, body); `default_http` uses `urllib`
  - `estimate_sfx(seconds: float) -> int` (40/s, rounded up), `estimate_music(seconds: float) -> int` (7/s, rounded up)
  - `balance(api_key: str, http: Http = default_http) -> int` (`character_limit - character_count`)
  - `pending_estimates(ledger_text: str, now: datetime) -> int` (estimates from ledger rows of the last 120 s)
  - `generate(kind: str, *, root: Path, out: str, prompt: str, seconds: float, reserve: int, api_key: str | None, loop: bool = False, http: Http = default_http, now: datetime | None = None) -> dict`; `kind` is `"sfx"` or `"music"`; the result has `path`, `estimate`, `balance_before`
  - Ledger file: `docs/audio-ledger.md`, a Markdown table: `| time (UTC) | kind | file | seconds | estimate | balance before |`

- [ ] **Step 1: Write the failing test** `mcp/tests/test_elevenlabs.py`

```python
import json
from datetime import UTC, datetime, timedelta

from godot_kit_mcp import elevenlabs

KEY = "sk_test_secret_value"
NOW = datetime(2026, 9, 25, 13, 0, 0, tzinfo=UTC)


class FakeHttp:
    def __init__(self, balances, status=200):
        self.balances, self.status, self.calls = list(balances), status, []

    def __call__(self, method, url, headers, body):
        self.calls.append({"method": method, "url": url, "headers": headers,
                           "json": json.loads(body) if body else None})
        if url.endswith("/v1/user/subscription"):
            left = self.balances.pop(0)
            return 200, json.dumps({"character_limit": 10000, "character_count": 10000 - left}).encode()
        return self.status, b"ID3-fake-audio"


def _gen(project, http, **kw):
    args = dict(root=project, out="assets/audio/sfx/horn.mp3", prompt="scooter horn, two short beeps",
                seconds=1.0, reserve=1500, api_key=KEY, http=http, now=NOW)
    args.update(kw)
    return elevenlabs.generate("sfx", **args)


def test_estimates():
    assert elevenlabs.estimate_sfx(1.2) == 48
    assert elevenlabs.estimate_music(42) == 294


def test_generates_writes_file_and_ledger(project):
    http = FakeHttp([4444])
    r = _gen(project, http)
    assert r["ok"], r
    assert (project / "assets/audio/sfx/horn.mp3").read_bytes() == b"ID3-fake-audio"
    ledger = (project / "docs/audio-ledger.md").read_text(encoding="utf-8")
    assert "| 2026-09-25T13:00:00Z | sfx | assets/audio/sfx/horn.mp3 | 1.0 | 40 | 4444 |" in ledger
    gen = http.calls[1]
    assert gen["url"].startswith("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128")
    assert gen["json"]["duration_seconds"] == 1.0 and gen["json"]["model_id"] == "eleven_text_to_sound_v2"
    assert gen["headers"]["xi-api-key"] == KEY
    assert KEY not in ledger and KEY not in json.dumps(r)


def test_refuses_below_reserve_without_calling_generation(project):
    http = FakeHttp([1520])
    r = _gen(project, http)
    assert r["ok"] is False and "reserve" in r["summary"]
    assert len(http.calls) == 1 and not (project / "assets/audio/sfx/horn.mp3").exists()


def test_recent_charges_count_against_balance(project):
    http = FakeHttp([1560, 1560])  # the API has not shown the first charge yet: 1560 - 40 pending - 40 < 1500
    assert _gen(project, http)["ok"]
    r = _gen(project, http, out="assets/audio/sfx/horn2.mp3", now=NOW + timedelta(seconds=30))
    assert r["ok"] is False and "reserve" in r["summary"]


def test_old_ledger_rows_do_not_count(project):
    http = FakeHttp([4444, 4404])
    assert _gen(project, http)["ok"]
    later = _gen(project, http, out="assets/audio/sfx/b.mp3", now=NOW + timedelta(minutes=5))
    assert later["ok"]


def test_missing_key_and_api_error(project):
    assert "ELEVENLABS_API_KEY" in _gen(project, FakeHttp([4444]), api_key=None)["summary"]
    r = _gen(project, FakeHttp([4444], status=401))
    assert r["ok"] is False and not (project / "docs/audio-ledger.md").exists()


def test_music_request_shape(project):
    http = FakeHttp([4444])
    r = elevenlabs.generate("music", root=project, out="assets/audio/music/a.mp3", prompt="instrumental merengue",
                            seconds=42, reserve=1500, api_key=KEY, http=http, now=NOW)
    assert r["ok"] and r["estimate"] == 294
    body = http.calls[1]["json"]
    assert body == {"prompt": "instrumental merengue", "music_length_ms": 42000,
                    "model_id": "music_v1", "force_instrumental": True}


def test_duration_limits(project):
    assert _gen(project, FakeHttp([4444]), seconds=31)["ok"] is False
    assert _gen(project, FakeHttp([4444]), seconds=0.2)["ok"] is False
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_elevenlabs.py`
Expected: FAIL with `ImportError: cannot import name 'elevenlabs'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/elevenlabs.py`

```python
"""ElevenLabs sound effects and music, guarded by a credit reserve and a ledger."""

import json
import math
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from . import config
from .result import fail, ok

API = "https://api.elevenlabs.io"
SFX_CREDITS_PER_S = 40
MUSIC_CREDITS_PER_S = 7  # measured 2026-09-25: 288 credits per ~42 s track
PENDING_WINDOW = timedelta(seconds=120)  # the balance takes ~60 s to show a charge
LEDGER = "docs/audio-ledger.md"
LEDGER_HEADER = (
    "# ElevenLabs ledger\n\n"
    "| time (UTC) | kind | file | seconds | estimate | balance before |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)
LIMITS = {"sfx": (0.5, 30.0), "music": (3.0, 300.0)}
TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

Http = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]


def default_http(method: str, url: str, headers: dict[str, str], body: bytes | None) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def estimate_sfx(seconds: float) -> int:
    return math.ceil(SFX_CREDITS_PER_S * seconds)


def estimate_music(seconds: float) -> int:
    return math.ceil(MUSIC_CREDITS_PER_S * seconds)


def balance(api_key: str, http: Http = default_http) -> int:
    status, body = http("GET", f"{API}/v1/user/subscription", {"xi-api-key": api_key}, None)
    if status != 200:
        raise RuntimeError(f"balance request failed with HTTP {status} (the key needs the user_read permission)")
    data = json.loads(body)
    return int(data["character_limit"]) - int(data["character_count"])


def pending_estimates(ledger_text: str, now: datetime) -> int:
    total = 0
    for line in ledger_text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            continue
        try:
            when = datetime.strptime(cells[0], TIME_FMT).replace(tzinfo=UTC)
            estimate = int(cells[4])
        except ValueError:
            continue
        if now - when < PENDING_WINDOW:
            total += estimate
    return total


def _request(kind: str, prompt: str, seconds: float, loop: bool) -> tuple[str, dict]:
    if kind == "sfx":
        return f"{API}/v1/sound-generation?output_format=mp3_44100_128", {
            "text": prompt, "duration_seconds": seconds, "loop": loop,
            "prompt_influence": 0.6, "model_id": "eleven_text_to_sound_v2",
        }
    return f"{API}/v1/music?output_format=mp3_44100_128", {
        "prompt": prompt, "music_length_ms": int(seconds * 1000),
        "model_id": "music_v1", "force_instrumental": True,
    }


def generate(kind: str, *, root: Path, out: str, prompt: str, seconds: float, reserve: int,
             api_key: str | None, loop: bool = False, http: Http = default_http,
             now: datetime | None = None) -> dict:
    if kind not in LIMITS:
        return fail(f"kind must be 'sfx' or 'music', got {kind!r}")
    low, high = LIMITS[kind]
    if not low <= seconds <= high:
        return fail(f"{kind} duration must be between {low:g} and {high:g} seconds")
    if not api_key:
        return fail("Set the ELEVENLABS_API_KEY environment variable (never put the key in a file).")
    try:
        target = config.resolve_inside(root, out)
    except ValueError as exc:
        return fail(str(exc))
    now = now or datetime.now(UTC)
    estimate = estimate_sfx(seconds) if kind == "sfx" else estimate_music(seconds)
    ledger_path = root / LEDGER
    ledger_text = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    before = balance(api_key, http)
    available = before - pending_estimates(ledger_text, now)
    if available - estimate < reserve:
        return fail(f"Refused: {available} credits available, this costs ~{estimate}, "
                    f"and the reserve is {reserve}.", balance=before, estimate=estimate)
    url, payload = _request(kind, prompt, seconds, loop)
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    status, body = http("POST", url, headers, json.dumps(payload).encode())
    if status != 200:
        return fail(f"ElevenLabs returned HTTP {status}: {body[:300].decode('utf-8', 'replace')}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    rel = target.relative_to(root.resolve()).as_posix()
    row = f"| {now.strftime(TIME_FMT)} | {kind} | {rel} | {seconds} | {estimate} | {before} |\n"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text((ledger_text or LEDGER_HEADER) + row, encoding="utf-8")
    return ok(f"Generated {rel} (~{estimate} credits, balance was {before})",
              path=str(target), estimate=estimate, balance_before=before)
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_elevenlabs.py`
Expected: `8 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/elevenlabs.py mcp/tests/test_elevenlabs.py
git commit -m "feat(mcp): ElevenLabs generation with credit reserve and ledger"
```

---

### Task 9: Intake questionnaire and project scaffold

**Files:**
- Create: `mcp/src/godot_kit_mcp/intake.py`
- Test: `mcp/tests/test_intake.py`

**Interfaces:**
- Produces:
  - `QUESTIONS: list[dict]` (12 items, each `{"id", "question", "options", "recommended"}`; `options` may be empty for free text)
  - `Fetch = Callable[[str], bytes]`; `default_fetch` uses `urllib` with a `User-Agent`
  - `pick_gut_release(releases: list[dict], godot_version: str) -> tuple[dict, bool]` (the bool is `True` when `target_commitish == "godot_<major>_<minor>"`)
  - `install_gut(target: Path, godot_version: str, fetch: Fetch = default_fetch) -> dict`
  - `scaffold(target: Path, answers: dict[str, str], template_dir: Path, godot_version: str, fetch: Fetch = default_fetch) -> dict` (refuses a non-empty target; fills `{{key}}` placeholders in text files; lists placeholders left unfilled; installs GUT)
  - Placeholder keys used by the template (later plan): `game_name`, `pitch`, `genre`, `core_loop`, `platforms`, `session_length`, `art_direction`, `narrative`, `maps`, `audio`, `languages`, `out_of_scope`, `first_checkpoint`

- [ ] **Step 1: Write the failing test** `mcp/tests/test_intake.py`

```python
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
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_intake.py`
Expected: FAIL with `ImportError: cannot import name 'intake'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/intake.py`

```python
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
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_intake.py`
Expected: `6 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/intake.py mcp/tests/test_intake.py
git commit -m "feat(mcp): intake questionnaire and project scaffold with GUT download"
```

---

### Task 10: Knowledge search

**Files:**
- Create: `mcp/src/godot_kit_mcp/knowledge.py`
- Test: `mcp/tests/test_knowledge.py`

**Interfaces:**
- Produces:
  - `Card(name: str, topic: str, confidence: str, path: Path, body: str)`
  - `parse_card(text: str) -> tuple[dict[str, str], str]` (YAML-like front matter between the first two `---` lines, `key: value` only; returns `({}, text)` without front matter)
  - `load_cards(root: Path) -> list[Card]` (all `*.md` under `root`; the card name falls back to the file stem)
  - `search(cards: list[Card], query: str, topic: str = "", limit: int = 10) -> list[dict]` (each hit: `name`, `topic`, `confidence`, `path`, `preview`, `score`; best first)
  - `get(cards: list[Card], name: str) -> Card | None`
  - `default_root() -> Path | None` (`config.kit_root() / "knowledge" / "cards"` if it exists)

- [ ] **Step 1: Write the failing test** `mcp/tests/test_knowledge.py`

```python
from godot_kit_mcp import knowledge

PALETTES = """---
name: pixel-art-palettes
topic: pixel-art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 40-52)"]
---
## Rules
- Use 3-5 shades per material ramp. WHY: fewer shades read clearly at small sizes.
## Checklist
- [ ] Silhouette readable in black
"""

CAMERA = """---
name: camera-look-ahead
topic: game-feel
confidence: opinion
---
## Rules
- Offset the camera toward the velocity by 20-30% of the screen. WHY: players see what comes.
"""


def _cards(tmp_path):
    (tmp_path / "pixel-art").mkdir()
    (tmp_path / "game-feel").mkdir()
    (tmp_path / "pixel-art/pixel-art-palettes.md").write_text(PALETTES, encoding="utf-8")
    (tmp_path / "game-feel/camera-look-ahead.md").write_text(CAMERA, encoding="utf-8")
    return knowledge.load_cards(tmp_path)


def test_parse_card():
    meta, body = knowledge.parse_card(PALETTES)
    assert meta["name"] == "pixel-art-palettes" and meta["topic"] == "pixel-art"
    assert body.startswith("## Rules")
    assert knowledge.parse_card("no front matter") == ({}, "no front matter")


def test_search_ranks_and_previews(tmp_path):
    hits = knowledge.search(_cards(tmp_path), "palette shades")
    assert hits[0]["name"] == "pixel-art-palettes"
    assert hits[0]["preview"].startswith("- Use 3-5 shades")
    assert len(hits) == 1


def test_search_topic_filter_and_empty(tmp_path):
    cards = _cards(tmp_path)
    assert knowledge.search(cards, "camera", topic="pixel-art") == []
    assert [h["name"] for h in knowledge.search(cards, "camera", topic="game-feel")] == ["camera-look-ahead"]
    assert knowledge.search(cards, "   ") == []


def test_get(tmp_path):
    cards = _cards(tmp_path)
    assert knowledge.get(cards, "camera-look-ahead").confidence == "opinion"
    assert knowledge.get(cards, "missing") is None
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_knowledge.py`
Expected: FAIL with `ImportError: cannot import name 'knowledge'`.

- [ ] **Step 3: Implement** `mcp/src/godot_kit_mcp/knowledge.py`

```python
"""Keyword search over knowledge/cards (distilled, reviewed game-dev rules)."""

import re
from dataclasses import dataclass
from pathlib import Path

from . import config

WORD_RE = re.compile(r"[a-z0-9]{2,}")


@dataclass
class Card:
    name: str
    topic: str
    confidence: str
    path: Path
    body: str


def parse_card(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            meta = {}
            for line in lines[1:end]:
                key, sep, value = line.partition(":")
                if sep:
                    meta[key.strip()] = value.strip()
            return meta, "\n".join(lines[end + 1:]).lstrip("\n")
    return {}, text


def load_cards(root: Path) -> list[Card]:
    cards = []
    for path in sorted(root.rglob("*.md")):
        meta, body = parse_card(path.read_text(encoding="utf-8"))
        cards.append(Card(meta.get("name", path.stem), meta.get("topic", path.parent.name),
                          meta.get("confidence", ""), path, body))
    return cards


def _preview(body: str) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.lower().startswith("## rules") and i + 1 < len(lines):
            return lines[i + 1][:200]
    return (lines[0] if lines else "")[:200]


def search(cards: list[Card], query: str, topic: str = "", limit: int = 10) -> list[dict]:
    terms = set(WORD_RE.findall(query.lower()))
    if not terms:
        return []
    hits = []
    for card in cards:
        if topic and card.topic != topic:
            continue
        name, top, body = card.name.lower(), card.topic.lower(), card.body.lower()
        score = sum(3 * name.count(t) + 2 * top.count(t) + min(body.count(t), 5) for t in terms)
        if score:
            hits.append({"name": card.name, "topic": card.topic, "confidence": card.confidence,
                         "path": str(card.path), "preview": _preview(card.body), "score": score})
    hits.sort(key=lambda h: (-h["score"], h["name"]))
    return hits[:limit]


def get(cards: list[Card], name: str) -> Card | None:
    return next((c for c in cards if c.name == name), None)


def default_root() -> Path | None:
    kit = config.kit_root()
    folder = kit / "knowledge" / "cards" if kit else None
    return folder if folder and folder.is_dir() else None
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `uv run pytest -q tests/test_knowledge.py`
Expected: `4 passed`.

- [ ] **Step 5: Commit**

```bash
git add mcp/src/godot_kit_mcp/knowledge.py mcp/tests/test_knowledge.py
git commit -m "feat(mcp): knowledge card search"
```

---

### Task 11: Wire the 21 tools, plugin manifest and smoke test

**Files:**
- Modify: `mcp/src/godot_kit_mcp/server.py` (replace the whole file)
- Create: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `knowledge/cards/.gitkeep`
- Test: `mcp/tests/test_server.py`

**Interfaces:**
- Consumes: every module above.
- Produces: the MCP tools, with exactly these names: `godot_find`, `godot_import`, `godot_test`, `godot_run_scene`, `godot_screenshot`, `godot_export`, `tiled_export`, `greybox_tileset`, `greybox_sprite`, `pixelorama_open`, `elevenlabs_balance`, `elevenlabs_sfx`, `elevenlabs_music`, `plan_status`, `plan_next_task`, `plan_mark`, `checkpoint_record`, `intake_questions`, `project_scaffold`, `knowledge_search`, `knowledge_get`. Every tool takes `project_dir: str = "."` where it needs a project. The plan tools read and write the plan file as bytes, so CRLF survives.

- [ ] **Step 1: Write the failing test** `mcp/tests/test_server.py`

```python
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
```

- [ ] **Step 2: Run it and see it fail**

Run: `uv run pytest -q tests/test_server.py`
Expected: FAIL: `test_exactly_the_spec_tools` finds no tools, and `call()` fails on unknown tools.

- [ ] **Step 3: Replace** `mcp/src/godot_kit_mcp/server.py`

```python
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
```

- [ ] **Step 4: Run the whole suite**

Run: `uv run pytest -q`
Expected: every test passes (Godot integration tests run only when Godot is found).

- [ ] **Step 5: Create the plugin manifests** (repo root)

`.claude-plugin/plugin.json`:

```json
{
  "name": "godot-kit",
  "version": "0.1.0",
  "description": "Agents, commands and an MCP server to take a 2D game idea to a playable MVP with Godot 4, GDScript, Tiled and Pixelorama.",
  "license": "MIT",
  "mcpServers": {
    "godot-kit": {
      "command": "uvx",
      "args": ["--from", "${CLAUDE_PLUGIN_ROOT}/mcp", "godot-kit-mcp"],
      "env": { "GODOT_KIT_ROOT": "${CLAUDE_PLUGIN_ROOT}" }
    }
  }
}
```

`.claude-plugin/marketplace.json`:

```json
{
  "name": "desarrollo-godot-kit",
  "owner": { "name": "desarrollo-godot-kit contributors" },
  "plugins": [
    {
      "name": "godot-kit",
      "source": "./",
      "description": "Godot 4 + GDScript MVP kit: agents in a /loop with checkpoints, plus the godot-kit MCP server."
    }
  ]
}
```

`knowledge/cards/.gitkeep`: empty file.

- [ ] **Step 6: Smoke test against a real project**

Run from `mcp/` (with Motoconcho's path; skip the Godot calls if an agent is working in that repo right now, because import writes its `.godot/` cache):

```bash
uv run python - <<'EOF'
import asyncio, json
from godot_kit_mcp.server import server
P = "/Users/usuario/repos/motoconcho-kit"
for name, args in [("godot_find", {"project_dir": P}), ("plan_status", {"project_dir": P}),
                   ("plan_next_task", {"project_dir": P}), ("godot_test", {"project_dir": P})]:
    r = asyncio.run(server.call_tool(name, args))
    print(name, json.loads(r.content[0].text)["summary"])
EOF
```

Expected: `godot_find` prints the Godot 4.7 path; `plan_status` prints the done/total count of Motoconcho's plan; `plan_next_task` prints its next task; `godot_test` prints `N/N tests passed`.

Then check that the server starts over stdio: `uvx --from . godot-kit-mcp` must start and wait for input without errors (stop it with Ctrl+C).

- [ ] **Step 7: Commit**

```bash
git add mcp/src/godot_kit_mcp/server.py mcp/tests/test_server.py .claude-plugin knowledge/cards/.gitkeep
git commit -m "feat(mcp): wire the 21 tools and add the plugin manifest"
```

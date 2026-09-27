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

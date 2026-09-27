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

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

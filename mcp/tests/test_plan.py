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
    assert new_lines[7] == "- [x] **T0.2 · game-designer**: Resources."
    assert new_lines[9] == "  Done: created data/*.tres"
    assert new_lines[:7] == old_lines[:7]          # todo antes de T0.2 intacto
    assert new_lines[8] == old_lines[8]            # la línea *Depends on:* no se toca
    assert new_lines[10:] == old_lines[9:]         # el resto solo se desplaza por la nueva línea Done:


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

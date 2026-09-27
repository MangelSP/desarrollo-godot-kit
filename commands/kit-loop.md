---
description: Run one turn of the Godot Kit development loop — advance the plan by one task, or stop cleanly at a checkpoint. Meant to be driven by /loop.
---

# `/godot-kit:kit-loop`

One turn of the MVP build loop. Intended to be run repeatedly via `/loop /godot-kit:kit-loop`, self-paced, one task per turn, stopping cleanly at every checkpoint.

## Steps

1. Delegate the entire turn to the `orchestrator` agent. It will:
   - call `plan_next_task`;
   - if the result is a checkpoint, a blocked task, or "plan complete" — stop and report to the human instead of proceeding;
   - otherwise delegate the task to its owner agent (bringing in `game-designer` first if a needed number is missing), run `godot_import` and `godot_test`, run `qa-tester` and `code-reviewer`, call `plan_mark`, and commit only the task's own paths.
2. Relay the orchestrator's two-line turn summary to the human as this command's output. Don't add commentary beyond what the orchestrator reports — it already did the verification.

## When the orchestrator stops the loop

Report clearly which of these happened, and what the human needs to do next:

- **Checkpoint reached**: show the checkpoint's brief (what to try, what to approve) and wait.
- **Task blocked**: show the task id and the blocking reason.
- **Two consecutive verification failures**: show the task id and the last failure output; it needs human or design attention.
- **Plan complete**: congratulate briefly and suggest `/godot-kit:kit-status` for the final picture.

Do not start a second task in the same turn, even if the first one closed cleanly and the next one looks trivial — one task per turn keeps `/loop` checkpoint-safe.

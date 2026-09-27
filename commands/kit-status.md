---
description: Read-only summary of MVP progress — milestone counts, recent commits, blockers, and the next checkpoint.
---

# `/godot-kit:kit-status`

A quick, read-only status check. No delegation to programming or design agents, no plan edits.

## Steps

1. Delegate to `reporter`, which reads `plan_status` and recent git history and returns a short summary: milestone progress, recent activity, any blocked task, and the next pending checkpoint.
2. Relay that summary to the human as-is.

Use this any time you want a status snapshot without advancing the loop.

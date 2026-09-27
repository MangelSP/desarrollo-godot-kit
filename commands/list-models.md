---
description: Show the model and effort each Godot Kit agent is currently set to.
---

# /godot-kit:list-models

Show, in one table, which model and effort each of the 15 Godot Kit agents runs on right now.

## What to do

1. Find the plugin's `agents/` directory (the plugin install path, or `./agents/` when this kit repo is the working directory).
2. For every `*.md` in it, read the frontmatter `name`, `model`, and `effort`.
3. Print a table sorted by name: `agent · model · effort`. Show `—` where effort is absent (agents that don't set it use the default).
4. Below the table, print the current "profile" if it matches a known one:
   - **default**: orchestrator/game-architect/code-reviewer on opus·high, game-designer on opus·medium, executors on sonnet·medium, reporter on haiku·low.
   - **all-opus**: every agent on opus.
   - **budget**: orchestrator on opus, architect/reviewer on sonnet, the rest on haiku.
   Otherwise say "custom".
5. Remind the user they can change any of them with `/godot-kit:set-model <agent|all> [model] [effort]`.

Read-only: do not edit any file.

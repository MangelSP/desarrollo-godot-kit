---
description: Change the model and/or effort of one Godot Kit agent (or all), by editing the agent's frontmatter.
argument-hint: <agent-name|all> [model] [effort]
---

# /godot-kit:set-model

Change which model and effort a Godot Kit agent runs on. In Claude Code an agent's model lives in the `model:` / `effort:` fields of its `.md` frontmatter, so this command edits those fields directly — there is no central override.

## Arguments

`$ARGUMENTS` = `<agent-name|all> [model] [effort]`

- **agent-name**: one of the 15 agents (`orchestrator`, `producer`, `game-architect`, `game-designer`, `narrative-writer`, `ux-ui-designer`, `ui-programmer`, `gameplay-programmer`, `ai-programmer`, `level-designer`, `technical-artist`, `audio-designer`, `qa-tester`, `code-reviewer`, `reporter`), or `all` to change every agent.
- **model** (optional): `opus`, `sonnet`, `haiku`, `fable`, `inherit`, or a full model id. Omit to leave the model unchanged.
- **effort** (optional): `low`, `medium`, `high`, `xhigh`, `max`. Omit to leave effort unchanged. Use `none` to remove the effort field.

## What to do

1. Find the plugin's `agents/` directory. In an installed plugin the agents live under the plugin's install path; if this repo is the working directory, they are in `./agents/`. Locate the target agent file(s).
2. Parse `$ARGUMENTS`. If no model and no effort are given, just show the agent's current `model`/`effort` and stop.
3. Validate: model must be one of the allowed values or a plausible full model id; effort must be one of the allowed levels (or `none`). If invalid, say so and stop — do not guess.
4. Edit the frontmatter of each target file with the Edit tool:
   - Replace the `model:` line's value (add the line under `name:` if it is missing).
   - Replace the `effort:` line's value; if effort is `none`, remove the line; if effort is given and the line is missing, add it.
   - Change ONLY those lines. Never touch the body or other frontmatter fields.
5. For `all`, apply the same model/effort to every agent (useful for "make everything opus" or "everything haiku for a cheap dry run").
6. Report a table of what changed: agent → old (model, effort) → new (model, effort).

## Notes

- Plugin agent files may be read-only if installed under a managed plugin path. If an edit is refused, tell the user to run this against a local copy of the kit, or to copy the agent into `.claude/agents/` and edit there (a project-level agent overrides the plugin one).
- Guardrail: warn (do not block) if the user sets `orchestrator` or `code-reviewer` below `sonnet` — those roles carry the plan and the reviews, and a weak model there degrades the whole loop.
- After changing models, the new setting applies to the NEXT time that agent is dispatched, not to any run already in flight.

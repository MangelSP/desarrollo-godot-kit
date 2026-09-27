---
description: Start a new 2D Godot game from a questionnaire — draft the GDD, get human approval, write architecture and the MVP plan, and scaffold the project.
---

# `/godot-kit:new-game`

Take a game idea from nothing to a scaffolded, playable-skeleton Godot 4 project with an approved GDD, an architecture doc, and an MVP plan ready for `/godot-kit:kit-loop`.

## Steps

1. Call `mcp__godot-kit__intake_questions` to get the questionnaire (12 questions, each multiple-choice with a recommended option, per the design spec §7).
2. Ask the human **one question at a time**, in order, showing the recommended option and letting them pick another or answer freely. Don't batch all 12 into one message — that defeats the point of a guided intake. Record each answer.
3. Once all 12 are answered, delegate to `game-designer` with the full set of answers to draft `docs/gdd.md`: pitch, genre/camera, core loop, platforms, session length, art direction, narrative yes/no, maps yes/no, audio approach, language(s), explicit non-goals, and the first checkpoint target.
4. **CHECKPOINT 0**: present the drafted GDD to the human and stop. Do not proceed until they approve it or ask for changes. If they ask for changes, send them back to `game-designer` and re-present.
5. Once approved, delegate to `game-architect` to write `docs/architecture.md` and any initial ADRs from the approved GDD.
6. Delegate to `producer` to write `docs/mvp-plan.md`: milestones and tasks with acceptance criteria, each owned by exactly one agent, with checkpoints placed sensibly (at minimum, one near the end of the MVP).
7. Call `mcp__godot-kit__project_scaffold` with the target directory and the intake answers to write the project template and fetch the matching GUT release.
8. **Model profile**: ask the human, once, which model profile the agents should use for this game (they can change any agent later with `/godot-kit:set-model`):
   - **default** (recommended): orchestrator/architect/reviewer on opus·high, game-designer on opus·medium, executors on sonnet·medium, reporter on haiku·low. Balanced cost and quality.
   - **all-opus**: every agent on opus. Highest quality, highest cost.
   - **budget**: orchestrator on opus, architect/reviewer on sonnet, the rest on haiku. Cheapest; more errors in code and design.
   Apply the chosen profile by running `/godot-kit:set-model` for each agent that differs from default (skip if they pick default — that's how the agents ship). Show a short table of the final assignment.
9. Confirm Milestone 0 (project scaffolding, GUT installed, clean `godot_import`) is marked done in the plan, then report back to the human: where the project lives, a summary of the GDD, the model profile in use, and that `/godot-kit:kit-loop` is ready to run.

## Rules

- Never invent an answer to a questionnaire item on the human's behalf — if they want a recommendation, give it and let them confirm.
- Never skip CHECKPOINT 0. The whole plan is built on the approved GDD; building architecture or a plan against an unapproved GDD wastes everyone's time.
- If `narrative-writer` isn't needed (the GDD says no narrative), don't schedule it into the plan.
- Keep the non-goals list explicit in the GDD — it's what protects scope for the rest of the project.

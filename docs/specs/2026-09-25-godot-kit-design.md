# Godot Kit: design spec

- **Date:** 2026-09-25
- **Status:** draft, pending review
- **First consumer:** Motoconcho (`~/repos/motoconcho-kit`)

## 1. Goal

A public, open-source (MIT) kit that takes a 2D game idea to a playable MVP using Godot 4 + GDScript, Tiled and Pixelorama, driven by a team of Claude Code agents that work in a `/loop` and stop at human checkpoints.

Success criteria:

1. `/new-game` turns a short questionnaire into a Godot project that imports cleanly, has GUT tests passing, and has a GDD, an architecture doc and an MVP plan.
2. `/loop /godot-kit:kit-loop` advances the plan one task per turn, with QA and code review, and stops at every checkpoint.
3. Works on macOS, Windows and Linux. No personal paths, no secrets in files.
4. Motoconcho can switch from its local agents to the kit without losing work.

Non-goals: 3D, C#/GDExtension, multiplayer, a GUI of its own, redistributing third-party code (GUT is downloaded, not vendored).

## 2. Decisions already made

| Topic | Decision |
| --- | --- |
| Location | Own repo `desarrollo-godot-kit` |
| Packaging | Claude Code plugin + marketplace in the same repo (approach A) |
| Audience | Public, open source |
| Language | English (docs, agents, code). Games can be in any language |
| Loop | `/loop` with checkpoints |
| Models | By decision level: Opus for decisions, Sonnet for execution, Haiku for mechanical work |
| MCP | Python (FastMCP), stdio, run with `uvx`. Four areas: Godot, assets, plan, intake. Plus knowledge search |
| Knowledge | Distilled cards from books and own experience; raw text stays private |

## 3. Repository layout

```text
desarrollo-godot-kit/
├── .claude-plugin/
│   ├── marketplace.json        # /plugin marketplace add <repo>
│   └── plugin.json             # plugin "godot-kit": agents, commands, skills, MCP server
├── agents/                     # 15 agents (section 4)
├── commands/                   # new-game.md, kit-loop.md, kit-status.md
├── skills/                     # godot-gdscript, tiled-pipeline, greybox-art, pixel-art-for-games,
│                               # gut-testing, elevenlabs-budget, game-design-by-genre, game-feel, ux-ui
├── mcp/
│   ├── pyproject.toml          # package godot-kit-mcp, entry point godot-kit-mcp
│   ├── src/godot_kit_mcp/
│   │   ├── server.py           # FastMCP app, registers tools
│   │   ├── config.py           # .godot-kit.toml + env + OS defaults
│   │   ├── proc.py             # subprocess with hard timeouts
│   │   ├── godot.py
│   │   ├── assets.py
│   │   ├── png.py              # stdlib-only PNG writer (zlib + struct)
│   │   ├── elevenlabs.py
│   │   ├── plan.py
│   │   ├── intake.py
│   │   └── knowledge.py
│   ├── gdscript/               # tiled_to_godot.gd, tmx_reader.gd, screenshot.gd (run by Godot)
│   └── tests/                  # pytest
├── templates/project/          # what /new-game writes into a new game
├── knowledge/
│   ├── cards/<topic>/<name>.md # public, reviewed cards
│   └── private/                # git-ignored: raw OCR and unreviewed distillations
├── tools/split_cards.py        # splits a distilled book file into cards/
├── docs/                       # getting-started, agents, loop, mcp, pipelines, knowledge
├── examples/motoconcho.md
├── README.md
└── LICENSE
```

## 4. Agents

Plugin agents cannot declare `hooks`, `mcpServers` or `permissionMode`. They all see the plugin's MCP server.

| Agent | model · effort | Role | Writes to |
| --- | --- | --- | --- |
| `orchestrator` | opus · high | Master plan from the GDD; each loop turn picks, delegates, verifies DoD, commits, decides continue/stop | `docs/mvp-plan.md` (structure) |
| `producer` | sonnet · medium | PO: tasks with acceptance criteria, scope, checkpoint briefs for the human | `docs/mvp-plan.md` (tasks) |
| `game-architect` | opus · high | Scenes, autoloads, signals, data, ADRs | `docs/architecture.md`, `docs/adr/` |
| `game-designer` | opus · medium | Concept, rules, economy, balance | `docs/gdd.md`, `data/*.tres` |
| `narrative-writer` | sonnet · medium | Story, scripts, dialogue. Only if the GDD says the game has narrative | `docs/narrative.md`, `data/dialogue/` |
| `ux-ui-designer` | sonnet · medium | Screen flows, HUD spec, touch controls, accessibility | `docs/ux.md` |
| `ui-programmer` | sonnet · medium | Implements `docs/ux.md` | `scenes/ui/` |
| `gameplay-programmer` | sonnet · medium | Rules and physics | `scenes/`, `scripts/`, `autoload/` |
| `ai-programmer` | sonnet · medium | NPCs, state machines, navigation | `scenes/npc/` |
| `level-designer` | sonnet · medium | Tiled maps + export | `maps/`, `scenes/world/` |
| `technical-artist` | sonnet · medium | Greybox, PNG sprites for Pixelorama, camera, effects | `assets/sprites/`, `scenes/**/visual/` |
| `audio-designer` | sonnet · medium | Procedural audio; ElevenLabs optional under budget | `assets/audio/`, `docs/audio.md` |
| `qa-tester` | sonnet · medium | GUT tests, balance sims, scene screenshots | `tests/`, `docs/qa/` |
| `code-reviewer` | opus · high | Review before closing a task. Read-only | reports only |
| `reporter` | haiku · low | Status summaries | reports only |

Rules for every agent: never invent numbers (they go to a `.tres` marked `PROVISIONAL (Dn)` and are listed in the plan), nothing outside the MVP scope, no paid API calls without a budget line in the plan, only write inside owned folders, commit only own paths (`git add <paths>`, never `-A`).

## 5. Loop and checkpoints

Usage: `/loop /godot-kit:kit-loop` (self-paced). One task per turn.

Each turn, the `kit-loop` command delegates to `orchestrator`, which:

1. Calls `plan_next_task`. If it returns a checkpoint, a blocked task or "plan complete", it writes a brief for the human, calls `ScheduleWakeup` with `stop: true` and ends.
2. Delegates the task to its owner agent (and to `game-designer` first if numbers are missing).
3. Runs `godot_import` and `godot_test`. On failure, sends the output back to the owner once; a second failure marks the task `[!]` and stops the loop.
4. Delegates to `qa-tester` (tests for any new rule) and `code-reviewer`. Critical or major findings go back to the owner once.
5. Calls `plan_mark(task, "done", note)`, commits the task's paths, and returns a two-line summary.

Stop conditions: checkpoint, blocked task, two consecutive failures, a paid-API budget that would be exceeded, or plan complete.

### Plan format (parsed by the MCP, editable by hand)

The format Motoconcho already uses:

```markdown
## Milestone 1: Driving

- [ ] **T1.2 · gameplay-programmer**: One-line task.
  *Accept:* criteria.
  *Depends on:* T1.1.
- [ ] **T1.6 · producer** CHECKPOINT: Human playtests the driving.
```

States: `[ ]` todo, `[~]` in progress, `[x]` done, `[!]` blocked. Completion notes go on a `Done:` line under the task.

## 6. MCP server (`godot-kit-mcp`)

Python ≥ 3.11, `mcp` (FastMCP) as the only runtime dependency. Stdio transport. Declared in `plugin.json` as `uvx --from ${CLAUDE_PLUGIN_ROOT}/mcp godot-kit-mcp`.

### Configuration

Lookup order for each tool path: `.godot-kit.toml` in the project root → environment variable (`GODOT_BIN`, `TILED_BIN`, `PIXELORAMA_BIN`) → `PATH` → OS defaults (macOS `/Applications/*.app/Contents/MacOS/*`, Windows `Program Files`, Linux Flatpak and `~/.local/bin`). Secrets only from env (`ELEVENLABS_API_KEY`).

```toml
# .godot-kit.toml (per game, committed)
[tools]
godot = ""          # empty = auto-detect
tiled = ""
pixelorama = ""

[elevenlabs]
reserve_credits = 1500   # never go below this balance
```

### Tools

Every tool returns a JSON object with `ok`, a short `summary`, and data. Tools never raise raw exceptions and every subprocess has a hard timeout (Godot can hang).

| Area | Tool | What it does |
| --- | --- | --- |
| Godot | `godot_find` | Resolves the executable and returns its version |
| | `godot_import` | `--headless --editor --quit`; returns parsed errors and warnings |
| | `godot_test` | Runs GUT; returns totals and failing tests with messages |
| | `godot_run_scene` | Runs a scene headless for N frames; returns the log |
| | `godot_screenshot` | Runs a scene with rendering for N frames, saves the viewport to PNG, returns the path, so agents can see results |
| | `godot_export` | Exports a preset (Android, desktop) |
| Assets | `tiled_export` | `.tmx` → `TileMapLayer` scene via the bundled GDScript converter, which reads the `.tmx` XML directly (Tiled's `tscn` plugin crashes on 1.12.2) |
| | `greybox_tileset` | Palette + tile names → tileset PNG (stdlib PNG writer) |
| | `greybox_sprite` | Simple shape (triangle, rect, circle, hexagon) + color + size → PNG |
| | `pixelorama_open` | Opens a PNG in Pixelorama for the human to touch up |
| | `elevenlabs_balance` | Real credit balance |
| | `elevenlabs_sfx` / `elevenlabs_music` | Generates one sound or track only if `balance - estimate ≥ reserve_credits`; logs cost to `docs/audio-ledger.md` |
| Plan | `plan_status` | Counts by state per milestone |
| | `plan_next_task` | First `[ ]` task whose dependencies are done; flags checkpoints |
| | `plan_mark` | Sets a task's state and adds its `Done:` line |
| | `checkpoint_record` | Stores the human's feedback under the checkpoint task |
| Intake | `intake_questions` | Returns the questionnaire (section 7) as JSON |
| | `project_scaffold` | Writes the template into a folder from the answers; downloads the GUT release matching the Godot version |
| Knowledge | `knowledge_search` | Keyword search over `knowledge/cards` (topic filter); returns names, topics, first lines |
| | `knowledge_get` | Returns one card |

### Testing

- pytest unit tests for config resolution, plan parsing and marking, PNG writer, ledger arithmetic, card search and split.
- Integration tests that run only when Godot is found (`godot_import`, `godot_test` and `tiled_export` against a fixture project). ElevenLabs is never called in tests.

## 7. `/new-game` questionnaire

The orchestrator asks one question at a time (multiple choice with a recommended option):

1. One-sentence pitch.
2. Genre and camera (top-down, side-scroller, puzzle, …).
3. Core loop in three verbs.
4. Target platforms and orientation.
5. Session length.
6. Art direction: greybox only, or pixel art (sprite size and palette).
7. Does it need narrative (story, dialogue)? If yes, `narrative-writer` is enabled.
8. Maps with Tiled?
9. Audio: procedural placeholders, or ElevenLabs with a credit budget.
10. Player-facing language(s).
11. What is explicitly out of the MVP.
12. First checkpoint: what should the human be able to try first?

Output: `game-designer` drafts `docs/gdd.md` → **checkpoint 0: human approves the GDD** → `game-architect` writes the architecture and ADRs → `producer` writes the plan with checkpoints → `project_scaffold` and Milestone 0.

## 8. Knowledge base

- Raw OCR and service outputs live in `knowledge/private/` (git-ignored). Book text is never published.
- `tools/split_cards.py` splits a distilled file into `knowledge/cards/<topic>/<name>.md`, deduplicating by name and keeping `sources`.
- A human reviews each card before it moves from private to public: own words, no long quotes, numbers checked, `> CHECK:` lines resolved.
- Skills are short summaries per domain that link to cards. Conflicting rules between sources are shown to the human to decide.

## 9. Motoconcho migration (later sub-project)

Install the plugin, replace `.claude/agents/` with the kit's agents, move `tools/tiled_to_godot.gd` and `tmx_reader.gd` into the kit (they become `tiled_export`), and keep Motoconcho's docs as they are. Done only between Motoconcho milestones.

## 10. Build order

1. MCP server: config, proc, plan, godot, then assets, intake, knowledge.
2. Agents, commands and skills.
3. Templates and `/new-game`.
4. Knowledge pipeline and first reviewed cards.
5. Docs, README, LICENSE, `examples/motoconcho.md`.
6. Motoconcho migration.

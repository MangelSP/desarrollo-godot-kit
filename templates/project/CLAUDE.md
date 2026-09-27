# {{game_name}}: project instructions for Claude Code

{{pitch}}

Genre: {{genre}}. Core loop: {{core_loop}}. Platforms: {{platforms}}. Session length: {{session_length}}.

**Godot 4.3+ with GDScript only** (no C#, no GDExtension, no plugins that need compiling).

## Documents that rule

| File | What it is | Who maintains it |
| --- | --- | --- |
| `docs/gdd.md` | Rules and numbers for the game. Source of truth | `game-designer` |
| `docs/architecture.md` | Scenes, autoloads, signals and data | `game-architect` |
| `docs/mvp-plan.md` | Milestones and tasks with their owning agent and status | `producer` |
| `docs/adr/` | Technical decisions (one per file) | `game-architect` |
| `docs/qa/` | QA reports and bugs | `qa-tester` |

Before implementing something, read the GDD section that applies to it. If the code needs a number that isn't in the GDD, **don't make it up in the code**: add it to a `Resource` in `data/` and leave a note in `docs/mvp-plan.md` so `game-designer` can confirm it.

## Agent team (`.claude/agents/`)

The Godot Kit ships a team of specialized agents (producer, game-architect, game-designer, level-designer, gameplay-programmer, ai-programmer, ui-programmer, technical-artist, audio-designer, qa-tester, code-reviewer). Task flow: **producer** assigns → (**game-designer** confirms numbers if needed) → the relevant programmer implements → **qa-tester** writes or runs tests → **code-reviewer** reviews → **producer** marks the task done.

## Project structure

```
res://
├── autoload/        # Events, GameState, and whatever other systems the game needs
├── data/            # Resource classes (.gd) and values (.tres)
├── scenes/
│   ├── world/       # Level scenes, TileMapLayers, NavigationRegion2D, spawns
│   ├── player/       # Player character scene(s)
│   ├── npc/         # Enemies, NPCs, patrol/traffic-style actors
│   ├── ui/          # HUD, touch controls, menus, modals
│   └── audio/       # AudioManager and players
├── scripts/         # Pure utilities with no nodes (formulas, helpers)
├── assets/          # sprites/, audio/, fonts/ (empty in greybox)
├── tests/           # GUT tests: unit/ and integration/
└── addons/gut/      # GUT test framework
```

## GDScript conventions

- Godot 4: `@export`, `@onready`, `signal x(arg: Type)`, `await`, `super()`. No Godot 3 syntax (`export var`, `onready var`, `yield`, `connect("x", self, "y")`).
- **Static typing always**: `var speed: float = 0.0`, `func fare(km: float) -> int:`. The project has `debug/gdscript/warnings/untyped_declaration = warn` on.
- Names: scenes `.tscn` in `PascalCase` (`Player.tscn`, `Main.tscn`); everything else (files, folders) in `snake_case` (`player.gd`, `enemy_basic.tres`), classes in `PascalCase` (`class_name PlayerData`), constants in `UPPER_SNAKE`, signals in past tense (`trip_completed`, `score_changed`).
- Identifiers and API in English; player-facing text follows {{languages}}.
- One script per scene. No rule logic in visual nodes: the rule lives in a pure function (in `scripts/` or an autoload) so it can be tested with GUT.
- Communication between systems through signals on the `Events` autoload. A child calls its parent only through a signal.
- Balance numbers live in Resources (`data/*.tres`), never hardcoded.
- Greybox: everything visual with `Polygon2D`, `ColorRect`, `Line2D` or `_draw()`. No images until real assets exist.
- Performance target: 60 fps on mid-range hardware. No `get_node` in `_process`; cache with `@onready`.

## Tooling

Godot, Tiled and Pixelorama paths are auto-detected by the Godot Kit MCP, or set explicitly in `.godot-kit.toml` under `[tools]` if auto-detection picks the wrong install. ElevenLabs credit reservation is also configured there.

Commands run through the Godot Kit MCP tools (`godot_import`, `godot_test`, `tiled_export`, …) rather than raw shell invocations, so paths and versions stay consistent across machines.

## Definition of done (DoD) for each task

1. Implements what the GDD says, without inventing rules.
2. The project imports with no errors and no new warnings.
3. Every new rule or formula has a passing GUT test.
4. `code-reviewer` reports no critical issues.
5. The task is marked in `docs/mvp-plan.md` with a line describing what was done.

## Limits

- Don't add anything from "Out of scope" (`docs/gdd.md`) without the user approving it: {{out_of_scope}}
- Don't delete scenes or resources owned by another area without telling the `producer`.
- Make small commits per task.

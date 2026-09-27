---
name: godot-gdscript
description: Godot 4 GDScript conventions for this kit — static typing, signals, @export/@onready, no Godot 3 syntax, and keeping game rules in pure testable functions. Load before writing or reviewing any .gd file.
---

# Godot 4 GDScript conventions

## Godot 4 syntax only

Never write Godot 3 patterns:

| Godot 3 (never) | Godot 4 (always) |
| --- | --- |
| `export var speed = 10` | `@export var speed: float = 10.0` |
| `onready var x = $Foo` | `@onready var x: Node2D = $Foo` |
| `yield(x, "signal")` | `await x.signal` |
| `connect("x", self, "y")` | `x.connect(_on_x)` or the signal-name form |
| `func _ready(): .init()` (Godot 3 super) | `super()` / `super._ready()` |

## Static typing, always

Every variable, parameter, and return type is typed: `var speed: float = 0.0`, `func fare(km: float) -> int:`. If a project enables `debug/gdscript/warnings/untyped_declaration = warn`, treat that warning as something to fix, not ignore.

## Naming

- Scenes (`.tscn`) in `PascalCase` (`Player.tscn`, `World.tscn`).
- Everything else (scripts, folders) in `snake_case` (`player.gd`, `enemy_grunt.tres`).
- Classes in `PascalCase` (`class_name PlayerData`), constants in `UPPER_SNAKE`, signals named in the past tense (`trip_completed`, not `trip_complete` or `on_trip_complete`).

## Rules live in pure functions

One script per scene. No rule logic in a visual/node script — a rule (a formula, a state transition, a balance calculation) belongs in a `static func` in `scripts/` or an autoload, with typed inputs and outputs, so GUT can test it without instancing a scene. Nodes call the pure function and apply its result; they don't reimplement the logic inline.

## Communication through signals

Systems talk to each other through signals declared on a shared `Events` autoload (or whatever autoload the project's architecture doc names for this). A child node calls its parent only via signal, never by walking up the tree. Avoid `get_node("/root/...")` reaching across unrelated scenes — the only cross-scene reach that's normal is a node talking to an autoload.

## Numbers belong in Resources

Any number that affects balance or difficulty (speed, cost, cooldown, damage) lives in an `@export`ed field on a `Resource` (`.tres`), never as a literal in a `.gd` file. If a needed number doesn't exist anywhere yet, that's a design gap — flag it, don't invent it.

## Performance basics

Cache node lookups with `@onready`; never call `get_node` inside `_process` or `_physics_process`. Move actors in `_physics_process` using `velocity` and `move_and_slide()`. Avoid allocating new `Array`/`Dictionary` objects in a hot per-frame path.

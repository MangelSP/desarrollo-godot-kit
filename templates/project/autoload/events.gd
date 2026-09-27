extends Node
## Global signal bus (docs/architecture.md).
##
## Only declares signals: no state or logic here. Whoever produces a fact emits it
## (`Events.score_changed.emit(...)`) and whoever reacts connects to it.
## Every new signal is added here AND to docs/architecture.md in the same commit.
##
## This file ships with a handful of EXAMPLE signals so the project imports and runs from
## day one. game-architect replaces them with the real signal catalog for this game once
## docs/architecture.md defines the actual systems.

# Signals here are emitted from other scripts, never from this one, so Godot would warn
# UNUSED_SIGNAL on all of them: in a signal bus that warning is a false positive by design.
@warning_ignore_start("unused_signal")

# --- Example signals (replace with the real catalog) ---
signal game_started
signal player_spawned(player: Node2D)
signal score_changed(score: int, delta: int)
signal game_over(reason: StringName)

@warning_ignore_restore("unused_signal")

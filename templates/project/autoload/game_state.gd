extends Node
## Global game state (docs/architecture.md).
##
## Holds the current run's state so scenes can read and update it without passing it around
## by hand. Keep this to plain data and small helpers; rules and formulas belong in
## scripts/ (pure functions) so they can be unit-tested with GUT.
##
## This is a minimal EXAMPLE. gameplay-programmer extends it with the real state once
## docs/gdd.md defines the game's actual rules and numbers.

var score: int = 0
var is_playing: bool = false


func reset() -> void:
	score = 0
	is_playing = false

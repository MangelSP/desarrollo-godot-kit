extends GutTest
## Smoke test: confirms the project imports and the base autoloads exist, so `godot_test`
## has something to run green from day one. Replace/extend as the real systems land.


func test_true_is_true() -> void:
	assert_true(true, "sanity check")


func test_events_autoload_exists() -> void:
	var events: Node = get_node_or_null("/root/Events")
	assert_not_null(events, "Events autoload should be registered in project.godot")


func test_game_state_autoload_exists() -> void:
	var game_state: Node = get_node_or_null("/root/GameState")
	assert_not_null(game_state, "GameState autoload should be registered in project.godot")


func test_game_state_has_reset() -> void:
	var game_state: Node = get_node_or_null("/root/GameState")
	assert_true(game_state.has_method("reset"), "GameState should expose reset()")

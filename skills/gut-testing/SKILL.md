---
name: gut-testing
description: Writing and running GUT (Godot Unit Test) tests for this kit — unit tests for pure functions, integration tests for scenes, and running them headless via godot_test.
---

# GUT testing

## Layout

- `tests/unit/`: tests for pure functions (formulas, state-transition logic) with no scene involved. These are the cheapest and most valuable tests — every GDD rule expressed as a formula should have one.
- `tests/integration/`: tests that instance real scenes (commonly with `add_child_autofree`) to check that signals fire in order, nodes wire up correctly, and a full slice of the loop behaves as expected end to end.
- `tests/sim/`: headless, no-render simulations for balance — a simple bot plays out many sessions and reports aggregate outcomes to compare against `game-designer`'s targets.

## Writing a test

```gdscript
extends GutTest

func test_reward_scales_with_distance() -> void:
    assert_eq(Reward.payout(50.0, 10.0, 1.0), 100)

func test_never_goes_negative() -> void:
    assert_gte(Economy.spend(10, 999), 0)
```

- One test proves one thing; the test name says what.
- Assert against the GDD's actual numbers/examples where the GDD gives one — that keeps the test as a living check against the design doc, not just against whatever the code happens to do.
- If a test fails because the code is wrong, fix the code, not the test. If the GDD is ambiguous or the test's expectation is unclear, that's a question for `game-designer`, not a reason to loosen the assertion.

## Running

Use the `godot_test` MCP tool (`mcp__godot-kit__godot_test`), which runs GUT headless and returns totals plus failing tests with messages — don't shell out to `godot` directly for this if the tool is available, it already handles the flags and timeout.

## Installing GUT

If a new project doesn't have GUT yet, `project_scaffold` installs the release matching the project's Godot version automatically. If it's missing for another reason, install the Godot-4-compatible release from the official `bitwes/Gut` repository into `addons/gut/` and enable the plugin in `project.godot` — GUT is downloaded, never vendored/committed as source in this kit.

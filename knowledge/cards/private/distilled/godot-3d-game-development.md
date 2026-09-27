<!-- 1 Introduction (pp. 15-29) -->
---
name: godot-install-and-first-project
topic: Godot engine setup and project creation
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 1 (pp. 15-29)"]
---
## Rules
- Download Godot from the official site; pick the build matching your OS (Linux, macOS, Windows, Linux server) and your CPU architecture (64-bit for x86_64, 32-bit for x86).
- Choose the **standard** build, not the mono/C# build, unless you specifically plan to script in C#. WHY: the standard build is smaller and matches the book's GDScript examples.
- The download is a compressed archive, not an installer — extract it to a folder, then optionally create a desktop shortcut. WHY: Godot is a portable single executable; there is no install step.
- Create each new project inside its own **empty** folder and give it a meaningful name instead of the default. WHY: Godot writes `project.godot` and asset folders into the project path; a dedicated folder prevents file collisions and keeps projects portable.
- Select the **OpenGL ES 3.0** renderer for simple 2D projects. WHY: it is lighter than Vulkan and sufficient for 2D scenes.
- On first launch, dismiss the initial dialog (close button or Cancel) to reach the Project Manager, then use **New Project**.
- Use **Create & Edit** to create the project and immediately open the editor.

> CHECK: The chapter states the book's code works best with engine versions 3.1–3.5, but the target engine for this knowledge base is Godot 4. Verify version-specific menu names and renderer options against Godot 4 docs.

## Checklist
- [ ] OS and architecture identified before downloading.
- [ ] Standard (non-mono) build downloaded and extracted.
- [ ] Empty, well-named project folder chosen.
- [ ] Renderer selected (OpenGL ES 3.0 for 2D).
- [ ] Project created and editor opened.

## Anti-patterns
- Downloading the mono/C# build by default — adds weight and diverges from GDScript examples.
- Creating a project directly in a folder that already holds unrelated files.
- Leaving the default project name, which makes multiple projects hard to tell apart later.

---
name: godot-scene-and-node-basics
topic: Scene tree, nodes, and the editor workflow
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 1 (pp. 15-29)"]
---
## Rules
- Create scenes via **Scene | New Scene**. Every new scene gets a default root node based on the scene type: `Node2D` for 2D, `Node3D` for 3D, `Control` for UI. WHY: the root node type determines which properties and children make sense for that scene.
- Add child nodes with the plus button in the Scene panel, `Ctrl + A`, or right-click → **Add Child Node**. WHY: all gameplay objects in Godot are nodes arranged in a tree.
- In the Add Node dialog, 2D nodes are colour-coded blue — use the colour coding to filter quickly.
- Rename the root node to something descriptive (e.g. `2D_world`) as soon as the scene is created. WHY: `$NodeName` references in scripts become readable and less error-prone.
- Select a node to see its properties in the **Inspector** panel; edit values there rather than in code when the value is static.
- Toggle node visibility with the circle/eye button in the Scene panel; move nodes by selecting and dragging in the viewport.
- Zoom the viewport with the mouse scroll wheel; resize a Control node by dragging its red handles after selection.
- Save a scene the first time you press Play — accept the save prompt and confirm the default `res://` location.

## Checklist
- [ ] Correct scene type chosen (2D / 3D / UI).
- [ ] Root node renamed meaningfully.
- [ ] Child nodes added and named.
- [ ] Static values set in the Inspector, not hard-coded.
- [ ] Scene saved under `res://` before or at first play.

## Anti-patterns
- Leaving the root node named `Node2D`/`Node3D` — makes `$` paths ambiguous in larger scenes.
- Setting positions/scales in code when they never change — clutters scripts and hides layout intent.
- Forgetting to save the scene before playing, then losing edits on close.

---
name: gdscript-attach-and-signals
topic: GDScript attachment and signal wiring
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 1 (pp. 15-29)"]
---
## Rules
- Attach a script via right-click on the node → **Attach Script**. Available languages: NativeScript (C++), GDScript, Visual Script. Use **GDScript** — it is the engine default and needs no extra download.
- GDScript is Python/Lua-like; prior Python or C# experience transfers directly.
- Connect a Button's `pressed` signal by selecting the node, opening the **Node** tab (second Inspector tab), choosing `pressed`, and clicking **Connect** twice (once to open the dialog, once to confirm).
- Accept the auto-generated handler name (`_on_Button_pressed`) so the connection and the function stay in sync.
- Inside a handler, reach sibling/child nodes with the `$` shorthand: `$Label.set_text("...")`.
- `_ready()` runs automatically when the scene starts — use it for initial setup; never call it manually.
- Delete the auto-generated comment lines from new scripts to keep them readable.

## Checklist
- [ ] Script attached to the correct node (usually the scene root).
- [ ] Language set to GDScript.
- [ ] Signal connected through the Node tab, not by hand-typing the connection.
- [ ] Handler body references nodes via `$Name`.
- [ ] `_ready()` used only for initialization.

## Anti-patterns
- Hand-writing signal connections in code when the editor can generate them — easy to typo and hard to trace.
- Putting gameplay logic on a leaf node (e.g. the Label) instead of the scene root — breaks the "root owns the scene" convention.
- Leaving boilerplate comments in every new script.

---
name: node2d-transform-properties
topic: Node2D position, rotation, and scale
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 1 (pp. 15-29)"]
---
## Rules
- `Node2D` is the base class for all 2D nodes and the parent of every child in a 2D scene. It inherits from `Node` and exposes transform properties.
- Core properties: `position`, `rotation`, `rotation_degrees`, `scale`, `transform`, plus the `global_*` variants and `z_index`, `z_as_relative`.
- Position: `set_position(Vector2)` / `get_position() -> Vector2`. In a `Vector2`, the first component is horizontal (x), the second vertical (y).
- Rotation: `set_rotation(radians)` / `get_rotation() -> radians`. To work in degrees, use the `rotation_degrees` property instead of converting by hand.
- Radian↔degree conversion: `degrees = radians * 180 / PI`; `1 radian ≈ 57.2958°`; `180° = PI radians`.
- Scale: `set_scale(Vector2)` / `get_scale()`. Uniform scale uses the same value on both axes, e.g. `Vector2(1.5, 1.5)`.
- Use `self` to refer to the node the script is attached to.
- Declare variables with `var`; use `export var` when you want the value editable from the Inspector (useful for tuning and testing).
- Use `print()` to output values to the Output panel while debugging.
- `#` starts a one-line comment.

## Checklist
- [ ] Positions expressed as `Vector2(x, y)` with x horizontal, y vertical.
- [ ] Rotation either kept in radians or handled via `rotation_degrees`.
- [ ] Scale applied uniformly unless non-uniform stretch is intentional.
- [ ] Tunable values marked `export var`.
- [ ] Debug values checked with `print()`.

## Anti-patterns
- Mixing radians and degrees in the same calculation without converting — produces wildly wrong angles.
- Hard-coding magic numbers for position/scale instead of `export var` — makes tuning require a code edit.
- Using `set_position`/`set_scale` for values that never change at runtime — set them in the Inspector instead.

> CHECK: The OCR shows `$".".set_rotation(...)` and `$".".set_scale(...)` as the way to target the root node. Verify the idiomatic Godot 4 form (e.g. `rotation = ...` / `scale = ...` on `self`) before publishing examples.

<!-- 2 Towards 2D Game (pp. 30-44) -->
---
name: gdscript-control-flow-basics
topic: GDScript control flow (while, for, if/elif/else, match)
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- Use `while condition:` when the number of iterations is unknown and depends on runtime state; use `for i in range(from, to, step)` when the count is known. WHY: `for` over a range is bounded and readable; `while` handles data-driven termination.
- `range(a, b)` is exclusive of `b`; `range(0, 30, 3)` yields 0, 3, 6 … 27. WHY: off-by-one errors are the most common loop bug.
- `for i in array` iterates over values; `for i in range(0, len(array))` iterates over indices. Pick the form that matches what you need inside the body. WHY: mixing them up silently gives wrong values.
- `for i in "Hello GD"` iterates over the characters of a string. WHY: strings are iterable, useful for text filtering.
- `break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to the next. WHY: both are needed to express early exit and filtering without extra flags.
- Comparison operators: `==`, `>`, `<`, `>=`, `<=`, `!=`. Logical operators: `&&` (and), `||` (or), `!` (not). WHY: these are the only operators you need for branching conditions.
- Use `elif` for a second mutually exclusive condition and `else` as the fallback. WHY: chained `if` statements evaluate every branch; `elif` stops at the first match.
- Ternary form: `var state = "nice" if is_nice else "not nice"`. WHY: keeps a two-way choice on one line.
- `match` branches on a value; list several values in one branch with commas (`1,2,3:`). WHY: replaces long `if/elif` chains and is easier to read.
- `match` works on `typeof()` results too, so you can dispatch by data type. WHY: lets you count or route mixed-type arrays in one pass.
- Declare a function with `func name(params):`; use `-> void` when nothing is returned, `-> int` / `-> String` etc. when a value is returned. WHY: explicit return types document intent and catch mistakes.
- Use `return value` to send a result back; a function without `return` returns nothing. WHY: callers must know whether to expect a value.
- If a block of code is repeated more than twice, extract it into a function. WHY: fewer lines, less duplication, easier to fix bugs in one place.
## Checklist
- Loop bound correct (inclusive vs exclusive)?
- Loop variable incremented inside `while` before any `continue`?
- Every branch of an `if/elif/else` chain covered, including the fallback?
- `match` has a branch for every value you expect, plus a default if input is untrusted?
- Function return type matches what it actually returns?
## Anti-patterns
- Forgetting `n += 1` in a `while` loop → infinite loop.
- Using `if` chains where `elif` is meant → multiple branches run for one input.
- Putting `continue` before the increment in a `while` loop → the counter never advances.
- Duplicating the same code block in three or more places instead of writing a function.
> CHECK: The chapter's `while typeof(a[n]) == TYPE_INT` example never shows `n` being initialized; verify the intended starting index before reusing it.

---
name: gdscript-types-and-typeof
topic: GDScript data types and the typeof() type constants
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- `typeof(value)` returns an integer type constant; compare it against the `TYPE_*` constants (or their numeric values) to branch on data type. WHY: GDScript is dynamically typed, so runtime type checks are the way to filter mixed data.
- Core constants to memorise: `TYPE_NIL=0`, `TYPE_BOOL=1`, `TYPE_INT=2`, `TYPE_REAL=3` (float), `TYPE_STRING=4`, `TYPE_VECTOR2=5`, `TYPE_RECT2=6`, `TYPE_VECTOR3=7`, `TYPE_TRANSFORM2D=8`, `TYPE_COLOR=14`, `TYPE_NODE_PATH=15`, `TYPE_OBJECT=17`, `TYPE_DICTIONARY=18`, `TYPE_ARRAY=19`. WHY: these cover almost every value you touch in a 2D game.
- Pool array constants: `TYPE_RAW_ARRAY=20` (PoolByteArray), `TYPE_INT_ARRAY=21`, `TYPE_REAL_ARRAY=22`, `TYPE_STRING_ARRAY=23`, `TYPE_VECTOR2_ARRAY=24`, `TYPE_VECTOR3_ARRAY=25`, `TYPE_COLOR_ARRAY=26`. WHY: typed pools are the fast path for bulk numeric data.
- `TYPE_MAX=27` is a sentinel marking the end of the constant list, not a real type. WHY: don't use it in comparisons.
- Prefer the named constant (`TYPE_VECTOR2`) over the raw number (`5`) in code. WHY: names survive refactors and read clearly.
- Keep large data collections single-typed. WHY: mixed arrays force a `typeof` check on every element and slow down iteration.
## Checklist
- Every element of a hot-path array the same type?
- Type checks written with `TYPE_*` names, not magic numbers?
- `TYPE_REAL` used for floats (not `TYPE_FLOAT`, which does not exist)?
## Anti-patterns
- Assuming `typeof(1.0) == TYPE_INT` — floats report `TYPE_REAL`.
- Storing ints, strings and vectors in one array and then branching per element in a tight loop.

---
name: gdscript-arrays
topic: GDScript arrays and Pool*Array types
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- Create arrays with `var arr = []` or `var arr = Array()` for mixed types; use `PoolIntArray()`, `PoolRealArray()`, `PoolStringArray()`, `PoolVector2Array()`, `PoolVector3Array()`, `PoolColorArray()`, `PoolByteArray()` for single-typed data. WHY: pool arrays are compact and faster for large numeric sets.
- `PoolByteArray` holds integers 0–255 only. WHY: it is a byte buffer, not a general int array.
- `arr.append(x)` adds at the end; if the array is empty the element lands at index 0. WHY: append is the standard growth operation.
- Pre-fill defaults with a loop: `for i in range(0, 15): arr.append(0)`. WHY: avoids null checks later.
- `len(arr)` gives the element count; `arr.size()` is the equivalent for dictionaries. WHY: you need the bound for index loops.
- `arr.count(value)` counts occurrences of a value; `arr.find(value)` returns the index of a value. WHY: both are one-call replacements for hand-written search loops.
- `arr.sort()` sorts numbers ascending or strings alphabetically; `arr.shuffle()` randomises order in place. WHY: avoids writing your own sort.
- `arr.insert(index, value)` inserts at a position; `arr[index] = value` overwrites; `arr[index]` reads. WHY: covers the three basic mutations.
- Call `randomize()` before using `randi()`; `randi() % 100` gives 0–99. WHY: without `randomize()` the sequence repeats every run.
- Arrays can be declared inline with initial values: `var arr = [39, 51, 36]`. WHY: shorter than appending in `_ready()`.
- Filter a mixed array into typed arrays with a `for` loop plus `typeof` checks. WHY: downstream code then works on homogeneous data.
## Checklist
- `randomize()` called once before any `randi()`?
- Correct pool type chosen for the data (int vs float vs vector)?
- Index loop bounded by `len(arr)`, not a hard-coded number?
- `find()` result checked for a valid index before use?
## Anti-patterns
- Using `find()` as a boolean — index 0 is falsy in some languages; check the returned index explicitly.
- Mixing types in a large array and type-checking every element in the game loop.
- Forgetting `randomize()` and wondering why "random" values repeat.

---
name: gdscript-dictionaries
topic: GDScript dictionaries (key-value storage)
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- Declare with `var dict = {1: 9, 2: 24, 3: 9}` — key first, colon, then value. WHY: keys can be ints or strings, values can be any type.
- `dict.size()` returns the entry count; `dict.keys()` returns the key list; `dict.values()` returns the value list. WHY: these three cover most inspection needs.
- Assigning to an existing key overwrites it; assigning to a new key appends it: `dict[1] = 6`, `dict["new_key"] = "Text value"`. WHY: one syntax handles both update and insert.
- Values can be arrays or nested dictionaries: `dict[3] = [9,18,24,30]`, `dict[5] = {"first":"very good", ...}`. WHY: lets you model structured records without classes.
- Access nested data by chaining indices: `dict[3][2]` for an array element, `dict[5]["first"]` for a nested dictionary value. WHY: the same bracket syntax works at every depth.
- Build default-filled dictionaries with a loop: `for i in range(0,9): dict[i] = 0`. WHY: guarantees every key exists before gameplay reads it.
## Checklist
- Every key the game reads initialised before first access?
- Nested structures accessed with the correct number of brackets?
- String keys spelled identically at write and read sites?
## Anti-patterns
- Reading a key that was never set — returns null and breaks arithmetic downstream.
- Using a dictionary where a fixed-size array would do — dictionaries have more overhead.

---
name: node2d-transform-scale-position
topic: Node2D transform, scale and global position
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- `Node2D` is the base game object for all 2D nodes; child sprites inherit its transform. WHY: moving the parent moves the whole group.
- Scale: `set_scale(Vector2(x, y))` to set, `get_scale()` to read. `Vector2(3, 3)` triples the object's size. WHY: uniform scaling needs both components equal.
- Transform: `Transform2D(rotation_in_radians, position_vector)` combines rotation and position; apply with `set_transform(trans)`, read with `get_transform()`. WHY: one property carries both placement and orientation.
- Global position: `set_global_position(Vector2(x, y))` and `get_global_position()` work in scene coordinates, independent of parent transforms. WHY: use global position when you need absolute placement; use local when you want parent-relative motion.
- `const global_pos = Vector2(18, 18)` declares a compile-time constant. WHY: constants cannot be accidentally reassigned at runtime.
- `export var sca = Vector2(0, 0)` exposes a variable in the inspector for tuning without editing code. WHY: fast iteration on values during testing.
- Rotation is in radians, not degrees. WHY: passing degrees gives wildly wrong orientations.
## Checklist
- Using `set_global_position` when the node has a transformed parent, and local position when it does not?
- Rotation values converted to radians?
- Scale components non-zero (zero scale makes the node invisible)?
## Anti-patterns
- Setting local position on a child and expecting it to match scene coordinates.
- Using `export var` for values that must never change at runtime — use `const` instead.

---
name: node2d-z-index
topic: Node2D z_index and 2D render order
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 2 (pp. 30-44)"]
---
## Rules
- `z_index` controls draw order in 2D. Default is `0`. WHY: it is the only ordering knob for overlapping 2D nodes.
- Higher `z_index` draws on top; lower draws behind. `1` is above default, `-1` is below. WHY: gives a simple integer scale for layering.
- Set with `set_z_index(value)`, read with `get_z_index()`. WHY: lets you change layering at runtime (e.g. a player stepping in front of a tree).
- Use `match` on the z-index value when you need to react differently per layer. WHY: it is a small, fixed set of discrete values.
## Checklist
- Background layers negative, gameplay layer 0, foreground/UI positive?
- Z-index changed at runtime only where the game logic requires it?
## Anti-patterns
- Relying on scene-tree order for layering — it is fragile once nodes are added dynamically.
- Using large arbitrary z-index values instead of a small documented range.

<!-- 3 Making 2D Games (pp. 45-58) -->
---
name: 2d-vector-movement
topic: 2D math and sprite movement in Godot
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 3 (pp. 45-58)"]
---
## Rules
- Represent 2D positions as `Vector2(x, y)`: x = horizontal, y = vertical. Use it for both `set_position()` and `translate()`.
- `set_position(Vector2)` teleports to an absolute coordinate; `translate(Vector2)` adds an offset relative to the current position. Pick based on whether you track absolute or delta movement.
- `move_local_x(amount)` / `move_local_y(amount)` are shorthand for translating along one local axis — use them for simple axis-aligned motion.
- For timer-driven movement, add a `Timer` node, set `wait_time` (e.g. 0.3), enable auto-start, and connect the `timeout` signal to a handler.
- Stop the timer when the target condition is met, e.g. `if $icon.get_position().x > 150: $Timer.stop()`. WHY: an unstopped timer keeps mutating position forever.
- Use `Transform2D(rotation_radians, Vector2(x, y))` with `set_transform()` when you need position and rotation in one assignment.
- Spawn repeated props with a helper function taking a `Vector2` parameter; call it from `_ready()` or a loop.
- Space props evenly with `for i in range(10, 360, 30)` (start, stop, step) — step controls the gap in pixels.
- Add randomness to spacing with `randi() % 11 + 1` added to the base x. WHY: `% n` bounds the result to 0..n-1, `+1` shifts it to 1..n.
## Checklist
- [ ] Timer `wait_time` and auto-start set before connecting `timeout`.
- [ ] Movement loop has an explicit stop condition.
- [ ] Spawn helper adds the sprite as a child of the scene root (`.add_child(sprite)`).
- [ ] `set_scale(Vector2(0.3, 0.3))` applied when the source texture is too large.
## Anti-patterns
- Incrementing a manual counter (`n += 1`) when `translate()` already accumulates position — redundant state that drifts out of sync.
- Leaving a movement timer running after the goal is reached.
- Hardcoding absolute positions in a loop instead of deriving them from the loop index.

---
name: godot-random-numbers
topic: Random number generation in GDScript
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 3 (pp. 45-58)"]
---
## Rules
- Call `randomize()` once at startup (e.g. in `_ready()`) before any random call. WHY: without it the generator uses a fixed default seed and produces the same sequence every run.
- `randf()` returns a float in [0, 1] — use it for probability rolls and normalized interpolation.
- `randi()` returns an unsigned 32-bit integer (0 to 2^32-1). Bound it with modulo: `randi() % 100 + 1` gives 1..100.
- `rand_range(min, max)` returns a float in the given range — use it when you need a float spread, not an integer.
- `rand_seed(seed)` returns a value whose `.hash()` can be passed to `seed()` to reproduce a sequence deterministically. Use for reproducible level layouts or tests.
- To place N objects with jitter: loop over base positions, add `randi() % range + 1` to the coordinate, then spawn.
## Checklist
- [ ] `randomize()` present exactly once, before first random call.
- [ ] Modulo bounds match the intended inclusive range (watch the off-by-one from `+1`).
- [ ] Deterministic seeds used only where reproducibility is wanted.
## Anti-patterns
- Calling `randomize()` inside a per-frame or per-spawn function — reseeds constantly and destroys distribution quality.
- Using `randi() % n` without `+1` when you need 1..n instead of 0..n-1.
- Assuming `randf()` returns anything other than [0, 1].

---
name: 2d-physics-bodies
topic: Choosing and configuring 2D physics bodies
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 3 (pp. 45-58)"]
---
## Rules
- Body selection table:
  - `StaticBody2D` — immovable environment: walls, platforms, floors.
  - `KinematicBody2D` — player-controlled / script-driven characters.
  - `RigidBody2D` — objects driven by the physics simulation (impulses, gravity).
  - `Area2D` — collision detection / triggers without physical response.
- Every physics body needs a `CollisionShape2D` (or `CollisionPolygon2D`) child; without it there is no collision.
- Enable visible collision shapes via the Debug menu while developing. WHY: invisible shapes make collision bugs nearly impossible to diagnose.
- `StaticBody2D` properties:
  - `constant_linear_velocity` — does not move the static body, but pushes bodies that collide with it (conveyor / escalator effect).
  - `constant_angular_velocity` — same, but imparts spin.
  - `friction` — 0 (none) to 1 (full).
  - `bounce` — 0 (none) to 1 (full).
  - `physics_material_override` — swap in a `PhysicsMaterial` with its own friction/bounce/rough/absorb.
- `RigidBody2D` properties:
  - `mode`: 0 rigid (default), 1 static, 2 kinematic, 3 character (rigid without rotation).
  - `mass` default 1; `weight` derives from mass × default gravity; `inertia` 0 means auto-calculated.
  - `friction` default 1, `bounce` default 0, `gravity_scale` default 1 (multiplies default gravity).
  - `contact_monitor` default false — set true to receive collision signals.
  - `max_contacts_reported` default 0 — must be raised (e.g. 4) or no contacts are reported.
  - `can_sleep` default true; sleeping bodies skip force calculation until woken by collision or `apply_impulse()` / `add_force()`.
  - `linear_damp` reduces `linear_velocity` over time.
  - `use_custom_integrator(true)` disables internal force integration; the body then moves only via `_integrate_forces()`.
- Continuous collision detection modes: 0 disabled (fastest, can miss fast small objects), 1 ray cast (faster, less precise), 2 shape cast (slowest, most precise). Use mode 2 for fast small projectiles.
- Build bodies in code by instantiating the body, a `CollisionShape2D`, and a shape resource (`RectangleShape2D` with `set_extents()`), then chaining `add_child()`.
## Checklist
- [ ] Correct body type chosen for the object's role.
- [ ] Collision shape added as a child and sized.
- [ ] Visible collision shapes enabled in Debug.
- [ ] `contact_monitor = true` and `max_contacts_reported > 0` if collision signals are needed.
- [ ] CCD mode raised for fast, small moving objects.
## Anti-patterns
- Expecting `RigidBody2D` to emit collision signals with default settings.
- Using `StaticBody2D` for anything that must move on its own.
- Leaving `max_contacts_reported` at 0 while relying on contact callbacks.
- Using CCD mode 2 everywhere — it is the slowest option.

> CHECK: The chapter uses Godot 3 API names (`KinematicBody2D`, `set_position`, `rand_range`, `rand_seed`, `set_extents`, `set_mode`). In Godot 4 these are `CharacterBody2D`, `position`, `randf_range`, `seed`, `size`, and `mode` is replaced by `freeze`/`lock_rotation`. Verify against the Godot 4 docs before applying.

<!-- 4 Creating a 2D Game (pp. 59-73) -->
---
name: 2d-character-movement
topic: 2D character setup and movement
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Build a 2D character as `KinematicBody2D` with `CollisionShape2D` and `Sprite2D` as children; rename the root node (e.g. `2D_character`) and attach a GDScript.
- Use a rectangle collision shape for a placeholder character; swap in final art later.
- Move the character by reading input in `_process` and calling `set_position` with a movement factor: `pos.x ± mf` for left/right, `pos.y ± mf` for up/down. Use `mf = 3` as a starting speed.
- Read the current position each frame via `get_position()` before applying the delta, so movement is relative, not absolute.
- Use the built-in `ui_right`, `ui_left`, `ui_up`, `ui_down` actions for prototyping; remap them for a real game.
- Expose the movement factor as a variable so it can be tuned before play or modified at runtime by power-ups.

WHY: A kinematic body with a simple position offset gives predictable, physics-free control and is the fastest way to validate a 2D character before adding animation or physics.

## Checklist
- [ ] Root node renamed and script attached.
- [ ] Collision shape sized to match the sprite.
- [ ] `pos` and `mf` declared with `onready var` at the top of the script.
- [ ] All four directions tested in a running scene.

## Anti-patterns
- Moving the root node instead of the body node when the script lives on a parent — the offsets then apply to the wrong transform.
- Hard-coding speed in four places; use one `mf` variable.

> CHECK: The chapter's sample script attaches to a parent node and calls `$KinematicBody2D.get_position()`, which is unusual — verify whether the script should live on the body itself in Godot 4 (where `KinematicBody2D` is replaced by `CharacterBody2D`).

---
name: 2d-ball-physics-material
topic: RigidBody2D ball setup and bounce
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Create the ball as `RigidBody2D` with `CollisionShape2D` (circle) and `Sprite2D` children.
- In the inspector set: custom integrator **on**, contact monitor **on**, contact reported **3**. Contact monitoring is required for the body-entered signal to fire.
- Give the ball a `PhysicsMaterial` with `bounce = 1` and apply it via `set_physics_material_override()` in `_ready()`.
- Keep the ball's custom integrator enabled at start so it stays still; disable it (`set_use_custom_integrator(false)`) when the player presses Play so gravity takes over.

WHY: A bounce of 1 makes collisions feel lively and smooth; toggling the custom integrator gives a clean "start the game" moment without teleporting the ball.

## Checklist
- [ ] Contact monitor enabled, otherwise no collision callbacks.
- [ ] Physics material created in code or as a resource and assigned.
- [ ] Ball tested inside the real environment scene, not in isolation.

## Anti-patterns
- Forgetting `contact_monitor = true` and then wondering why `body_shape_entered` never fires.
- Setting bounce above 1 — the ball gains energy and never settles.

---
name: 2d-environment-tilemap
topic: Building the 2D game environment
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Start the environment scene with a `ColorRect` as background: set size first, then color. Replace it later with a `Sprite2D` background texture.
- Use `StaticBody2D` nodes for a handful of walls/props; they can carry linear and angular velocity values if you want moving obstacles.
- Switch to `TileMap` once the level has many repeated collision objects — a tilemap is the better solution at that scale.
- Every tile that should block movement needs a collision shape: create the tileset, add a texture, click **New single tile**, drag to select the region, then click the **Collision** button and pick the collision type.
- Keep passive elements (background, walls, tiles) in the environment scene; add active elements (props, ball, character) as instances on top.

WHY: Separating passive level geometry from active gameplay objects keeps scenes small and lets you reuse the same environment across levels.

## Checklist
- [ ] Background sized to the viewport.
- [ ] Play area enclosed by static bodies or collision tiles.
- [ ] Tileset saved as a resource, not rebuilt per scene.

## Anti-patterns
- Using `StaticBody2D` for dozens of identical blocks — use a tilemap instead.
- Adding tiles without collision shapes and then debugging why the ball passes through walls.

---
name: code-generated-props
topic: Generating game props from code
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Write one factory function `create_props(prop_name, posx, posy, v)` that builds a `StaticBody2D` with a `CollisionShape2D` (`RectangleShape2D`) and a `Sprite2D`, then adds both as children and adds the body to the scene.
- Order inside the factory: create nodes with `.new()`, set their properties, add children to the body, set name and position, then `add_child` the body.
- Size the collision with `shape.set_extents(Vector2(15, 30))` and the sprite with `sprite.set_scale(Vector2(0.3, 0.3))`; keep the two consistent so the hitbox matches the art.
- Preload textures at the top of the script (`onready var textura = preload("res://prop_rect.png")`) rather than loading inside the loop.
- Lay out rows with `for f in range(120, 1040, 40)` and increment a counter `i` to give each prop a unique name (`"prop" + str(i)`).
- Use the `v` parameter as a prop type discriminator: `v == 1` simple prop, `v == 2` multi-hit prop, and so on.

WHY: A single parameterised factory avoids duplicating dozens of near-identical scenes and makes level layout a matter of changing loop bounds.

## Checklist
- [ ] Every generated prop has a unique name.
- [ ] Texture preloaded once.
- [ ] Collision extents and sprite scale verified visually.

## Anti-patterns
- Duplicate prop names — collision handling by name will match the wrong object.
- Loading textures with `load()` inside the generation loop.

---
name: prop-scoring-and-signals
topic: Collision signals, scoring and multi-hit props
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Connect the ball's `body_shape_entered(body_id, body, body_shape, local_shape)` signal and handle scoring inside the generated callback.
- Identify the prop by name: loop `for f in range(1, 72)` and compare `body.get_name() == "prop" + str(f)`.
- On a hit, call `body.queue_free()` to remove the prop and increment `score`, then update a `Label` with `"S C O R E: " + str(score)`.
- For multi-hit props, keep an array (`onready var prob_b = []`) of already-hit prop names. On collision: if the name is in the array, free the body; otherwise append the name and leave it alive.
- Use a local `pro` flag set to `true` before the name loop and flipped to `false` when a repeat hit is detected, so the first-hit branch only runs once.
- For visual feedback on multi-hit props, add a second `Sprite2D` child on the first hit and `queue_free()` that child when the prop is finally destroyed.
- Award points either per hit or only on the final hit — pick one and keep it consistent.

WHY: Name-based lookup plus a hit array is the simplest way to give props hit points without adding a custom script to every instance.

## Checklist
- [ ] Signal connected from the ball, not the prop.
- [ ] Score label updated on every scoring event.
- [ ] Multi-hit props removed from the array logic when freed.

## Anti-patterns
- Comparing `body.name` directly instead of `body.get_name()` in code that must stay robust.
- Forgetting to free the secondary sprite, leaving ghost art on screen.

---
name: custom-prop-scene
topic: Custom props with export variables and instancing
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Build a reusable prop scene: `StaticBody2D` root with `CollisionShape2D` and `Sprite2D` children, plus a script on the root.
- Declare `export var pos_x`, `export var pos_y`, `export var prop_img` (preloaded texture) and `export var prop_name` so each instance can be configured in the inspector.
- In `_ready()`, apply them: `$Sprite.set_texture(prop_img)`, `set_position(Vector2(pos_x, pos_y))`, `set_name(prop_name)`.
- Instantiate from code with `onready var scene = preload("res://ShineProp.tscn")` then `var instance = scene.instance(); add_child(instance)`.
- Randomise placement with `randomize()` and `rnd = randi() % 22 + 1`, then offset: `instance.pos_x += rnd * 40`.
- Always give each instance a unique name (`instance.prop_name = "custom_prop_" + str(n)`) because collision handling matches by name.
- Vary appearance by assigning different preloaded textures to `instance.prop_img` per spawn loop.

WHY: Export variables turn one scene into a family of variants, so you get variety without duplicating scenes or writing new scripts.

## Checklist
- [ ] All export variables have sensible defaults.
- [ ] Unique name assigned before `add_child`.
- [ ] `randomize()` called before the first `randi()`.

## Anti-patterns
- Instancing several copies without renaming — name-based collision logic breaks.
- Calling `randi()` without `randomize()`, producing the same layout every run.

---
name: godot-troubleshooting-and-style
topic: Debugging workflow and coding style
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Set the main scene via **Project | Project Settings | General | Run | Main Scene** before running with F5.
- Red dots in the debugger are errors that stop execution; yellow dots are warnings that do not.
- For "Identifier X is not declared in the current scope", declare the variable at the top of the script (e.g. `onready var pos = Vector2(0, 0)`) and continue with F5 rather than restarting.
- For "The argument 'delta' is never used", either use `delta` or rename it to `_delta` in the function signature.
- Warnings can be disabled globally under **Project Settings | Debug | GDScript**.
- Style: leave at least two blank lines between functions, put spaces around operators and after commas, and align important data so it is easy to scan.

WHY: Reading the debugger colour coding and fixing warnings as you go keeps the project runnable and makes later bugs easier to isolate.

## Checklist
- [ ] Main scene configured.
- [ ] No red errors before moving on.
- [ ] Warnings either fixed or deliberately suppressed.

## Anti-patterns
- Restarting the editor for every parse error instead of fixing and continuing.
- Leaving unused-argument warnings everywhere until real warnings are invisible.

---
name: playability-polish
topic: Improving play-ability
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Do not start polishing until one full game level is playable end to end.
- Improve in this order: sprite quality, then collision smoothness, then audio, then game mechanics.
- Swap placeholder textures for final art by changing the `preload` path in the script header and the `set_texture` call — no structural changes needed.
- When you change a sprite's size, update both `shape.set_extents(...)` for the collision and `sprite.set_scale(...)` so the hitbox still matches the art.
- Replace the `ColorRect` background with a `Sprite2D` texture for a richer frame.
- Use a tilemap with collision tiles for the game frame once the level has many repeated elements.
- Verify the resource path after copying it (RMB | Copy Path) — a broken path silently fails to load.

WHY: Play-ability comes from the sum of graphics, collision feel, audio and mechanics; polishing before the level works wastes effort on a design that may change.

## Checklist
- [ ] One level completable start to finish.
- [ ] Collision extents re-checked after every art swap.
- [ ] All preload paths verified.

## Anti-patterns
- Scaling a sprite without updating its collision shape, producing invisible walls or pass-throughs.
- Adding menus and audio before the core loop is fun.

---
name: simple-game-menu
topic: Building a basic game menu
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 4 (pp. 59-73)"]
---
## Rules
- Create a `Node2D` named `MainMenu` as the menu root; set layer 1 and scale 0.3 on both axes.
- Add a `Sprite2D` background (e.g. `Table.png`) and place four `TextureButton` nodes on top of it.
- Give each button two textures: one for the normal state and one for hover.
- Wire the Play button to start the game, e.g. `$RigidBody2D.set_use_custom_integrator(false)` so gravity begins acting on the ball.
- Wire the Exit button to `get_tree().quit()`.

WHY: A minimal menu with two working buttons is enough to turn a test scene into something a player can start and leave cleanly.

## Checklist
- [ ] Menu root scale and layer set.
- [ ] Hover texture assigned on every button.
- [ ] Play and Exit both tested.

## Anti-patterns
- Building a full menu system before the gameplay loop is finished.
- Leaving the ball's custom integrator on after Play, so nothing moves.

<!-- 5 2D Adventure (pp. 74-89) -->
---
name: turn-based-board-with-buttons
topic: turn-based movement on a button grid
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Build the board from `Button` nodes, not custom input handling: each field is a 64×64 button placed in a lane; the button's `pressed` signal gives you mouse interaction and the field graphic for free.
- Keep a 1D integer array as the authoritative board state, e.g. `var space = [0,0,0,0,0,0,1,0]` where `1` marks the tile the character occupies. WHY: one array is the single source of truth; the sprite position is derived from it, so state and visuals cannot drift apart.
- Route every button through one shared function: each `_on_ButtonN_pressed()` calls `uni_func(n)` with its field index. WHY: movement, action-point and text logic live in one place instead of six copies.
- Rename buttons to field names in `_ready()` (`$Button3.set_name("Field1")` … `$Button8.set_name("Field6")`) so you can look up a field by index: `get_node("Field" + str(no))`. WHY: index-to-node lookup avoids a second array of node references.
- Convert field index to sprite position with `get_global_position()` plus a half-tile offset (`pos += Vector2(32, 32)` for 64×64 fields) to center the sprite on the tile.
- Allow a move only to an adjacent field: check `space[no+1] == 1 or space[no-1] == 1` before moving. WHY: this is the whole adjacency rule for a 1D lane; no pathfinding needed.
- On a legal move, swap the flags: set `space[no] = 1` and clear the old tile (`space[no+1] = 0` or `space[no-1] = 0`). WHY: keeps exactly one occupied tile.
- Guard the move with the action-point check *before* the adjacency check: `if $"/root/singleton".action_points > 0:` then the move calculation. WHY: prevents negative action points and blocks movement when the turn is spent.
- Use a `TileMap` (new `TileSet` created from the inspector) purely as background art behind the buttons; position nodes carefully so tiles and buttons line up.

## Checklist
- [ ] Six 64×64 buttons laid out in a lane, each with a `pressed` signal connected.
- [ ] `space` array length = fields + 1, exactly one `1`.
- [ ] `_ready()` renames all buttons to `Field1..FieldN`.
- [ ] `uni_func(no)` handles: action-point gate → adjacency check → position set → flag swap.
- [ ] Sprite offset matches half the field size.

## Anti-patterns
- Duplicating movement code inside each button handler instead of one `uni_func`.
- Moving the sprite without updating `space` (or vice versa) — the two will desync after a few clicks.
- Checking adjacency before action points, which lets a spent turn still move the character.
- Hardcoding node paths like `$Button3` for logic instead of the renamed `FieldN` names.

> CHECK: OCR shows `var pos = .get_node(...)` — the leading dot is likely a broken `$` or `get_node` on the scene root; verify the exact call in the book's source files.

---
name: singleton-globals-action-points
topic: autoload singleton for turn/action-point state
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Put cross-scene state (action points, period, character speed) in one autoloaded script: create `singleton.gd` extending `Node`, then enable it in Project Settings → AutoLoad with a name and `Enable = true`.
- Initialize values in `_ready()` of the singleton: `action_points = 2`, `period = 0`. WHY: the autoload runs before gameplay scenes, so every scene sees valid values.
- Access it from any scene by absolute path: `$"/root/singleton".action_points`. WHY: no signal wiring or node references needed between unrelated scenes.
- Give the player a fixed number of actions per turn (2 here); a "Next Turn" `TextureButton` resets `action_points = 2` and increments `period` by 1.
- Refresh the HUD from the same function that mutates state: `writte_action_points()` sets both the action-point label and the period label, and is called from the next-turn handler. WHY: one refresh path prevents stale labels.
- Store tunables like `speed` in the singleton too, and read them in `_ready()` of the character scene (`speed = $"/root/singleton".speed`). WHY: balance values change in one file.

## Checklist
- [ ] `singleton.gd` exists and is registered in AutoLoad with Enable checked.
- [ ] All mutable globals declared `onready var` and assigned in `_ready()`.
- [ ] Next-turn button resets action points and increments period, then refreshes HUD.
- [ ] Every action-consuming code path checks `action_points > 0` first.
- [ ] HUD labels (`ActionP`, `PeriodLabel`) updated only via the shared refresh function.

## Anti-patterns
- Storing turn state in the gameplay scene — it resets when the scene is reloaded or when the platformer sub-scene is instantiated.
- Forgetting to enable the autoload; the `$"/root/singleton"` path then fails at runtime.
- Decrementing action points in several places instead of one gated function.

---
name: area-description-text
topic: textual area narration for adventure fields
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Keep one string array of area descriptions indexed by field number, with index 0 as an empty placeholder: `var field_text = ["", "You are ...", ...]`. WHY: the placeholder makes `field_text[no]` line up with the 1-based field indices used by the buttons.
- Display narration in a `RichTextLabel` placed in the upper part of the screen; it handles long text and lets you set font and size. WHY: plain `Label` is awkward for multi-line prose.
- Update the text inside the same movement function: `$RichTextLabel.set_text(field_text[no])`. WHY: narration then always matches the tile the character just entered.
- Give the label a background sprite (e.g. `bt_text.png`) and/or a `ColoredRectangle` in a `CanvasLayer` for readability over the tilemap.
- Set a default narration string in the editor so the label is never empty before the first move.

## Checklist
- [ ] `field_text` array length matches the number of fields (plus the empty slot).
- [ ] `RichTextLabel` anchored top-center, readable over the background.
- [ ] Text set on every successful move, not only on first entry.
- [ ] Background sprite/rectangle added via `CanvasLayer` so it stays fixed on screen.

## Anti-patterns
- Indexing `field_text` with a 0-based button index — off-by-one narration.
- Using a plain `Label` for paragraph-length text.
- Leaving the label with no default text, showing an empty panel at game start.

> CHECK: OCR shows `RichTehtLabel` in one place — treat as `RichTextLabel`.

---
name: platformer-character-kinematicbody2d
topic: 2D platformer character movement and animation
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Build the player as `KinematicBody2D` + `CollisionShape2D` (CapsuleShape2D) + `AnimatedSprite` as children.
- Move with `move_and_collide(Vector2(speed, 0))` inside `_process`, driven by `Input.is_action_pressed("ui_right")` / `"ui_left"`. WHY: `move_and_collide` stops at collision shapes, which is what a platformer path needs.
- Stop explicitly on key release: `if Input.is_action_just_released("ui_right"): $hero.move_and_collide(Vector2(0, 0))`. WHY: without it the character keeps its last motion.
- Flip the sprite to face travel direction: `set_flip_h(true)` when moving left, `false` when moving right.
- Toggle the walking animation with `_set_playing(true)` while a direction key is held and `_set_playing(false)` on release.
- Apply simple gravity by calling `move_and_collide(Vector2(0, 1))` every frame in `_process`.
- Configure the `AnimatedSprite`: create `SpriteFrames`, add a `NewAnimation` named `Walking`, load the frame images (shift-select first-to-last), set scale ≈ 0.12 and speed scale ≈ 6.
- Instantiate the character scene from the level: `preload("res://PlayerCharacter.tscn")`, then `instance()`, `set_position(Vector2(130, 450))`, `add_child(s)` in `_ready()`. WHY: preload keeps the scene out of the level file and lets you spawn it at a chosen spot.

## Checklist
- [ ] Collision shape sized to the sprite, not the sprite's raw pixel bounds.
- [ ] Both left and right branches handle press, release, flip and animation.
- [ ] Gravity applied unconditionally each frame.
- [ ] Character scene saved and preloaded by the level scene.
- [ ] Spawn position tuned to the actual tilemap layout.

## Anti-patterns
- Using `move_and_slide` semantics with a manually zeroed velocity and no release handling — the character drifts.
- Forgetting `set_flip_h` so the character moonwalks.
- Leaving the animation playing after key release.
- Hardcoding the spawn position without checking it against the tilemap.

---
name: platformer-tilemap-and-bounds
topic: tilemap background, collisions and level bounds
confidence: consensus
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Use `TileMap` with a `TileSet` created from the inspector for the platformer background; tile size 32×32 with quadrant size 16 for the main set.
- Give collision shapes only to tiles the character must stand on or bump into (ground, platforms, bridge); leave decorative tiles (signboards, direction objects, springs) without collision. WHY: collision shapes define the walkable path.
- For large repeated/water background areas, add a second `TileMap` with its own tile set (cell size 64×64, quadrant 16) using repeated/water-surface textures. WHY: mixing scales in one tile set is awkward.
- Keep level geometry rectangular so tiles align cleanly.
- Bound the play area with `StaticBody2D` + `CollisionShape2D` walls on both sides. WHY: the collision shapes, not code, define where the character can go.
- Build info panels from two `Sprite` nodes plus a `RichTextLabel`, placed upper-middle, and uncheck their `visible` property in the inspector so they start hidden and are shown when resources are found.

## Checklist
- [ ] TileSet created and assigned; tiles placed to form a walkable path.
- [ ] Collision shapes on all path tiles, none on decoration.
- [ ] Second tilemap for repeated/water background if needed.
- [ ] Left and right `StaticBody2D` borders present.
- [ ] Info panel nodes exist and start invisible.

## Anti-patterns
- Adding collision to every tile, including decoration — the character snags on scenery.
- Relying on code to clamp the character instead of collision walls.
- Leaving info panels visible at level start.

---
name: quest-instantiation-and-layering
topic: embedding a platformer sub-scene as a quest
confidence: opinion
sources: ["Godot 3D Game Development, Marijo Trkulja, ch. 5 (pp. 74-89)"]
---
## Rules
- Keep the platformer as its own scene (`2D_landscape.tscn`) and preload it in the adventure scene: `onready var platf_scene_1 = preload("res://2D_landscape.tscn")`.
- Add a `CanvasLayer` node named `Platformer` in the adventure scene and add the instanced platformer as its child when the quest starts. WHY: a layer keeps the sub-game positioned and drawn above the board regardless of board coordinates.
- Trigger the quest from a button: in `_on_quest_btn_button_down()` do `var platform = platf_scene_1.instance()` then `$Platformer.add_child(platform)`.
- Treat the quest as optional content offered when the character reaches an unexplored field.

## Checklist
- [ ] Platformer scene saved and preloaded (not loaded at runtime).
- [ ] `Platformer` layer node exists in the adventure scene.
- [ ] Quest button signal connected and handler instantiates the scene.
- [ ] Sub-scene position/size verified inside the layer.

## Anti-patterns
- Instantiating the platformer directly under the board root, so it inherits board transforms.
- Loading the scene with `load()` on every button press instead of preloading once.
- Adding the quest scene without a layer, causing it to be hidden behind board elements.

> CHECK: the chapter does not state how the quest ends or how the platformer returns control to the board — verify in the book's sample project.
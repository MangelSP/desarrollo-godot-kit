<!-- 1 Applying SOLID Principles in Godot (pp. 3-32) -->
---
name: solid-principles-godot-overview
topic: SOLID principles applied to Godot architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Treat scripts and scenes as the equivalent of classes: scripts provide inheritance/contracts, scenes provide composition/encapsulation. WHY: Godot's node-based system has no literal classes, so mapping OOP concepts onto scripts+scenes lets you apply SOLID directly.
- Apply SOLID as guidance, not law. Use it to reduce coupling and keep classes small; abandon it when it slows a prototype. WHY: over-engineering early is as harmful as spaghetti code.
- Apply SOLID aggressively only when the project is large, long-lived, or team-based. WHY: that is where merge conflicts, brittle dependencies, and scaling pain actually appear.
- For game jams and prototypes, prioritize a playable build over perfect architecture. WHY: players judge feel, not code structure.
- Use signals, Resources, and @export to decouple systems instead of direct node references. WHY: these are Godot's native abstraction mechanisms.

## Checklist
- Can you name the single purpose of each script in one sentence?
- Does adding a new content type (enemy, weapon, item) require editing existing scripts? If yes, OCP is violated.
- Do any scripts use hard-coded `get_node("../X")` paths? If yes, DIP is violated.
- Do subclasses change method signatures or return types of their parent? If yes, LSP is violated.
- Do base classes contain methods that most subclasses never use? If yes, ISP is violated.
- Are `_process`/`_physics_process` bodies longer than a few delegation calls?

## Anti-patterns
- Treating SOLID as rigid law and blocking progress on small projects.
- Assuming Godot's lack of `class`/`interface` keywords means OOP principles don't apply.
- Letting one script accumulate input, movement, health, UI, and audio logic.
- Adding features by growing `if/elif` chains on node names instead of using polymorphism.

---
name: srp-single-responsibility-godot
topic: Single Responsibility Principle in Godot scripts and nodes
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- A script should have exactly one reason to change. If you can list multiple unrelated reasons (movement, health, UI, audio), split it. WHY: each extra responsibility is a separate risk of breaking unrelated features.
- Keep `_physics_process`/`_process` as a high-level manager that delegates to single-purpose methods (`_apply_gravity`, `_handle_movement_input`, `_handle_jump_input`). WHY: a 50-line inline loop is unreadable and hard to modify.
- Push responsibilities into child nodes/components: `HealthComponent`, `AudioComponent`, `SaveComponent`. WHY: composition is Godot's natural strength and keeps the root script small.
- Attach a dedicated script to child nodes (e.g., `AudioManager.gd` on the `AudioStreamPlayer`) rather than driving that node's logic from the parent. WHY: the parent then only calls `play_footstep()` and stays ignorant of details.
- Replace direct references to UI/audio with signals (`health_changed`, `player_damaged`). WHY: decouples the emitter from any specific listener.
- Split monolithic scripts into separate files (`PlayerMovement.gd`, `PlayerHealth.gd`) when multiple developers work in parallel. WHY: monolithic files cause constant merge conflicts in Git.
- Use dependency injection via `@export` variables so a script receives its dependencies instead of creating them. WHY: makes the script reusable and testable.
- Type injected dependencies explicitly (e.g., `@export var audio_component: AudioComponent`) rather than `Node`. WHY: you get autocomplete and type safety, at the cost of flexibility.
- Implement `_get_configuration_warnings()` to flag unassigned `@export` dependencies. WHY: surfaces forgotten Inspector assignments as a yellow warning before runtime.
- Add `@tool` to scripts that use `_get_configuration_warnings()` so the check runs in the editor. WHY: warnings must appear before you press Play.

## Checklist
- Does the script handle both logic and presentation? If yes, split.
- Does the script create its own dependencies with `new()` or `load()`? If yes, inject them instead.
- Are there more than ~3 unrelated responsibilities in the file?
- Would moving a UI node in the Scene Tree break this script? If yes, it is coupled to structure.
- Could this movement logic be reused on an NPC without dragging UI/audio along?

## Anti-patterns
- A `Player.gd` that handles input, movement, health, HUD updates, and SFX playback.
- A `GameManager` that manages player data, game state, and UI all at once.
- Calling `health_label.text = ...` and `audio_player.play()` directly from gameplay logic.
- Using `new()`/`load()` inside a gameplay script to build its own helpers.

---
name: ocp-open-closed-godot
topic: Open/Closed Principle via inheritance and Resources
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Create a base `Enemy` class with common state (`damage`, `health`) and an overridable `attack(target)` method; let each enemy type extend it. WHY: new enemies are added without touching the base or the Player.
- Have the Player call `body.attack(self)` after checking `body.is_in_group("enemies")` and `body.has_method("attack")`. WHY: the Player stays closed for modification regardless of enemy count.
- Register base classes with `class_name` so they are globally available. WHY: enables `extends Enemy` and type checks without preloads.
- Use custom `Resource` scripts (e.g., `WeaponStats extends Resource` with `@export` damage/cooldown) to define content variants as `.tres` files. WHY: hundreds of weapons can be authored in the Inspector with zero code changes.
- Choose Duck Typing (`has_method("attack")`) when you want maximum flexibility across unrelated types. WHY: any node with the method qualifies, including non-`Enemy` types like traps.
- Choose Explicit Typing (`body is Enemy`) when you want autocomplete and strict safety. WHY: guarantees you interact with the expected class, at the cost of rejecting non-inheriting types.

## Checklist
- Does adding a new enemy/weapon/item require editing an existing script? If yes, refactor.
- Is there a growing `if/elif` chain keyed on node names or types?
- Are shared behaviors in a base class and specialized behaviors in subclasses?
- Are data-driven variants expressed as `.tres` Resources rather than code branches?

## Anti-patterns
- A `match`/`if-elif` block in `Player.gd` listing every enemy type by name.
- Editing the base `Enemy` class every time a new enemy is added.
- Hard-coding weapon stats in scripts instead of exporting them as Resources.

---
name: lsp-liskov-substitution-godot
topic: Liskov Substitution Principle and contract safety in GDScript
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Subclasses must keep the same method signatures and return types as their parent. WHY: GDScript is dynamically typed; the editor will not warn you, and the game crashes at runtime.
- If a subclass needs extra data, add new methods (e.g., `get_max_health()`) instead of changing the parent's contract. WHY: existing callers relying on the base contract keep working.
- Callers should guard optional subclass methods with `has_method("get_max_health")` before invoking them. WHY: lets subclasses extend capability without breaking base-class assumptions.
- Prefer strict Static Typing where practical. WHY: it turns LSP violations into editor errors instead of runtime crashes.
- Ensure every subclass can handle every signal and method call the parent could handle. WHY: prevents "Game Over" crashes when the engine calls a missing or mismatched method.

## Checklist
- Do all overrides return the same type as the parent method?
- Do all overrides accept the same argument count and types?
- Are new capabilities exposed as additional methods rather than modified signatures?
- Are optional methods guarded with `has_method()` at call sites?

## Anti-patterns
- Overriding `get_health() -> int` to return a `String` in a subclass.
- Removing a parent method (e.g., `take_damage()`) in a subclass.
- Changing argument types in an override and assuming callers will adapt.

---
name: isp-interface-segregation-godot
topic: Interface Segregation via minimal base classes, signals, and components
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Keep base classes minimal: only shared state and truly universal behavior (`take_damage()`, `_die()`). WHY: subclasses should not inherit dead or stubbed methods.
- Put specialized behavior (shooting, slashing, igniting) in the subclass, not the base. WHY: prevents method pollution and keeps the API honest.
- Use focused signals (`health_depleted`, `ammo_changed`) instead of one fat signal carrying a Dictionary. WHY: listeners subscribe only to data they care about.
- Use node composition for optional abilities: attach a `FlyComponent` only to entities that fly. WHY: entities without the ability carry no empty methods.
- Let callers trigger subclass attacks polymorphically via a shared method name (`attack(target)`) or signals. WHY: avoids forcing a common interface that not all subclasses need.

## Checklist
- Does the base class expose methods that most subclasses never call?
- Are there empty or stubbed overrides in subclasses?
- Are signals narrow and purpose-specific?
- Are optional abilities implemented as attachable components rather than base methods?

## Anti-patterns
- A single `Entity` class with `fly()`, `swim()`, and `cast_magic()` for all subclasses.
- A `player_updated(data_dict)` signal that forces every listener to parse a dictionary.
- Adding new attack types by editing the base class (also violates OCP).

---
name: dip-dependency-inversion-godot
topic: Dependency Inversion via exports, signals, and a Signal Bus
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Never use hard-coded `get_node("../Player")` paths in gameplay logic. WHY: it couples the script to the exact Scene Tree layout and breaks on any reorganization.
- Inject dependencies with `@export var target: Node2D` and assign them in the Inspector. WHY: the script no longer cares where the node lives.
- Have children emit signals rather than calling specific parent methods. WHY: the parent depends on the child's signal, not the child on the parent's concrete class.
- For global systems, treat Autoloads as abstractions (Service Locator / Event Bus), not concrete managers. WHY: direct `AudioManager.play_sound()` calls couple every caller to that implementation.
- Implement a Signal Bus: an `Events.gd` Autoload declaring signals like `player_damaged(amount)` and `game_over`. WHY: sender and receiver are fully decoupled and either side can be replaced.
- Emit from high-level code (`Events.player_damaged.emit(amount)`) and connect from low-level code (`Events.player_damaged.connect(_on_player_damaged)`). WHY: both sides depend only on the abstraction.

## Checklist
- Are there any `get_node()` calls with relative paths in gameplay scripts?
- Are cross-system dependencies injected via `@export` or routed through the Signal Bus?
- Do enemies ever touch player internals or the HUD directly?
- Can you swap the UI or audio system without editing gameplay scripts?

## Anti-patterns
- An `Archer.gd` that does `get_node("../Player").health -= 10` and then updates the HUD.
- Calling Autoload methods directly from many scripts, creating hidden global coupling.
- Passing a parent reference into a child so the child can call parent methods.

---
name: extensible-interaction-system
topic: Combining OCP and ISP for an extensible interaction system
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Define an `Interactable` base (`class_name Interactable extends Area2D`) with an `interact(user: Node)` method that warns if not overridden. WHY: establishes the contract without complex inheritance.
- Have concrete items (`Chest`, `Door`, `Lever`) extend `Interactable` and override `interact()`. WHY: new interaction types are added without touching the Player.
- Give the Player an `@export var interaction_area: Area2D` and query `get_overlapping_areas()` on the interact action. WHY: the Player detects by abstraction, not by object name.
- Check `if area is Interactable` before calling `area.interact(self)`, then `return` after the first hit. WHY: type-based dispatch keeps the Player closed for modification.
- Never branch on `collider.name == "Door"` / `"Chest"`. WHY: name-based checks break on rename and require editing the Player for every new interactable.

## Checklist
- Does adding a new interactable require editing `Player.gd`? If yes, refactor.
- Is the interaction contract expressed as a base class or shared method name?
- Is the detection area injected via `@export` rather than hard-coded?
- Does the Player stop after the first successful interaction?

## Anti-patterns
- `if collider.name == "Door": collider.open() elif collider.name == "Chest": collider.loot()`.
- Checking concrete class names instead of the `Interactable` abstraction.
- Hard-coding the interaction area path with `get_node()`.

---
name: feature-based-project-structure
topic: Organizing Godot projects by feature instead of file type
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 1 (pp. 3-32)"]
---
## Rules
- Group files by feature, not by file type: `res://Player/` holds `Player.gd`, `Player.tscn`, `PlayerIcon.png`; `res://Enemies/Goblin/` holds `Goblin.gd`, `Goblin.tscn`, `GoblinSkins.png`. WHY: everything needed to work on one system lives in one folder.
- Keep each feature folder self-contained so it can be dragged into another project with all dependencies. WHY: enables reuse in sequels or other projects.
- Avoid top-level `res://Scripts/`, `res://Scenes/`, `res://Sprites/` splits for growing projects. WHY: it forces jumping between three folders to work on one feature and violates SRP at the project level.

## Checklist
- Can you work on the Player by opening a single folder?
- Could you copy a feature folder into a new project and have it compile?
- Are assets colocated with the scenes and scripts that use them?

## Anti-patterns
- Organizing by file extension once the project reaches hundreds of files.
- Scattering a single feature's scripts, scenes, and assets across three global folders.

<!-- 2 Deciding Between Scenes and Scripts (pp. 33-58) -->
---
name: scene-vs-script-decision
topic: Choosing between scenes and scripts in Godot 4
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 2 (pp. 33-58)"]
---
## Rules
- Use a **scene (.tscn)** when the object has visual structure, a node hierarchy, or is reused as a prefab (player, enemy, UI layout, level). WHY: scenes are declarative data that Godot parses and instantiates in one optimized pass.
- Use a **standalone script (.gd)** when the feature is pure logic or data with no visual representation (save system, damage calculator, state machine, tooling). WHY: avoids the memory and transform-tracking overhead of the Scene Tree.
- Prefer `RefCounted` for temporary logic objects that should auto-free when no longer referenced. WHY: prevents memory leaks without manual cleanup.
- Prefer `Resource` (.tres) for passive, serializable game data (enemy stats, item definitions, config). WHY: it is a data container that can be saved to disk and edited without code changes.
- Keep static structure (node creation, textures, positions, collision shapes) in the scene, not in `_ready()`. WHY: declarative setup is faster and easier to maintain than imperative `Node.new()` + `add_child()` chains.
- Keep behavior and dynamic logic in scripts. WHY: scripts are imperative and define *how* things act, complementing the scene's *what*.
- Use `class_name` on script-only classes to register them globally and expose them in the Create New Node dialog. WHY: bridges scripts into the editor workflow.
- Use `@tool` when a script must run inside the editor (visual debug gizmos, `_get_configuration_warnings` validation). WHY: catches misconfiguration before runtime.
- Use `@export` references instead of `$Path` lookups for components. WHY: decouples logic from tree structure and survives node renames.
- Organize exports with `@export_group`, `@export_subgroup`, and `@export_category`. WHY: keeps the Inspector usable as the project scales and self-documents for future you.

## Checklist
- Does the feature need a visual representation or node hierarchy? → scene.
- Is it pure logic/data with no world presence? → script.
- Will it be instanced multiple times? → scene (or Resource component).
- Does it need to be saved to disk? → Resource.
- Does it need editor-time behavior? → add `@tool`.
- Are there more than ~5 exported variables? → group them.

## Anti-patterns
- Building node trees imperatively in `_ready()` when the structure is constant. WHY: slower and harder to maintain than a scene.
- Wrapping pure logic (e.g., save/load) in a scene with invisible nodes. WHY: unnecessary Scene Tree overhead.
- Using `$Path` references for swappable components. WHY: breaks on rename and couples logic to hierarchy.
- Putting volatile, frequently changing data into scene properties. WHY: clutters version-control diffs; a script or Resource is cleaner.

---
name: scene-instantiation-performance
topic: Scene loading and instantiation performance
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 2 (pp. 33-58)"]
---
## Rules
- Use `preload()` for scenes you know you will need, storing them in a `const`. WHY: parses the file at script load time, avoiding mid-gameplay stutter.
- Use `load()` only when the path is dynamic (built at runtime) or when the asset is large and may never be used. WHY: `preload()` requires a static string and forces the asset into memory immediately.
- For very large scenes (whole levels, dense environments), use threaded loading via `ResourceLoader.load_threaded_request()`, poll with `load_threaded_get_status()`, then retrieve with `load_threaded_get()`. WHY: keeps the main loop running so animations and loading UI stay smooth.
- For small scenes (a few dozen nodes), prefer simple synchronous loading. WHY: instantiation completes in a fraction of a frame; threaded complexity is unnecessary.
- Only reach for threaded loading when you can actually feel the freeze during transitions. WHY: avoid premature complexity.

## Checklist
- Is the scene path known at compile time? → `preload()`.
- Is the path computed at runtime? → `load()`.
- Is the asset huge and possibly unused? → `load()` on demand.
- Is the scene so large it freezes even a loading screen? → threaded `ResourceLoader`.
- In threaded loading: request → poll status in `_process` → retrieve → `set_process(false)`.

## Anti-patterns
- Calling `load("res://x.tscn").instantiate()` inside a gameplay action (e.g., firing a weapon). WHY: synchronous parse causes a visible frame drop.
- Preloading massive late-game assets that most players never see. WHY: wastes RAM.
- Leaving the `_process` polling loop running after a threaded load completes. WHY: needless per-frame work; call `set_process(false)`.

---
name: inherited-scenes-vs-composition
topic: Balancing inheritance and composition
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 2 (pp. 33-58)"]
---
## Rules
- Use **Inherited Scenes** for visual specialization: same node structure and scripts, different sprites, scales, colors, or stats (Goblin/Orc/Troll from BaseEnemy; Confirm/Cancel from BaseButton). WHY: base-scene changes propagate to all variants, avoiding edits across many files.
- Use **script inheritance** for logic specialization: a subclass that meaningfully adds or overrides behavior. WHY: shared functions and variables without duplicating code.
- Use **composition (components/Resources)** for functional additions: mix-and-match capabilities like Health, Attack, Patrol. WHY: a HealthComponent can be reused by Player, Enemy, and Crate.
- Prefer composition over deep inheritance chains in large projects. WHY: composition stays modular and scales; deep trees become rigid spaghetti.
- If a subclass only reuses superclass behavior without modifying it, convert it to a component instead. WHY: inheritance without specialization is a sign of misapplied reuse.
- For mutable per-instance data on shared Resources, either enable **Local to Scene** in the Inspector or call `duplicate()` in code. WHY: Resources are shared by reference by default, so one Goblin's damage would affect all.
- Keep shared Resources for static read-only data (base damage, max health); duplicate for volatile state (current HP). WHY: balances memory savings with correct per-instance state.

## Checklist
- Do variants share a strict fundamental identity? → Inherited Scene.
- Does the subclass add/override meaningful behavior? → script inheritance.
- Do unrelated objects share a capability? → component/Resource.
- Is the Resource mutable per instance? → Local to Scene or `duplicate()`.
- Is the inheritance chain deeper than 2–3 levels? → refactor toward composition.

## Anti-patterns
- Manually rebuilding 50 enemy scenes by hand instead of inheriting from a base. WHY: a single collision-layer change would require editing 50 files.
- Sharing a mutable Resource across many instances without duplication. WHY: all instances read/write the same data container.
- Deep inheritance trees for behavior variation. WHY: rigid and hard to change; composition handles it better.

---
name: resource-based-components
topic: Resource-based behavior components
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 2 (pp. 33-58)"]
---
## Rules
- Define a base component as a `Resource` subclass (e.g., `AttackComponent extends Resource`), then create specialized `.tres` variants that override methods. WHY: swap behavior by swapping a data file, no subclassing of the host.
- Expose the component on the host with `@export var attack_component: AttackComponent`. WHY: designers assign it in the Inspector; logic stays decoupled from the tree.
- Assign components via code with `ComponentClass.new()` when you prefer not to use the editor. WHY: same flexibility without Inspector wiring.
- Use components for anything you plan to reuse or fine-tune; use a single custom script only for truly unique behavior. WHY: components reduce duplication and narrow bug searches.
- Prototype first, architect second: hard-code a mechanic, prove it works, then extract to a component when you need it in ~10 places. WHY: avoids over-engineering during exploration.
- Skip the component approach for game jams, small projects, or one-off bosses with non-reusable mechanics. WHY: upfront setup cost outweighs benefit when speed matters.

## Checklist
- Will this behavior appear on more than one object type? → component.
- Will designers need to tweak values without code? → Resource component.
- Is this a one-off mechanic? → single script is fine.
- Are components small and single-responsibility? → aligns with SOLID.
- Are exported components grouped in the Inspector? → use `@export_group`.

## Anti-patterns
- Copy-pasting near-identical attack/health code into dozens of enemy scripts. WHY: duplication multiplies bugs and maintenance.
- Forcing the component pattern onto a small prototype. WHY: slows iteration for no long-term gain.
- Using `@onready var x = $Component` for swappable components. WHY: breaks on rename and couples to tree layout; use `@export` instead.

---
name: hybrid-scene-script-resource-architecture
topic: Hybrid architecture combining scenes, scripts, and resources
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 2 (pp. 33-58)"]
---
## Rules
- Split complex systems by responsibility: scene = presentation, Resource = data, standalone script = logic. WHY: each layer uses the tool it is best at, keeping the whole maintainable.
- Example split for a weapon: `assault_rifle.tscn` holds Sprite2D, AudioStreamPlayer, and a Marker2D spawn point; `rifle_stats.tres` holds fire rate, damage, and ammo; `ballistics.gd` (no node) holds bullet-drop and wind formulae. WHY: designers tune balance in data, programmers own logic, artists own visuals.
- Link scenes and scripts through Autoloads and Resources for cross-system access. WHY: provides shared services without hard tree dependencies.
- Treat the scene/script choice as a spectrum, not binary. WHY: real systems combine declarative structure with imperative behavior.

## Checklist
- Does the system mix visuals, data, and logic? → split into scene + Resource + script.
- Is balance data separated from code? → move to a `.tres`.
- Are cross-cutting services (save, audio, input) available globally? → Autoload.
- Can a designer change behavior without touching code? → yes if data lives in Resources.

## Anti-patterns
- Forcing an entire complex system into one scene or one script. WHY: becomes messy and hard to extend.
- Hard-coding balance values (damage, fire rate) inside scripts. WHY: blocks designer iteration and clutters diffs.
- Coupling logic to specific node paths across systems. WHY: brittle; use exported references or Autoloads.

<!-- 3 Organizing Scenes for Scalability (pp. 59-86) -->
---
name: modular-scene-hierarchies
topic: Scene composition and modularity in Godot 4
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Make every scene runnable in isolation (F6) without crashing: it must not depend on a specific parent node existing. WHY: isolated scenes are testable, reusable, and safe to refactor.
- Keep gameplay scene trees shallow. Nesting depth is a coupling cost, not organization. WHY: each extra level tightens coupling and makes debugging harder.
- Exception: UI scenes may nest deeply (MarginContainer > VBoxContainer > Panel > HBoxContainer) because those nodes only handle visual layout, not logic. WHY: responsive containers need nesting; logic does not.
- Extract repeated sub-structures (engine, thruster, sound) into their own scene and instance them, instead of embedding them in every parent. WHY: one authoritative version, no duplicated logic, lower memory footprint.
- For internal node references inside a scene, prefer Scene Unique Nodes (`%ShieldBar`) or `@export` variables over hard-coded paths like `get_node("UI/Container/Label")`. WHY: unique names survive moving the node anywhere inside the same scene.
- Store unique-node references at the top of the script with `@onready var shield_bar: ProgressBar = %ShieldBar`. WHY: one clear, refactor-safe reference point.
- Use `@export` for references a designer should wire in the Inspector (e.g. a UI node pointing at the player); use `%` for purely internal references. WHY: `@export` clutters the Inspector and can be cleared accidentally.
- When instancing a projectile at runtime, add it to the game world (`get_tree().root.add_child(...)`), not to the firing ship. WHY: a child of the ship would inherit the ship's movement.
- Set the spawned object's `global_position` (and `rotation` if needed) after `add_child()`. WHY: global transforms are only valid once the node is in the tree.
- Use `preload()` for projectile scenes so they are ready in memory before firing. WHY: avoids a load hitch on the first shot.
- Use editor drag-and-drop instancing for static objects (doors, placed asteroids); use runtime `instantiate()` for dynamic content (projectiles, loot, enemy waves). WHY: dynamic objects cannot be placed beforehand.

## Checklist
- Can I press F6 on this scene and have it run without null errors?
- Does this scene represent exactly one focused idea (PlayerShip, EnemyDrone, CockpitUI)?
- Is any node structure duplicated across two or more scenes? → extract to a scene.
- Are internal references using `%` or `@export` rather than long paths?
- Are runtime-spawned objects parented to the world root, not to the spawner?

## Anti-patterns
- One giant scene containing player, enemies, and UI. WHY: merge conflicts, broken paths, untestable pieces.
- Hard-coded paths like `get_node("../CockpitUI/HealthBar")` from inside a gameplay scene. WHY: breaks on any tree reorganization.
- Adding extra plain `Node`s purely to group things visually in the tree. WHY: adds depth and coupling for zero functional gain.
- Exposing dozens of internal components as `@export` just to avoid unique names. WHY: Inspector clutter and accidental clearing of essential references.

---
name: instancing-vs-inherited-scenes
topic: Choosing between composition and specialization
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Use **Instancing (composition)** when you need to combine distinct pieces of functionality, or place multiple copies of the same object. Examples: asteroids in a level, a Laser Cannon scene attached to a PlayerShip.
- Use **Inherited Scenes (specialization)** when you need a variation of a generic object that shares common logic. Example: `BaseEnemy.tscn` → `KamikazeDrone.tscn`, `HeavyBomber.tscn`.
- Build a `BaseEnemy.tscn` with collision shape, AI script, and base sprite; create variants via *New Inherited Scene* (Ctrl+Shift+N). WHY: changes to the base propagate to all variants automatically.
- Override only the differing properties in the inherited scene (sprite texture, speed, damage). WHY: keeps the variant minimal and the shared logic single-sourced.
- For larger games, move tunable stats out of the Inspector into custom `Resource` files (e.g. `WeaponStats` → `plasma_stats.tres`) plugged into the inherited scene. WHY: separates data from the visual tree and enables data-driven design.
- If you copy-paste the same node structure into many scenes, convert it to a scene and instance it. WHY: one edit updates every instance; copy-paste requires editing every copy.

## Checklist
- Am I combining parts (→ instance) or specializing a base (→ inherit)?
- Does the base scene contain only logic shared by all variants?
- Are variant differences limited to overridden properties or swapped resources?
- Would a designer need to change these numbers often? → consider a Resource.

## Anti-patterns
- Duplicating a `Fuel Canister` structure into 50 levels and later editing each one. WHY: maintenance nightmare and human error.
- Using inheritance to bolt unrelated functionality onto a base class. WHY: inheritance is for specialization, not composition.
- Hard-typing stat values into many inherited scenes when a shared Resource would do. WHY: data drift and no single source of truth.

---
name: call-down-signal-up
topic: Loose coupling between scenes
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Golden rule: **Call Down, Signal Up.** Parents call methods on their children; children emit signals upward and never call their parent directly. WHY: a child should not need to know who its parent is.
- Siblings must never reference each other. Route through the parent: sibling A signals up, parent calls down to sibling B. WHY: keeps siblings fully decoupled.
- Direct references are fine *within* one encapsulated scene (e.g. `player_ship` calling `blaster.fire()` on its own child). WHY: the child is an intrinsic part of that scene.
- Direct references across unrelated scenes (Player → UI, Player → GameManager) are an anti-pattern. Use signals or an EventBus instead. WHY: cross-scene paths break on any tree change.
- Connect signals in code inside `_ready()` for dynamic objects rather than visually in the editor. WHY: the connection lives next to the logic and is easy to read.
- To let a listener find an emitter without brittle paths, expose an `@export var player_node: Node2D` and wire it in the Inspector. WHY: safe, explicit, refactor-proof.
- Prefer signal listeners over polling in `_process`. WHY: listeners run only on the event, not every frame.
- For global broadcasts (score, lives, weapon changes), use an Autoload EventBus singleton with typed signals. WHY: no node needs a reference to any other node.
- Suppress the "unused signal" warning in the EventBus with `@warning_ignore("unused_signal")`. WHY: EventBus signals are emitted by other scripts, so the warning is a false positive.

## Checklist
- Does any child node call a method on its parent or a sibling? → convert to a signal.
- Does any script use `get_node("../...")` to reach outside its own scene? → replace with signal or `@export`.
- Are signal connections made in `_ready()` for runtime-created objects?
- Is the EventBus registered under Project Settings → Globals → Autoload?
- Can this scene be dropped into an empty test level and still work?

## Anti-patterns
- `get_node("../CockpitUI/HealthBar").update_health(health)` from the player script. WHY: breaks when the UI moves; player cannot exist without the UI.
- A button searching for its Menu parent to call a function. WHY: the button should emit `pressed` and let the parent decide.
- Two sibling components (Weapon, Movement) referencing each other directly. WHY: creates a hidden dependency web; the parent should mediate.

---
name: groups-for-management
topic: Using groups to categorize nodes
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Use the scene hierarchy for spatial ownership (moving a parent moves children); use groups for logical tags (all enemies, all destructibles). WHY: they solve different problems.
- Register nodes in `_ready()` with `add_to_group("Destructible")`. WHY: registration happens automatically as soon as the node spawns.
- Broadcast to a group with `get_tree().call_group("Destructible", "take_hit", 100)`. WHY: one call reaches every member without keeping references.
- Keep group names semantic and non-technical: `Collectibles`, `Destructible` — not `Group1`. WHY: names are read by humans during debugging.
- One concept per group. A node may belong to several groups, but each group should mean one thing. WHY: overlapping semantics make membership unpredictable.
- Use groups for management tasks: multiplayer entity sync, environmental triggers responding to one event, showing/hiding UI on transitions, updating all audio players from a volume slider.
- Prefer an EventBus with typed signals over `call_group` for complex broadcasts. WHY: IDEs can trace signals but not magic strings.

## Checklist
- Is this relationship spatial (parent/child) or logical (tag)? → choose hierarchy or group accordingly.
- Does every group name describe a single concept?
- Does every member of the group actually implement the method being called?
- Could this broadcast be a typed EventBus signal instead?

## Anti-patterns
- `call_group("Destructible", "take_hit", 100)` when members may not all have `take_hit(int)`. WHY: blind assumption; runtime errors and no IDE tracing.
- Using groups as a substitute for scene structure. WHY: groups are logic-level relationships, not hierarchies.
- Names like `Group1`, `Stuff`, `Misc`. WHY: meaningless to teammates and future you.

---
name: naming-conventions-and-folders
topic: Team naming and project folder structure
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Prefix node names by role: `UI_`, `Enemy_`, `Menu_`, `Btn_`, `Lbl`. WHY: distinguishes a `HealthLbl` from a `health` variable at a glance.
- Use `snake_case` for all files: scenes (`main_menu.tscn`) and scripts (`enemy_controller.gd`).
- Keep the scene's root node in `PascalCase` (`MainMenu`) to match Godot's native class naming.
- Align file names with class names: `enemy_controller.gd` defines `class_name EnemyController`. WHY: global search and Quick Load find the file by class name.
- Organize the project by type: `Assets/` (raw .png, .wav, fonts), `Scenes/` (assembled .tscn, subfoldered by Levels/UI/Characters), `Scripts/` (.gd, mirroring the Scenes structure). WHY: separates imported data from built content and reduces cognitive load.
- Pick one strategy (by Type or by Feature) and make every team member follow it. WHY: consistency matters more than the specific choice.
- Optimize for predictability over personal preference. WHY: nobody should spend mental energy deciding where a file goes.

## Checklist
- Do node names carry a role prefix where ambiguity is possible?
- Are all files `snake_case` and all scene root nodes `PascalCase`?
- Does each script's `class_name` match its filename?
- Can a new teammate find a goblin sprite without opening a script?
- Is the folder strategy documented and followed by everyone?

## Anti-patterns
- Mixed casing (`MainMenu.tscn`, `mainmenu.tscn`, `Main_Menu.tscn`) in the same project. WHY: breaks search and tooling assumptions.
- A flat `res://` dumping ground once the asset count reaches hundreds. WHY: impossible to locate files; artists and programmers step on each other.
- Scripts scattered next to scenes with no mirror structure. WHY: external editors like VS Code treat the project as a file system and become hard to navigate.

---
name: avoiding-scene-tree-bloat
topic: Preventing and fixing Scene Tree bloat
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Load and free scenes dynamically: instantiate only when needed, and call `queue_free()` as soon as the object is done. WHY: keeps active node count low and memory footprint small.
- Example: a collectible calls `queue_free()` immediately after the player collects it.
- Use signals and groups instead of hard references to specific nodes. WHY: avoids a tangled dependency web that breaks on any move.
- Move static or configuration data (RPG stats, inventory lists, settings) into `Resource` (.tres) files instead of Nodes. WHY: Resources are lighter and keep the tree for visual/logic objects only.
- Refactor when one node handles too many tasks (input + movement + inventory UI). Extract logic into child scenes or separate scripts. WHY: every node should have one clear purpose.
- Split UI into its own scene and instance it where needed; go further by making each UI element its own scene. WHY: elements can be added or removed without touching existing ones.
- Target clarity, not minimalism: the goal is not the fewest nodes, but every node having a reason to exist.

## Troubleshooting table
| Symptom | Diagnosis | Fix |
|---|---|---|
| Endless scrolling in the tree | Tree too long, can't find nodes | Modularize: split UI/environment branches into their own `.tscn` and instance them back |
| Broken paths / null instance errors when moving a UI element | Hard-coded `get_node("root/UI/Bar")` | Decouple: use Scene Unique Nodes (`%Bar`) or signals |
| Copy-paste fatigue across 50 copies | Duplicated node structures | Inheritance: create a Base scene, make variants Inherited Scenes |
| Slow load times / freeze on level load | Thousands of objects spawned at once | Runtime Instancing: `instantiate()` heavy objects only when needed |

## Checklist
- Are any nodes kept in the tree purely to store data? → move to a Resource.
- Does any scene reload every frame instead of using sub-scenes?
- Are there "container" nodes with dozens of children that serve no logic?
- Does any single node handle more than one clear responsibility?
- Are off-screen or finished objects freed with `queue_free()`?

## Anti-patterns
- Keeping every object active in the tree for the whole level. WHY: memory and runtime cost, plus a tree nobody can navigate.
- Using Node objects as data containers for stats or settings. WHY: bloats the tree and mixes data with presentation.
- Deeply nested signals or hard-coded sibling dependencies. WHY: fragile and hard to debug.
- Never refactoring a growing "god node". WHY: it becomes the single point of failure for the whole scene.

---
name: scalable-architecture-void-defenders
topic: Reference architecture — EventBus, weapon components, PlayerShip
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 3 (pp. 59-86)"]
---
## Rules
- Create an `event_bus.gd` Autoload (Project Settings → Globals → Autoload) holding typed signals such as `score_changed(new_amount: int)`, `player_lives_changed(current_lives: int)`, `weapon_changed(weapon_name: String, ammo: int)`. WHY: the purest form of loose coupling — no node knows any other node.
- Annotate EventBus signals with `@warning_ignore("unused_signal")`. WHY: they are emitted from other scripts, so the warning is a false positive.
- Build weapons as their own scenes. A projectile scene: `Area2D` root + `Sprite2D` + `CollisionShape2D` + `VisibleOnScreenNotifier2D`. WHY: Area2D is enough for hitboxes; the notifier frees off-screen projectiles.
- In the projectile script, connect `area_entered` and `screen_exited` in `_ready()`. WHY: connections live next to the logic.
- Move projectiles with `Vector2.UP.rotated(rotation)` in `_physics_process`. WHY: fixed timestep and the projectile always flies out of the muzzle.
- Free off-screen projectiles with `queue_free()` in the `screen_exited` handler. WHY: automatic garbage collection.
- On hit, check `area.has_method("take_damage")` before calling it, then `queue_free()` the projectile. WHY: duck typing keeps the projectile decoupled from any specific target type.
- Create the Plasma Blaster as an Inherited Scene of the Laser, overriding only speed, damage, and texture. WHY: shared movement logic, minimal variant.
- Build the Blaster as a component scene: `Node2D` root + `Marker2D` (Muzzle, ~-25px Y) + `Timer` (CooldownTimer, 0.5s, One Shot) + `AudioStreamPlayer2D` (FireSound). WHY: reusable across ship types.
- In `Blaster.fire()`, guard with `if not cooldown_timer.is_stopped(): return` and `if projectile_scenes.is_empty(): return`. WHY: prevents spam and crashes.
- Spawn projectiles with `get_tree().root.add_child(shot)`, then set `shot.global_position = muzzle.global_position` and `shot.rotation = global_rotation`. WHY: projectile must not inherit the ship's transform.
- Build the PlayerShip as `CharacterBody2D` + `Sprite2D` + `CollisionPolygon2D` + instanced `Blaster` + `Camera2D` + shield sprite + shield audio. Add the ship to the `Player` group.
- In `PlayerShip._physics_process`, call `blaster.fire()` on input (Call Down). In `take_damage()`, emit `EventBus.player_lives_changed` (Signal Up). WHY: the ship is self-contained and testable in an empty level.
- Use `get_tree().call_deferred("reload_current_scene")` for game over. WHY: deferred calls are safe during physics processing.

## Checklist
- Is the EventBus registered as an Autoload and are all signals typed?
- Does the projectile free itself off-screen and on impact?
- Does the Blaster guard against cooldown spam and empty projectile lists?
- Is the PlayerShip in the `Player` group?
- Can `PlayerShip.tscn` be dropped into an empty level and fly, shoot, and take damage with no null errors?

## Anti-patterns
- Adding spawned projectiles as children of the ship. WHY: they would move with the ship.
- Calling `area.take_damage()` without `has_method()` check. WHY: crashes on any overlapping Area2D that lacks the method.
- Hard-coding weapon stats in the Blaster script instead of `@export` or a Resource. WHY: no per-variant tuning, no data-driven workflow.
- Player script reaching into the HUD or GameManager directly. WHY: breaks the Call Down / Signal Up contract and kills reusability.

> CHECK: The chapter references Figure 3.2 (folder structure) and Figure 3.7 (orange inherited-scene indicator) as images; the exact folder tree and color legend are described in prose but not fully reproduced in the OCR text.

<!-- 4 When Not to Use Nodes (pp. 87-112) -->
---
name: node-overuse-recognition
topic: architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Treat the Scene Tree as a renderer/simulator, never as a database. Nodes are heavyweight: they carry transforms, pause modes, physics callbacks, `_process` hooks, and signal connections.
- Ask three questions before making something a Node. If all three answers are "No", do not use a Node:
  1. Does it need to draw on screen?
  2. Does it need physical collision?
  3. Does it need a position in the spatial parent/child transform hierarchy?
- Legitimate exceptions (utility nodes that depend on engine subsystems): `Timer` (scene clock), `AudioStreamPlayer` (audio bus), `AnimationPlayer` (frame loop).
- Pure data, math, or abstract logic belongs in a `Resource` or a plain `Object`/`RefCounted`.
- Detect the anti-pattern by looking for container nodes whose only job is to hold other nodes that only hold variables.
- Concrete smell: using `add_child()` to store data and `get_children()` to read it, instead of an `Array` or `Dictionary`.
- WHY: every node in a data-only role still pays tree-notification, transform, and pause-state costs for functionality you never use, and it couples your data to the Scene Tree.

## Checklist
- [ ] List every node in the scene; for each, name the draw/collide/transform reason it exists.
- [ ] Any node failing all three questions → convert to `Resource` (persistent) or `RefCounted` (transient).
- [ ] Inventory/cargo/stats/skill-tree systems are stored as typed arrays or dictionaries, not child nodes.
- [ ] Data survives with the UI closed (deleting the UI node must not delete the data).
- [ ] Game logic can run before the node enters the tree.

## Anti-patterns
- "Inventory Node": one child node per sword/potion/laser battery under a parent node.
- Instantiating a full `PackedScene` just to remember the player picked up one item.
- Reading inventory with `get_node()` or iterating children — breaks if logic runs before `_ready`.
- Keeping the inventory UI loaded permanently just to preserve item data.
- Treating the editor hierarchy panel as a visual database because it gives instant feedback.

> CHECK: OCR shows "idx_..." anchor artifacts throughout; ignore them, but verify the exact wording of the three Scene Tree questions against the print edition.

---
name: lightweight-object-hierarchy
topic: architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Choose the lowest tier of the object hierarchy that meets your needs; each step down removes engine overhead.
- Decision table:

| Class | Use case | Memory | Inspector | Serializable |
|---|---|---|---|---|
| `Object` | extreme performance, temporary data | manual `free()` | no | no |
| `RefCounted` | math calculators, logic managers, state machines | automatic | no | no |
| `Resource` | items, stats, configurable data, save files | automatic | yes | yes |
| `Node` | rendering, physics, scene hierarchy | automatic `queue_free()` | yes | partial |

- `Object`: use only for maximum-performance temporary structures where you accept manual memory management. Dangling references crash on access.
- `RefCounted`: default base for any script without `extends`. Reference-counted; deletes itself when the last reference goes out of scope. Use for pure logic, state machines, data processors that are not saved to disk.
- `Resource`: extends `RefCounted`, adds serialization to `.tres`/`.res` and Inspector support via `@export`. Use for anything a designer configures, anything saved to disk, anything shared between objects.
- Always write `extends RefCounted` explicitly even though GDScript defaults to it. WHY: signals intent and memory model to other developers without requiring engine trivia.
- Precedent: Godot's own `Tree` UI node uses lightweight `TreeItem` objects for rows instead of Nodes, so it can render thousands of rows cheaply.
- `FileAccess` is a `RefCounted`: the file stream closes and frees itself when the variable goes out of scope — no manual cleanup.

## Checklist
- [ ] Does this need to be saved to disk? → `Resource`.
- [ ] Does a designer need to edit it in the Inspector? → `Resource`.
- [ ] Is it shared by multiple objects? → `Resource`.
- [ ] Is it transient logic with no persistence? → `RefCounted`.
- [ ] Is it a hot-path temporary structure and you can manage memory? → `Object`.
- [ ] Does it draw, collide, or need a transform? → `Node`.

## Anti-patterns
- Extending `Node` for a pure math helper or state machine.
- Using `Object` when `RefCounted` would do — you inherit manual `free()` and dangling-pointer risk for no gain.
- Storing a reference to a freed `Object` and accessing it later.

---
name: resource-based-data-model
topic: data-driven-design
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Define custom `Resource` subclasses with `class_name` + `extends Resource` and `@export` fields to create data blueprints.
- Use `@export_multiline` for description text and `@export` for typed fields (`Texture2D`, `int`, `bool`).
- Use typed arrays for collections: `@export var items: Array[ItemData] = []`. WHY: the type system rejects invalid entries at the API boundary.
- Call `emit_changed()` after every mutation of a Resource's data. WHY: it broadcasts the built-in `changed` signal so listeners update without polling.
- Save player data with `ResourceSaver.save()`; load with the matching loader. No manual JSON serialization loop needed.
- Create concrete `.tres` files in the FileSystem via right-click → New Resource → search the `class_name`. One file per item/stat block (e.g. `PlasmaBlaster.tres`, `ScoutFighter.tres`).
- Inject volatile runtime data (player inventory) via a method call, not `@export`. WHY: prevents data bleed between save files and allows loading inventories on the fly.
- Keep the Resource blueprint authored once by a programmer; designers then create/duplicate/tune dozens of variants in the Inspector without touching GDScript.

## Checklist
- [ ] Data class extends `Resource`, not `Node`.
- [ ] Every designer-facing field has `@export`.
- [ ] Collections are typed arrays.
- [ ] Every mutator calls `emit_changed()`.
- [ ] Runtime-owned data is injected, not exported.
- [ ] Concrete `.tres` files exist for each variant.

## Anti-patterns
- Hardcoding stats as variables on an enemy node instead of a shared stats Resource.
- Exporting player-owned runtime data in the Inspector.
- Mutating a Resource array without `emit_changed()` — UI silently goes stale.

---
name: mvc-separation-data-and-presentation
topic: architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Split systems into three roles:
  - Model: pure `Resource` data (e.g. `CargoData`). Knows nothing about the screen.
  - View: Scene Tree UI nodes (`GridContainer`, `TextureRect`). Knows how to draw, nothing about game data.
  - Controller: a script that listens to Model signals and tells the View what to draw.
- Controller setup: store the model in a plain `var` (not `@export`), connect `model.changed` to an update function, then call the update function once to force the initial draw.
- Update function order: (1) clear existing visual children with `queue_free()`, (2) instantiate one slot scene per data entry, (3) push data into each slot.
- Guard optional slot APIs with `has_method()` before calling them.
- WHY: a bug in drag-and-drop UI can then never delete the player's cargo data; the data layer is unit-testable without creating any UI.

## Checklist
- [ ] Model has zero references to UI nodes.
- [ ] View has zero references to game data.
- [ ] Controller connects to `changed` and performs an initial draw.
- [ ] Update clears old children before rebuilding.
- [ ] Model can be tested in isolation.

## Anti-patterns
- UI script reading `get_children()` of a data node to find items.
- Data node holding a reference to its UI so it can refresh itself.
- Rebuilding UI without clearing old children (duplicate slots).

---
name: refcounted-logic-and-static-utils
topic: architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Stateless helpers: use `class_name X extends RefCounted` with `static func`. Call directly on the class (`GameUtils.get_screen_bounds(node)`); no instance, no Autoload, no node in the tree.
- Static functions cannot remember state between frames — use them only for pure computation.
- Stateful transient logic: instantiate a `RefCounted` subclass. Create it inside the function that needs it; when the local variable goes out of scope, Godot frees it automatically.
- Long-lived logic state: hold a `RefCounted` instance as a class-level variable on the owning node. When the owner is freed, the reference count drops to zero and the helper is freed too — no `queue_free()` needed.
- Pass context explicitly into static helpers (e.g. pass the calling `Node` so it can reach `get_viewport()`), rather than making the helper a node.
- WHY: logic that never calls `add_child()` never enters the visual hierarchy, so the engine skips transform updates, pause-state checks, and tree notifications for it.
- Example pattern: a `DamageRoll` created per hit, used for one calculation, then discarded; a `ComboTracker` held as a class variable for the player's lifetime.

## Checklist
- [ ] Pure math/utility → `static func` on a `RefCounted` class.
- [ ] Per-event calculation → instantiate, use, let it fall out of scope.
- [ ] Persistent logic state → class-level `RefCounted` variable on the owner.
- [ ] No `add_child()` anywhere in logic-only classes.
- [ ] `extends RefCounted` written explicitly.

## Anti-patterns
- Creating a `Manager` node for turn-based combat or loot generation.
- Registering a global Autoload for a stateless calculation.
- Putting damage formulas inside the Player node (violates Single Responsibility).

---
name: strategy-pattern-with-resources
topic: data-driven-design
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Define behavior as `Resource` subclasses so it can be swapped at runtime and configured in the Inspector.
- Use `@abstract class_name AttackPattern extends Resource` for the base. Mark the required method `@abstract` too.
- WHY `@abstract` on the class: the editor stops offering the base type in the New Resource menu, so only concrete subclasses appear.
- WHY `@abstract` on the method: subclasses that forget to implement it fail immediately instead of silently running an empty body.
- Concrete subclasses (`PlasmaBurst extends AttackPattern`) add their own `@export` fields (fire speed, projectile scene) and implement `execute(user, target)`.
- The consumer node exposes `@export var attack_pattern: AttackPattern` and only calls `attack_pattern.execute(self, target)`. It never branches on which attack it holds.
- This is composition over inheritance: the drone is granted an ability at runtime instead of being locked into a class hierarchy.
- Adding a new enemy variant is a data operation: create a generic enemy scene, create a new Resource file, tune values in the Inspector, drag it into the slot. No new code.
- WHY: polymorphism means the consumer is immune to feature creep — dozens of behaviors can be added without reopening its script.

## Checklist
- [ ] Base class and its required method both marked `@abstract`.
- [ ] Every behavior is a separate `Resource` file, not an `if/else` branch.
- [ ] Consumer exports the base type, not a concrete type.
- [ ] Consumer calls only the shared interface method.
- [ ] New variants require zero edits to consumer scripts.

## Anti-patterns
- One `Enemy.gd` with thousands of lines of `if/else` per attack type.
- `match` on an enum of attack types inside the enemy script.
- Exporting a concrete attack class instead of the abstract base (blocks swapping).

---
name: enemy-inheritance-and-scene-inheritance
topic: gameplay-architecture
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 4 (pp. 87-112)"]
---
## Rules
- Build a `BaseEnemy` scene: `Area2D` root + `Sprite2D` + `CollisionShape2D`, added to a `"Destructible"` group, with a script holding shared state (`speed`, `health`) and shared behavior (`die()`).
- Create variants with FileSystem → right-click base scene → New Inherited Scene. Rename the root; inherited children render orange in the editor.
- Override exported values in the Inspector per variant (e.g. health 20, speed 400) and swap the sprite texture.
- Detach the inherited script and attach a new one that does `class_name KamikazeEnemy extends BaseEnemy`. Only declare what is unique to the variant.
- Override `_physics_process` to replace generic movement with specialized movement; inherited variables like `speed` remain available.
- Find targets with groups: `get_tree().get_first_node_in_group("Player")`, and always null-check before using.
- For smooth turning, compute the direction angle and use `lerp_angle(rotation, target_rotation, rotation_speed * delta)` instead of `look_at()`. WHY: `look_at()` snaps instantly; lerping gives the player a fair chance to dodge.
- Add `PI / 2.0` to the target angle when the sprite's nose points up. WHY: Godot's 0 radians points along +X, so a 90° offset aligns the nose rather than the right wing.
- On collision, gate damage with both a group check and duck typing: `if body.is_in_group("Player") and body.has_method("take_damage")`.
- WHY inheritance here: DRY (one place to add a hit-flash effect for all enemies), fast new variants, and polymorphism (any system can trust every enemy has `take_damage()`).

## Checklist
- [ ] Base scene has shared state, shared cleanup, and a group membership.
- [ ] Variants are inherited scenes, not copies.
- [ ] Variant script extends the base `class_name`, not `Area2D`.
- [ ] Variant declares only new fields and overridden methods.
- [ ] Target lookup is null-checked with a fallback behavior.
- [ ] Damage application checks group + `has_method`.

## Anti-patterns
- Duplicating the base scene and editing both copies (drift).
- Variant scripts re-declaring `speed`/`health` already on the base.
- Using `look_at()` for a chasing enemy that should telegraph its turn.
- Applying damage to anything that collides, without a group or method check.

> CHECK: OCR renders "idx_..." anchors and one broken word ("nd listens") in the MVC section; verify the `changed` signal connection snippet against the print edition.

<!-- 5 Using Autoloads and Singletons (pp. 113-136) -->
---
name: autoload-basics
topic: Autoloads and the Singleton Pattern
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- Register a script or scene as an Autoload via Project Settings → Globals (Autoload tab); Godot instantiates it as a direct child of the root viewport at game start, outside the active level.
- The Node Name you assign becomes the global identifier used to call the script from anywhere (e.g. `GameState.player_health`, `AudioManager.play_sfx()`).
- Autoloads persist across `change_scene_to_file()` and `change_scene_to_packed()` because they are peers of the level, not children of it. WHY: the level subtree is destroyed on scene change, but the Autoload sits above it.
- Use Autoloads only for systems that must survive scene changes: audio managers, scene loaders/transitions, network managers, event buses, application-level config.
- Keep each Autoload single-purpose. WHY: a focused service is testable and refactorable; a broad one couples unrelated systems.
- Prefer an Event Bus Autoload (signals only) over Groups for global messaging. WHY: signals give IDE autocomplete and type safety, Groups rely on magic strings.

## Checklist
- Does this system need to survive a scene change? If no, do not make it an Autoload.
- Is it a service (audio, network, transitions, config) rather than data? If data, use a Resource instead.
- Is the Autoload small and single-purpose?
- Are callers decoupled via signals or injected references rather than hardcoded Autoload names?

## Anti-patterns
- Putting player state (health, inventory, position) in an Autoload. WHY: state persists after death/return to menu, requires manual resets, and breaks local multiplayer.
- Putting heavy visual scenes (3D pause menus, particle systems) in an Autoload. WHY: they stay in memory for the whole session.
- Creating one `GameManager`/`Global.gd` that handles spawning, score, upgrades, and dialogue. WHY: tight coupling, race conditions, memory bloat, painful refactors.
- Using Autoloads for stateless utility math. WHY: a Node costs memory and runs engine callbacks every frame; static functions cost nothing.

---
name: autoload-use-cases
topic: Sound use cases for Autoloads
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- AudioManager: hold the `AudioStreamPlayer` in the Autoload so music crossfades continue across level loads. Levels call `AudioManager.crossfade_music(path)`.
- SceneLoader / SceneManager: run fade-out, load the next `PackedScene` with `ResourceLoader`, then fade in. WHY: it exists between the two scenes, so it is the only object that survives the swap.
- NetworkManager: keep the `ENetMultiplayerPeer` and `multiplayer.multiplayer_peer` assignment in an Autoload so the socket survives lobby→gameplay transitions.
- EventBus: an Autoload that only declares signals. Senders call `EventBus.score_changed.emit(100)`; listeners call `EventBus.player_died.connect(show_game_over)`.
- ConfigurationManager: store application-wide settings (resolution, volume) that must apply everywhere.

## Checklist
- Audio: does music need to keep playing during a scene change? → Autoload.
- Transitions: does something need to exist while the old scene is destroyed and the new one loads? → Autoload.
- Networking: must the connection outlive any single scene? → Autoload.
- Cross-system messaging: do unrelated nodes need to talk without a node path? → EventBus Autoload.

## Anti-patterns
- Attaching an `AudioStreamPlayer` to a level scene. WHY: music cuts out the moment the level unloads.
- Attaching the network script to a lobby scene. WHY: switching to gameplay destroys the node and drops the connection.
- Wiring UI directly to the Player via `get_node()` paths. WHY: brittle; an EventBus decouples them.

---
name: avoiding-global-state
topic: Global state pitfalls and the God Object
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- Rule of thumb: Autoloads manage systems, not data. Add `AudioService`, not `PlayerStats`.
- Treat any Autoload variable that any script can mutate as a bug risk. WHY: non-linear data flow makes bugs hard to trace.
- If a low-level object (e.g. a Coin) hardcodes `GameManager.add_score(10)`, it is tightly coupled and will crash in any project or test scene without that Autoload.
- Split responsibilities: a God Object acting as database + audio engine + state machine + I/O means a change to one domain can break another.

## Checklist
- Does this Autoload hold mutable gameplay state? → move it to a Resource or the owning node.
- Does any local scene reference an Autoload by name inside gameplay logic? → refactor to signal or injected reference.
- Does the Autoload mix static data with active background systems? → split it.
- Would renaming one variable force edits across dozens of scripts? → the Autoload is too broad.

## Anti-patterns
- `Global.gd` holding `player_hp`, `inventory_list`, `current_level_name`, `music_volume`, `enemy_count`, `is_game_over` plus `save_game`/`load_game`/`play_sound`. WHY: violates single responsibility; race conditions on shared vars; permanent memory use; refactor nightmare.
- Assuming global accessibility implies global storage. WHY: reachability and ownership are different concerns.

---
name: dependency-injection-singletons
topic: Dependency injection and setter injection with Autoloads
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- For fire-and-forget events, replace hardcoded Autoload calls with a local signal on the object, and let the containing scene connect it to the Autoload.
  - Coin: `signal coin_collected(amount: int)` → `coin_collected.emit(10)`.
  - Level `_ready()`: `$Coin.coin_collected.connect(GameManager.add_score)`.
- For continuous queries (e.g. playing footsteps, fetching save data), use setter injection: declare a typed variable on the consumer and assign the Autoload in `_ready()`, allowing overrides.
- Define an interface with `@abstract` (Godot 4.5+) so injected services are strongly typed and autocomplete works.
- In tests, inject a dummy implementation of the interface instead of the real Autoload. WHY: tests run without loading audio files or initializing heavy systems.

## Checklist
- Is the interaction a one-shot notification? → signal.
- Is the interaction a repeated query/command? → setter injection with a typed variable.
- Does the consumer default to the global Autoload but allow replacement? → assign in `_ready()`, not at declaration.
- Does the interface exist as an `@abstract` class so mocks are type-safe?

## Anti-patterns
- Duck typing the injected service (assuming it has the right methods). WHY: no compile-time or IDE safety.
- Calling the Autoload name directly inside gameplay methods (`AudioManager.play_sfx(...)` in `jump()`). WHY: prevents swapping in a mock or alternative implementation.
- Skipping the interface and injecting raw Nodes. WHY: mocks become fragile and untyped.

---
name: singleton-alternatives
topic: Static functions, Resources, and Groups as Autoload alternatives
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- Static functions: use for stateless utilities and math (`class_name Utils` + `static func calculate_damage`). Zero memory overhead, thread-safe, portable across projects.
- Resources: use for static data and shared state (item stats, inventory, config). Player, HUD, and SaveManager can all reference the same `.tres`; changes are visible to all. Reference-counted, so memory is freed when unused.
- Groups: use for one-to-many broadcast (`get_tree().call_group("game_listeners", "on_player_died")`). Fire-and-forget; missing listeners cause no crash.
- Prefer an EventBus Autoload over Groups for global messaging. WHY: signals give autocomplete and type safety; Groups rely on magic strings.

## Checklist
- Stateless math/parsing? → static function.
- Shared data read by multiple systems? → Resource.
- Broadcast to many unknown listeners? → Group or EventBus signal.
- Persistent background service? → Autoload.

## Anti-patterns
- Using a static function for anything needing `_ready()`/`_process()` or a `self` reference. WHY: static functions have no instance lifecycle; you must pass a Node explicitly.
- Relying on Groups for critical logic. WHY: misspelled method names fail silently or throw hard-to-trace runtime errors.
- Storing dynamic state in a Resource without a save/load path. WHY: Resources are not designed to persist runtime state automatically.

---
name: data-driven-spawning-and-collision-layers
topic: Exported scene arrays and collision layer/mask setup
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 5 (pp. 113-136)"]
---
## Rules
- Spawn enemies from an exported array: `@export var enemy_scenes: Array[PackedScene]`, then `enemy_scenes.pick_random().instantiate()`.
- Link the spawner Timer via `@export var enemy_spawner: Timer` and drag it in the Inspector. WHY: renaming or moving the node does not break the reference.
- Position spawned enemies just off-screen: `Vector2(randf_range(50.0, screen_width - 50.0), -50.0)`.
- Name collision layers in Project Settings → Layer Names → 2D Physics before assigning them.
- Assign layers/masks by role, e.g. Layer 1 = Player, Layer 2 = Projectiles, Layer 3 = Enemies:
  - Laser: Layer 2, Mask 3.
  - Player: Layer 1.
  - Enemy: Layer 3, Mask 1 and 2.
- Let the engine filter collisions. WHY: masks are evaluated in C++ before GDScript is notified, saving CPU in bullet-hell scenarios.

## Checklist
- Is the spawner's enemy list an exported array rather than `preload` strings?
- Are all spawner dependencies exported and wired in the Inspector?
- Are collision layers named and assigned per role?
- Do projectiles ignore other projectiles via masks?

## Anti-patterns
- `preload("res://enemies/base_enemy.tscn")` inside spawn logic. WHY: magic-string paths break on refactor/Git merges, force designers to edit code, and scale poorly.
- Leaving everything on default Layer 1 / Mask 1. WHY: the engine computes every overlap and signals GDScript for collisions the script ignores.
- Hardcoding an array of specific preload statements for each enemy type. WHY: adding a type requires code changes.

> CHECK: The chapter references "Godot 4.5's @abstract annotation" — verify the exact Godot version that introduced `@abstract` before relying on it.

<!-- 6 Applying Event-Driven Patterns (pp. 137-168) -->
---
name: call-down-signal-up-event-out
topic: node communication rules
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Parent → Child: parent may hold a direct reference and call child functions (`hitbox.enable()`). WHY: parent owns its children, so the dependency direction is safe.
- Child → Parent: child must never call `get_parent().some_method()`. Emit a signal instead; the parent connects if it cares. WHY: a child that hardcodes a parent method can only ever be attached to that one parent type.
- Cross-system (unrelated branches of the tree): broadcast to a global Event Bus, never walk the tree with `get_node("../../...")`. WHY: long node paths break on every scene restructure.
- Never let a node push data to a receiver it looked up itself. Invert responsibility: sender broadcasts, receiver subscribes. WHY: sender stays testable in isolation (e.g. Player scene with no UI present).
- Decision table:
  | Situation | Mechanism |
  |---|---|
  | Parent controls child | direct call (Call Down) |
  | Child reports to parent | signal (Signal Up) |
  | Unrelated systems / UI / audio / achievements | Event Bus (Event Out) |
  | Persistent shared state | Observable Resource |
  | Engine lifecycle / OS events | `_notification()` |
## Checklist
- Can this scene be run standalone (F5 on the scene) without crashing? If not, it has an upward or sideways hard dependency.
- Does any script contain a `get_node()` path that starts with `..`? Replace with a signal.
- Does any script call a method on an object it did not create or receive as a parameter? Replace with a signal or bus event.
## Anti-patterns
- `get_node("../UI/HealthBar").update_value()` from gameplay code — breaks when the UI moves or is absent.
- `get_parent().add_score()` from an enemy — couples the enemy to one specific parent.
- Wiring every interaction through the Level script with rigid node paths — bloats the Level with references it should not know about.
- Using direct references "just for the prototype" and never refactoring — this is the stated primary cause of large-project failure.

---
name: connecting-signals-in-code
topic: dynamic signal connections
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Use the editor Node panel for signals between nodes that exist at edit time (static scenes).
- For runtime-spawned objects (enemies, projectiles, loot), connect in code right after `instantiate()`/`add_child()`: `enemy.died.connect(_on_enemy_died)`. WHY: there is nothing to click in the editor for objects that do not exist yet.
- Pass the function as a Callable reference — no parentheses: `.connect(_on_enemy_died)`, not `.connect(_on_enemy_died())`. WHY: parentheses would execute it immediately and pass the return value.
- Use `await` on a signal to sequence time-based logic in one readable block instead of splitting it across callbacks:
  ```gdscript
  animation_player.play("intro")
  await animation_player.animation_finished
  start_game()
  ```
  WHY: avoids a separate `_on_animation_finished()` handler for a single linear sequence.
- Disconnect or use one-shot connections for signals whose target may be freed, to avoid calls into freed objects.
## Checklist
- Every dynamically spawned node that the parent cares about has its signal connected at spawn time.
- No `.connect(func_name())` with parentheses anywhere.
- Long `await` chains are not used for logic that must survive node deletion.
## Anti-patterns
- Relying on editor connections for runtime-spawned nodes (impossible).
- Splitting one linear sequence into many callback functions when `await` would do.
- Forgetting to connect, then debugging "the score never increases" for an hour.

---
name: event-bus-pattern
topic: global event bus (publisher/subscriber)
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Implement the bus as a script `extends Node` registered as an Autoload named `EventBus`. WHY: `Node` is the minimum type that can live in the tree and hold signals; heavier bases waste memory.
- The bus contains only signal definitions — no logic, no state. WHY: Single Responsibility; a stateless bus is a pure router.
- Type every signal parameter (`signal score_changed(new_amount: int)`). WHY: a wrong-type emit becomes an immediate engine error instead of a silent bug.
- Publishers emit and immediately continue (often `queue_free()` right after). They never check whether a listener exists. WHY: this is what makes senders independent of receivers.
- Subscribers connect in `_ready()`: `EventBus.score_changed.connect(update_score)`.
- Suppress the "defined but never used" warning with `@warning_ignore("unused_signal")` on bus signals. WHY: the bus only defines signals; emitters live elsewhere.
- Keep the bus stateless. If you need authoritative values, put them in a separate stateful Resource/Autoload and have the bus only carry notifications. WHY: a stateless bus has no history, so late-loading listeners miss past events (race condition).
## Checklist
- Bus script has zero `var` declarations (or only constants).
- Every signal has typed parameters.
- Every subscriber connects in `_ready()` and does not search the tree for the publisher.
- No listener assumes it will receive events that fired before it loaded.
## Anti-patterns
- Putting game state (`current_score`, `current_lives`) directly in the bus and calling it "the bus" — that is a stateful singleton, a different thing.
- Emitting from inside a signal handler (see cascading events).
- Using the bus for sequential, order-dependent logic.

---
name: event-bus-tradeoffs
topic: event-driven architecture risks
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- One-Hop Rule: an event should trigger a final reaction (update UI, play sound, change one state), never another event. WHY: A→B→C chains are unreadable and can loop infinitely.
- If several steps must happen in strict order, have one Manager listen to the initial event and then call the subsequent steps directly. WHY: explicit call order beats implicit broadcast order.
- Never use the bus for sequential, dependent logic (e.g. ScoreManager must finish before LevelManager checks the win threshold). Use Call Down or direct delegation. WHY: broadcast order to listeners is not guaranteed → race conditions.
- Reserve the bus for parallel, independent reactions (UI update + explosion sound at the same time).
- For critical global events, require a source/reason parameter: `signal level_completed(source: Node, reason: String)`. WHY: the bus decouples so thoroughly that you otherwise cannot trace who fired it.
- Log `source` and `reason` on critical events so a rogue emitter can be identified instantly.
## Checklist
- No signal handler emits another signal.
- No two listeners depend on each other's completion order.
- Every game-state-changing global event carries a sender or reason argument.
- You can name, for each bus event, exactly which scripts are allowed to emit it.
## Anti-patterns
- Cascading events (spaghetti logic) — debugging becomes near-impossible and infinite loops crash the game.
- Assuming listeners run in a particular order.
- Any script being able to emit `level_completed` with no identification — a stray bullet can end the game and you cannot find it.

---
name: namespacing-and-event-objects
topic: organizing events at scale
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Use namespacing when you have too many signals and need to group channels by domain (Player, World, Audio, UI).
- Namespacing in GDScript: declare inner classes holding signals, then instantiate them as variables on the bus:
  ```gdscript
  class PlayerEvents:
      signal health_changed(new_health: int)
      signal died
  var Player = PlayerEvents.new()
  ```
  Emit as `EventBus.Player.health_changed.emit(health)`.
- The `.new()` instantiation is mandatory — an inner class is only a blueprint and cannot emit signals until instantiated.
- Use Event Objects when one signal carries complex or frequently changing data.
- Event Object: a lightweight class (`class_name EnemyDeathEvent extends RefCounted`) with public fields; emit one object instead of N arguments.
  ```gdscript
  signal enemy_destroyed(event: EnemyDeathEvent)
  ```
  WHY: adding a field later does not change the signal signature, so no subscriber breaks.
- Listeners take one typed parameter and read only the fields they need (`event.points`), ignoring the rest.
- Professional projects use both together: an Event Object (payload) over a namespaced signal (channel).
- Decision table:
  | Problem | Pattern |
  |---|---|
  | Too many signals, naming collisions | Namespacing |
  | One signal, growing/changing payload | Event Object |
## Checklist
- Signal names are unique within their namespace class.
- Any signal with 3+ parameters is a candidate for an Event Object.
- Adding a new field to an event requires zero changes to subscriber signatures.
## Anti-patterns
- 50 flat signals on one bus with no grouping.
- Changing a signal signature (`enemy_destroyed(points, pos)`) and breaking every listener — use an Event Object instead.
- Confusing the two patterns: namespacing organizes channels, Event Objects organize payloads.

---
name: notifications-vs-signals
topic: engine notifications
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Notifications are engine-sent memos; signals are your own gameplay events. Use the right one.
- `_ready()`, `_process()`, `_enter_tree()` are helper wrappers over the notification system. Override `_notification(what: int)` only for lifecycle events with no helper.
- Use a `match` on `what` with the human-readable constants, never raw integers:
  ```gdscript
  func _notification(what: int) -> void:
      match what:
          NOTIFICATION_WM_FOCUS_OUT:
              get_tree().paused = true
          NOTIFICATION_WM_CLOSE_REQUEST:
              save_game()
  ```
- `NOTIFICATION_WM_FOCUS_OUT` = window lost focus (Alt-Tab / other monitor) → good place for auto-pause.
- `NOTIFICATION_WM_CLOSE_REQUEST` = user clicked the window X → last chance to save before the engine shuts down.
- Decision table:
  | Need | Use |
  |---|---|
  | Gameplay logic, UI updates, quest triggers | Signals |
  | Memory management, OS interaction, object cleanup | Notifications |
  | Custom name and arguments | Signals |
  | Only Godot's integer constants | Notifications |
- Performance: notifications are C++-level calls and faster than signals; signals carry parsing overhead.
## Checklist
- `_notification()` uses `match` with named constants, not magic numbers.
- Auto-pause and save-on-quit are wired to the WM notifications.
- No custom gameplay event is implemented as a notification.
## Anti-patterns
- Comparing `what` against literal integers like `1004`.
- Using notifications for gameplay events you defined yourself.
- Ignoring `NOTIFICATION_WM_CLOSE_REQUEST` and losing player progress.

---
name: observable-resources
topic: reactive persistent state
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Use Observable Resources for state (nouns): health, ammo, XP, master volume, inventory. Use the Event Bus for actions (verbs): jumped, died, fired.
- Implement as a custom `Resource` with `class_name`, saved as a `.tres` file, shared by Player, upgrade menu, and HUD. WHY: all consumers read the same data object.
- Emit a signal from the property setter so any write automatically broadcasts:
  ```gdscript
  @export var max_shield: int = 50:
      set(value):
          max_shield = value
          shield_capacity_changed.emit(max_shield)
  ```
- Gameplay code then only writes `stats.max_shield = 100`; the resource handles notifying the UI. WHY: frontend and backend can never drift out of sync.
- Never poll state every frame (`_process` reading player health). Subscribe to the resource signal instead. WHY: polling is costly and redundant.
- Pulling state out of node scripts into a resource decouples game state from the Scene Tree — you can delete the player, swap levels, or rebuild the UI and the data survives.
## Checklist
- Every mutable shared value has a setter that emits.
- No `_process()` loop reads another system's state just to mirror it in the UI.
- The resource file is referenced (not duplicated) by every consumer.
## Anti-patterns
- Duplicating state across Player, HUD, and a manager, then manually syncing.
- Polling instead of subscribing.
- Putting persistent state in the Event Bus (see event-bus-pattern).

---
name: push-pull-ui-initialization
topic: avoiding startup race conditions
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- A race condition occurs when a signal fires before the listener connects. Godot runs `_ready()` bottom-to-top, so you cannot guarantee who wins.
- Symptom: UI randomly shows 0 lives because the Player broadcast before the HUD connected.
- Fix with Push/Pull in the listener's `_ready()`:
  1. Push — subscribe to future updates: `EventBus.score_changed.connect(update_score)`.
  2. Pull — read the current authoritative value from the stateful source (e.g. `PlayerStats` / a stateful Autoload).
  3. Initialize the UI with that pulled value immediately.
- Keep the single source of truth in a stateful Resource or Autoload that loads before any level (Autoloads load first).
- Keep the Event Bus stateless; it carries no history, so it can never answer "what is the current value?".
## Checklist
- Every UI element that mirrors state both subscribes AND pulls an initial value in `_ready()`.
- The authoritative state holder is an Autoload or a shared Resource, not a node inside the level.
- Test by loading the UI late (or disabling it) and confirming correct values on frame one.
## Anti-patterns
- Relying purely on signals for initial UI values — the message is lost if the listener was not ready.
- Storing authoritative values in the Event Bus and calling it "state".
- Assuming a fixed `_ready()` order between siblings.

---
name: powerup-inheritance-and-static-typing
topic: modular collectible design
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Build a `BasePowerup` scene: `Area2D` root + `Sprite2D` + `CollisionShape2D` + `VisibleOnScreenNotifier2D`; Collision Layer = 5 (Powerups), Mask = 1 (Player).
- Base script holds shared behavior (movement, screen-exit cleanup, collision) and a virtual `apply_powerup(_player) -> void: pass` that children override. WHY: children inherit movement/collision and only define their effect.
- Use "New Inherited Scene" and "Extend Script…" so children inherit the base scene and script without duplicating logic.
- Free the power-up on pickup and on `screen_exited` via `queue_free()`.
- Prefer static typing over duck typing for the pickup check:
  ```gdscript
  if body is PlayerShip:
      apply_powerup(body as PlayerShip)
  func apply_powerup(player: PlayerShip) -> void:
  ```
  WHY: `is` checks the real class, not a misspellable group string; typed parameters give editor errors before runtime.
- `has_method("activate_shield")` (duck typing) is acceptable only when many unrelated object types must interact with the same system. WHY: it relies on magic strings — a typo fails silently at runtime.
- Decision table:
  | Priority | Approach |
  |---|---|
  | Safety, performance, autocomplete, structured codebase | Static typing (`: PlayerShip`) |
  | Extreme flexibility across unrelated types | Duck typing (`has_method`) |
- Accept the trade-off: static typing couples the power-up to one class, so `SupportDrone`/`PlayerTwoRover` will bounce off it even if they have the same method.
## Checklist
- Base scene defines collision layer/mask once; children only swap the texture.
- Child scripts contain only the overridden `apply_powerup`.
- Pickup check uses `is` + typed parameter, not `is_in_group("Player")`.
- Every power-up frees itself on pickup and on leaving the screen.
## Anti-patterns
- Rewriting movement/collision code in every power-up instead of inheriting.
- `is_in_group("Player")` with a typo'd group name — silently never triggers.
- `player.activate_shield()` on an untyped parameter — crashes with "Method not found" if the wrong body touches it.

---
name: decoupled-spawner-and-hud
topic: data-driven spawning and procedural UI
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 6 (pp. 137-168)"]
---
## Rules
- Spawn with `Timer` nodes, not manual countdowns in `_process()`. Connect `timeout` in `_ready()` and call `start()`.
- Expose spawn data via `@export`: `@export var powerup_scenes: Array[PackedScene]`, `@export var enemy_scenes: Array[PackedScene]`.
- Spawn pattern: `pick_random()` → `instantiate()` → `add_child()` → set `global_position` to a random X within `randf_range(50.0, screen_width - 50.0)` and Y = `-50.0` (just above the screen).
- The level script must not know what a power-up is. WHY: new power-up types are added purely through the Inspector, with zero code changes.
- HUD structure: `CanvasLayer` → `Control` (Full Rect) → `MarginContainer`/`HBoxContainer` groups for score, lives, weapon.
- Export UI assets instead of hardcoding paths: `@export var life_texture: Texture2D`, `@export var digit_textures: Array[Texture2D]` (indices 0–9). WHY: artists swap assets in the Inspector without touching code.
- Procedural digit rendering: clear children with `queue_free()`, convert score to `String`, loop characters, `int(character)` as index into `digit_textures`, spawn a `TextureRect` per digit.
- Procedurally spawned `TextureRect`s must be configured in code: `expand_mode = EXPAND_KEEP_SIZE`, `stretch_mode = STRETCH_KEEP_ASPECT_CENTERED`, `custom_minimum_size = Vector2(32, 32)`. WHY: editor sizing does not apply to code-created nodes.
- Use sentinel values for special cases: `ammo < 0` means infinite ammo, so the label omits the counter. WHY: ammo can never be negative naturally.
- Alternative for complex UI: make a small `life_icon.tscn` with a pre-configured `TextureRect` and `instantiate()` it in the loop. WHY: keeps UI configuration in the editor, not in scripts.
## Checklist
- Spawners are `Timer` nodes with `timeout` connected in `_ready()`.
- All spawnable scenes are `@export`ed arrays, not hardcoded `preload` paths.
- HUD containers are cleared with `queue_free()` before rebuilding.
- Code-created `TextureRect`s set size and stretch mode explicitly.
- Score/lives update only via Event Bus signals, never by searching for the Player.
## Anti-patterns
- Hardcoding power-up types in the level script.
- Manual countdown logic in `_process()` instead of a Timer.
- Spawning `TextureRect`s without setting `custom_minimum_size`/`stretch_mode` — icons warp.
- Hardcoding texture file paths in the HUD script instead of exporting them.

<!-- 7 Implementing State and Strategy Patterns (pp. 169-198) -->
---
name: state-pattern-fsm-godot
topic: State Pattern / Finite State Machine in Godot 4
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 7 (pp. 169-198)"]
---
## Rules
- Build the FSM from Nodes: a `StateMachine` parent node with one child `State` node per behavior. WHY: the Scene Tree visually documents the entity's behaviors, states hook into `_process`/`_physics_process` natively, and the Remote Scene Tree shows the active state at runtime.
- Create a base `state.gd` (`class_name State extends Node`) with virtual `enter()`, `exit()`, `update(delta)`, `physics_update(delta)` and a `transition_requested(state, new_state_name)` signal. WHY: the empty virtuals form a strict contract so the manager can call any of them on any state without crashing.
- Give each state an exported `state_id: String` and key the manager's `states` dictionary by `state_id` (falling back to node name, lowercased). WHY: transitions then survive node renames/reorganization in the Scene Tree.
- In `StateMachine._ready()`, iterate `get_children()`, skip non-`State` children with a guard clause, register each in `states`, and connect each child's `transition_requested` to the manager's handler. WHY: states self-register; no manual list to maintain.
- Expose `@export var initial_state: State`, call `initial_state.enter()` and set `current_state` in `_ready()`. WHY: the starting behavior is configured in the Inspector, not hardcoded.
- Delegate engine callbacks: `_process` calls `current_state.update(delta)`, `_physics_process` calls `current_state.physics_update(delta)`, both guarded by `if not current_state: return`. WHY: only the active state runs logic, saving CPU and preventing conflicting behaviors.
- Transition handler order: (1) ignore if `state != current_state` (stale/delayed signal), (2) look up the new state, (3) `push_warning` and return if missing, (4) `current_state.exit()`, (5) `new_state.enter()`, (6) assign `current_state = new_state`. WHY: prevents ghost transitions from old states and guarantees cleanup before setup.
- States emit `transition_requested` instead of calling `get_parent().change_state()`. WHY: the state stays decoupled from the manager's existence and internals.
- Each state script handles only its own behavior plus its own transition conditions; it must not contain other states' logic. WHY: single responsibility makes bugs locatable to one file.
- Put decision guard clauses at the top of `physics_update` (target still valid? in range?) and `return` early. WHY: skips movement math when a transition is imminent.
- For ship-style movement: compute `direction = (target.global_position - actor.global_position).normalized()`, rotate with `lerp_angle(actor.rotation, direction.angle() + PI/2, rotation_speed * delta)`, then `actor.velocity = Vector2.UP.rotated(actor.rotation) * speed; actor.move_and_slide()`. WHY: `+PI/2` compensates for sprites facing up while Godot's 0 rad points right; `lerp_angle` gives weighty turning; `move_and_slide` handles collisions.
- Give states an `@export var actor: CharacterBody2D` pointing at the controlled body. WHY: a state Node has no position/velocity of its own.
- Find the player via `get_tree().get_first_node_in_group("Player")` in `enter()`. WHY: avoids hardcoded node paths.
- Scene layout: `CharacterBody2D` (root) → `Sprite2D`, `CollisionShape2D`, `Node` named `StateMachine` → one child Node per state (e.g. Patrol, Chase, Attack), each with a script extending `state.gd`.

## Checklist
- [ ] Base `State` class with virtuals and `transition_requested` signal exists.
- [ ] `StateMachine` auto-registers children and connects their signals.
- [ ] `initial_state` assigned in the Inspector.
- [ ] Every state has a unique `state_id`.
- [ ] Transition handler has both guard clauses (stale state, missing target state).
- [ ] Each state file contains only its own behavior and transition rules.
- [ ] `actor` export wired to the root body in every state.

## Anti-patterns
- One `_physics_process` with nested `if hp > 50 and distance > 300 ... elif ...` chains — grows into hundreds of fragile lines.
- Calling `get_parent().change_state()` directly from a state — couples state to manager internals.
- Keying states by raw node name only — breaks on rename.
- Letting a deactivated state's delayed signal trigger a transition — causes ghost state changes.
- Attaching a full state machine to thousands of trivial objects (e.g. debris particles) — unnecessary memory/CPU cost.

---
name: state-vs-strategy-choice
topic: Choosing between State and Strategy patterns
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 7 (pp. 169-198)"]
---
## Rules
- Use the State Pattern when the object passes through distinct, mutually exclusive phases and transitions itself based on internal rules (Idle/Patrol/Chase/Attack, boss phases). WHY: states own their transition logic and only one is active at a time.
- Use the Strategy Pattern when the object performs one consistent task but the algorithm should be swappable (weapon types, status effects, interactables). WHY: strategies rarely self-transition; a parent calls them.
- Refactor when you see any of these code smells: a Boolean cluster (`is_moving`, `is_shooting`, `is_stunned`) checked in `_process`; an enum + `match` block over ~50 lines; "shotgun surgery" where one feature change forces edits in many files. WHY: each added flag doubles the complexity of every conditional.
- Keep simple binary toggles as plain Booleans (e.g. `is_open` on a door). WHY: a two-state object does not justify a state machine.
- Reserve these patterns for complex entities: players, bosses, advanced AI. WHY: nodes/resources have a small but nonzero memory cost.
- Organize folders deliberately when splitting into many small files. WHY: dozens of tiny strategy/state scripts can slow you down if unfindable.

## Checklist
- [ ] Identify whether the problem is "what is it doing now" (State) or "how does it do X" (Strategy).
- [ ] Confirm the feature is complex enough to justify the pattern.
- [ ] Confirm the entity count is low enough that per-entity nodes are affordable.
- [ ] Plan folder structure before creating many small files.

## Anti-patterns
- Over-engineering: `open_state.gd`/`closed_state.gd` for a door that only opens and closes.
- Applying a state machine to thousands of trivial objects.
- Using Strategy for mutually exclusive phases that need their own transition rules.
- Refactoring prematurely before any code smell appears.

---
name: strategy-pattern-custom-resources
topic: Strategy Pattern via Custom Resources in Godot 4
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 7 (pp. 169-198)"]
---
## Rules
- Implement strategies as scripts extending `Resource` (`class_name WeaponStrategy extends Resource`), saved as `.tres` files. WHY: resources are pure data objects outside the Scene Tree — no `_process`, negligible memory, hot-swappable.
- Define the base strategy with shared exported fields (`fire_rate`, `energy_cost`) and a virtual method whose body calls `push_error("Abstract method ... must be overridden!")`. WHY: the base acts as an interface/contract; the error catches a designer dragging the blueprint into a slot.
- Give the virtual method a fixed signature that includes everything the strategy needs from the world, e.g. `fire(spawn_location: Vector2, direction: Vector2, parent_container: Node) -> void`. WHY: all subclasses stay interchangeable.
- Pass a `parent_container` (e.g. a dedicated `Projectiles` Node2D) into `fire()` and call `parent_container.add_child(projectile)`. WHY: (a) resources have no `add_child`/`get_tree()` access — resource isolation; (b) projectiles parented to the ship inherit its transform and would slide with it — relative movement problem.
- Guard the container: `if parent_container: ... else: push_warning(...)`. WHY: surfaces misconfiguration instead of silently dropping projectiles.
- Set projectile transform as `global_position = spawn_location` and `rotation = direction.angle() + PI/2`. WHY: `+PI/2` aligns an up-facing sprite with the travel direction.
- For spread shots, iterate an angle array (e.g. `[-spread_angle, 0, spread_angle]` with `spread_angle = 15.0`), rotate the base direction with `direction.rotated(deg_to_rad(angle))`, and instantiate one projectile per angle. WHY: keeps all vector math inside the strategy file.
- In the consumer (e.g. `Blaster`), expose `@export var basic_weapon: WeaponStrategy` and `@export var upgraded_weapon: WeaponStrategy` and hold `var current_strategy: WeaponStrategy`. WHY: strategies are injected via the Inspector, no code changes to add weapons.
- `fire()` should: return if the cooldown timer is running, error if no strategy, delegate to `current_strategy.fire(muzzle.global_position, Vector2.UP.rotated(global_rotation), get_tree().current_scene)`, play sound, then `cooldown_timer.start(current_strategy.fire_rate)`. WHY: pure delegation; per-weapon timing comes from the resource.
- Swap weapons by overwriting `current_strategy` with another resource. WHY: no Boolean flags, no branching; the next shot uses the new algorithm.
- To add a weapon: create a new strategy script + `.tres`, assign it to an export slot. WHY: the player/blaster scripts stay closed to modification (Open-Closed Principle).

## Checklist
- [ ] Base strategy extends `Resource` with shared exports and an error-throwing virtual.
- [ ] Every concrete strategy overrides the virtual with the exact same signature.
- [ ] `parent_container` is passed and validated in every `fire()`.
- [ ] Projectiles are added to a neutral container, not the shooter.
- [ ] Consumer holds `current_strategy` and delegates; no bullet math in the consumer.
- [ ] Cooldown uses `current_strategy.fire_rate`.
- [ ] `.tres` files created and assigned in the Inspector.

## Anti-patterns
- Hardcoding weapon behavior in `player_ship.gd` with arrays of packed scenes and strings.
- Calling `add_child(laser)` on the player/blaster node — projectiles inherit the ship's transform and drift with it.
- Calling `get_tree().root.add_child(...)` from inside a Resource — resources lack tree access; pass the container instead.
- Toggling `is_using_spread_shot = true` style flags instead of swapping the strategy resource.
- Leaving the base strategy's `fire()` empty without `push_error` — silent failures.

---
name: refactoring-conditionals-to-patterns
topic: Refactoring conditional logic into State/Strategy patterns
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 7 (pp. 169-198)"]
---
## Rules
- Refactor an enum + `match` inside `_physics_process` into a Node-based state machine. WHY: adding a case (e.g. `EMP_STUNNED`) otherwise means editing the enum, the match, and adding new variables to the player script.
- Refactor Boolean clusters into a State Pattern so the entity is physically in exactly one state. WHY: eliminates invalid flag combinations and the checks that guard against them.
- Refactor "shotgun surgery" (one feature change touching many files) into a Strategy Pattern. WHY: the algorithm is encapsulated in one standalone resource.
- Refactor any `if/else` or `match` block exceeding ~50 lines. WHY: it is a manually written, badly structured state machine.
- Keep plain Booleans for simple binary toggles (open/closed door). WHY: patterns are not silver bullets.
- After refactoring, the original script (e.g. `player_ship.gd`) should be closed to modification; new behavior is added as new state scripts or strategy resources. WHY: enforces the Open-Closed Principle and prevents regressions.
- Expect debugging to become deterministic: a bug in a behavior is guaranteed to live in that behavior's file. WHY: isolation removes the search space.

## Checklist
- [ ] Scan for enum+match blocks, Boolean clusters, and shotgun-surgery edits.
- [ ] Classify each: phases → State; algorithm variants → Strategy; binary toggle → leave as Boolean.
- [ ] Extract one file per behavior/algorithm.
- [ ] Verify the original script no longer contains the extracted logic.
- [ ] Verify adding a new behavior requires only a new file + Inspector assignment.

## Anti-patterns
- Refactoring everything at once instead of only the identified code smells.
- Building a state machine for a two-state object.
- Leaving residual conditional branches in the original script after extraction.
- Adding new features to a bloated script "just this once" instead of extending via a new state/strategy.

> CHECK: The OCR text for `StateMachine._physics_process` reads `if not current_state: return current_state.physics_update(delta)` on one line — verify whether the `return` and the call are on separate lines in the source.

<!-- 8 Creating Component-Based Systems (pp. 199-222) -->
---
name: inheritance-limits-and-composition
topic: Entity-Component architecture
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 8 (pp. 199-222)"]
---
## Rules
- Treat an entity as an empty container node (`Node2D`/`CharacterBody2D`); attach behavior as child component nodes instead of extending a base class.
- Prefer composition when: entities are multifaceted and share overlapping behaviors, a mechanic is used across many object types, or environmental objects are highly interactive.
- Keep inheritance when: the object is simple and single-purpose, or it is a one-off that will never be reused.
- Apply YAGNI: do not build a generic component for a feature only one object needs today. Write the logic inline first.
- Apply DRY as the trigger to refactor: the moment you copy-paste the same logic into a second script, extract it into a component.
- Expect these trade-offs before committing: denser scene tree, more complex data passing, risk of building generic components that never get reused.
- Do not build a "god class" with boolean flags (`is_moving`, `can_shoot`) to fake feature mixing — that is the failure mode composition replaces.
## Checklist
- [ ] List the behaviors the entity needs; each becomes one component or is reused from the library.
- [ ] Confirm at least two entity types will share each new component before extracting it.
- [ ] Verify no component script references a sibling component directly.
- [ ] Verify the entity's root script contains only wiring and lifecycle logic.
## Anti-patterns
- Deep inheritance chains (`Boss extends Enemy extends Character`) — a change in a base class silently breaks unrelated children.
- Duplicating shooting/healing/movement code into parallel branches because a single parent cannot be shared.
- Building a fully generic component framework up front for features that may never ship.
> CHECK: OCR shows "idx_..." markers scattered in the text; they are artifacts, not content.

---
name: pure-component-design
topic: Component design
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 8 (pp. 199-222)"]
---
## Rules
- Make a component self-contained: one responsibility, zero external dependencies, no knowledge of its parent entity.
- Extend `Node` (not `Node2D`/`Area2D`) for pure logic/data components so they have no physical presence in the world.
- Declare `class_name` so the component appears in the Add Node search and can be added like a built-in node.
- Expose tunables with `@export` so designers edit values in the Inspector without touching code.
- Emit local signals for state changes (`died`, `health_changed(new_health, max_health)`) instead of calling into the parent.
- Never call `queue_free()`, spawn particles, or drop loot from inside a component — that belongs to the parent controller.
- Do not hardcode `EventBus.emit()` inside a reusable component: it couples the component to one project's autoload and floods global channels with every minor object's data.
- To reach global systems, use the parent as a relay: component emits local signal → parent connects → parent emits to the EventBus.
- Separate data from physics: a `HealthComponent` tracks numbers; a `HitboxComponent` (extends `Area2D`) handles collisions.
- Make the hitbox a passive alarm: `damage(amount)` only emits `hit_received(amount)`; it does not look up or call the health pool.
- Let the projectile be the active agent: it detects the overlap and calls `damage()` on the hitbox.
- Allow multiple hitboxes to feed one health pool (e.g. armored hull halves damage, weak spot doubles it).
## Checklist
- [ ] Component extends `Node` unless it genuinely needs physics/rendering.
- [ ] `class_name` declared and component findable in Add Node.
- [ ] No `get_parent()`, no sibling lookups, no autoload calls inside the component.
- [ ] All outputs are signals; all inputs are exported vars or public methods.
- [ ] Parent connects the component's signals in `_ready()`.
## Anti-patterns
- Hitbox that inspects what hit it and computes damage — forces it to know every weapon in the game.
- Exported direct reference from hitbox to health component — silently fails if unassigned in the Inspector.
- Component that deletes its own owner or plays death VFX.

---
name: controller-wiring-and-signal-relay
topic: Entity composition and communication
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 8 (pp. 199-222)"]
---
## Rules
- The entity root script acts as a motherboard: it holds components and wires their signals in `_ready()`; it contains almost no logic of its own.
- Route conditional damage in the controller, not the components: e.g. `if shield.current_health > 0: shield.take_damage(amount) else: health.take_damage(amount)`.
- Wire reaction components directly to trigger signals: `shield.shield_broken.connect(stun.trigger_stun)` and `.connect(flash.trigger_flash)`.
- Keep components "dumb": the hitbox must not know a shield exists; the shield must not know how to stun.
- Use Groups for target identification: add the hitbox to a group (e.g. `"enemy"`) and check `area.is_in_group(...)` in the projectile.
- Use duck typing for safe execution: check `area.has_method("damage")` before calling it, so the projectile never needs the target's class.
- Replace magic strings with constants in a global autoload (e.g. `GameGlobals.GROUP_ENEMY = "enemy"`) so autocomplete catches typos.
- Apply the Event Relay Pattern: low-level component signal → middleman (spawner/parent) → broad high-level signal for the level.
- Example relay chain: `HitboxComponent` detects hit → `HealthComponent` emits `died` → entity script plays explosion and frees the node → `EnemySpawner` emits `enemy_defeated(100)` → `LevelManager` calls `GameManager.add_score(score)`.
- Never let a spawned enemy call `GameManager.add_score()` directly — it breaks if the enemy is reused in a level without that manager.
## Checklist
- [ ] Every cross-component interaction goes through the controller or a signal relay, never a direct node path.
- [ ] Projectile scripts contain no reference to specific enemy classes.
- [ ] Group names and method names used in duck typing are constants, not literals.
- [ ] Each layer only knows its direct neighbors: component → parent → spawner → level manager.
## Anti-patterns
- Enemy script hard-referencing `GameManager` — crashes when dropped into another level.
- Projectile checking `if area is AlienDrone` — must be edited for every new enemy type.
- Controller that computes damage math itself instead of delegating to components.

---
name: spawner-and-instantiation
topic: Dynamic entity spawning
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 8 (pp. 199-222)"]
---
## Rules
- Build spawners as self-contained nodes (e.g. `Marker2D` with `class_name EnemySpawner`) that create their own `Timer` in `_ready()` from an `@export var spawn_interval: float` — no manual Timer node needed.
- Export `enemy_scene: PackedScene` and instantiate with `enemy_scene.instantiate()`.
- After instantiating, look up the child component with `get_node_or_null("HealthComponent")` and connect its `died` signal before adding it to the tree.
- Never `add_child()` the enemy directly to the spawner — the enemy would be dragged along when the spawner moves.
- Do not rely on `get_parent().add_child()` alone — it is brittle in deeply nested trees.
- Export an optional `spawn_container: Node` so designers choose where spawned entities live; fall back to `get_parent()` when it is unset.
- Set `new_enemy.global_position = global_position` after adding to the tree.
- Emit a broad relay signal (`enemy_defeated(score_value)`) from the spawner instead of letting enemies report score themselves.
## Checklist
- [ ] Spawner creates and starts its own timer.
- [ ] Health component lookup is null-safe.
- [ ] `spawn_container` exported with a safe fallback.
- [ ] Spawner emits its own high-level signal; it never calls the score manager directly.
## Anti-patterns
- Spawning enemies as direct children of the spawner node.
- Global manager polling every frame to check whether enemies died.
- Enemies holding a reference to the spawner that created them.

---
name: refactoring-to-components
topic: Refactoring strategy
confidence: opinion
sources: ["Godot 4 Best Practices, Robert Henning, ch. 8 (pp. 199-222)"]
---
## Rules
- Start with a monolithic script; refactor to components only when a second or third object needs the same logic.
- Extract in this order: health/data first (most universal), then physics/damage detection, then movement, then offense.
- When extracting, move the logic out completely — leave no duplicate copy behind in the original script.
- Convert direct cross-script calls into signals during extraction; if a call cannot become a signal, the boundary is wrong.
- Keep the refactored root script to wiring plus lifecycle callbacks (`_ready`, `on_death`).
- Accept the trade-off: composition buys reusability and isolated debugging at the cost of a denser scene tree and more complex data flow.
## Checklist
- [ ] The same logic exists in exactly one file after refactoring.
- [ ] Original monolith script shrank to wiring only.
- [ ] New component is attached to at least two entity types, or the extraction was premature.
- [ ] Debugging a behavior means opening one component file, not scrolling a 500-line script.
## Anti-patterns
- Refactoring everything to components before the game design stabilizes.
- Extracting a component that is used by exactly one object and never reused.
- Leaving half the logic in the monolith and half in the component.

<!-- 9 Using Factory and Builder Patterns (pp. 223-242) -->
---
name: factory-pattern-spawner-node
topic: Factory Pattern for spawning nodes in Godot 4
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Implement a Factory as a reusable `Node2D` component (commonly called a "Spawner") with `class_name Spawner`. WHY: makes it searchable in the Add Node menu and reusable across scenes.
- Expose the product via `@export var product_scene: PackedScene` and the destination via `@export var parent_container: Node`. WHY: keeps the Factory agnostic — it doesn't hardcode what it builds or where it goes.
- Declare a `signal product_created(product: Node)` and emit it after the product is added to the tree. WHY: lets other components react to new objects without the Factory knowing about them.
- `spawn()` must validate `product_scene` first: `if not product_scene: push_error(...); return null`. WHY: fails loudly in the editor instead of crashing at runtime.
- Parent resolution order: use `parent_container` if set, otherwise fall back to `get_tree().current_scene`. WHY: sensible default without forcing configuration.
- Position the product only if it is a `Node2D`: copy `global_position` and `global_rotation` from the Spawner. WHY: the Spawner's placement in the level defines the spawn point.
- Return the product from `spawn()` so callers can post-configure it (velocity, stats, etc.). WHY: separates creation (Factory) from gameplay tuning (manager).
- Use `container.call_deferred("add_child", product)` only when spawning from inside a physics callback (e.g. `_on_area_entered`). WHY: Godot errors if you mutate the tree mid-physics-step; normal `add_child()` is fine in 99% of cases.
- Callers should null-check the return value before using it. WHY: `spawn()` returns `null` on missing blueprint.

## Checklist
- [ ] `product_scene` and `parent_container` exported, not hardcoded.
- [ ] `push_error` guard on missing scene.
- [ ] `product_created` emitted after `add_child`.
- [ ] Position/rotation copied only for `Node2D` products.
- [ ] `spawn()` returns the product node.
- [ ] Deferred add only in physics callbacks.

## Anti-patterns
- Scattering `instantiate()` + `add_child()` + positioning across player/enemy/level scripts. WHY: changing the container or setup requires editing every call site.
- Building a dedicated Factory for a one-off object (e.g. a single Final Boss). WHY: over-engineering; adds files and tree nodes for no reuse.
- Hardcoding the product scene inside the Factory script. WHY: kills the Inspector-driven flexibility that makes the pattern worth it.

---
name: factory-vs-direct-spawning
topic: Deciding when to introduce a Factory
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Default to direct script spawning while prototyping. WHY: patterns add indirection; don't pay for it before you need it.
- Refactor to a Factory the moment the same spawning logic is copied into a second or third script. WHY: duplicated creation code is the concrete signal that the pattern is justified.
- Use a Factory when any of these hold: multi-step initialization, data injection, randomized properties, many scripts spawn the same object, the product varies by data/random/exported arrays, or the object must be routed to a separate container.
- Keep direct spawning when: setup is one or two lines, only one script ever spawns it, the scene is always identical, or the object is added as a child of its creator.
- Let the pain of duplicated code dictate when to introduce the pattern, not architectural ambition.

## Checklist
- [ ] Count how many scripts contain the same instantiation block.
- [ ] Check whether the product varies at runtime (data/random).
- [ ] Check whether the product needs a dedicated container.
- [ ] If all answers are "no / one script", keep it inline.

## Anti-patterns
- Adding a Factory for every object "for consistency". WHY: clutters the Scene Tree and file list, hurts readability.
- Introducing a Factory before any duplication exists. WHY: speculative abstraction.

---
name: builder-pattern-method-chaining
topic: Builder Pattern for complex multi-step object construction
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Extend `RefCounted` for Builders, not `Node`. WHY: the Builder is a transient in-memory helper, not part of the Scene Tree; Godot frees it automatically when unreferenced.
- Each configuration method (`add_title`, `add_button`, `set_size`, ...) must end with `return self`. WHY: returning `self` is what enables method chaining.
- Provide a terminal `build()` method that returns the finished product (e.g. the root `Control`), not `self`. WHY: marks the end of the chain and hands back a node any script can add to the tree.
- Use `Callable` parameters to wire signals at construction time (e.g. `btn.pressed.connect(callable)`). WHY: lets the caller inject behavior without the Builder knowing about game logic.
- In GDScript, use `\` as the line-continuation character to write a readable multi-line chain.
- Add `@tool` at the top of the script and drive generation from an `@export` setter to preview Builder output live in the editor. WHY: gives visual feedback without pressing Play.
- In the `@tool` preview setter, free existing children first (`for child in get_children(): child.queue_free()`). WHY: prevents stacking duplicate previews on each toggle.
- Reserve the Builder for objects needing many optional parts or nested children (procedural UI, dungeons, dialogue trees).

## Checklist
- [ ] Builder extends `RefCounted`.
- [ ] Every step method returns `self`.
- [ ] `build()` returns the product node.
- [ ] Signal wiring uses `Callable` parameters.
- [ ] `@tool` preview clears old children before rebuilding.

## Anti-patterns
- Using a Builder for an object with one or two simple properties. WHY: a Factory or direct instantiation is shorter and clearer.
- Passing ten positional arguments into a single `_init()`/`spawn()` ("constructor telescoping"). WHY: unreadable call sites and easy argument-order bugs.
- Making the Builder a `Node` in the Scene Tree. WHY: unnecessary tree pollution for a transient helper.

---
name: configuration-object-pattern
topic: Configuration Object as a middle ground between Factory and Builder
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- When a Factory needs many optional parameters, define a lightweight config class (`class_name ProjectileConfig extends RefCounted`) holding all fields with sensible defaults.
- Callers create the config, override only the fields they care about, and pass the single object to the Factory: `ProjectileFactory.spawn(config)`.
- Keep the Factory's public API to a single `spawn(config)` function. WHY: avoids argument explosion while retaining per-call customization.
- Use the Configuration Object for highly variable objects (projectiles, particle effects); reserve the true Builder for multi-step structural assembly.
- A `Custom Resource` is an acceptable alternative to `RefCounted` when the config should be editable/savable in the Inspector.

## Checklist
- [ ] Config class has defaults for every field.
- [ ] Factory signature takes one config argument.
- [ ] Callers override only the fields they need.

## Anti-patterns
- Growing `spawn()` into a long positional argument list. WHY: constructor telescoping — hard to read and error-prone.
- Reaching for a full Builder when a config object suffices. WHY: unnecessary complexity for flat parameter sets.

---
name: factory-builder-selection
topic: Choosing between Factory and Builder
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Rule of thumb: need 100 of something now → Factory. Need 1 thing requiring 10 setup steps → Builder.
- Factory: one call (`spawn()` / `create()`) returns a finished product immediately; objects are mostly identical; hides allocation, hierarchy, and instantiation boilerplate.
- Builder: several chained calls before `build()`; object has many optional parts or nested children; hides property injection, dependency linking, and structural layout.
- The patterns are not mutually exclusive — a Builder is essentially a specialized Factory with step-by-step customization.
- Typical Factory uses: spawning enemies, generating particle effects. Typical Builder uses: procedural levels, dynamic UI, dialogue trees.

## Checklist
- [ ] Count how many instances you need per call site.
- [ ] Count how many configuration steps the object needs.
- [ ] If many instances and few steps → Factory. If one instance and many steps → Builder.

## Anti-patterns
- Dedicated Factory for a unique object that appears once. WHY: over-engineering.
- Builder for a simple object with one or two properties. WHY: ceremony without benefit.

---
name: procedural-generation-with-factories
topic: Composing decoupled components for procedural generation
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Build procedural systems by composing independent components rather than writing one large manager script.
- A modifier component (e.g. `RadialPositionRandomizer`) should extend `Node` (not `Node2D`) when it only does math and needs no world position.
- Wire the modifier to the Factory via `spawner.product_created.connect(_on_product_created)` in `_ready()`. WHY: event-driven decoupling — the modifier never needs to know when or how spawning happens.
- In the handler, guard with `if product is Node2D:` before touching `global_position`. WHY: safely ignores non-2D products instead of crashing.
- Random ring placement: `angle = randf() * TAU`, `distance = randf_range(min_radius, max_radius)`, `offset = Vector2(cos(angle), sin(angle)) * distance`, then `product.global_position += offset`. WHY: the Spawner already placed the product at its center, so adding the offset moves it onto the ring.
- Assemble the field in the Scene Tree: Timer (looping N times) → `Spawner.spawn()` → `product_created` → modifier repositions. WHY: no asteroid-specific script is needed at all.
- Keep component count bounded. If firing one laser requires tracing five scripts and three Factories, the design is over-fragmented.

## Checklist
- [ ] Modifier connects to `product_created` in `_ready()`.
- [ ] `is Node2D` guard present before position math.
- [ ] `TAU` used for full-circle angles.
- [ ] Spawner placed at the intended center of the formation.
- [ ] Trace the call path; if it exceeds ~3 hops, simplify.

## Anti-patterns
- Writing a monolithic `AsteroidFieldManager` that handles timing, math, and instantiation. WHY: recreates the boilerplate the Factory was meant to remove.
- Splitting logic into so many micro-components that debugging requires following a maze of files. WHY: the goal of a pattern is readability, not fragmentation.

---
name: centralizing-creation-benefits
topic: Benefits and practices of centralized object creation
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 9 (pp. 223-242)"]
---
## Rules
- Managers should hold a reference to the Factory (`@onready var asteroid_factory: Spawner = $AsteroidFactory`) and call `spawn()`, never instantiate scenes themselves.
- After `spawn()`, null-check the result and `return` early if it is `null`. WHY: prevents crashes when the Factory lacks a blueprint.
- Let the manager apply only gameplay-specific logic (velocity, spin, stats) to the returned product. WHY: separates "how it's made" from "how it behaves".
- Expose tuning values (e.g. `@export var base_speed: float = 150.0`) so designers can adjust without editing scripts.
- Swap `product_scene` in the Inspector to change what a system spawns (asteroids → mines → comets) without touching manager code. WHY: Inspector-driven variation is the payoff of decoupling.
- For debugging, temporarily replace `product_scene` with a lightweight placeholder (e.g. a plain `Sprite2D`) to test manager logic independently of broken assets.
- Treat the Spawner as the single point of failure: when a spawned object misbehaves, inspect the Spawner script first.

## Checklist
- [ ] Manager references a Spawner node, not a PackedScene.
- [ ] Null-check after `spawn()`.
- [ ] Gameplay tuning lives in the manager, not the Factory.
- [ ] Tuning values exported for designers.
- [ ] Placeholder scene available for isolating manager bugs.

## Anti-patterns
- Managers calling `instantiate()` and `add_child()` directly. WHY: reintroduces scattered creation logic and merge conflicts.
- Injecting gameplay-specific behavior into the Spawner. WHY: the Factory must stay agnostic to remain reusable.

> CHECK: The chapter text mentions `call_deferred` in the Spawner's narrative ("The spawner also introduces new objects safely using call_deferred") but the shown `spawn()` code uses plain `container.add_child(product)`. Verify whether the final Spawner implementation always defers or only defers in physics callbacks.

<!-- 10 Applying Command and Service Patterns (pp. 243-262) -->
---
name: command-pattern-input-decoupling
topic: Command Pattern for input handling
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 10 (pp. 243-262)"]
---
## Rules
- Encapsulate each player action (move, shoot, shield) as a standalone `RefCounted` object with a single `execute(actor: Node) -> void` method. WHY: actions become data packets that can be queued, replayed, remapped, or generated by AI without touching the receiver's code.
- Extend `RefCounted`, never `Node`, for command objects. WHY: creating a Scene Tree node per button press causes memory bloat; commands are instructions, not scene entities.
- Pass the receiver (`actor`) as a parameter to `execute()` instead of letting the command search the Scene Tree or call global functions. WHY: the same command class then works for the player, any NPC, or a network-driven actor.
- Guard receiver calls with `actor.has_method("...")` inside `execute()`. WHY: keeps commands portable across projects and prevents hard crashes when the actor lacks the method.
- Put input polling in a separate Invoker (e.g. `PlayerInputHandler.get_command() -> Command`) that only constructs and returns the command, never executes it. WHY: the invoker does not know which actor will receive the command, so execution must be deferred.
- Use Godot's `InputMap` logical actions (`"fire_weapon"`) rather than physical keys (`"button_x"`) in the invoker. WHY: remapping becomes a data change, not a code change.
- Drive execution from the controller's `_physics_process()`: fetch the command, then call `command.execute(player_actor)` if non-null. WHY: keeps a single, predictable point where intent meets the actor.
- For real-time action games, execute movement and combat commands in parallel on the same frame (no queue, no `await`). WHY: forcing the player to finish a move animation before firing feels broken.
- For turn-based/strategy games, route commands through a queue so each completes before the next starts. WHY: sequential ordering is the gameplay contract in those genres.
- Reuse the identical command architecture for AI: an AI module produces the same `Command` objects a keyboard would. WHY: one character script drives players, enemies, and automated test/demo actors.

## Checklist
- [ ] Base `Command` class extends `RefCounted` with `execute(actor: Node) -> void`.
- [ ] Every concrete command takes its parameters in `_init()` (not `_ready()`).
- [ ] Invoker returns `Command` or `null`; it never calls `execute()`.
- [ ] Controller owns the `player_actor` reference and calls `execute()`.
- [ ] Commands use `has_method()` before invoking receiver methods.
- [ ] Input actions are read via `InputMap` names, not raw key codes.

## Anti-patterns
- Hardcoding `Input.is_action_pressed()` + direct `ship.fire_laser()` inside the ship script: couples invoker to receiver, blocks remapping, AI control, and replay.
- Commands that look up the player via `get_node()` or call global functions: unusable for NPCs and untestable.
- Extending `Node` for commands: Scene Tree bloat per input event.
- Executing the command inside the input handler: the handler does not know the target actor.
- Forcing all commands through a blocking queue in a real-time shooter: movement and shooting must run in parallel.

> CHECK: The chapter's testing snippet shows `MoveCommand.new()` with no args and later `move_cmd.unit = ship`, while the earlier `MoveCommand._init(target: Vector2)` takes a target. The two code samples appear inconsistent — verify the real constructor signature before copying.

---
name: command-queue-manager
topic: Command queue and history management
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 10 (pp. 243-262)"]
---
## Rules
- Keep two arrays on the receiver: `command_q: Array[Command]` (pending) and `history_q: Array[Command]` (executed). WHY: the queue drives execution order; history enables replays and undo.
- Add a boolean lock `awaiting_execution` to prevent re-entrant execution. WHY: without it, a new command can start while the current one is mid-animation.
- `add_command(c)` appends to `command_q` and immediately calls `execute_next_command()`. WHY: keeps the queue draining without a separate polling loop.
- `execute_next_command()` follows five steps: (1) guard clause on `awaiting_execution or command_q.is_empty()`, (2) set lock, grab `command_q.front()`, `await c.execute(self)`, (3) `pop_front()` and `push_front()` into history, (4) trim history past `MAX_HISTORY`, (5) clear lock and recurse. WHY: this is the minimal correct sequential executor.
- Cap history with a constant (e.g. `MAX_HISTORY = 50`) and `pop_back()` the oldest entries. WHY: unbounded history is a memory leak over long sessions.
- Validate the receiver with `is_instance_valid(self)` (or the actor) before `await c.execute(...)`. WHY: queued commands may target objects destroyed before their turn.
- Ensure every command has a guaranteed exit condition for its `await`. WHY: a command that never finishes jams the whole queue and freezes the actor permanently.
- Use `await` inside `execute()` to make it a coroutine; the queue pauses on that line until it resolves. WHY: this is how the queue knows an animation finished without polling.

## Checklist
- [ ] `command_q` and `history_q` are typed `Array[Command]`.
- [ ] `awaiting_execution` lock is set before `await` and cleared after.
- [ ] `is_instance_valid()` check before executing a dequeued command.
- [ ] `MAX_HISTORY` constant enforced with `pop_back()`.
- [ ] Recursive call at the end of `execute_next_command()` to drain the queue.
- [ ] Every command's `await` has a terminating signal or timeout.

## Anti-patterns
- No lock flag: overlapping command execution corrupts state.
- Unbounded `history_q`: RAM grows with playtime.
- Executing a command whose receiver was `queue_free()`d: crash on dangling reference.
- Commands that await a deleted UI animation or a signal that never fires: permanent queue jam.
- Using `size() == 0` instead of `is_empty()`: stylistic, but the chapter prefers `is_empty()` for clarity.

---
name: undo-redo-commands
topic: Undo/Redo via reversible commands
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 10 (pp. 243-262)"]
---
## Rules
- Give each reversible command an `undo(actor: Node) -> void` alongside `execute(actor: Node) -> void`. WHY: the command owns the knowledge of how to reverse itself, so the manager stays dumb.
- Cache the pre-execution state inside `execute()` (e.g. `initial_position = actor.global_position`) before mutating anything. WHY: undo needs the exact starting state, which may not be reconstructible later.
- Initialize commands with `_init()` parameters (e.g. `MoveCommand.new(target)`), not `_ready()`. WHY: `RefCounted` has no `_ready()`.
- Let the command ask the actor to create the `Tween`; the command itself cannot create one because it is not a `Node`. WHY: keeps engine-level animation on the receiver.
- Undo flow: pop the newest command from `history_q`, `await command.undo(actor)`, push it onto a `redo_q`. WHY: three steps are sufficient for a full undo/redo stack.
- Redo flow: pop from `redo_q`, `await command.execute(actor)`, push back onto `history_q`.
- Clear `redo_q` whenever a brand-new command is issued after undos. WHY: industry-standard "overwrite the future timeline" behavior.
- Guard undo/redo against empty stacks so mashing the button cannot crash. WHY: player input is not trustworthy.

## Checklist
- [ ] Every reversible command implements both `execute()` and `undo()`.
- [ ] `execute()` caches the state that `undo()` needs.
- [ ] `history_q` and `redo_q` are separate typed arrays.
- [ ] `redo_q.clear()` is called on any new command.
- [ ] Empty-stack guard exists in `undo_last_command()` / `redo_last_command()`.
- [ ] Both directions use `await` so animations complete before the next step.

## Anti-patterns
- Reversing actions by memorizing coordinates in the manager script: defeats the pattern and breaks for non-positional actions.
- Forgetting to clear `redo_q`: players can redo into a timeline that no longer makes sense.
- Calling `undo()` without `await`: the next command starts before the reverse animation ends.
- Undo on an empty history without a guard clause: index error / crash.

---
name: service-pattern-cross-cutting
topic: Service Pattern for global systems
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 10 (pp. 243-262)"]
---
## Rules
- Implement cross-cutting systems (audio, save, analytics, logging) as Autoload services rather than per-entity nodes or scattered globals. WHY: avoids Scene Tree bloat and lifecycle bugs where a dying entity takes its helper node with it.
- Keep services stateless: accept data as parameters, do the job, forget it. WHY: stateful Autoloads become "spaghetti globals" that any script can mutate, making bugs untraceable.
- Do not store player health, score, or inventory in an Autoload. WHY: that data belongs to the player object; the service should only persist or transmit it.
- For audio, pre-allocate a pool of `AudioStreamPlayer` nodes in `_ready()` (e.g. `POOL_SIZE = 10`) as children of the service. WHY: pooled players live in global scope, so sounds survive the caller's `queue_free()`.
- `play_sound(stream)` loops the pool, uses the first player where `not player.playing`, assigns the stream, plays, and returns early. WHY: early return keeps the loop cheap and the intent clear.
- Emit `push_warning("Audio pool is full! Sound dropped.")` when no player is free. WHY: silent drops are hard to diagnose; a warning surfaces pool exhaustion during development.
- Fetch services with `get_node_or_null("/root/Audio")` plus `has_method("play_sound")` instead of referencing the Autoload name directly. WHY: direct Autoload references create a hard compile dependency that breaks when the script is copied to another project.
- After handing off the sound request, the caller may `queue_free()` immediately. WHY: the service owns playback; the caller's lifetime is irrelevant.

## Checklist
- [ ] Service is an Autoload with a clear, single responsibility.
- [ ] No mutable game state stored at the top of the service script.
- [ ] Audio service pre-allocates a fixed pool in `_ready()`.
- [ ] `play_sound()` returns early on the first free player.
- [ ] Pool exhaustion produces a `push_warning`.
- [ ] Callers use `get_node_or_null()` + `has_method()` before invoking the service.
- [ ] Caller frees itself right after the request without cutting audio.

## Anti-patterns
- Giving every enemy its own `AudioStreamPlayer`: Scene Tree bloat, and the explosion sound cuts off when the enemy is freed.
- Autoload holding `player_health`, `current_score`, `inventory`, and mutating them from anywhere: untraceable global state.
- Hardcoding `Audio.play_sound()` in a script: breaks portability to projects without that Autoload.
- Service that grows unbounded internal caches: it is no longer stateless.

---
name: testing-commands-and-services
topic: Isolated testing with mocks
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 10 (pp. 243-262)"]
---
## Rules
- Test commands against a lightweight mock actor (e.g. `MockShip extends Node2D` with only `global_position`) instead of loading the real scene. WHY: tests run in milliseconds without booting the game, physics, or rendering.
- Configure the command with predictable numbers (e.g. 500 px at 100 px/s) and assert the computed result (5.0 s). WHY: exact math makes pass/fail unambiguous.
- Test guard clauses explicitly: instantiate an empty `CommandUnit`, call `undo_last_command()`, and assert `awaiting_execution == false`. WHY: proves the system rejects invalid input instead of crashing.
- Swap the real service for a mock during tests (e.g. `MockAudioService` that logs instead of playing). WHY: avoids blasting real sounds during test runs and isolates gameplay logic from engine-level audio.
- Keep mock services API-compatible with the real ones (`play_sound(stream)`). WHY: tests then validate the same call contract the game uses.

## Checklist
- [ ] Mock actor class exists with only the properties the command touches.
- [ ] Command tests assert exact numeric outcomes, not "looks right".
- [ ] Empty-queue / empty-history guard tests exist.
- [ ] Mock service implements the same method signatures as the real service.
- [ ] Tests do not instantiate the full player scene or load levels.

## Anti-patterns
- Testing by booting the whole game, spawning the player, and watching the screen: slow and non-deterministic.
- Asserting only that no error was thrown: misses wrong math.
- Using the real `AudioService` in tests: noisy, slow, and couples gameplay tests to engine audio.
- Skipping failure-path tests (empty undo, missing receiver): the crash paths are exactly what needs coverage.

> CHECK: The chapter's test snippet calls `move_cmd.execute()` with no actor argument and sets `move_cmd.unit`/`move_cmd.speed`/`move_cmd.target_position` as fields, which conflicts with the earlier `execute(actor: Node)` signature and `_init(target: Vector2)` constructor. Verify the actual API before writing tests.

<!-- 11 Adopting Data-Driven Design (pp. 263-282) -->
---
name: ddd-vs-dod
topic: data-driven design concepts
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 11 (pp. 263-282)"]
---
## Rules
- Treat Data-Driven Design (DDD) as an architectural choice: separate game logic (code) from game configuration (Resources, JSON, CSV). WHY: lets designers and modders change content without touching or recompiling code.
- Do not confuse DDD with Data-Oriented Design (DOD). DOD is a memory-layout optimization for CPU cache efficiency and is generally reserved for Godot's C++ servers, not GDScript. WHY: GDScript manages memory automatically, so DOD techniques give little benefit there.
- Split your project into two layers:
  - Hard architecture = low-level, rarely-changing systems (physics via `move_and_slide`, rendering server, input handlers).
  - Soft architecture = game-specific logic (power-up behavior, inventory, enemy AI).
- Rule: soft architecture must contain no hardcoded gameplay numbers. It should be an empty vessel that reads values from an external data source. WHY: keeps code stable while content scales.
- Prefer one generic script + data over one class per content variant. A single `Weapon` script fed `{"damage": 50, "element": "Fire"}` replaces `FireSword`, `IceSword`, etc. WHY: adding 1000 weapons then costs zero new GDScript.
- Decision table:
  | Situation | Approach |
  |---|---|
  | Value changes during balancing | external data (Resource/JSON) |
  | Value is a universal engine rule | hardcode in hard architecture |
  | New content variant of an existing type | new data entry, same script |
  | New mechanic/behavior | new code in soft architecture |
## Checklist
- [ ] List every gameplay number currently hardcoded in scripts.
- [ ] Classify each as hard architecture (keep) or soft architecture (externalize).
- [ ] Confirm each soft-architecture system can run with swapped data and no code edit.
- [ ] Verify adding a new content item requires no new script or scene.
## Anti-patterns
- Hardcoding `var speed: float = 150.0` inside `_physics_process`. WHY: forces designers to edit source code and restart the game to balance.
- Creating a dedicated class/script per item, weapon, or enemy type. WHY: codebase grows linearly with content and becomes unmaintainable.
- Moving a constant to the top of the script and calling it "data-driven". WHY: non-programmers still must open GDScript.
- Assuming DOD-style struct packing in GDScript will improve performance. WHY: the language abstracts memory layout.

---
name: prototype-pattern-resources
topic: resource-based data management
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 11 (pp. 263-282)"]
---
## Rules
- Use the Prototype Pattern: define a custom `Resource` (`.tres`) as the master blueprint; instances reference it instead of duplicating stats. WHY: one shared copy in memory instead of N copies, and one edit updates all instances.
- Define prototypes as `class_name X extends Resource` with `@export` fields (e.g. `prototype_id`, `display_name`, `base_health`, `movement_speed`, `sprite_texture`). WHY: `@export` exposes a drag-and-drop slot in the Inspector, the bridge between programmer and designer.
- Instance scripts should be thin: `@export var stats: EnemyPrototype` plus only per-instance state (`current_health`, position, velocity). WHY: keeps shared data centralized and per-object state correct.
- Initialize instance state from the prototype in `_ready()` (e.g. `current_health = stats.base_health`).
- Mutate only instance state on damage/death (`current_health -= amount`), never the prototype.
- Hard rule: prototypes hold static, unchanging data only (max health, base speed, damage, textures, AI aggressiveness). Nodes hold changing state (current HP, position, status effects). WHY: Resources are shared references — a mutable field on the prototype is shared by every instance.
- Build sub-prototypes by inheritance/override: a sub-prototype inherits base values and overrides only what differs (e.g. base speed 100 inherited, health raised to 150). WHY: changing the base prototype propagates to all sub-prototypes.
- Compose prototypes from sub-prototypes via exported Resource fields (`movement_logic: MovementPrototype`, `weapon_loadout: WeaponPrototype`). WHY: flattens the node hierarchy while building a rich data hierarchy; designers mix and match in the Inspector.
- Store behavior in Resources as stateless calculators: a virtual method takes current physical state and returns a result, e.g. `calculate_velocity(current_pos, target_pos, speed) -> Vector2`. WHY: logic becomes swappable data with no new enemy subclasses.
- Guard nested logic calls with a null check before use (`if stats.movement_logic != null:`).
## Checklist
- [ ] Every prototype field is static/unchanging.
- [ ] No per-instance mutable value lives on a Resource.
- [ ] Instance script reads prototype data in `_ready()`.
- [ ] Sub-prototypes override only differing fields.
- [ ] Behavior Resources are stateless (no stored position/HP).
- [ ] Null checks around optional nested Resources.
## Anti-patterns
- Storing `current_health` on the shared prototype. WHY: damaging one enemy drains health for all instances reading the same Resource.
- Duplicating all stats into each sub-prototype instead of inheriting. WHY: base changes no longer propagate; data drifts.
- Putting per-frame mutable state inside a behavior Resource. WHY: shared Resource state leaks between all users.
- Deep enemy class inheritance instead of composed data. WHY: reintroduces the rigid OOP coupling DDD removes.

---
name: json-external-data-zero-trust
topic: external data with JSON
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 11 (pp. 263-282)"]
---
## Rules
- Use JSON for data that non-Godot collaborators (designers, writers, translators, level designers) must edit. WHY: `.tres` files require the Godot editor; JSON is editable in any text tool or spreadsheet export.
- Prefer plain text over binary for configuration. WHY: humans can debug, validate, and diff it; binary is smaller/faster but opaque.
- JSON maps naturally to Godot `Dictionary` key-value pairs, so translation is straightforward.
- Adopt a Zero-Trust policy for any file loaded from outside the compiled game: never trust, always verify. WHY: external files can be typo'd, truncated, or malicious.
- Run this validation gauntlet in order, aborting safely on any failure:
  1. Existence: `FileAccess.file_exists(path)`.
  2. Readability: open with `FileAccess.open(path, FileAccess.READ)` and read text.
  3. Syntax: `JSON.new().parse(text)`; check `error != OK`, then log `get_error_line()` and `get_error_message()`.
  4. Root structure: `typeof(data) != TYPE_DICTIONARY` → abort.
  5. Key presence: `data.has("waves")` → abort if missing.
  6. Type check: `typeof(data["waves"]) != TYPE_ARRAY` → abort.
- On failure, `push_error`/`push_warning` and return an empty `Dictionary` or `null`; never crash. WHY: a game with Zero-Trust ignores a broken mod and keeps running.
- Support live reload: bind a hotkey (e.g. F5) in `_input()` to re-run the loader. WHY: balance changes take effect without restarting the game.
- Load external images with `Image.new()` + `image.load(path)`, check the returned `Error` against `OK`, then convert with `ImageTexture.create_from_image(image)`. WHY: raw `Image` cannot be assigned to `Sprite2D`/UI nodes; they need `Texture2D`.
- Guard asset loading with `FileAccess.file_exists()` and return `null` on failure.
## Checklist
- [ ] Every external read goes through all six validation steps.
- [ ] Parse errors log line number and message.
- [ ] Loader returns a safe empty value on any failure.
- [ ] Hotkey reload path re-validates from scratch.
- [ ] External textures checked for existence and load error before conversion.
## Anti-patterns
- Injecting parsed JSON straight into game logic without type checks. WHY: `"health": "one hundred"` crashes on integer assignment.
- Assuming an array key exists and looping it. WHY: a deleted comma or section causes a fatal null reference.
- Trusting mod files to be well-formed or non-malicious. WHY: huge numbers or odd structures can overflow memory or break logic.
- Silently swallowing parse errors with no console output. WHY: designers cannot diagnose why their data was ignored.

---
name: mod-loading-pipeline
topic: moddable systems
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 11 (pp. 263-282)"]
---
## Rules
- Ship mod content outside the `.pck`: read mods from `user://mods/`. WHY: the exported `.pck` is a sealed archive players cannot easily edit; `user://` is a writable OS folder (e.g. AppData on Windows).
- Note: Godot's `.pck` is an open archive by default; encryption is an optional export setting. Do not rely on obscurity for security.
- Implement the pipeline in five stages:
  1. Discovery — scan `user://mods/` for new files.
  2. Parsing and validation — run the JSON through the full Zero-Trust gauntlet.
  3. Texture loading — `load_external_texture()` for custom `.png`/`.jpg`.
  4. Dynamic prototype creation — `EnemyPrototype.new()`, then map validated JSON fields to Resource properties.
  5. Injection — register the finished Resource in a central Autoload database.
- Create Resources at runtime with `.new()` and assign fields from the parsed dictionary (e.g. `new_prototype.base_health = parsed_json["base_health"]`). WHY: custom Resources are plain objects; no editor step is needed.
- Register mods in a global Autoload (e.g. `EnemyDatabase.register_enemy(mod_id, prototype)`) and guard against duplicate IDs. WHY: game logic then cannot tell built-in content from modded content.
- Have spawners query the database by ID only. WHY: a modded enemy works with zero changes to spawner or instance code.
## Checklist
- [ ] Mods directory is `user://mods/`, not inside the `.pck`.
- [ ] Discovery handles zero mods and malformed filenames.
- [ ] Every mod passes validation before prototype creation.
- [ ] Missing textures fall back gracefully (null texture or default).
- [ ] Autoload database rejects duplicate mod IDs.
- [ ] Spawners resolve enemies by ID through the database.
## Anti-patterns
- Hardcoding mod paths inside the exported archive. WHY: players cannot add files there.
- Injecting a prototype before validation completes. WHY: one bad mod can crash the whole boot sequence.
- Letting game logic branch on "is this a mod?" WHY: reintroduces coupling and doubles the code paths to maintain.
- Assuming mod assets are always present when the JSON references them. WHY: missing `.png` files must degrade to a warning, not a crash.

> CHECK: The OCR text shows a missing closing parenthesis in the `calculate_velocity` call inside `_physics_process` (`stats.base_speed` line) and a missing closing brace in the `load_level_data` snippet. Verify against the printed code before copying.

<!-- 12 Structuring Gameplay Logic (pp. 283-304) -->
---
name: three-layer-gameplay-architecture
topic: Game architecture / separation of concerns
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Split gameplay code into three layers: Presentation (rendering, animation, audio), Domain (rules, math, state machines, no Scene Tree knowledge), Persistence (save/load to disk).
- Presentation scripts must be "dumb": they translate input downward and render numbers handed to them. They never compute game math or decide game state.
- Domain scripts must never reference `Sprite2D`, `Tween`, `AudioStreamPlayer`, `Label`, or any node path. They operate on plain data only.
- Persistence is the only layer allowed to touch `FileAccess` / `DirAccess`.
- Data flows as a waterfall: pure data at top → math in the middle → visual nodes at the bottom.
- Apply this architecture only when the project is commercial, data-heavy (RPG), or maintained by a team for years. For game jams, small mobile puzzles, and throwaway prototypes, direct `@onready` coupling to the Scene Tree is acceptable.
- WHY: mixing layers means a cosmetic change (deleting a health bar, renaming a node) crashes core mechanics with a null reference, and math cannot be tested without booting the graphics engine.

## Checklist
- [ ] Each script answers "which single layer am I?" before you write it.
- [ ] No Domain script contains a `$NodePath` or `@onready var` pointing at a visual node.
- [ ] No Presentation script contains arithmetic that changes game state.
- [ ] Save/load code lives only in the Persistence layer.
- [ ] Files are grouped by feature (e.g. `/Features/LevelManagement/`), not by type (`/Scripts/`).

## Anti-patterns
- Storing score/health inside a `Label` or `ProgressBar` value — the UI becomes the source of truth.
- Using a `Timer` node or `global_position` of a sprite to drive game rules.
- Letting a `HUDManager` compute combo multipliers or decide when the player is dead.
- Treating the three-layer split as mandatory for every project — it is overkill for small scopes.

---
name: god-class-diagnosis
topic: Code smells / refactoring triggers
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Flag a script as a God class if it matches 2+ of these: many hundreds/thousands of lines; manages multiple domains (damage math + UI + disk writes) in one file; a dozen unrelated `@onready var` node references at the top; acts as a universal signal hub or global-state Autoload.
- Typical Godot offenders: `LevelManager.gd`, `player_ship.gd` that handle input, movement, physics, scoring, waves, and audio at once.
- Refactor by drawing boundaries on responsibility, not by arbitrarily splitting the file into smaller tangled files.
- The first boundary to cut is always math vs. nodes.
- WHY: a God class has a huge blast radius (a velocity tweak breaks enemy AI), is undebuggable, and forces every teammate to edit the same file (merge conflicts, onboarding pain).

## Checklist
- [ ] Count lines; > several hundred is a warning sign.
- [ ] List the domains the script touches; more than one means split.
- [ ] Count `@onready` references to unrelated nodes.
- [ ] Check whether other systems depend on this script directly.

## Anti-patterns
- Splitting a God class into several smaller scripts that still each mix math and visuals.
- Keeping the God class as an Autoload "just for convenience" while adding new responsibilities.

---
name: pure-data-objects
topic: Game state representation
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Represent long-lived game state as Pure Data Objects extending `RefCounted` or `Resource`, never `Node`.
- Pure Data Objects contain only variables: no functions, no signals, no math.
- Example fields for a level: `current_score: int`, `current_wave: int`, `player_health: int`, `is_game_over: bool`.
- Store enums as integers in the data object; on load, cast back using the enum's `.values()` array.
- WHY: `RefCounted`/`Resource` objects float free of the Scene Tree, so they are immune to physics frames, pausing, and `queue_free()` lifecycle bugs, and they serialize trivially.

## Checklist
- [ ] Data object has zero `func` declarations.
- [ ] Data object has zero `signal` declarations.
- [ ] Data object is not added as a child of any node.
- [ ] Save system can grab one object instead of hunting the Scene Tree for a Label and a Player node.

## Anti-patterns
- Storing score in a `Label` node's text or in a global Autoload dictionary.
- Putting validation or clamping logic inside the data container.
- Attaching the data object to the Scene Tree to "make it easier to find".

---
name: context-hierarchy-and-dependency-injection
topic: Scoping and wiring
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Structure the game as a `RootContext` (main scene) owning global systems, with child contexts such as `MainMenuContext` and `GameplayContext`.
- Each context owns the Pure Data Object for its scope and guards it from outside access.
- Wire dependencies by passing objects explicitly (constructor injection), e.g. `LevelController.new(level_state)`.
- Use `Call Down, Signal Up`: parents call methods on children; children only emit signals upward and never know their parent.
- The context is the only place that connects Domain signals to Presentation methods.
- WHY: global Autoloads let any script (even a test scene) mutate any state; explicit injection makes dependencies visible and prevents accidental cross-scene interference.

## Checklist
- [ ] `GameplayContext` creates the `LevelState`, injects it into `LevelController`, and connects `LevelController` signals to `HUDManager` methods.
- [ ] `LevelController` and `HUDManager` hold no reference to each other.
- [ ] No gameplay script reads or writes another context's data.
- [ ] Global Autoloads are limited to stateless services (audio, file I/O).

## Anti-patterns
- A `GlobalVars` Autoload holding all game state.
- A Main Menu script able to trigger a game-over sequence or overwrite in-match health.
- Children reaching up with `get_parent()` to call methods on the context.

---
name: persistence-layer
topic: Save/load
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Implement persistence as a global Autoload service (`PersistenceManager`) — this is the one legitimate global, because it is a stateless read/write utility.
- On `_ready()`, check `DirAccess.dir_exists_absolute(BASE_SAVE_DIR)` and call `DirAccess.make_dir_recursive_absolute()` if missing, so a fresh install never crashes.
- Save path: `user://game_saves/` plus a master file name such as `void_defenders_save.json`.
- Serialize with `JSON.stringify(dict)` and write with `FileAccess.open(path, FileAccess.WRITE)`; always `close()` the file.
- Expose a `pre_save_path_changed` signal that the manager emits before a scene transition; contexts listen and pack their data before unload.
- The context converts its Pure Data Object into a `Dictionary` (e.g. `{"score": ..., "wave": ..., "health": ...}`) and hands it to the manager.
- On load, use `saved_data.get("score", 0)` style defaults so missing keys never crash.
- WHY: saving pure data avoids fragile node paths that break when the Scene Tree is reorganized, and the pre-save signal guarantees zero data loss on quit.

## Checklist
- [ ] Save directory creation is idempotent and recursive.
- [ ] Every `FileAccess.open` result is null-checked before writing.
- [ ] Every opened file is closed.
- [ ] Load path supplies defaults for every key.
- [ ] No gameplay script calls `FileAccess` directly.

## Anti-patterns
- Saving `NodePath` strings or node references into the save file.
- Writing save files from inside a Presentation or Domain script.
- Assuming the save directory exists on first launch.

---
name: static-typing-before-refactor
topic: Refactoring safety
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Convert all GDScript to strict static typing before starting a large refactor: `var score: int = 0`, `func add_points(amount: int) -> void:`.
- WHY: when moving functions between files, untyped code silently accepts wrong arguments and crashes at runtime; static typing makes the editor flag mismatches immediately with a red error line.

## Checklist
- [ ] Every variable has an explicit type.
- [ ] Every function has typed parameters and a return type.
- [ ] Editor shows no type warnings before you begin moving code.

## Anti-patterns
- Refactoring a monolith while leaving `var score = 0` untyped.
- Using `Variant`/untyped dictionaries as the interface between new layers.

---
name: monolith-refactor-sequence
topic: Refactoring procedure
confidence: consensus
sources: ["Godot 4 Best Practices, Robert Henning, ch. 12 (pp. 283-304)"]
---
## Rules
- Refactor in this order: (1) enforce static typing, (2) extract Pure Data Object, (3) extract Domain controller, (4) extract Presentation renderer, (5) wire everything in the context via dependency injection.
- Domain controller signature pattern: `_init(initial_state: LevelState)`, methods like `enemy_destroyed(point_value: int)` and `player_took_damage(amount: int)`, emitting `score_changed(new_score)` and `game_over`.
- Presentation methods take finished values only: `update_score_display(new_score: int)`, `show_game_over()` — no state checks, no math, no global signal connections.
- WHY: this order keeps the project runnable at each step and prevents introducing silent bugs while code moves between files.

## Checklist
- [ ] After step 2, the data object has no functions.
- [ ] After step 3, the controller has no `$NodePath` references.
- [ ] After step 4, the HUD has no `Events.*.connect` calls.
- [ ] After step 5, the context is the only file that knows about all three layers.
- [ ] A headless test can instantiate `LevelController` with a fake `LevelState` without loading the HUD.

## Anti-patterns
- Extracting the UI first and leaving math in the old script.
- Keeping the old God class alive as a thin wrapper that still holds state.
- Connecting Domain signals directly to Presentation inside the Domain script.

> CHECK: The OCR text cuts off mid-sentence at "data that must survive between game ___" and the `GameplayContext._ready()` code block appears truncated (missing closing braces and the `level_controller.game_over.connect(...)` closing paren). Verify the exact code against the book before reproducing it.
<!-- 1 Introducing Godot 4 (pp. 25-40) -->
---
name: godot4-csharp-toolchain-setup
topic: Godot 4 + C# environment setup
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 1 (pp. 25-40)"]
---
## Rules
- Download the **.NET** build of Godot, not the standard build. The download page shows two buttons; only "Godot Engine - .NET" ships the C# bindings. WHY: the plain build cannot compile or run C# scripts.
- Godot is portable: unzip the archive and run the executable. No installer, no registry writes. WHY: lets you keep the engine on a USB stick and pin a project to a specific engine version.
- Install the Microsoft .NET SDK separately from Godot. WHY: Godot relies on MSBuild from the SDK to generate the `.csproj` and compile your C# code.
- Use an external IDE/editor for C# even though Godot has a built-in script editor. WHY: the built-in editor is designed around GDScript; C# tooling (IntelliSense, refactoring, debugging) lives in the IDE.
- If using VS Code, install the extension published by **Microsoft** named "C#". WHY: third-party C# extensions may not integrate with the Godot/MSBuild workflow.
- Keep engine version and SDK version current and matched to the book/tutorial you follow. WHY: C# API surface and project file format change between Godot major versions.
- Verify the toolchain by creating a project and compiling once before writing gameplay code. WHY: catches missing SDK or wrong Godot build immediately instead of mid-feature.

## Checklist
- [ ] Downloaded "Godot Engine - .NET" (not the plain build)
- [ ] Unzipped and launched the editor successfully
- [ ] Installed the latest stable .NET SDK
- [ ] Installed an IDE/editor and the Microsoft C# extension
- [ ] Created a test project in an empty folder and confirmed MSBuild compiles it

## Anti-patterns
- Downloading the non-.NET Godot build and then wondering why C# scripts do not attach or compile.
- Skipping the .NET SDK because "Godot includes everything" — it does not include MSBuild.
- Installing a random C# extension in VS Code instead of the Microsoft one.
- Assuming C# knowledge is required to start; the book states programming/OOP fundamentals matter more than C# syntax.

> CHECK: OCR gives engine version "4.5.1" and ".NET 8.0" as "current" — verify against the actual latest releases, since these are time-sensitive.

---
name: godot-scene-node-model
topic: Scene system, node tree, and composition
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 1 (pp. 25-40)"]
---
## Rules
- Treat every object in Godot as a `Node`. A scene is a tree of nodes; the root is itself a node. WHY: this uniformity is what makes scenes reusable and nestable.
- Build a game object by composing several nodes into one scene (e.g. a first-person player = `CharacterBody3D` root + `CollisionShape3D` + camera rig + model). WHY: each node owns one concern, so you configure behaviour by combining nodes rather than subclassing one giant class.
- Reuse a scene as a prefab by dragging its `.tscn` file into another scene. No export/convert step is needed. WHY: this is Godot's main advantage over engines that require an explicit prefab step, and it makes prototyping fast.
- Nest scenes inside scenes (a `PackedScene` node appears as a child with a clapperboard icon). WHY: nested scenes stay independently editable and are instanced, not copied.
- Use **composition over inheritance** for cross-cutting traits: make `HealthComponent` and `ArmorComponent` as separate scenes and attach them to any actor that needs them. WHY: avoids duplicating health/armor logic across every enemy and player type.
- Use inheritance for "is-a" relationships (a child node inherits its parent's properties); use composition for "has-a" capabilities. WHY: mixing them up produces deep, brittle trees.
- Use polymorphism by extending a base scene (e.g. an `Item` scene) so variants inherit shape, collision and model, then override specifics. WHY: one base definition, many item types.

## Checklist
- [ ] Root node type chosen to match the actor's physics role (e.g. `CharacterBody3D` for a player)
- [ ] Collision shape is a child of the body, not a sibling
- [ ] Reusable sub-objects (model, camera rig, components) extracted into their own scenes
- [ ] Scripts attached to the node that owns the behaviour, not to the root by default
- [ ] No duplicated logic that could be a shared component scene

## Anti-patterns
- Building one monolithic scene with dozens of unrelated nodes instead of nesting reusable sub-scenes.
- Copy-pasting a player scene to make an enemy instead of instancing and overriding.
- Putting health/armor fields directly on every actor class instead of a `HealthComponent`/`ArmorComponent` scene.
- Assuming a nested scene is a copy — it is an instance; editing the source changes all uses.

---
name: godot-editor-ui-navigation
topic: Godot 4 editor interface layout
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 1 (pp. 25-40)"]
---
## Rules
- Project Manager is the first screen: create, import, rename, remove or delete projects there. Create new projects in an **empty folder**. WHY: Godot writes its project files into the chosen directory and expects to own it.
- Scene/Import panel (top-left) has two tabs: **Scene** shows the node tree of the currently open scene; **Import** shows per-asset import properties with a **Re-import** button. WHY: asset settings (compression, filtering) are per-file and must be re-applied after changes.
- Viewport (centre) is where the scene renders. The view-switcher above it toggles **2D / 3D / Script / Asset Library**. WHY: Script view lists scripts available in the open scene; Asset Library is where third-party plugins are found and uploaded.
- In 3D view, use the axis gizmo (top-right of viewport) to click an X/Y/Z axis for an orthographic view, or drag it to orbit. WHY: precise alignment is much faster with axis-locked views than free orbit.
- FileSystem panel (bottom-left) shows the project's file tree under `res://`. WHY: `res://` is the project root path used in all resource references.
- Inspector/Node/History panel (right): **Inspector** edits the selected node's properties (transform, scale, rotation, etc.); **Node** lists the node's signals and groups; **History** logs every action, scoped to the scene or globally. WHY: History is the undo/audit trail when you lose track of a change.
- Bottom panel tabs: **Output** (debug prints, errors, warnings), **Debugger** (detailed errors, resource monitoring), **Audio** (buses, effects, per-bus volume), **Animation** (preview, Bézier curves), **Shader Editor** (GLSL-like shader language), **MSBuild** (compiles the C# project; shows build warnings/errors). WHY: MSBuild output is the first place to look when C# fails to compile.

## Checklist
- [ ] New project created in an empty folder
- [ ] Correct view (2D/3D) selected before editing transforms
- [ ] Import tab checked after changing an asset's source file
- [ ] MSBuild tab open when working on C# code
- [ ] History tab consulted when an unexpected change appears

## Anti-patterns
- Creating a project inside a non-empty folder or inside another project.
- Editing a node's transform in the wrong view (2D vs 3D) and getting unexpected values.
- Ignoring the Output/Debugger tabs and debugging by guesswork.
- Forgetting to re-import an asset after editing it externally, then wondering why the old version renders.

---
name: godot-project-file-naming
topic: Project folder structure and naming conventions
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 1 (pp. 25-40)"]
---
## Rules
- Use **PascalCase** for folder and file names. WHY: consistent, sortable, and matches C# type naming so files and classes line up.
- Use **snake_case** for node and scene names. WHY: keeps node paths readable in code and matches common Godot/GDScript convention.
- Always create an `addons/` folder for plugins and third-party components. WHY: Godot recognises `addons/` as the plugin location; scattering plugins elsewhere breaks enable/disable.
- Godot imposes **no** mandatory project structure — the layout is your choice. WHY: the engine resolves everything through `res://` paths, so any tree works; pick one and stay consistent.
- A conventional starting layout: `assets/` (with `audio/`, `sfx/`, `ui/fonts/`, `resources/`), `scenes/`, `scripts/`, `addons/`. WHY: separates raw assets from scenes and code, which keeps diffs clean in Git.

## Checklist
- [ ] `addons/` exists at project root
- [ ] Folders and files use PascalCase
- [ ] Nodes and scenes use snake_case
- [ ] Assets, scenes and scripts are in separate top-level folders
- [ ] Structure documented so collaborators follow it

## Anti-patterns
- Mixing naming conventions within the same folder.
- Placing plugins outside `addons/`.
- Dumping scenes, scripts and raw assets into the project root.
- Reorganising folders late in a project without updating resource paths (breaks references).

> CHECK: The chapter says Godot "does not prescribe" a structure but then gives naming rules — confirm whether the PascalCase/snake_case split is the author's own convention or documented Godot guidance before treating it as a hard rule.

<!-- 2 Understanding How C# Works in Godot (pp. 41-68) -->
---
name: godot-csharp-editor-setup
topic: Godot C# tooling configuration
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Set `Editor > Editor Settings > Dotnet > Editor > External Editor` to your IDE (e.g. Visual Studio Code) so double-clicking a `.cs` script opens it in that IDE instead of Godot's built-in editor. WHY: avoids copy-pasting code between editors.
- Changes to Editor Settings apply immediately; no engine or project restart required. WHY: saves iteration time.
- In VS Code, open the project folder (not a subfolder) via `File > Open Folder...` so all scripts and `.vscode` config are in the workspace. WHY: the debugger and task runner resolve paths relative to the workspace root.
- Create `.vscode/launch.json` with `type: "coreclr"`, `request: "launch"`, `preLaunchTask: "build"`, `program: "${env:GODOT4}"`, `cwd: "${workspaceFolder}"`, `stopAtEntry: false`. WHY: `coreclr` is the .NET debugger; `launch` starts the project under the debugger so breakpoints work.
- Prefer the `GODOT4` environment variable over a hard-coded executable path in `program`. WHY: a hard-coded path breaks when the Godot binary moves; env vars survive relocation.
- On Windows, set `GODOT4` via System Properties > Environment Variables > New (variable name `GODOT4`, value = path to Godot executable). Restart VS Code/Godot (sometimes the machine) for it to take effect. WHY: env vars are read at process start.
- Create `.vscode/tasks.json` with a task `label: "build"`, `command: "dotnet"`, `type: "shell"`, `args: ["build"]`, `problemMatcher: "$msCompile"`. WHY: `preLaunchTask: "build"` must match this label so the project compiles before launch; `$msCompile` surfaces C# compiler errors in the Problems panel.
- If using a literal path in `program`, replace backslashes with forward slashes. WHY: JSON/VS Code path parsing expects forward slashes.

## Checklist
- [ ] Godot .NET build installed (not the standard build).
- [ ] External Editor set to your IDE in Editor Settings.
- [ ] Project folder opened as workspace root in VS Code.
- [ ] `launch.json` present with `coreclr` / `launch` / `preLaunchTask: build`.
- [ ] `GODOT4` env var points to the Godot executable.
- [ ] `tasks.json` present with a `build` task using `dotnet build`.
- [ ] Breakpoint hit test: set a breakpoint in a `_PhysicsProcess` method and run.

## Anti-patterns
- Hard-coding the Godot executable path in `launch.json` as the primary approach — it silently breaks on move/update.
- Opening a subfolder instead of the project root in VS Code — debugger and task paths resolve incorrectly.
- Skipping `tasks.json` — `preLaunchTask: "build"` fails and the debugger launches stale binaries.
- Assuming Editor Settings changes need a restart — they do not; wasting time restarting.

> CHECK: The chapter's `launch.json` snippet appears truncated in the OCR (missing closing braces). Verify the exact JSON against the book's GitHub repo before copying.

---
name: godot4-csharp-api-changes
topic: Godot 4 C# API and language conventions
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Target the .NET SDK, not the legacy Mono SDK. WHY: Godot 4 ships C# support through .NET, giving access to current class libraries, the C# compiler, and first-class Microsoft tooling.
- Expect Godot signals to be exposed as C# events. WHY: idiomatic C# developers can subscribe with `+=` instead of using `Connect`.
- Follow PascalCase for public members, methods, and Godot API calls, matching .NET naming conventions. WHY: Godot 4 renamed many API functions to align with .NET style, so mixed casing will look inconsistent and may not compile against the new names.
- Use the official C# debugger (via `coreclr`) rather than GDScript-only tooling. WHY: it integrates with standard .NET debugging workflows (breakpoints, watch, call stack).
- Consult the dedicated "GDScript vs C#" documentation page when porting examples. WHY: syntax and API names differ enough that direct translation causes errors.

## Checklist
- [ ] Project uses the .NET edition of Godot 4.
- [ ] Code style uses PascalCase for public API surface.
- [ ] Signal handling uses C# events where idiomatic.
- [ ] Debug configuration uses `coreclr`.

## Anti-patterns
- Following Godot 3 / Mono-era tutorials verbatim — API names and SDK assumptions changed.
- Mixing snake_case Godot 3 names with Godot 4 C# API — will not resolve.

---
name: godot-csharp-script-node-binding
topic: C# script structure and node inheritance
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Name the C# class identically to the script file (e.g. `PlayerMovement.cs` → `class PlayerMovement`). WHY: Godot resolves the script's class by filename; a mismatch breaks attachment.
- Declare the class `partial`. WHY: Godot's source generators emit the other half of the class for engine integration.
- Inherit from the Godot class matching the node the script is attached to (attach to `CharacterBody2D` → inherit `Godot.CharacterBody2D`; attach to `Sprite2D` → inherit `Godot.Sprite2D`). WHY: the script *is* the node's behavior; wrong base class means missing node API.
- From Godot 4.2 onward, the `Godot.` prefix on the base class is optional. WHY: the engine resolves the Godot namespace automatically.
- Use the built-in template offered when attaching a script (e.g. the `CharacterBody2D` basic-movement template) as a starting point. WHY: it wires up `_PhysicsProcess`, gravity, and input handling correctly.

## Checklist
- [ ] Class name == file name.
- [ ] Class marked `partial`.
- [ ] Base class matches attached node type.
- [ ] Script attached to the intended node (right-click node > Attach Script).

## Anti-patterns
- Renaming the file without renaming the class (or vice versa).
- Omitting `partial` — source-generated members will not merge.
- Inheriting `Node` for a `CharacterBody2D` script — loses `IsOnFloor`, `MoveAndSlide`, etc.

---
name: godot-characterbody2d-movement
topic: 2D character movement with CharacterBody2D
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Put movement and physics logic in `_PhysicsProcess(double delta)`, not `_Process`. WHY: `_PhysicsProcess` runs at a fixed rate (default 60 Hz) independent of frame rate, keeping physics stable.
- Multiply velocity changes by `delta` (cast to `float`). WHY: `delta` is elapsed seconds since the last physics tick; without it, movement speed varies with hardware performance.
- Apply gravity only when airborne: `if (!IsOnFloor()) velocity.Y += gravity * (float)delta;`. WHY: prevents gravity accumulating while grounded.
- Read gravity from Project Settings (`Project > Project Settings > Physics > 2D > Default Gravity`, default -9.8) rather than hard-coding. WHY: centralizes tuning.
- Jump only when grounded and the action is just pressed: `if (Input.IsActionJustPressed("ui_accept") && IsOnFloor()) velocity.Y = JumpVelocity;`. WHY: `IsActionJustPressed` prevents auto-repeat; `IsOnFloor` prevents mid-air jumps.
- Read directional input with `Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down")` returning a `Vector2`. WHY: `GetVector` normalizes diagonal input automatically.
- Call `MoveAndSlide()` as the last step after updating `Velocity`. WHY: it resolves collisions and updates the body's actual velocity; calling it earlier uses stale input.
- Note the template uses a lowercase `velocity` placeholder that must be assigned to the node's `Velocity` property before `MoveAndSlide()`. WHY: `Velocity` is the engine property; `velocity` is a local variable.

## Checklist
- [ ] Movement code inside `_PhysicsProcess`.
- [ ] Every velocity change multiplied by `delta`.
- [ ] Gravity applied only when `!IsOnFloor()`.
- [ ] Jump gated on `IsOnFloor()` and `IsActionJustPressed`.
- [ ] `MoveAndSlide()` called last.
- [ ] `Velocity` assigned from the local `velocity` before `MoveAndSlide()`.

## Anti-patterns
- Doing movement in `_Process` — frame-rate-dependent physics.
- Forgetting `delta` — speed scales with FPS.
- Calling `MoveAndSlide()` before applying input — one-frame lag and missed collisions.
- Hard-coding gravity instead of reading Project Settings.

---
name: godot-2d-scene-node-structure
topic: Building 2D scenes and collision shapes
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Create scenes via the Scene panel: choose 2D, 3D, UI, or Other Node (to pick a specific root). WHY: the root node type determines the scene's category and available API.
- For a player, use `CharacterBody2D` as root. WHY: it is a physics-less body — you implement collision response yourself via code, giving full control over movement.
- Add a `CollisionShape2D` child to any physics body. WHY: without a shape the body cannot collide or interact; Godot shows a warning icon.
- Assign a concrete shape resource (e.g. `RectangleShape2D`, `CircleShape2D`, `CapsuleShape2D`) to the `CollisionShape2D`'s `Shape` property. WHY: the node needs an actual shape instance, not just the node.
- Resize collision shapes using the viewport control handles or the `Size` property, **not** the `Scale` property. WHY: scaling a shape distorts collision math; `Size` is the intended dimension control.
- Add a `Sprite2D` child and set its `Texture` (e.g. `icon.svg`) for visuals. WHY: separates visual from collision.
- Align the sprite edges with the collision shape edges. WHY: mismatched bounds cause visual/physical desync.
- Save scenes with the `.tscn` extension (e.g. `Player.tscn`, `World.tscn`). WHY: `.tscn` is Godot's text scene format.
- Nest the player scene into the world scene by dragging `Player.tscn` from the FileSystem panel into the Scene panel. WHY: instancing keeps the player reusable across levels.
- Use `StaticBody2D` for immovable geometry like ground. WHY: static bodies skip continuous physics updates, saving CPU.

## Checklist
- [ ] Root node type matches the scene's purpose.
- [ ] Every physics body has a `CollisionShape2D` with a non-empty `Shape`.
- [ ] Collision shape sized via handles or `Size`, not `Scale`.
- [ ] Sprite aligned to collision bounds.
- [ ] Scene saved as `.tscn`.
- [ ] Player scene instanced into world scene.
- [ ] Player placed above ground so gravity settles it.

## Anti-patterns
- Leaving `Shape` as `<empty>` — no collisions, warning persists.
- Using `Scale` to size a collision shape — distorts physics.
- Using `CharacterBody2D` for static ground — wastes physics budget; use `StaticBody2D`.
- Duplicating player nodes per level instead of instancing `Player.tscn`.

---
name: godot-input-map-actions
topic: Input map and action names
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 2 (pp. 41-68)"]
---
## Rules
- Reference input actions by string name in code (e.g. `"ui_left"`, `"ui_accept"`). WHY: actions decouple code from physical keys, so remapping is a settings change, not a code change.
- Access the input map at `Project > Project Settings > Input Map`. WHY: this is where actions and their key bindings live.
- Toggle "Show Built-in Actions" to see Godot's default actions (`ui_accept`, `ui_left`, `ui_right`, `ui_up`, `ui_down`, etc.). WHY: built-ins are hidden by default and easy to miss.
- Built-in actions can be edited or deleted; create custom actions (e.g. `"running"`) for game-specific inputs. WHY: keeps engine defaults intact while adding your own.

## Checklist
- [ ] All input read via named actions, not raw key codes.
- [ ] Built-in actions visible in Input Map for reference.
- [ ] Custom actions defined for game-specific inputs.

## Anti-patterns
- Hard-coding key codes (`Key.Shift`) instead of actions — breaks remapping.
- Assuming built-in actions are visible without toggling the option.

<!-- 3 Organizing and Setting Up a Project for a 3D Action Game (pp. 69-89) -->
---
name: godot-project-structure-by-feature
topic: project organization
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 3 (pp. 69-89)"]
---
## Rules
- Organize Godot projects by **feature/module**, not by asset type. Create one folder per gameplay feature (e.g. `player/`, `world/`) containing that feature's scenes, scripts, models, and textures together. WHY: Godot packs assets inside scenes, so everything a scene needs lives near it and is easier to find and move.
- Add a `lib/` (a.k.a. `utilities/`) folder for scripts and systems reused across multiple scenes. WHY: shared code has no single owning feature and would otherwise be duplicated or misplaced.
- Add an `addons/` folder for third-party plugins and systems. WHY: keeps external code separated from your own so upgrades and removals are clean.
- Keep naming consistent across the whole project (folder names, file names, scene names). WHY: consistency matters more than which scheme you pick; mixed conventions cause navigation errors.
- Aim for **low coupling, high cohesion**: an object should depend on as few other objects as possible, and everything inside it should serve one responsibility. WHY: decoupled objects can be modified in isolation without breaking unrelated code.
- Prefer signals over direct references to keep scenes and objects decoupled. WHY: a signal lets a sender notify listeners without knowing who they are, removing hard dependencies.
- Put item/collectible logic in an abstract item class that each item inherits from, not inside a `World` object. WHY: avoids duplicated code per item variant, keeps `World` from bloating, and makes items reusable.
- Only put things inside an object that the object actually needs to know about. Ask "does this object care about this data?" before adding it. WHY: unrelated data increases coupling and forces edits in multiple places when one feature changes.

## Checklist
- [ ] Feature folders created (`player/`, `world/`, …) with scenes, scripts, and assets co-located.
- [ ] `lib/` folder exists for cross-scene reusable scripts.
- [ ] `addons/` folder exists for third-party plugins.
- [ ] Naming convention chosen and applied uniformly.
- [ ] Each script/scene has a single clear responsibility (high cohesion).
- [ ] Cross-object communication uses signals where practical (low coupling).
- [ ] Shared systems (items, etc.) live in their own class, not inside a container object.

## Anti-patterns
- **Organizing by asset type** (all scripts in one folder, all models in another): splits a single feature across many folders, making edits to one feature require jumping between directories. Acceptable only for very small projects.
- **God-object containers**: stuffing item data, spawn logic, and unrelated systems into `World` (or any single manager). Causes bloated scripts, duplicated code for variants, hard debugging, and non-reusable pieces.
- **Tight coupling via direct references** where a signal would do: makes refactoring one object ripple into many others.
- **Inconsistent structure**: mixing conventions mid-project; the author stresses consistency over the specific scheme chosen.

> CHECK: The chapter's exact folder examples (player/, world/, lib/, addons/) are confirmed in the text; verify whether the author also recommends a top-level `assets/` or `scenes/` folder — the OCR does not show one.
---
name: godot-version-control-github-desktop
topic: version control setup
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 3 (pp. 69-89)"]
---
## Rules
- Use Git for version control; use GitHub as the hosting platform. WHY: Git is free, well-documented, and integrates cleanly with Godot; GitHub adds a web UI and GUI tooling.
- Use **GitHub Desktop** as the GUI client for cloning and managing repos locally. WHY: it is beginner-friendly and acts as an intermediary between the local machine and GitHub servers.
- When creating a repo in GitHub Desktop, set: a **Name** with no spaces, a **Description**, a **Local path** (author uses `Documents/`), optionally a **README**, a **Git ignore** (choose the **Godot** template), and a **License** (author uses **MIT**, same as Godot). WHY: the Godot `.gitignore` prevents machine-generated files from being committed; a license defines reuse rights.
- The default and first branch is `main`. WHY: it is created automatically and is the branch GitHub Desktop tracks by default.
- To publish a local repo to GitHub, click **Publish repository** in the top bar, set the public/private flag, then confirm. WHY: this pushes the local repo to GitHub servers so it survives local failure.
- Follow the daily workflow: **Fetch → Pull → Commit → Push**. WHY: fetch/pull bring remote changes down before you commit, and push saves your committed work to the server.
- For solo projects, a single `main` branch is sufficient; skip branching/forking/merge-conflict features unless you actually need them. WHY: extra Git features add complexity without benefit for one-person work.

## Checklist
- [ ] GitHub account created (or an alternative chosen).
- [ ] GitHub Desktop installed and signed in.
- [ ] New repository created with a space-free name and a local path.
- [ ] Godot `.gitignore` selected.
- [ ] License chosen (MIT recommended).
- [ ] Repository published to GitHub (public or private decided).
- [ ] First commit and push completed after importing assets.

## Anti-patterns
- **Repo names containing spaces**: causes friction in paths and tooling; use hyphens instead.
- **Skipping `.gitignore`**: machine-generated files get committed and clutter the repo.
- **Committing without pulling first** in a multi-person or multi-device setup: risks conflicts and lost work.
- **Switching version control systems mid-project**: the author notes this is tedious; choose the right tool up front.

> CHECK: The chapter lists alternatives (GitLab, Bitbucket, SourceForge, AWS CodeCommit, Mercurial, SVN, Azure DevOps) but the OCR does not state a recommendation among them beyond "choose what fits your team" — treat as informational, not a rule.
---
name: godot-importing-initial-assets
topic: asset import
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 3 (pp. 69-89)"]
---
## Rules
- Import assets by **dragging files/folders from the OS into Godot's FileSystem panel**. WHY: Godot auto-detects and imports on drop; a progress prompt appears and no manual import step is needed.
- For the player model, use the **GDQuest godot-3d-mannequin** repo: download the ZIP, extract, and take the `.glb` (plus materials) from `godot-csharp/assets/3d/mannequiny`. WHY: it is a free, rigged, animated model suitable for a third-person controller.
- After importing the `.glb`, double-click it to confirm it opens and renders correctly, then close the window and save the project. WHY: verifies the import succeeded before building on it.
- For world/level textures, use **Kenney prototype textures** (`kenney.nl/assets/prototype-textures`). WHY: free, purpose-built for prototyping levels.
- Rename imported folders to meaningful names (author renames `textures` → `env_textures`) and place them into the feature folders (`player/`, `world/`). WHY: keeps the feature-based structure intact and avoids ambiguous folder names.
- Download only the files you need (use **Download ZIP** on GitHub) rather than cloning entire repos. WHY: avoids pulling large unrelated content into the project.

## Checklist
- [ ] Player `.glb` and its materials imported into `player/`.
- [ ] Model opens and renders in Godot without errors.
- [ ] Texture pack imported and renamed (e.g. `env_textures`).
- [ ] Assets placed into the correct feature folders.
- [ ] Project saved after import.
- [ ] Changes committed and pushed to GitHub.

## Anti-patterns
- **Cloning whole asset repos** when only a few files are needed: wastes space and clutters the project.
- **Leaving default folder names** like `textures`: ambiguous once multiple texture sets exist; rename to reflect purpose.
- **Building on an unverified import**: always open the imported asset once to confirm it loaded correctly.
- **Forgetting to push after importing**: imported assets are part of the project; commit and push so they are backed up.

> CHECK: The chapter references a `godot-csharp` folder inside the mannequin repo — verify the exact path still exists, as repo layouts can change.

<!-- 4 Creating Our Player Controller (pp. 91-143) -->
---
name: player-scene-node-structure
topic: Godot 4 3D player scene composition
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- Root the player scene on `CharacterBody3D` named `Player`; drag the rigged `.glb` model in as an **instanced (packed) scene** child, not as loose nodes. WHY: keeps the model encapsulated so one edit propagates to every scene that uses it.
- Right-click the instanced model → **Editable Children** to reach inner nodes (e.g. `AnimationPlayer`). WHY: you keep the link to the source scene instead of breaking it.
- Add `CollisionShape3D` as a direct child of the root; pick `New CapsuleShape3D`; then shrink `Radius`/`Height`/`Position` until the capsule hugs the mesh. WHY: an oversized capsule makes the player collide with the world too early.
- Camera rig hierarchy: `Node3D` (rename `CameraPivot`) → `SpringArm3D` → `Camera3D`. WHY: rotating the pivot rotates arm and camera together with one line of code.
- Set `SpringArm3D.Length` to ~3 m (default 1 m). WHY: the arm pushes the camera back along its length and pulls it in when geometry blocks the view.
- Position the pivot at neck height behind the head; leave yaw/pitch to the script.
- Save the scene as `Player.tscn` and test it standalone with the scene-only Play button (clapperboard icon).
- Rename the model root to `Body` for readable `GetNode` paths.

## Checklist
- [ ] Root is `CharacterBody3D`, named `Player`
- [ ] Model is an instanced scene with Editable Children enabled
- [ ] `CollisionShape3D` present, capsule fitted to mesh
- [ ] `CameraPivot` → `SpringArm3D` → `Camera3D` chain exists
- [ ] `SpringArm3D.Length` ≈ 3
- [ ] Default animation set to `idle` in the AnimationPlayer dropdown
- [ ] Scene saved as `Player.tscn`, runs without errors

## Anti-patterns
- Adding the model's nodes directly into the player scene (loses reuse and makes bulk edits painful).
- Leaving the capsule at default size — causes phantom early collisions.
- Attaching the camera directly to the root instead of a pivot — you then need duplicate rotation code for arm and camera.
- Forgetting `Use Collision` on test geometry (see test-area card).

> CHECK: OCR shows `MouseMode.Enum.Visible` / `Hidden`; the real Godot enum is `Input.MouseModeEnum.Visible` / `Hidden` / `Captured` / `Confined`.

---
name: third-person-camera-mouse-look
topic: Third-person camera control with mouse
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- In `_Ready()`, set `Input.MouseMode = Input.MouseModeEnum.Captured`. WHY: locks the cursor to screen center so `InputEventMouseMotion.Relative` gives usable deltas. `Hidden` is not enough — you need relative motion tracking.
- Handle look in `_Input(InputEvent @event)`; test `if (@event is InputEventMouseMotion m)`.
- Cache the pivot: `cameraPivot = GetNode<Node3D>("CameraPivot");` in `_Ready()`. Prefer unique-name access (`%CameraPivot`) over long paths.
- Yaw: `cameraPivot.RotateY(ConvertDegreesToRadian(-m.Relative.X * cameraSensitivity_H));`
- Pitch: `cameraPivot.RotateX(ConvertDegreesToRadian(-m.Relative.Y * cameraSensitivity_V));`
- `RotateY`/`RotateX` take **radians**; convert with `num * ((float)Math.PI / 180)`.
- Clamp pitch after rotating: `cameraPivot.Rotation = cameraPivot.Rotation.Clamp(-maxSpringRotation, maxSpringRotation);` with `maxSpringRotation = new Vector3(30, 30, 0)`. WHY: without clamping the camera flips over the player.
- Expose sensitivity as `[Export(PropertyHint.Range,"0,0.5")] private float CameraSensitivity_H = 0.05f;` (and `_V`). WHY: there is no universally correct value; tune it in the Inspector with a slider.
- Start both sensitivities at 0.05 and adjust per device.

## Checklist
- [ ] Mouse mode captured in `_Ready`
- [ ] `_Input` handles `InputEventMouseMotion`
- [ ] Pivot node cached once, not fetched per frame
- [ ] Degrees→radians conversion applied to both axes
- [ ] Pitch clamped to ±30° (or your chosen bound)
- [ ] Sensitivities exported and range-hinted
- [ ] Tested: slow mouse movement feels smooth, no over-tilt

## Anti-patterns
- Passing raw degrees into `RotateY`/`RotateX` — rotation becomes wildly oversensitive.
- Using `MouseModeEnum.Hidden` when you need relative mouse deltas.
- Calling `GetNode` every frame inside `_Input`.
- Omitting the clamp — camera rolls past vertical and the view inverts.

---
name: player-movement-relative-to-camera
topic: CharacterBody3D movement and facing
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- Attach a C# script to the root using the **Basic Movement** template; keep the template code and extend it.
- Read input into `inputDir` (Vector2), build `direction` (Vector3), then rotate it into camera space: `direction = direction.Rotated(Vector3.Up, cameraPivot.Rotation.Y);` WHY: without this, "forward" is always world +Z and breaks once the camera orbits.
- Apply velocity: `velocity.X = direction.X * currSpeed; velocity.Z = direction.Z * currSpeed;`
- Face the movement direction with `rotation.Y = Mathf.LerpAngle(rotation.Y, Mathf.Atan2(velocity.X, velocity.Z), 0.15f);` then `body.Rotation = rotation;`
  - `Atan2` takes X and Z (not Y) because Y is the vertical/jump axis.
  - The lerp factor (~0.15) controls turn smoothing.
- Cache `body = GetNode<Node3D>("Body");` and `rotation = body.Rotation;` in `_Ready()`; `Node3D.Rotation` components are read-only, so assign the whole vector back.
- Call `MoveAndSlide()` after all velocity and animation-condition updates.

## Checklist
- [ ] Script attached to root, C# language, Basic Movement template
- [ ] `direction` rotated by `cameraPivot.Rotation.Y`
- [ ] Body node cached in `_Ready`
- [ ] `LerpAngle` used for smooth turning
- [ ] `MoveAndSlide()` is the last movement call
- [ ] Tested: orbit camera fully, then walk forward — player moves away from camera

## Anti-patterns
- Using world-space direction without camera rotation — player walks the wrong way after orbiting.
- Feeding `velocity.Y` into `Atan2` — pitch/jump contaminates facing.
- Assigning `body.Rotation.Y` directly — it is read-only; assign the full `Rotation`.

---
name: animation-tree-state-machine
topic: AnimationTree state machine for locomotion
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- Prefer `AnimationTree` over driving `AnimationPlayer` from script. WHY: state-based transitions give free blending and stay maintainable as states grow.
- Add `AnimationTree` as a child of the player root; set `Tree Root` = `New AnimationNodeStateMachine`; assign the `AnimationPlayer` to the `Anim Player` slot.
- Set `AnimationTree.Active = true` in the Inspector. WHY: nothing plays until it is active.
- Build states: `idle`, `walk`, `run`, `air_jump`, `air_land`. Connect with the connector tool; transitions are directional.
- Put the **condition** on the transition, not the state: select the connector → `Advance` → `Mode = Auto`, `Condition = <name>`.
- Drive conditions from `_PhysicsProcess` before `MoveAndSlide()`:
  - `anim.Set("parameters/conditions/idle", IsOnFloor() && inputDir == Vector2.Zero);`
  - `anim.Set("parameters/conditions/move", IsOnFloor() && inputDir != Vector2.Zero && currSpeed == walkSpeed);`
  - `anim.Set("parameters/conditions/running", IsOnFloor() && currSpeed == runSpeed);`
  - `anim.Set("parameters/conditions/falling", !IsOnFloor());`
  - `anim.Set("parameters/conditions/landing", IsOnFloor());`
- Cache `anim = GetNode<AnimationTree>("AnimationTree");` in `_Ready()`.
- Set non-looping animations (jump, land) to non-looping in the `AnimationPlayer`; keep idle/walk/run looping.
- Transition graph: `idle↔walk`, `walk↔run`, `idle→air_jump`, `walk→air_jump`, `air_jump→air_land`, `air_land→idle`, `air_land→walk`, `run→walk`, `run→idle`.
- Hover a condition in the AnimationTree Inspector to read its exact path string.

## Checklist
- [ ] `AnimationTree` child added, `Tree Root` set, `Anim Player` assigned
- [ ] `Active` checked
- [ ] Every state reachable and every state has an exit
- [ ] Conditions named consistently between graph and script
- [ ] Jump/land animations set non-looping
- [ ] Tested: idle→walk→run→jump→land→idle with no flicker

## Anti-patterns
- Two-way connectors without conditions — the model flickers between states.
- Forgetting `Active = true` — animations silently never play.
- Managing all animation from script without a tree — becomes unmaintainable as states multiply.
- Leaving jump set to looping — the character loops the takeoff pose.

---
name: jump-and-run-mechanics
topic: Jump state flag and walk/run speed switching
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- Add `private bool jumping = false;` and gate the deceleration block with `if (jumping == false) { velocity.X = Mathf.MoveToward(velocity.X, 0, currSpeed); velocity.Z = Mathf.MoveToward(velocity.Z, 0, currSpeed); }` WHY: otherwise horizontal velocity is killed mid-air and you can only jump straight up.
- On jump: `if (Input.IsActionJustPressed("ui_accept") && IsOnFloor()) { velocity.Y = JumpVelocity; jumping = true; }`
- Reset the flag every frame you are grounded: `if (IsOnFloor()) { jumping = false; }` WHY: forgetting this leaves the player unable to decelerate after landing.
- Replace the single `Speed` constant with `public const float walkSpeed = 4.0f; public const float runSpeed = 8.0f;` plus `private float currSpeed = walkSpeed;`
- Swap every `Speed` reference in velocity and `MoveToward` calls to `currSpeed`.
- Run input: create a `run` action in Project Settings → Input Map, bind Left Shift.
- `if (Input.IsActionPressed("run") && IsOnFloor()) { currSpeed = runSpeed; }`
- `if (Input.IsActionJustReleased("run") && IsOnFloor()) { currSpeed = walkSpeed; }` WHY: `IsActionPressed` alone never restores walk speed on release.
- Use `IsActionPressed` for held state, `IsActionJustPressed` for one-shot, `IsActionJustReleased` for release.

## Checklist
- [ ] `jumping` flag declared, set on jump, cleared on ground
- [ ] Deceleration wrapped in `if (!jumping)`
- [ ] `Speed` fully replaced by `currSpeed`
- [ ] `run` action exists in Input Map and is bound
- [ ] Both press and release handlers present
- [ ] Tested: run → release → speed returns to walk; jump while moving keeps momentum

## Anti-patterns
- Decelerating while airborne — kills air control.
- Never resetting `jumping` — player slides forever after landing.
- Only handling `IsActionPressed` for run — the player stays fast after releasing Shift.
- Hard-coding speed in multiple places instead of one `currSpeed` variable.

---
name: test-area-blockout
topic: Blockout test scene for player movement
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 4 (pp. 91-143)"]
---
## Rules
- Create a separate `TestArea` 3D scene; do not test inside the player scene.
- Add a `CSGBox3D` as ground; set `Size` to `(25, 1, 25)`. WHY: a 25×25 m pad is enough to test walking, running, turning and falling off the edge.
- Tick `Use Collision` on the CSGBox3D. WHY: CSG nodes have no collision by default and the player falls through.
- Drag a texture from the FileSystem panel onto the material slot in the Inspector. WHY: visual contrast makes it easy to judge movement speed and direction.
- Drag `Player.tscn` from FileSystem into the scene tree as an instance.
- Switch the viewport to `Perspective` mode for blockout work.
- Blockout with primitives (cubes, cylinders) before any art pass — this is standard level-design practice for testing scale and flow.

## Checklist
- [ ] `TestArea` scene saved separately
- [ ] CSGBox3D sized 25×1×25
- [ ] `Use Collision` enabled
- [ ] Texture applied
- [ ] `Player.tscn` instanced into the scene
- [ ] Perspective view active
- [ ] Tested: player walks, runs, jumps, and falls off the edge with the land animation

## Anti-patterns
- Testing movement in the player scene itself — no ground, no context.
- Forgetting `Use Collision` — player clips through the floor and you debug the wrong thing.
- Building detailed art before the blockout is validated.

> CHECK: OCR renders the figure caption as "14.13" and garbles the Chinese caption text; the intended figure is the Player.tscn instance inside TestArea.

<!-- 5 Creating Our Game World (pp. 144-204) -->
---
name: importing-3d-assets-gltf
topic: 3D asset import pipeline in Godot 4
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Prefer glTF 2.0 / `.glb` for all 3D models; Godot imports them natively. WHY: it is the officially supported interchange format.
- Do not rely on FBX; Godot does not support it because it is proprietary. If FBX is the only source, convert it first via the official FBX-to-glTF converter. WHY: avoids broken or missing meshes.
- Keep imported models in a dedicated folder (e.g. `world/models/`) rather than the project root. WHY: keeps the FileSystem panel navigable as the project grows.
- Use the Scene panel's **Import** tab to inspect and change per-asset import options, then press **Reimport**. WHY: import settings live on the source file, not on the scene instance.
- Use **Advanced Import Settings** to verify node structure, materials and physics before committing. WHY: catching a bad import early is cheaper than fixing it after level design.
- Imported model nodes are packed by default; right-click → **Editable Children** (or **Make Local**) to expose internal nodes. WHY: you cannot attach collision or scripts to locked internals.
- Godot never overwrites the original model file; all edits are stored as import metadata. WHY: source assets stay reusable across projects.

## Checklist
- [ ] Model is `.glb` / glTF 2.0.
- [ ] Files placed under a project subfolder, not root.
- [ ] Import tab shows the correct asset name when selected.
- [ ] Advanced Import Settings opened once to confirm mesh + material nodes.
- [ ] `Editable Children` enabled on any model you need to modify.

## Anti-patterns
- Editing the original `.glb` in an external tool to fix a Godot-side problem — fix it in import settings instead.
- Assuming an imported model has collision. It has none; only visuals.
- Leaving every model packed and then wondering why the Mesh toolbar button does nothing.

> CHECK: OCR shows both "log_stackLarge2" and "log_stackLarge" — verify the exact asset filename used in the book's example.

---
name: adding-collision-to-meshes
topic: Collision shape creation for imported meshes
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Imported meshes have zero collision by default; add it explicitly or the player walks through everything. WHY: models are visual-only data.
- Two supported workflows:
  1. **At import time** — Advanced Import Settings → select the `MeshInstance3D` node → enable **Physics** → choose Body Type → **Reimport**.
  2. **After placement** — select the `MeshInstance3D` in the scene → viewport toolbar **Mesh** button → **Create Collision Shape…**.
- Body Type decision table (import-time physics):
  | Body Type | Creates | Use for |
  |---|---|---|
  | Static | `StaticBody3D` | walls, ground, props that never move |
  | Dynamic | `RigidBody3D` | vehicles, objects that need real physics |
  | Area | `Area3D` | large scene elements, trigger zones |
- Shape Type decision table:
  | Shape | Cost | Use for |
  |---|---|---|
  | Convex (single/multiple) | low | solid, convex objects, small props |
  | Trimesh (concave) | high, scales with mesh complexity | complex or concave geometry where accuracy matters |
- For small props (mushrooms, statues) use **Create Single Convex Collision Sibling** with placement **Static Body Child**. WHY: cheap and accurate enough for pickups.
- After generating a collision sibling, reparent `CollisionShape3D` under the `StaticBody3D`; otherwise both nodes show warnings and do not recognise each other. WHY: a shape only applies to its parent body.
- Verify collision by walking the player into the object in a test scene.

## Checklist
- [ ] Every solid model the player can touch has a collision shape.
- [ ] Body Type matches whether the object moves.
- [ ] Shape type chosen for performance, not maximum precision by default.
- [ ] `CollisionShape3D` is a child of the body node, not a sibling.
- [ ] Tested in play mode, not just in the editor viewport.

## Anti-patterns
- Using Trimesh collision on every prop — it is the most expensive option and rarely needed.
- Adding a `CollisionShape3D` as a sibling of `StaticBody3D` and ignoring the warnings.
- Forgetting to Reimport after changing import-time physics, then testing stale collision.

---
name: level-design-and-world-environment
topic: Building the first 3D level and environment settings
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Before redesigning, save the old test area: right-click the test root node → **Save Branch as Scene**. WHY: you keep a reusable sandbox for testing new objects and mechanics.
- Build the level by dragging models from the FileSystem panel into the viewport; they are added to the scene tree automatically.
- Viewport transform shortcuts: **Q** select, **W** move, **E** rotate, **R** scale. WHY: far faster than clicking the toolbar.
- Add a `WorldEnvironment` node as a child of the scene root for sky, fog and global illumination. WHY: without it the level looks flat and unlit.
- `WorldEnvironment` shows a warning until an `Environment` resource is assigned: Inspector → Environment → **New Environment**.
- Recommended baseline environment setup:
  1. Background → Mode = **Sky**.
  2. Sky → Sky = **New Sky** → Sky Material = **New ProceduralSkyMaterial**; tune Top/Horizon/Ground colours.
  3. Enable **SSIL** (screen-space indirect lighting) with defaults.
  4. Enable **SDFGI** (signed-distance-field global illumination) with defaults.
- Volumetric Fog (bottom of the Environment list): author used **Density = 0.04**, **Length = 30**. Lower Length = more detail, higher cost.
- For fog only in a specific region: enable Fog in the Environment but set Density = 0, then add a separate Volumetric Fog node locally. WHY: global fog would cover the whole level.

## Checklist
- [ ] Old test area saved as its own scene.
- [ ] `WorldEnvironment` present with a non-empty Environment resource.
- [ ] Background Mode = Sky with a ProceduralSkyMaterial.
- [ ] SSIL and SDFGI enabled.
- [ ] Volumetric Fog density/length tuned and visually checked.

## Anti-patterns
- Leaving `WorldEnvironment` with an empty Environment resource — the node does nothing.
- Cranking Volumetric Fog Density high "for atmosphere" — it hides the level and costs performance.
- Designing the level before collision exists, then discovering the player falls through everything.

---
name: wind-shader-vertex-animation
topic: Shader-based wind sway for foliage
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Godot shaders use their own GLSL-derived language, separate from GDScript and C#; they run on the GPU and control geometry and pixels.
- Two core processor functions: `vertex()` runs per vertex (can set position), `fragment()` runs per pixel.
- `shader_type spatial;` marks a shader as applying to 3D objects. Other types: canvas_item, particles, sky, fog.
- `uniform` declarations become editable parameters in the Inspector. Example: `uniform float wind_strength = 0.02;` appears as "Wind Strength".
- Workflow to add a shader to one surface of a model:
  1. Open the model scene, select the `MeshInstance3D`.
  2. Inspector → Mesh → expand → pick the target Surface (e.g. Surface 0 = leaves).
  3. Material dropdown → **Convert to ShaderMaterial**. Godot preserves existing colour/behaviour and generates equivalent shader code.
  4. Open the **Shader Editor** (bottom of the Output panel) and edit.
- Sway implementation (author's values):
  ```
  VERTEX.x += sin(VERTEX.x + TIME) * wind_strength;
  VERTEX.z += cos(VERTEX.z + TIME) * wind_strength;
  ```
  `TIME` drives the animation; `sin` on X and `cos` on Z gives a more natural, layered sway.
- Apply the shader only to the foliage surface, not the trunk. WHY: trunks should stay rigid.
- Tune `wind_strength` in the Inspector at runtime to find a good value; the author's default is 0.02.

## Checklist
- [ ] Shader applied to the correct surface only (leaves, not bark).
- [ ] `wind_strength` exposed as a uniform, not hard-coded.
- [ ] Both X and Z axes animated for natural motion.
- [ ] Shader file and model scene both saved.
- [ ] Verified in the World scene, not just the model scene.

## Anti-patterns
- Applying the sway shader to the whole model — the trunk bends like rubber.
- Hard-coding the strength constant, making it untweakable per tree.
- Editing the shader without saving, then wondering why the level looks unchanged.

---
name: collision-layers-and-masks
topic: Physics layer and mask configuration
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Definitions: **layers** say what an object *is*; **masks** say what an object *listens for*. Two objects collide only if each one's mask includes the other's layer.
- Default state: every layer and mask is 1, so everything collides with everything. WHY: fine for prototypes, unmanageable past a handful of objects.
- Name layers before using them: Inspector → Layer field → three-dot icon → **Edit Layer Names** → Project Settings → **3D Physics → Layer Names** (not 3D Render). WHY: numeric checkboxes become unreadable fast.
- Author's three-layer scheme:
  | Layer | Name | Contents |
  |---|---|---|
  | 1 | player | the player character |
  | 2 | collectible | pickups |
  | 3 | world | ground, trees, static geometry |
- World geometry: set every colliding `StaticBody3D` to layer **world**.
- Collectible (mushroom) configuration:
  - Collision layer = **collectible** only; uncheck layer 1.
  - Mask = **player** only.
  WHY: the pickup must be detectable by the player but must not collide with other collectibles or the world.
- Use the three-dot checkbox UI to set layers by name instead of memorising indices.

## Checklist
- [ ] Layer names defined in 3D Physics → Layer Names.
- [ ] All world geometry on the world layer.
- [ ] Player on the player layer.
- [ ] Collectibles on the collectible layer with mask = player.
- [ ] Collision tested in play mode after every layer change.

## Anti-patterns
- Leaving everything on layer 1 and mask 1 — collectibles then push each other around.
- Setting a collectible's mask to its own layer, so it never detects the player.
- Editing layer names under 3D Render by mistake; physics ignores them.

---
name: collectible-composition-pattern
topic: Reusable pickup component using composition
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Attach the pickup script to the `StaticBody3D` collision node, not the scene root. WHY: (a) the collision callback fires there, and (b) the node can be reused across different pickup models.
- This is composition: one node = one responsibility, so components are reusable and extensible. It is the core design idea of Godot's node system.
- Pickup script (`CollectibleTrigger`) minimal implementation:
  ```csharp
  public void PickUp() { this.GetParent().QueueFree(); }
  ```
- `GetParent()` is mandatory before `QueueFree()` here. WHY: the script sits on the `StaticBody3D`; freeing it alone would leave the mesh floating. `GetParent()` reaches the model root and frees the whole prop.
- `QueueFree()` marks the node for deletion at end of frame, removing it and all children from the scene tree. It only takes effect at runtime; stopping the game restores the prop.
- Extract the configured `StaticBody3D` + `CollisionShape3D` into its own scene: right-click → **Save Branch as Scene**, named e.g. `PickupComponent.tscn`. WHY: new pickups then need only a mesh plus a dragged-in component.
- To build a new pickup: create a scene from the model (use **New Inherited** from the model's clapperboard icon), add a convex collision sibling, then drag `PickupComponent.tscn` into the viewport and match the parent/child order.
- Group pickups under a dedicated `Node3D` (e.g. `Collectibles`) for scene-tree tidiness.

## Checklist
- [ ] Script attached to the collision body, not the root.
- [ ] `PickUp()` calls `GetParent().QueueFree()`.
- [ ] `PickupComponent.tscn` saved and reused for every pickup type.
- [ ] Node hierarchy of each new pickup matches the reference scene.
- [ ] Each new pickup tested individually in play mode.

## Anti-patterns
- Calling `QueueFree()` directly on the collision body — leaves an invisible mesh behind.
- Copy-pasting the collision node and script per pickup instead of reusing a component scene.
- Attaching the script to the scene root, so the collision callback never fires.

---
name: player-collision-detection-and-pickup
topic: Detecting collisions from CharacterBody3D and triggering pickups
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- The player can touch several objects in one frame, so iterate all slide collisions rather than checking a single one.
- Detection loop pattern:
  ```csharp
  public void CheckForCollectibleCollision() {
      for (int index = 0; index < GetSlideCollisionCount(); index++) {
          KinematicCollision3D collision = GetSlideCollision(index);
          if (collision.GetCollider() is CollectibleTrigger collectible) {
              collectible.PickUp();
          }
      }
  }
  ```
- `GetSlideCollisionCount()` returns the number of contacts from the last `MoveAndSlide()`; `GetSlideCollision(index)` returns the details of one contact.
- Use C#'s `is` pattern matching to test the collider type and bind it in one step. WHY: avoids casts and null checks.
- Call `PickUp()` on the matched component to remove the prop. WHY: the pickup owns its own removal logic — the player only reports the contact.
- Use long, descriptive method names and add `///` XML doc comments above C# methods. WHY: the author's stated preference; the editor auto-generates the comment template.
- Print a debug line (`GD.Print`) while wiring up detection, then keep or remove it deliberately.

## Checklist
- [ ] Loop uses `GetSlideCollisionCount()`, not a hard-coded count.
- [ ] `KinematicCollision3D collision = GetSlideCollision(index);` present inside the loop.
- [ ] Type check uses `is CollectibleTrigger`.
- [ ] `PickUp()` called on the matched instance.
- [ ] Verified via console output and by watching the scene tree at runtime.

## Anti-patterns
- Checking only collision index 0 — pickups are missed when the player touches two things at once.
- Comparing by node name or tag strings instead of by type.
- Calling `QueueFree()` from the player script instead of delegating to the collectible.

---
name: rain-particle-system
topic: GPUParticles3D rain effect
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 5 (pp. 144-204)"]
---
## Rules
- Use `GPUParticles3D` over `CPUParticles3D`; the GPU version exposes more customisation. WHY: better visual control at the same cost for weather effects.
- The gold wireframe box in the viewport is the particle emission AABB; drag its handles to resize.
- Core properties: **Emitting** (on/off), **Amount** (particles per frame), **Sub Emitter** (nested effects), **Time** (lifetime), **Collision**, **Drawing** (AABB), **Trails**, **Process Material**, **Draw Passes**.
- Configure **Draw Passes first** so you can see shape changes live.
- Rain drop mesh (author's values):
  - Pass 1 → **New RibbonTrailMesh**.
  - Section Length = **0.02** (shortens the ribbon into a drop).
  - Sections = **3** (down from the default 5).
  - Curve: Max Value = **0.1**, three control points from 0 → 0.1 → 0, giving a teardrop profile.
- Process Material (author's values):
  - **New ParticleProcessMaterial**.
  - Spawn → Emission Shape = **Box** (default Point spawns all particles at one spot).
  - Emission Box Extents = **X 50, Y 10, Z 50** — sized to cover the level, positioned above the ground.
  - Direction Y = **-3** (negative Y makes rain fall; a small X value tilts it for wind).
  - Initial Velocity: Min **100**, Max **150** (higher = heavier rain).
  - Gravity default Y = -9.8.
  - Display → Color = **#D5E6F2**.
  - Collision → Mode = **Hide on Contact** so drops vanish on impact.
- Scale Amount to the desired intensity: a few hundred for light rain, thousands for a downpour.

## Checklist
- [ ] `GPUParticles3D` added as a child of the scene root.
- [ ] Amount raised from the default 8.
- [ ] Draw Passes configured before Process Material.
- [ ] Emission Shape = Box with extents covering the play area.
- [ ] Direction Y negative; velocity range set.
- [ ] Colour and Hide-on-Contact collision set.
- [ ] Effect checked in play mode with fog enabled.

## Anti-patterns
- Leaving Emission Shape at Point — all drops spawn from one pixel.
- Forgetting to set Direction Y negative, so rain streaks sideways.
- Using very high Amount without checking frame cost.
- Skipping the Curve on the ribbon mesh, leaving square particles.

<!-- 6 Developing and Managing the User Interface (pp. 205-271) -->
---
name: godot-control-nodes-and-anchors
topic: Godot UI Control nodes and anchoring
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Create UI scenes with the "User Interface" scene template; the root node is a `Control` node and the viewport switches to 2D with the origin at the top-left corner.
- All UI nodes (Button, Label, Slider, Container, Panel, etc.) derive from `Control` and appear green in the node list.
- Use anchors (four green corner markers) to define how a Control scales and repositions across resolutions. Anchors are the primary mechanism for multi-platform UI adaptation.
- Use the eight bound points on a Control's edge to resize it; drag inside the node to move it.
- For full-screen overlays (main menu, pause screen), set the anchor preset to "Full Rect" or "Set to Current Ratio" so the node fills the viewport.
- Prefer anchor presets over manually dragging anchors when the target is a standard layout (full rect, centered, etc.).
- Set `Label` text via the `Text` property; set font size via `Label Settings` → `Font` → `Size`. Default font size is 16 px — too small for readable UI; use 32 px or larger for headings.
- Keep UI elements inside the light-blue screen boundary lines in the editor; anything outside will not be visible at runtime.
- Name UI nodes by function (e.g. `MainMenu`, `Play`, `Settings`, `CloseButton`) to make debugging and scene navigation easier.

## Checklist
- [ ] New UI scene created from the User Interface template.
- [ ] Root `Control` renamed to something descriptive.
- [ ] Anchors set (Full Rect / Set to Current Ratio) for any element that must fill or scale with the screen.
- [ ] Font sizes raised above the 16 px default where readability matters.
- [ ] All UI elements verified inside the blue screen bounds.

## Anti-patterns
- Relying on `Transform` size/position alone for full-screen UI: it only resizes the node itself and does not adapt to window resizing. Use anchors instead.
- Leaving the default 16 px font size on labels intended for menus or headings.
- Placing UI outside the blue viewport boundary and expecting it to render.

> CHECK: OCR shows "标签节点有四个锚点" (Label has four anchors) — verify whether the author means four corner anchors or the standard anchor points; the exact count is not critical to the rule.
---
name: godot-ui-theme-editor
topic: Godot UI Theme resource and Theme Editor
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Create a Theme by selecting a `Control` node, expanding the `Theme` property in the Inspector, and choosing "New Theme". The Theme Editor panel appears in the bottom dock.
- In the Theme Editor, click `+` next to the Type dropdown, search for a node type (e.g. `button`), and choose "Add Type" to start styling that type.
- Keep "Show Default" enabled to see all configurable states for the selected type.
- Theme Editor property tabs and their use:
  - **Color** — font/icon colors per state (hover, click, disabled).
  - **Constants** — type-specific numeric parameters (outline size, spacing).
  - **Font** — font file for text.
  - **Font Size** — font size for all variants of the type.
  - **Icons** — textures overlaid on the type.
  - **StyleBoxes** — main tab for visual appearance per state (normal, pressed, hover, focus, disabled).
  - **Custom Settings** — create type variants (e.g. a differently colored Button).
- StyleBox types:
  - `StyleBoxEmpty` — renders nothing.
  - `StyleBoxTexture` — uses a texture.
  - `StyleBoxFlat` — fully customizable via properties (color, border, corner radius, shadow) with no texture.
  - `StyleBoxLine` — a single line; used for sliders and separators.
- For a flat button, typical `StyleBoxFlat` values: Border Width 3 px on all sides, Border Color a contrasting hex (e.g. `#163660`), Corner Radius 5 px on all corners, Expand Margins 3 px left/right, Shadow Size 2 px, Shadow Offset 2 px on X and Y.
- StyleBox resources are edited in the Inspector, not in the Theme Editor. Use the back arrow at the top-right of the Inspector to return to the Theme Editor.
- Styles set on a base type propagate to derived types: styling `Button` also styles `CheckButton`, `CheckBox`, and other Button-derived types.
- Save the Theme as a `.tres` file (e.g. `UI_Theme.tres`) via the Theme property dropdown → "Save As…", then load it into any `Control` root via the Theme property → "Load".
- Once a Theme is assigned to a scene root, all child Controls of matching types automatically inherit the styles — no per-node styling needed.
- After saving, the Theme property in the Inspector exposes sub-properties per type (Button, CheckBox, Panel, …); these can be tweaked directly without opening the Theme Editor.
- Only add a type to the Theme if it is used in multiple places; one-off nodes (e.g. a single Panel) do not need a Theme entry.

## Checklist
- [ ] Theme resource created and saved as `.tres`.
- [ ] Base types styled (Button, HSlider, etc.) before variants.
- [ ] Theme assigned to every UI scene root that should share the look.
- [ ] StyleBox states configured for at least normal; hover/pressed/disabled as needed.
- [ ] Verified derived types (CheckBox, CheckButton) inherit the base style.

## Anti-patterns
- Styling each Button node individually instead of via a Theme — breaks consistency and multiplies work.
- Forgetting to save the Theme as a separate resource; the styles stay locked to one scene.
- Adding every node type to the Theme "just in case" — bloats the resource.

> CHECK: OCR shows "Border Width 3 px" and "Corner Radius 5 px" as the author's chosen values; these are examples, not universal defaults. Treat as starting points.
---
name: godot-main-menu-scene
topic: Building and embedding the main menu
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Build the main menu as its own UI scene (`MainMenu.tscn`) with a `Control` root, then embed it into the world scene as an instanced child.
- Use a `Panel` node as the background for the menu's text and buttons; size it via the eight bound points and anchor it (Full Rect or Set to Current Ratio) so it scales with the window.
- Use `VBoxContainer` to stack buttons vertically; use `HBoxContainer` for horizontal rows. Containers auto-size and auto-space their children.
- Anchor the container to its parent (Panel) using the anchor preset "Set to Current Ratio" rather than dragging anchors manually.
- Add the first `Button` as a child of the container, set its `Text`, then duplicate it (Ctrl+D) for the remaining buttons and rename each (`Play`, `Settings`, `Credits`, `Quit`).
- To embed the menu in the world: open `World.tscn`, add a `Camera3D` named `MenuCamera` as a direct child of the root, position it high above the level for a top-down view, and enable its `Current` property.
- Instance `MainMenu.tscn` into `World.tscn` via the "Instantiate Child Scene" (chain icon) button or by dragging from the FileSystem panel.
- Parent the `MainMenu` instance under `MenuCamera` in the node tree for tidy organization.
- Instanced scenes show a highlighted icon next to their node name in the Scene panel (nested scenes).

## Checklist
- [ ] `MainMenu.tscn` saved with `Control` root and Theme assigned.
- [ ] `Panel` background sized and anchored to full rect.
- [ ] `VBoxContainer` anchored inside the Panel.
- [ ] Buttons created, renamed, and text set.
- [ ] `MenuCamera` added to `World.tscn`, positioned, and set `Current`.
- [ ] `MainMenu.tscn` instanced into `World.tscn` and parented under `MenuCamera`.

## Anti-patterns
- Building the menu directly inside `World.tscn` instead of as a separate scene — harder to reuse and test.
- Forgetting to set `MenuCamera.Current` — the menu camera will not activate.
- Leaving the menu camera at ground level — the menu background becomes a flat, uninteresting view.
---
name: godot-menu-button-signals-and-transition
topic: Wiring menu buttons and the play transition
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Attach a script to the menu root (`MainMenu.cs`) before connecting signals; Godot auto-generates receiver methods in the attached script.
- Connect buttons via the Node tab → `button_down()` signal → Connect; rename the receiver method to something descriptive (`ExitGame`, `OnPlayClicked`, `OnSettingsClicked`).
- Quit button: `GetTree().Quit();` — `GetTree()` returns the active scene tree (the World scene, since MainMenu is nested inside it).
- Play transition requires coordinated changes across `MainMenu.cs` and `World.cs`:
  - `MainMenu.OnPlayClicked()`: play the transition animation, then call `GetOwner<World>().PlayerStart();`
  - `World.PlayerStart()`: set `player.ProcessMode = ProcessModeEnum.Always;` and `Input.MouseMode = Input.MouseModeEnum.Captured;`
- On menu start (`World._Ready()`), if `menuCamera.Current` is true:
  - `Input.MouseMode = Input.MouseModeEnum.Visible;` — restore the cursor for UI interaction.
  - `player.ProcessMode = ProcessModeEnum.Disabled;` — freeze the player and all its children while the menu is up.
- `ProcessModeEnum.Disabled` stops the node and all descendants; `Always` re-enables them; `Inherit` is the default.
- Build the menu slide-out with an `AnimationPlayer` node on the menu scene:
  - Create a new animation named `MenuTransition`.
  - Set the duration to 0.5 s for a quick transition (default is 1 s).
  - Click the keyframe icon next to the `Position` property of the Panel to add a track at time 0.
  - Move the timeline to 0.5 s, move the Panel off-screen (e.g. X 64, Y 692 to slide down), and click the keyframe icon again.
  - Play the animation from the start to verify.
- Trigger the animation from code: declare `private AnimationPlayer animPlayer;`, assign it in `_Ready()` via `GetNode<AnimationPlayer>("AnimationPlayer")`, and call `animPlayer.Play("MenuTransition");` in `OnPlayClicked()`.
- `GetOwner<World>()` returns the owner of the current node — for a nested MainMenu scene, that is the World root.

## Checklist
- [ ] Script attached to menu root before connecting signals.
- [ ] Quit, Play, Settings buttons each connected with a named receiver method.
- [ ] `World.cs` declares `menuCamera` and initializes it in `_Ready()`.
- [ ] Menu start disables player processing and shows the mouse.
- [ ] `PlayerStart()` re-enables player processing and captures the mouse.
- [ ] `AnimationPlayer` with `MenuTransition` (0.5 s) created and keyframed.
- [ ] `animPlayer.Play("MenuTransition")` called on Play.

## Anti-patterns
- Forgetting to disable player `ProcessMode` on menu start — the player can still move behind the menu.
- Forgetting to restore `MouseMode` to `Captured` after Play — the cursor stays visible during gameplay.
- Hardcoding the animation duration at 1 s — feels sluggish for a menu transition.
- Connecting signals before attaching the script — no receiver method is generated.
---
name: godot-settings-menu-and-sliders
topic: Settings scene, volume sliders, and close button
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Create `Settings.tscn` from the User Interface template, rename the root to `Settings`, and assign `UI_Theme.tres` to its Theme property so all child Controls inherit styles.
- Add a `ColorRect` as the settings background: set its `Color` to a contrasting hex (e.g. `#ABD4F6`), set `Size` to fill the screen, and set the anchor preset to "Full Rect" / "Set to Current Ratio".
- Add a `Label` named `Title` with text "Settings" and font size 75 px; position it at the top (e.g. Size 384×103, Position 362,55).
- Add an `HSlider` named `MusicSlider` as a child of the Settings panel; size ~482×113, position ~454,257.
- Duplicate the Title label to create `MusicLabel`; position it to the left of the slider (e.g. 104,254) and anchor it with "Set to Current Ratio".
- Multi-select `MusicLabel` + `MusicSlider` (Shift+click) and duplicate with Ctrl+D to create `SFXSlider` and `SFXLabel`; rename and reposition (slider at 454,400; label at 104,400).
- Style the `HSlider` in the Theme Editor by adding the `HSlider` type, then configuring:
  - `grabber_area` → new `StyleBoxFlat`, BG Color `#003E65`, Corner Radius 10 px on all corners.
  - `grabber_area_highlight` → new `StyleBoxFlat`, BG Color `#CB8B59`, Corner Radius 10 px on all corners.
  - `slider` → `StyleBoxLine`, Color matching `grabber_area`, Grow Begin/End −10 px, Thickness 12 px.
  - `grabber` (and `grabber_disabled`, `grabber_highlight`) → assign a circular texture (e.g. `red_circle.png` from Kenney UI Pack).
- Keep Alpha at 255 when setting colors unless transparency is intentional.
- Add a `CloseButton` as a child of the `ColorRect`; size ~70×77, position ~996,55; set `Text` to "X" (or assign an icon).
- If using an icon on the close button: enable `Flat`, set `Icon Alignment` to Center, enable `Expand Icon`. Note that some Theme Button properties (e.g. color feedback) do not apply when `Flat` is on; the hover scale effect still works.
- Connect `CloseButton.button_down()` to a receiver method `OnSettingsClose` in `Settings.cs`; body: `this.QueueFree();` — destroys the settings scene at end of frame, returning to the main menu.

## Checklist
- [ ] `Settings.tscn` root has `UI_Theme.tres` assigned.
- [ ] `ColorRect` fills the screen and is anchored.
- [ ] Title label sized and positioned.
- [ ] Music and SFX sliders + labels created, positioned, and anchored.
- [ ] `HSlider` type added to Theme with grabber_area, grabber_area_highlight, slider, and grabber styles.
- [ ] `CloseButton` added, styled, and connected to `OnSettingsClose`.
- [ ] `OnSettingsClose` calls `QueueFree()`.

## Anti-patterns
- Forgetting to assign the Theme to the Settings root — sliders and buttons use default Godot styling.
- Using the default slider grabber texture — it is small and semi-transparent; replace it with a proper circular texture.
- Leaving the settings scene in the tree after closing — always `QueueFree()` to keep the scene clean.
- Expecting all Button Theme properties to apply when `Flat` is enabled — color feedback is suppressed.
---
name: godot-settings-navigation
topic: Opening and closing the settings scene from the main menu
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 6 (pp. 205-271)"]
---
## Rules
- Open the settings scene from the main menu by instantiating it in code, not by dragging it into the scene tree:
  - Declare `Node settingsScene = ResourceLoader.Load<PackedScene>("res://user_interface/Settings.tscn").Instantiate();`
  - Then `AddChild(settingsScene);` to attach it as a child of the menu root.
- `ResourceLoader.Load<PackedScene>(path).Instantiate()` loads and instantiates a packed scene; the resource is cached for later reuse.
- If the scene path changes, update the string in the `Load` call — it is a hardcoded path.
- `AddChild()` attaches the instantiated node to the calling node; since the script is on the menu root, the settings scene becomes a child of `MainMenu`.
- Close the settings scene with `this.QueueFree();` in the close button's receiver method — the node is destroyed at end of frame, revealing the main menu underneath.
- Instantiating and destroying the settings scene on demand (rather than keeping it in the tree) keeps the scene graph clean and independent.

## Checklist
- [ ] `OnSettingsClicked` in `MainMenu.cs` loads and instantiates `Settings.tscn`.
- [ ] `AddChild(settingsScene)` called after instantiation.
- [ ] `OnSettingsClose` in `Settings.cs` calls `QueueFree()`.
- [ ] Scene path in `ResourceLoader.Load` matches the actual file location.
- [ ] Verified: clicking Settings opens the panel; clicking X returns to the menu.

## Anti-patterns
- Adding `Settings.tscn` as a permanent child of `MainMenu.tscn` in the editor — it would always be visible and waste resources.
- Forgetting `AddChild()` after `Instantiate()` — the node exists but is not in the tree and will not render.
- Using a stale scene path after moving the file — the load fails silently or throws.
- Calling `Free()` instead of `QueueFree()` — can crash if the node is still processing.

<!-- 7 Adding Sound Effects and Music (pp. 272-305) -->
---
name: godot-audio-nodes
topic: Godot 4 audio node selection
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- Use `AudioStreamPlayer` for non-positional audio: UI sounds, menu transitions, and background music that should play at constant volume everywhere. WHY: it ignores listener position, so volume never attenuates.
- Use `AudioStreamPlayer2D` when sound must attenuate with distance from the listener in 2D space (e.g. UI elements on the left/right of the screen panning to the matching speaker). WHY: it computes panning/attenuation from position.
- Use `AudioStreamPlayer3D` for positional sound in 3D scenes (e.g. a fountain whose volume changes as the player walks away). WHY: distance-based attenuation in 3D space.
- Default listener when no `AudioListener2D` exists is the screen center; `AudioListener2D` can only be placed at screen corners/edges. WHY: 2D audio is screen-space.
- Default listener when no `AudioListener3D` exists is the `Camera3D` node. WHY: 3D audio is world-space and follows the camera.
- Only one AudioListener may be active at a time, like Camera nodes. WHY: a single listening point is required for consistent mixing.
- Supported audio file formats are only `.wav`, `.ogg`, `.mp3`. WHY: Godot's importer rejects other formats.
- For a 3D game, still use plain `AudioStreamPlayer` for background music if you want it to play uniformly across the whole scene. WHY: positional nodes would make music fade with distance.
## Checklist
- Decide per sound: positional (2D/3D) or global (plain player)?
- Confirm the listener setup matches the scene dimensionality.
- Verify the imported file extension is one of the three supported formats.
- Name the node after its purpose (e.g. `MainMenuTransition`, `WorldMusic`) so `GetNode<T>()` lookups stay readable.
## Anti-patterns
- Using `AudioStreamPlayer2D`/`3D` for menu or UI sounds — volume will vary unexpectedly with position.
- Assuming a listener exists and is positioned where you want; without one, 2D falls back to screen center and 3D to the camera.
- Importing `.flac`, `.aac`, or other formats and expecting them to play.

---
name: godot-audio-buses
topic: Audio bus layout and effects
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- Open the bus panel from the Audio tab at the bottom of the Output panel. WHY: that is where the AudioBusLayout resource is edited.
- Create separate buses for logical groups — at minimum `Music` and `SFX`. WHY: lets you set independent volume and effects per group.
- Every bus routes into the `Master` bus; Master's output is fixed and cannot be reassigned. WHY: Master is the final mix destination.
- Each bus exposes: name, Solo (S), Mute (M), Bypass (B), a VU meter, an effects list, and an output target. WHY: these are the controls you use to shape the mix.
- Bypass skips all effects on that bus; Mute silences it; Solo plays only soloed buses. WHY: useful for isolating a group while debugging.
- Add effects (distortion, amplify, reverb, etc.) via the "Add Effect" dropdown under the bus volume; each effect has its own inspector properties (e.g. distortion has a Mode such as LoFi). WHY: effects are per-bus, not per-stream.
- The bus layout is a resource: you can load the default layout, save the current one, or create a new layout from the top-right buttons. WHY: layouts are reusable and versionable.
- Bus index order in the layout resource determines the numeric index returned by `AudioServer.GetBusIndex(name)`. WHY: code addresses buses by index, so order matters.
## Checklist
- Create Music and SFX buses before assigning any stream.
- Assign each `AudioStreamPlayer`'s `Bus` property to the correct bus.
- Save the bus layout resource after edits.
- Verify bus indices at runtime with a debug print if code depends on them.
## Anti-patterns
- Leaving everything on Master — you lose independent music/SFX volume control.
- Hardcoding bus indices in code instead of resolving them by name via `GetBusIndex`.
- Forgetting to save the layout, so runtime and editor disagree.

---
name: audio-stream-player-properties
topic: AudioStreamPlayer configuration
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- `Stream`: the loaded audio clip — set via the dropdown (Load) or by dragging the file onto the property. WHY: without a stream nothing plays.
- `Volume Db`: per-stream volume that overrides the bus default. WHY: fine-tune individual clips without touching the bus.
- `Pitch Scale`: multiplier on the sample rate; changes pitch and tempo together. WHY: quick variation without re-authoring audio.
- `Playing`: read/write flag for whether the stream is currently playing.
- `Autoplay`: plays the stream as soon as the scene loads. WHY: convenient for background music that should start immediately.
- `Stream Paused`: true pauses, false resumes.
- `Mix Target`: which channels the audio targets — set per speaker/headphone/surround setup.
- `Max Polyphony`: number of simultaneous voices; when exceeded, the oldest voices are cut off. WHY: prevents voice explosion on rapid repeated sounds.
- `Bus`: selects which bus the stream routes through (e.g. set to `SFX` or `Music`). WHY: this is how per-group volume control takes effect.
- For a simple UI/menu sound you typically only change `Stream` and `Bus`; leave the rest at defaults. WHY: minimal config avoids surprises.
## Checklist
- Load the clip into `Stream`.
- Set `Bus` to the intended group.
- Enable `Autoplay` only for music that must start on scene load.
- Raise `Max Polyphony` for sounds that can overlap (e.g. rapid footsteps).
## Anti-patterns
- Leaving `Bus` on Master when the project has dedicated Music/SFX buses.
- Setting `Autoplay` on a one-shot UI sound — it will fire on scene load instead of on the button press.
- Assuming `Pitch Scale` changes pitch only; it also changes tempo.

---
name: triggering-audio-from-code
topic: Playing sounds and music from C#
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- Declare a field of type `AudioStreamPlayer` and assign it in `_Ready()` with `GetNode<AudioStreamPlayer>("NodeName")`. WHY: the string must exactly match the node name in the scene tree.
- Call `audioPlayer.Play()` to start the stream loaded in that node. WHY: this is the standard trigger for one-shot sounds.
- Trigger UI sounds inside the button's signal handler (e.g. before hiding the menu). WHY: keeps sound tied to the interaction.
- To play music after a menu closes, call a dedicated method on the owning scene (e.g. `TriggerWorldMusic()`) rather than doing it in `_Process`. WHY: one-shot logic in `_Process` runs every frame.
- Access the parent scene from a nested scene with `GetOwner<World>()`, then call its public methods. WHY: `GetOwner` returns the scene root that owns the nested node.
- Add a `GD.Print(...)` inside one-shot trigger methods while testing to confirm they fire exactly once. WHY: catches accidental repeated calls.
- Move one-time setup (camera switch, mouse capture, process mode) out of `_Process` into the trigger method. WHY: `_Process` is for per-frame work only.
## Checklist
- Field declared, assigned in `_Ready()` with the exact node name.
- `Play()` called from the correct signal handler.
- One-shot logic lives in a named method, not `_Process`.
- Debug print confirms single execution.
## Anti-patterns
- Typo in the `GetNode` string — silently returns null and playback never happens.
- Leaving one-time transitions inside `_Process`, causing them to re-run every frame.
- Calling `Play()` on a node whose `Stream` is unset.

---
name: syncing-audio-with-animation
topic: Async delay to sync sound with UI animation
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- If you hide a node immediately after starting an animation, the animation is skipped. WHY: visibility is set before the animation has time to run.
- Delay the follow-up action with an `async` method using `await Task.Delay(TimeSpan.FromSeconds(1))`. WHY: `await` suspends the method until the delay completes, then continues.
- Add `using System.Threading.Tasks;` to access `Task`. WHY: `Task` lives in that namespace.
- Choose the delay to match the animation length (the example uses 1 second because the menu animation is under 1 second). WHY: too short truncates the animation, too long feels laggy.
- Alternative without `Task`: `await ToSignal(GetTree().CreateTimer(1f), SceneTreeTimer.SignalName.Timeout);`. WHY: uses Godot's own timer/signal system instead of .NET.
- Mark the method `async void` when it is invoked as a fire-and-forget signal handler. WHY: signal handlers cannot be awaited by the caller.
## Checklist
- `using System.Threading.Tasks;` present.
- Animation started, sound started, then `await` delay, then visibility change.
- Delay value >= animation duration.
- `this.Visible = false` removed from the synchronous handler and placed after the `await`.
## Anti-patterns
- Setting `Visible = false` in the same synchronous block as `animPlayer.Play(...)`.
- Guessing a delay shorter than the animation.
- Using `Thread.Sleep` — it blocks the main thread and freezes the game.

> CHECK: The chapter shows `async void HideMenu()`; confirm whether the author also mentions returning `Task` for testability — OCR is unclear.

---
name: volume-slider-to-bus
topic: Wiring UI sliders to audio bus volume
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 7 (pp. 272-305)"]
---
## Rules
- Configure each volume slider with: `Tick Count = 1`, `Max Value = 1`, `Step = 0.05`, `Value = 1` (start at full volume). WHY: a 0–1 range with 5% steps gives smooth, consistent control.
- Use identical slider settings for Music and SFX sliders. WHY: consistent feel across controls.
- Connect the slider's `value_changed(value: float)` signal to a handler named for its purpose (e.g. `ChangeMusicVolume`, `ChangeSFXVolume`). WHY: descriptive names beat auto-generated `_on_..._value_changed`.
- Resolve the bus index once in `_Ready()`: `musicBus = AudioServer.GetBusIndex("Music");`. WHY: avoids repeated string lookups and keeps the name in one place.
- Apply volume with `AudioServer.SetBusVolumeDb(busIndex, Mathf.LinearToDb(value));`. WHY: slider values are linear 0–1 but the audio API expects decibels.
- Always wrap the slider value in `Mathf.LinearToDb(...)` before passing it to `SetBusVolumeDb`. WHY: passing a raw 0–1 value produces near-silence or wrong loudness.
- Verify the bus index with a debug print (the example expects `1` for Music). WHY: index depends on layout order.
## Checklist
- Slider properties set (Tick Count 1, Max 1, Step 0.05, Value 1).
- Signal connected to the correctly named handler.
- Bus index field declared and assigned in `_Ready()`.
- `Mathf.LinearToDb` applied in the handler.
- Test: drag slider to minimum, exit settings, trigger the sound — it should be silent.
## Anti-patterns
- Passing the raw slider value to `SetBusVolumeDb` without `LinearToDb`.
- Hardcoding the bus index instead of using `GetBusIndex`.
- Different slider ranges for Music and SFX, causing inconsistent UX.
- Forgetting to set the player's `Bus` property, so the slider appears to do nothing.

<!-- 8 Adding Navigation and Pathfinding (pp. 306-336) -->
---
name: godot-navigation-nodes-overview
topic: Godot navigation node types
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Use `NavigationRegion3D` to host a `NavigationMesh` resource; it defines the walkable area for 3D agents.
- Use `NavigationAgent3D` on the moving entity (NPC) to compute paths and handle avoidance. It requires a NavigationRegion3D + NavigationMesh to function.
- Use `NavigationLink` to connect two otherwise disconnected points on the NavMesh (e.g. jump gaps, doors).
- Use `NavigationObstacle` to add dynamic/static blockers that reroute agents without rebaking.
- Use `Marker3D` nodes as patrol waypoints; they are editor-only gizmos with no runtime cost.
- 2D and 3D navigation nodes share the same logic; only the plane dimension differs. Pick the matching variant.
- For custom A* without a NavMesh, use `Astar3D`; for server-level path queries, use `NavigationServer`.
- WHY: Each node has one job — region defines space, agent consumes it, links/obstacles patch it. Mixing roles causes silent path failures.

## Checklist
- [ ] NavMesh baked and visible as highlighted area in viewport
- [ ] Agent node is a child of the moving CharacterBody3D
- [ ] Avoidance Enabled = true if NPCs must dodge each other
- [ ] Debug > Enable checked while testing to visualize path

## Anti-patterns
- Expecting the NavMesh to appear without baking — it stays empty until you bake.
- Placing the agent on a separate branch of the tree from the body it moves.

> CHECK: OCR lists NavigationMesh as "not in the node list" — it is a Resource, not a Node. Confirm wording matches your Godot version.

---
name: baking-navigation-mesh
topic: Baking a NavigationMesh
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Add `NavigationRegion3D` to the world scene, then in Inspector set Navigation Mesh → New NavigationMesh.
- All geometry that should be walkable OR should block agents must be a child of the NavigationRegion3D node.
- Bake by selecting the NavigationRegion3D and clicking "Bake NavigationMesh" above the viewport.
- Re-bake every time you add or remove child geometry under the region. WHY: the baked mesh is a precomputed snapshot; it does not track scene changes.
- Baking precomputes data so it is not recalculated at runtime — same principle as lightmap/texture baking.
- Organize the scene tree by category (trees, ground, terrain as separate Node3D parents) before baking; keeps the region's children manageable.

## Checklist
- [ ] Region node selected before baking
- [ ] All obstacles (trees, props) parented under the region
- [ ] Viewport shows highlighted walkable area after bake
- [ ] Re-baked after any geometry change

## Anti-patterns
- Baking with geometry outside the region — those objects are invisible to navigation.
- Forgetting to re-bake after moving a tree; agents will walk through it.

---
name: npc-character-body-setup
topic: Building a navigable NPC scene
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Root the NPC scene at `CharacterBody3D` (same pattern as the player).
- Add `CollisionShape3D` with a `CapsuleShape3D`; add `MeshInstance3D` with a `CapsuleMesh` as a child for a quick prototype.
- Add `NavigationAgent3D` as a child of the CharacterBody3D.
- In the agent's Avoidance section, set Avoidance Enabled = true so the agent steers around obstacles.
- Assign a dedicated collision layer for NPCs (e.g. Layer 4 named `npc`). Set Layer = 4 (what it is) and Mask = 3 (what it collides with).
- Capsule-only NPCs are the recommended prototype when no animation exists or when testing in first-person.

## Checklist
- [ ] CharacterBody3D root
- [ ] CapsuleShape3D collision + CapsuleMesh visual
- [ ] NavigationAgent3D child, avoidance on
- [ ] Layer named and assigned; Mask set to scene layer
- [ ] Scene renamed to something specific (e.g. ForestDweller.tscn), not "NPC.tscn"

## Anti-patterns
- Leaving the default generic scene name — it becomes ambiguous once you add variants.
- Confusing Layer (self identity) with Mask (collision targets).

---
name: patrol-waypoints-and-random-selection
topic: Waypoint patrol with random target selection
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Add four `Marker3D` children under the NPC (Patrol1..Patrol4), positioned on the NavMesh.
- Store waypoints as `List<Vector3>` populated in `_Ready()` via `GetNode<Marker3D>("...").GlobalPosition`.
- Keep a `currPatrolPoint` Vector3 and an `int patrolNum` index; never pick the same index twice in a row or the NPC stalls.
- Random selection loop: save `prevPatrolNum = patrolNum`, then `while (prevPatrolNum == patrolNum) patrolNum = rInt.Next(0, 4);`. WHY: `Random.Next(min, max)` is exclusive of max, so 4 covers indices 0–3.
- Add `using System;` for the `Random` class.
- Expose a `public bool moveNPC = true` toggle to pause NPCs (e.g. while the main menu is open).
- Keep speed as `private float speed = 1.5f` unless designers need runtime tuning; then make it `[Export]`.

## Checklist
- [ ] 4 Marker3D children placed on the NavMesh
- [ ] Waypoints added to list in `_Ready()`
- [ ] Random loop excludes current index
- [ ] `Next(0, N)` upper bound equals waypoint count

## Anti-patterns
- `Next(0, 3)` for four waypoints — index 3 is never reached.
- Selecting the current waypoint again — NPC freezes in place.

---
name: npc-movement-physics-process
topic: Driving an NPC with NavigationAgent3D
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Cache the agent in `_Ready()`: `navAgent = GetNode<NavigationAgent3D>("NavigationAgent3D");`.
- Do all path queries in `_PhysicsProcess`, not `_Process`. WHY: `GetNextPathPosition()` must run in the physics frame to keep agent path logic in sync.
- Movement per physics frame:
  1. `Vector3 currLocation = GlobalTransform.Origin;`
  2. `Vector3 nextLocation = navAgent.GetNextPathPosition();`
  3. `Vector3 newVelocity = (nextLocation - currLocation).Normalized() * speed;`
  4. `this.Velocity = newVelocity;`
  5. `MoveAndSlide();`
- Provide `public void SetTarget(Vector3 targetPosition)` that assigns `navAgent.TargetPosition = targetPosition;`.
- Connect the agent's `target_reached` signal to a handler (e.g. `OnNavAgentTargetReached`).
- In the handler, pause with `await ToSignal(GetTree().CreateTimer(3f), SceneTreeTimer.SignalName.Timeout);` before picking the next waypoint. Mark the handler `async void`.
- Get the world root with `GetOwner<World>()` to call back into world-level patrol logic.

## Checklist
- [ ] Agent cached in `_Ready()`
- [ ] All movement in `_PhysicsProcess`
- [ ] Velocity normalized before scaling by speed
- [ ] `MoveAndSlide()` called after setting Velocity
- [ ] `target_reached` connected and handler marked async

## Anti-patterns
- Calling `GetNextPathPosition()` in `_Process` — path desync.
- Forgetting `MoveAndSlide()` — velocity is set but the body never moves.
- Skipping normalization — diagonal targets move faster than straight ones.

---
name: godot-groups-for-npc-management
topic: Using Godot groups to batch-manage NPCs
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- Add NPCs to a group via Inspector → Node tab → Groups → enter name (e.g. `npc`) → Add.
- A grouped node shows a square-with-dot icon in the scene tree.
- Broadcast to all members with `GetTree().CallGroup("npc", "SetTarget", patrolPoints[patrolNum]);` — no manual iteration needed.
- `CallGroup` arguments: group name, method name, then the arguments passed to that method.
- Call the broadcast function both after choosing a new waypoint and at the end of `PlayerStart()` so NPCs begin patrolling immediately.
- WHY: groups scale to N NPCs with one line; per-instance loops do not.

## Checklist
- [ ] Group name matches the string used in `CallGroup`
- [ ] Every NPC instance is in the group
- [ ] Target method is public and matches the signature passed
- [ ] Broadcast triggered on start and on waypoint change

## Anti-patterns
- Typo between group name and `CallGroup` string — silent no-op.
- Assuming all NPCs should share the same waypoint; add per-NPC logic if overlap looks wrong.

---
name: navigation-debug-visualization
topic: Debugging navigation paths
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 8 (pp. 306-336)"]
---
## Rules
- On the NavigationAgent3D, open Debug → Enable to draw the current path in the viewport.
- Set a high-contrast path color (e.g. #CD0243) so it reads against the level background.
- Increase path point size (e.g. 50 px) to make waypoints visible.
- Large dots = path points; connecting lines = the route from current position to target.
- Toggle any node's visibility with the eye icon in the scene tree to declutter (e.g. hide rain particles while inspecting the NavMesh).

## Checklist
- [ ] Debug enabled on the agent
- [ ] Path color contrasts with scene
- [ ] Point size readable at gameplay zoom
- [ ] Debug disabled before shipping

## Anti-patterns
- Leaving debug drawing on in a release build — visual noise and minor cost.
- Debugging path issues without first confirming the NavMesh is baked.

<!-- 9 Setting Up Lighting in Godot (pp. 338-364) -->
---
name: godot-lighting-nodes-overview
topic: Godot 4 lighting nodes and renderer limits
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 9 (pp. 338-364)"]
---
## Rules
- Use the Forward+ renderer for 3D projects targeting low-end hardware; it is the author's chosen renderer and supports the most lights per scene. WHY: Forward+ gives the best performance/feature balance for modest devices.
- Pick the light node by use case:
  | Node | Shape | Typical use |
  |---|---|---|
  | DirectionalLight3D | Parallel rays, infinite distance | Sun / moon, outdoor key light |
  | OmniLight3D | Spherical, radius-based | Indoor rooms, lanterns, street lamps, candles |
  | SpotLight3D | Cone | Flashlights, car headlights |
- Remember all three inherit from Light3D, so Color, Energy (intensity) and shadow settings are shared. WHY: learn one property set, reuse everywhere.
- Know the Forward+ cap: up to 512 lights per scene by default; change it in Project Settings if needed. WHY: large projects can exceed the default.
- For old hardware or other renderers, prefer baked lightmaps over many real-time lights. WHY: real-time lights are expensive; baking trades flexibility for performance.
- Light can also come from materials with an Emission property and from global/ambient light (Sky resource, SDFGI) set on the WorldEnvironment. WHY: these fill the scene without adding light nodes.
## Checklist
- Confirm the active renderer before tuning lights.
- Count expected simultaneous lights; raise the Project Settings limit if near 512.
- Decide per light: real-time vs baked.
## Anti-patterns
- Assuming all light nodes behave the same — Directional, Omni and Spot differ in shape and shadow cost.
- Relying on hundreds of real-time lights on low-end targets instead of baking.
> CHECK: exact Project Settings path/name for the light limit is not stated in the text.

---
name: directional-light-setup
topic: Configuring DirectionalLight3D
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 9 (pp. 338-364)"]
---
## Rules
- Add a DirectionalLight3D via the scene panel "+" button, search "light", pick DirectionalLight3D. WHY: it is the standard sun/outdoor light.
- Leave Sky Mode at its default "Light and Sky" unless you need the light to affect only the scene (Light Only) or only the sky (Sky Only). WHY: default gives natural combined result.
- Enable the Shadows option under the Shadow section to make scene objects cast shadows. WHY: without it, no shadow detail appears.
- Choose Directional Shadow Mode by quality/performance:
  | Mode | Effect |
  |---|---|
  | PSSM 4 (default) | 4 shadow splits, sharpest, most expensive |
  | PSSM 2 | 2 splits, blurrier, cheaper/faster |
  | Orthogonal | blurriest, cheapest |
  WHY: fewer splits = less GPU cost but softer shadows.
- Set Color to a soft sunlight tone rather than pure white; the author uses hex #FFFFC4. WHY: pure white looks harsh; warm yellow reads as natural daylight.
- Experiment with tints for mood: orange for sunset, purple for storms. WHY: color is the cheapest way to set scene tone.
## Checklist
- Add node, keep Sky Mode default.
- Enable Shadows.
- Pick shadow Mode for your performance budget.
- Set a non-white Color.
- Verify shadows in the viewport by framing trees/objects.
## Anti-patterns
- Leaving Color at pure white — produces harsh light and shadows.
- Using PSSM 4 on low-end targets when PSSM 2 or Orthogonal would suffice.

---
name: omni-light-indoor-setup
topic: Using OmniLight3D for indoor lighting
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 9 (pp. 338-364)"]
---
## Rules
- Use OmniLight3D for enclosed spaces (rooms, lanterns, lamps) because it radiates in all directions from a point. WHY: matches how local light sources behave.
- Build a test room from 5 CSGBox3D nodes: 3 walls, 1 ceiling, 1 wall with an entrance. WHY: gives a closed volume to judge indoor light.
- Set each CSGBox3D Collision Layer to 3 so the player collides with them. WHY: CSG collision is enabled but has no matching mask by default, so the player falls through.
- Add the OmniLight3D inside the room, then drag the white handle on the sphere edge to resize its reach. WHY: visual sizing is faster than typing numbers.
- Tune the three core properties:
  | Property | Purpose |
  |---|---|
  | Range | Light radius (actual reach also affected by Attenuation) |
  | Attenuation | How brightness falls off with distance |
  | Shadow Mode | How shadows are rendered |
- Use the clapperboard Play button to run only the currently open scene. WHY: F5 loads the project's default scene (World.tscn), which is the wrong scene for testing.
## Checklist
- Build closed room from CSG boxes.
- Set Collision Layer 3 on every CSG box.
- Add OmniLight3D inside.
- Adjust Range/Attenuation/Shadow Mode.
- Test with the clapperboard Play button.
## Anti-patterns
- Forgetting Collision Layer 3 — player falls through the floor.
- Pressing F5 to test a non-default scene and loading the wrong level.

---
name: day-night-cycle
topic: Building a day/night cycle with DirectionalLight3D + AnimationPlayer
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 9 (pp. 338-364)"]
---
## Rules
- Add the sun as a child of the WorldEnvironment node in World.tscn, or reuse an existing DirectionalLight3D. WHY: keeps environment and sun together.
- Rename the node to Sun for clarity.
- Set the Sun's Position to x=7, y=26, z=7 (meters). WHY: gives a good starting angle for sweeping light.
- Enable Shadows and set Blur to 2. WHY: softer shadows blend better with the scene.
- Set Color to a soft yellow (author uses #FFFFC4). WHY: white looks unnatural for a sun.
- Add an AnimationPlayer as a child of Sun; create a new animation named day_time.
- Add a Property Track for Sun's Rotation.
- Set animation length to 12 (seconds) and enable looping. WHY: 12 s represents one in-game day; loop makes it continuous.
- Add keyframes: at t=0 set Rotation X = -90°, at t=12 set Rotation X = 270°. WHY: a full sweep of the sky.
- Trigger playback from script only after the player presses Play, by calling `sun.play();` inside the PlayerStart() function. WHY: the cycle should start with gameplay, not on load.
- Expose the AnimationPlayer with `[Export] public AnimationPlayer sun;` and drag the node into the Inspector. WHY: avoids GetNode path coupling.
- Rebuild the C# project after adding an [Export] variable. WHY: the Inspector only updates after a rebuild.
## Checklist
- Sun node under WorldEnvironment, renamed.
- Position 7/26/7, Shadows on, Blur 2, Color #FFFFC4.
- AnimationPlayer child of Sun, animation "day_time".
- Property track on Rotation, length 12, loop on.
- Keyframes at -90° (t=0) and 270° (t=12).
- [Export] AnimationPlayer, rebuild, assign in Inspector.
- Call sun.play() in PlayerStart().
## Anti-patterns
- Hardcoding the day length only in the AnimationPlayer — consider exposing it as a variable for tuning.
- Forgetting to rebuild after adding [Export] — the Inspector won't show the slot.
## Extensions
- Add a second, softer DirectionalLight3D as a moon enabled after sunset; fantasy settings can use multiple moons.
> CHECK: whether the 12-second length is intended as a placeholder or a recommended default; the text presents it as the author's choice.

<!-- 10 Understanding Accessibility and Additional Features (pp. 365-388) -->
---
name: accessibility-features-overview
topic: game accessibility
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Treat accessibility as a launch requirement, not a post-launch patch: it widens the audience and signals polish.
- There is no universal accessibility standard — the right set depends on genre. Twitch/action games need input-remapping and difficulty options; text-heavy games need font size, contrast and subtitle controls.
- Start with these four broadly applicable features:
  1. **Colorblind modes** — a filter applied to UI and game world. A community tool exists (godot-colorblindness by Paulloz).
  2. **Key rebinding** — let players remap controls instead of shipping one fixed scheme.
  3. **Subtitles** — on by default, with adjustable size and color, plus an optional background box for contrast.
  4. **Scalable UI** — let players resize HUD/UI elements so they fit different screens and eyesight.
- Reference external checklists when scoping: "Can I Play That?" (caniplaythat.com) and the Game Accessibility Guidelines site (gameaccessibilityguidelines.com), which tiers criteria by category.
- WHY: players differ in vision, motor control and cognition; a fixed one-size design silently excludes them.

## Checklist
- [ ] Colorblind filter available and toggleable.
- [ ] Every gameplay action is rebindable.
- [ ] Subtitles default ON, with size/color options and optional background.
- [ ] UI/HUD scale is adjustable.
- [ ] Reviewed against an external accessibility guideline list.

## Anti-patterns
- Assuming accessibility is optional polish — it is now an industry baseline and jam expectation.
- Copying another game's accessibility menu wholesale without checking your genre's specific barriers.
- Shipping subtitles off by default.

> CHECK: The chapter notes Godot 4's editor did not support OS screen readers at time of writing (open PR referenced). Verify current Godot version status before claiming screen-reader support.

---
name: settings-ui-tabbar-refactor
topic: UI / settings menu
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Split a settings screen into tabs (e.g. Audio, Controls) using a `TabBar` node placed at the top of the screen. This is the common convention and keeps the scene extensible.
- Scene tree shape: root `Settings` → `CanvasLayer` → `TabBar` + one `Panel` per tab (`AudioPanel`, `ControlsPanel`).
- Add tabs via the TabBar inspector's Tabs → Add Element; set Title only (Icon unnecessary for text tabs); leave Disabled unchecked so both tabs are interactive at startup.
- Suggested TabBar transform: Size x:399 y:85, Position x:90 y:55 (top-left of the ColorRect).
- Style TabBar through a Theme resource on the root node: add a TabBar theme type, then Override All on the font-color tab and set:
  - font_disabled_color #000000 alpha 168
  - font_hovered_color #000000 alpha 255
  - font_outline_color #FFFFFF alpha 255
  - font_selected_color #000000 alpha 255
  - font_unselected_color #484848 alpha 198
  - font_size 40
- StyleBoxes: `tab_focus` = StyleBoxFlat with BG alpha 0 (invisible); `tab_hovered` = StyleBoxFlat BG #E86A17 alpha 68, corner detail 8, top border 12, border blend #CCCCCC, bottom-left/right radius 7, expand bottom 5, content margins L/R 5, top 6, bottom -1; `tab_selected` = same as hovered but BG #7B7B7B alpha 109, border blend #E86A17, expand L/R 5 bottom 3, content margins L/T/R 6 bottom -1; `tab_unselected` = StyleBoxLine color #000000 alpha 255, grow end 5, thickness 5, content margins 12 all sides.
- Panels: Size x:1053 y:482, Position x:55 y:133. Override the theme's Panel style with `StyleBoxEmpty` so the panel background is transparent.
- Hide `ControlsPanel` at startup (eye icon) — it is shown only when the Controls tab is selected.
- Move audio widgets (MusicSlider, MusicLabel, SFXSlider, SFXLabel) under `AudioPanel`; build `ControlsPanel` as a VBoxContainer with six Buttons: Left, Right, Up, Down, Jump, Run.
- Delete the old "Settings" title label once tabs provide the heading.
- WHY: tabs scale better than a flat list and match player expectations from other games.

## Checklist
- [ ] TabBar is a child of CanvasLayer, not of a Panel.
- [ ] Both tabs interactive at startup.
- [ ] Theme overrides applied on the root so children inherit.
- [ ] Panels use StyleBoxEmpty override.
- [ ] ControlsPanel hidden by default.

## Anti-patterns
- Leaving the default tiny TabBar at the scene origin.
- Forgetting to override the inherited Panel style, leaving an unintended semi-transparent black background.

---
name: tab-switching-signal-logic
topic: UI / signal wiring
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Connect the TabBar's built-in `tab_selected(tab: int)` signal to a handler in the existing script (Settings.cs).
- Name the receiver method `TabChanged` and give it a matching signature: `private void TabChanged(int tab)`.
- Godot does NOT auto-generate the callback body when connecting — you must write the function yourself with the exact name and parameter types.
- Implement switching with a switch on the tab index:
  - case 0 → `audioMenu.visible = true; controlsMenu.visible = false;`
  - case 1 → the inverse.
- Only toggle the parent Panel's `visible`; children inherit visibility, so no per-widget toggling is needed.
- WHY: index-based switching keeps the handler trivial and independent of tab titles.

## Checklist
- [ ] Signal connected to a script that exists.
- [ ] Method name and parameter type match the signal exactly.
- [ ] Both cases handled; no fall-through.
- [ ] Panel references assigned (audioMenu, controlsMenu).

## Anti-patterns
- Expecting the editor to create the callback stub.
- Toggling every child widget instead of the parent panel.

---
name: save-data-formats
topic: persistence
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Choose the save format by data size, readability and security needs:
  | Format | Human-readable | Compact | Encryption | Best for |
  |---|---|---|---|---|
  | JSON | yes | no | no | jams, small player-data saves |
  | Binary serialization | no | yes | no | large data, machine-only reads |
  | ConfigFile | yes | yes | yes | settings and small saves needing some protection |
- JSON: nested key/value structure, e.g. `{"player_name":"Kati","mushrooms_collected":{"blue":1,"red":3}}`. Easy to read but verbose and insecure at scale.
- Binary serialization: Godot exposes a Variant-based serialization API; smallest footprint but not human-inspectable. Consult the binary serialization API docs for per-type byte sizes.
- ConfigFile: create a ConfigFile object, write values, call `save()`. Combines readability, small size and optional encryption.
- When exporting the project, mark JSON files so they are not exported as resources/scenes.
- WHY: picking the wrong format costs you either file size, debuggability or tamper resistance.

## Checklist
- [ ] Format chosen against the table above.
- [ ] JSON files flagged for export handling.
- [ ] Save/load path tested after export, not just in-editor.

## Anti-patterns
- Using JSON for large or sensitive save data.
- Assuming binary saves are secure — they are compact, not encrypted.

---
name: tween-animation-basics
topic: animation / Tween
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Use Tween for simple, lightweight interpolation (object or UI motion) where the target value is not fixed; prefer AnimationPlayer for authored, complex sequences.
- Declare a field to track the tween: `private Tween _itemTween;`
- Create and configure it in `_Ready()`: `_itemTween = CreateTween().SetLoops();` — `SetLoops()` with no argument means infinite looping.
- Animate a property with `TweenProperty(target, "property:component", finalValue, durationSeconds)`:
  - Float: `_itemTween.TweenProperty(this, "position:y", .25f, 1f).AsRelative();`
  - Rotation: `_itemTween.TweenProperty(this, "rotation:x", ChooseRandomDegree(), 1f).AsRelative();`
- Call `AsRelative()` to treat the final value as an offset from the current value rather than an absolute target.
- Insert a pause between loop iterations with `TweenInterval(seconds)`, e.g. `.5f`.
- Random helper: `using System;` then `public float ChooseRandomDegree() { Random r = new(); return r.Next(0, 30); }` — returns 0–30.
- WHY: assigning the tween to a variable lets you track and manage it; a single tween per object/property avoids conflicting writes.

## Checklist
- [ ] Tween stored in a field, not created inline and forgotten.
- [ ] `SetLoops()` called if the animation should repeat.
- [ ] `AsRelative()` used when the offset matters.
- [ ] Interval added if the loop should breathe.

## Anti-patterns
- Letting multiple tweens animate the same property of the same object — they fight each other.
- Using Tween for long, authored cutscene sequences where AnimationPlayer is clearer.

---
name: scene-switching
topic: scene management
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 10 (pp. 365-388)"]
---
## Rules
- Prefer multiple scenes over one giant scene; instantiate sub-scenes (player, collectibles) into the main scene.
- Two switching approaches, differing only in what happens to the old root:
  1. **Additive** — keep the old scene and stack the new one on top:
     `testScene = ResourceLoader.Load<PackedScene>("res://test_area.tscn").Instantiate();`
     `GetTree().Root.AddChild(testScene);`
  2. **Replace** — remove the old scene entirely:
     `GetTree().ChangeSceneToFile("res://test_area.tscn");`
- Bind each to an input action in Project Settings (e.g. `SwitchScene` on key 1, `SwitchSceneTwo` on key 2) and check with `Input.IsActionJustPressed("SwitchScene")` in `_PhysicsProcess`.
- Additive loading is useful for overlays; it is wrong for level transitions because both levels stay alive.
- `ChangeSceneToFile` replaces the scene-tree root: old nodes are freed, music stops, lighting resets, and old-scene data becomes inaccessible.
- WHY: replacing frees memory and resets state cleanly; additive preserves state but doubles live scenes.

## Checklist
- [ ] Input actions created in Project Settings before referencing them in code.
- [ ] Correct method chosen for the intent (overlay vs. level change).
- [ ] Any data that must survive a replace is saved before switching.

## Anti-patterns
- Using additive loading for level transitions — two levels run simultaneously.
- Expecting to read old-scene variables after `ChangeSceneToFile`.

<!-- 11 Exporting Your Game (pp. 389-415) -->
---
name: godot-export-templates-setup
topic: Godot export templates
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 11 (pp. 389-415)"]
---
## Rules
- Export templates are per-platform binaries that convert your project's code and assets into a runnable executable. Without a template for a platform, Godot shows a red "Export templates for this platform are missing" warning and cannot export.
- Install templates via Project → Export → Add… → pick platform → click the "Manage Export Templates" link → "Download and Install". The download source dropdown turns into a progress bar; click Close when done.
- Templates must match your exact Godot version. A mismatched template is unusable and Godot re-shows the red missing-template warning. WHY: template binaries are built against a specific engine build.
- You do not need the target OS installed to export for it — Godot serializes the project correctly with the right template. You only need the target OS to *test* the exported build.
- Custom export templates exist for cases where you use a specific or private SDK; otherwise use the official defaults.
- HTML5/web export is not available for C# projects in Godot 4 as of this writing. WHY: the C#-to-web toolchain is still being worked on by the community.
- For older Godot versions, download templates from the engine download archive, choosing the .NET button next to "Export Templates" for your version.

## Checklist
- [ ] Open Project → Export and confirm no red missing-template text remains for each target platform.
- [ ] Verify the template version matches the editor version exactly.
- [ ] Confirm the yellow (not red) warning appears after install — yellow only means optional metadata like icon/app info is unset.

## Anti-patterns
- Downloading a template for a different Godot minor/patch version and expecting it to work.
- Assuming you need a Mac/Windows/Linux machine to produce that platform's build.
- Planning a C# web build for itch.io browser play — not supported.

> CHECK: OCR shows a duplicated "Debug" bullet in the Options list; verify the exact label of the second one (likely a separate debug-related toggle) against the Godot 4 export dialog.

---
name: godot-export-preset-options
topic: Godot export preset configuration
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 11 (pp. 389-415)"]
---
## Rules
- Export buttons: "Export All" builds every added preset; "Export Project" builds only the selected preset; "Export PCK/ZIP" produces a package that is not directly runnable (used e.g. for HTML5 uploads).
- Name: set the executable name to your project name, not the default preset name. WHY: this is what players see.
- Export Path: save outside the project directory, in an easy-to-find folder. WHY: keeps build artifacts out of source control and easy to locate.
- Debug vs Release: use Debug for test builds (error guards, debug logs for crash/bug hunting); use Release for the final build (performance optimizations).
- Export Console Wrapper: default "Debug Only". Set to "No" for the final release. WHY: otherwise a console window pops up when players run the executable.
- Embed PCK: enable it. WHY: fewer files to manage, easier hot updates, mod support, and it obscures the codebase from casual inspection.
- Architecture: pick the architecture matching your target players' platform.
- Texture Format: BPTC and S3TC are defaults; ETC2 and ASTC are the mobile-oriented lossy compression formats. Leave defaults unless you have a mobile target.
- Codesign: applies to Windows and macOS only. Unsigned executables trigger OS warnings and make players wary; signing methods differ per OS.
- Modify Resources: enable to change the executable icon and metadata (Icon, File Version, Product Version, Company Name, Product Name, File Description, Copyright, Trademarks). Use semantic versioning like 1.0.0 for File/Product Version.
- Company Name is a required field; it defaults to the literal "Company Name" — replace it.
- Enabling Modify Resources triggers a yellow warning that rcedit must be configured in Editor Settings for the icon/metadata to apply on Windows.

## Checklist
- [ ] Name set to project name.
- [ ] Export path outside the project folder.
- [ ] Release build selected for shipping; Debug for testing.
- [ ] Console Wrapper = No for release.
- [ ] Embed PCK enabled.
- [ ] Architecture matches target.
- [ ] Modify Resources filled in (icon, versions, company, product, copyright).
- [ ] rcedit configured if you changed the icon on Windows.

## Anti-patterns
- Shipping a release build with the console wrapper enabled (console window appears for players).
- Leaving Company Name as the default placeholder.
- Exporting to a path inside the project directory.

---
name: godot-export-resource-filtering
topic: Export resource and file filtering
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 11 (pp. 389-415)"]
---
## Rules
- The Resources tab's "Export Mode" controls what gets packed. Options:
  - Export all resources in the project — everything, no filtering (default).
  - Export selected scenes (and dependencies) — pick scenes; useful to exclude test/debug scenes.
  - Export selected resources (and dependencies) — same idea, for resources.
  - Export all resources except resources checked below — everything minus a specified exclusion list; good for removing test scenes/scripts.
  - Export as dedicated server — strips all visual elements and replaces them with placeholders.
- For a normal single-player game with no test-only content, keep the default "Export all resources in the project".
- Non-resource files (e.g. .json dialogue, .csv game data) must be declared in the two filter fields below Export Mode, as comma-separated file-type patterns. WHY: otherwise Godot tries to serialize them into the executable.
- Leave the non-resource filter fields blank if your project has no such files.

## Checklist
- [ ] Decide whether any test/debug scenes or scripts must be excluded.
- [ ] List every non-resource file type (json, csv, txt) in the filter fields.
- [ ] Confirm no data files are silently packed as resources.

## Anti-patterns
- Shipping test/debug scenes to players because you left Export Mode on "all resources".
- Forgetting to declare .json/.csv data files, causing Godot to attempt serializing them.

---
name: godot-export-windows-walkthrough
topic: Exporting a Windows build
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 11 (pp. 389-415)"]
---
## Rules
- Open Project → Export…, select the target OS preset (e.g. Windows Desktop).
- Set Export Path via the folder icon: choose a location outside the project, create a dedicated folder (e.g. godot_book_exports) for all builds.
- Name the executable descriptively per platform (e.g. godot-book-windows) so builds are distinguishable.
- Click "Export Project…" to build only the selected platform; a progress window appears and disappears when done.
- The resulting executable appears in the export folder with the Godot engine icon by default.
- Linux and macOS export follow the same steps; only the packaging differs per platform.

## Checklist
- [ ] Preset selected for the target OS.
- [ ] Export path set to a dedicated, outside-project folder.
- [ ] Executable named per platform.
- [ ] Export Project… run and progress window completed.
- [ ] Executable verified present in the export folder.

## Anti-patterns
- Using the same generic executable name for every platform, making builds hard to tell apart.
- Exporting into the project directory.

---
name: itch-io-publishing
topic: Publishing a build to itch.io
confidence: opinion
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. 11 (pp. 389-415)"]
---
## Rules
- itch.io is free to publish on (unlike Steam/GOG) and is the standard venue for game jams and indie prototypes. Choose it for prototypes and jam entries.
- Register, then use the dashboard's "Create new project" button.
- Project URL is auto-generated from the title but editable before creating the project — set it deliberately.
- Short description/tagline: 1–2 lines summarizing the core hook.
- Classification = Games; Kind of project = Downloadable for an executable build.
- Release status: use Prototype or In Development for unfinished work.
- Pricing: choose "No payments" for a free prototype.
- Uploads: upload a ZIP; the per-file size limit is 1 GB.
- Details section: Description, Genre (one only), Tags (max 10, avoid duplicating genre/platform names), AI generation disclosure (yes/no), App store links, Custom noun, Community settings, Visibility & access (draft / restricted / public).
- Visibility: set draft or restricted while still developing and not wanting feedback.
- After upload, tick the platform checkbox (e.g. Windows) next to the file and untick "Hide this file and prevent it from being downloaded".
- Do not navigate away from the project page during upload.
- Optional but recommended: cover image, screenshots, and a YouTube demo link improve exposure.

## Checklist
- [ ] Account created and logged in.
- [ ] Title, URL, tagline, classification, kind, release status, pricing set.
- [ ] ZIP uploaded (under 1 GB).
- [ ] Platform checkbox ticked; "hide file" unticked.
- [ ] Genre chosen, ≤10 relevant tags added.
- [ ] AI disclosure answered.
- [ ] Visibility set appropriately for the current stage.
- [ ] Save clicked, then View Page to verify.

## Anti-patterns
- Leaving the project page mid-upload.
- Forgetting to untick "Hide this file", making the build undownloadable.
- Using tags that duplicate the genre or platform names.
- Publishing as public before you want feedback.

> CHECK: OCR of the itch.io form is partly garbled (Chinese/English mix); verify exact wording of the "Release status" and "Pricing" option labels against the live site.

<!-- Appendix: Transitioning from Godot 3 to Godot 4 (pp. 464-482) -->
---
name: godot-3-to-4-migration-decision
topic: engine-version-migration
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. Appendix: Transitioning from Godot 3 to Godot 4 (pp. 464-482)"]
---
## Rules
- Treat a Godot 3 → 4 upgrade as a real project task, not a quick port: most engine code was refactored, so component handling differs substantially. Budget time proportional to project size and number of systems used.
- Decide per project, not globally:
  - Hard deadline / commercial project → weigh the technical debt you can absorb; staying on 3.x LTS is a valid choice.
  - Game jam / hobby project → upgrading or even rebuilding from scratch in Godot 4 is cheap and worth it.
- Prefer Godot 4 for new long-lived projects: it has all new features and bug fixes, better error reporting, and a longer support window than 3.x.
- Stay on Godot 3.6 LTS if your project depends on systems that were removed or rewritten beyond recognition; the community plans to backport compatible features into 3.6.
- If you use C#: accept that Godot 4 C# projects cannot currently be exported to iOS, Android, or HTML5. GDScript projects can. C# export support is on the 4.x roadmap.
- When unsure whether a feature exists in a given version, check the official docs first — they are community-maintained and updated regularly.
## Checklist
- [ ] List every engine system your project touches (rendering, tilemaps, shaders, tweens, time, particles).
- [ ] Classify each as: unchanged / renamed / rewritten / removed.
- [ ] Estimate migration cost from that list, not from gut feeling.
- [ ] Confirm target platform support for your scripting language (C# vs GDScript).
- [ ] Read the official "Upgrading to Godot 4" doc page before starting.
## Anti-patterns
- Upgrading a deadline-bound project without first measuring which systems are affected.
- Assuming the automatic converter handles everything — it only fixes a subset (e.g. node renames).
- Choosing Godot 4 solely because it is newer when your project relies on removed systems.
- Assuming C# and GDScript have identical export platform support in Godot 4.

---
name: godot-4-core-system-changes
topic: engine-changes-overview
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. Appendix: Transitioning from Godot 3 to Godot 4 (pp. 464-482)"]
---
## Rules
- Rendering: the main renderer moved from OpenGL to Vulkan, improving shading, lighting, shadows, and CPU/GPU efficiency. A separate OpenGL-based 2D renderer exists for mobile/low-end devices and can also run 3D with limitations.
- FSR 1.0 (AMD FidelityFX Super Resolution) is supported; FSR 2.0 and a DirectX 12 renderer are planned. FSR works on both AMD and NVIDIA GPUs.
- TileMap/TileSet was rewritten from scratch. New capabilities: layer support for foreground/background, random tile painting for decoration, finer per-tile collision layer settings, selection-tool stamps for painting large multi-tile elements, and tile gap artifacts are eliminated.
- Shaders/VFX additions: `FogVolume` node for volumetric fog placed at specific scene positions; updated Shader Editor and extended shader language; Decals for layering materials onto surfaces; sky shaders for dynamically updated sky backgrounds; GPU-based particle systems with trails, collision, and scene interaction (e.g. bouncing off surfaces); noise filters for procedural content.
- Editor UX: multi-window support. Enable it via the three-dot button next to any dock panel → "Make Floating". Useful for multi-monitor setups and long property lists.
- Node renames: `Spatial` → `Node3D`. Godot auto-updates old node names when opening a Godot 3 project in Godot 4.
- Shader file extension: Godot 3 accepted `.shader` and `.gdshader`; Godot 4 accepts only `.gdshader`.
- Time API: Godot 3 exposed time functions via `OS`; Godot 4 introduces a dedicated `Time` object.
- Tweens: Godot 3 required a separate Tween node wired to the animated node; Godot 4 lets you create/manage/destroy tweens directly in the target object's script (e.g. `TweenProperty`), with easing and multiple simultaneous tweens.
## Checklist
- [ ] Grep the project for `Spatial` and confirm auto-rename results in every scene.
- [ ] Rename all `.shader` files to `.gdshader`.
- [ ] Find every `OS`-based time call and repoint it to the `Time` class.
- [ ] Find every Tween node and convert it to script-based tween creation.
- [ ] Re-check tilemap collision layers after the TileSet rewrite.
## Anti-patterns
- Assuming the Vulkan renderer is the only option — pick the OpenGL 2D renderer for low-end/mobile targets.
- Leaving `.shader` files in place and expecting them to load.
- Keeping standalone Tween nodes out of habit; the new API is script-local.
- Trusting the auto-converter to fix time, tween, and shader-extension changes — it does not.

---
name: godot-4-upgrade-preparation
topic: migration-preparation
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. Appendix: Transitioning from Godot 3 to Godot 4 (pp. 464-482)"]
---
## Rules
- Back up the project before touching anything. If it is in Git, create two branches off main:
  1. A Godot 3 branch that keeps the current working version — you can keep developing there if the upgrade stalls or disappoints.
  2. An upgrade branch where the conversion happens; merge to main only after full testing.
- This branch split gives you both a safety net and a measurable estimate of the upgrade's real time cost.
- Before running the converter, do the manual prep work:
  - Rename all shader files to `.gdshader`.
  - Locate every time-function call (they move to the `Time` object).
  - Locate every Tween node (they become script-based tweens).
- Marking these call sites up front measurably reduces upgrade time, because the converter cannot fix them.
## Checklist
- [ ] Backup / commit current state.
- [ ] Create `godot3-legacy` branch.
- [ ] Create `godot4-upgrade` branch.
- [ ] Rename `.shader` → `.gdshader`.
- [ ] List all time-function call sites.
- [ ] List all Tween nodes.
- [ ] Only then run the project converter.
## Anti-patterns
- Converting in place on the main branch with no fallback.
- Running the converter before renaming shaders and auditing time/tween usage.
- Deleting the Godot 3 branch after a "successful" conversion — you lose the ability to compare behavior.

---
name: godot-4-project-converter-usage
topic: project-conversion-tool
confidence: consensus
sources: ["Godot 4 and C# Game Development, Kati Baker, ch. Appendix: Transitioning from Godot 3 to Godot 4 (pp. 464-482)"]
---
## Rules
- The project upgrade tool is now built into the engine (it was a separate component at Godot 4's launch).
- Procedure:
  1. Download/unzip the project.
  2. Open Godot 4 → Project Manager → click **Import**.
  3. A dialog asks whether to convert; choose **Convert Full Project**.
  4. Confirm the second dialog with **OK**.
  5. The project appears in the project list; open it.
- Use **Convert project.godot Only** only as a fallback, e.g. when the full conversion fails.
- After conversion, scene and resource IDs are updated to Godot 4 naming conventions, but you must still verify every piece of content manually against the Godot 3 behavior.
- Expect errors that come from fully rewritten systems; those have no automated migration path and require manual fixes.
## Checklist
- [ ] Import via Project Manager, not by opening the folder directly.
- [ ] Choose "Convert Full Project".
- [ ] Open the converted project and walk every scene.
- [ ] Compare runtime behavior against the Godot 3 branch.
- [ ] Fix rewritten-system errors by hand.
- [ ] Merge to main only after full testing.
## Anti-patterns
- Choosing "Convert project.godot Only" as the default — it is a fallback, not the normal path.
- Treating a successful conversion as a finished migration; the tool does not validate behavior.
- Skipping the side-by-side comparison with the Godot 3 branch.

> CHECK: The chapter references figures (Appendix Fig. 1–6) that are not in the OCR text; the exact wording of the converter dialogs and the full diff table in Fig. 1 could not be verified.
---
name: tiled-pipeline
description: How this kit uses Tiled — editor only, never its own scene exporter. Maps are authored as .tmx text and turned into Godot scenes by the tiled_export MCP tool. Load before touching any .tmx file or level scene.
---

# Tiled pipeline

Tiled is the **editor only**. It is never the thing that produces the final Godot scene.

## Why

Tiled's own "export as scene" plugin is known to crash (segfault) on the pinned Tiled version this kit targets. Relying on it would make level export flaky and unrepeatable across machines.

## The actual pipeline

1. Author or edit the level as a `.tmx` file — it's plain XML text, so an agent can write or patch it directly, and a human can open the same file in the Tiled app to retouch it visually.
2. Turn it into a Godot scene with the `tiled_export` MCP tool (`mcp__godot-kit__tiled_export`), which reads the `.tmx` XML directly and builds `TileMapLayer`s (and whatever else the project's converter emits) without going through Tiled's own exporter at all.
3. Re-run `tiled_export` any time the `.tmx` changes — the Godot scene is a build artifact of the `.tmx`, not a hand-edited file. Don't hand-edit the generated scene and expect it to survive the next export.

## Rules

- Never invoke Tiled's own "export as map to .tscn" feature — it's the thing that crashes.
- Treat the `.tmx` as the source of truth for level layout; treat the exported scene as disposable and regeneratable.
- If a human wants to touch up a map visually, point them at the `.tmx` in the Tiled app, not at the generated scene.
- If `tiled_export` fails or produces something wrong, that's a converter bug to report, not a reason to hand-edit the generated scene as a workaround.

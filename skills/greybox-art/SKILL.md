---
name: greybox-art
description: Building greybox visuals — shapes and a defined palette before any real art exists — using the greybox_tileset/greybox_sprite MCP tools, structured so sprites can later replace them without touching gameplay logic.
---

# Greybox art

Before any real art asset exists, the game should already read clearly using shapes and color alone. This isn't a placeholder to be embarrassed about — a good greybox pass catches readability and game-feel problems cheaply, before art is sunk into them.

## How to build it

- Use `greybox_tileset` (palette + tile names → tileset PNG) and `greybox_sprite` (shape + color + size → PNG) to generate greybox art by code, from the palette the GDD defines. Never hand-paint greybox art in a GUI — it should be regenerable from a palette change alone.
- Prefer simple, distinguishable shapes: a triangle or arrow for the player (shows facing), circles for pickups, rectangles for obstacles, and consistent silhouettes per category so the player learns the visual language fast.
- Keep every entity's visual behind a dedicated child node (commonly named `Visual`) that only reads state — properties or signals exposed by the gameplay node. Gameplay code never draws directly and never reaches into `Visual`'s internals.

## Why the separation matters

When real sprites are ready, swapping greybox for final art means replacing the contents of that one `Visual` node — nothing in the gameplay script changes, and nothing needs to be retested beyond "does it still look right." If greybox drawing logic and gameplay logic are tangled together, that swap becomes a rewrite instead of a swap.

## Sequencing

1. Palette and shape language come from the GDD (ask `game-designer` if missing — don't invent colors).
2. Build the greybox pass early, before or alongside first-pass gameplay, so game feel can be judged with something on screen.
3. Sprites replace greybox later, per game/genre — see the `pixel-art-for-games` skill when that time comes. The greybox version stays in the project as a fallback/reference, not deleted.

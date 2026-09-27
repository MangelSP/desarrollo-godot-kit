---
name: pixel-art-for-games
description: Ground rules for pixel art sprites — canvas sizes, limited palettes, outlines, and animation frame counts — before generating or touching up game sprites. Search knowledge for "pixel art" for the fuller distilled reference.
---

# Pixel art for games

This is the short, actionable version. For the deeper reference (readability principles, animation timing, palette theory), call `knowledge_search("pixel art")` — the distilled cards go further than this summary should.

## Before generating anything

- Confirm the sprite size and the palette against the GDD's art-direction answer from the intake questionnaire — don't guess a resolution.
- Common canvas sizes: 16×16 or 32×32 for a top-down character on a tile-based world; scale consistently across all sprites in the same game (mixing effective resolutions is the single most common thing that makes pixel art look wrong).

## Rules of thumb

- **Limited palette**: pick a small palette (commonly under 32 colors total for the whole game) and reuse it everywhere; don't let each sprite invent its own colors.
- **Outlines**: a consistent outline treatment (dark outline on every sprite, or none on any sprite) — mixing outlined and non-outlined sprites reads as inconsistent.
- **Readability at target size**: a sprite must read correctly at the size it's actually displayed at in-game, not just when zoomed in during editing — always check it at 1x.
- **Animation**: keep frame counts modest (a walk cycle commonly needs 4-8 frames, not 24) — pixel art animation relies on clear key poses more than smooth interpolation.
- **No anti-aliasing** on pixel edges; keep hard pixel boundaries so the art matches its own genre conventions.

## Workflow in this kit

1. Generate the sprite by code as a PNG (matching the GDD's palette), never by drawing in a GUI.
2. Hand it to the human for touch-up with `pixelorama_open` — the human retouches in the Pixelorama app; the agent doesn't draw in that GUI itself.
3. Keep the greybox shape version around as a fallback until the sprite is confirmed good (see the `greybox-art` skill).

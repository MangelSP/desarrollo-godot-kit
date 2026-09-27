<!-- 0 Introduction chapter (pp. 5-21) -->
---
name: what-is-pixel-art
topic: definition of pixel art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Treat a graphic as pixel art only if every pixel is placed intentionally by the artist. Aliased (non-smoothed) edges alone do not make it pixel art.
- Do not count digitized photos, pre-rendered 3D models, or full-motion video sprites as pixel art, even if they appear on screen as sprites.
- Do not count Oekaki or binary art as pixel art; they share aliased graphics but are a different discipline.
- Resolution and color-count limits are historical, not defining. Modern pixel art may use large canvases and many colors.
- Judge the technique, not the tool: a simple program can produce real pixel art, an advanced one cannot substitute for technique.
## Checklist
- [ ] Can you point to each pixel and say why it is there?
- [ ] Was the sprite hand-edited at pixel level (not scaled, filtered, or auto-generated)?
- [ ] Are edges aliased by intent, not by accident?
## Anti-patterns
- Assuming "no blur = pixel art". Aliased output from a soft brush is still not pixel art.
- Believing better software produces better pixel art. Tools do not define the artist.

---
name: pixel-art-workflow
topic: drawing workflow and layers
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Default to drawing on a single layer; this keeps you close to traditional drawing and forces deliberate pixel placement.
- Use multiple layers when they pay off: animation with many overlapping parts, scenes, and mock game screenshots.
- Merge layers once the count gets unmanageable.
- Pick one of two entry paths: (a) sketch → line art → block shapes → shade → clean up, or (b) block shapes first, then chisel and refine like 2D sculpting.
- If a tiny canvas blocks you, draw at high resolution first, shrink to target dimensions, then trace the sketch and continue.
- Keep your existing illustration method if you already have one; only switch if you want to experiment.
## Checklist
- [ ] Layer count justified (animation/scene) or reduced to one?
- [ ] Sketch shrunk to final canvas size before tracing?
- [ ] Clean-up pass done last?
## Anti-patterns
- Stacking layers out of habit on a single static sprite.
- Drawing directly at tiny resolution when you cannot yet judge shapes at that scale.

---
name: pixel-art-software
topic: software selection
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Dedicated pixel tools: GraphicsGale (free, strong tileset/export/palette tools, basic timeline), Aseprite (~$20, best animation timeline, retro palette access, reskinnable UI).
- General art tools usable for pixel work: Pro Motion (~$40, strong onion skin, zoom to 5000%, plugin-friendly), Paint Tool SAI (~$50, color shifting, smooth 1px lines, tablet-friendly), Clip Studio Paint (~$50 one-time, "Dot Pen" brush, basic animation), GIMP (free, capable but non-intuitive for pixel work), Photoshop (subscription, needs manual setup for pixel precision).
- MS Paint: use only the Windows XP or Vista version. Versions after Windows 7 ship non-pixel tools that cannot produce clean pixel art.
- Choose based on your own testing, not on reputation. Keep the tool you already know unless a specific feature (e.g. animation timeline) is missing.
## Checklist
- [ ] Does the tool give a hard 1px pencil with no anti-aliasing?
- [ ] Does it have an eyedropper, eraser, and bucket?
- [ ] Does it export tilesets/spritesheets if you need them?
- [ ] Is the animation timeline good enough for your frame count?
## Anti-patterns
- Buying expensive software expecting it to fix weak technique.
- Using post-Win7 MS Paint for pixel art.

---
name: pixel-art-hardware
topic: input hardware
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Mouse: precise clicking, good for clean-up and final touches, poor for free strokes.
- Tablet: good for intuitive strokes and sketching, awkward for repeated clicking.
- Either is acceptable; pick per task or use both.
- Map frequent actions to keyboard shortcuts and extra mouse/tablet buttons (frame flipping, tool switching) to cut hand travel.
- A second monitor is optional but genuinely useful; modern resolutions make dual screens unnecessary for pixel work.
## Checklist
- [ ] Shortcuts bound for pencil, eyedropper, bucket, frame step?
- [ ] Input device matched to the current phase (sketch vs clean-up)?
## Anti-patterns
- Forcing one device for all phases when the other is clearly better suited.

---
name: core-pixel-art-tools
topic: minimum toolset
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Four mandatory tools: pencil (1px, crisp, no smoothing), eyedropper (color pick, often right-click), eraser (or erase via transparency/background color), bucket (flood fill one solid color).
- Useful extras: selection, recolor, line, rotation, circle, color settings.
- Avoid automatic tools: blur, soft brushes, blurred gradients. You cannot predict their output, which breaks the 100%-control premise of pixel art.
- If a program lacks an eraser, it usually maps pencil to left-click and eyedropper to right-click.
## Checklist
- [ ] Pencil produces exactly 1px, no anti-aliasing?
- [ ] Bucket fill checked for gaps before use?
- [ ] Any blur/soft-brush tool disabled or unused?
## Anti-patterns
- Flood-filling an area with unclosed outlines; the fill leaks across the whole canvas.
- Relying on blur to fake shading instead of placing pixels.

---
name: canvas-size-and-sprite-ratio
topic: canvas sizing
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- Decide canvas size before drawing; it constrains every later decision.
- For beginners, choose a canvas smaller than a GBA screen (240x160).
- A safe general target is the maximum resolution of older consoles.
- For online display, size is free; for game sprites, size is dictated by the target platform and readability.
- Evaluate the sprite-to-canvas ratio for playable characters:
  - Metroid II (Game Boy): sprite ≈ 1:24, ~4% of screen — large, cramped for maneuvering.
  - Super Metroid (SNES): sprite ≈ 1:38, ~2.5% of screen — low ratio, more environment visible.
  - Cave Story (PC): sprite ≈ 1:300, ~0.33% of screen — tiny but still readable.
- Tiles are a useful size reference for small sprites.
## Checklist
- [ ] Canvas size fixed before first stroke?
- [ ] Sprite-to-canvas ratio computed and compared against a reference game of the same genre?
- [ ] Ratio leaves enough visible environment for the intended movement style?
## Anti-patterns
- Starting without a canvas size and rescaling later.
- Copying a ratio from a game with different movement/readability needs.

---
name: mixels-and-scaling
topic: mixels and resizing
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 0 (pp. 5-21)"]
---
## Rules
- When resizing pixel art, use whole-number factors only: 2x, 3x, 4x. Never 1.25x, 1.5x, 2.5x.
- Never mix different pixel scales in one piece. Mixing scales produces "mixels" (mixed pixels) that read as inconsistent.
- Never mix different aspect ratios in one piece.
- Rotated pixel art also produces mixels; avoid combining rotated sprites with unrotated ones in the same artwork.
- Exception: allow mixels and rotation for gameplay needs — turning arms, aiming weapons, any smooth 360° motion. Gameplay takes priority over graphical purity.
## Checklist
- [ ] All assets in the piece share one pixel scale?
- [ ] All assets share one aspect ratio?
- [ ] Any rotated sprite justified by gameplay, not decoration?
## Anti-patterns
- Scaling a sprite by 150% to fit a layout.
- Placing a rotated sprite next to unrotated ones in a static illustration.
- Mixing background, UI numbers, characters, and tiles at different scales in one screen.

> CHECK: The chapter lists many example images (by Michafrar, Anubis Jr., Yaa, SoapH, cyanatar, StevenM) without captions tying them to specific rules; no rule was extracted from them.

<!-- 1 Line Art (pp. 22-37) -->
---
name: pixel-line-art-fundamentals
topic: pixel art line art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 1 (pp. 22-37)"]
---
## Rules
- Use 1px line width for most pixel art sprites; it maximizes readability at small sizes. Thicker lines are allowed only if they stay clean and easy to follow.
- Keep line width consistent across the entire sprite. Inconsistent width breaks visual coherence.
- Thin lines suit small areas; thicker lines suit larger sprites or specific styles. Choose one and commit.
- Treat every edge in the sprite as a line, even in lineless art. Shading boundaries and shape edges must follow the same cleanliness rules as drawn lines.
- Draw lines first, then chisel away unwanted pixels with the selection tool rather than redrawing from scratch. Chiselling is faster and more precise than freehand drawing.
- Do not rely on "pixel perfect" brush options in Aseprite or Pro Motion; they reduce but do not eliminate jaggies. Fix jaggies manually pixel by pixel.
- Jaggies are unavoidable — expect them on every line and curve and plan to clean them up.
- To spot jaggies, mentally overlay the intended HD line over your pixel line; deviations reveal the errors.

## Checklist
- [ ] Line width is uniform across the whole sprite.
- [ ] No row of pixels is surrounded by larger neighbouring rows (jaggies).
- [ ] Staircase steps on a line all use the same pixel count.
- [ ] Steeper lines use larger steps; shallower lines use smaller steps — but never mixed within one line.
- [ ] Curves were drawn then chiselled, not plotted pixel by pixel.
- [ ] Shading edges on smooth surfaces are free of jaggies.
- [ ] "Pixel perfect" tool output was manually verified and corrected.

## Anti-patterns
- Mixing staircase sizes on one line (e.g. a 1px step inside a 2px-step staircase) — creates visible jaggies.
- Drawing curves pixel by pixel from scratch — slow and error-prone; chisel instead.
- Trusting automatic pixel-perfect brushes as a final fix — they leave residual jaggies.
- Using natural, variable-width brushstrokes — pixel art needs deliberate, uniform strokes.
- Assuming lineless art needs no cleanup — edges and shading still require jaggy removal.

> CHECK: OCR is garbled around the "stairs" explanation (p. 27); verify exact wording of the staircase rule and whether the author gives a numeric step-to-slope table.

---
name: pixel-outline-types
topic: pixel art outlines
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 1 (pp. 22-37)"]
---
## Rules
- Choose one outline type per sprite and apply it consistently; the outline defines the sprite's style more than any other single attribute.
- No outline: shapes are solid colours, sometimes with internal lines. Best for backgrounds and lineless styles. Still requires jaggy removal.
- Black inline: black outline plus black internal lines. Effective for 8-bit-era limitations but reads as muddy in modern art; use only for deliberate retro style.
- Black contour: black outline on the outer edge only, interior fully coloured with little to no black. Best default for moving sprites and small handheld screens because it separates the character from the background.
- Coloured outline: each outline segment uses the darkest shade of the colour it surrounds. Outline must be a single solid colour per segment.
- Shaded outline: outline itself is shaded, showing the light source. Most common pixel art outline; blends well with both light and dark backgrounds.
- Selective outline: a shaded-outline variant where the outline breaks into segments; reads as broken lines on light backgrounds but works better on dark backgrounds.
- Outline thickness is a stylistic choice; thicker outlines need less anti-aliasing, softer/thinner outlines need more anti-aliasing.

## Checklist
- [ ] Outline type chosen and documented for the sprite set.
- [ ] Black contour: interior contains no stray black pixels.
- [ ] Coloured outline: each segment matches the darkest shade of its enclosed colour.
- [ ] Shaded outline: light source direction is readable from the outline alone.
- [ ] Selective outline: verified against both light and dark backgrounds.
- [ ] Outline thickness consistent around the whole sprite.

## Anti-patterns
- Mixing outline types within one sprite or sprite set — destroys stylistic unity.
- Using black inlines for modern sprites — makes them look muddy.
- Coloured outlines with multiple colours inside one segment — breaks the single-solid-colour rule.
- Thin soft outlines without added anti-aliasing — edges look harsh or noisy.
- Assuming outline choice is cosmetic — it changes the entire perceived style.

> CHECK: OCR lists "Selective Outlines" under both shaded outlines and the summary; confirm whether the author classifies selective outlines as a subtype of shaded outlines or as a separate category.

<!-- 2 Anti-Aliasing (pp. 38-59) -->
---
name: anti-aliasing-purpose-and-tradeoffs
topic: Anti-aliasing fundamentals
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- Anti-aliasing (AA) = placing intermediate-colour pixels in the "corners" of steps to bridge two colours. It smooths jaggies on curves and diagonals.
- AA is optional, not mandatory. A solid drawing with clean shapes reads well with or without AA. WHY: AA is "icing on the cake" — it adds detail, it does not fix bad shapes.
- Use AA when: large sprites, smooth/soft art styles, high-contrast colour pairs meeting at an edge, small tight curves, faces/eyes, and typography (letters and numbers always benefit).
- Skip AA when: tiny sprites (AA blurs them and hurts readability), crisp/crayon/sharp art styles, low-contrast colour pairs, and 45° lines on low-colour palettes (e.g. NES-era limits).
- AA costs palette slots. On a 4-colour sprite, spending colours on AA means fewer colours elsewhere. WHY: AA trades colour budget for edge smoothness.
- AA is placed pixel by pixel, so you keep full control of tone and feel; heavy AA shifts the piece toward vector/blurry look.
- AA works best on the inside of a sprite; it looks bad on the outside of the silhouette. WHY: outside AA breaks the outline and reads as a halo.
## Checklist
- Decide AA vs no-AA per sprite based on size, style, and palette budget.
- Zoom out to 1x/2x to judge the result — never judge AA zoomed in only.
- Check that base colours and shapes read correctly before adding AA.
- Verify AA does not exceed 2–3 shades.
## Anti-patterns
- Adding AA to a tiny sprite: it becomes a blurry blob.
- Using AA to compensate for a weak drawing or bad shapes.
- Heavy AA everywhere: loses the pixel-art feel and turns into a raster/vector look.
- AA on the outside of the outline.

---
name: anti-aliasing-amount-and-shades
topic: AA application quantities
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- Number of AA pixels to add: roughly half the length of the line/step being smoothed. Too little is better than too much.
- Shades of AA: 1 shade to start practicing, 2 for smoother results, 3 only if you have spare colours and confidence.
- A mix of 1 and 2 shades is the recommended default.
- Longer steps need longer AA runs; flatter curves need more shades than steep ones. WHY: a flatter curve has more gradual colour transition in the source image.
- Low-contrast colour pairs need little to no AA. WHY: the eye barely sees the step, so AA adds cost without visible benefit.
- High-contrast colour pairs benefit most from AA — insert intermediary pixels to bridge them.
- More colours in the sprite allow more AA variety; fewer colours mean less need for AA.
## Checklist
- Count the step length, then add about half that many AA pixels.
- Cap AA at 2 shades unless the palette is generous.
- Zoom out and confirm the AA is visible but not blurry.
- Compare with reference sprites from games you like to calibrate amount.
## Anti-patterns
- Overdoing AA: the blurred side looks nearly identical to a lighter version, so the extra work is wasted.
- Using 3+ shades on a small sprite.
- Adding AA to low-contrast edges.

---
name: anti-aliasing-curves-and-45-lines
topic: AA on curves and diagonals
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- Flat curves (near-horizontal/vertical): rarely in small sprites, common in large art. AA is optional; longer steps = longer AA runs.
- 45° lines: AA is rare here. On low-colour hardware (NES) there is little to no AA. Sprites with more colours can afford AA on diagonals.
- Convex curve: centre of the curve gets light AA pixels, ends get dark AA pixels.
- Concave curve: centre gets dark AA pixels, ends get light AA pixels.
- Darker AA pixels make the 45° segment look thicker; lighter AA pixels make it look thinner.
- To round a 45° line: place a lighter pixel on one side and a darker pixel on the other side of the line. The lighter pixels curve the sides; the darker ones create the tip.
- Keep the outline colour solid when AA would stand out against the background (e.g. dark background vs light AA pixels).
## Checklist
- Identify convex vs concave before choosing light or dark AA.
- For 45° lines, decide whether you want the segment thicker (dark) or thinner (light).
- Test AA against the actual background colour, not just the sprite.
- Zoom out to confirm the curve reads as rounded.
## Anti-patterns
- Applying AA to 45° lines on a low-colour palette where it adds noise.
- Letting AA pixels break a solid outline against a contrasting background.
- Using the same light/dark AA direction for both convex and concave curves.

---
name: anti-aliasing-jagged-lines
topic: Fixing jagged lines with AA
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- For a jagged line, first imagine the ideal smooth line, then fill in the biggest gaps with AA pixels.
- For smaller remaining gaps, use a lighter AA colour.
- Further smoothing is optional — stop when the line reads smooth enough.
- Fuller lines are better; AA on the inside of the sprite only.
- This technique also works for other types of jagged lines, not just curves.
## Checklist
- Draw/visualise the intended smooth line first.
- Fill biggest gaps with the primary AA shade.
- Fill smaller gaps with a lighter shade.
- Stop and zoom out; do not over-smooth.
## Anti-patterns
- Filling every gap with the same shade.
- Continuing to add AA past the point where the line already reads smooth.
- Placing AA on the outside of the silhouette.

---
name: line-weight-with-aa
topic: Line weight control via AA
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- Dark pixels make a line look thicker; light pixels make it look thinner/sharper. This works even on 1px lines.
- Use this to vary line weight without changing line thickness — e.g. mouths: dark lips, light dimples.
- Lighter lines on the tip of a curve can imitate brushstrokes.
- Keep the number of shades low; do not use too many.
- Line weight control is the basis of sub-pixel animation (see the Sub-pixeling chapter).
## Checklist
- Decide per line whether it should read thicker (add dark) or thinner (add light).
- Limit shades used for weight variation.
- Check the face/eyes area first — that is where line weight matters most.
## Anti-patterns
- Overdoing AA for line weight when 1–2 colours give the same result.
- Using many shades to vary weight.

---
name: banding-avoidance
topic: Banding
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 2 (pp. 38-59)"]
---
## Rules
- Banding = two rows of pixels of the same length perfectly hugging each other along an edge. It is always bad.
- Banding makes curves look blocky, makes lines appear thicker than intended, blurs the outline, and mimics pillow shading.
- Banding is often invisible zoomed in — always check at 1x/2x where it bleeds into the sprite.
- Fixes (pick one): remove a pixel or two from the edge; add a pixel or two to the edge; use darker AA shades.
- Parallel banding = several bands stacked in parallel rows. It is rare; fix by moving pixels around until the bands break up.
- Banding is sometimes unavoidable; eliminate as much as you can, then move on.
## Checklist
- Inspect edges at 1x and 2x for equal-length adjacent pixel rows.
- If banding found, apply one of the three fixes and re-check zoomed out.
- Check for parallel banding in large shaded areas.
- Confirm the outline is not blurred by the AA.
## Anti-patterns
- Judging AA only zoomed in and missing banding.
- Leaving equal-length pixel rows hugging along a curve.
- Stacking multiple parallel bands of AA pixels.
- Letting AA follow the outline perfectly, producing pillow shading.

> CHECK: OCR text for the banding fix examples (pp. 57) is partly garbled; verify the exact pixel edits shown in the book's before/after images.

<!-- 3 Colour (pp. 60-85) -->
---
name: colour-picker-models
topic: colour models for pixel art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Use the HSV/HSL model (Hue, Saturation, Value) as the default picker for pixel art work; it maps directly to how you reason about shading (hue shift, saturation shift, value shift).
- Treat "Brightness" as a synonym for Value; treat "Luminosity" as a variant where the third slider moves toward white instead of the pure hue — check which one your tool uses before copying values.
- Use RGB only when you need additive reasoning: raise all three sliders equally for greys, move sliders closer together for duller colours, raise them for lighter colours.
- Do not assume colour values look identical across programs or monitors; the same numeric colour renders differently per tool and display.
- When sharing pixel art, expect brightness/colour to vary per device and platform; verify on at least one second display before finalising.
## Checklist
- [ ] Confirm which picker layout your tool uses (square, triangle, circle) and which slider is Value vs Luminosity.
- [ ] Confirm whether your tool shows a mix preview; use it to avoid guessing intermediate colours.
- [ ] Re-check your palette on a second monitor or a different brightness setting.
## Anti-patterns
- Assuming a colour picked in one program will look the same in another.
- Judging dark colours only on your own monitor — low-brightness colours are the first to disappear elsewhere.
> CHECK: OCR lists picker layouts for MSPaint/GraphicsGale, Aseprite/SAI/Photoshop/CSP, and Pro Motion/Photoshop, but the mapping of layout to program is garbled — verify before citing.

---
name: palettes-and-colour-ramps
topic: palette construction and ramps
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Build an explicit palette when the sprite is large or uses many colours; for tiny sprites, eye-dropping from the canvas is acceptable and faster.
- Reuse the same colours across different ramps to create shared tones and harmony; shared colours are the main tool for keeping a low colour count.
- Keep one ramp per main colour family (e.g. skin, hair, cloth, metal); a ramp is an ordered light-to-dark sequence, not a random set.
- Size the ramp to the sprite: for small sprites 2-3 colours per ramp is enough — two similar colours are indistinguishable at that scale.
- Organise the palette by perceived luminosity, not by arbitrary order, so it is intuitive to pick from.
- Display format does not matter; what matters is that you personally know how to navigate the palette.
## Checklist
- [ ] One ramp per material/colour family.
- [ ] Shared colours marked and reused across ramps.
- [ ] Ramp length matched to sprite size.
- [ ] Palette sorted by perceived brightness.
## Anti-patterns
- Using many near-identical shades on a small sprite — wasted colours with no visible effect.
- Letting the palette grow unchecked on large art; you lose track of which colour is which.
- Too many shades makes animation harder: colours flash between frames when near-duplicates are used inconsistently.

---
name: hue-shifting
topic: hue shifting for shading
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Do not shade with a single hue plus black; shift the hue between the light and dark ends of each ramp.
- Default direction: shift highlights toward yellow and shadows toward purple, because yellow is the brightest hue and purple the darkest.
- Shift hue in either direction on the slider; the amount is a style choice — subtle and drastic shifts are both valid.
- Use hue shift to set mood: warm hues (red, orange, yellow) read as warm/happy, cool hues (blue, purple, teal) read as cold/sad.
- To find good shadow colours quickly, test multiply layers over the base colour, then eye-drop the results into your palette.
- Hue and saturation control are essential for both shading and anti-aliasing; do not rely on value alone.
## Checklist
- [ ] Every ramp has a hue difference between its lightest and darkest entry.
- [ ] Shadow hue chosen deliberately (warm or cool), not defaulted to black.
- [ ] Mood of the scene matches the hue direction chosen.
## Anti-patterns
- Flat ramps that only change brightness — they read as dull and lifeless.
- Shifting every ramp toward the same hue regardless of the scene's lighting.
- Shifting so far that the ramp no longer reads as one material.

---
name: saturation-shifting
topic: saturation control in shading
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Treat hue and saturation as separate tools: hue sets atmosphere, saturation directs the eye to a specific area of the shading.
- Choose one of these saturation strategies per sprite and apply it consistently:
  - Vibrant light + dull dark (most common, reads as natural).
  - Dull light + vibrant dark (reads as glowing or backlit).
  - One shade heavily saturated as an accent.
  - Mixed saturation across the ramp for a stylised look.
- Do not treat colour values as fixed numbers; experiment and judge by eye.
## Checklist
- [ ] Decide the saturation strategy before building the ramp.
- [ ] Check that the most saturated shade is where you want the viewer to look.
## Anti-patterns
- Uniform saturation across all shades — flattens the shading and wastes the tool.
- Randomly varying saturation per shade with no intent.

---
name: black-tones-and-greys
topic: black tones, greys and neutral colours
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Avoid pure black unless truly necessary; substitute dark brown, deep purple, dark green or dark grey.
- Tinting blacks is purely aesthetic, not a technical limitation — apply it for style, and vary it per sprite or per scene.
- Use greys as substitutes for colours: desaturated colours mimic how a hue looks under a different light, so greys blend into any palette.
- Use greys especially for night-time, fiery-red or toxic-green lighting palettes, where the whole scene is tinted.
- Blending two complementary colours yields near-pure grey, which makes grey a useful blending colour.
- Give shadows a colour tint, and complement the shadow colour with the highlight colour.
## Checklist
- [ ] No pure black in the palette unless justified.
- [ ] Black tone chosen to match the scene's light (purple for night, brown for warm interiors, etc.).
- [ ] Greys used where a colour would otherwise clash with the scene lighting.
## Anti-patterns
- Defaulting to pure black outlines and shadows in every sprite.
- Using the same black tone across all sprites in a game when the lighting differs.

---
name: contrast-and-readability
topic: contrast for game sprites
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Make readability the top priority when choosing colours for game sprites; a static illustration has more freedom than an in-game sprite.
- Give each character one main colour that either covers most of the body or highlights its most important features.
- Add a sub colour that contrasts strongly with the main colour to mark secondary features.
- Use contrast to separate the character from the background — this is a game-specific requirement, not an illustration requirement.
- Prefer a contrasting colour over a black outline to define details; black outlines make the sprite muddy and waste pixels.
## Checklist
- [ ] One identifiable main colour per character.
- [ ] Sub colour contrasts with the main colour.
- [ ] Sprite silhouette still reads against the actual game background.
## Anti-patterns
- Defining every detail with a black outline instead of colour contrast.
- Character colours too close to the background palette.

---
name: colour-limits-and-constrained-palettes
topic: working under colour limits
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Limiting colours is optional; do it only to replicate retro hardware, to mod an existing game, or for the challenge.
- Count transparency as one colour in the total when matching a hardware limit.
- Typical target for a single sprite: 16 colours including transparency; many sprites work well at 10.
- Reduce colours in this order: fuse similar ramps, drop barely visible shades (faint AA, near-invisible dark tones), share highlights between ramps, then merge darkest shades.
- Stop reducing when the sprite starts losing quality, colour or detail; the threshold differs per sprite — there is no universal rule.
- For scenes, reuse colours across objects; place colours from different ramps together freely.
- Keep objects that should read as separate in different colours; give objects that should read as one unit the same colour.
- For severely limited palettes, reorder the palette by perceived luminosity to make it usable, and extend it with dithering.
- Use dithering sparingly: excessive dithering makes surfaces look textured or rough.
## Checklist
- [ ] Colour count includes transparency.
- [ ] Each reduction step re-checked visually before continuing.
- [ ] In scenes, adjacent objects checked for accidental colour merging.
- [ ] Dithering density checked at 1:1 zoom.
## Anti-patterns
- Reducing colours past the point where the sprite degrades.
- Letting two objects that should be distinct share the exact same colour and touch directly.
- Heavy dithering used as a substitute for actual shading.

---
name: colour-correction-and-output-target
topic: colour correction per output medium
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 60-85)"]
---
## Rules
- Adjust colours per output target, not once for all:
  - Print: colours are severely restricted by CMYK; RGB values will shift, so fix the palette to the print gamut.
  - Web: embed an sRGB ICC profile so you can see and compensate for browser colour shifts.
  - Games: colours may not match other assets in the project; adjust even when the image looks fine in isolation.
- Revisit and revise colours throughout production; look at others' pixel art, then look back at your own, and change colours one by one if still unsatisfied.
## Checklist
- [ ] Output medium identified before finalising the palette.
- [ ] Print work converted and checked against CMYK.
- [ ] Web work previewed with sRGB profile applied.
- [ ] Game sprites compared side by side with other in-game assets.
## Anti-patterns
- Finalising a palette in RGB and sending it straight to print.
- Judging a game sprite only in isolation from the rest of the game's art.

<!-- 4 Readability (pp. 86-113) -->
---
name: sprite-size-readability-tradeoff
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Smaller sprites are harder to read; every pixel carries more meaning. At 16x16 you cannot convey subtle expressions (e.g. shock) that read easily at 32x32+.
- Choose sprite size from the smallest feature that must be visible, not from the whole design. Ask: must hands move? must the mouth animate? must facial expression read? is an item held? Then size to that feature.
- Big sprites: prioritize clean lines, solid drawing, volume, shading, anatomy. Small sprites: prioritize recognizable features and simple shapes.
- Adapt the character design to the canvas instead of forcing the original design into it. Sacrifice unimportant details from concept art or photo references.
- Shrinking a sprite makes animation look smoother and makes costume swaps cheaper, because fewer pixels change per frame.
- Above roughly 190px tall, pixel art starts to blur into "binary art" (hand-drawn-looking HD art); if you reach that point, question whether pixel art is the right medium.
- WHY: readability is clarity — how easily the viewer understands what you drew without being told.

## Checklist
- Write down the minimum visible feature before picking a canvas size.
- Test the sprite at 100% zoom, not zoomed in.
- Confirm the silhouette still identifies the character at final in-game scale.
- Confirm the sprite still reads when scaled down further (e.g. shrinking Yoshi in Mario Kart).

## Anti-patterns
- Adding every detail from the concept art into a small sprite (produces mud).
- Assuming a bigger canvas automatically fixes readability — it does not; a sprite can always be improved at any size.
- Reducing frame count to keep a high-res look; it reads as cheap.

> CHECK: exact pixel dimensions of the Cryamore original (~190px) vs reduced (~130px) are from the OCR and should be verified.

---

---
name: pixel-placement-and-minimal-features
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Treat every pixel as load-bearing at low resolution: moving 1-2 pixels can flip the interpretation of the whole sprite.
- To fix a misread sprite, change as little as possible first. Example: adding a 2px line for a Game Boy cartridge slot turned "boy holding a cup" into "boy holding a Game Boy".
- Diversify characters with tiny edits to a few features only. The Kunio-kun series differentiated characters by adjusting only eyes and hairstyles within ~6x6 px areas.
- Keep small sprites simple: flat shapes over line art, few details, strong shapes.
- Iterate: produce multiple versions of a sprite and, if undecided, let other people pick.
- WHY: at small sizes a single pixel's color and position changes the whole read, so minimal, targeted edits are the safest fix.

## Checklist
- When a sprite misreads, list the 2-3 pixels causing the ambiguity before redrawing.
- Verify the fix did not create a new misread (e.g. cup becomes beard or flute).
- Keep a version history of the sprite so you can compare reads side by side.

## Anti-patterns
- Redrawing the whole sprite drastically to fix one ambiguity — risks new readability problems.
- Adding detail to "explain" the shape; extra pixels usually add mud instead.

---

---
name: hands-and-eyes-as-symbols
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Draw hands as flat mitten shapes first, then add detail. Do not start with line art at small sizes.
- The index finger plus opposable thumb define a human hand; those two are enough to show gripping, pinching, and pointing.
- Draw 3 fingers + thumb when space is tight; draw 5 only when there is room.
- Separate fingers with different shades/brightness rather than outlines; use highlights and shadows for volume.
- If stuck or on a deadline, draw the hand at high resolution in a paint program, shrink it, and use it as reference (study the resulting anti-aliasing).
- Eyes are the first thing viewers look for; polish them on every character sprite, humanoid or animal.
- If there is no room for eyes (they would be under 1px), omit them and suggest the eye area with shadow instead.
- Glasses: pick one — render the frames and drop the eyes, or render the top of the frame and drop the bottom.
- A single white shine pixel, or AA/sub-pixel shading, changes the eye's expression; test at 100% zoom.
- WHY: faces and hands carry identity and intent, so they are the highest-value pixels to get right.

## Checklist
- Zoom out to 100% before judging eye or hand readability.
- Check that the thumb and index finger are distinguishable.
- Check that no finger blends into the palm or an adjacent finger.
- Check the eye shine reads at final scale.

## Anti-patterns
- Attempting per-finger line art at small sizes.
- Outlining every finger instead of using value separation.
- Leaving eyes unpolished because the sprite is "just a small one".

---

---
name: proportions-silhouette-and-color-design
topic: Character Design
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Big heads give room for expression and identity; realistic proportions shift the focus to body language, volume, shading and anatomy.
- Match proportions to the sprite's function: overworld, battle, dialogue portrait, icon, and cutscene sprites legitimately use different proportions for the same character.
- Design a clear silhouette first, then fill it with detail. The silhouette must show head, limbs, and cloth.
- Avoid overlapping elements in the silhouette; when overlap is unavoidable, separate features with color contrast.
- Limit each character to 2-3 main colors (one primary, one secondary). This makes the design recognizable and readable.
- Assign colors by meaning: a color that misrepresents a feature causes misreads (orange nose on a bat reads as a beak; orange Yoshi arms read as saddle stirrups).
- Diversify poses and body proportions to give bodies personality.
- WHY: silhouette and color are the two cues that survive at small scale and in motion.

## Checklist
- Fill the silhouette with a single flat color and check it is still identifiable.
- Count the main colors; if more than 3, cut.
- Check each color against the feature it represents (does the nose color read as a nose?).
- Check the sprite reads in every pose it will use.

## Anti-patterns
- Overlaying limbs or props without a contrast break.
- Using a color for a body part because it "looks nice" rather than because it describes the part.
- Reusing one proportion set for all sprite roles in the game.

---

---
name: light-shadow-and-spacing
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Replace outlines with value contrast where space is tight: dark pixels fill the silhouette and separate features, bright pixels highlight edges and key details.
- Light and dark can swap roles depending on background color and light source; use both together for shape, volume and depth.
- Spacing: leave a gap between adjacent features. A mouth needs clear space above and below it, or it stops reading as a mouth.
- Remove in-lines (internal black outlines) when they hinder readability.
- Fix tangents by moving or resizing areas, not by adding pixels. Example: give hair 2px of width by shifting part of the face, or move the ear to free space for the eyes.
- When the palette lacks a needed tone, substitute the nearest available tone (e.g. darkest skin tone for dark brown hair) and re-check the read.
- WHY: touching shapes merge visually, and in-lines plus tangents destroy the separation the viewer needs.

## Checklist
- Scan the sprite for any two features that touch; add at least 1px of separation.
- Check for in-lines and delete the ones that do not carry information.
- Check for tangents where an edge runs parallel and close to another edge.
- Test multiple spacing variants before committing.

## Anti-patterns
- Letting a mouth touch the chin or nose.
- Keeping in-lines "because they were in the reference".
- Fixing a tangent by shrinking the feature instead of relocating it.

---

---
name: sprites-on-backgrounds
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Sprites must always stand out from backgrounds for gameplay clarity. Decide explicitly what the player should focus on.
- Use three techniques, ideally together: (1) give sprites and objects clear outlines, (2) shift background colors to be softer/lower contrast than the foreground, (3) blur or reduce detail in the background so it is out of focus.
- Apply the same separation logic outside games (photography, illustration) — it is a readability rule, not a game rule.
- WHY: if foreground and background share value or saturation, the player cannot parse the play space.

## Checklist
- Check sprite vs background contrast in grayscale.
- Check that background saturation and detail are lower than the sprite's.
- Check that outlines exist on interactive objects.

## Anti-patterns
- Detailed, high-contrast backgrounds behind small sprites.
- Relying on color alone for separation without value contrast.

---

---
name: aa-dithering-and-readability-testing
topic: Readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 4 (pp. 86-113)"]
---
## Rules
- Use anti-aliasing moderately to clean curves and improve clarity; it costs space, so skip it when space is tight.
- Avoid dithering on small sprites. Dithering makes small sprites look rougher and less smooth; reserve it for large pixel art, textured surfaces, or tight palette limits.
- Test readability with a permanent 1x (100%) preview while working.
- Test by blurring the image: if it looks bad blurred, fix the pixel version. Blurring also reveals banding.
- Test by upscaling (e.g. Waifu2x) to expose bad curves and jaggies, then fix them in the pixel version.
- Ask another person what the sprite is without telling them the intended subject; prefer someone with little pixel art experience.
- WHY: artists judge sprites at high zoom, but players see them small, blurred, and in motion.

## Checklist
- Keep a 100% preview open at all times.
- Run a blur test and an upscale test before finalizing.
- Run a blind identification test with a second person.
- Re-check curves after any AA change.

## Anti-patterns
- Judging readability only at 800% zoom.
- Using dithering to shade a 16x16 sprite.
- Shipping a sprite nobody else has identified correctly.

<!-- 5 Dithering (pp. 114-133) -->
---
name: dithering-purpose-and-tradeoffs
topic: When and why to use dithering in pixel art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- Use dithering only when you must fake extra shades with a limited palette; with unlimited colours, prefer clean cel-shading. WHY: dithering adds grain that reads as noise when it isn't needed.
- Keep dithering contrast low between the two mixed colours. WHY: high-contrast dithering looks harsh and the pattern becomes visible instead of blending.
- Never animate dithering. WHY: the pattern shifts between frames and produces wobbling, distracting motion.
- Reserve dithering for static, large areas: skies, space, vast backgrounds, textures. WHY: it needs space to read as a gradient and it hurts sprite readability.
- Prefer clean solid shapes for small sprites and tilesets. WHY: dithering eats the few pixels available and destroys silhouette clarity.
- Use dithering sparingly overall — "less is more". WHY: it is time-consuming and clashes easily with other visuals.
- If you have no colour limit, you may still dither a small highlight or buffer-shade inside an otherwise cel-shaded drawing. WHY: it imitates soft shading without abandoning the cel-shaded look.

## Checklist
- Does this area have enough space for the pattern to read as a gradient?
- Is the contrast between the two mixed colours low?
- Is the surface static (no animation)?
- Would a solid shape or an extra shade solve this instead?
- Does the dithering stay invisible at 100% zoom and only blend at a distance?

## Anti-patterns
- Dithering a small animated sprite.
- Dithering high-contrast colour pairs.
- Dithering everywhere "because retro".
- Using dithering to fake a gradient in a 2-3 pixel wide band.

---
name: checkered-dithering
topic: Checkerboard dither patterns and gradient levels
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- Build gradients from a fixed ladder of checker patterns: sparse checker → denser checker → cross → solid square → diamond, and so on. WHY: each brightness level has a known pattern, so you never get lost mid-gradient.
- Choose the number of intermediate levels between two shades based on gradient length and available shades; it is a preference call. WHY: more levels suit long gradients, fewer suit short ones.
- When freestyling large areas, never allow a 2x1 run or two horizontally touching pixels. WHY: wide pixels break the checker rhythm and read as a different, wrong pattern.
- For curves, test the result and expect double pixels; if they appear, select the existing dither block and slide it rather than redrawing. WHY: sliding preserves the pattern and is faster than rebuilding.
- If dithering sits inside a tileset, tiles are always an even pixel count, so double pixels may be unavoidable — provide two different tile variants. WHY: two tiles let the pattern continue correctly across the seam.
- Checkered dithering is the best choice for gradients over large areas. WHY: it distributes both colours evenly and blends smoothly.

## Checklist
- Pattern ladder consistent across the whole gradient?
- No 2x1 or touching horizontal pixel pairs?
- Curve seams checked for double pixels?
- Tileset seams covered by a second tile variant?

## Anti-patterns
- Mixing pattern types randomly inside one gradient.
- Redrawing a whole curve dither when sliding a block would fix it.
- Using one tile variant where the seam forces a double pixel.

---
name: line-and-dent-dithering
topic: Parallel lines, discontinued lines, dents
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- Use parallel lines for smears, blur and buffer-shade/opacity tricks, not for gradients. WHY: lines read as motion blur better than checkerboards do.
- Use parallel lines only for limited animation, never for smooth animation. WHY: the line pattern breaks apart when it moves.
- Use discontinued (broken) lines when you need more distinct value levels than plain parallel lines give. WHY: breaking the lines adds intermediate steps and a distinct look.
- Use dents — a single row of checkerboard — for textures when space is tight. WHY: one row is enough to suggest material without a full gradient.
- Do not use dents for gradients. WHY: a single row cannot express multiple brightness levels.

## Checklist
- Is the target a blur/smear or a gradient? (lines vs checkers)
- Is the animation limited-frame or smooth?
- Do you need more than two intermediate values? (discontinued lines)
- Is space too tight for a full checker gradient? (dents)

## Anti-patterns
- Parallel lines used as a sky gradient.
- Line dithering on a smoothly animated sprite.
- Dents used to build a multi-step gradient.

---
name: intertwined-and-random-dithering
topic: Woven/overlapping dither and randomized dither
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- For intertwined (woven) dithering, build two separate dither layers and let them overlap. WHY: two layers prevent you from losing track of which patch belongs to which gradient.
- Keep the light-to-dark flow seamless even when patches overlap. WHY: the eye must still read one continuous gradient.
- Avoid hand-placed random dithering in most cases; if you use it, convert it into a repeating tile or pattern. WHY: loose random pixels read as noise and look lazy.
- If random dithering comes from a filter, spray tool or photo reduction, clean it up manually. WHY: automatic output is not handcrafted pixel art and needs control.
- Random dithering is acceptable on very large canvases where the noise averages out. WHY: at large scale the eye blends it into a gradient.

## Checklist
- Two layers used for the woven sections?
- Gradient direction still readable across overlapping patches?
- Random noise converted into a repeating tile?
- Filter output manually corrected?

## Anti-patterns
- Loose random pixels on a small sprite.
- Shipping raw auto-dither output untouched.
- Overlapping patches that reverse the light-to-dark direction.

---
name: stylised-dithering-and-texture
topic: Stylised dithering, textures vs gradients
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- Use stylised dithering — custom shapes, motifs, controlled randomness — to get gradients without the gritty feel. WHY: a deliberate motif reads as intent, not noise.
- Reserve stylised dithering for large areas; it needs space. WHY: the motif must repeat enough times to be recognised.
- Separate the two goals: gradients are light-to-dark transitions, textures are the feel of a material. WHY: confusing them produces muddled art.
- Textures do not require a gradient. WHY: a material can be flat in value and still read as a texture.
- Dithering can suggest texture only in patches, not as a full gradient. WHY: a repeating motif reads as surface, not as shading.
- Convert random dither into a repeating tile set to control it. WHY: controlled randomness stays readable and reusable.

## Checklist
- Is this a gradient or a texture? Pick one goal per area.
- Does the motif repeat enough to be recognised?
- Is the area large enough for the motif?
- Does the texture need a value gradient at all?

## Anti-patterns
- Using a texture motif as a shading gradient.
- Stylised dithering on a tiny sprite.
- Random noise presented as a texture.

---
name: dithering-tools-and-workflow
topic: Dither brushes, HD index painting, manual cleanup
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 5 (pp. 114-133)"]
---
## Rules
- Use dither brushes/patterns in your editor (Aseprite, GraphicsGale, Pro Motion) instead of copy-pasting checker blocks. WHY: it removes the most time-consuming part of dithering.
- Aseprite: create a brush with CTRL+B. WHY: it is the built-in shortcut for custom brush creation.
- For Photoshop workflows, consider Dan Fessler's HD Index Painting technique to make dithering easier to manipulate. WHY: it keeps indexed-colour control while painting.
- Always manually fix the result of any brush or filter. WHY: pixel art is about control; automated output is a starting point, not a finish.
- Study dithering usage in shipped game art to calibrate how much and how strongly to use it. WHY: observation is the fastest way to learn the right dosage.
- Shade with clean shapes first; add dithering only afterwards if still needed. WHY: solid shapes are the safer default and dithering is an optional layer.

## Checklist
- Dither brush or pattern set up in the editor?
- Automated result reviewed pixel by pixel?
- Reference game art checked for dosage?
- Clean-shape version tried before dithering?

## Anti-patterns
- Hand-placing every checker pixel when a brush exists.
- Trusting a filter or brush output without cleanup.
- Adding dithering before the base shading is solid.

> CHECK: OCR lists "Pokémon Mystery Dungeon 3: Explorers of the Sky (NDS)" and "Pokémon Mystery Dungeon 3: EoS (NDS)" — verify the exact game title and platform before citing it as a reference.

<!-- 6 Game Perspectives (pp. 134-160) -->
---
name: choosing-a-game-perspective
topic: game perspective selection
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- Treat every 2D game view as a pseudo-3D projection: it implies length, width and depth but is drawn on a flat 2D field. Pick the projection that serves gameplay first, then make art match it.
- Use orthographic/multiview views (side, top-down, top) when you want simple collision, tile-friendly level building and no vanishing points.
- Use paraline views (isometric, 45° dimetric, oblique) when you need to show 3 sides of objects and verticality (towers, plateaus, height-based gameplay).
- Use true perspective (vanishing points, sprites scaling with distance) only when the game design justifies the extra art/programming cost; most engines must resize sprites automatically because manual scaling is too expensive.
- Match the view to the movement axis: side view = 1 plane, horizontal + vertical movement; top-down = free roaming on a square grid; isometric = diagonal movement on a diamond grid.
- Keep the player's travel line consistent: in side-scrollers the character stays on a single 2D path even when the art suggests up/down movement.
- Add parallax scrolling to orthographic views to fake depth, since they have none.
- When in doubt, choose the view that makes collision and level authoring easiest; free-form art that can't be turned into a playable map is a programming nightmare.

## Checklist
- Does the chosen projection support the core movement (1 axis, 4 directions, 8 directions, free roam)?
- Can the level be built from a tile grid, or does it need free-form art with hand-made collision?
- Are vertical structures (towers, cliffs) important? If yes, prefer paraline over pure top view.
- Is the camera angle readable for the player at all times (can they tell where they are walking)?
- Will sprites need to scale with distance? If yes, budget for engine-side scaling.

## Anti-patterns
- Picking a view for looks and then fighting it during level design or collision authoring.
- Using true perspective in a 2D game without automatic sprite scaling — the illusion breaks.
- Drawing free-form backgrounds that cannot be converted into a collision map.
- Assuming a "realistic" top-down view will look good; a truthful 90° top view hides the character's face and reads poorly (see the top-view card).

---
name: orthographic-multiview-views
topic: orthographic projections
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- Orthographic = flat views with no perspective and no vanishing points; parallel lines stay parallel and scale does not change with distance.
- Only 1 or 2 planes are visible; gameplay happens on a single 2D plane.
- Everything sits on a perpendicular 90° grid: vertical and horizontal lines form right angles.
- Treat the grid as a guideline only — you may draw objects at any angle you like.
- Side view variants: cross-section (camera directly in front, world is a slice), top-down-ish (camera slightly above ground), oblique (front flat, sides slanted). The character's travel line never changes.
- Side views suit corridor-type levels and platformers/shoot-'em-ups.
- Top-down view uses square tiles, which makes world building fast; it suits free-roaming overworlds and exploration.
- Top-down camera angle is a dial: front > top (beat-'em-ups), front ≈ top (common, easy tile sets), top > front (good for showing altitude).
- Top view (exactly 90° straight down) is rare and only fits aerial gameplay, maps, blueprints or floor plans; it lacks depth.
- If height matters, prefer top-down, dimetric or planometric oblique over pure top view.

## Checklist
- Is the grid 90° and consistent across all tiles?
- Does the visible plane count (1 or 2) match the gameplay needs?
- For side-scrollers: is the character locked to one path, and does the art avoid implying free vertical movement?
- For top-down: is the camera angle chosen deliberately (front-heavy vs top-heavy) and applied consistently?
- Is parallax used to compensate for missing depth?

## Anti-patterns
- Mixing camera angles between areas without a design reason (see the Zelda perspective problem card).
- Using pure 90° top view for gameplay that needs to communicate height.
- Letting the 90° grid constrain art so much that objects look stiff — the grid is a guide, not a law.

---
name: zelda-perspective-problem
topic: mixing top-down and 1-point perspective
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- A room drawn in 1-point perspective (camera directly above, walls visible) is geometrically correct, but sprites drawn at a 45° tilt are not — they only look right near the north wall.
- Near the south wall the same sprite reads as if the character is lying on the floor; flipping the screen upside down makes the error obvious.
- Accept this as a deliberate cheat: keep the room in 1-point perspective and the objects in top-down 45°, because a technically correct character (seen from above) would be unreadable.
- If walls block the view of the play area, delete them and create an invisible "4th wall"; some games keep walls, others remove them to show more floor.
- Keep overworld and dungeon views consistent in style even if their projections differ, so the player isn't disoriented.

## Checklist
- Are sprites near the south wall still readable?
- Do walls hide gameplay-relevant floor? If yes, remove or fade them.
- Is the perspective cheat applied consistently across all rooms?

## Anti-patterns
- Trying to make sprites geometrically correct for a 1-point room — the character becomes unreadable.
- Mixing perspective styles randomly between rooms without a gameplay reason.

---
name: paraline-views-isometric-dimetric-oblique
topic: paraline / axonometric projections
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- Paraline views show 3 sides of an object at all times, use true measurements, and are seen from a bird's-eye view.
- Isometric: all axes equal; focuses on all planes (top + sides); grid is diamond-shaped.
- Dimetric (45° dimetric): only 2 axes equal; focuses on the horizontal (top) plane; guidelines are 1x1 pixel steps at 45°, vertical axis stays 90°.
- Oblique: front plane is flat/orthographic, all other planes slant and stay parallel; usually 45° (1x1), sometimes 2x2 or 3x3 lines. Think "side-scroller + 2 more planes".
- Isometric pixel art cannot use exact 30° lines; use 2-pixel stairs (≈26.5°), which is the closest practical approximation and makes world construction easier.
- Isometric diamond tiles do not align to square grids; free-form diamonds look cleaner but are hard to tile. Tiled diamonds align perfectly but produce chunky double-pixel crossings.
- To avoid chunky crossings, draw diamonds as lineless shapes (checkerboard style) instead of outlining lines.
- One diamond spans 2 square tiles; every other adjacent diamond spans 4 tiles.
- Always use a grid as a guide, whether or not you ship tile sets.
- To convert a top-down map to oblique, skew it vertically by 45° (1 unit) instead of 30°.
- To convert a side-scroller sprite to isometric: skew by 30° (0.5), then move parts to add depth, then clean up. Skew in the direction the object faces — never the opposite way.
- When skewing a square to isometric, pre-scale the length by cos 30° ≈ 0.866 (≈87%) so the diamond keeps equal sides after skewing.
- Terrain: most isometric fields are flat; slopes are rare in 2D games. In grid RPGs with 4-direction movement, slopes only appear in 4 directions.
- 45° dimetric is uncommon but useful when tall structures would otherwise block gameplay; it is sometimes called axonometric/plan/military/planometric oblique.

## Checklist
- Is the grid diamond-based and consistent (2-pixel stairs for iso, 1x1 for 45° dimetric)?
- Are crossings handled with lineless shapes rather than outlines?
- If converting sprites: skew direction matches facing, and length pre-scaled to ~87%?
- Does the level need slopes? If yes, confirm the movement system supports the required directions.
- Can the art be turned into a collision map?

## Anti-patterns
- Outlining isometric diamonds with lines — produces chunky double-pixel intersections.
- Skewing sprites the wrong way (against their facing direction).
- Forgetting the cos 30° (~87%) pre-scale, leaving diamonds with unequal sides.
- Building free-form isometric backgrounds that cannot be converted into a playable, collidable map.

---
name: true-perspective-and-scaled-sprites
topic: true perspective in 2D games
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- True perspective uses vanishing points; objects skew toward the vanishing point and shrink with distance.
- Non-game pixel art follows normal art/painting perspective rules; game pixel art usually does not.
- 2D games can use perspective, but sprites must grow and shrink with distance — manual scaling is too costly, so use engine-side automatic resizing.
- 3D environments with sprite textures can be manipulated to imitate a traditional top-down view.
- In-game illustrations (cutscenes, backgrounds) can freely imitate true perspective without affecting gameplay.

## Checklist
- Does the engine support automatic sprite scaling before committing to a perspective view?
- Are scaled sprites still readable at the smallest and largest sizes?
- Is perspective used only in illustrations/cutscenes where it won't break gameplay readability?

## Anti-patterns
- Hand-scaling every sprite for distance in a 2D game — unsustainable.
- Using true perspective for gameplay space when the player must judge positions precisely.

---
name: top-view-readability-and-faking
topic: top-down readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- A truthful 90° top-down view shows only the top of the character's head, making the protagonist hard to identify and the scene uninteresting.
- Fake the top-down view: tilt many objects (fences, trees, props) at ~45° so they read better, even though the ground plane stays top-down.
- This faking technique is long-standing practice (e.g. DS Pokémon games tilt fences and trees at 45°).
- When a large structure is ambiguous from the only angle it's ever seen, flip it vertically or adjust it until it can't be misread (example: Chrono Trigger's Black Omen reading as a tower).
- Always get outside feedback on readability — the artist knows what the object is meant to be, the player does not.

## Checklist
- Can the player identify the protagonist from the top-down view?
- Are props tilted/faked so they read as 3D objects rather than flat shapes?
- Is any large structure ambiguous from its only visible angle?
- Has someone unfamiliar with the art confirmed it reads correctly?

## Anti-patterns
- Rendering a literal 90° top-down view with no faked angles — it looks flat and confusing.
- Assuming your own reading of an ambiguous sprite matches the player's.

---
name: constructing-objects-with-guides
topic: object construction in perspective
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- Two approaches: eyeball (fast, estimate measurements, deconstruct into simple geometric shapes) or construct (slower, precise, uses guidelines). Learn to construct first so your eyeballing becomes reliable.
- Build complex objects from primitives: cube, cylinder (tree stump, barrel), pyramid (roof, tent), cone (tree, tower), sphere (mushroom, bowl).
- Circle on a horizontal plane: draw the square, draw the medians, draw an oval around the square, then draw the circle within.
- Circle on a vertical plane: same principle, adapted to the vertical plane's skew.
- Finding the tip of a cone/pyramid: use the base's medians and extend to the apex.
- For organic forms (e.g. a tree), block in rough ovals as a skeleton, outline the outer shape of the ovals to get leaf rows, adjust ovals if the outline fails, then block shapes, define details and shading, and finally add highlights and shadows.
- This deconstruction method works for any perspective, not just isometric.

## Checklist
- Are guidelines/grid in place before drawing details?
- Is the object reducible to one or more primitives?
- For circles: square + medians + oval + inner circle?
- For organic shapes: ovals blocked first, outline derived from them?
- Details and shading added only after the block shape is correct?

## Anti-patterns
- Eyeballing everything without ever learning construction — errors compound and are hard to diagnose.
- Detailing and shading before the underlying block shape is correct.
- Drawing circles freehand without the square/median/oval guide.

---
name: showing-scale-in-2d
topic: conveying scale
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 6 (pp. 134-160)"]
---
## Rules
- 2D games usually view the world like looking into a shoebox from the top or side, because those are the easiest camera angles to play.
- Low-angle shots are near-impossible for gameplay in 2D: the player can only move left/right and cannot tell where they are walking. In 3D the player can move the camera back down, so low angles work there.
- Use low-angle shots only in cutscenes as a storytelling device to convey mood and scale.
- To convey scale in gameplay, split the view into 2 planes, use Mode 7-style scaling, or spread graphics across 2 screens.

## Checklist
- Is any low-angle shot confined to a cutscene?
- Does the gameplay view keep the player oriented at all times?
- Are scale tricks (2 planes, scaling, dual screens) used deliberately rather than as a gimmick?

## Anti-patterns
- Using low-angle shots during gameplay in a 2D game — the player loses spatial orientation.
- Relying on camera tricks for scale when the level design itself doesn't communicate size.

<!-- 7 Clean-up (pp. 161-186) -->
---
name: cleanup-workflow-rough-to-final
topic: Pixel art clean-up workflow
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- Treat clean-up as a distinct final pass, not part of the initial drawing. Revise roughs and re-draw over them with detail, mirroring 2D animation clean-up.
- Standard pipeline: rough sketch → base flat colours → shading → details → clean-up. Follow this order regardless of whether you start from a paper sketch or a pixel-brush rough.
- Expect the final sprite to diverge from the sketch. Capcom-style sprites (JoJo's, Street Fighter) were digitized from paper and changed heavily at the line-art and shading stages. Do not cling to the original sketch.
- When the canvas is cramped, drop line-art and build with shapes of light/shadow instead. Lines only help when constructing geometric structure.
- For in-between animation frames, use blobs of colour rather than lines — you work with light and shadow, which is faster.
- Establish one area first (e.g. the coat) to lock in style, palette and lighting, then propagate that style to the rest.
- Revisit finished areas as you go. Moving parts with the selection tool and redrawing from scratch mid-process is normal.
- Set the light source at the sketch stage so colours for characters and background can be chosen together, instead of starting from white and doing the background last.
- Self-assess in addition to taking external feedback. Most changes happen at the very end, after critique or self-critique.
- Do not hesitate to improve a sprite you consider "done".

## Checklist
- [ ] Rough sketch exists (paper or pixel brush)
- [ ] Flat colours laid over sketch
- [ ] One area fully detailed to establish style/palette/lighting
- [ ] Light source defined before colour picking
- [ ] Shading pass done with shapes, not just lines
- [ ] Detail pass done
- [ ] Clean-up pass: re-draw over roughs
- [ ] Final self-critique and external feedback round

## Anti-patterns
- Treating clean-up as optional or skipping it because the sprite "looks fine".
- Committing to the original sketch when the pixel version needs different proportions or shapes.
- Relying on line-art on a cramped canvas where lines can't describe form.
- Doing the background last from a white base instead of choosing colours against the established light source.
- Assuming all changes are improvements for every viewer — art is subjective; some audiences prefer the old version.

---
name: cleaner-shapes-clusters
topic: Shape/cluster language in pixel art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- Treat pixels of the same colour as clumps (clusters, chunks, blocks). Clean, well-crafted clusters make a sprite more readable.
- Aim for the readability of clean-cut art (Castlevania: SotN) over noisy art (Lemmings). Cleaner shapes are more believable as textures.
- Test: reduce a sprite to ~5 unique colours. If the shapes still read, the shape language is good.
- Avoid "lazy lines" (Walt Stanchfield's term): lines/shapes that describe nothing — no shape, texture, softness or hardness. Tracing produces this overall sameness.
- Apply the same shape discipline to shading: light and shadow areas start as shapes, even in highly detailed pieces.
- Anti-aliasing does not replace good shapes. AA only softens lines and shapes; drawing skill is the deciding factor.
- Dithered artwork is also made of shapes — dithering blends the cel-shading bands.
- Shape quality is subjective; study other artists' work (e.g. Pixelation.org community, Marco Bucci's "Good Shapes" series) rather than assuming one correct answer.

## Checklist
- [ ] Every cluster describes something (form, texture, light, shadow)
- [ ] No stray single pixels that read as noise
- [ ] Sprite still reads when reduced to ~5 colours
- [ ] Shading areas are deliberate shapes, not arbitrary fills
- [ ] AA used only to soften, not to rescue bad shapes

## Anti-patterns
- Dithering that reads as random noise (e.g. Knuckles' red dithering around the mouth in the Sonic 2 sprite) — remove it if it doesn't read.
- Judging quality by how clean each individual cluster is rather than how the whole piece assembles.
- Using AA as a crutch for weak drawing.

---
name: adjusting-sprites-aspects
topic: Sprite adjustment aspects
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- When adjusting a sprite, evaluate these aspects: silhouette, design, colours, pixel shapes, lighting, readability. This is not a strict checklist — more aspects exist beyond the book.
- Silhouette: widen and distinguish it. Fire Emblem's Bonewalker gained a bigger skull, a more 3D sword and readable pelvis cloth.
- Detail space: a bigger skull allowed subpixels for eyes and mouth. Enlarge a feature when it needs subpixel detail.
- Lighting: pronounce highlights and shadows even when the palette barely changes (Bonewalker, Pulseman drill platform). Shading must respect the light source; the old Pulseman platform ignored it.
- Outline shading: shade the outline itself and round the edges to make an object read as more 3D.
- Cast shadows: show one part casting a shadow onto another (drill platform onto the red piece).
- One pixel can make a difference: a single white pixel changed the pupil size in Drawn to Life's Frostwind boss.
- Face clean-up: make eye sockets geometric (e.g. 90°), widen smiles so they separate from the nose, add AA to the jaw and smooth the outline (Pokémon Platinum's Barry).
- Simplify similarly-coloured pixel shapes; smaller, more readable hands (Barry).
- Design changes to suit taste are out of scope for this book — don't treat them as clean-up.

## Checklist
- [ ] Silhouette distinguishable and wide enough
- [ ] Highlights/shadows pronounced, light source respected
- [ ] Outline shaded, edges rounded where 3D form is wanted
- [ ] Cast shadows present where objects overlap
- [ ] Single-pixel details (pupils, eye highlights) checked
- [ ] Face: eye socket angle, smile separation, jaw AA
- [ ] Similarly-coloured shapes simplified

## Anti-patterns
- Changing pixels without checking the silhouette first.
- Shading that ignores the light source.
- Assuming every change is an improvement for all viewers — art is subjective.

---
name: multiple-versions-and-selection-tool
topic: Iteration and editing tools
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- When unsure which variant looks better, produce multiple versions and let others vote. Alone, take a break and compare with fresh eyes.
- For big uncertainty (posture, mood), do multiple full sketches rather than pixel-level variants.
- If nothing works at small size, think outside the box and start fresh.
- Use the selection tool to move parts instead of redrawing from scratch — it saves significant time and fixes off-model work.
- Use the lasso tool for irregular selections, but ensure it is aliased (not anti-aliased) or it will produce soft edges.
- Tweak and fix things as you go; pixel art is easy to edit, so proportions can be fixed even at the very end.
- Use the selection tool to fix perspective: e.g. show more of a barrel's top lid and less of the cylinder.
- To check perspective consistency, place sprites next to each other and compare.

## Checklist
- [ ] Multiple versions made for uncertain details (e.g. mouth open vs closed)
- [ ] Selection/lasso tool used for moving parts before redrawing
- [ ] Lasso tool set to aliased
- [ ] Proportions checked at the end
- [ ] Perspective checked by placing sprites side by side

## Anti-patterns
- Redrawing pixels from scratch when a selection move would do.
- Using an anti-aliased lasso, which produces soft edges.
- Committing to the first variant without comparison.

---
name: scaling-rotating-cleanup
topic: Scaling and rotating sprites
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- When shrinking a sprite, sacrifice detail and prioritise readability (see the Readability chapter, "Size Matters").
- A naive resize produces a pixelated mosaic. Use it as a base and redraw important features and lines over it.
- Expect heavy eyedropper/pencil switching during resize clean-up.
- Prefer starting big and going smaller over the reverse. Enlarging is more of a drawing task than a clean-up task.
- Rotated sprites are the most common clean-up case (body parts, backgrounds). Same process: chisel and add pixels while eyedropping and redrawing over the rotated result.
- Shrinking sprites is one of the best exercises for learning intuitive pixel placement.

## Checklist
- [ ] Resized base used only as reference, not final
- [ ] Key features and lines redrawn
- [ ] Readability checked at final size
- [ ] Rotated parts chiselled and re-pixelled

## Anti-patterns
- Shipping the raw resized mosaic.
- Scaling up and expecting clean-up to be quick — it becomes a full drawing task.

---
name: sharpness-and-contrast-tweaks
topic: Sharpness, contrast and final tweaks
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 7 (pp. 161-186)"]
---
## Rules
- Do not use sharpen filters. Apply sharpening manually.
- Sharpness is not only fuzziness/clearness — colour, contrast and shapes all contribute.
- Method 1: rely on light and shadow rather than line-art. Line-art hands produce unreadable colour splotches; clean shapes with higher contrast read better.
- Method 2: add more highlights.
- Method 3: add darker lines to make elements pop.
- Contrast can be changed without moving any pixels: recolour every ramp, or use colour sliders then manually fix. Contrast covers mood, hue, saturation and values.
- Tangents: tangent outlines stand out as a flaw in comics/storyboards. In animation you can get away with them, so don't worry there.
- Light & shadow: touching up colours is not enough — fix light sources, highlights, shadows and areas by playing with shapes.
- Character modelling: reference model sheets when adding or reducing detail, to make judgement calls.
- Line weight: lighter line-art at the bottom of a sprite implies line weight that a pure black outline cannot show.
- Only apply these tweaks if you feel they are necessary.

## Checklist
- [ ] No sharpen filter used
- [ ] Light/shadow used instead of line-art where readability suffers
- [ ] Highlights added
- [ ] Darker lines added to make elements pop
- [ ] Contrast checked across mood, hue, saturation, values
- [ ] Tangent outlines checked (ignored for animation)
- [ ] Model sheet referenced for detail changes
- [ ] Line weight varied (lighter at bottom)

## Anti-patterns
- Applying a sharpen filter.
- Relying on line-art alone for readability.
- Adjusting colours without also fixing light sources and shadow shapes.
- Leaving tangent outlines in a static sprite.

<!-- 8 Subpixeling (pp. 187-212) -->
---
name: subpixeling-fundamentals
topic: Subpixeling basics and pixel shifting
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- Treat a pixel as the smallest addressable unit; you cannot split it. Subpixeling fakes motion smaller than 1 px by redistributing a pixel's value (brightness/colour) into neighbouring pixels.
- Model pixel shifting as pouring water between cups: total value stays constant, only distribution changes. Moving a pixel ~0.5 px ahead darkens/lightens the adjacent pixel.
- Subpixels do not have to be exactly 50% shifts. Any intermediate value works; pick a colour that sits roughly between the two source colours.
- Reuse colours already present in the sprite palette for subpixels. Only create new transition colours when the palette genuinely lacks a usable in-between.
- Use 1–2 AA shades for subpixeling. More shades smooth transitions but are rarely needed.
- Subpixel only the areas that benefit. Leave other pixels completely still — moving every pixel causes banding and hurts readability.
- Direction rule: subpixels follow the angle of the shape, not the direction of the overall motion. Horizontal angle → horizontal subpixels; vertical angle → vertical subpixels.
- Diagonal subpixel movement is a combination of horizontal and vertical carry-over. Approximate the 45° direction; it does not need to be mathematically exact.
- When a shape moves away it can leave a "ghost" AA shell behind. Never leave light-coloured AA on an outline.
- Subpixeling is about movement, not shading. Do not confuse it with animated shading/light.
- Workflow: duplicate the frame, edit it slightly, then flip back and forth between frames to verify the shift reads correctly.
- For in-betweens that appear on screen only briefly, funky-looking frames are acceptable. Never let a rough subpixel in-between stay on screen long.
## Checklist
- [ ] Palette contains the AA colours needed (no unnecessary new colours added)
- [ ] Only 1–2 AA shades used for the shift
- [ ] Subpixel direction matches the angle of the shape being moved
- [ ] Non-moving pixels left untouched
- [ ] No light AA left on outlines
- [ ] Frames flipped back and forth to confirm the illusion reads
## Anti-patterns
- Shifting every pixel on the canvas → banding, unreadable motion.
- Using math to compute exact subpixel colours instead of eyeballing an in-between colour.
- Treating subpixeling as moving shading/light.
- Overdoing subpixeling → sprite looks like it is melting or made of jelly.
- Leaving light-coloured AA on an outline after a shape moves away.

---
name: subpixeling-use-cases
topic: When to use subpixeling
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- Use subpixeling for easing in/out: when in-betweens must be spaced very close together, subpixel them to avoid wobble.
- Use subpixeling to give life to still parts during large movements, so motionless areas stand out less.
- Use subpixeling on small canvases (32x32 px or less) where believable motion is otherwise hard to achieve.
- Use subpixeling for barely-moving effects: wind, laughter, shaking, shivering, staggering, flinching, being stunned, sleeping, flickering lights, wobbling/jiggling.
- Use subpixeling for idle animations to add detail that free drawing or moving parts cannot provide.
- For still images, subpixeling is equivalent to anti-aliasing and line weight control.
- Not every body part needs subpixeling. Subpixelate only the parts that benefit; other parts can be duplicated and slid normally.
- Some body parts can stay frozen or delayed while others shift. Motion readability matters more than uniform subpixeling.
- For the most subtle idle motion, keep the silhouette completely still and swim pixels inside the contours.
- When working with very few colours, swim full pixels inside the sprite instead of AA subpixels; the principle is identical.
- Large-scale sprites (e.g. Capcom golden-age fighters) often need no subpixeling at all — plain in-betweens and full 1 px motion suffice. Reserve subpixels for small, carefully placed details.
## Checklist
- [ ] Identified whether the motion is large (full-pixel in-betweens may suffice) or subtle (subpixel needed)
- [ ] Chosen which body parts get subpixels and which stay frozen
- [ ] Confirmed the sprite's silhouette can stay still if the effect is meant to be internal
- [ ] Checked palette size — few colours → swim full pixels instead of AA
## Anti-patterns
- Subpixeling an entire large-scale sprite when full-pixel motion would read fine.
- Adding subpixels to every body part "just in case".
- Assuming all smooth animations require subpixels.

---
name: subpixeling-line-weight-and-split-pixels
topic: Line weight, split pixels, and shape tricks
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- In still images, subpixeling = anti-aliasing = line weight control. Thinner lines read lighter; shrinking a line brightens its shape and edges.
- Brightening works only when shading inside a dark zone. Inside dark shapes the opposite applies: thinner lines read darker.
- Split pixels are one pixel's value divided across two adjacent blocks at ~50% brightness each. They approximate a pixel that cannot exist.
- You may add slightly more weight (brightness) to one side of a split pixel — this is AA combined with split pixels.
- Split pixels can reuse an existing palette colour (e.g. grey) rather than introducing a new one.
- AA placement can bend, skew, or thin a shape while the outline stays identical. Direction and placement of AA push the perceived shape.
- Horizontal lines can appear thinner than vertical lines and vice versa; this effect is subtle and easily ignored.
- Line weight and shading are easy to confuse — the same AA can serve both purposes.
- Adding or removing pixels on round corners can add extra movement to animations. Use with moderation.
## Checklist
- [ ] Line weight changes match the background value (lighter on dark, darker on light)
- [ ] Split pixels use ~50/50 value division, optionally weighted to one side
- [ ] Split pixel colours reused from the existing palette where possible
- [ ] Corner pixel additions/removals kept minimal
## Anti-patterns
- Brightening thin lines inside a dark shape (inverts the intended read).
- Introducing new colours for split pixels when an existing palette colour works.
- Overusing corner pixel additions until the silhouette breaks.

---
name: selective-outline
topic: Selective outlines (sel-out)
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- A selective outline is a broken/segmented outline with AA gaps that lets a foreground object blend with its background.
- Use selective outlines only on layers with a transparent background, and only when the object will appear on dark backgrounds. On light backgrounds they look jagged.
- Darker sel-out lines suit sprites that will mostly appear in dark environments; lighter sel-out lines suit light environments.
- Selective outlines make transitions smoother when one layer slides over another.
- If backgrounds vary between dark and light areas, either make sel-out fuller and less segmented, drop sel-out entirely, or apply hints of AA to other outline types.
- Selective outlines can be animated with subpixeling, similar to line weight.
## Checklist
- [ ] Object's typical background is known (dark vs light)
- [ ] Sel-out line value chosen to match that background
- [ ] Outline is fuller/less segmented if backgrounds vary
- [ ] Sel-out only applied on transparent-background layers
## Anti-patterns
- Using a selective outline on a light background → jagged edges.
- Using a heavily segmented sel-out over mixed dark/light backgrounds.
- Applying sel-out to layers that are not transparent.

---
name: subpixeling-animation-and-readability
topic: Animating subpixels, arcs, and readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- When a curve crosses into a new pixel row, new pixels pop in. Aim for at least 2–3 pixels when popping shapes and lines; avoid transitions to single pixels.
- Subpixeling animation = duplicating a frame and editing it slightly. Flip between frames to check the shift.
- Subpixel direction follows the angle of the shape, not the general animation direction. A cape moving up/down but curved horizontally subpixels horizontally.
- Subpixel motion is partly optical illusion: a shape can appear to move up/down while its internal lines shift left/right (waving/rippling).
- Do not subpixel facial features. If the eye shape morphs too much it sticks out. If you must, keep it extremely subtle.
- To keep faces consistent: hold the face across multiple frames while the head/body pixel-shifts, or have in-betweens favour the keyframes (closer and more similar to the keys).
- Subpixeling a face that moves only 1 px produces very blurry in-betweens even at high frame rates.
- Pose-to-pose subpixeling is not guaranteed to work; straight-ahead animation is often easier for subpixels.
- Keep a general sense of direction and arcs — "general" is the keyword. Delayed motions and changed arcs are allowed.
- Set up extremes (keyframes where motion starts/stops) first, then work on the in-betweens where subpixeling happens.
- For intense/complex idle animations, study 3D-rendered sprites (e.g. Donkey Kong Country) to untangle pixel placement.
- When the silhouette hardly moves, onionskin tools are useless — the effect is purely pixel/colour shifting inside the sprite.
## Checklist
- [ ] Extremes defined before in-betweens
- [ ] Popped rows/lines are at least 2–3 px wide
- [ ] Face held consistent across frames
- [ ] Subpixel direction matches shape angle, not overall motion
- [ ] In-betweens favour keyframes when easing
## Anti-patterns
- Subpixeling facial features until the eye shape morphs visibly.
- Popping a curve down to a single pixel.
- Relying on pose-to-pose subpixeling without testing whether straight-ahead reads better.
- Expecting onionskin to help when the silhouette does not move.

---
name: subpixeling-pitfalls-and-shortcuts
topic: Pitfalls, cheap shortcuts, and study habits
confidence: opinion
sources: ["Pixel Logic, Michael Azzi, ch. 8 (pp. 187-212)"]
---
## Rules
- Do not overdo subpixeling. Excessive subpixels make sprites look like they are melting or made of jelly, and the technique is time-consuming.
- Subpixeling is not animated shading. Treating it as moving light/shadow will confuse the process.
- Cheap auto-subpixel shortcut (unreliable, requires manual cleanup): lock/reduce sprite colours → resize 200% nearest-neighbour → move sprite 1 px horizontally or vertically → resize 50% with blur enabled.
- The shortcut produces a blurry result and does not guarantee a usable in-between; it is only a reference for beginners learning pixel shifting.
- Subpixeling is the least-documented pixel-art technique. Study downloaded sprites closely — that is the best way to learn it.
- If you are only an illustrator, the line-weight section is the most relevant part; if you are an animator, revisit the chapter after learning animation basics.
## Checklist
- [ ] Confirmed subpixeling is actually needed before spending time on it
- [ ] Any auto-generated subpixels manually cleaned up
- [ ] Reference sprites collected for close study
## Anti-patterns
- Shipping the auto-blur shortcut output without manual cleanup.
- Overdoing subpixels until the sprite looks like jelly.
- Confusing subpixeling with animated shading.

> CHECK: OCR is mostly clean, but the "Quick but cheap subpixels" steps and the "split pixels" 50% claim are paraphrased from image captions; verify exact wording against pp. 195 and 211 if precision matters.

<!-- 9 Animation (pp. 213-237) -->
---
name: pixel-animation-timing-framerates
topic: Animation timing, framerates and frame-length math
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Define timing as "how many drawings/frames show an action", not wall-clock duration. WHY: lets you reason about motion independent of the target framerate.
- Use the standard vocabulary: on ones = 1 unique drawing per frame; on twos = each drawing held 2 frames; on threes = held 3 frames. WHY: shared language with animators and sprite sheets.
- Convert drawings-per-second to frame length with these reference values (rounded, use for quick math):
  - 24 drawings/s ≈ 0.04 s/frame (42 ms); 12 ≈ 0.08 s (83 ms); 8 ≈ 0.12 s (125 ms); 6 ≈ 0.17 s (167 ms).
  - At 60 FPS: 60 drawings/s ≈ 0.02 s (16 ms); 30 ≈ 0.03 s (33 ms); 20 ≈ 0.05 s (50 ms); 15 ≈ 0.06 s (50-60 ms); 10 ≈ 0.1 s (100 ms).
- Remember 1 centisecond = 0.01 s = 1/100 s; 1 millisecond = 0.001 s. WHY: some editors ask for ms/cs instead of frame counts.
- Mix ones, twos and longer holds inside one animation; never keep a constant cadence for the whole clip. WHY: constant cadence reads as mechanical.
- For snappy game actions (attacks, hits, jumps) prefer ones or twos; reserve threes/fours for slow, heavy or ambient motion. WHY: gameplay needs immediate visual feedback.
- When your tool's timeline stores single frames only (Photoshop, GraphicsGale style), set each frame's duration individually instead of grouping. WHY: those tools have no "extended frame" concept.
## Checklist
- [ ] Decide target framerate (24 for cinematic feel, 60 for gameplay) before choosing ones/twos.
- [ ] Write the intended drawings-per-second next to each action in your notes.
- [ ] Verify the exported clip plays at the intended speed in-engine, not just in the editor.
- [ ] Check whether your editor uses grouped frames or per-frame durations, and adapt your workflow.
## Anti-patterns
- Assuming "on twos" means the same wall-clock speed at 24 FPS and 60 FPS. It does not.
- Animating everything on ones at 60 FPS for a retro-styled game; it looks sterile and costs memory.
- Copying frame-length numbers between a 24 FPS and a 60 FPS project without converting.

---
name: pixel-animation-keyframes-readability
topic: Key frames, extremes, breakdowns and readability
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Treat animation as the study of motion: study real creatures, objects and forces, plus exaggerated motion from existing animation. WHY: reference analysis is the fastest way to improve.
- Make key frames clearly distinct from each other. If two keys look too similar, the audience cannot read the action. WHY: more in-betweens never fix weak keys.
- Prioritize strong silhouettes; readability matters more in animation than in a still sprite. WHY: the pose must be legible in a single frame at gameplay speed.
- Aim for the animation to *feel* good before it looks good. WHY: players read motion, not individual frames.
- Use breakdowns (passing positions / mid-keys) to route A → X → B instead of a straight A → B. WHY: breakdowns add character, arcs and variety.
- When studying a reference (film, game, real life): (1) step frame by frame, (2) find the extremes just before a direction change, (3) draw your own in-betweens from those extremes instead of rotoscoping, (4) stylize unless the poses are already overemphasized. WHY: copying footage frame-by-frame produces lifeless, off-model results.
- Keep anticipation short or absent for gameplay-critical actions; use it freely for cosmetic or wind-up animations. WHY: input must feel instant.
- Direct anticipation opposite to the main action's direction. WHY: it reads as energy building up before the move.
- One frame of anticipation can be enough. WHY: "you don't see it, but you feel it".
## Checklist
- [ ] Can each key pose be identified from its silhouette alone?
- [ ] Does every direction change have an extreme pose?
- [ ] Is there at least one breakdown between the two most distant keys?
- [ ] Does the anticipation frame read as opposite to the action?
- [ ] Does the action start within one or two frames of the input?
## Anti-patterns
- Adding in-betweens to fix an animation whose keys are too similar.
- Rotoscoping reference footage frame by frame without stylizing.
- Long wind-up anticipation on a player attack in an action game.
- Skipping breakdowns and going straight from A to B on expressive motions.

---
name: pixel-animation-easing-subpixel
topic: Ease in/out, subpixeling and moving holds
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Ease in/out = acceleration and deceleration: place in-betweens closer to the key they favour. WHY: natural motion never starts or stops at constant speed.
- Use a timing chart to plan spacing; if frame 2 favours frame 1 and frame 4 favours frame 5, they sit closer to those keys than to frame 3.
- Use subpixeling only when two drawings must be closer than 1 pixel apart. WHY: 1 pixel is the minimum distance for a normal transform or drag.
- Produce subpixel frames by duplicating the nearest key and shifting/editing it by sub-pixel amounts. WHY: it is faster and stays on-model.
- Reserve subpixeling for slow-ins/slow-outs and the most subtle movements. WHY: it multiplies frame count and memory cost.
- Work on strong key frames first, then add subpixels. WHY: subpixeling cannot rescue bad posing.
- For a moving hold (action stops but the character keeps drifting), duplicate the key and edit it with subpixeling. WHY: it eases into the maximum pose without a hard freeze.
- For a regular hold, keep the body still but animate small secondary parts. WHY: a fully frozen pose looks dead.
- Expect moving holds to be rare in pixel art. WHY: each unique frame costs storage, which is why old games avoided them.
## Checklist
- [ ] Are in-betweens spaced closer to the key they favour?
- [ ] Is every subpixel frame derived from a duplicated key rather than drawn from scratch?
- [ ] Does the slow-in/slow-out actually need subpixels, or would a normal 1-pixel step read fine?
- [ ] Do holds keep at least one small part alive?
## Anti-patterns
- Sprinkling subpixels everywhere instead of fixing key poses.
- Using subpixeling for fast actions where the eye cannot resolve it.
- Freezing the entire character on a hold with zero secondary motion.

---
name: pixel-animation-smears-overshoots
topic: Smears, multiples and overshoots
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Use elongated smears as a single stretched in-between that connects two keys and mimics motion blur. WHY: it sells fast motion in one frame.
- Keep smear frames on screen very briefly — animate them on ones at 24 FPS (about 0.05 s). WHY: smears should be felt, not seen.
- Use multiples (after-image smears) as an alternative to stretched smears; they multiply the object instead of stretching it. WHY: multiples loop better in cycles.
- Prefer multiples for looping cycles, elongated smears for one-shot actions.
- Add an overshoot frame that passes the destination and snaps back to the key. WHY: it gives motion a snap/pop.
- Vary overshoot strength: a 1-pixel overshoot is valid and still readable. WHY: subtle recoil is felt even when not consciously seen.
- Combine overshoots with squash & stretch for exaggerated impacts, and with smears when the smear must reach past the key.
- Apply overshoot in 2D perspective too, not only along the screen axes. WHY: perspective still applies to 2D objects.
- Avoid dithered blur frames. WHY: they only worked on CRT displays and are inefficient today.
## Checklist
- [ ] Is every smear frame held for roughly one frame at 24 FPS or less?
- [ ] Does the smear connect two readable keys rather than replace one?
- [ ] Does the overshoot return to the key, with or without settling in-betweens?
- [ ] Is the overshoot direction consistent with the motion arc and perspective?
## Anti-patterns
- Holding a smear for several frames so the audience sees the trick.
- Using stretched smears in a looping walk/run cycle instead of multiples.
- Overshooting so far that the pose reads as a different action.
- Using dithered blur to fake motion blur in a modern game.

---
name: pixel-animation-overlap-followthrough
topic: Overlap, delayed pixels and follow-through
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Split a character into leading parts and trailing parts; the leader moves first, the rest follow with a delay. WHY: this is what makes motion feel physical.
- Treat overlap as dragging and follow-through as settling. WHY: two distinct phases with different timing needs.
- Animate the leading action first, then draw the following actions. WHY: planning order prevents tangled timing.
- Apply overlap at the pixel level: when one pixel moves, neighbouring pixels catch up one or two frames later ("delayed pixels"). WHY: it reads as subpixel motion using whole pixels.
- Use delayed pixels instead of anti-aliasing when animating 45° shapes. WHY: AA at 45° gets messy; delayed pixels stay clean and the transition reads smoother.
- Alternatively use "stretchy pixels" that extend to bridge two positions, but check playback. WHY: stretchy pixels can stand out badly.
- Add follow-through to capes, hair, cloth and anything pulled by an outside force; it continues after the main action ends. WHY: it adds realism and fakes extra motion under frame limits.
- Use subpixeling on the settle phase of a follow-through. WHY: it makes the ending convincing.
## Checklist
- [ ] Is there a clear leading part and at least one trailing part?
- [ ] Are trailing parts delayed by 1-2 frames relative to the leader?
- [ ] For 45° transitions, did you use delayed pixels rather than AA?
- [ ] Did you play the animation back to judge delayed vs stretchy pixels?
- [ ] Does every cloth/hair element settle after the main action?
## Anti-patterns
- Moving all body parts simultaneously with no delay.
- Using anti-aliasing on 45° pixel transitions.
- Leaving stretchy pixels in without checking playback.
- Ending a follow-through abruptly with no settle frames.

---
name: pixel-animation-production-methods
topic: Four production methods for pixel animation
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Choose one of four build methods per project: silhouette animation, recycling frames, start from traditional art, or simple lineart. WHY: each has different cost/quality tradeoffs.
- Silhouette method: block out poses as flat shapes or blobs of colour first. WHY: it locks readability and colour layout early, and shapes can be reused or touched up.
- Recycling method: duplicate an existing frame and modify it with copy, resize, slide, rotate, cut and skew. WHY: a solid base sprite is your main resource; redrawing everything wastes time.
- Always edit recycled frames enough that they look distinct. WHY: unedited sliding produces robotic, "tweened" results.
- Use place-and-trace (shift-and-trace) — a previous frame as a guide under a blank frame — to keep features uniform. WHY: it is the traditional equivalent of recycling.
- Combine silhouette and recycling to build rough in-betweens fast, then clean up. WHY: you see the final motion sooner at the cost of more cleanup.
- Traditional-art method: draw at high resolution, shrink to a pixel-friendly size, then trace/edit. Optimize with: shrink without blur, reduce colours, raise contrast, apply a sharpen filter. WHY: this pipeline keeps control while digitizing.
- Simple lineart method: line art → colours → shading → clean-up, shading every frame individually. WHY: it is pixel art from start to finish, unlike the traditional pipeline.
- 3D-model-to-sprite is a valid route for very large animation counts; the cleanup still requires pixel-art skill.
## Checklist
- [ ] Pick the method before starting the first frame.
- [ ] If recycling: list which parts are reused per frame.
- [ ] If traditional: verify the shrink step introduces no blur before tracing.
- [ ] If silhouette: confirm each blob pose reads as a distinct silhouette.
- [ ] Confirm recycled frames differ enough to avoid a tweened look.
## Anti-patterns
- Sliding body parts around and calling it a new frame.
- Redrawing every frame from scratch in a project that could recycle.
- Shrinking high-res art with a blurring resample and tracing the mush.
- Mixing production methods mid-animation without a style pass.

---
name: pixel-animation-limited-frames
topic: Limited-frame animation and minimum frame counts
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Treat 3 frames as the minimum for a convincing loop; 2 frames only flickers and cannot show arcs. WHY: two drawings give no path from A to B.
- Build limited animations from: a strong anticipation key, a breakdown/mid-point if possible, an overshoot for snappy motion, and accurate silhouettes.
- For a 3-frame run loop, make the legs interchangeable so the cycle reads correctly. WHY: it doubles the apparent motion for free.
- For 4-frame loops, reuse one frame (usually a breakdown) so the cycle closes. WHY: it keeps the loop seamless without new art.
- For walk cycles, animate the character travelling across the screen instead of in place, tracking foot contact, then reposition frames to the centre. WHY: it exposes sliding and contact errors immediately.
- For circular motion, place objects around a circle rather than going back and forth. WHY: it produces a correct arc with few frames.
- Narrow overlapping actions down to 3 frames where possible.
## Checklist
- [ ] Does the loop have at least 3 unique frames?
- [ ] Is there an anticipation key and an overshoot frame where the action needs snap?
- [ ] For runs: are the leg poses interchangeable?
- [ ] For walks: did you test by moving the character across the screen?
- [ ] Does the loop close without a visible pop?
## Anti-patterns
- Shipping a 2-frame loop for a run or walk.
- Animating a walk in place without ever checking foot contact against the ground.
- Using back-and-forth motion where a circular placement would give a proper arc.

---
name: pixel-animation-onion-skin
topic: Onion skin usage in pixel art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Use onion skin only for line-art-style pixel animation and for predicting in-betweens. WHY: with many colours the overlay becomes an unreadable mess.
- When keys are far apart, onion skin gives enough info to draw an in-between; when they are close, it misleads you. WHY: you cannot literally draw "between the lines" at pixel resolution.
- Favour the key frame when placing tight in-betweens so the shape stays intact. WHY: preserving the silhouette matters more than exact midpoint spacing.
- If your pixel art has no line art, do not rely on onion skin. WHY: there are no outlines to interpolate against.
- Note that some tools call the feature "light table".
## Checklist
- [ ] Is the animation line-art based? If not, limit onion skin use.
- [ ] Are the two reference frames far enough apart for the overlay to be readable?
- [ ] Did you favour the key rather than splitting the difference exactly?
## Anti-patterns
- Using onion skin on a heavily coloured, anti-aliased sprite and trying to read the overlay.
- Blindly placing in-betweens at the visual midpoint of the onion skin.

---
name: pixel-animation-line-boiling
topic: Line boiling — causes and fixes
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Define boiling as the wobble/jitter of hand-drawn lines across frames; it is inevitable in traditional art but avoidable digitally.
- Fix boiling by: using the selection tool to slide parts instead of redrawing, subpixeling tight in-betweens, and using economical limited animation.
- Accept that limited animation trades boiling for choppiness; pick a balance between retro limitation and modern smoothness.
- Avoid redrawing a standing character every frame. WHY: boiling is most visible when nothing should be moving.
- Do not use boiling as a stylistic effect in pixel art. WHY: at low resolution there is no room for it, and one odd frame breaks the animation.
- Note that games like Yoshi's Island use intentional boil only on backgrounds and objects, not on characters or enemies.
## Checklist
- [ ] Are static poses held rather than redrawn?
- [ ] Are tight in-betweens subpixeled and aligned?
- [ ] Did you slide parts with the selection tool instead of redrawing them?
- [ ] Did you play the loop and look for single-frame jitter?
## Anti-patterns
- Redrawing an idle character frame by frame.
- Copying the hand-drawn "boil" look into a low-resolution sprite.
- Fixing boiling by adding frames everywhere, producing a sterile high-framerate look.

---
name: parallax-scrolling-and-background-motion
topic: Parallax scrolling, top-down depth and background distortion
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 9 (pp. 213-237)"]
---
## Rules
- Apply the core rule: closer layers move faster, farther layers move slower; skies and distant objects (sun, moon, stars, mountains) barely move.
- Split the background into layers and move them at different speeds to add depth.
- Use the three parallax types deliberately:
  1. All layers move in the same direction at different speeds (standard depth).
  2. Layers move in opposite directions (camera-turn illusion).
  3. Background loops while the front is frame-by-frame, giving a revolving camera.
- Use parallax in top-down views too, not only side-scrollers; let foreground elements (e.g. grass) travel over background elements (e.g. leaves).
- Create stretch/skew perspective by moving each pixel scanline at a different speed in code. WHY: it fakes depth without new art.
- For vertical stretch effects, author floor and ceiling of a structure as a single asset and stretch it as the character moves, revealing either side.
## Checklist
- [ ] Are background layers ordered by distance and given matching speeds?
- [ ] Do distant elements stay nearly static?
- [ ] Does the chosen parallax type match the intended camera behaviour?
- [ ] For top-down scenes, is there at least one foreground element overlapping the background?
- [ ] For scanline stretch, is the source asset built to reveal both sides?
## Anti-patterns
- Moving all background layers at the same speed (no depth).
- Scrolling the sky or distant mountains at the same rate as the ground.
- Restricting parallax to side-scrollers only.
- Building separate floor and ceiling assets when a single stretchable asset would work.
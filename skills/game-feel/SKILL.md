---
name: game-feel
description: Juice and game feel basics — camera look-ahead/shake, easing, and impact feedback — before tuning how an action feels. Search knowledge for "game feel" for the fuller reference.
---

# Game feel

Short version. For the fuller reference (hit-stop timing, squash-and-stretch math, layered feedback theory), call `knowledge_search("game feel")`.

## The core idea

A mechanically correct action can still feel bad. Feel comes from feedback layered on top of the mechanic — visual, audio, and camera responses that confirm an action landed, not from the mechanic itself.

## Cheap, high-value techniques

- **Screen shake on impact**: drive it from a decaying "trauma" value rather than a fixed offset, so repeated hits don't stack into something nauseating. Always make the amount tunable — too much shake is the most common overcorrection.
- **Camera look-ahead**: bias the camera slightly in the direction of movement/aim so the player sees more of what's ahead than what's behind. Smooth the camera's position rather than snapping it.
- **Easing, not linear motion**: UI transitions, camera zoom changes, and any tweened value should use an easing curve (ease-out for something arriving, ease-in-out for a back-and-forth), not a linear interpolation, which reads as robotic.
- **Impact feedback stacking**: a meaningful hit or pickup should hit at least two of: a flash/color change, a small scale pulse, a particle burst, and a sound — one alone tends to feel flat.
- **Hit-stop / freeze frames**: a brief (a few frames) pause on a strong impact makes it read as more powerful, if the game's genre suits it (avoid it in anything that demands tight, uninterrupted control).

## How to apply it in this kit

- Expose every feel parameter (shake amount/decay, look-ahead distance, ease type) on a Resource or exported variable — never hardcode a magic tuning number, the same rule as any other balance value.
- Feel work belongs to `technical-artist` for camera/visual feedback and to `audio-designer` for the audio layer; `gameplay-programmer` exposes the signals/state (impact happened, speed, etc.) they react to.
- Tune one parameter at a time and get a read from the human before stacking more — feel is subjective and easy to overshoot.

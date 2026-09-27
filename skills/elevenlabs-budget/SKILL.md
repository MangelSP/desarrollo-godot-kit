---
name: elevenlabs-budget
description: Generating audio with ElevenLabs under a hard credit reserve — check balance first, never overspend, log every generation to the ledger. Load before calling elevenlabs_sfx or elevenlabs_music.
---

# ElevenLabs budget discipline

ElevenLabs is optional, paid, and shared across the whole project's credit pool. Synthetic placeholder audio (see the audio-designer agent) covers the MVP by default; ElevenLabs is only for when the project has explicitly budgeted for real audio.

## Before generating anything

1. Call `elevenlabs_balance` to get the real, current balance — never assume it from a previous call in this conversation.
2. Compute the estimated cost of the generation you're about to request.
3. Only proceed if `balance - estimate >= reserve_credits` (the reserve is set per project in `.godot-kit.toml`). If it isn't, stop — don't generate partial or cheaper-than-asked-for audio as a workaround without checking with the human first.

## Never generate audio that isn't already planned

Every sound or music generation must already be listed in `docs/audio.md` with its estimated duration and cost before you call `elevenlabs_sfx` or `elevenlabs_music`. If a task calls for a sound that isn't in that doc yet, add it there first — with the estimate — rather than generating on the fly.

## Always log

After a successful generation, record it in the project's audio ledger (cost, prompt, duration, date) so the running balance stays auditable without another API call. This is what lets `producer`/`orchestrator` reason about remaining budget without hitting the API.

## Defaults to prefer

- SFX generation is priced per second of fixed-duration output (commonly ~40 credits/second, capped around 30 seconds) — keep requested durations as short as the sound actually needs.
- Prefer the synthetic placeholder path for anything iterative (you'll want to re-tune it) and reserve ElevenLabs for sounds/music that are close to final.
- Never call ElevenLabs from an automated loop turn (`kit-loop`) without the budget line already present in the plan — a paid call the human didn't expect is a stop condition, not something to push through.

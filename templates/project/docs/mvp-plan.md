# MVP plan

**Question the MVP answers:** TBD — `producer` fills this in with the user once the core loop is validated.
**Exit criteria:** TBD.

States: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked. Whoever finishes a task leaves a line below it with what was done.

---

## Milestone 0: Project base

- [x] **T0.1 · game-architect**: scaffold the project (this template), install GUT, confirm a clean import.
  *Accept:* `godot --headless --editor --quit` runs with no errors.
  Done: project scaffolded from the Godot Kit template; GUT installed; import clean.
- [ ] **T0.2 · game-architect**: write `docs/architecture.md` (scene tree, autoloads, `Events` signals and Resource classes) and an initial ADR for the tech baseline.
  *Accept:* every system named in the GDD has an owner (scene or autoload) and every signal it needs is listed with types.
- [ ] **T0.3 · game-designer**: fill in `docs/gdd.md` with the real rules, numbers and curve for this game, and create the first `data/*.tres` Resources they depend on.
  *Depends on:* T0.2.

Everything past this point is up to `producer` to plan with the user, milestone by milestone.

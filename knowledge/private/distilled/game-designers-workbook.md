<!-- How to Use This Book (pp. -2--1) -->
---
name: workbook-as-practice-tool
topic: game design practice methodology
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. How to Use This Book (pp. -2--1)"]
---
## Rules
- Treat design skill as trainable through volume: the primary learning loop is "make lots of games", not reading theory. WHY: repetition builds intuition that no amount of analysis substitutes for.
- Use isolated exercises to drill individual sub-skills (e.g. one mechanic, one system) separately from full projects. WHY: a full game hides which specific skill failed; isolation makes the feedback signal clean.
- Do exercises in any order — thematic chapter grouping is a suggestion, not a sequence. WHY: motivation and relevance drive completion more than curriculum order.
- Skip exercise types you dislike; do all of a type you like. WHY: sustained practice beats forced coverage for skill acquisition.
- Treat the workbook itself as a game (playful, self-directed). WHY: the same engagement mechanics that make games fun sustain long practice.
- Assume transfer across interactive media: skills from digital, tabletop, LARP, escape rooms, sports, improv, ARG, interactive theater, toys, pinball, arcade, CYOA, playground games all feed each other. WHY: design intuition is about player experience, not platform.
## Checklist
- [ ] Pick a session goal: one sub-skill to drill, not "get better at design".
- [ ] Choose exercise type by interest or by instructor syllabus, not by page order.
- [ ] Track which exercise categories you have and have not touched.
- [ ] After each exercise, name the one skill it trained.
## Anti-patterns
- Reading the book front-to-back without doing the exercises.
- Forcing yourself through disliked exercise types "for completeness".
- Assuming lessons only apply to your target platform (e.g. only console games).
- Treating the workbook as a reference text rather than a practice regimen.
> CHECK: Page numbers are given as pp. -2--1 (negative), which is likely an OCR/front-matter artifact. Verify actual page range before citing.

<!-- Types of Exercises (pp. 0-0) -->
---
name: exercise-type-taxonomy
topic: game-design-practice
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. Types of Exercises (pp. 0-0)"]
---
## Rules
- Classify every design exercise you run into one of eight types, because each type trains a different muscle and mixing them up wastes time:
  1. **What Is...** — introduces one fundamental practice; goal is first-hand experience, not a polished result.
  2. **Breaking It Down** — isolate one component of an existing game and manipulate it in isolation.
  3. **What a Concept** — take a cross-game concept (e.g. resource conversion, hidden information) and experiment with variations.
  4. **Level Design** — arrange elements inside the game world's space (layout, pacing of space, sightlines).
  5. **Remix** — start from an existing game and modify/improve it.
  6. **Narrative Design** — build story elements as one part of the design, not the whole.
  7. **Cross-Training** — borrow a skill from another discipline (writing, music, architecture, improv) to widen your design range.
  8. **Reflection** — process lessons from other exercises and plan your future practice.
- Pick the type by the *output you want*, not by the topic: want a new mechanic → Breaking It Down; want a better map → Level Design; want a new take on a known game → Remix.
- Run exercises in a rough progression: What Is... → Breaking It Down / What a Concept → Level Design / Remix → Reflection. WHY: fundamentals must exist before you can isolate or recombine them.
- Treat Reflection as a scheduled step, not an optional one. WHY: unprocessed exercises produce activity without skill gain.
- When stuck on an original design, switch to Remix or Cross-Training. WHY: constraints from an existing game or foreign discipline break blank-page paralysis faster than free brainstorming.
- Keep Narrative Design exercises scoped to story as a *component*; do not let them absorb the whole design session. WHY: game design is systems-first; story is one subsystem among many.
## Checklist
- [ ] Named the exercise type before starting.
- [ ] Stated the single skill or component the exercise targets.
- [ ] Chose a time box appropriate to the type (fundamentals short, Remix/Level Design longer).
- [ ] Scheduled a Reflection pass after the exercise.
- [ ] Recorded what changed in your design practice, not just what you made.
## Anti-patterns
- Treating every exercise as "make a full game" — most types target one component or skill.
- Skipping Reflection because the exercise "went fine."
- Assuming game design equals narrative design; story is a part, not the whole.
- Jumping to Remix before you can isolate components (Breaking It Down), which produces shallow copies.
- Doing Cross-Training without connecting the borrowed skill back to a game design decision.

> CHECK: The chapter lists exercise categories but the source text gives no page numbers (pp. 0-0) and no ordering or time-box guidance; the progression and time-box rules above are inferred, not stated.

<!-- 1 Setting the Stage (pp. 2-35) -->
---
name: gdd-purpose-and-structure
topic: Game Design Documents
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Treat the GDD as a living document, not a frozen spec: revise it continuously through production. WHY: the design changes as you learn from playtests.
- Split one monolithic GDD into many small GDDs, each scoped to a single mechanic, level, or NPC behavior. WHY: small docs stay readable and are easier to update without breaking unrelated sections.
- Change the GDD's purpose by project stage: before production it is a pitch (sells the idea to stakeholders, team, and yourself); during production it is the blueprint. WHY: the same artifact serves persuasion early and reference later.
- Include pictures. Concept drawings, storyboards, wireframes, and schematics communicate faster than prose. WHY: visuals remove ambiguity about what the player sees.
- Keep the top-level GDD at low detail; push specifics into future, narrower GDDs. WHY: premature detail locks in decisions you have not tested.
- No single GDD template fits all games — drop sections that do not apply and add sections your game needs. WHY: games are too diverse for one-size-fits-all structure.

## Checklist
Recommended top-level GDD sections:
- Game title
- Executive summary (1–2 sentences on the core idea)
- Audience (demographics, personality, or named personas with reasons they would enjoy it)
- Experience pillars (what the player must do/see/feel even if everything else changes)
- Platform(s) (pieces or hardware)
- Goals of the player (how they win; can they win at all; same goal for all players?)
- Obstacles blocking those goals (other players, NPCs, the world)
- Interface (what the player physically does: place a card, press a button, swipe)
- Elements (2–3 example objects/units and how they help or hinder)
- Story: setting and genre; main characters (name, playable or NPC, description, want, obstacle)
- Concept drawings

## Anti-patterns
- Writing one giant document that nobody updates.
- Writing prose where a diagram would do.
- Filling every template section even when it does not apply to the game.

---
name: rulespace-remix-method
topic: Design Exploration
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Explore "rulespace" (the universe of possible rules) by starting from a known game as base camp, then changing one rule at a time. WHY: a familiar base isolates the effect of your change.
- Change exactly one rule per iteration, and write the new rule precisely enough that a reader without you present can apply it. WHY: untestable ambiguity hides whether the change worked.
- Test the change by playing against yourself before judging it. WHY: solo play is the cheapest first filter.
- After testing, write a re-revised version of the rule. WHY: first drafts of rules almost always need a second pass.
- Then add further rules that support the first change — e.g. to fix first-player advantage or kill a dominant strategy. WHY: single-rule changes often expose new imbalances that need follow-up.

## Checklist
- Pick a well-known base game.
- Identify a rule to change (not the board/playfield rule if the exercise forbids it).
- Write the replacement rule with a rule number.
- Playtest solo.
- Revise the rule; playtest again.
- Add supporting rules for balance.
- Re-test.

## Anti-patterns
- Changing several rules at once so you cannot attribute the outcome.
- Judging a rule change without playing it.
- Leaving a known dominant strategy or first-player advantage unaddressed after the change.

---
name: maze-design-progression
topic: Level Design
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Know the wall-following rule: keeping one hand on the wall always solves a maze with fully connected walls and exits on the outer edge; it fails on mazes with floating "islands". WHY: this tells you which mazes are trivially solvable.
- Choose the difficulty axis deliberately: a top-down view makes a maze with islands harder to read; an inside-the-maze view makes a simple connected maze harder to navigate. WHY: the same layout plays differently depending on player perspective.
- Add islands (floating wall sections) to break wall-following and raise difficulty. WHY: it removes the guaranteed solution.
- Use non-planar geometry (e.g. a cube) to add difficulty. WHY: paths that cross folds cannot be seen in a flat view.
- Use toroidal wrapping (left exits right, bottom exits top) as another difficulty lever. WHY: it breaks the player's mental model of edges as boundaries.
- Escalate collectible mazes in this order: three-key/one-door, then three-key/three-door. WHY: keys turn dead ends into rewards; matching doors turn exploration order into a puzzle.
- Place the exit first, then let the player choose a start. WHY: it guarantees the goal is reachable before you build the route.

## Checklist
- Decide planar vs non-planar vs toroidal.
- Decide islands or no islands.
- Place the ending.
- Choose a starting point.
- For key mazes: place keys so dead ends are rewarding.
- For multi-door mazes: verify each key/door pairing creates a solvable order.

## Anti-patterns
- Building a maze where wall-following trivially wins when you wanted a challenge.
- Dead ends that give nothing — they read as punishment instead of reward.
- Assuming a layout that is hard top-down is also hard from inside.

---
name: accessibility-considerations
topic: Accessibility
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Frame accessibility as designing for difference, not only disability. WHY: accommodations (like a ramp) usually improve the experience for everyone.
- Contrast: meet a minimum of 3:1, and preferably 4.5:1, for elements that must stand out. WHY: below that, text and UI become unreadable for many players.
- Never rely on color alone: use brightness, shape, and/or motion as redundant channels. WHY: color vision deficiency is common.
- When color must carry a message, pick pairs that contrast even for color-blind players (e.g. orange against blue). WHY: red/green pairs fail for the most common deficiency.
- Support screen readers, and consider voice-over in addition to or instead of text. WHY: text-only UI excludes blind players.
- Make type as large as possible, and let players switch fonts. WHY: different people find different fonts readable (relevant to dyslexia).
- Reduce motor demands where possible: avoid requiring fast reflexes or smooth continuous motions like drag-and-drop. WHY: these exclude players with motor impairments.
- Avoid forcing memorization: any information the player must retain should be findable, referenceable, or discoverable through consequence-free experimentation. WHY: memory limits vary.
- Eliminate flashing patterns that can trigger seizures. WHY: photosensitive epilepsy is a hard safety constraint.
- For VR, keep framerates high and eliminate player accelerations. WHY: low framerate and forced acceleration cause motion sickness.
- Represent instructions and story in non-audio form; provide captions. WHY: deaf players miss audio-only content.
- Check physical space: can players reach the game, use the interface comfortably, and see the display?
- If an accommodation is infeasible or would dilute the design too far, state clearly up front (before purchase or time investment) who is excluded and why. WHY: audiences accept stated limits; they do not accept surprises.

## Checklist
- Run the game through a color-blindness simulator (e.g. Sim Daltonism on Mac, Color Oracle on PC).
- Play with keyboard only.
- Play with sound off.
- Play one-handed.
- Then watch a real person play.

## Anti-patterns
- Treating accessibility as a post-launch patch.
- Using color as the only signal for state or messaging.
- Hiding known exclusions until after the player has paid or invested time.

---
name: schematic-drawing-technique
topic: Design Communication
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Arrange multiple views of an object as if drawn on the faces of a flattened box (left, front, right, back). WHY: it shows all sides in a predictable, readable layout.
- Omit box faces that are redundant or trivially predictable. WHY: fewer views means less clutter.
- Tuck extra angles (e.g. 3/4 view) into the corners of the layout. WHY: it adds information without breaking the grid.
- Use magnified detail views to highlight small areas. WHY: small features vanish at full-object scale.
- Use cuts to remove redundant material and save space. WHY: it keeps the drawing compact.
- Use section views (crosshatch the cut planes) to show inner workings. WHY: a dollhouse is essentially a section view — internals matter.
- Indicate dimensions with extending lines and extent lines; mark imprecise values with a tilde (~) meaning "approximately". WHY: false precision misleads the reader.
- Label everything. WHY: there is effectively no upper limit on useful labels.

## Checklist
- Pick the minimum set of views that shows every distinct side.
- Add detail views for small features.
- Add a section view if internals matter.
- Dimension all critical measurements; mark approximations with ~.
- Label every part.

## Anti-patterns
- Drawing a single view and assuming the reader infers the rest.
- Stating precise numbers you have not measured.
- Leaving parts unlabeled.

---
name: capturing-feeling-in-mechanics
topic: Design Method
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Start from a feeling, not a theme: pick a solitary activity you know well and design a game that evokes the same feeling. WHY: it trains translating experience goals into mechanics.
- Do not copy the activity's surface look; only the feeling must match. WHY: superficial resemblance is not the design target.
- Constrain the exercise: turn-based, single-player. WHY: constraints force creative problem-solving and make the design testable.
- Choose a game type deliberately (card, pen-and-paper, dexterity, dice, board, digital, other) based on which best carries the feeling. WHY: the medium shapes which sensations are available.
- Ask whether an existing mechanic already evokes a similar feeling, and borrow from it. WHY: reusing proven mechanics shortens the path to the target experience.

## Checklist
- Name the activity.
- Describe how doing it feels.
- Name existing mechanics with a similar feel.
- Pick the game type.
- Outline the solitaire game.
- Playtest and check the feeling actually lands.

## Anti-patterns
- Designing the activity's literal simulation instead of its feeling.
- Choosing a medium before deciding what feeling you are targeting.

---
name: randomized-idea-generation
topic: Ideation
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 1 (pp. 2-35)"]
---
## Rules
- Generate game ideas by randomly combining one entry from each of four columns: Field, Goal, Players, Turns. WHY: random constraints produce combinations you would not reach by free brainstorming.
- Use the dice-column procedure to pick entries: think of a number 1–10, cross off that many dice from the top of the list, then take dice sequentially from there. WHY: it removes your own selection bias.
- Specify the resulting game in as much detail as you can before judging it. WHY: thin ideas are easy to dismiss; fleshed-out ones reveal their merit.
- Treat constraints as a creative unlock rather than a limitation. WHY: constrained brainstorming often feels easier, not harder.

## Checklist
- Randomly select Field, Goal, Players, Turns.
- Write the combined game's rules.
- Sketch the play area (square grid, hex grid, or line/squiggle based).
- Add any extra rules.
- Test it.

## Anti-patterns
- Re-rolling until you get a combination you already like.
- Stopping at the one-line concept without specifying rules.

> CHECK: The chapter's reflection prompts ("who is the game designer you?", "define what better means to you") are personal exercises, not design rules; they were intentionally omitted. Verify whether the book intends them as required process steps.

<!-- 2 Abstract Strategy (pp. 36-62) -->
---
name: abstract-strategy-core-rules
topic: Abstract strategy game design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Define an abstract strategy game by five rule slots: board geometry, turn order, legal move, win condition, draw condition. Change one slot at a time to learn what each contributes.
- Keep the first prototype on a small grid (6x6 to 8x8) with 4-16 pieces per player. WHY: small state space lets you finish test games in minutes and see whether the core loop is interesting before adding content.
- Make every move add, move, or remove exactly one piece. WHY: a single atomic action per turn keeps the game readable and makes forks (see fork card) possible to reason about.
- State the draw condition explicitly (board full, no legal moves, repetition). WHY: without it, playtests stall and you cannot tell whether the design is broken or just unfinished.
- When remixing an existing game, change exactly one rule, playtest, then amend that rule before changing anything else. WHY: isolating one variable is the only way to attribute a playtest result to a cause.
- Preserve the "spirit" of the original only after you have tested single-rule changes; then allow unlimited changes. WHY: free remixing before you understand the base rules produces noise, not insight.

## Checklist
- [ ] Board shape and size written down (rectilinear, hex, triangle, or graph).
- [ ] Turn structure written down (alternating, extra turn on trigger, simultaneous).
- [ ] Legal move written down in one sentence.
- [ ] Win condition written down in one sentence.
- [ ] Draw condition written down in one sentence.
- [ ] One-rule variant tested and amended at least once.
- [ ] Full remix tested against a second player, not only solo.

## Anti-patterns
- Changing several rules at once and then judging the result. You cannot tell which change caused the outcome.
- Adding pieces, board size, and special abilities before the base move/win loop is fun. Complexity hides a boring core.
- Leaving the draw condition implicit. Playtests then end in confusion rather than data.
- Copying a known game's rules verbatim and calling it a remix. No design learning occurs.
> CHECK: OCR shows a 7x7 grid in the Connect Four remix, but standard Connect Four is 7 wide x 6 tall. Verify the intended dimensions before using this as a design constraint.

---
name: forks-as-design-goal
topic: Forks and tactical tension
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Define a fork as a move that creates two winning (or materially good) threats, of which the opponent can answer only one. WHY: this is the minimal unit of tactical tension in a turn-based game.
- Design the board so a single move can plausibly threaten two separate lines or two separate pieces. WHY: forks are impossible if every move has only one axis of consequence.
- Aim for a game where a new player can create a fork unaided within their first few games. WHY: if forks only appear at expert level, the tactical layer is too deep for the target audience.
- Keep the piece count and move set small ("think checkers, not chess") when the goal is teaching forks. WHY: fewer piece types means the player can hold all threat relationships in working memory.
- Test forks by playing against a friend and observing whether they find a fork without prompting. WHY: designer knowledge of the game is not evidence that the tactic is discoverable.

## Checklist
- [ ] At least one move type can threaten two targets at once.
- [ ] Board geometry allows lines in more than one direction (row, column, diagonal).
- [ ] A novice playtester created a fork unprompted.
- [ ] The opponent always has exactly one legal answer to a fork, not zero and not two.

## Anti-patterns
- Making every piece identical and every move symmetric, so no move can create asymmetric threat. Forks require asymmetry.
- Adding so many piece types that the player cannot track which pairs of threats are live.
- Treating forks as an emergent accident rather than a design target. If you never test for it, it may not exist.

---
name: mda-framework
topic: MDA framework (mechanics, dynamics, aesthetics)
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Work in the order mechanics -> dynamics -> aesthetics. WHY: play is what makes a game a game; the play parts must be settled before presentation choices can be evaluated.
- Define mechanics as what the player can do and how the world responds. Write these first, concretely.
- Define dynamics as how mechanics interrelate to create systems the player cannot fully predict. Ask "what makes the consequences of an action hard to foresee?"
- Define aesthetics broadly: look, sound, story, setting, theme, plus the intended emotional effect and type of play.
- Tie aesthetics back to mechanics so the game is easier to learn and intuit. WHY: a theme that matches the actions gives players a mental model for the rules.
- Treat each step as iterative and as a trigger to re-evaluate earlier steps. A dynamic may suggest a new mechanic; an aesthetic choice may force new constraints on mechanics.
- Remember the player experiences the layers in reverse: aesthetics first, then dynamics, then mechanics. WHY: first impressions are aesthetic, so onboarding must work at that layer.

## Checklist
- [ ] Mechanics listed as concrete player actions and world responses.
- [ ] Dynamics listed as interactions that create unpredictability.
- [ ] Aesthetics listed as setting, mood, and intended emotional effect.
- [ ] Each aesthetic choice justified by a mechanic or dynamic it supports.
- [ ] At least one re-evaluation pass where a later layer changed an earlier one.

## Anti-patterns
- Starting from story and never specifying mechanics. The result is a setting, not a game.
- Choosing a theme that contradicts the mechanics (e.g., a relaxing theme over a high-pressure timer).
- Treating MDA as a one-way pipeline instead of a loop. You lose the feedback that makes the layers cohere.

---
name: theming-manifestation-and-dramatic
topic: Theming an abstract game
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Split theme into two parts: manifestation theme (what the player sees immediately: place, time, genre) and dramatic theme (the underlying statement of belief about how the world works or ought to).
- Write the dramatic theme as a short declarative sentence ("love conquers all", "you can't cheat an honest man"). WHY: a one-line thesis is testable against every mechanic and piece name.
- Treat the truth of the dramatic theme as irrelevant; only the point of view matters.
- Choose a theme weight on a spectrum from heavy (all mechanics, text, and images support the theme, e.g., Monopoly) to light (only names and shapes support it, e.g., chess) to none (Tetris).
- When pitching, produce two versions of the same game: one lightly themed and one heavily themed. WHY: this forces you to decide what each theme element actually buys you.
- Use manifestation theme expectations to teach rules, or deliberately subvert them for surprise. Pick one intent per element.

## Checklist
- [ ] Manifestation theme written: where and when.
- [ ] Dramatic theme written as one sentence.
- [ ] Theme weight chosen (heavy / light / none) and stated.
- [ ] Every piece name and board element checked against the dramatic theme.
- [ ] A light and a heavy version both sketched.

## Anti-patterns
- Heavy manifestation theme with no dramatic theme. The game looks like something but says nothing.
- Theme elements that contradict the mechanics, forcing players to unlearn their intuition.
- Assuming a theme must be added at all. Unthemed abstract games are a valid choice.

---
name: narrative-retrofit-of-abstract-games
topic: Retrofitting narrative onto an abstract game
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Build the retrofit in three layers: setting, cast, moveset.
- Setting: pick a place and time that fits the board geometry and the possible piece placements. Decide whether the space is continuous (a pool) or discrete (lockers in a hallway).
- Cast: give every piece a name, a defining characteristic, and a desire. For non-human pieces, also state what kind of being it is.
- Moveset: map each mechanical action to a narrative meaning. For chess that means move, capture, check, checkmate; for checkers in an office setting, capture could mean forcing a rival out of the company.
- Validate the framework by playing a game, logging the moves, and writing the story those moves produce. If the story is unsatisfying, the framework is missing a character trait or a move meaning, not the story itself.

## Checklist
- [ ] Setting chosen and justified by board geometry.
- [ ] Every piece has name, characteristic, desire (and species if non-human).
- [ ] Every mechanical action has a narrative meaning.
- [ ] A full game logged and converted into a story.
- [ ] Framework revised where the story felt forced.

## Anti-patterns
- Naming pieces without giving them desires. Names alone generate no story.
- Mapping only capture and victory, ignoring movement and threat. Most of the story lives in the quiet moves.
- Writing the story first and bending the moves to fit it. The moves are the source material.

---
name: discretizing-continuous-actions
topic: Converting continuous activities into turn-based space
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Pick a continuous activity with little decision-making (knitting, splitting firewood, a dance). WHY: low decision content makes the discretization step visible.
- Break the activity into discrete steps and assign each step to a turn. This converts continuous time into turn-based time.
- Choose a space representation: square grid, hex grid, triangle grid, graph, or directed graph. Match the representation to the movement the activity actually has.
- Decide what each cell or node represents (a location, a state, a stage of the task).
- Define the transition condition that moves an element from one cell or node to another.
- Represent unpredictable parts of the activity with a randomizer (dice column). WHY: real activities have variance; without a randomizer the conversion feels deterministic and flat.
- Note that some grids and graphs can emulate one another (embedding). Pick the one that makes the transitions easiest to read.

## Checklist
- [ ] Activity broken into named steps.
- [ ] Each step mapped to a turn.
- [ ] Space type chosen (square / hex / triangle / graph / directed graph).
- [ ] Cell or node meaning written down.
- [ ] Transition conditions written down.
- [ ] Randomizer assigned to the genuinely unpredictable parts.

## Anti-patterns
- Using a square grid for an activity whose natural adjacency is hexagonal or graph-like. The mismatch shows up as awkward rules.
- Discretizing an activity that is mostly decision-making. You end up rebuilding an existing strategy game instead of learning the technique.
- Omitting randomness entirely, producing a puzzle rather than a game.

---
name: randomized-design-constraints
topic: Random constraint generation for abstract game ideas
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 2 (pp. 36-62)"]
---
## Rules
- Generate a design brief by randomly selecting one option from each of four columns: piece movement, piece abilities, number of pieces, grid size.
- Use the following option sets as the pool:
  - Piece movement: all pieces move the same way / pieces do not move but change state / two piece types with different movement / one piece more powerful than the rest / most pieces simple with a few special abilities / every piece moves differently.
  - Piece abilities: capture by jumping over / capture by moving into the space / capture by trapping between two of your pieces / add a piece every turn / add a piece on a certain arrangement / pieces never enter or leave the board.
  - Number of pieces: 16 / 14 / 12 / 8 / 6 / 4 per player.
  - Grid size: 6x6 / 6x7 / 7x7 / 7x8 / 6x8 / 8x8.
- Write the resulting game in full detail, including additional rules, before evaluating it. WHY: the constraint combination is the point; judging it before it exists defeats the exercise.
- Lay out the game on paper and play it. WHY: a constraint brief that is never played produces no design knowledge.

## Checklist
- [ ] One option rolled per column.
- [ ] Full rules written, including any rules the brief does not cover.
- [ ] Board laid out and played at least once.
- [ ] Notes recorded on which constraint caused the most interesting tension.

## Anti-patterns
- Re-rolling until you get a combination you already like. You lose the value of working outside your habits.
- Leaving gaps in the rules because the brief did not specify them. The gaps are where your design work happens.
- Treating the generated game as a finished product rather than a study.

<!-- 3 Story (pp. 63-84) -->
---
name: storyboard-communication
topic: storyboarding
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- Use storyboards to communicate a sequence of key moments to the team before production; they sit between script and final asset.
- Keep panels low-detail: draw only what the audience will see or hear. WHY: over-detailed boards constrain artists, costume, and production designers.
- Never write a character's mental state in a panel description. WHY: it limits the actor's or animator's interpretation.
- Label each panel with a slug line (INT./EXT., location, time of day) plus action and dialogue, comic-book style.
- Connect panels with lines joining frame corners and arrowheads showing travel direction.
- Vary panel duration freely: one panel can be a multi-minute shot or a fraction of a second; context and description carry the timing.
- Use standard camera-move vocabulary so the team can visualize your intent (see camera-move card).
- For nonlinear games, storyboard a single user story (one player's path) rather than the whole system.

## Checklist
- [ ] Slug line present on every panel
- [ ] Only visible/audible content described
- [ ] Camera move noted where it matters
- [ ] Panel-to-panel arrows drawn
- [ ] Detail level low enough that downstream artists stay free

## Anti-patterns
- Writing internal thoughts or emotions in panel text
- Rendering finished-quality art in a storyboard
- Omitting camera moves, forcing the team to guess framing
- Storyboarding every branch of a nonlinear system instead of one representative path

---
name: camera-move-vocabulary
topic: storyboarding
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- Default to static shots; they are the most common and prioritize clarity of emotion and action.
- Use pans and tilts for point of view.
- Use tracking and trucking to follow linear action such as walking.
- Use arc shots to convey awe.
- Use a pedestal to reveal a subject head to toe (establishing something new).
- Use a boom to signal a hierarchy change: subject appears to grow or shrink.
- Use rack focus for a literal and metaphorical shift of focus.
- Use dolly in/out for context and exposition (part-to-whole or whole-to-part).
- Use zoom like a dolly but note it flattens or deepens the background around the subject.
- Use push/pull to signal something just changed between character and environment.
- Named combinations: boom up/down = pedestal + tilt; arc = truck + pan rotating around subject; push/pull = dolly + zoom (Jaws, Vertigo, Goodfellas).

## Checklist
- [ ] Shot choice matches the intended emotional beat
- [ ] Combination moves named consistently across the team
- [ ] Framing term (ECU, CU, MS, WS, EWS, TS, OTS) specified per panel

## Anti-patterns
- Using a zoom when you want a dolly's spatial feel (background distortion is a side effect, not neutral)
- Picking flashy moves for every panel, destroying clarity
- Inventing non-standard move names the team cannot parse

> CHECK: OCR lists framing terms (ECU, CU, MS, WS, EWS, TS, OTS) without definitions; verify exact framing definitions from another source before teaching them.

---
name: interactive-story-flow
topic: narrative design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- Model interactive story structure as a flow diagram: a start point, optional endpoint, and steps with branching choices.
- Allow branches to merge back into shared nodes. WHY: merging keeps consequence scope manageable and avoids writing whole parallel storylines.
- Use false choices (branches that reconverge) deliberately to control narrative outcome while limiting writing cost.
- Prototype narrative flow with a diagram before writing full dialogue.
- Start with a very small scope, e.g. a brief elevator conversation, to validate the structure.

## Checklist
- [ ] Start node defined
- [ ] End node(s) defined or explicitly open-ended
- [ ] Merge points marked on the diagram
- [ ] False choices identified and intentional
- [ ] Diagram small enough to redraw in one sitting

## Anti-patterns
- Fully branching trees with no merges (writing cost explodes)
- Adding false choices without tracking that the player can notice the lack of consequence
- Skipping the flow diagram and writing dialogue first

---
name: roll-and-move-narrative
topic: narrative design
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- In a roll-and-move narrative game, write one card per board space; each card advances the journey's story.
- Make the story amusing enough that a single-player run is satisfying on its own.
- Cards may carry gameplay consequences (redirect to another space, grant a choice) in addition to story text.
- Playtest early and often, watching specifically for continuity errors.
- Avoid callbacks to cards the player may not have landed on. WHY: unreferenced callbacks confuse players who skipped those spaces.
- Decide your branching-dialogue policy before writing cards.
- Playtest method: instead of a token, write a unique symbol per playthrough plus the turn number in each visited space.

## Checklist
- [ ] Every space has a card
- [ ] Each card advances the journey narrative
- [ ] Gameplay effects on cards are unambiguous
- [ ] No callback depends on an unvisited card
- [ ] Single-player run tested for satisfaction
- [ ] Continuity pass done after playtest

## Anti-patterns
- Cards that are pure mechanics with no story beat
- Cross-references to spaces the player might never reach
- Writing all cards before any playtest

---
name: hidden-role-game-parameters
topic: hidden role games
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- Treat hidden-role games as a procedural narrative about keeping and discovering secrets.
- Define four parameters explicitly before designing: role set, traitors' goal, loyals' goal, elimination method.
- Role-set options scale from one hidden role (Traitor) up to four (Traitor, Accomplice, Anti-Traitor, Anti-Traitor's Assistant).
- Traitor win conditions commonly fall into: sabotage the loyals' goal, eliminate all loyals, or eliminate all loyals then complete their own goal.
- Loyal win conditions commonly fall into: gather all items, answer N trivia questions, complete a memory match, solve a stepwise puzzle, move an object to a goal zone, or eliminate all traitors.
- Elimination methods include: public vote between rounds, blind vote, token cost (e.g. 3 tokens to eliminate, each player starts with 1), elimination on a player's turn, or decree by an elected President.
- Not every player needs a unique role; "everyone gets a different role" is one option among several.
- Sanity-check the design by seating 8 players in a circle, labeling each with a name, personality trait, and role, then simulating the playthrough.

## Checklist
- [ ] Role set chosen and counted
- [ ] Traitor goal stated
- [ ] Loyal goal stated
- [ ] Elimination method stated with exact costs/votes
- [ ] 8-player simulation run and design adjusted

## Anti-patterns
- Leaving the elimination method vague (it drives pacing and table talk)
- Assuming unique roles are required
- Skipping the simulated playthrough before committing to the design

---
name: three-act-story-anatomy
topic: story structure
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 3 (pp. 63-84)"]
---
## Rules
- Structure stories with three acts: beginning, middle, end; this is the default even when told out of order.
- Beginning contains exposition (characters, setting, central conflict) and introduction of the conflict.
- Middle contains an attempt to face the conflict, at least one setback, and a recovery.
- End contains the outcome (win, lose, or draw) and the denouement: practical and emotional consequences.
- Use the beat list as a reverse-engineering tool: dissect a known story into the bullets to learn the pattern.
- Use the beat list as a generative tool: write an original story from the bullets, using yourself or an acquaintance as protagonist and a simple desire as the conflict.

## Checklist
- [ ] Exposition establishes characters, setting, conflict
- [ ] Conflict introduced explicitly
- [ ] At least one setback in the middle
- [ ] Recovery beat present
- [ ] Outcome clear (win/lose/draw)
- [ ] Denouement covers practical and emotional fallout

## Anti-patterns
- Skipping the setback, producing a flat middle
- Ending at the outcome with no denouement
- Treating three-act structure as mandatory for every story (it is the default, not a law)

<!-- 4 Sport (pp. 85-100) -->
---
name: sport-rules-light-vs-heavy
topic: rules specification and player interpretation
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- Treat rules as living in the players' minds, not in the components: leave gaps only where players can fill them consistently. WHY: under-specified rules let groups self-balance and house-rule, which raises engagement.
- Match specification level to the game's scope: tabletop RPGs need a human judge (GM) because a full ruleset is impossible; digital games are conventionally fully specified because anything the engine allows is permitted. WHY: the medium sets player expectations about what is legal.
- Deliberately leave parameters open only when the community can arbitrate them (Monopoly-style house rules). WHY: open parameters without an arbiter become arguments, not play.
- When you leave a rule open, decide who judges: the group, a designated player, or the system. WHY: unassigned judgment is the main failure mode of rules-light design.
- For digital games, assume players will treat every reachable state as legal; if you don't want it, block it. WHY: convention, not text, defines the rulebook on a computer.

## Checklist
- For each rule, ask: is this specified, judged by a person, or left to the group?
- Does the medium (tabletop, digital, physical sport) match the specification level?
- Can a new player infer the open rules from context within one session?
- Does leaving this open create fun negotiation or unfun dispute?

## Anti-patterns
- Leaving a rule open with no arbiter and no social convention to resolve it.
- Fully specifying a game whose fun depends on player improvisation.
- Assuming digital players read the manual; they read the engine's affordances instead.

> CHECK: OCR shows the reflection prompt but no explicit design rule list; the rules above are inferred from the chapter's framing. Verify against pp. 86-87.

---
name: sport-field-redesign-constraints
topic: level/arena design for sports
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- When redesigning a playfield, keep the ruleset fixed and change only the geometry. WHY: isolates whether the field, not the rules, drives the fun.
- Preserve mandatory spatial features: a center circle for kickoff and an out-of-bounds area for restarts and corner kicks. WHY: removing them breaks the existing ruleset.
- Explore three dimensions, not just 2D outlines. WHY: elevation adds tactical options without new rules.
- Test fairness separately from symmetry: a field can be asymmetric and still fair. WHY: symmetry is one fairness strategy, not the only one.
- Vary goal count as a design lever (not always two). WHY: goal count changes scoring pace and defensive priorities.

## Checklist
- Does the new shape still contain every location the rules reference?
- Is there a defined out-of-bounds region?
- Is the field fair for both teams, even if not mirror-symmetric?
- Does the design work in 3D, not just as a top-down sketch?

## Anti-patterns
- Redesigning the field while also rewriting the rules; you lose the comparison.
- Assuming symmetry equals fairness.

---
name: sport-rule-remix-method
topic: iterating on an existing sport's rules
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- Start from a fully written ruleset (basketball's 10 abridged rules are the model) and change exactly one rule. WHY: single-variable changes let you attribute consequences.
- After changing a rule, predict two consequences: effect on play and effect on watchability. WHY: sports are spectator products, not just player activities.
- Use the abridged-rules format: teams, arena, scoring, ball/equipment, start condition, movement limits, contact rules, end condition, winner. WHY: a complete skeleton exposes which rule you are actually touching.
- Treat each rule as a lever with a known cost: e.g., removing the step limit speeds play but reduces individual skill expression. WHY: forces trade-off reasoning instead of wishful additions.

## Checklist
- Is the changed rule stated in one sentence?
- What breaks in the other nine rules as a result?
- Does the change help or hurt a spectator with no context?
- Can you state the intended consequence before playtesting?

## Anti-patterns
- Changing several rules at once and calling it one design.
- Ignoring the spectator dimension when modifying a sport.

---
name: sport-randomized-idea-grid
topic: combinatorial ideation for new sports
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- Generate sport concepts by rolling one entry from each of four columns: Teams, Arena, Score Points By, The Catch. WHY: forces combinations you would not choose deliberately.
- Use these column options as a starting palette:
  - Teams: one-on-one; two teams of two; two teams of 4-10; four individual competitors; two teams of four with animal companions; two teams of 11-25.
  - Arena: open field 100m x 75m; hard strip 1.5m wide; dirt circle 6m across; hard surface 23m x 8m bisected by a net; Olympic-sized pool; arena filled with obstacles.
  - Score by: moving a thing into a designated area; touching an opponent in a certain way; stealing something from the opponent; pushing an opponent out of bounds; hitting a target; rendering an opponent immobile.
  - The Catch: body-part restriction; tool-only restriction; no more than two steps without doing something; must ride an animal or machine; some players blindfolded; must stay within a specific zone.
- Fill the gaps left by vague prompts with your own concrete rules. WHY: the grid supplies constraints, not a finished design.
- Write the resulting ruleset down before evaluating it. WHY: vague ideas hide contradictions that only appear in text.

## Checklist
- Did you roll one entry per column?
- Did you resolve every vague term into a concrete rule?
- Does the combination produce a coherent win condition?

## Anti-patterns
- Treating the grid output as a finished design.
- Ignoring a roll because it seems silly; the odd combinations are the point.

---
name: sport-playground-game-decomposition
topic: designing equipment-free physical games
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- Decompose existing playground games into atomic elements (e.g., "touch another player against their will," "link arms to form a group") at a granularity of roughly 10-12 elements. WHY: recombination needs small, mixable parts.
- Recombine elements into a new game rather than inventing from scratch. WHY: proven elements carry proven fun.
- Target the audience explicitly: rules must be simple enough for five-year-olds. WHY: playground games are learned by demonstration, not reading.
- Design for a wide range of player counts. WHY: playground groups vary in size session to session.
- Reference games to mine: Tag, Freeze Tag, Red Rover, Blob, Hide and Seek, Sardines, Duck Duck Goose, Simon Says, Red Light Green Light, Mother May I, Murder Handshake, Thumbs Up, Thumb War, Ghost in the Graveyard.

## Checklist
- Are the rules explainable in under a minute to a child?
- Does it work with 3 players and with 15?
- Does it need zero equipment?
- Are the elements you combined still recognizable?

## Anti-patterns
- Rules that require reading or a referee.
- Designing for a fixed player count.

---
name: sport-toy-design-play-patterns
topic: toy and play-pattern design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 4 (pp. 85-100)"]
---
## Rules
- Identify the "toy" at the core of a game: ball for sports, virtual gun for FPS, car for racing. WHY: the toy is what players manipulate; the game is the structure around it.
- Design toys to serve specific play patterns. Reference list with examples:
  - Occupational role-play: pretend pizza parlor
  - Caretaking role-play: baby doll, hospital
  - Ritual play: hand-slapping patterns, cat's cradle
  - Kinetic cooperative play: double dutch, keepy-uppy, catch
  - Kinetic competitive play: jumping contest, bloody knuckles
  - Combat role-play: cops and robbers
  - Proxy role-play: dolls, action figures
  - Musical play: toy instruments
  - Art play: finger paints
  - Aesthetic play: styling hair, decorating notebooks
  - Construction play: Lego, Lincoln Logs
  - Collection play: sorting coins, collecting seashells
  - Performance play: karaoke, puppet theater
  - Dexterity play: block towers, marbles
- Score a toy design with Marvin Glass's 10 questions; count affirmative answers:
  - 5-6 affirmative: probably a good toy
  - 7-8: commendable
  - 9-10: excellent idea
- Glass's 10 questions: active role; inventive play; sturdy enough for rough play; easy to understand; easy to use; pleasant to touch; allows playing together; challenges mentally and/or physically; lets children explore adult work patterns realistically; gives a sense of discovery or self-expression.

## Checklist
- Which two play patterns does this toy target?
- Count affirmative answers to Glass's 10 questions.
- Is the toy sturdy enough for rough play?
- Does it support group play, not just solo?

## Anti-patterns
- Designing a toy that only supports one play pattern.
- Ignoring durability; toys are handled roughly.
- Optimizing for adult aesthetics over child play value.

<!-- 5 Word Games (pp. 101-120) -->
---
name: serious-games-taxonomy
topic: serious-games
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- Classify a serious game by its measurable goal before designing mechanics:
  - **Educational**: increase knowledge, skill, or interest in a topic.
  - **Persuasive**: argue a position on a real-world issue.
  - **Behavior change**: build/break habits or reframe player behavior.
  - **Wellness**: produce a direct physiological effect (some are FDA-approved for clinical use).
  - **Citizen science**: aggregate many players' puzzle-solving to produce publishable knowledge.
- Pick the category first, then choose mechanics that serve that category's success metric.
- WHY: each category implies a different definition of "winning" — a persuasive game is judged by attitude shift, not by fun alone.

## Checklist
- [ ] Goal category chosen and written down.
- [ ] Success metric defined in real-world terms (test score, attitude survey, habit log, physiological measure, data output).
- [ ] Mechanics traced back to that metric.

## Anti-patterns
- Treating "serious" as a genre of mechanics rather than a goal; the same mechanic can serve any category.
- Shipping a serious game with no measurement plan — you cannot claim impact without one.

> CHECK: chapter only lists the categories and poses the debate question; no design method for serious games is given. Verify against other sources before treating this as a full framework.

---
name: word-scramble-rule-anatomy
topic: word-games
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- A word-scramble (Scrabble-style) game is defined by 12 separable rules; treat each as a tuning knob:
  1. Player count: 2–4.
  2. Turn order: alternating.
  3. Tile acquisition: random draw from a bag.
  4. Hand size: 7 letters, refilled after each turn.
  5. Placement: play a word or extend existing word(s) using tiles from hand into empty board spaces.
  6. Adjacency: new tiles must be cardinally adjacent to at least one existing tile; the first word must cover the center star.
  7. Direction: words read left-to-right or top-to-bottom only — never both, never non-contiguous.
  8. Legality: any move producing a non-word sequence is illegal.
  9. Scoring: sum letter values of all tiles in the word(s) formed, including tiles not placed this turn.
  10. Multipliers: Wx3, Wx2, Lx3, Lx2 — applied only if a tile was placed on that space this turn.
  11. End condition: play ends when the bag can no longer refill a hand.
  12. Victory: highest total score.
- To remix: change exactly one rule, playtest, then either revise that rule or change a second rule to support it.
- WHY: changing one rule at a time isolates cause and effect; stacking changes makes it impossible to tell which one broke the game.

## Checklist
- [ ] Play a baseline game first (solitaire vs. yourself is acceptable) before changing anything.
- [ ] Change only one rule per iteration.
- [ ] After playtesting, record whether the change produced the intended effect.
- [ ] If not, revise the same rule or add a supporting change.

## Anti-patterns
- Changing several rules at once and attributing the result to one of them.
- Playing defensively in a solo baseline test — you know both hands, so optimize for best word instead.

---
name: crossword-construction
topic: puzzle-design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- Build the solution grid first, then black out unused squares; this is the hardest step — use pencil and expect false starts.
- Number squares sequentially in reading order (left-to-right, top-to-bottom) at the top-left corner of each word start; copy numbers and black squares to produce the puzzle grid.
- Clues are split into Across and Down sections.
- Clues need not be unambiguous alone: intersecting letters and the letter count of the space constrain the answer. Example: "one and ___" could be "the same", "done", or "only" — only one fits the space.
- Black squares give the constructor freedom to avoid awkward intersections.
- Mix clue obscurity levels; easier clues supply information that unlocks harder ones.
- Masterful puzzles link solutions thematically, which lets clues become even less specific.
- WHY: redundancy between clue, length, and crossings is what makes a crossword solvable without every clue being precise.

## Checklist
- [ ] Solution grid complete and black squares marked.
- [ ] Word starts numbered in reading order.
- [ ] Across and Down clue lists written.
- [ ] Clue difficulty spread across easy → hard.
- [ ] Puzzle tested on another person.

## Anti-patterns
- Assuming your clues are easy enough — the curse of knowledge means clues are harder than you think.
- Writing clues that are only solvable with the exact intended answer and no crossing support.

---
name: word-find-difficulty-tuning
topic: puzzle-design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- Word find is a valid microcosm of puzzle-level design: difficulty and fun vary enormously with the same word list.
- Start with a theme that yields many short words (≤5 letters).
- Prefer words sharing common letters so they can overlap on a small board.
- Difficulty knobs:
  - **Easier**: fill empty spaces with letters that do not appear in any target word.
  - **Harder**: fill with sequences that create red herrings (near-miss words).
- Grid topology changes the puzzle: a hex grid gives each cell 6 neighbors instead of 8; a triangular grid gives 3 neighbors but still 6 directions for words.
- WHY: neighbor count and direction count independently control how many false paths a solver must check.

## Checklist
- [ ] Theme chosen; word list built (≤5 letters, shared letters).
- [ ] Words placed on grid; remaining cells filled.
- [ ] Filler letters chosen deliberately (neutral vs. red herring).
- [ ] Grid proofread for unintended inappropriate words.

## Anti-patterns
- Random filler letters — you lose control of difficulty and risk accidental words.
- Skipping the final proofread pass.

---
name: hangman-underspecification
topic: word-games
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- Hangman's core rules: one game-master picks a word/phrase; guessers take turns naming letters; correct letters are written above every matching underline; wrong letters add a body part to the gallows and go in a wrong-letter area; guessers lose when the figure is complete, win when all letters are filled or the phrase is guessed early.
- The game is deliberately underspecified — the game-master decides:
  - When guessers may guess the whole phrase, and how often.
  - How many body parts make a complete hanged man.
- To remix: keep the locked structural rules (writing surface visible to all; gallows drawn) and alter one other rule, changing as many supporting rules as needed.
- WHY: the loose rules are the design space; tightening them is the actual design work.

## Checklist
- [ ] Phrase chosen before looking at any guess list.
- [ ] Wrong-letter tracking area drawn.
- [ ] Stop condition defined (reasonable-solver threshold or completed figure).
- [ ] Revised rule written down explicitly.

## Anti-patterns
- Leaving "when can you guess the phrase" undefined — it lets guessers brute-force early.
- Testing your own phrase while knowing it; use a fixed guess sequence instead.

---
name: chain-reactions
topic: game-systems
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- A chain reaction is when one action produces the effect of multiple actions, and those consequences produce further consequences (e.g. multi-capture in checkers, cascades in match-three games like Bejeweled).
- Chain reactions are desirable because they amplify and return the player's input, rewarding attention.
- They provide a comeback route without rubber-banding (catch-up mechanics that shrink the gap between leaders and trailers).
- Constraint: do not let chain reactions worsen first-mover advantage.
- WHY: a cascade that only the leader can trigger converts a reward mechanic into a runaway-leader mechanic.

## Checklist
- [ ] Identify what triggers the chain and what each link produces.
- [ ] Verify a trailing player can still initiate chains.
- [ ] Check whether the first player can chain more easily than later players.

## Anti-patterns
- Adding cascades without checking first-mover impact.
- Using rubber-banding as a substitute for chain-reaction comeback design.

---
name: randomized-word-game-idea-generator
topic: ideation
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 5 (pp. 101-120)"]
---
## Rules
- Generate a word-game concept by rolling one entry from each of four columns, then filling in the gaps yourself:
  - **Players**: solitaire; 2–4 free-for-all; 4 in teams of two; 2–4 cooperative; 2–4 vs. one mastermind; casual party game for 5+.
  - **Materials**: pencil and paper; letter dice; square letter tiles; letter card deck; giant floor mat of letters; alphabet refrigerator magnets.
  - **Object**: make the most words; make the longest words; make the highest-scoring words; be last with letters remaining; be first to use up your letters; fill a given space with valid words.
  - **Twist**: letters can be stolen; some letters locked until "freed"; words must fit a theme; some spaces accept only certain letters; a root word can be used only once; your letters can be rearranged into another word.
- The combinations are intentionally vague — the designer's job is to resolve the ambiguity into concrete rules.
- WHY: forcing an unfamiliar player-count/material pairing breaks default assumptions and produces concepts you would not reach by free brainstorming.

## Checklist
- [ ] One pick per column, recorded.
- [ ] Ambiguities listed and resolved into explicit rules.
- [ ] Prototype played before judging the concept.

## Anti-patterns
- Re-rolling until you get a "comfortable" combination — that defeats the exercise.
- Leaving the vague terms unresolved and calling the concept done.

<!-- 6 Quantitative (pp. 121-152) -->
---
name: player-feedback-methods
topic: playtesting
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Pick your feedback method by what you need: surveys = least info, most formal rigor; live playtesting = most informative but hardest to interpret; analytics = huge volume of *what* but zero *why*.
- Treat all feedback as problem identification only. If a tester (or your own head) proposes a solution, be suspicious of it — the designer owns the solution.
- When a player blames themselves ("I'm bad at strategy games"), treat it as a softener for criticism of your game and look for the design flaw.
- Fix flaws at playtest stage; cost and difficulty of fixing rise steeply later in production.
- Do not intervene during a live session — it invalidates the experiment.
- Analytics ambiguity: high retry counts can mean frustration *or* engaged experimentation. Never conclude from behavior data alone.
- Recruit both target-demographic testers and proxy testers.

## Checklist
- [ ] Decide which of the three methods answers your current question.
- [ ] Write down what you will NOT do during a session (intervene, defend).
- [ ] Log each reported problem separately from any proposed fix.
- [ ] For each analytics anomaly, form at least two competing hypotheses.
- [ ] Schedule fixes before the next production milestone.

## Anti-patterns
- Reacting defensively to negative feedback.
- Accepting a player's suggested solution as the design answer.
- Treating analytics as self-explanatory.
- Skipping playtests because watching new players struggle is uncomfortable.

---
name: probability-basics-for-designers
topic: probability
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Single event from N equally likely outcomes: p = 1/N (fair d6 → 1/6).
- OR of mutually exclusive events: add probabilities (roll 5 or 6 = 1/6 + 1/6 = 1/3).
- Compound events: enumerate all outcomes and count the ones you want (two d6 summing to 7 → 6/36 = 1/6).
- AND of independent events: multiply probabilities.
- Conditional probability: multiply along the branch (P(1st ace) × P(2nd ace | 1st ace) = 4/52 × 3/51).
- Expected value = Σ (outcome value × its probability). Two coin flips (values 0,1,2): 0×1/4 + 1×2/4 + 2×1/4 = 1.
- Before enumerating, look for a transformation that makes the problem trivial (P(2nd card is an ace) = P(1st card is an ace) = 4/52).
- Use expected value to check that two different random generators are equivalent in power (e.g. 4 coins vs. d4 − 0.5 both average 2).

## Checklist
- [ ] List the outcome space and confirm outcomes are equally likely before using 1/N.
- [ ] For compound events, enumerate or find a symmetry shortcut.
- [ ] Compute expected value for every random generator you give a player.
- [ ] Verify two asymmetric generators have equal expected value before calling the matchup fair.

## Anti-patterns
- Assuming outcomes are equally likely when they are conditional.
- Balancing by feel without computing expected value.
- Enumerating 36+ outcomes when a symmetry argument gives the answer instantly.

---
name: emergence-and-system-classes
topic: emergence
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Emergence = complex or surprising behavior from simple parts.
- Four behavior classes: 1 simple, 2 recursive/fractal, 3 chaotic, 4 complex. Ascending complexity is 1 → 2 → 4 → 3, not numeric order.
- Class 2 (recursive) is interesting but never surprising; class 3 (chaotic) is surprising but never interesting. Target class 4, which has both.
- Computers themselves are class-4 systems — that is the design target for game systems.
- One-dimensional cellular automata are the minimal testbed: a row of cells, each next state determined by the cell plus its two neighbors under a fixed rule.
- A hero/dungeon system (mood + direction + items, only hero and surroundings change per timestep) is Turing complete — capable of arbitrary information transformation.
- A rule whose start and end states are identical is a halting condition.

## Checklist
- [ ] Define the system's simple parts and the per-timestep update rule.
- [ ] Classify observed behavior: simple, recursive, chaotic, or complex.
- [ ] Push toward class 4 (both surprising and interesting).
- [ ] Include an explicit halting condition where the system must terminate.

## Anti-patterns
- Settling for class 2 (pretty but predictable) or class 3 (surprising but meaningless).
- Adding complexity to the parts instead of letting it emerge from the rules.

---
name: balance-strategies
topic: balance
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Balance means making the game *feel* fair — true fairness is one option, perceived fairness is the other.
- Strategy 1 — symmetry: identical resources and actions for all players (chess, football). Neutralize first-mover or side asymmetry by swapping sides (two games in chess, half-time switch in football).
- Strategy 2 — intransitivity: A beats B, B beats C, C beats A (rock-paper-scissors). Any odd number of elements supports first-order intransitivity.
- Intransitivity also comes from numeric attributes: give each archetype one high, one medium, and two low attributes, with no two archetypes sharing the same value set.
- Design for synergies — combinations of elements that are stronger together than alone (classic RPG party: fighter/tank/rogue/healer/ranger).
- In a balanced strategy game, all viable strategies (offensive, defensive, production, mixed) should be playable; none should dominate all others.
- Math relationships suggest fairness but only playtesting confirms it — play strategies against yourself to test.

## Checklist
- [ ] Choose symmetry or intransitivity as the primary balance lever.
- [ ] If symmetric, add a side-swap mechanism to cancel positional advantage.
- [ ] If asymmetric, give each archetype a distinct high/med/low attribute spread.
- [ ] Verify no single strategy dominates all others.
- [ ] Playtest each strategy against every other before shipping.

## Anti-patterns
- Assuming a mathematically tidy parameter set is balanced without testing.
- Giving two archetypes identical attribute spreads (kills intransitivity).
- Letting one dominant strategy exist.

---
name: input-vs-output-randomness
topic: randomness
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Input randomness: random information revealed *before* the player decides (poker hand, drawn cards). Keeps players alert and reactive.
- Output randomness: randomness applied *after* the decision (hit percentages, damage rolls). Gives a looser, comedic feel and encourages playful responses.
- Randomness is a double-edged sword: it improves approachability and keeps games close between unequal players, but it removes pride in accomplishment and makes random loss of progress feel punishing.
- Place randomness on a spectrum from none (Go, chess, billiards, mancala) to all (roulette, Candyland, War).
- To *add* randomness to a deterministic game: pick a game on the left of the spectrum and push it toward the middle.
- To *remove* randomness: pick a game on the right (gambling, pure-chance kids' games) and strip randomness while preserving what makes it unique. Removing is harder than adding.

## Checklist
- [ ] Decide whether the game needs input randomness, output randomness, or both.
- [ ] Check whether randomness is masking a skill gap or undermining earned progress.
- [ ] When adding randomness, test with actual dice rolls before committing.
- [ ] When removing randomness, confirm the game still has a reason to exist.

## Anti-patterns
- Using output randomness on high-stakes progress loss (feels severely discouraging).
- Adding randomness without checking whether it destroys the sense of earned accomplishment.

---
name: reducing-randomness-tools
topic: randomness
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Shuffle and deal: instead of dealing one card at a time in a circuit, deal 2–3 cards per player round-robin and force each player to discard all but one.
- Repeated dice rolls: give players a fixed pool of each possible result and let them choose when to spend each.
- Bid against the house and each other: when hidden information is not essential, give players a budget to spend on cards, dice, or other resources.
- Replace strict hierarchies with intransitivity: reframe challenges as decisions rather than luck (e.g. make a straight beat a full house in poker so players counter opponents instead of chasing the strongest hand).
- Pre-stack: let players prearrange their cards or dice, then reveal simultaneously and resolve.
- Intransitive dice exist — sets of dice that beat each other on average over repeated rolls.

## Checklist
- [ ] Identify the randomness source you want to reduce.
- [ ] Pick the matching tool: deal, dice pool, bidding, intransitivity, or pre-stacking.
- [ ] Verify the game still feels unique after the change.
- [ ] Test that the reduced-randomness version is still fun, not just fairer.

## Anti-patterns
- Removing randomness without preserving the game's identity.
- Using intransitivity where hidden information is the core of the game.

---
name: narrative-variables
topic: narrative-design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- A variable is a name associated with a remembered value (e.g. "Ben's Money").
- Extend the four story-flow shapes (oval = start/end, rectangle = step, diamond = decision, arrow = connection) with two more: check variable and modify variable.
- Track at least one variable per story; it can be anything (money, happiness 1–10, blood alcohol, sheep count).
- Avoid traditional game stats (health, ammo, charisma) when practicing — they hide the mechanic's generality.
- Variables drive branching: a diamond that checks a variable routes the story based on its value.

## Checklist
- [ ] Name the variable and its initial value.
- [ ] Add at least one modify-variable node.
- [ ] Add at least one check-variable diamond with distinct exits per range.
- [ ] Trace the story to confirm every branch is reachable.

## Anti-patterns
- Using only health/ammo/charisma variables in the exercise.
- Adding a variable that is never checked or modified.

---
name: race-track-level-design
topic: level-design
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Race track: players start on a line and take turns moving through a track without hitting walls; first to the finish wins.
- First move: choose one of the eight neighboring grid points around the start.
- Every later move: either the same speed and direction as last turn, or one of the eight neighboring points around that projected spot.
- Design tracks to be as fair as possible by counting the minimum distance each player must travel.
- Every track needs a reason to exist — ask "what is interesting about this track?"
- For advanced tracks, add new elements (obstacles, teleporters) to change the movement puzzle.

## Checklist
- [ ] Count minimum travel distance for each starting position.
- [ ] Confirm no starting position has a shorter optimal path.
- [ ] State the track's design intent in one sentence.
- [ ] Play a solo round and count moves per player.

## Anti-patterns
- Designing tracks without checking path-length fairness.
- Adding obstacles that only affect one lane.

---
name: battleship-remix
topic: game-remix
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Battling Ships: two 10×10 grids, one per player.
- Each player places five ships of lengths 1×2, 1×2, 1×3, 1×4, 1×5, each rotatable 90° (horizontal or vertical).
- Players alternate announcing one coordinate to fire at.
- The defender must truthfully report hit (occupied) or miss.
- A ship is sunk when every occupied space has been hit.
- First player to sink all enemy ships wins.
- After playing, revisit the rules: what would you change? Was it balanced? Well-paced? What mechanics would make it more interesting?

## Checklist
- [ ] Place all five ships within the grid, no overlaps.
- [ ] Confirm hit/miss reporting is truthful.
- [ ] Track sunk ships per player.
- [ ] After a round, list at least one rule change to test.

## Anti-patterns
- Allowing ships to overlap or extend off-grid.
- Skipping the post-game rule-revision pass.

---
name: adding-randomness-to-deterministic-games
topic: randomness
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Pick a deterministic game (chess, checkers, draughts, any sport, Go, Reversi, mancala, Battleship, tic-tac-toe, Stratego, Diplomacy, Connect Four).
- Introduce one or more six-sided dice as the random element.
- Test the idea with actual dice rolls before committing to the design.
- Use diagrams to make the modified rules clear.
- Adding randomness is simpler and more intuitive than removing it.

## Checklist
- [ ] Name the deterministic game and the exact rule the dice will affect.
- [ ] Roll real dice to test the new rule.
- [ ] Diagram the modified flow.
- [ ] Check the game still has a reason to be played.

## Anti-patterns
- Bolting randomness onto a rule where it destroys the core skill expression.
- Testing the idea only in your head.

---
name: feedback-and-analytics-interpretation
topic: analytics
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 6 (pp. 121-152)"]
---
## Rules
- Analytics = automated collection of player behavior data (level completion time, popular solutions, when players stop).
- Analytics tells you *what* players do, never *why*.
- Behavior data alone cannot distinguish frustration-driven retries from enjoyment-driven experimentation.
- Use analytics to inform iterations, not to conclude intent.
- Combine analytics with live playtesting to recover the *why*.

## Checklist
- [ ] Define the metrics you will collect before launch.
- [ ] For each metric anomaly, list at least two competing explanations.
- [ ] Pair analytics findings with a live playtest to test the explanation.
- [ ] Feed findings into the next iteration.

## Anti-patterns
- Treating a metric as self-explanatory.
- Using analytics as a substitute for watching players.

> CHECK: OCR of the class-numbering table on p. 128 is garbled — the text states ascending complexity is 1 → 2 → 4 → 3, but the table labels appear mismatched (Class 3 listed as "Chaotic" and Class 4 as "Complex" in one place, reversed elsewhere). Verify the canonical Wolfram class labels before relying on the numbering.

<!-- 7 Outside the Box (pp. 153-172) -->
---
name: player-creativity-outlets
topic: Player Creativity and Self-Expression
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- Treat avatar customization and virtual-space decoration as meaning-making features, not core mechanics: their gameplay effect is usually small to nonexistent, so budget them as retention/attachment features, not as balance-critical systems.
- Use open-ended puzzles when you want players to craft unique solutions: keep an automated victory check, but expect the solution space to be hard to test and debug — the freer the system, the higher the QA cost.
- For genuinely creative output (drawing, acting, composing), do not attempt automated scoring. Either make it consequence-free (self-assessed) or let other players judge it, as in party games.
- Expect an "empty canvas" problem: many players freeze or self-criticize when asked to be creative. Provide prompts, constraints, or starting templates to lower the barrier.
- If creativity can be shared in a multiplayer digital game, it becomes user-generated content (UGC). Weigh the studio incentive (player minutes replace studio-made content) against the range from empowering to exploitative design.

## Checklist
- Does the creative feature affect gameplay balance? If no, keep it out of the core loop and out of balance testing.
- Is the creative output machine-assessable? If not, decide: no consequence, or peer-judged.
- Have you given players a starting point (prompt, template, constraint) so the blank canvas is not intimidating?
- If UGC: is the sharing loop empowering for the creator, or does it extract labor without return?

## Anti-patterns
- Building a fully free creative system and assuming it can be tested like a deterministic mechanic.
- Attaching hard rewards or progression to unassessable creative output.
- Adding avatar customization and expecting it to carry the core gameplay experience.
- Shipping UGC features that only benefit the studio's content pipeline.

---
name: theme-park-design-cross-training
topic: Themed Experience Design (Head/Heart/Stomach, Weenies, Hub-and-Spoke)
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- Split any theme into two layers: the manifestation theme (the surface subject, e.g. "cool cars") and the dramatic theme (the message about life, e.g. "family and loyalty"). Keep the dramatic theme short, one sentence.
- Choose a manifestation theme that hits at least one of three audience draws: Head (intellectual interest), Heart (aspiration — something the guest wishes they could do), Stomach (pleasant visceral sensation).
- Lay out space using hub-and-spoke: a central landmark with branching paths. WHY: it spreads visitors evenly across attractions (raises capacity, cuts queues) and prevents guests getting lost.
- Place a "weenie" — a tall, far-visible attraction or sculpture — as a navigation anchor. Use it to pull guests toward the center, then let paths branch.
- Use berms (earthwork walls disguised as natural features) to block sightlines and control reveal/pacing.
- Support each main attraction with ancillary facilities: gift shops, restrooms, eateries, information booths, photo stations. A well-designed shop can itself function as an attraction.
- For variation, consider: attractions that pass through berms/weenies/shops, areas gated by visitor type or time of day, and seasonal changes (e.g. a coaster running backward at Halloween).

## Checklist
- Manifestation theme chosen and named?
- Dramatic theme written as one terse sentence?
- Park name chosen, with a fitting typeface for the entrance gate?
- Map drawn at roughly the scale of one "land" (about 2-3x the size of a single detailed area map)?
- At least one weenie visible from far away?
- Hub-and-spoke path structure with no dead ends that strand guests?
- Ancillary facilities placed around each attraction?
- Berms used to manage sightlines?

## Anti-patterns
- Using privately owned IP for the theme (use public-domain properties instead).
- A layout where guests must backtrack or can get lost because there is no central anchor.
- Treating the dramatic theme as a long explanation instead of a short message.

---
name: body-activity-discretization
topic: Decomposing Physical Activities into Turn-Based Rules
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- To adapt a physical activity into a game, discretize it along three axes: time (e.g. one fluid motion per turn), space (e.g. at most one step per turn), and body (e.g. four limbs as separate resources).
- Use "fluidity" as a constraint: a single continuous motion per turn naturally limits how far a player can move without needing a distance rule.
- Model damage/loss as disabling discrete body parts (struck arm goes behind the back; one disabled leg means standing on the other; both legs means playing on knees). Last player with any limb remaining wins.
- Allow the defender a single fluid motion to evade on each attack, then freeze both attacker and defender until the next turn.
- When designing any game involving physical touch or intrusion into personal space, explicitly design for safety and for how players signal and maintain consent.
- Adapt rules for players with nonstandard bodies; specify body zones on a diagram if the game targets specific areas.

## Checklist
- Time, space, and body all discretized?
- Turn order defined (e.g. clockwise from a starting player)?
- Win condition stated in terms of remaining resources?
- Consent/safety signaling built into the rules?
- Accessibility variant for nonstandard bodies considered?

## Anti-patterns
- Leaving movement continuous so turns have no natural endpoint.
- Adding physical contact rules without any consent mechanism.
- Assuming all players have the same body layout and range of motion.

---
name: micro-ttrpg-design
topic: Micro Tabletop RPG Design
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- Target a micro-RPG at a few pages, 1-6 players, all audiences, and roughly 15 minutes of playtime. Compensate for missing detail with short sessions and trust in the players/GM.
- State the goal explicitly: the point is to tell an entertaining story, not to solve problems or win.
- Include character creation with constraints: let players pick a name, an ability, and a flaw or degradation (e.g. a superpower weakened by old age). Prompting a character sketch helps.
- Use random event tables (d6, re-roll duplicates) to force events, but let players choose how they respond. WHY: randomness supplies structure; choice preserves agency.
- Use "pass the baton": no single player or GM monologues for long; players hand narration to each other.
- Reward players with moments of free-form storytelling as a treat, not as the default mode.
- End with a shared crisis scene where everyone narrates how they cooperate, then close.

## Checklist
- Player count, audience, and playtime stated up front?
- Intro text sets the scene in a few lines?
- Character creation prompts (name, attributes, sketch)?
- At least one d6 event table with 6 entries?
- A mechanism that rotates narration between players?
- Fits within the page budget?

## Anti-patterns
- Writing a multi-volume ruleset when the format is a few pages.
- Letting one player narrate the whole session.
- Making the game about winning rather than about the story.

---
name: roll-and-move-randomized-design
topic: Roll-and-Move Game Design (Randomized Constraint Exercise)
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- Build a roll-and-move game by randomly selecting one option from each of four categories: Dice, Pieces, Movement, Winning. Combine them, then write the extra rules needed to make the combination coherent.
- Dice options range from one d6, two d6 (choose one), two d6 (keep both if matching), two d6 split between two tokens, a dice "hand" of four d6 with one new die per turn, to six d6 under a cup with a pre-chosen number.
- Pieces options range from one token per player, two tokens, four numbered tokens that only move on their number, to zero starting tokens with a cost to add and a cost to move.
- Movement options include exact-landing shortcuts, moving opponents back 10 spaces on collision, sad-trombone spaces that send you back 5, jumping over tokens to push them back, and blocking rules where a token cannot pass the one ahead unless a specific number is rolled.
- Winning conditions can be inverted: first to reach all victory spaces wins, first to visit every space on a cyclical board wins, first to the exit wins, or first to the exit loses.
- After combining, sketch a rough board layout, then formalize it with interesting spaces connected in a logical order.

## Checklist
- One option picked from each of the four categories?
- Additional rules written to resolve interactions between the picks?
- Board sketched, then formalized?
- Dice rolls used sequentially and crossed out to track state?

## Anti-patterns
- Combining categories without writing the extra rules that make the combination playable.
- Assuming pure roll-and-move holds interest: modern entries like Monopoly and Trivial Pursuit add substantial player decision-making for a reason.

---
name: pub-trivia-question-design
topic: Pub Trivia Question Design
confidence: opinion
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 7 (pp. 153-172)"]
---
## Rules
- Distinguish standard trivia (tests a single fact) from pub trivia (requires synthesizing facts from multiple fields to reach one answer or a list).
- Write pub trivia by relating information across different domains of human endeavor so a team can attack the question from several angles (history, theater, beer, etc.).
- Build multi-clue questions: give several parallel facts that converge on one answer (e.g. several events that all occurred in the same year).
- Design for discussion and collaboration: the question should reward teammates combining partial knowledge, not just one expert recalling a fact.
- Convert a standard question into a pub question by adding cross-domain clues rather than by making the fact more obscure.

## Checklist
- Does the question require combining at least two fields of knowledge?
- Can it be approached from more than one angle by different teammates?
- Is the answer unambiguous once synthesized?
- Does it create discussion rather than a single recall test?

## Anti-patterns
- Writing pub trivia as standard trivia with harder facts.
- Questions solvable only by one narrow specialist with no route for the rest of the team.

<!-- 8 Bonus Round (pp. 173-184) -->
---
name: player-motivation-frameworks
topic: player motivation
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"]
---
## Rules
- Use Quantic Foundry's six-factor model to audit what your game offers: Action (visceral excitement), Social, Mastery (strategic thinking), Achievement (progression/completion), Immersion (incl. story), Creativity. WHY: gives a concrete checklist to spot missing or over-weighted appeal.
- Use the theme-park triad as a faster filter: Head (intellectual interest), Heart (aspirational attraction), Stomach (visceral/sensory anticipation). WHY: three buckets are enough to sanity-check a pitch in seconds.
- Pick 1-2 dominant factors per game and design around them; do not try to max all six. WHY: motivation factors pull design in conflicting directions (e.g. Immersion vs. fast Action).
- Treat player time, attention, and money as an investment the game must repay with value. WHY: frames design decisions as an exchange, not a favor.
## Checklist
- [ ] Named the 1-2 primary motivation factors for the game.
- [ ] Checked each of the six factors: present, absent, or deliberately excluded.
- [ ] Verified the core loop delivers the chosen factor within the first minutes.
## Anti-patterns
- Assuming "fun" is one thing; different players buy different factors.
- Adding story/immersion to a game whose audience came for Mastery or Action without checking it serves them.
> CHECK: OCR shows "Settings X" and a dog-breed dropdown near the motivation text — likely a UI mockup screenshot, not part of the framework. Verify page layout.

---
name: drawing-party-game-deconstruction
topic: party game design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"]
---
## Rules
- Deconstruct any party game into atomic elements before designing: number of artists at once, team structure, prompt source (random pool vs. player-written), drawing visibility (public process vs. private), who guesses, and scoring triggers.
- Use these known element sets as reference:
  - Pictionary: one artist at a time, two teams, random prompt from pool, category revealed to all, drawing public, teammates guess.
  - Picture Telephone: cooperative, everyone draws in turn, player-written prompts, private drawing, guess becomes next prompt, repeat N times.
  - Drawful: every player for themself, random prompt from game, private drawing, all players caption every drawing, all captions shown with the true prompt mixed in, points for correct guess and for fooling others.
  - A Fake Artist Goes to New York: hidden-role team split (fake artist + question master vs. everyone), category revealed, prompt hidden from one player, one stroke per turn, vote to identify the fake artist, points to either side.
- Recombine at least three elements from different games plus new elements to form a coherent new game. WHY: recombination produces novelty while keeping proven interaction patterns.
- Keep the "everyone is sometimes the artist" property if you want low downtime. WHY: rotating the active role keeps all players engaged.
## Checklist
- [ ] Listed each element of the source game separately (role, prompt, visibility, scoring).
- [ ] Chose 3+ elements from different games to recombine.
- [ ] Defined who scores and when for every outcome.
- [ ] Named the resulting game.
## Anti-patterns
- Copying a whole game and reskinning it; that is not recombination.
- Combining elements that contradict (e.g. private drawing plus public-process guessing) without a rule that resolves it.

---
name: sokoban-level-design
topic: level design
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"]
---
## Rules
- Enforce the core sokoban constraints: avatar cannot move through blocks; avatar cannot push more than one block at a time; blocks only move when pushed from behind; blocks move only to an adjacent grid cell in a cardinal direction.
- Win condition: get the avatar to the exit.
- Every puzzle must have at least one solution AND at least one way to get permanently stuck. WHY: the stuck state is what creates the planning challenge; without it the level is not a puzzle.
- Difficulty scales with step count and block count, not with board size alone. A level with more steps but the same block count is harder, not bigger.
- Add key blocks and locks for variety: locks are stationary and block avatar movement; when a key block touches a lock, both disappear; in all other respects key blocks behave like normal blocks.
- Two keys and two locks raise both solve difficulty and design difficulty — expect to iterate more.
- Use extra empty space deliberately to misdirect the player. WHY: open space hides the intended solution path.
## Checklist
- [ ] Verified at least one solution exists by playing it, not by reasoning alone.
- [ ] Verified at least one dead-end/stuck state exists.
- [ ] Confirmed no unintended shorter solution was created by added misdirection space.
- [ ] For key/lock levels: confirmed each lock is reachable and each key is not trivially consumed.
## Anti-patterns
- Designing a level with no way to fail — it becomes a corridor, not a puzzle.
- Adding decorative space that accidentally opens a direct route to the exit.
- Assuming a solution exists because the layout "looks" solvable.

---
name: mobile-music-game-wireframe
topic: UI wireframing
confidence: opinion
sources: "The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"
---
## Rules
- Wireframe on templates at the target device's correct aspect ratio, not on a generic rectangle. WHY: touch layout and safe areas depend on real proportions.
- For a touch music-performance game (Guitar Hero / Rock Band style), the required screens are: difficulty select, song select, in-game volume adjustment, and score sharing to social media.
- Keep in-game volume controls reachable during play (settings screen plus in-game access). WHY: players adjust audio mid-session.
- Design the share flow as its own screen/step, not a button that silently posts. WHY: social sharing needs a confirmation and a preview.
## Checklist
- [ ] Difficulty select screen wireframed.
- [ ] Song select screen wireframed.
- [ ] In-game volume control wireframed.
- [ ] Social score-share screen wireframed.
- [ ] All screens drawn at the target aspect ratio.
## Anti-patterns
- Drawing wireframes at desktop aspect ratio for a phone game.
- Burying volume control only in a pause menu with no in-play access.

---
name: level-design-finish-first-level-last
topic: level design process
confidence: opinion
sources: "The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"
---
## Rules
- Build your first level last. WHY (Romero's rule): the first level must teach mechanics you have not finished designing yet; building it early guarantees rework.
- Build a mid-game level first to lock down the core mechanic, then build the tutorial/first level once the mechanic is stable.
## Checklist
- [ ] Core mechanic implemented and playable before any tutorial level is built.
- [ ] First level built only after the mechanic set is frozen.
## Anti-patterns
- Treating the first level as a prototype for the whole game's mechanics.

---
name: designer-growth-broadening
topic: career development
confidence: opinion
sources: "The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. 8 (pp. 173-184)"
---
## Rules
- Watch for "deepening without broadening": getting better at the same design muscle while never adding new ones. WHY: narrow skill growth caps the range of games you can make.
- Deliberately grow in an uncommon direction — study adjacent disciplines, genres, or non-game fields. WHY: a unique mix of influences is what differentiates your work in a crowded field.
- Keep a written plan for how you will stay sharp and develop a distinctive voice.
## Checklist
- [ ] Identified one skill you are deepening and one you are broadening.
- [ ] Chosen a broadening direction that is uncommon among your peers.
- [ ] Written down the plan, not just thought about it.
## Anti-patterns
- Only practicing the discipline you are already strongest in.
- Copying the influences everyone else in your niche already copies.

<!-- A Appendix A: Random Dice, Cards, Letters (pp. 189-190) -->
---
name: randomizer-selection
topic: Choosing dice, cards, or letter draws for randomness
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. A (pp. 189-190)"]
---
## Rules
- Pick the randomizer by the *shape* of the probability curve you need, not by theme:
  - Flat, equal chance for every value → single die or a draw from a uniform deck.
  - Bell curve (middle values common, extremes rare) → sum of 2+ dice (2d6, 3d6).
  - Weighted but bounded → custom deck with duplicated cards.
- Use dice when you need: repeatable independent rolls, open-ended ranges, or values that can repeat (no memory between rolls).
- Use cards when you need: no repeats until the deck cycles, exact control of the odds per outcome, or hidden information held in hand.
- Use letter draws (Scrabble-style tiles) when the outcome must also be a *symbol* the player manipulates (spelling, set collection), not just a number.
- Match the randomizer to the number of outcomes: a d6 gives 6 equally likely results; a 52-card deck gives 52 unique results but only 4 of each rank.
- If the design needs both a curve and no-repeat memory, combine: draw cards, then roll dice to resolve.

## Checklist
- [ ] List every distinct outcome the randomizer must produce.
- [ ] Decide whether repeats within a session are allowed.
- [ ] Decide whether the distribution should be flat or curved.
- [ ] Check the physical/digital cost: more dice = more handling time; bigger decks = more setup and shuffling.
- [ ] Confirm the randomizer's range covers the full stat/score range in the game.

## Anti-patterns
- Using a single die for a "rare critical" outcome — every face is equally likely, so crits are not rare.
- Using a deck when you actually want independent rolls; the deck's memory changes the odds as it depletes.
- Adding dice to "make it more random" — summing dice makes results *less* extreme, not more.
- Choosing a randomizer for flavor before checking whether its probability curve fits the design goal.

> CHECK: The OCR of pp. 189-190 is largely garbled (rotated/overlapping text). The specific tables, dice notations, and letter-tile examples in the original appendix could not be read. Verify the exact randomizer lists and any probability tables against the printed book before relying on the numbers above.

<!-- B Appendix B: Additional Workspaces and Grids (pp. 191-194) -->
---
name: appendix-b-ocr-limited
topic: source-quality
confidence: consensus
sources: ["The Game Designers Workbook, Bobby Lockhart, Eric Lang, ch. B (pp. 191-194)"]
---
## Rules
- Treat this chapter as unusable for rule extraction: the supplied text contains only the title, copyright line, and repeated running heads.
- Do not invent grid dimensions, workspace layouts, or exercise steps that are not present in the text.
- If the physical book is available, re-scan pp. 192-194 at higher resolution before writing any card from this chapter.

## Checklist
- Confirm whether pp. 192-194 contain figures (grids/workspaces) rather than prose; figure-only pages often OCR to nothing.
- Check whether the appendix is a printable template set referenced elsewhere in the book; if so, cite the referencing chapter instead.

## Anti-patterns
- Fabricating "standard" grid sizes or workspace templates and attributing them to this appendix.
- Marking this chapter as covered when no substantive content was read.

> CHECK: pp. 192-194 appear to be image-only (grid/workspace templates). Verify whether they contain any extractable text or only diagrams before producing further cards.
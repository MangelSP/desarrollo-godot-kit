<!-- Introduction: What Is a Game? (pp. 10-22) -->
---
name: plaything-taxonomy
topic: game definition and classification
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Introduction: What Is a Game? (pp. 10-22)"]
---
## Rules
- Classify every interactive entertainment object on two axes: **has a goal?** and **players interact with each other to affect the outcome?**
- Toy = no goal. Player just plays. (e.g. a Frisbee, a plastic dinosaur)
- Puzzle = has a goal, but the player works alone; no interaction between agents. (e.g. brainteaser, solitaire logic puzzle)
- Competition = two or more agents, but each acts independently; one player's actions do not change the other's outcome. (e.g. a foot race)
- Game = has a goal **and** agents interact — either against each other or together against the game itself.
- Treat "agent" as any actor that makes decisions: a human player, the computer/AI, or the game system itself.
- To convert a toy into a game, add exactly three things: a goal, rules, and player interaction. (Frisbee → Frisbee golf / Ultimate)
- Cooperative games are a valid game subtype: all agents work together against the game system rather than against each other.
- WHY: this taxonomy tells you what your design still lacks. If playtesters say it "feels like a toy", the missing ingredient is a goal or interaction, not more content.

## Checklist
- [ ] Can a player lose or win? If no → it is a toy, not a game.
- [ ] Do players' choices change what other players (or the system) must do? If no → it is a competition or puzzle.
- [ ] Is the goal stated in one sentence a new player can repeat back?
- [ ] Are the rules written down, not just implied by the prototype?
- [ ] If cooperative: is the "opponent" (the game system) capable of applying pressure?

## Anti-patterns
- Calling a goal-less sandbox a game. It is a plaything; players will not return without a goal.
- Assuming "multiplayer" equals "game". Parallel independent play (each player runs their own race) is a competition, not a game.
- Adding rules without adding interaction — you get a more complex toy, not a game.

---
name: game-dev-process
topic: development workflow
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Introduction: What Is a Game? (pp. 10-22)"]
---
## Rules
- Run every project through five repeating stages: **Concept → Design → Implementation → Testing → Evaluate**.
- Concept: state what would make this a great game, in one or two sentences.
- Design: define the goal and how the game works; brainstorm broadly and without judging ideas.
- Implementation: choose a structure and build a **prototype** — an early version meant only for testing, not for shipping.
- Testing: play it. Ask "does it work?" and "how can we improve it?"
- Evaluate: analyze test results, then decide between two actions — adjust the current prototype, or discard it and try a different one.
- Loop back to Design or Implementation after Evaluate; the process is a cycle, not a line.
- Keep a dedicated development notebook for the whole project: observations, data, designs, test results.
- WHY: writing decisions down turns playtest impressions into comparable data across iterations, so you can tell whether a change actually helped.
- There is no single correct way to approach a project; the process is a scaffold, not a rulebook.

## Checklist
- [ ] Notebook exists and is used for every session.
- [ ] Goal written down before building the prototype.
- [ ] Prototype is cheap and disposable by design.
- [ ] At least one playtest with another person before evaluating.
- [ ] Evaluation recorded as a decision: keep, adjust, or replace.

## Anti-patterns
- Polishing a prototype before it has been tested. Prototypes are for learning, not for looks.
- Skipping Evaluate and jumping straight to more Implementation — you lose the reason for the change.
- Treating the five stages as one-way. Without looping back, testing produces no design change.

---
name: game-research-and-idea-sourcing
topic: ideation
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. Introduction: What Is a Game? (pp. 10-22)"]
---
## Rules
- Source ideas from four recurring origins: boredom, a desire to teach something, frustration with existing games, and mashups of two known games.
- Mashup recipe: take the core mechanic of one game and the theme or setting of another. (Example cited: a classic dice-rolling core + Japanese movie monsters.)
- Maintain two running lists in the notebook: **features I want to use** and **features I do not want to use**.
- Build the "do not want" list from your own negative play experiences — e.g. early player elimination, runaway leaders, long downtime.
- Study your least favorite games as carefully as your favorites; the failures are more instructive.
- Play widely. Designers are typically avid players of their own medium.
- WHY: a written wish list and hate list converts taste into concrete design constraints you can check a prototype against.

## Checklist
- [ ] Favourite games listed with the specific reason (theme? a rule? tension?).
- [ ] Least favourite games listed with the specific reason.
- [ ] Wish list of themes/rules to reuse started.
- [ ] Avoid list started.
- [ ] At least one mashup idea written as "core of X + theme of Y".

## Anti-patterns
- Copying a favourite game wholesale. Study the mechanic, not the whole product.
- Only studying good games — you will repeat the mistakes you never named.
- Keeping ideas in your head. Untracked ideas cannot be compared or combined later.

---
name: prototyping-with-paper-dice
topic: physical prototyping
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Introduction: What Is a Game? (pp. 10-22)"]
---
## Rules
- Build dice from stiff paper (heavy construction paper or index cards) to prototype randomisers in minutes.
- d6 net: six 2-inch squares in a cross — four squares in a column, three across the middle row.
- Number the faces 1–6 in the centre of each square, cut out the cross, fold on the lines, tape the edges.
- Balance tip: apply the same amount of tape to every edge, otherwise the die is weighted and rolls unfairly.
- d8: build from triangles instead of squares.
- Standard d6 fact: opposite faces always sum to 7. Use this to lay out pips correctly.
- Dice faces need not be numbers — use words, letters, symbols, or pictures (a letter-dice game is still a dice game).
- To turn dice into a game, add the three missing pieces: a goal, simple rules, and player interaction. (e.g. "roll three party-hat symbols to win")
- WHY: paper dice let you test randomness and symbol distribution before committing to art, manufacturing, or code.

## Checklist
- [ ] Net drawn with equal-sized faces.
- [ ] Opposite faces sum to 7 (d6).
- [ ] Tape distributed evenly on all edges.
- [ ] Goal and rules written in the notebook before the first play.
- [ ] Played with a second person and the result recorded.

## Anti-patterns
- Uneven tape or folded corners — the die becomes biased and your test data is worthless.
- Testing a dice game solo only. Interaction problems only appear with a second player.
- Jumping to a digital randomiser before the physical rule set is proven.

> CHECK: The chapter's "Try This!" for the d8 says to use triangles, but gives no net layout. Verify a correct octahedron net before teaching it.

<!-- 3 Your Brain on Games (pp. 75-89) -->
---
name: flow-state-design
topic: player motivation / flow
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Treat "fun" as the primary goal, not a side effect of learning or escapism. Players start playing because the experience itself is enjoyable; learning and social skills are byproducts, not the entry hook. WHY: if you justify a mechanic only by its educational value, players who don't want to learn will drop out.
- Aim for flow: a state where the player is fully absorbed, forgets outside problems, and loses track of time. Use this as the success criterion for a session, not "player completed the level". WHY: absorption is what makes a session feel worth repeating.
- Keep challenge matched to player skill so absorption is possible; flow is described as the state where we "feel and perform our best". WHY: too easy → boredom, too hard → anxiety, both break absorption.
- Design for flow in non-game contexts too (creation, movement, craft) — the same absorption principle applies to any interactive system. WHY: flow is a property of the activity, not of games specifically.
> CHECK: the chapter names flow but gives no numeric difficulty-tuning formula; verify any specific challenge/skill ratio against other sources before citing numbers.

## Checklist
- Can a player describe a session as "I lost track of time"?
- Is the core loop enjoyable on its own, before any reward or learning payoff?
- Does difficulty scale with demonstrated player skill?

## Anti-patterns
- Selling the game on its educational or therapeutic value instead of the experience.
- Assuming players play to escape or to learn; those are outcomes, not motives.

---
name: types-of-fun
topic: player experience / fun taxonomy
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Pick which kinds of fun your game delivers and design mechanics that serve them. The chapter lists five:
  - Hard fun — joy from doing something challenging.
  - Simple fun — relaxing, mindless activity.
  - Creative fun — building or making something.
  - Destructive fun — destroying something.
  - Exploratory fun — discovering the unknown.
- WHY: "fun" is not one thing; a mechanic that serves hard fun (tight timing, high failure rate) actively fights simple fun (low pressure, no fail state).
- Use the list as a coverage check: a game that only delivers one type will appeal to a narrow audience; mixing two or three broadens appeal without diluting the core.
- Map each major system to at least one fun type; if a system serves none, cut it.

## Checklist
- Which of the five fun types does each core system serve?
- Do any two systems pull toward incompatible fun types (e.g. punishing difficulty plus mindless relaxation)?
- Is the fun type stated in the pitch consistent with the mechanics actually built?

## Anti-patterns
- Treating "fun" as a single scalar and tuning only difficulty.
- Adding a creative or destructive mode that has no mechanical support (e.g. a build mode with nothing to build toward).

---
name: reward-system-dopamine
topic: neuropsychology of reward
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Assume the player's brain reinforces whatever the game rewards. The VTA releases dopamine, which travels to the nucleus accumbens (NAc) and produces the feeling that the experience was good and should be repeated. WHY: this is the mechanism behind "one more turn" — the reward must be delivered for the loop to stick.
- Deliver a reward signal on every meaningful player action, not only at level end. Dopamine pathways also reach areas controlling emotion, attention, planning, movement, and memory. WHY: frequent small rewards keep attention and learning engaged, not just pleasure.
- Vary reward types across systems (progress, discovery, social, mastery) rather than scaling one currency. WHY: dopamine is tied to many pathways, so a single reward channel saturates and stops motivating.
- Treat reward design as behavior reinforcement: whatever you pay out most reliably is what players will optimize for.

## Checklist
- Does every core action produce a visible/audible reward within a short delay?
- Are rewards spread across more than one pathway (progress, social, mastery, discovery)?
- Is there any action the player repeats that gives no feedback at all?

## Anti-patterns
- Back-loading all reward to the end of a level or match.
- Rewarding only one behavior (e.g. kills) so all other play styles feel unrewarded.
- Chasing compulsion: the chapter notes addiction involves loss of control and continuing despite negative consequences — do not design toward that.

---
name: mood-chemicals-beyond-dopamine
topic: neuropsychology / player emotion
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Design for more than pleasure. Four chemicals are named and each maps to a design lever:
  - Dopamine — pleasure/reward → use for progress and success feedback.
  - Serotonin — mood, sleep, learning, and the feeling of being full or satisfied → use for completion, closure, and a satisfying end state.
  - Oxytocin — closeness to other people → use for co-op, shared goals, and social bonding moments.
  - Endorphins — released under stress, fear, or pain, reducing pain and improving mood → use for tension, scares, and intense sequences.
- WHY: a game that only triggers dopamine feels hollow; satisfaction, bonding, and tension are separate levers with separate mechanics.
- Note that low serotonin is linked to depression — a game with no satisfying closure leaves players flat even if it is rewarding moment to moment.

## Checklist
- Does the game have a satisfying completion state (serotonin), not just a reward stream?
- Is there a mechanic that creates closeness between players (oxytocin)?
- Is there a deliberate tension or fear beat (endorphins)?

## Anti-patterns
- Using only score and loot as emotional levers.
- Ending sessions abruptly with no closure beat.

---
name: maslow-and-modern-needs
topic: player needs / motivation
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Games satisfy higher-order needs, not survival needs. Maslow's pyramid (bottom to top): food/shelter → safety → love/belonging → self-esteem → growth and creativity. Each level builds on the one below. WHY: players arrive with lower needs already met, so design for the top of the pyramid.
- Target the top levels directly: understanding, exploration, adventure, novelty, excitement, and make-believe. Games deliver these safely — the player can feel like a soldier without real danger.
- Prefer the modern three-need model for concrete design decisions:
  1. Autonomy — the player feels independent and able to make choices.
  2. Relatedness — the player cares for others and is cared for.
  3. Competence — the player feels good at what they do.
- WHY: the three-need model is directly actionable (add choices, add social bonds, add mastery feedback) while the pyramid is a hierarchy, not a checklist.
- Use the pyramid as a sanity check that you are not designing for needs the player already satisfies outside the game.

## Checklist
- Does the player make meaningful choices (autonomy)?
- Is there a person or group the player cares about in-game (relatedness)?
- Does the player get clear evidence of getting better (competence)?
- Does the game offer exploration, novelty, or make-believe?

## Anti-patterns
- Designing around survival or scarcity themes as if the player lacked those needs.
- Offering choices that are cosmetic only — that fails autonomy.
- No visible skill progression — that fails competence.

---
name: emotional-payoffs
topic: player motivation / payoff design
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Define the payoff — what the player gets out of the game — before building systems. The chapter names six recurring payoffs:
  - Emotional: feeling clever, funny, cool, or thrilled; getting lost in a story.
  - Socializing: playing with friends/family, feeling that you matter to them; also a place to practise good sportsmanship.
  - Creativity: expressing yourself through builds, decks, clues, or performance.
  - Strategic thinking: outthinking opponents, planning several moves ahead, solving a mystery.
  - Collecting: gathering cards or items, and belonging to a community of collectors.
  - Competition: the thrill of victory.
- Design the payoff moment explicitly. Example given: Cranium is built around the moment players high-five each other. WHY: naming the moment forces the mechanics to deliver it rather than hoping it emerges.
- Treat losing well as a designed outcome: a game where players rage on loss has a payoff problem, not a player problem.
- Support the metagame — everything the player can do around the game: collecting, trading, discussing strategy, making deals, practising. WHY: these activities extend the joy beyond the moment of play and lengthen the game's life.

## Checklist
- Can you name the single payoff moment your game is built around?
- Which of the six payoffs does the game deliver, and which systems deliver each?
- Does the game support metagame activity outside the session?
- Is there a graceful loss experience?

## Anti-patterns
- Building mechanics first and hoping a payoff emerges.
- Ignoring the metagame so the game only exists while it is being played.
- Rewarding only victory, leaving losing players with nothing.

---
name: games-improve-cognition
topic: cognitive benefits / evidence
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 3 (pp. 75-89)"]
---
## Rules
- Expect measurable cognitive transfer from strategy games. Cited evidence: a 2008–2009 study gave half a middle-school math class a 30-week chess program on top of normal instruction; the chess group finished with higher test scores and grades.
- Expect faster pattern recognition in experts. Brain scans of professional vs amateur Shogi players found the caudate nucleus activated in pros when given only two seconds to move; amateurs did not show this, and pros did not use it when given longer. Interpretation: the caudate nucleus supports fast pattern recognition and next-move selection, and is now thought to relate to memory and learning rather than only voluntary movement.
- Expect long-term brain-health benefits. A 2003 New England Journal of Medicine study found older people who played board/card games, did crosswords, read, or wrote for fun were less likely to develop dementia or Alzheimer's. A French study found board game players were 15 percent less likely to develop dementia than non-gamers.
- Use these findings as design justification for depth and pattern-based play, not as marketing copy. WHY: the benefits come from sustained, pattern-rich play, which is a design property.

## Checklist
- Does the game have learnable patterns an expert can recognise quickly?
- Is there a long-term progression that rewards sustained play?
- Are fast and slow decisions meaningfully different in the game?

## Anti-patterns
- Claiming cognitive benefits for games with no pattern depth or decision variety.
- Citing the 15 percent figure without noting it comes from a specific French study on board games.

> CHECK: the chapter does not give the sample size or full citation for the 2003 NEJM study or the French study; verify before quoting in external material.

<!-- 4 Game Design (pp. 90-112) -->
---
name: game-idea-sources
topic: Generating game concepts
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 4 (pp. 90-112)"]
---
## Rules
- Treat every game as starting from a design problem, not just a "cool idea": phrase it as "How do I make a <type> game about <theme> that <audience/goal>?" — this forces you to define scope, format and target player before designing.
- Start from either a **theme** or a **mechanic**, not both at once. Pick one as the anchor and derive the other.
- Mashup method: take 1–2 elements (dice, drafting, hidden roles) from game A and graft them onto game B, then rewrite the rules that the graft breaks. Cheap way to get a novel core loop.
- Random generator method: list N themes, N mechanics, N components (N = sides of your die: 6/12/20), roll separately for each, then design the game that the combination forces. Use when stuck.
- Mine non-game sources for themes: news events, books, sports, travel, movies, dreams, personal experiences. Themes are free; mechanics are the work.
- Keep a design notebook: write a short design memo for each idea. The act of writing exposes whether the idea is actually good.
## Checklist
- [ ] Can I state the design problem in one sentence?
- [ ] Is my anchor a theme or a mechanic (not a vague vibe)?
- [ ] Does the idea imply a format (board / card / RPG / microgame)?
- [ ] Have I written it down before evaluating it?
## Anti-patterns
- Stopping at the first idea — the first idea is rarely the best one.
- Judging ideas during brainstorming; negative judgment kills volume.
- Getting attached to an idea before testing it.
- Designing theme and mechanics simultaneously with no anchor — leads to a game that does neither well.
> CHECK: OCR shows "Marvin Gardens" vs real "Marven Gardens" — irrelevant to game design, ignore.

---
name: game-elements
topic: Core elements of a tabletop game
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 4 (pp. 90-112)"]
---
## Rules
Design every game against these five elements; if one is undefined, the game is not designed yet:

| Element | Question it answers | Notes |
|---|---|---|
| Space | Where is it played, where is it set? | Play location and fiction/setting are separate; a game can have one without the other (Scrabble has no setting). |
| Components | What physical pieces exist? | Board, cards, dice, counters, timers, tokens, money, tiles, maps, apps. Fewer components = cheaper and faster to prototype. |
| Mechanics | What choices does the player make? | One **core mechanic** plus several supporting ones. A game is "a series of interesting choices." |
| Goals | How do you win? | Must be a single explicit victory condition. Cooperative games: one shared win/lose condition for the whole team. |
| Rules | How do you play? | Must cover: box contents, overview, setup, goal, turn steps, scoring. |

- Common mechanics to draw from: acting, betting, rolling dice, bidding, attacking, eliminating players, pattern building, tile placement, trading, voting, storytelling, card drafting, press-your-luck, tapping (rotate a card 90° to spend/activate it, untap to reuse).
- Card drafting: pick from a limited face-up set; the pick both helps you and denies opponents. Use when you want indirect player interaction.
- Press-your-luck: player may repeat a risky action for a big payoff until they stop or bust (e.g. blackjack). Use to add tension without adding rules.
- Cooperative design: define one shared victory condition and at least two distinct loss conditions (e.g. Pandemic: cure all diseases = win; pandemic outbreak OR running out of time = lose).
- Resources: name the concrete resource types (wool, brick, lumber, grain) and the conversion (spend resources → build roads/settlements/cities).
## Checklist
- [ ] Space: play surface and setting both decided (or explicitly none)?
- [ ] Components: full list written, each with a purpose?
- [ ] Mechanics: one core mechanic named, supporting mechanics listed?
- [ ] Goals: victory condition stated in one sentence; loss conditions stated?
- [ ] Rules: setup, turn order, turn actions, win, scoring all covered?
## Anti-patterns
- Mechanics with no decision attached (pure randomness with no choice).
- Victory condition that is vague or discovered mid-game.
- Adding components that no mechanic uses.
- Cooperative game with only a win condition and no way to lose.

---
name: design-principles-fun
topic: Design principles for fun and fairness
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 4 (pp. 90-112)"]
---
## Rules
- **Play length**: match length to the game's depth. Light games ~15 min (Uno); heavy games may run hours (Monopoly, Dominion) or multi-session (D&D campaigns). Default bias: err shorter. If you can cut time without cutting decisions, cut it.
- **Luck vs strategy**: aim for a mix. Pure strategy (chess, Go) and pure luck (Bunco) are both valid but niche. Luck lets players avoid agonizing over every move; too much luck makes thinking feel pointless.
- **Fairness / catch-up**: avoid early elimination and runaway leaders. Two standard fixes:
  - Keep all players in until the end (common in European-style games).
  - Add a catch-up feature: a bonus for a big play (Scrabble all-tiles bonus) or a mechanism that stalls the leader (Settlers of Catan's Robber).
- **Balance**: the game should be challenging but not punishing; the outcome should feel deserved.
- Microgame constraints: few components, fast rounds (e.g. 16 cards + a few tokens). No fixed definition of "small" — one card and a few coins still counts. Small size does not mean shallow.
## Checklist
- [ ] Target play length written down and tested against real sessions?
- [ ] At least one luck source and one skill source present?
- [ ] No player can be eliminated before the final third of the game?
- [ ] A trailing player has a plausible path to win?
- [ ] Rules tested by someone who is not the designer?
## Anti-patterns
- Runaway leader with no catch-up mechanism — the last half of the game is decided.
- Early player elimination in a long game.
- Luck so dominant that player decisions don't change the outcome.
- Padding play length with downtime rather than decisions.

---
name: iterative-design-process
topic: Iterative design and prototyping workflow
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 4 (pp. 90-112)"]
---
## Rules
- The loop is: **idea → prototype → test → change → repeat**. Repeat until the game works; there is no fixed number of iterations.
- Separate **design** (concept, rules, elements) from **development** (turning the concept into a publishable product). The same person may do both, but treat them as distinct phases.
- Write a design document once the concept is settled. Format is free; its job is to let other people understand the goal and rules. This is the handoff artifact to development.
- Write the rules **before** playtesting: testers must be able to play without you explaining. Rules must cover box contents, setup, who goes first, what happens each turn, how to win, how to score.
- Rules length is a tradeoff: too many instructions is as much a problem as too few.
- Playtest at every stage of design and development, not just at the end.
- Study an existing game similar to yours: read its rules, note what is confusing, note what you would do differently, then write yours.
- Brainstorming rules: don't stop at the first idea; generate far more ideas than you need; treat every idea as good during the session (no negative judgment); don't get attached; test the ideas.
## Checklist
- [ ] Problem statement written in one sentence.
- [ ] Prototype built (paper is fine).
- [ ] Rules written covering setup / turn / win / scoring.
- [ ] Rules tested by a reader who was not present at design time.
- [ ] Design document written for the development handoff.
- [ ] At least one iteration completed after the first playtest.
## Anti-patterns
- Playtesting with the designer explaining the rules — hides rule gaps.
- Skipping the written rules and going straight to a prototype.
- Treating the first prototype as the design.
- Brainstorming with immediate criticism.
- No design document, forcing developers to guess intent.

<!-- 5 Game Development and Beyond (pp. 113-132) -->
---
name: design-vs-development-loop
topic: game production pipeline
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Treat design and development as two distinct phases of one repeating loop: design = idea + prototype + test + revise; development = break, refine, produce, ship.
- Keep the design document alive through the whole development cycle; it is the contract between designer intent and the dev team.
- Write two versions of the design doc: a short pitch paragraph for managers/marketing, and a detailed spec (mechanics, rules, components) for developers, playtesters, writers, artists, engineers.
- Expect the dev team to include non-designers: playtesters, writers, artists, managers, marketing, product engineers. Each needs different depth of information.
- WHY: developers who lack the designer's intent will "fix" the game into something else; a shared doc prevents drift.

## Checklist
- [ ] Short description exists for non-technical stakeholders.
- [ ] Detailed spec covers mechanics, rules, components, edge cases.
- [ ] Doc is versioned and updated after every playtest round.
- [ ] Every team role can find the info it needs without asking the designer.

## Anti-patterns
- Treating the design doc as a one-time deliverable written before development starts.
- Assuming the dev team already knows the rules because the designer does.
- Skipping the loop and going straight from idea to production.

---
name: prototyping-kit-and-paper-prototypes
topic: prototyping
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Build the cheapest possible prototype first: paper board, hand-written rules, scavenged tokens. Goal is only to test whether the concept is fun.
- Build several prototypes in parallel or in sequence; adjust between each.
- Keep a reusable prototyping kit: old playing cards, card sleeves, full-page/name-tag/address labels, paper of many colors and weights, dice, tokens from other games, plastic cubes and chips, sandwich and snack bags, boxes.
- For card prototypes, print faces on paper and sleeve them with a real playing card behind for stiffness so they can be shuffled and dealt. Glueing a discarded card to the back is the fallback.
- Make meeples by drawing shapes on cardstock/chipboard, cutting several copies, and gluing them in layers until thick enough to stand. Typical meeple height 0.5–1.5 inches.
- Make a sturdy board: print/draw on 8.5x11 paper, glue to chipboard cut 0.25 inch larger on all sides, cover the back with contact paper, tape the edges with binding or duct tape.
- For a folding board, join two 8.5x11 panels with binding tape on the underside, leaving a small gap at the fold.
- WHY: paper is fast to change; a physical prototype exposes rule ambiguity that a mental model hides.

## Checklist
- [ ] Rules written out in full detail — better too much than too little.
- [ ] All components present and playable without the designer explaining.
- [ ] Prototype cost low enough that throwing it away is painless.

## Anti-patterns
- Investing in art or final components before the mechanics are proven fun.
- Testing only in your head or on a screen when a table prototype would be faster.
- Writing terse rules that only make sense to the author.

---
name: playtesting-protocol
topic: playtesting
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Playtest at multiple stages: early tests check whether mechanics are fun before rules are final; later tests fix gameplay and rule issues; final tests check packaging and presentation.
- Playtest with yourself first, then with outsiders who have never seen the game.
- Do not explain the rules during a test. Hand over the written rules and observe whether players can follow them unaided.
- During the session: watch silently and take notes. After the session: interview players about what they liked, disliked, and found unclear.
- Record all observations in a design notebook, then revise the game and rules, then playtest again. Repeat until the game is fun and playable.
- Bring in fresh testers after each revision round so the rules are validated by people with no prior exposure.
- Expect many iterations — hundreds of tests is normal for a polished design.
- WHY: the designer cannot see their own game objectively; only naive players reveal unclear rules and unfun mechanics.

## Checklist
- [ ] Rules readable and complete without verbal explanation.
- [ ] Notes taken on every unclear rule and every moment of confusion.
- [ ] Post-game interview conducted with each tester group.
- [ ] Changes made and re-tested with new players.
- [ ] Packaging/presentation tested in a late round.

## Anti-patterns
- Skipping playtesting — the most common mistake of new designers.
- Explaining rules verbally and counting that as a successful test.
- Testing only with friends who already know the game.
- Arguing with testers instead of noting their confusion.

---
name: publishing-routes
topic: publishing and manufacturing
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Three routes to market: (1) work inside a game company that publishes and markets your game, (2) design independently and license/pitch to a publisher, (3) self-publish.
- Self-publishing means owning every step: funding, artwork, manufacturing, distribution, marketing. Treat it as running a business, not just making a game.
- Small companies and self-publishers commonly raise money via investors or crowdfunding (Kickstarter and similar).
- Manufacturing sequence: art department polishes graphics and edits rules → designs packaging → production selects materials for board, pieces, packaging → computer files are printed.
- Distribution: publishers rarely sell direct. Distributors buy in bulk at wholesale or below-wholesale, warehouse the stock, take store orders, and ship.
- Retail channels: small hobby/game shops stock hobby games; big-box stores stock mass-market plus popular hobby titles; online marketplaces sell everything.
- Crowdfunding reference point: in 2017 the average successful tabletop campaign raised over $65,000.
- WHY: each route shifts risk and control — licensing trades margin for reach, self-publishing trades reach for margin and control.

## Checklist
- [ ] Route chosen before budgeting (in-house / license / self-publish).
- [ ] Funding source identified if self-publishing.
- [ ] Art and rule editing scheduled before production.
- [ ] Distribution channel matched to game type (hobby vs mass-market).
- [ ] Reprint plan considered if demand exceeds first print run.

## Anti-patterns
- Assuming a publisher will handle manufacturing if you never pitched or signed.
- Underestimating print-run demand — under-printing causes scalping and lost sales.
- Self-publishing without budgeting for art, editing, and marketing, not just printing.

---
name: market-segments-and-marketing
topic: marketing
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Segment the board game market into four buckets before writing any marketing copy: mass-market, hobby, American specialty, European.
- Mass-market: classic family and party games sold in big-box stores (Monopoly, Scrabble, Taboo, Boggle, Cranium, most kids' games). Broad, casual audience.
- Hobby: complex games with recurring purchases — expansions, cards, miniatures. Covers roleplaying, war games, collectible card games. Audience buys repeatedly.
- American specialty: American games that are neither mass-market nor hobby — strategy, sports, mystery titles.
- European (or Euro-style): mostly German in origin, more strategic and thoughtful than mass-market; now produced worldwide. Examples: Settlers of Catan, Carcassonne, Ticket to Ride, Pandemic, Puerto Rico.
- Match advertising media to the segment: TV, magazine, newspaper, online.
- WHY: a game marketed to the wrong segment gets ignored by the people who would actually buy it.

## Checklist
- [ ] Segment assigned to the game.
- [ ] Comparable titles named within that segment.
- [ ] Ad channels chosen that reach that segment.
- [ ] Price and complexity consistent with the segment's expectations.

## Anti-patterns
- Marketing a heavy strategy game to the mass-market family audience.
- Assuming one ad channel reaches all four segments.
- Ignoring the recurring-purchase behavior of hobby players.

---
name: crowdfunding-and-demand-risk
topic: crowdfunding
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. 5 (pp. 113-132)"]
---
## Rules
- Crowdfunding works best with a polished prototype already playtested — backers fund production, not idea discovery.
- Set a funding goal that covers development plus production, not just printing.
- Plan the retail print run separately from the backer run; backer demand does not equal total demand.
- Expect demand to overshoot: a successful campaign can leave retail pre-orders far exceeding the extra copies printed, driving secondary-market prices up and forcing a reprint.
- WHY: a campaign that under-prints loses retail sales and damages the brand; a campaign that over-prints ties up cash.

## Checklist
- [ ] Prototype polished and playtested before launch.
- [ ] Goal covers development + production.
- [ ] Backer copies and retail copies budgeted separately.
- [ ] Reprint contingency planned.
- [ ] Fulfillment weight and shipping cost estimated (large games can be very heavy).

## Anti-patterns
- Launching a campaign with an untested idea.
- Printing only the backer quantity and ignoring retail pre-orders.
- Treating crowdfunding as free money rather than an obligation to deliver.

> CHECK: The chapter's Gloomhaven figures (goal $70,000, ~5,000 backers, ~$400,000 raised, 2,000 retail copies vs 25,000 pre-orders, 20 lb box) are cited as a case study; verify exact numbers against the printed page before reusing them as data.

<!-- Glossary (pp. 153-159) -->
---
name: game-genre-and-format-vocabulary
topic: Game genres, formats, and play contexts
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Classify a game by its core player activity before anything else:
  - Adventure game = interactive story driven by exploration + puzzle-solving.
  - Escape room = physical adventure game; players solve puzzles and clues to leave a room.
  - Cooperative game = players must work together (win/lose as a group).
  - Collectible/trading card game (CCG) = strategy card game with designed cards the player collects to customize a deck.
  - Eurogame = board game tradition originating mainly in Germany.
  - Hobby game = specialty game for a passionate niche audience.
- Separate "plaything" (interactive entertainment: toy, game, or puzzle) from "game" when scoping a project — a puzzle or toy may need no win condition.
- Treat augmented reality (AR) as a distinct format: it inserts real-world images into the game environment or interacts with real-world objects. Do not conflate AR with 3-D rendering or holography.
- Use "metagame" for everything around the core play the player can participate in (deck building outside matches, community, collecting). Design the metagame deliberately, not as an afterthought.
- Use "mechanic" for a specific element or type of gameplay; use "deck building" for the mechanic where the player selects cards to build a custom set.
- Use "theme" for the central recurring idea; keep theme separate from mechanics in design docs.
## Checklist
- [ ] Genre label chosen (adventure / escape room / CCG / Eurogame / hobby) and written down.
- [ ] Player count and cooperation model stated (solo, competitive, cooperative).
- [ ] Format stated (physical, digital, AR, hybrid).
- [ ] Metagame elements listed separately from in-session mechanics.
- [ ] Theme written as one sentence, distinct from the mechanic list.
## Anti-patterns
- Calling any story-driven game an "adventure game" when it has no exploration or puzzle-solving loop.
- Treating AR as a rendering feature rather than a gameplay format with real-world interaction.
- Mixing theme and mechanic in the same design bullet, which hides which one is actually changing.
> CHECK: Glossary gives no numeric thresholds for genre definitions; genre boundaries are descriptive, not measurable.

---
name: game-production-and-business-terms
topic: Publishing, funding, and manufacturing vocabulary
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Distinguish the roles in the supply chain: manufacturer makes the product; distributor buys from the manufacturer and sells/delivers to stores; distribution is how the product is divided up and shipped.
- Distinguish mass market (large-scale sales) from hobby game (specialty niche). Pricing, packaging, and marketing differ per channel.
- Know the funding routes: crowdfunding (many people each contributing a small amount), investor (gives money for future profits), license (sell the right to publish; author typically gets royalties, a percentage of profits).
- Protect the invention: a patent is a government license giving the inventor/creator the sole right to make and sell the product.
- Budget for packaging (wrapper plus all container parts) and marketing (communication to make the business known) as separate line items from manufacturing.
- Treat "brick-and-mortar" as the physical-store channel; plan how it differs from online sales.
- Royalty = money paid to the creator per unit sold. Model it per unit, not as a lump sum.
## Checklist
- [ ] Funding route chosen and its obligations written down (crowdfunding / investor / license / self-fund).
- [ ] Channel chosen (mass market vs hobby) and packaging spec matches it.
- [ ] Royalty rate and per-unit basis defined in any license.
- [ ] Patent decision made before public disclosure.
- [ ] Distributor vs direct-sales path decided.
## Anti-patterns
- Confusing distributor with manufacturer when planning margins.
- Assuming a patent is automatic — it must be applied for and granted.
- Treating marketing as optional after manufacturing costs are sunk.
> CHECK: Glossary defines terms but gives no royalty percentages, margins, or minimum print runs.

---
name: playtesting-and-iteration
topic: Playtesting, prototyping, and iterative design
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Playtest = testing a new game for bugs and design flaws before bringing it to market. Do it before release, not after.
- Build a prototype (an early version of a design used for testing) rather than polishing assets first.
- Work iteratively: arrive at the result through repeated rounds, making the product or idea a bit better each round. Never expect one pass to be final.
- Brainstorm without judgment, often in a group, to generate options before evaluating them.
- Use critique (a judgment expressing an opinion) as structured feedback, and keep it separate from the brainstorm phase.
- Target "flow" — the state where players feel and perform their best — as the success criterion for a session, not just "fun".
- Aim for intuitive design: players should understand things without needing proof or explanation.
## Checklist
- [ ] Prototype exists before any final art or packaging work.
- [ ] At least one playtest round completed with recorded design flaws.
- [ ] Each iteration names the one thing being improved this round.
- [ ] Feedback captured as critique (opinion) vs bug (defect), separately.
- [ ] Flow checked: did players stay engaged and perform well?
## Anti-patterns
- Skipping playtests because the rules "seem clear" to the designer.
- Judging ideas during brainstorming, which kills option generation.
- Iterating on everything at once so you cannot tell what caused the improvement.
> CHECK: Glossary defines playtest and iterative process but gives no sample sizes or iteration counts.

---
name: player-motivation-and-brain-chemistry
topic: Player motivation, reward, and social bonding
confidence: opinion
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Design reward loops with dopamine in mind: it is a neurotransmitter that produces feelings of pleasure.
- Support well-being and happiness with serotonin, a neurotransmitter with wide-ranging body functions that contributes to feelings of well-being and happiness.
- Use social interaction as a reward channel: oxytocin is released when interacting with people you like and makes you happy — cooperative and social play taps this.
- Reduce frustration and pain perception with endorphins, hormones released in the brain that reduce pain and improve mood.
- Treat the nucleus accumbens (NAc) as the addiction-related brain region; be deliberate about compulsion loops rather than accidental ones.
- The caudate nucleus plays roles in different types of learning — vary learning tasks (pattern, sequence, recall) to engage it.
- Organize player needs with a pyramid of needs: most-important needs at the base, less-important above. Satisfy lower needs before layering higher ones.
- Note that "agent" means a player of a game and can be a person, a computer, or the game itself — design AI opponents as agents with the same affordances as humans.
## Checklist
- [ ] Reward schedule mapped to a specific chemical/behavioral goal (pleasure, bonding, relief).
- [ ] Social/cooperative channel present if oxytocin-driven bonding is a goal.
- [ ] Compulsion loops reviewed for addiction risk (NAc) and documented.
- [ ] Learning tasks varied to exercise different learning types.
- [ ] Needs pyramid used to order feature priority.
## Anti-patterns
- Using only dopamine-style variable rewards and ignoring social and relief channels.
- Shipping compulsion loops without reviewing addiction risk.
- Treating AI opponents as non-agents with different rules than human players.
> CHECK: Glossary lists brain terms but gives no dosages, timings, or measured effects; treat all mappings as design heuristics, not science.

---
name: logic-and-deduction-in-game-design
topic: Logic, deduction, and puzzle design
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Define logic as the math-based principle that things should work together in an orderly way. Enforce internal consistency: every rule must combine with the others without contradiction.
- Use deduction (using logic or reason to figure out or form an opinion) as the core loop for mystery and puzzle games.
- Use anagrams (a word or phrase made by reordering another's letters) as a concrete word-puzzle mechanic.
- Use tarot cards and fortune-telling props as thematic devices; they are special cards used to tell fortunes, not a rules system.
- Keep "strategy" (a careful plan for achieving a goal, plus the skill of making and carrying out plans) distinct from "tactics" (a carefully planned action to achieve something). Design both layers.
- Use "simultaneous" resolution when players act at the same time; it changes balance versus turn order.
- Use "suit" (all cards sharing a symbol, e.g. hearts or spades) as the grouping axis for card mechanics.
## Checklist
- [ ] Every rule checked against the others for contradictions (orderly interaction).
- [ ] Deduction loop has enough information for a solvable conclusion.
- [ ] Strategy layer and tactics layer both present and named.
- [ ] Turn order or simultaneous resolution chosen deliberately.
- [ ] Card grouping axis defined (suit, type, cost).
## Anti-patterns
- Puzzle with insufficient clues, making deduction impossible rather than hard.
- Mixing strategy and tactics in one design note so neither is tuned.
- Adding a word mechanic (anagram) without a validation rule for acceptable answers.
> CHECK: Glossary defines logic and deduction but gives no puzzle-difficulty metrics.

---
name: history-and-culture-theme-reference
topic: Historical and cultural theme vocabulary
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Use BCE/CE for dates: BCE counts down to zero, CE counts up from zero; these nonreligious terms correspond to BC and AD.
- For ancient Egypt themes, use the correct terms: pharaoh (ruler), papyrus (paper from the papyrus plant), pyramid.
- For ancient Rome themes: legion (large group of soldiers), Latin (language of ancient Rome and its empire), chariot (two-wheeled cart with a platform, pulled by horses).
- For Mesoamerican themes: Aztecs established an empire in central Mexico between 1300 and the 1500s.
- For South Asian themes: Hindu (follower of Hinduism, a group of beliefs and practices from South Asia), Sanskrit (primary language of Hinduism), raja (king or prince in India).
- For medieval European themes: Crusader (European soldier in the wars in the Middle East, 11th–13th centuries); infantry = soldiers trained to fight on foot.
- For archaeology themes: artifact = an object made by people from past cultures (tools, pottery, jewelry); archaeologist studies ancient peoples through bones, tools, and artifacts.
- Use "legacy" for something from the past, and "descendent" for a person related to someone who lived in the past.
## Checklist
- [ ] Date format consistent (BCE/CE) across all in-game text.
- [ ] Culture-specific titles correct (pharaoh, raja, curator, aristocrat).
- [ ] Material terms correct (papyrus, lapis lazuli, ebony).
- [ ] Military terms correct (legion, infantry, chariot).
- [ ] Sensitivity review done for cultures used as theme.
## Anti-patterns
- Mixing BC/AD and BCE/CE in the same game text.
- Using "artifact" for a modern object; it means an object from past cultures.
- Flattening distinct cultures into one generic "ancient" theme.
> CHECK: Glossary is a term list; it gives no guidance on cultural consultation or representation review.

---
name: real-world-disease-and-society-terms
topic: Disease, society, and economics vocabulary
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Scale disease terms precisely: epidemic = hits large groups at the same time and spreads quickly; pandemic = outbreak spreading across more than one continent.
- Named real diseases in the glossary include Ebola (rare and deadly virus) and SARS (contagious, sometimes fatal respiratory illness with flu-like symptoms). Treat these as sensitive subject matter.
- Distinguish dementia (a group of brain diseases causing gradual decline in thinking and memory) from Alzheimer's disease (a form of dementia that worsens over time and affects memory, thinking, and behavior).
- Use economic terms correctly: economic = relating to a country's resources and wealth; consumer = a person who buys goods and services; inequality = differences in opportunity and treatment based on social, ethnic, racial, or economic qualities.
- Use "Great Depression" for the severe worldwide economic downturn of the late 1920s and 1930s.
- Use "American dream" for the ideal that material prosperity means success — treat it as a contested ideal, not a fact.
- Use "smart home" for a house where all electric devices are monitored or controlled by a computer.
## Checklist
- [ ] Epidemic vs pandemic used at the correct geographic scale.
- [ ] Disease names used only where the design intends real-world reference.
- [ ] Dementia and Alzheimer's not used interchangeably.
- [ ] Economic terms checked against their precise definitions.
- [ ] Sensitivity review for real diseases and social inequality as theme.
## Anti-patterns
- Using "pandemic" for a local outbreak, or "epidemic" for a global one.
- Using real disease names as casual flavor text.
- Treating the American dream as an uncontested positive in narrative.
> CHECK: Glossary defines terms but gives no ethical guidance for using real diseases in games.

---
name: technology-and-making-terms
topic: Technology, prototyping hardware, and craft vocabulary
confidence: consensus
sources: ["Game Logic Level Up, Angie Smibert, ch. Glossary (pp. 153-159)"]
---
## Rules
- Define technology broadly: the tools, methods, and systems used to solve a problem or do work. A paper prototype counts as technology.
- Use 3-D printing for physical components: a machine that makes a physical object from a 3-D model by laying down many thin layers of material.
- Distinguish 3-D (appears solid, measurable in length, width, depth) from holograph (a laser-produced picture that looks three-dimensional).
- Use "electrode" for a conductor through which electricity enters or leaves an object, substance, or region — relevant for touch/conductive game hardware.
- Use "digital" for anything involving computer technology; use "interactive" for a two-way flow of information.
- Use "makeshift" for a temporary substitute or device — acceptable for prototypes, not for shipped components.
- Use "solidify" for making something more solid or stronger, e.g. locking in a mechanic after testing.
## Checklist
- [ ] Prototype method chosen (paper, 3-D printed, digital) and labeled as temporary.
- [ ] 3-D vs holograph used correctly in any marketing copy.
- [ ] Any electronic component's electrode/contact points specified.
- [ ] "Interactive" used only where information flows both ways.
## Anti-patterns
- Calling a static display "interactive" when information flows one way only.
- Shipping makeshift parts as final components.
- Using "3-D" for a laser hologram or vice versa.
> CHECK: Glossary defines hardware terms but gives no tolerances, materials, or printer settings.
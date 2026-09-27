<!-- 1 Mission Control (pp. 1-4) -->
---
name: ux-vs-ui-definitions
topic: UX and UI definitions for games
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 1 (pp. 1-4)"]
---
## Rules
- Treat UX as the umbrella: everything from first contact with the product through the entire experience. UI is a subset focused on visual interaction points (mostly digital) that let interactions happen.
- Do not use "UX" and "UI" interchangeably in team communication; they describe different scopes and different owners. WHY: conflating them causes misrouted feedback ("bad UI" vs "bad flow") and unclear responsibilities.
- Scope UI work to: fonts, icons, interaction design, information hierarchy, flow curation, on-screen feedback. Scope UX work to: the whole player journey, friction balance, learnability, emotional arc.
- Accept that UI and UX can each save or ruin the other; a clean menu with a broken flow still fails, and a great flow with unreadable UI still fails. WHY: players judge the combined result, not the org chart.
- When a game is criticised, classify the complaint as UX (flow, pacing, comprehension) or UI (legibility, layout, input affordance) before assigning a fix.

## Checklist
- [ ] For each feature, name the UX goal (what the player should feel/understand) and the UI goal (what they see and press).
- [ ] Confirm every UI element has a UX reason to exist.
- [ ] Confirm every UX intent has a visible UI affordance.
- [ ] Route feedback to the correct discipline before triage.

## Anti-patterns
- Using "UX/UI" as one job title in planning docs, then expecting one person to own both scopes.
- Treating UI as decoration applied after gameplay is done.
- Assuming a good-looking menu equals a good experience.

---
name: game-ux-friction-balance
topic: Friction design in games vs apps
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 1 (pp. 1-4)"]
---
## Rules
- Do not copy app/web UX goals into games. Apps and streaming services minimise friction; games deliberately include it. WHY: challenge is the product in games, not an obstacle to remove.
- Design UX to help players enjoy overcoming challenges, not to remove the challenges. The fun comes from the friction being surmountable and legible.
- Separate two friction types and handle them differently:
  - Intentional friction: gameplay challenge, difficulty, mastery, tension. Keep and tune it.
  - Unintentional friction: confusing menus, unclear icons, hidden controls, bad navigation. Remove it.
- Never justify annoying menus as "it's a game, friction is fine." WHY: menu friction is not gameplay; it only delays the player from the fun.
- When playtesting, ask whether a slowdown was a challenge the player wanted to beat or a chore they wanted to skip.

## Checklist
- [ ] List every point where the player must stop playing to operate the interface.
- [ ] For each, label it intentional (gameplay) or unintentional (UI/UX debt).
- [ ] Remove or reduce all unintentional friction.
- [ ] Verify intentional friction is readable: the player understands why they failed and what to try next.

## Anti-patterns
- Applying "reduce clicks" dogma to core gameplay loops.
- Applying "it's a game" excuses to settings menus, inventories, and tutorials.
- Adding friction for "immersion" without a gameplay payoff.

---
name: ui-ux-as-specialist-discipline
topic: Why UI/UX needs dedicated roles
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 1 (pp. 1-4)"]
---
## Rules
- Treat UI/UX as a specialist discipline, not a side task for programmers or spare artists. WHY: as games, budgets, and player expectations grew, ad-hoc ownership produced inconsistent, low-usability results.
- Expect UI/UX work to scale with project complexity: bigger systems, more platforms, and larger audiences require dedicated people for flow, hierarchy, and interaction design.
- If you cannot hire specialists, explicitly assign the responsibilities (fonts, icons, interactions, information hierarchy, flow) to named owners with time budgeted. WHY: unassigned work becomes afterthought work.
- Recognise that UX in older games emerged passively from game design; modern games need it designed on purpose.

## Checklist
- [ ] Identify who owns: information hierarchy, flow, iconography, typography, interaction feedback.
- [ ] Budget time for UI/UX tasks in the schedule, not as leftover polish.
- [ ] Review whether UI/UX is being treated as an obligation or a designed feature.

## Anti-patterns
- Assuming "the game feels right" is enough validation without structured UX review.
- Shipping UI as a necessary afterthought.
- Loading UI/UX duties onto generalist roles with no allocated time.

---
name: interface-scope-in-games
topic: What counts as interface in a game
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 1 (pp. 1-4)"]
---
## Rules
- Treat everything the player sees and interprets as part of the experience, even if it is not a HUD element. Rocks, trees, and weapons convey information and affordances just like real-world objects.
- Use in-world elements to carry information and natural affordances where possible, instead of adding overlay UI. WHY: environmental cues reduce UI clutter and keep the player in the game world.
- When deciding "is this UI?", ask whether the element communicates state, options, or affordances to the player. If yes, it belongs in the UX review even if it is diegetic.
- Note that early games show the range: Tennis for Two had no on-screen score (kept on lab notes), while Pong (1973) displayed score on screen. Score visibility is a design decision, not a given.

## Checklist
- [ ] Inventory all information channels: HUD, menus, diegetic objects, audio, animation, lighting.
- [ ] Check that critical state (score, health, objectives) is communicated somewhere the player will notice.
- [ ] Check that environmental cues are consistent and readable, not just decorative.

## Anti-patterns
- Reviewing only the HUD and menus while ignoring in-world signalling.
- Duplicating the same information in overlay UI and environment without a reason.
- Assuming players will infer state that is never communicated.

---
name: ux-foundations-affordances-feedback
topic: Core UX concepts to apply
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 1 (pp. 1-4)"]
---
## Rules
- Apply user-centred design: design for real people with an empathetic eye, not primarily for aesthetics. (Don Norman's framing, cited by the author.)
- Provide affordances: make an object's possible uses clear from its appearance. WHY: players act on what looks actionable.
- Provide feedback: every action must produce a visible reaction, and inaction must also be readable as a state. WHY: without feedback the player cannot tell whether input registered.
- Use iconography for complex or subtle meaning that would take words to express; this is a long-standing pattern from early symbols to modern emojis.
- Treat these as practical checks on every interactive element, not abstract theory.

## Checklist
- [ ] For each interactive element: does it look interactive (affordance)?
- [ ] After each input: is there immediate feedback?
- [ ] When nothing happens: is the "no action" state communicated?
- [ ] Can any label be replaced by a clear icon without losing meaning?

## Anti-patterns
- Designing for visual polish while ignoring whether players can tell what to do.
- Silent inputs with no confirmation.
- Icons whose meaning requires a tooltip to be understood.

> CHECK: The chapter is an introduction and does not give concrete numeric thresholds (timings, sizes, counts). Any numbers in these cards would be invented; verify against later chapters before adding specifics.

<!-- 2 Hunt for the Unicorn (pp. 5-18) -->
---
name: ui-ux-role-taxonomy
topic: UI/UX role definitions and responsibilities
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 2 (pp. 5-18)"]
---
## Rules
- Treat role titles as a guide, not a contract: studios use inconsistent titles for the same work. Read the job description's duties, not its title, before deciding if you qualify.
- Map each role to its primary deliverable so you can staff a team:
  - UX Researcher → personas, user stories, journey maps, usability reports, heuristic evaluations.
  - Interaction Designer → low-fidelity wireframes and prototypes for usability testing.
  - UX Writer / Content Designer → in-game copy, tone, formatting, brand voice.
  - UX Architect → information hierarchy, navigation map, big-picture data analysis.
  - UX Designer → full process generalist (research, personas, navigation, testing, prototyping, wireframes).
  - UX/UI Designer → high-fidelity concepts, pre-viz, animation/icon/typography style, VFX, plus UX research and in-engine implementation.
  - UI Designer → interface design, often dipping into UX.
  - UI Artist / Visual Designer → interface graphics, style, brand integration, cohesive visual language.
  - UI Technical Artist → bridge art↔engineering, tooling, asset optimisation, technical constraints.
  - UI VFX Artist → in-world communication FX (grenade arcs, danger zones) and feedback FX (level-up, loot reveals).
  - UI Scripter/Implementer → takes finished designs into the engine: layout, data structure, logic.
  - UI Programmer/Engineer → responsive, performant UI code across platforms.
  - UX Strategist → UX vision, business/player liaison, team composition, competitive analysis.
  - UI/UX Manager/Director/Head → leadership, culture, process, cross-discipline collaboration.
- In small studios, expect these responsibilities to be absorbed by game designers, directors, or the publisher. Plan for it rather than assuming a specialist exists.
- When a role is missing, the fallback is usually assumptions and personal preference — flag this as a project risk.
- WHY: The industry is young and studios don't follow a template, so title-based assumptions cause mis-hiring and duplicated or dropped work.

## Checklist
- Does the job description list concrete deliverables (wireframes, reports, in-engine work) or only a title?
- Which specialist roles does this team actually have vs. which are absorbed?
- Who owns research, copy, information architecture, and implementation on this project?
- Is there a dedicated UX researcher, or is research being done by designers/production?

## Anti-patterns
- Assuming you don't qualify for a role because of its title.
- Assuming a title guarantees a specific skill set (e.g. a UI Artist who does all UX design).
- Treating "UI" and "UX" as interchangeable when staffing.
- Letting design decisions default to personal preference because no researcher is on the team.

---
name: ui-ux-common-traits
topic: Shared competencies across all UI/UX roles
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 2 (pp. 5-18)"]
---
## Rules
- Hire and evaluate UI/UX candidates on these shared traits regardless of title:
  - Communicates clearly and fluently.
  - Prioritises user experience over user interface.
  - Keeps the player as the primary focus.
  - Uses brevity, consistency, and familiarity in design.
  - Knows common traits, trends, and functions of the discipline.
  - Prioritises accessibility.
  - Treats data analytics as a driving force, not an obstacle.
- WHY: Titles and responsibilities vary wildly across studios, so these traits are the only stable signal of a good fit.
- Ignore gatekeeping arguments about "what real UX is" — they don't affect player outcomes.
- WHY: The overlap and dilution of roles is real but not a priority problem; arguing about it wastes time.

## Checklist
- Can the candidate explain their work to non-specialists?
- Do they default to UX reasoning before visual polish?
- Do they cite player data or research when defending a decision?
- Do they treat accessibility as a baseline requirement?

## Anti-patterns
- Rejecting candidates over title semantics.
- Treating UI and UX as the same discipline.
- Letting social-media gatekeeping shape hiring criteria.

---
name: generalist-vs-specialist
topic: Career path — generalist vs specialist
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 2 (pp. 5-18)"]
---
## Rules
- Early career: generalise. Take on as many responsibilities as possible to build breadth.
- Later career: specialise in the areas you enjoy and are strongest at.
- The industry needs both generalists (big-picture view) and specialists (deep detail).
- Aim to be both over time: breadth first, depth later.
- WHY: You can't know which specialism suits you until you've tried the full pipeline.
- Expect to spend significant time explaining your role and justifying your work regardless of specialism.
- WHY: Role ambiguity is structural in this industry, not a personal failing.

## Checklist
- Have you worked across at least one full production cycle?
- Can you name the parts of the pipeline you enjoy most?
- Do you have a specialism you can defend as expert-level?

## Anti-patterns
- Trying to be an expert from day one.
- Specialising before you understand the adjacent roles.
- Treating title progression as the only measure of career growth.

---
name: seniority-and-feedback
topic: Seniority levels and professional maturity
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 2 (pp. 5-18)"]
---
## Rules
- Judge seniority by relationship with feedback, not by title. How someone gives and receives critique is the truest signal of maturity.
- Demonstrate self-critique openly so others see you can handle honesty.
- WHY: Visible self-critique signals strength and gives the team permission to be honest.
- Never argue with constructive feedback; treat it as a chance to show willingness to improve.
- Seniority bands and typical expectations:
  - Intern: short engagement (a few months), low-risk meaningful tasks, assigned senior coach.
  - Junior/Associate: isolated, educational tasks where mistakes don't harm the product.
  - Mid-level: 2–4 years or one full production cycle; owns more features, needs less supervision, still benefits from mentorship.
  - Senior: self-sufficient, fully owns features, coordinates with management, mentors juniors.
  - Lead: people management, scheduling, welfare, or purely technical; advocates for the discipline.
  - Principal: deep craft expert, runs features independently, raises the team's technical bar.
  - Director/Head: direction, logistics, management, outsourcing, HR; less hands-on production.
- Distinguish Lead vs Principal: Lead focuses on the team, Principal focuses on the discipline's practical capability.
- WHY: Promoting a great craftsperson into management can remove your best producer without producing a good manager.

## Checklist
- Can the person articulate their own weaknesses unprompted?
- Do they accept critique without defensiveness?
- Is the promotion to lead driven by people skills or just craft skill?
- Does the team have a mix of seniority levels (culture and fresh perspectives come from juniors)?

## Anti-patterns
- Expecting a promotion without demonstrating value.
- Gossip, lying, or untrustworthy behaviour.
- Entitlement instead of proactivity.
- Failing to advocate for yourself.
- Not being a positive team player.
- Promoting on craft skill alone into people management.
- Treating title as the only metric of progression (leads to stagnation or job-hopping).

---
name: internship-and-junior-conditions
topic: Intern and junior role expectations
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 2 (pp. 5-18)"]
---
## Rules
- A good internship: paid (modestly), treated as associate/junior, meaningful low-risk work, assigned senior coach, real career foundation.
- A bad internship: unpaid grunt work with no coaching or education.
- WHY: Internships are the main path to the professional experience employers demand but rarely provide.
- Junior/associate tasks should be isolated and educational so mistakes don't damage the product.
- WHY: This lets juniors learn safely while seniors retain responsibility for shipped quality.
- Expect juniors to need supervision overhead that reduces senior productivity — budget for it.
- WHY: Ignoring this cost is why studios over-hire seniors and starve the junior pipeline.
- Juniors bring new ideas and push for more inclusive, accessible design; treat that as an asset.

## Checklist
- Is the intern paid and assigned a named senior coach?
- Are junior tasks scoped so failure is contained?
- Is senior time explicitly allocated for mentoring?
- Does the team have at least one junior to keep culture and perspectives fresh?

## Anti-patterns
- Using interns as free labour for unwanted work.
- Hiring only seniors because they deliver faster — this kills the future talent pipeline.
- Giving juniors high-risk, product-critical tasks without supervision.

<!-- 3 Basic Training (pp. 19-27) -->
---
name: education-path-selection
topic: career education paths for game UX/UI
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 3 (pp. 19-27)"]
---
## Rules
- Treat a degree/diploma as evidence you can finish something, not as proof of employability. Employers assess demonstrated skill, character, reliability and teachability. WHY: hiring pools are large after 2022-2024 layoffs, so credentials alone do not differentiate candidates.
- Pick an education route by answering three questions first: (1) do you want structure or full control, (2) can you absorb the cost or debt, (3) does the route produce a portfolio you can show. WHY: each route trades cost, time and demonstrable output differently.
- If you plan to work abroad, verify visa rules before choosing a course. For the USA, expect to need: a bachelor's degree or higher in a relevant field (check it counts as STEM), a specialty occupation, and an employer sponsor. WHY: a degree may be a legal requirement, not just a hiring preference.
- For any paid course, verify accreditation, provider reputation, course transparency, professional endorsements, student testimonials and industry relevance before paying. WHY: some certificates carry no recognised industry value.
- Budget for hardware/software if the course requires your own kit — this is an upfront cost on top of tuition. WHY: it is often omitted from advertised pricing.
- Build soft skills (communication, teamwork, accountability, pitching, deadlines) deliberately on every route. WHY: they map directly to milestone-driven game production.
- Network regardless of route: alumni, recruiters, peers, events, online communities, mentorship programmes. WHY: referrals open doors but only get you the interview, not the job.
- Keep learning daily outside formal study: new software, side projects, game jams. WHY: it is the main way to gain a competitive edge and it is free.
## Checklist
- Compare at least 3 routes: university degree, independent/bootcamp course, self-directed.
- Attend open days (near and far); talk to both lecturers and current students.
- Inspect the range and quality of student work and where alumni now work.
- Ask which competitions students won or were shortlisted for.
- Check whether staff have current or previous industry experience.
- Confirm the syllabus is up to date with current tools and processes.
- For self-directed study: write your own syllabus and schedule before starting.
- For internships: apply early; treat them as highly competitive.
## Anti-patterns
- Assuming a prestigious institution or course guarantees a job.
- Paying more and assuming better quality — price and quality are not correlated.
- Skipping "boring" fundamentals to jump to advanced topics; it causes later struggles and drop-off.
- Self-teaching with no structure, risking inefficient, incorrect or outdated practice.
- Doing an online/self-directed route and never talking to anyone, so soft skills stagnate.
- Choosing a course without checking whether its certificate is recognised by employers.

---
name: portfolio-over-credentials
topic: demonstrating skill to employers
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 3 (pp. 19-27)"]
---
## Rules
- Make the portfolio the primary artefact of any education route; document what you learned in detail, including self-taught home projects. WHY: self-education is the hardest route to "show", but the most impressive when shown well.
- Expect a performance test in hiring (e.g. find and report bugs in a build) and be assessed on report quality. WHY: employers test the actual skill, not the certificate.
- Show relevant work samples: personal projects, freelance work, coursework, websites. WHY: they demonstrate capability where a diploma only shows attendance.
- Speak about your work ethic and passion in interview; pair it with evidence. WHY: character and teachability are explicitly assessed.
- Treat a referral as an interview opportunity only — you are still hired on merit. WHY: vouching carries limited weight.
## Checklist
- Portfolio contains at least one project per claimed skill.
- Each project states what you did, what you learned, and the outcome.
- Practise a bug-reporting/QA-style performance test before interviewing.
- Prepare to explain your process, not just show final screens.
## Anti-patterns
- Presenting a certificate as the headline credential with no work behind it.
- Assuming a contact inside a studio removes the need to prove merit.
- Leaving self-taught work out of the portfolio because it was "just at home".

---
name: ux-observation-as-free-training
topic: building UX/UI judgement
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 3 (pp. 19-27)"]
---
## Rules
- Study the UX and UI of every game and app you touch; it is free, always-available training. WHY: the author calls it the best free education available and it is everywhere.
- Set aside recurring time for extra creative objectives and new software, but protect work-life balance. WHY: sustained skill growth needs consistency, not crunch.
- Start with small, achievable projects rather than large ones. WHY: finishing small work builds portfolio evidence and momentum.
## Checklist
- Keep a running log of UX/UI observations from games you play.
- Schedule weekly time for a side project or new tool.
- Scope each side project so it can be finished.
## Anti-patterns
- Only studying UX/UI inside coursework and never in daily play.
- Taking on an oversized personal project and abandoning it.
- Using "keep learning" as justification for unhealthy working hours.

> CHECK: The chapter is career-education advice, not game-development technique. If your knowledge base expects engine/implementation rules, this chapter yields little of that — confirm the intended scope before adding more cards.

<!-- 4 UX: Know Thy User (pp. 28-55) -->
---
name: ux-vs-ui-and-why-ux-matters
topic: UX fundamentals
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- Treat UI as the visual layer (layout, colour, typography, icons) and UX as function, emotion and the reason those visuals exist. Design both, but justify visual choices by user needs.
- In games UX has a dual mandate: remove friction for routine tasks (menus, settings, store) AND deliberately add friction where the game design wants tension or challenge. Never strip friction that is the core of the design.
- Judge a design against these qualities in order: Useful, Usable, Discoverable, Credible, Desirable, Accessible, Valuable. A game that fails "useful" or "usable" gets refunded or uninstalled immediately.
- Plan accessibility features early. Cost and effort rise sharply when they are retrofitted; treat them as a design input, not a polish task.
- Assume players will not look for a good experience — they should feel it subconsciously. If a player has to hunt for a function, the design failed.
- Do not use "I like it this way" as a design argument. Personal taste may drive style, tone and story, but not usability decisions.
## Checklist
- For each screen, name the user goal and the friction level the design intends.
- Confirm the price, currency balance and checkout button are all findable in one glance in any store flow.
- Confirm accessibility options exist for every feedback channel you rely on (colour, audio, haptics).
- Confirm the first 5 minutes of play match the promise of the trailer and store page.
## Anti-patterns
- Assuming a strong franchise or fun core loop excuses a bad interface; it only delays the cost.
- Treating accessibility as "making the game easier" — it is inclusion, not difficulty reduction.
- Copying a successful competitor's UX without checking whether its audience matches yours (survivorship bias).
> CHECK: OCR shows "demand response to audience feedback" in the Among Us sentence — likely a mangled phrase; verify original wording before citing.

---
name: ux-psychology-cognitive-biases
topic: UX psychology
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- Hick's Law: more choices = longer decisions. Stagger character customisation into stages or cap it at a few critical choices. For very large option sets, add favourites, dynamic sorting, search and "new item" markers.
- Fitts's Law: target acquisition time depends on distance and size. Make frequent or critical buttons large and near the player's resting input position; use padding/negative space to separate them. Invert this deliberately for QTEs where distance is the intended challenge.
- Miller's Law: working memory holds roughly 7 ± 2 items. Keep simultaneous HUD elements and required facts within that budget, or offload them to persistent on-screen indicators.
- Doherty Threshold: keep system response under 400 ms. If a wait is unavoidable (level load, purchase), show feedback or let the player do something small during the wait.
- Progressive disclosure: reveal mechanics and information in layers as the player interacts, building on what they already learned (skill trees, fog of war, new weapons).
- Attentional spotlight: players see only what they attend to. Use one clear visual cue (highlight, animation) per moment; never direct attention to two competing feedback sources at once.
- Priming: place visual or verbal cues before an event (ammo and health pickups before an arena) to set expectations.
- Von Restorff: make the one element that matters visually distinct — the player's own name, the primary action button, rare loot.
- Anchoring: the first minutes set the reference point for the whole game. Make the opening experience representative of the intended quality and tone.
- Nudging: guide behaviour with environmental or UI cues (warnings, team-composition messages) rather than hard blocks.
- Framing: presentation of information affects decisions more than the data. Use it to reduce confusion, not to deceive.
- Tesler's Law: complexity is conserved. You can move it between systems and UI, but removing it entirely removes the challenge and the fun.
- Loss aversion: players feel losses more than gains. Provide safety nets (checkpoint restarts, companion resupply) so high-stakes play does not stall.
- Sunk cost: be willing to cut a feature you have invested in when it no longer delivers. Give players an escape from a dead run.
- Reactance: forced restrictions create negative emotion. Explain or justify them diegetically; prefer visible in-world barriers over invisible walls, and never yank camera control away.
- IKEA effect / endowment effect: customisation and ownership raise perceived value. Let players name and personalise items, and introduce changes to familiar systems gradually.
- Goal-gradient: visible progress toward a goal increases motivation. Use progress bars, quest lists, objective HUDs.
- Peak-end rule: players remember the most intense moment and the ending. Engineer both.
- Serial position effect: first and last items in a list are remembered best — place important options there.
- Postel's Law: be strict in what the system outputs, forgiving in what it accepts. Recover from wrong input and tell the player how to fix it.
- Jakob's Law: users expect genre conventions. Match established patterns unless the status quo is genuinely inadequate.
- Default bias: players take the default. Make alternatives discoverable and clearly beneficial.
- Skeuomorphism: real-world metaphors (cog = settings) speed recognition, but overuse clutters and dates the UI.
- Aesthetic-usability effect: attractive UI hides usability flaws — do not let it mask real problems in testing.
- Cognitive dissonance: marketing and mechanics must agree. A "fast-paced action" promise with slow mechanics reads as broken.
- Affect heuristic: mood distorts judgement. Run a well-being check before interviews or playtests and discount data from upset participants.
- Confirmation bias: test assumptions with real players instead of assuming you know what they want.
## Checklist
- Count simultaneous HUD elements and required remembered facts; keep within 7 ± 2.
- Measure input-to-feedback latency; flag anything over 400 ms.
- Check every forced restriction has an in-world justification.
- Check every important list has its key items first or last.
## Anti-patterns
- Invisible walls as the default boundary solution.
- Forcing camera movement to show the player something.
- Adding options without sorting, search or favourites.
- Designing from personal preference and calling it intuition.

---
name: ux-psychology-motivation-and-time
topic: Motivation, reward and time
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- Scarcity: limited-time events, rare items and constrained resources raise perceived value and engagement. Use rarity tiers and limited ammo/lives deliberately.
- Variable reward: unpredictable rewards sustain long-session play. Use them in high-time-investment games and for returning-player bonuses.
- Curiosity gap: give just enough story or mechanic information to make the player want the next piece. Core technique for narrative and mystery games.
- Investment loops: chain progress → reward → new capability → repeat. The loop must be both challenging and rewarding, and the underlying activity must be fun.
- Temptation bundling: pair a low-enjoyment task (grinding, levelling) with a high-enjoyment one (exploration, combat) so the former gets done.
- Decision fatigue: cap the number and complexity of decisions per session segment; too many choices leads to apathy or irrational picks.
- Parkinson's Law: work expands to fill available time. Set explicit deadlines for UX tasks or they will be over-engineered.
- Weber-Fechner: perception of change is relative. Small increments are noticed on small values but not on large ones — scale feedback magnitude accordingly (pistol = slight rumble, bazooka = heavy rattle).
- Law of the instrument: do not default to the same tool or pattern every project. Also exploit it in-game — if the player has a gun, expect them to shoot everything, so design interactions around that.
- Delighters: add small unexpected extras (animations, easter eggs, petting animals) to raise memorability. They are optional polish, not core function.
## Checklist
- Verify each reward loop has a visible progress indicator.
- Verify low-fun tasks are bundled with a high-fun activity.
- Verify feedback intensity scales with the magnitude of the event.
- Set a timebox for each UX task before starting.
## Anti-patterns
- Grinding with no bundling or reward variety.
- Front-loading dozens of decisions in onboarding.
- Open-ended polish tasks with no deadline.

---
name: memory-learning-and-feedback
topic: Memory, learning and feedback
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- Recognition beats recall: show the option rather than requiring the player to remember it. Reuse familiar icons and control conventions so experienced players can operate a new game immediately.
- Heuristic learning: design so repeated actions become intuitive, removing the need for repeated tutorials and reminders.
- Negativity bias: negative experiences are remembered more strongly. Fix frustrating mechanics early; they dominate the player's overall memory of the game.
- Sensory appeal: deliver feedback through at least two channels (visual + audio + haptic). Never rely on colour change alone.
- Always provide toggles or intensity sliders for haptics and other stimulation. Vibration can cause physical pain for players with RSI or carpal tunnel and makes the game unplayable if it cannot be disabled.
- Feedback must be timely, relevant and unambiguous — it tells the player what happened and what to do next.
## Checklist
- Check every critical state change has multi-channel feedback.
- Check every stimulation channel has a settings toggle or intensity control.
- Check no tutorial repeats information the player has already internalised.
## Anti-patterns
- Colour-only feedback for state changes.
- Non-disableable vibration or screen shake.
- Leaving known frustrating mechanics in place because they are "part of the design".

---
name: gestalt-principles-for-game-ui
topic: Visual perception
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- Proximity: group related elements tightly and separate unrelated ones with space. Use it to distinguish menu options, controls and stats.
- Similarity: give elements with the same function the same colour, shape and style (e.g. all combat abilities one shape/colour, all magic another).
- Common region: enclose related elements in a shared panel, overlay, line or background to bind them.
- Continuity: align elements along a shared axis to signal relationship and ease navigation.
- Closure: the brain completes incomplete shapes. Use partial shapes and faded list edges to imply more content or motion.
- Figure-ground: contrast critical elements against their background so they are noticed immediately.
- Uniform connectedness: visually connect elements (same button style, stacked menus) so they read as one group.
- Common fate: elements that animate or change together are perceived as related — use synchronised motion to show grouping.
- Prägnanz: the brain simplifies complex images. Design the simplest form that still communicates the function.
## Checklist
- Check each functional group is separated by space, boundary or alignment.
- Check critical elements have sufficient contrast against their background.
- Check grouped elements share colour, shape and animation timing.
## Anti-patterns
- Mixing styles within one functional group of icons.
- Relying on subtle contrast for critical information.
- Overloading a panel with unrelated elements.

---
name: core-ux-principles
topic: UX principles
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 4 (pp. 28-55)"]
---
## Rules
- User-centricity: put the target user's needs first, but keep room for artistic vision and innovation. Games intentionally include friction; apps minimise it. Do not design purely from market research.
- Consistency: keep aesthetics, interaction and functionality uniform across the whole game so players build a reliable heuristic.
- Feedback: give clear, immediate information about actions and inactions, preferably across multiple channels.
- Equitable use: design so people with diverse abilities can play without special adaptation. Cover temporary and situational impairments as well as permanent disabilities.
- Affordance: make objects look like what they do (handles pull, big red buttons press). Lean on real-world understanding.
- Hierarchy: prioritise information with colour, size and placement so the player knows what matters and what happens next.
- Conceptual model: give players a mental model of how the world, UI, mechanics and controls fit together, via tutorials, documentation or consistent system behaviour.
- Error prevention: reduce the chance of errors with concise instructions, forgiving input and intuitive controls.
- Tolerance for error: make errors recoverable — multiple paths to a task, undo, buy-back of sold items.
- Low physical effort: use ergonomic layouts and streamlined menus. Avoid button holds and repeated rapid taps that cause discomfort or exclude players with physical limitations.
- Constraints: treat limited buttons, memory or time as design parameters that force focus, not as obstacles.
- K.I.S.S.: keep designs simple. Simple is not dull. Ask "why is this so complicated?" and "am I doing this for me?"
## Checklist
- Check every action has immediate, multi-channel feedback.
- Check every destructive or irreversible action has an undo or recovery path.
- Check no required action needs a sustained hold or rapid repeated tap.
- Check the control scheme fits the target input device's button count.
## Anti-patterns
- Designing for yourself rather than the target player.
- Inconsistent interaction patterns between screens.
- Irreversible actions with no confirmation or recovery.
- Rube Goldberg flows where a simple one would do.

<!-- 5 UX: Not UI (pp. 56-76) -->
---
name: ux-design-stages
topic: UX process
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Run UX in five stages: Research & Planning → Concept & Ideation → Design & Production → Testing & Iteration → Launch & Post-launch.
- Research stage defines audience identity/needs plus game objectives, mechanics, and competition.
- Ideation stage produces multiple proposals, then refines to the most practical and innovative; discard the rest.
- Production stage locks final features and pairs UX with UI and programming.
- Test with users at every production stage, not only at the end.
- Post-launch, treat the live player base as an expanded test pool for data analysis and fixes.
- Expect studio process to differ: team size, values, and resources vary; some studios have no UX role at all.
- WHY: each stage de-risks the next; skipping early research or late testing pushes cost into production.

## Checklist
- [ ] Audience and objectives written down before ideation.
- [ ] At least 2-3 competing design proposals generated.
- [ ] UX paired with UI/programming during production.
- [ ] Usability test scheduled per production milestone.
- [ ] Post-launch feedback loop defined (metrics + updates).

## Anti-patterns
- Treating UX as a single handoff instead of a loop.
- Assuming every studio runs the same pipeline.
- Deferring all user contact to launch.

---
name: ux-research-methods
topic: UX research
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Align research focus with project values first; build a roadmap from that alignment.
- Question wording: "what" for features, "how" for processes, "why" for motivations.
- One idea per question; keep language concise to get usable data.
- Pilot-test every question, then cut or refine the weak ones.
- Prioritise questions by project impact and ease of implementation.
- Actively watch for bias that skews results.
- Competitive analysis: study similar games for best practices, trends, strengths, weaknesses, audience expectations (Jakob's Law applies).
- Motivational model: pick which motivations to target and combine — action, achievement, completion, immersion, creativity, mastery, fantasy, story, power, social interaction.
- Player experience goals must use the same vocabulary as motivations and be measurable while leaving room to iterate.
- Goal template: "Players will feel like X when they do Y within constraint Z" — name the player, the feeling, and the mechanic.
- User interviews (in person, online, or phone) inform feature scope, structure, and UX improvements.
- Empathy map: four quadrants — what users see, hear, feel, do.
- Personas: build several, including extremes of the target group; each is research-based with goals, needs, behaviours, preferences.
- Persona creation steps: research → find patterns → define demographics/goals/motivations/pain points → give name and picture → test against real users → keep iterating.
- Journey mapping: chart awareness → final satisfaction; use it to find pain points, technical constraints, and opportunities.
- Journey maps require near-complete game design and stakeholder input, or they misrepresent the vision.
- WHY: research grounded in real users replaces assumptions and personal preference with evidence.

## Checklist
- [ ] Research focus tied to project values.
- [ ] Questions piloted and prioritised.
- [ ] Competitive analysis done on 3+ comparable titles.
- [ ] Motivations chosen and combined deliberately.
- [ ] Experience goals measurable and phrased in motivation language.
- [ ] 3+ personas including edge cases.
- [ ] Journey map validated with stakeholders.

## Anti-patterns
- Leading or double-barrelled questions.
- One persona representing the whole audience.
- Building a journey map before the game design is stable.
- Copying competitor features without checking audience expectations.

---
name: accessible-design-barriers
topic: accessibility
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Definitions to use: difficulty is relative; capability is the ability to overcome challenges; a barrier blocks that; disability is the mismatch between capability and barrier; accessibility is the mechanism that removes the mismatch.
- Never equate accessibility with lowering difficulty — the challenge is the game.
- Three barrier responses: (1) give tools to pass through — remapping, screen readers, aim assist, colour-blind support, text size, subtitles, audio cues; (2) provide a route around — branching paths, alternate mechanics (hold or single press instead of repeated presses), different playstyles and modes; (3) allow skipping — for non-core content, QTEs, or repeated failure.
- Precedent: GTA V lets players skip a mission after three failures; taxi rides can be skipped.
- Allow mid-game difficulty changes and automatic mechanic simplification.
- Subtitles should be on by default.
- Offer audio/text options before the first cutscene, not after.
- Let players adjust graphics settings before gameplay starts.
- Language: avoid "disabled" in option labels; name difficulty levels creatively (in-IP naming, e.g. Star Wars Jedi: Fallen Order) or split difficulty into categories (e.g. enemies, resources) as in The Last of Us Part II.
- Market reach argument: roughly 20-45% of the gaming population has a disability; the global player base approaches 3 billion by 2029.
- Publish accessibility features before release so players can judge whether they can play.
- WHY: barriers the player cannot control are not gameplay; removing them widens audience and preserves the intended challenge.

## Checklist
- [ ] Accessibility discussed at concept stage, not end of production.
- [ ] Remapping, subtitles, text scaling, colour-blind options present.
- [ ] At least one alternative path or mechanic for hard barriers.
- [ ] Skip option for non-core or repeatedly failed segments.
- [ ] Difficulty labels reviewed for non-judgemental wording.
- [ ] Accessibility feature list published pre-launch.

## Anti-patterns
- Tagging accessibility on at the end of production — leads to harder implementation, bad compromises, dropped features.
- Labelling options "disabled" or "easy/normal" without thought.
- Assuming accessibility features are only for other people.

---
name: information-architecture-and-user-flow
topic: information architecture
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- IA = logical, intuitive structure matching the user's mental model: clear hierarchy, consistent labels, grouped similar elements.
- Order content by importance and make essential elements more prominent — improves both speed of comprehension and aesthetics.
- User flow diagrams map the path a player takes to complete a task (menu navigation or a specific interaction).
- Use flow diagrams to decide when information appears and to minimise the number of steps to a goal.
- Flow diagrams double as planning artefacts for features and technical requirements.
- WHY: structure that matches expectations reduces search time and errors; flows expose missing steps before code exists.

## Checklist
- [ ] Hierarchy defined and reviewed against player expectations.
- [ ] Labels consistent across screens.
- [ ] Similar items grouped.
- [ ] Flow diagram exists for every core task.
- [ ] Step count per task reviewed for reduction.

## Anti-patterns
- Flat menus with everything at equal prominence.
- Designing screens without mapping the path into and out of them.
- Inconsistent naming for the same concept across screens.

---
name: interaction-design-rules
topic: interaction design
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Consistency and clarity: write an interaction guide defining each interaction type and where it is appropriate; keep it updated for team reference.
- Avoid making players relearn how to interact with similar things.
- K.I.S.S.: cut jargon; assume the player has never seen anything like this — nobody has played your game yet.
- Make interactions obvious; only hide things deliberately as easter eggs.
- If an interaction depends on a direction, indicate it visually.
- Conform to genre conventions where they exist (Jakob's Law); note familiar interactions in competitive analysis.
- Rely on recognition: give interactions affordance via familiar shapes and objects.
- Match tone to the game — neither patronising nor overly complex; keep tone consistent to avoid jarring shifts.
- Feedback is mandatory, including micro-interactions: colour change, sound, movement, vibration, effects.
- Every interaction should teach; players gradually learn, become independent, then embed in the game's ecosystem.
- WHY: consistent, obvious, feedback-rich interactions are the difference between frustrating and engaging.

## Checklist
- [ ] Interaction guide written and shared.
- [ ] Every interactive element has a visible affordance.
- [ ] Every input produces feedback within a frame or two.
- [ ] Directional interactions signposted.
- [ ] Tone reviewed against game's fiction.

## Anti-patterns
- Hiding interactions for no reason.
- Silent inputs with no micro-feedback.
- Mixing formal and jokey tone across the same UI.
- Reusing a different interaction pattern for the same action in different screens.

---
name: ux-writing
topic: UX writing
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Brevity: concise, on-target sentences; speak like a human; keep system information plain even when flavour is added elsewhere.
- Example: replace a long flavoured "controller disconnected" message with "Controller Disconnected: Please reconnect your controller."
- Never blame the player; tell them how to fix the mistake.
- Match voice to game tone: formal for serious games, light for playful ones.
- Avoid double negatives — rewrite "not insignificant" as "can significantly impact".
- Be specific in callouts: "Preview Item" or "Play Video" beats "More info".
- Use themed labels sparingly ("Set Sail" instead of "Start Game") — theming every option causes confusion.
- Use digits, not spelled-out numbers: "XP Level 42", "42 DMG".
- Prefer active voice: Subject + Verb + Object. Rewrite "This outfit can be customised by you" as "You can customise this outfit."
- Front-load the message: put the consequence first, e.g. "Returning to the main menu, any unsaved data will be lost. Continue?"
- Choose prepositions by meaning: "sync across platforms", not "to".
- Punctuation: no full stops in headers, buttons, labels, hints, incomplete sentences, bullet points, or single-line body text; use them in multi-sentence body text. Exclamation marks are common in games; question marks for questions and confirmations.
- WHY: copy is the primary channel for teaching mechanics and delivering feedback; clarity beats flavour when the two conflict.

## Checklist
- [ ] Every error message states the fix, not the fault.
- [ ] No double negatives in UI strings.
- [ ] Numbers written as digits.
- [ ] Active voice used throughout.
- [ ] First words carry the key information.
- [ ] Punctuation rules applied per element type.

## Anti-patterns
- Blaming or scolding copy.
- Themed labels on every menu item.
- Vague callouts like "More info".
- Spelling out large numbers in stat displays.

---
name: wireframes-and-prototypes
topic: prototyping
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- A wireframe shows organisation and placement of information and interactions with no colour, imagery, or typography — a blueprint for designers, artists, and engineers.
- Wireframes are the first stage of testing assumptions and getting stakeholder approval, and are reused across the design process.
- Low-fidelity wireframes: rough sketches, no artwork, fast to make; communicate the big idea, content requirements, and basic layout.
- High-fidelity wireframes: detailed and polished, use real content data and specific interface design patterns.
- If you adopt only one technique from this chapter, make it wireframes — you need a plan before you start.
- Prototypes (interactive or not) are tangible representations of final functionality and feel, and exist primarily to gather feedback.
- Test early with a digital prototype to cut wasteful iteration, given high production cost.
- Match fidelity to audience: designers read a paper sketch; stakeholders may need higher fidelity or a prototype to grasp the idea.
- WHY: fidelity is a communication budget — spend it where the viewer's imagination runs out.

## Checklist
- [ ] Wireframe exists for every screen before art.
- [ ] Fidelity chosen per audience (team vs stakeholder).
- [ ] Prototype built for any interaction whose feel is in question.
- [ ] Feedback captured from prototype sessions.

## Anti-patterns
- Presenting grey low-fidelity wireframes to stakeholders who cannot infer the intent.
- Skipping wireframes and going straight to polished UI.
- Building a prototype with no defined question to answer.

---
name: onboarding-and-ftue
topic: onboarding
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- The first five minutes are critical; FTUE covers those minutes and extends into initial gameplay.
- Onboarding is not only for new players — re-onboard whenever a new feature is introduced later.
- Order of early screens: accessibility options (e.g. text-to-speech for UI text) → preference settings → game start and tutorials.
- Never gate subtitles or graphics settings behind the first cutscene or first gameplay.
- Avoid forcing players to parrot called-out moves or read large blocks of text with multiple button prompts.
- Make tutorials fun and contextual; narrative framing makes lessons stick (e.g. Helldivers 2's in-fiction basic training).
- Teach through action at the moment of need: a single call to action during a dramatic beat (e.g. Spider-Man's mid-air "press to swing").
- Be selective: do not present all available options at once — overwhelming players is a failure mode.
- WHY: the opening shapes lasting opinion; friction before play damages immersion and comprehension.

## Checklist
- [ ] Accessibility and settings available before the first cutscene.
- [ ] Subtitles on by default.
- [ ] Tutorial teaches one idea at a time, in context.
- [ ] No long text blocks with multiple button prompts.
- [ ] Re-onboarding planned for late-game features.

## Anti-patterns
- Tiresome tutorials that force repeated inputs.
- Dumping every option on the player at start.
- Locking settings until after the opening sequence.

---
name: usability-testing-and-surveys
topic: usability testing
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Recruit unbiased testers who fall within the target persona range; match content rating and genre interest to the test group.
- GIGO: the tested build must contain all essential elements for the design intent. Testing whether exploding barrels feel satisfying requires smoke, fire, and sound; without them the data is worthless.
- The build need not be final quality, only complete enough to answer the question.
- Test throughout development, not once.
- Testers are not a focus group defining the game; they help improve yours. Ask about their feelings, needs, and understanding, not how the game should work.
- Survey framework — four question groups:
  - Frustration: most frustrating moment, most confusing aspect, most challenging part.
  - Favourite: favourite moment, most enjoyable/memorable aspect, and why.
  - Wanted: what they could not accomplish, what they wished they could do, and why.
  - Magic wand: what would you zap away, change, or add?
  - Doing: what were you doing, what objectives, what actions; what did you think you were meant to do at the time.
  - Describe: how would you describe the game to friends/family; overall impression.
- Confirm goals were understood even if not completed — comprehension matters more than completion.
- Do not report only positives; ignoring wants and frustrations hides severe issues. Missing feedback matters as much as received feedback.
- Contextualise results: one player struggling with a feature does not justify removing it — something else may have blocked understanding.
- WHY: structured question groups surface both confirmation and blind spots without leading the tester.

## Checklist
- [ ] Testers screened against personas and content rating.
- [ ] Build contains all elements needed for the test question.
- [ ] Survey covers frustration, favourite, wanted, magic wand, doing, describe.
- [ ] Follow-up "why" asked for every answer.
- [ ] Negative and missing feedback reviewed, not just wins.

## Anti-patterns
- Testing a violent game on children or a sports game on non-fans.
- Testing a feel-dependent feature without its audio/visual ingredients.
- Treating playtesters as designers.
- Survivorship/confirmation bias — reporting only positives.
- Reacting to a single complaint with a large redesign.

---
name: addressing-ux-issues
topic: UX iteration
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Systematic fix order: (1) identify and understand the root cause — fall in love with the problem; (2) analyse player data for behaviour, interactions, preferences; (3) workshop potential solutions; (4) study same-genre games for best practice; (5) gather cross-discipline perspectives.
- Prefer small, manageable fixes over one drastic change — fewer variables make impact verification easier.
- New problems introduced at this stage can overshadow the original issue.
- Re-test under the same conditions as the previous test to see whether the outcome changed.
- Monitor continuously: player behaviour, engagement and retention metrics, ongoing usability tests.
- WHY: small verified changes compound; large unverified changes hide their own effects.

## Checklist
- [ ] Root cause stated before any solution.
- [ ] Player data reviewed.
- [ ] Solutions workshopped with more than one discipline.
- [ ] Change size kept small.
- [ ] Re-test repeats prior conditions.
- [ ] Engagement/retention tracked after the change.

## Anti-patterns
- Jumping to a fix without a root cause.
- One large redesign in response to feedback.
- Re-testing under different conditions and comparing results.
- Iterating without testing.

---
name: effective-game-ux-principles
topic: UX principles
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 5 (pp. 56-76)"]
---
## Rules
- Predictable functionality improves usability and reduces errors — players should not keep relearning how things work.
- Difficulty is not linear; balance realism against gameplay.
- Do not overdo tutorials; the first five minutes are critical.
- Recognise micro-interactions; narrative feedback is more meaningful than raw system feedback.
- Accessibility is inclusive; do not silo UX decisions within the team.
- Never overwhelm players with too much information or too many options.
- Do not iterate without testing; do not redesign for its own sake.
- Only change things when they are broken or players ask — and only with clear goals.
- Keep changes small to avoid shocking players.
- Games need friction: a game with no friction is effectively a screensaver (Jordan DeVries). Friction should come from the intended challenge, not from the interface.
- You are not the user: collect feedback, research, and validate what players actually want to do.
- UX is adaptation, not an exact science; tastes shift with age and generation, so reassess approach per project.
- Game design is king and often overrides logical UX findings; stakeholders may not follow recommendations.
- WHY: games are entertainment and escapism, not a service transaction — the goal is finding the fun, not removing all friction.

## Checklist
- [ ] Friction audited: is each friction point intended challenge or accidental?
- [ ] No change made without a stated goal.
- [ ] UX decisions shared outside the UX team.
- [ ] Option count per screen reviewed for overload.
- [ ] Assumptions about player wants validated with data.

## Anti-patterns
- Removing all friction and flattening the experience.
- Redesigning working systems for novelty.
- Siloing UX decisions inside the UX team.
- Assuming your own preferences represent the audience.
- Large changes without a clear goal.

<!-- 6 UI: "Make it Pretty" (pp. 77-95) -->
---
name: ui-form-vs-function
topic: UI aesthetics vs usability
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Treat UI as a blend of emotion, design, interaction, brand and art — not a paint-over applied after UX is "done". WHY: aesthetics perceived as quality raise perceived functionality, so visuals are part of the function.
- When a stakeholder says "make it pretty", ask which specific visual principles are failing (hierarchy, contrast, spacing, type) instead of accepting a vague restyle brief. WHY: vague briefs produce identical rectangles with new colours and no memorability.
- Budget time for innovating wireframes into a distinctive visual direction; do not ship the first functional layout unchanged. WHY: functional-only UI is forgettable and wastes the brand opportunity.
- Allow unconventional UI presentations (e.g. floating in a fish tank) if they fit the game and remain readable. WHY: novelty creates fond memories and differentiation, provided usability is preserved.
- Apply the Rule of Cool deliberately: accept a small UX cost for a striking element only after consulting the UX designer. WHY: coolness can improve the experience, but unchecked it produces impractical designs.
## Checklist
- Does the visual direction match the game's tone, genre and brand?
- Is every "cool" element still readable and operable at gameplay speed?
- Has the UX designer reviewed and signed off on any deliberate UX trade-off?
- Would a player remember this screen a week later?
## Anti-patterns
- Treating "make it pretty" as the whole UI brief.
- Painting over the same layout with new colours and calling it art direction.
- Sacrificing readability for coolness without a UX review.
- Assuming a bad game can be rescued by UI polish.

---
name: ui-platform-constraints
topic: Platform-specific UI design
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Identify target platforms before any layout work: VR, mobile, console, PC, or multiplatform. WHY: each has different input, screen size, performance and certification constraints.
- Mobile: design for small screens and finger-sized touch targets; expect layouts to differ from PC/console. WHY: finger precision is far lower than a mouse cursor.
- PC: assume wide variance in hardware, displays, performance and mouse/keyboard setups; expose graphics and control options. WHY: players must be able to tune for their machine.
- Console: plan for strict platform certification checks and fixed specifications early. WHY: cert failures late in production are expensive.
- VR: avoid traditional flat-screen UI patterns; place UI in 3D space and test for comfort. WHY: screen-space UI strapped to the face causes discomfort and breaks immersion.
- Keep the experience seamless and immersive across platforms even when layouts differ. WHY: players expect the same game, not a downgraded port.
## Checklist
- Platform list confirmed and documented before wireframes.
- Touch target sizes validated on the smallest supported mobile device.
- Console cert requirements reviewed with the platform holder's checklist.
- VR UI tested for comfort, legibility and depth placement.
- PC settings menu exposes graphics, audio, input and UI scaling.
## Anti-patterns
- Designing one layout and scaling it to every platform.
- Ignoring console certification until submission.
- Reusing flat HUD conventions in VR.

---
name: visual-design-principles
topic: Visual design fundamentals for UI
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Consistency: keep one visual language across elements, motion, layout and design. WHY: consistency builds intuition and makes the UI look polished.
- Hierarchy: order elements by importance using size, colour, contrast and placement. WHY: players must find critical information fast.
- Contrast: vary elements enough to separate them from the rest of the interface. WHY: contrast creates visual interest and reinforces hierarchy.
- White space: leave intentional blank areas between elements. WHY: negative space declutters, balances and directs attention.
- Typography: choose fonts for readability first, tone second. WHY: unreadable type breaks the UI regardless of style.
- Colour: never use colour as the sole identifier. WHY: colour vision varies across players; pair colour with shape, icon or text.
- Simplicity: reduce visual complexity when information density is high. WHY: lowers cognitive load.
- Balance: use symmetrical (mirrored on a central axis) or asymmetrical (varied sizes and weights in equilibrium) composition deliberately. WHY: balance makes dense layouts feel stable rather than chaotic.
## Checklist
- One consistent visual language across all screens.
- Every screen has a clear primary, secondary and tertiary focus.
- Contrast checked for foreground vs background on all text and icons.
- White space used intentionally, not left over.
- Font legibility verified at the smallest rendered size.
- No information conveyed by colour alone.
- Layout balance chosen consciously (symmetric or asymmetric).
## Anti-patterns
- Mixing multiple unrelated visual styles across screens.
- Flat hierarchy where everything competes equally.
- Low-contrast text over busy backgrounds.
- Cramming elements edge to edge with no negative space.
- Colour-only status indicators (e.g. red/green only).

---
name: ui-representation-types
topic: Diegetic, non-diegetic, spatial and meta UI
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Classify each UI element on two axes: diegesis (does it exist in the game's reality?) and spatiality (does it sit in the 3D space?). WHY: classification drives cost, immersion and implementation approach.
- Non-diegetic (outside the narrative, player-only): default choice for most HUDs. Cheap to design and implement, independent of other disciplines. Risk: overuse causes information overload. WHY: it is the lowest-risk option but the least immersive.
- Meta (in the game's reality but not in 3D space, e.g. full-screen blood, sniper scope POV): use to blend information into the narrative. WHY: it delivers information with narrative flavour and can be subtle or intrusive as needed.
- Spatial (in the 3D world but not acknowledged by characters, e.g. ball-tracking arrows, grenade arcs, world-projected tutorials): use when orientation or world position matters. WHY: communicates direction and distance across three axes. Cost: more art direction and resources.
- Diegetic (in the world and acknowledged by characters, e.g. health on the character's suit, in-world wrist computer): use as a unique selling point when immersion is the goal. WHY: reduces screen clutter and deepens realism. Cost: many teams must coordinate; fragile to lighting, animation and performance changes.
- Decide representation after art direction and creative vision are set, then ask: is this element part of the story, and must it sit in the scene's space? WHY: choosing too late forces a fallback to non-diegetic overlays.
## Checklist
- Every UI element labelled as non-diegetic, meta, spatial or diegetic.
- Diegetic elements verified readable under all in-game lighting conditions.
- Spatial elements tested for occlusion and camera-angle legibility.
- Meta elements checked for how intrusive they become at peak intensity.
- Production cost and cross-discipline dependencies estimated per representation.
## Anti-patterns
- Defaulting everything to non-diegetic overlays without considering alternatives.
- Choosing diegetic UI late, when there is no budget to integrate it properly.
- Diegetic UI that becomes unreadable when environment lighting breaks.
- Assuming diegetic UI is automatically cheaper because it "takes less screen space".

---
name: attention-and-cognitive-load
topic: Directing player attention in UI
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Never assume players know where to look; design a deliberate attention hierarchy. WHY: unattended critical information causes failure and frustration.
- Distinguish endogenous attention (voluntary, player-driven, e.g. opening a quest log) from exogenous attention (involuntary, e.g. an incoming attack). WHY: each requires different presentation and placement.
- For endogenous flows, keep phrasing, iconography and presentation consistent between related systems (map, HUD markers, objectives). WHY: consistency lets players find what they already expect.
- For exogenous events, decide between peripheral placement (non-blocking but easy to miss) and central placement (unmissable but blocks gameplay). WHY: the right choice depends on how critical the event is.
- Design within the useful field of view (UFOV): the area where players can actually read and react at a glance. WHY: information outside UFOV is effectively invisible during play.
- Do not place related information on opposite sides of the screen. WHY: players cannot reliably connect them under time pressure.
- Account for target demographic: children and older or visually impaired players have a narrower UFOV. WHY: a smaller UFOV causes missed critical information and mistakes.
- Use multiple UI channels: visual (primary), audio (confirmation, errors, spatial direction) and haptics (tactile feedback). WHY: multi-channel feedback improves accessibility and immersion.
- Always provide a way to reduce or disable haptics. WHY: vibration can cause pain or stress for players with motor impairments.
## Checklist
- Attention hierarchy defined for every screen and HUD state.
- Endogenous and exogenous events listed separately with placement decisions.
- Related information grouped within the same visual region.
- UFOV tested with the target demographic, including older players.
- Audio cues present for confirmations, errors and off-screen threats.
- Haptics toggle and intensity control exposed in settings.
## Anti-patterns
- Displaying everything simultaneously and expecting players to absorb it.
- Fixing unclear mechanics by adding more UI ("fix it in UI").
- Placing critical warnings in the periphery where they are ignored.
- Blocking the central gameplay area with non-critical messages.
- Haptics with no opt-out.

---
name: common-ui-screens
topic: Start screen, frontend menus, settings, HUD, overlays
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Start screen: use it to detect and assign the input device, connect online, load the profile, and set the game's tone. WHY: it is the first second of the experience and a technical checkpoint.
- Frontend menus: keep navigation two to three levels deep when players must navigate backwards; unlimited depth is acceptable only for one-directional flows. WHY: deep back-navigation is confusing and slow.
- Frontend menus: use the main menu to foreshadow the world, show progress, or teach a mechanic. WHY: it is otherwise a skipped screen and a wasted opportunity.
- Avoid heavy animated menu backgrounds that slow transitions between screens. WHY: slow menu changes frustrate players and the trend has faded for that reason.
- Settings: expose graphics, audio, input, control bindings, UI, language and gameplay parameters. WHY: TVs, sound systems, environments, skills and needs differ per player.
- Settings: match the widget to the data — slider for continuous ranges, toggle for binary, discrete options for low/medium/high. WHY: mismatched widgets make options hard to set precisely.
- HUD: keep it unobtrusive and prefer dynamic reveals over always-on elements. WHY: too much simultaneous HUD causes clutter and cognitive overload.
- HUD density must match genre: minimal or absent in cinematic story games; strict and non-obstructive in competitive shooters; information-rich in RTS, MMO and city builders. WHY: players of dense genres expect and want the data.
- In-game overlays: decide whether the overlay pauses, slows time, or runs live, and whether it is transparent, opaque, full-screen or partial. WHY: the overlay's function determines its interaction model.
- Only include HUD features the game actually needs (no health bar without a health mechanic, no ammo counter in a gun-free game). WHY: unnecessary UI adds noise.
## Checklist
- Start screen handles input device detection and background loading.
- Menu depth audited: back-navigation never exceeds three levels.
- Main menu does something beyond listing buttons.
- Settings cover graphics, audio, input, bindings, UI, language, gameplay and accessibility.
- Each setting uses the correct widget type.
- HUD elements justified by an actual game mechanic.
- HUD density reviewed against genre expectations.
- Overlay behaviour (pause/slow/live) documented per overlay.
## Anti-patterns
- Deep nested menus that require repeated back-navigation.
- Long camera swoops between menu screens.
- Always-on HUD with every possible stat visible.
- Copying a shooter HUD into an RTS or vice versa.
- Settings screens that only expose developer defaults.

---
name: ui-art-routes
topic: Establishing UI art direction routes
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Present three to four routes to stakeholders, no more. WHY: too many options dilute the ideas and produce weaker or similar choices.
- Only present routes you would be happy to execute. WHY: you may have to build the chosen one.
- Define each route with four fields: Name, Slogan, Pillars, Execution. WHY: this template makes routes comparable and pitchable.
- Name: give each route a short catchy label (e.g. "retro-futurism", "sci-fi prehistoric tribal"). WHY: a name avoids re-explaining the theme and generates excitement.
- Slogan: one sentence summarising the route. WHY: busy directors need the pitch in one line.
- Pillars: three to five fundamental aesthetic aspects (e.g. tribal, high-tech, mystical, organic). WHY: constraints focus research and creativity.
- Execution: list the concrete techniques and include a few key research images. WHY: shows stakeholders you know how to deliver, not just what it looks like.
- Before collecting references, answer: what genre, who is the audience, what are the themes, is it new IP or an existing franchise? WHY: references gathered without these answers are unfocused.
- Plot the game on an immersion-to-abstraction axis. WHY: immersion pushes toward diegetic/spatial solutions; abstraction permits metaphorical, non-diegetic UI.
- For immersive routes, research the period's history, anthropology, art, typography and graphic design. For abstract routes, look at current and upcoming trends. WHY: the reference base determines authenticity.
- Use genre and competitor analysis to establish known affordances and spot what audiences are tired of. WHY: genre sets expectations you can meet or deliberately break.
## Checklist
- Three to four routes prepared, each with Name, Slogan, Pillars, Execution.
- Genre, audience, themes and IP status answered before research begins.
- Immersion vs abstraction position agreed with directors.
- Competitor UI reviewed for expectations and fatigue points.
- Each route has supporting key images, not a large dump.
## Anti-patterns
- Presenting a single route with no alternatives.
- Presenting ten routes, producing diluted or near-identical options.
- Starting reference collection before the game's vibe is defined.
- Pitching routes you would not want to build.

---
name: ui-research-and-mood-boards
topic: Reference research, mood boards and style guides
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Do not rely on internet search alone for references. WHY: online-only research repeats what already exists.
- Source primary references: visit locations, museums, exhibitions, libraries; photograph real signage, decals, covers and borders. WHY: raw references produce authentic but unique patterns.
- For historical settings, get to a museum or obtain period objects. WHY: period detail is rarely available online in usable form.
- For non-real settings, build your own references (e.g. photograph a leaking tank with a tablet underwater to capture refraction and caustics). WHY: custom references give you effects no stock image provides.
- Also draw from films in the same genre, period books, and nature. WHY: broad sources expand the idea space cheaply.
- Keep a small set of strong "hero" references rather than thousands of similar ones. WHY: large undifferentiated collections slow decisions and dilute direction.
- Organise references into subfolders by media type, pillar, mood, style and theme. WHY: an unorganised single "ideas" folder becomes unusable.
- Annotate every reference with why it is useful and what you like or dislike. WHY: notes preserve the reasoning when the reference is reused later.
- Practise restraint: keep the best reference and move the rest to a separate folder. WHY: hoarding references prevents a clear direction.
- Mood board: organise by pillars and keep the reference count concentrated. WHY: directors will not review hundreds of images and still grasp the route.
- If a route cannot be summarised with a few references, keep researching. WHY: an unclear mood board signals an unclear route.
- Style guide: document colour, typography, icons and core visual elements, and show "this, not this" examples. WHY: it communicates the UI vision to other departments, new team members, outsourcing partners and directors.
- Style guide: aim to give artists the tools to solve new problems, not to cover every case. WHY: a guide that only lists fixed solutions fails on unforeseen work.
## Checklist
- At least some references sourced outside the internet.
- Reference library organised into subfolders by pillar and media type.
- Notes attached to each retained reference.
- Hero references limited to a small, strong set.
- Mood board organised by pillars and readable at a glance.
- Style guide covers colour, typography, icons and do/don't examples.
- Style guide shared with other disciplines, outsourcing and new hires.
## Anti-patterns
- Pinterest-only research.
- One giant "ideas" folder with no structure.
- Mood boards with hundreds of images and no clear message.
- Style guides that only show the correct usage and never the wrong one.
- Treating the style guide as a complete problem-solving document.

---
name: ui-mockups-and-previs
topic: High-fidelity mockups and pre-visualisation
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 6 (pp. 77-95)"]
---
## Rules
- Produce a high-fidelity mockup or pre-vis before implementation. WHY: it lets you experiment with solutions and catch conflicts early, saving time and resources.
- Include all UI elements in the mockup: menus, buttons, icons and text. WHY: partial mockups hide integration problems.
- Make the mockup as close to the final product as possible. WHY: fidelity is what makes the pre-vis a reliable test of the real UI.
- Use a design tool such as Photoshop, XD, After Effects, Sketch or Figma. WHY: these support rapid iteration and animation previews.
- Use the mockup to test the route against the style guide before committing engineering time. WHY: cheaper to change a mockup than a shipped system.
## Checklist
- Mockup covers every screen in the flow, not just the hero screen.
- All elements present: menus, buttons, icons, text.
- Fidelity high enough to judge typography, contrast and spacing.
- Mockup reviewed against the style guide and chosen route.
- Problems and conflicts logged before implementation starts.
## Anti-patterns
- Jumping straight from wireframe to engine with no high-fidelity pass.
- Low-fidelity mockups used to make final visual decisions.
- Mockups that omit states (hover, disabled, error, loading).

<!-- 7 UI: Survival Guide (pp. 96-125) -->
---
name: ui-systems-architecture
topic: UI systems (menu manager, focus, input routing)
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Treat UI/UX as iterative, not linear: expect re-evaluation after art is added, since layouts that work in wireframes often break once visuals land. WHY: art changes perceived weight, contrast and spacing.
- Build a UI system of reusable components + patterns covering input routing, navigation and menu management. WHY: consistency, reuse, scalability, shared language between design/dev/stakeholders.
- Use a menu manager to create, show and control menu flow, so new options can be added without touching underlying code. WHY: decouples content from logic.
- Implement an explicit focus system: exactly one component is "focused" (ready to receive input) at any time. WHY: player must always know where input goes.
- Route input to the correct data asset/function/action rather than hard-wiring per-screen handlers. WHY: required for deep, multi-layered menus.
- Support both mouse and keyboard on PC — clicking, key-navigation to the element, and a single key to activate. Use WASD and arrow keys for directional navigation. WHY: either-only input excludes players.
- Design for left-handed PC players as a first-class case, not an afterthought.
- For VR, use spatial or diegetic UI with natural affordances (physical-feeling buttons/objects in world). WHY: flat screen-space UI breaks presence and readability in 3D.
- Pick input method from platform + game type: touch (thumb/finger pressure, direction, motion), gamepad (limited buttons/combos), mouse+keyboard, VR. WHY: each has different ergonomic and detection constraints.
- On touch, avoid small buttons in hard-to-reach zones and complex gestures; decide one-handed vs two-handed/landscape early. WHY: reachability and gesture complexity directly determine enjoyment.
- Treat "free cursor" navigation (Destiny-style) as a specialist tool: good for grid layouts, but costs more engineering and is less accessible; only use when the layout justifies it. WHY: poorly implemented free cursor is worse than D-pad/analog navigation.
> CHECK: OCR shows "pole-playing games" for RPGs — likely a typo, verify original wording.

## Checklist
- Can every interactive element be reached by every supported input device?
- Is focus state always visible and unambiguous?
- Can new menu entries be added without code changes?
- Are touch targets reachable in the intended grip (one hand / two hands)?
- Does the UI still read correctly after final art is applied?

## Anti-patterns
- Assuming the design is done once it looks good on paper or in a prototype.
- Shipping PC UI that requires a mouse only, or keyboard only.
- Adding free-cursor navigation by default because it looks modern.
- Porting screen-space UI directly into VR.

---
name: ui-design-patterns-catalogue
topic: UI widget and menu design patterns
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Don't argue about widget naming/classification; optimise for function. WHY: players never see the taxonomy, only the behaviour.
- Choose the pattern per problem, not the pattern you already have. WHY: no one-size-fits-all menu or HUD exists.
- Text: plan for variable-length strings (localisation can double or triple length; player names, level names, subtitles vary). Provide expansion room or pick a strategy:
  - Scale to fit: container grows with content.
  - Text-scaling: font size shrinks/grows inside a fixed box.
  - Truncation with ellipsis: last resort.
  - Scrolling text: looping animation for overflow in a fixed field.
  - Scroll box: manual scrollbar for multi-paragraph content.
- Keep UI copy concise; cut words if meaning is preserved. Allow extra words only when they add tone/fantasy and intent stays clear.
- Buttons must be familiar, accessible (never rely on one feedback channel) and have clear visual hierarchy.
- Every button needs: label or icon, a visible interactive hit area, and state visuals. Required states: default, hover/focused, pressed, deactivated, selected (selected only where applicable).
- Progress bars: define min/max bounds plus a fill graphic; support horizontal, radial, segmented circle, vertical, or partial-circle forms. Use them for both depleting resources (health, power) and accumulating progress (XP, timers).
- Menu pattern selection table:
  - Accordion: hierarchical content, space saving; poor discoverability of collapsed items, weak for screen readers.
  - Drop-down: grouped related options, space saving; hides options, awkward on some platforms.
  - Radial: intuitive, fast; hard limit on option count.
  - Hamburger: mobile space saving, familiar; hidden = discoverability/accessibility risk.
  - Grid: clear organisation, supports hierarchy via tile size; overwhelming when scrollable, especially on gamepad.
  - Flyout: clean UI; discoverability and accessibility risk.
  - Tab: fast on console (trigger/shoulder buttons), reduces menu layers; limited by horizontal space, keep tab count low.
  - Cross: HUD-friendly, icon-based, D-pad shaped; limited options, consumes space.
- Cards: group related info, use common-region principle, keep hierarchy clear, allow resize/rearrange for responsive layouts, leave generous white space. Avoid showing too many cards at once or overloading a card.
- Loader/throbber: always show motion during loads or waits. WHY: Doherty threshold — without feedback players assume the product is broken.
- Modals: use sparingly; they force interruption and break immersion. Always make them easy to close and unambiguous.
- Notifications: transient, non-blocking, usually no input required; may offer a routing action. Avoid overuse — they become noise.
- Sliders/steppers: intuitive and show current value, but limited precision/granularity — add numeric readout or fine-step control where exact values matter.
- Separators (visible lines) and spacers (blank space) both communicate grouping; pick one style and stay consistent.
- Carousel: show a position indicator (dots/count) so players know how many options exist; avoid long option sets.
- Checkboxes = boolean choice; toggle switches = binary state with explicit current-state feedback. Both states must be visually unambiguous.

## Checklist
- Does each widget have all required states designed?
- Does the chosen menu pattern fit the option count and input device?
- Is there a visible indicator for carousels, progress and loading?
- Are modals rare and closable?
- Are notifications non-blocking and time-limited?

## Anti-patterns
- Using a modal for routine information.
- Radial or cross menus with too many options.
- Toggle switches where the on/off state is ambiguous.
- Truncating text as the default overflow strategy.
- Scrollable grids on gamepad without strong navigation support.

---
name: colour-theory-and-contrast
topic: Colour theory, palettes and contrast for UI
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Limit the core palette to 2–4 colours; derive variety from tints, tones and shades. WHY: more colours read as chaotic and unprofessional.
- Define a named colour swatch language by usage/association (e.g. "alert", "legendary") and apply it consistently. WHY: consistent semantic naming beats arbitrary hue choices.
- Never rely on colour alone to convey information. WHY: ~1 in 12 men and 1 in 200 women have colour vision deficiency (CVD); ~300M people worldwide.
- Do not ship full-screen colour-blind filters. WHY: they shift every colour in the frame, break already-poor source colours, and "fix" CVD instead of designing around it.
- Preferred CVD solutions, in order: per-element colour pickers/wheels > selectable alternative palettes for names, reticles, enemy markers and gameplay info > redundant non-colour cues (shape, icon, pattern, text).
- Ensure text contrast is high enough to read; verify with a contrast checker against WCAG guidance.
- Give the primary action the highest contrast on screen. WHY: contrast creates hierarchy and directs the eye.
- Use contrast deliberately across multiple channels: colour, size, shape, texture, and position (horizontal/vertical/diagonal/radial).
- Check cultural context for colour meaning before locking a palette; avoid absolute claims like "red means bad". WHY: meanings vary by culture and game context.
- Consider texture on UI surfaces: it changes how a colour reads versus flat swatches.
- Treat colour as a support for UX, never a fix for confusing interactions.

## Checklist
- Is any gameplay-critical information encoded only in colour?
- Does the palette stay within 2–4 base colours?
- Has contrast been measured, not eyeballed?
- Are CVD alternatives available per element, not as a global filter?
- Does the primary action have the strongest contrast?

## Anti-patterns
- "Just make it go red" as the default feedback solution.
- Global colour-blind overlay filters.
- Too many hues in one screen.
- Ignoring CVD, low vision and dyslexia until late in production.

---
name: typography-for-ui
topic: Typeface selection, formatting and localisation
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Decide three font roles up front: body (workhorse), heading, and optional accent/decorative/caption/accessibility font.
- Keep font count low; if heading and body come from different typefaces, verify they pair well.
- Body text should be a clear serif or sans-serif that handles dense text; reserve decorative and script faces for headers/logos. WHY: decorative/script faces are hard to read small and often have poor language coverage.
- Avoid text below 18 pt — it becomes highly unreadable depending on the font.
- Use 2–3 weights total (e.g. regular + semi-bold) rather than adjacent weights like regular + medium. WHY: adjacent weights create weak, muddy hierarchy.
- Define a font usage guide (set sizes + weights) to keep the UI clean and reduce cognitive load.
- Terminology to use correctly: tracking = uniform spacing across a block; kerning = spacing between individual character pairs; leading = line spacing; cap-height = baseline to cap top; x-height = baseline to lowercase top (excl. ascenders/descenders). Higher x-height reads more open and accessible.
- Case usage: uppercase for short, urgent headers only (it reads "shouty" and is hard to read in bulk); sentence case for long UI text; title case for headings; lowercase only as a deliberate style.
- Licensing: most fonts need commercial licences; free fonts may still require credit; licences do not transfer between projects; keep a record of every font and its source.
- Never use the font behind a wordmark/logo, even if it is freely downloadable.
- Localisation: choose a Unicode font or a font-switching system that covers all required glyphs.
- Allow a 40% character buffer in layouts for translation growth.
- Provide maximum character limits for fixed-size text fields and add context notes to strings for localisation teams.
- Be careful with string concatenation of variables (e.g. [Legendary] [Sword]) — it can translate nonsensically. WHY: grammar and word order differ per language.
- Request a debug language-preview tool if one does not exist.

## Checklist
- Body, heading and accent fonts chosen and documented?
- Font licences recorded and valid for this project?
- Glyph coverage verified for every shipping language?
- 40% expansion buffer present in fixed text fields?
- Character limits and context notes supplied to localisation?
- No text below 18 pt?

## Anti-patterns
- Using a logo/wordmark font in the UI.
- Mixing many weights or many typefaces.
- Assuming a licence carries over to the next project.
- Designing text fields to the exact length of the English string.

---
name: iconography-design
topic: Icon design rules
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Design icons to work at multiple sizes; create an optimised small variant rather than relying on engine downscaling. WHY: detail that reads at large size turns to noise when scaled down.
- Match icon stroke width or fill amount to the typography it sits beside. WHY: mismatched weight makes the UI look assembled from parts.
- Build on pixel grids and guides to avoid half-pixels.
- Reduce icons to their simplest form. WHY: complexity increases comprehension time.
- Use established tropes (gear = options) unless you have a strong reason and a tested replacement.
- Test icons with people who lack context: ask "What does this mean?" Correct answers = a robust icon.
- New or brand-specific symbology is acceptable if it is thoroughly introduced and supported by heuristic descriptions.
- Watch for cultural offence and ambiguity across regions.

## Checklist
- Does the icon read at its smallest shipping size?
- Does stroke weight match adjacent text?
- Is it pixel-aligned?
- Has it been tested with uncontextualised users?
- Is any novel icon explained in-game?

## Anti-patterns
- Highly detailed icons scaled down by the engine.
- Inventing new symbols for common actions without explanation.
- Inconsistent icon style across the interface.

---
name: layout-alignment-and-anchoring
topic: Layout, alignment, rhythm, lines of force, anchoring, padding
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Align elements to establish hierarchy and a clear reading path; use the software's alignment tools even in rough mockups. WHY: a few minutes of alignment changes the overall impression.
- Design for the target market's reading direction (West: left-to-right, top-to-bottom); multiple regional layouts are usually impractical, so pick the primary market.
- Consider functional alignment too: place elements where their purpose implies they belong.
- Use rhythm (repeated shapes, colours, textures) for cohesion and variety (islands of detail) to avoid dullness; break long text with images, quotes, bullets or video.
- Design lines of force: start from the top navigation point and offset vertically per information block; diagonal lines are allowed. Trace the intended eye path and verify it hits the right elements in order.
- Anchor widgets to screen points (nine-point grid or custom axis) or stretch across corners/edges. Anchor from the primary parent downward. WHY: anchoring preserves layout when text resizes or the viewport changes.
- Test anchoring by expanding/retracting content and resizing the viewport, and observe what moves.
- Always use more padding than you think you need. WHY: generous padding looks more luxurious and absorbs variable content sizes without breaking layout.

## Checklist
- Is every element aligned to a shared grid or guide?
- Does the eye path hit primary action before secondary content?
- Are all widgets anchored, and tested under content/viewport change?
- Is padding generous enough for the longest expected string?
- Is rhythm varied enough to avoid monotony?

## Anti-patterns
- Free-floating elements with no alignment relationship.
- Anchoring children before parents.
- Tight padding that breaks when text expands.
- Assuming one layout works for all regions.

---
name: ui-animation-principles
topic: UI motion and animation techniques
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Define the purpose of every animation before building it: what information does this motion convey? WHY: motion should serve usability, accessibility and continuity, not just decoration.
- Classify interactions as real-time (direct player manipulation, e.g. scrolling) or non-real-time (triggered transitions after an action, e.g. button press). WHY: they need different timing and control models.
- Animate by manipulating properties over time: position, opacity, scale, rotation, anchor point, colour, stroke width, shape.
- Use easing so objects accelerate/decelerate like real-world objects. WHY: reinforces naturalism and continuity.
- Use offset and delay to signal hierarchy — e.g. header slides in, then subheader, ending on the action/button. WHY: it directs the reading order.
- Use parenting to link child properties to a parent so related elements move together.
- Use transformation (shape morphing) sparingly but deliberately — it is the most noticeable motion type.
- Animate value changes (score, combo, health) rather than leaving them static. WHY: it communicates that the data is live and interactive.
- Use masking to reveal/conceal and create continuity between a thumbnail and its expanded view.
- Use overlays to change the value of two layers at once, hiding or revealing information on demand.
- Use cloning so new objects visibly originate from an existing one. WHY: creates narrative and directs attention.
- Use obscuration (blur, modal) to clarify what is now in focus during transitions.
- Use parallax with the most important interactive element moving fastest.
- Use dimensionality (flip, slide-out) to imply real-world affordances players already understand.
- Use dolly/zoom (uniform scale manipulation) to imply travelling through elements and reveal detail.

## Checklist
- Does each animation have a stated purpose?
- Is easing applied rather than linear motion?
- Does offset/delay match the intended reading order?
- Are value changes animated, not snapped?
- Does motion survive being disabled for accessibility?

## Anti-patterns
- Animation added purely for "pizzazz" with no informational role.
- Linear, mechanical motion for UI transitions.
- Simultaneous equal-speed motion for elements of different importance.
- Motion that obscures the primary action.

---
name: ui-audio-feedback
topic: Audio as UI feedback
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Design distinct, recognisable sounds per action/event so players can identify interface state without looking. WHY: audio is a second feedback channel and improves intuitive understanding.
- Use pitch, tempo, chord and cadence to signal outcome: rising pitch/tempo implies conclusion or success; harsh or low tones imply failure.
- Use ambient sound, music and spatial audio to support atmosphere and immersion.
- Provide visual alternatives for any information conveyed only by audio. WHY: players with hearing impairments must not lose gameplay information.
- Give players volume controls plus per-category toggles (music, SFX, UI, voice) and any further customisation.

## Checklist
- Does every important UI event have a distinct sound?
- Is any critical information audio-only?
- Are per-category volume controls available?
- Do success/failure sounds differ clearly in pitch and tempo?

## Anti-patterns
- Audio as the sole channel for a gameplay-critical signal.
- Reusing one generic click sound for all events.
- No volume or category controls.

---
name: ui-workflow-organisation
topic: Naming conventions, folder structure, performance and engines
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 7 (pp. 96-125)"]
---
## Rules
- Follow the studio's existing naming convention rather than imposing your own; stay flexible.
- Naming rules: Latin characters and numbers only (no special characters); one consistent case (lowercase, camel, snake); no spaces (underscore only if the codebase allows); zero-pad numbers to the actual digit count needed (01–08, not 001–008).
- Recommended file name pattern: `Event_EventSpecific_Element_Type_Variation.extension` (e.g. `FE_Settings_BG_Texture_01.png`).
- Folder structure: organise by content type and intended use; use clear descriptive names; keep a logical hierarchy; avoid deep nesting; apply the same structure across projects/departments; review and update regularly; include a readme explaining the structure.
- Respect texture and computation budgets: use appropriate texture resolutions and space-saving techniques — channel packing, materials, signed distance fields, nine-slicing.
- Follow the power-of-two rule for textures. WHY: engines process data in limited chunks; non-power-of-two wastes memory and performance.
- Learn to bring your own artwork into the engine even if you are a graphic designer. WHY: it gives you control over the final look and reduces handoff loss.
- When choosing an engine, weigh third-party (Unreal, Unity — large community and docs) against in-house (no public resources, but the authors are in the building and can add features for your workflow).

## Checklist
- Do file names follow the studio convention and zero-padding rule?
- Is the folder hierarchy shallow and documented?
- Are textures power-of-two and within budget?
- Have you verified the asset in-engine, not just in the DCC tool?
- Is there a readme for new team members?

## Anti-patterns
- Inventing a personal naming scheme on an existing project.
- Deeply nested folders with vague names.
- Shipping high-resolution flipbook/animated textures without a performance check.
- Delivering mockups without ever opening the engine.

<!-- 8 Presentation Matters (pp. 126-137) -->
---
name: cv-resume-writing-rules
topic: Job application CV/résumé writing for game UX/UI roles
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 8 (pp. 126-137)"]
---
## Rules
- Keep the CV to 1–2 pages. Reviewers skim-read and have finite time; length dilutes signal.
- Curate content per application: re-tailor the CV to each job spec every time. Generic CVs read as low effort.
- Use keywords and language that mirror the job specification. Helps automated and human screening.
- Quantify achievements with tangible data and state your specific involvement in each project. "Shipped X feature used by Y players" beats "worked on X".
- Validate skills by showing what you learned/built, not by announcing the skill. Difference between claiming and demonstrating.
- Include a short personal statement with relevant hobbies as icebreakers; keep it brief.
- Export as PDF unless the submission is a web form or hosted on your own site. PDFs render reliably everywhere.
- Name files professionally: full name + document type + role applied for (e.g. `JaneDoe_CV_UXDesigner.pdf`).
- Verify every link works; if the portfolio is password-protected, embed credentials in the link. Reviewers click the portfolio first.
- Ensure the document prints cleanly — avoid solid black backgrounds.
- Proofread spelling and grammar; use tools or ask a mentor if writing in a second language.
- Omit secondary-school exam results unless explicitly requested; higher education and professional certifications suffice.
- Never list unsolicited references (people you haven't asked).
- First vs third person doesn't matter; clarity of content does.
- No photo — it wastes space better used for content.
## Checklist
- [ ] 1–2 pages, no filler or fluff
- [ ] Tailored to this specific job spec
- [ ] Achievements quantified, involvement explicit
- [ ] Portfolio link visible, working, accessible
- [ ] Filename includes name, doc type, role
- [ ] PDF export, prints legibly
- [ ] Spelling/grammar checked
- [ ] No skill progress bars, star ratings, or "brain" icons
## Anti-patterns
- Progress bars / star ratings / gamified skill scores (e.g. "Photoshop 9/10") — meaningless and reads as arrogant.
- Icon of a human brain listed as a skill — signals arrogance.
- Repetitive filler padding the page count.
- Unsolicited references.
- Broken or password-walled portfolio links.
> CHECK: OCR shows "deceleration of intent" in the cover-letter section (p. 136); likely "declaration of intent". Verify against print copy.

---
name: portfolio-curation-rules
topic: UX/UI portfolio content and ordering
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 8 (pp. 126-137)"]
---
## Rules
- Portfolio work must match or surpass the quality the target studio already ships. If it doesn't, spend the CV/portfolio-prep energy on making stronger pieces instead.
- Show only your best work. Anything included is fair game for interview questions — exclude projects that ended badly or that you didn't enjoy.
- Curate the order as a deliberate experience: lead with work closest to the studio's genre/style, not your most extreme range piece.
- Keep layout consistent across every piece — same structure, same reading pattern. Reviewer shouldn't re-learn how to read each entry.
- Lead with the final result ("money shot"), then show process underneath: wireframes, diagrams, pre-vis, prototypes.
- Recreate all process artifacts digitally. No photos of sketchbooks or sticky-note walls.
- Credit employers, studios, and collaborators with logos and a copyright blurb; follow studio approval policy if required. Watermark personal work or add your name/social handle.
- Write a short description per piece: your contribution, what you learned. Don't embellish, lie, or undersell.
- Include video/GIF for motion design work — it's a core UI skill and adds a dimension static images can't.
- For on-site interviews, bring a laptop/tablet and have an offline copy (PDF on external drive) of any web portfolio.
- Optional off-topic work (personal projects, life drawing, street art) at the end is fine and shows personality.
- For UX roles, demonstrate research, user flows, wireframing, personas, interaction design, information architecture. For art/design roles, add interfaces, iconography, typography, motion graphics, implementation examples.
## Checklist
- [ ] Every piece earns its place (skill demonstrated, defensible in interview)
- [ ] Order matches target studio's output
- [ ] Consistent template across pieces
- [ ] Final result first, process after
- [ ] All process art recreated digitally
- [ ] Credits, copyright blurb, watermark present
- [ ] Per-piece description states contribution + learning
- [ ] Motion work shown as video/GIF
- [ ] Offline backup of web portfolio ready
## Anti-patterns
- Leading with a genre the target studio doesn't make.
- Photos of physical sketchbooks or sticky-note walls.
- Inconsistent layouts that make the reviewer re-learn navigation.
- Including old work that drags down perception of current ability.
- No description, leaving reviewers to guess your contribution.

---
name: portfolio-platform-choice
topic: Choosing where to host a portfolio
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 8 (pp. 126-137)"]
---
## Rules
- Choose a platform you can maintain long-term; portfolio upkeep is continuous, so an unmaintainable format is a net loss.
- Optimise for reviewer access and readability first — great content behind a frustrating experience gets abandoned.
- Published digital document (PDF): full layout control, works on most machines/browsers, fits on a USB stick, emailable. Costs time to build; use reusable templates per piece.
- Prefabricated platform (ArtStation, Behance, template site): fastest path, handles hosting and layout, adds organic discovery and networking. Less presentation control.
- Custom website: maximum control and per-employer customisation, but only worth it if you have the time, skill, and drive — and it must be easy to update. A custom site that performs worse than a template reflects badly.
- On any public platform, add copyright notices and watermarks to assets and use privacy settings. Public work is exposed to theft and generative-AI training.
## Checklist
- [ ] Platform is maintainable with your available time
- [ ] Reviewer can reach content in minimal clicks
- [ ] Templates exist for adding new pieces quickly
- [ ] Watermarks/copyright on all public assets
- [ ] Privacy settings reviewed
## Anti-patterns
- Building a custom site you can't keep updated.
- Choosing a format that renders inconsistently on the reviewer's machine.
- Publishing unwatermarked work on open platforms.

---
name: portfolio-without-professional-experience
topic: Building a portfolio with no shipped titles
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 8 (pp. 126-137)"]
---
## Rules
- Coursework is acceptable as initial portfolio content — judge it by what skill it demonstrates, not by sentiment. Cut coursework that now looks weak; employers read it as your current ability.
- Compensate for missing years of experience with volunteer work, internships, and adjacent-field experience.
- Ask a trusted contact for a referral. Studios often fast-track referrals; only ask people who can genuinely vouch for your skills and professionalism.
- Show enthusiasm in correspondence: frame gaps as "I don't know yet, but I will soon" rather than "I can't do that".
- Mirror the studio's stated values and culture in your materials.
- List accomplishments and accolades where professional experience is thin.
- Build deep proficiency in the studio's engine or in emerging/underserved software. Technical scarcity offsets a thin CV.
- Replace tutorial-following pieces with personal projects: short, achievable, creative, each highlighting one specific ability.
- Case studies of existing games work well: analyse and improve a title's UX, modernise an old game's visual design, or re-imagine it in another genre. Be respectful when critiquing a studio you're applying to.
- Game jams produce legitimate portfolio experience (practical skill, networking, collaboration). Budget for travel, food, accommodation on paid/location events.
## Checklist
- [ ] Coursework vetted for demonstrated skill, weak pieces cut
- [ ] At least one personal project per target skill
- [ ] One case study tailored to the target studio's style
- [ ] Referral requested from someone who can vouch for you
- [ ] Engine/software expertise evidenced
## Anti-patterns
- Portfolios made only of followed tutorials — shows instruction-following, not problem-solving.
- Taking on a mammoth personal project while job-hunting; keep projects achievable.
- Pestering random developers online for referrals.

---
name: cover-letter-structure
topic: Cover letter writing for game UX/UI roles
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 8 (pp. 126-137)"]
---
## Rules
- One page. Bespoke per application — never a prefixed template.
- Mirror the language and voice of the job advert. The advert is a sample of how the studio writes; matching it helps them picture you in the role.
- Salutation: "Hello [Hiring Manager]" is fine when the name is unknown. Use published preferred pronouns; otherwise use ungendered language. Avoid "Dear" — reads old-fashioned.
- Introduction (first paragraph carries the weight — attention isn't guaranteed past it): state interest in the role, how you found it, and a one-line experience summary. Let the CV carry the detail.
- Body: engaging, ideally amusing; cover your background, interests, education, what you've learned and what you want to learn next, and the impact you'd bring. Name at least one specific thing that genuinely inspires you about the company or its games.
- Mention a referrer if you have one.
- Conclusion: thank them, give contact details and professional social links, sign off "All the best." + your name.
- Verify all links work and that social profile names are professional — employers will check social media.
## Checklist
- [ ] One page, tailored to this studio
- [ ] Salutation uses correct name/pronouns or neutral language
- [ ] Intro: role, source, experience summary
- [ ] Body: specific genuine detail about the studio, learning goals, impact
- [ ] Referrer named if applicable
- [ ] Contact + working professional links
- [ ] Language mirrors the job advert
## Anti-patterns
- Copy-paste cover letter reused across applications.
- "Dear Sir/Madam" or "Dear" openings.
- Generic praise that could apply to any studio.
- Unprofessional social handles linked from the letter.

<!-- 9 Dig Deep (pp. 138-154) -->
---
name: job-search-values-and-targeting
topic: Job search strategy for game UX/UI roles
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Before searching, write down your non-negotiables and compromises across: compensation/perks, relocation vs remote, studio size (AAA vs indie), target platform (mobile/console/VR), and urgency (need any job now vs can wait). WHY: a "perfect" role that ticks every box is rare; knowing your real constraints prevents wasted applications and bad fits.
- Apply to roles that genuinely match your goals, even if you feel under-qualified. WHY: waiting until you feel "ready" means missing openings; studios rarely require 100% of the listed criteria.
- Do not blanket-apply to every studio you can find. WHY: mass applications cause rejection fatigue, stress, and time loss without improving odds.
- Keep building your portfolio while you apply. WHY: it is the main lever you control and improves every future application.
- Use studio career pages as the primary source; they are usually the most current and give a direct application route (email or form).
- Send speculative applications when no matching role is listed. WHY: some studios keep candidates on file or create a role for a strong fit.
- Use job boards (LinkedIn, Glassdoor, Discord communities) for discovery only; find the real contact and apply directly.
- Avoid "easy apply" / one-click automated applications. WHY: they remove your control and often land in a spam folder.
- Read each posting carefully and follow its stated application instructions exactly. WHY: ignoring them signals poor communication and may get your application auto-discarded.
- Do not cold-call internal recruiters whose contact details are not public. WHY: it reads as intrusive rather than proactive.
- Verify external recruitment agencies before signing up; quality varies from career-building to commission-chasing spam.
- Treat referrals correctly: an employee recommending you is not nepotism, but you still go through the full process and scrutiny.
- QA is no longer an easy entry role; expect a rigorous process and demonstrate professional soft skills plus a relevant degree where possible.
## Checklist
- Values/constraints written down before searching
- Portfolio, CV, cover letter current
- Professional social profiles updated
- Application tracker created (studio, role, stage, contacts, outcome, feedback)
- Target list built from career pages, not job-board spam
- Each application tailored, not copy-pasted
## Anti-patterns
- Applying everywhere "like buying scratch cards"
- Using easy-apply buttons
- Cold-calling recruiters with no public contact info
- Skipping the posting's stated application method
- Applying only when you feel fully qualified
> CHECK: OCR shows "UIPeeps.com" and "WE CAN FIX IT IN UI" as Discord communities — verify exact names/URLs before citing.

---
name: application-etiquette-and-red-flags
topic: Recruitment etiquette and employer red flags
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Judge a studio by its recruitment process: responsiveness, respect for your time, transparency, and inclusivity. WHY: process quality is a cheap proxy for how organised and people-focused the studio is.
- Ask the recruiter up front what the process looks like and what happens at each stage. WHY: it sets expectations and lets you spot an unreasonable pipeline early.
- Learn the names and professional background of your interviewers before the interview.
- Request detailed feedback after an interview if it is not offered automatically.
- Track every application with stage, contacts, and outcomes. WHY: patterns in rejections reveal what to fix in your CV or portfolio.
- Follow up on correspondence, but do not pester.
- Know your salary target, start date, and contractual notice period before you apply.
- Treat every interaction as if the person may be a future colleague.
## Checklist
- Portfolio/CV/cover letter ready before applying
- Professional boundaries respected in all communication
- Interviewer names and backgrounds researched
- Feedback requested post-interview
- Application tracker maintained
- Salary, start date, notice period known
## Anti-patterns
- Multi-month interview pipelines with many lengthy stages
- Long silences, ghosting, or unresponsiveness
- Rude or poor communication
- Unnecessarily long art test that looks like free work
- Different interviewers than scheduled with no explanation
- Interview starting late with no acknowledgement
- Offers the studio cannot substantiate
- Interviewers who have not read your portfolio or CV
- Generic or unprepared questions
- Refusal to discuss compensation
- Non-inclusive language or morally questionable remarks
- "We are a family" — treat as a strong warning sign

---
name: interview-preparation-and-conduct
topic: Interview preparation and behaviour
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Research the studio's past projects and stated values before the interview. WHY: "What do you know about our studio?" is a standard warm-up testing genuine interest; do not improvise an answer.
- For remote interviews, be at your setup 15 minutes early and test mic, camera, and headset.
- For on-site interviews, arrive early enough to freshen up, get water, and settle.
- Keep CV, portfolio, and prepared questions on a second screen (remote) or laptop/tablet/printout (on-site).
- Practise active listening: let people finish, pause before answering, and note points to return to instead of interrupting.
- Use interviewers' names during conversation. WHY: it makes the exchange personal and memorable.
- Take notes during the interview, but do not let note-taking pull you out of the conversation; remotely, avoid looking like you are answering email.
- After the interview, write down the questions asked and your answers into your tracker and reword any question that failed to get you the information you wanted.
- Stay hydrated; a sip of water is a natural pause to think.
- Avoid heavy caffeine immediately before the interview; eat a light healthy snack instead.
- Convert nervous energy into kinetic energy (light exercise, dancing) and watch something funny for an endorphin lift.
- Avoid doom-scrolling social media before the interview.
- Dress appropriately for on-site; for remote, ensure at least the visible half is presentable.
- Practise mock interviews if time allows.
- Take three long deep breaths before starting.
## Checklist
- Studio research done (projects, values)
- Tech tested, 15 min early (remote)
- Notes/portfolio/questions accessible
- Water on hand, caffeine limited, snack eaten
- Questions asked written down afterwards
## Anti-patterns
- Improvising an answer to "what do you know about us"
- Interrupting out of enthusiasm
- Over-preparing with too many notes/windows open
- Doom-scrolling before the call
- Treating the interview as a script recital — rehearsed answers are detectable and break when you must go off-script

---
name: answering-interview-questions
topic: Structuring interview answers
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Identify the keywords the interviewer needs to hear for each question, then answer out loud without notes, concise and on point. WHY: interviewers tick off a checklist of expected signals and remember impressions, not your exact words.
- Keep answers short and free of filler or tangents. WHY: retention is limited; a clear main point survives, rambling does not.
- Mine the job spec for answer material — many expected answers are already implied there.
- Prepare for these common questions: what you know about the studio; why this role; what you bring; work ethic; proudest career moment; managing competing priorities; what motivates you; a time you failed; a difficult situation; strengths; weaknesses; disagreeing with a decision; salary expectations; notice period.
- Do not memorise a full script. WHY: rehearsed delivery is detectable and collapses when the interviewer deviates.
## Checklist
- Keyword list per common question
- Answers rehearsed aloud, not read
- Job spec re-read for answer material
- Salary figure and notice period ready
## Anti-patterns
- Reciting a scripted answer
- Long answers with filler
- Ignoring the job spec when preparing
> CHECK: OCR lists 14 common questions; confirm numbering and wording against the print edition before reusing verbatim.

---
name: questions-to-ask-interviewers
topic: Candidate questions and evaluating the employer
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Never answer "no" to "do you have any questions?" — prepare two or three. WHY: it is your only chance to evaluate the employer and to signal you already think like an employee.
- Ask open questions that force elaboration. WHY: yes/no questions let interviewers mask problems and tell you what you want to hear.
- Skip anything already answered in the interview or listed on the job ad. WHY: asking for information already given wastes everyone's time.
- High-value questions to use:
  - "What does success look like in this role?" — reveals performance review, promotion, and bonus processes.
  - "What advice would you give me to succeed here?" or "If I started today, how would you best use my skills?" — makes them visualise you in the role and reveals their leadership style.
  - "What were your team's biggest challenges this past year?" — reveals studio stability and team dynamics.
  - "How would you describe the studio culture — hierarchy, management, social, community?" — a "family" answer is a red flag.
  - "How much autonomy comes with the role?" — surfaces micromanagement, review process, and whether you can speak up.
  - "What would you add or remove from my CV, portfolio, or this interview?" — extracts feedback you may otherwise never get.
- If time runs out, ask permission to email a few more questions; a good interviewer will agree.
## Checklist
- 2-3 open questions prepared, none already answered
- Questions chosen to reveal culture, autonomy, and success metrics
- Follow-up email offer made if time is short
## Anti-patterns
- "Do you like working here?" or "When do the free snacks arrive?"
- Yes/no questions like "Is this a collaborative environment?"
- Leaving with only information you could have found online

---
name: art-and-design-tests
topic: Handling unpaid art/design tests
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Accept an art test only if it is well scoped, time-limited, and abstract enough to show creative thinking rather than reproduce the studio's existing work. WHY: a fair test yields new information; a bad one is free labour.
- Decline tests that ask you to produce assets for a game currently in production. WHY: that is unpaid production work, not assessment.
- Weigh the test against your real life: full-time work and responsibilities mean the extra hours come out of health, career, or relationships.
- As a hiring studio: use art tests only in final stages for top candidates, never as a blanket filter. WHY: strong portfolios can still fail under time and resource constraints, and blanket tests exclude candidates with limited free time.
- Design the brief to be achievable within a stated time limit, accounting for candidates who work full time.
- Give every test-taker professional, constructive feedback regardless of the hiring outcome.
## Checklist
- Test is abstract, not production assets
- Time limit stated and realistic
- Scope accounts for work/life commitments
- Feedback promised to all candidates
## Anti-patterns
- Tests that recreate the studio's current art
- Open-ended briefs with no time cap
- Using tests as a lottery to avoid making a hiring decision
- No feedback after a candidate invests hours

---
name: salary-negotiation
topic: Compensation research and negotiation
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Compute a survival baseline first (rent/mortgage, food, dependents, life outside work), then research market rates for your role, region, and studio size (Glassdoor, general search).
- Adjust expectations for location and studio type: major-city studios pay more but cost more to live in; small indies may pay less but offer remote work or cheaper locations.
- Value the whole package, not just salary: annual leave, sick pay, pension, medical cover, parental leave, bonus schemes, transport discounts, merchandise, learning budgets, flexible time, relocation support.
- You are not obliged to disclose your previous salary.
- Ask for more than your target so a lower counteroffer still satisfies you. WHY: it gives the studio room to feel they won a deal while you hit your number.
- Depersonalise the negotiation: talk about the company, not the interviewer ("Would Studio X...?" not "Would you...?").
- Frame your number as market demand, not aspiration: "I'm currently interviewing for positions that pay X to Y" rather than "I am looking for X."
- Lead with the value you bring, not what you want from them.
- Remember this is a starting salary; good studios run annual reviews, inflation adjustments, promotions, and milestone bonuses.
## Checklist
- Survival baseline calculated
- Market rate researched for role, region, studio size
- Benefits package valued alongside salary
- Target number and stretch number set
- Language depersonalised and market-framed
## Anti-patterns
- Naming a number below your baseline
- Disclosing prior salary as an anchor
- Asking for an unrealistic figure that prices you out
- Treating the negotiation as a personal favour request

---
name: offers-rejection-and-day-one
topic: Accepting offers, handling rejection, first day
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 9 (pp. 138-154)"]
---
## Rules
- Read the full contract before accepting; most are boilerplate, so a friend or family member's review is usually enough. Raise any concern politely with the hiring manager — you are still negotiating.
- Provide accurate referral contacts, choosing people who know your work, support you, and remember you. WHY: referrals usually only verify work history.
- Confirm visa and relocation needs early; the studio should support you once the process starts.
- On rejection: ask for feedback if none is given, respond politely, and move to the next application. WHY: hiring decisions are rarely about your performance alone — budgets, closures, and internal factors dominate.
- Do not speculate about why you were rejected; it is unproductive and harms self-esteem.
- First day: confirm start time (and first call time if remote) and be set up before it.
- Bring requested ID and official documents.
- Pay attention during the office tour.
- Do not talk about your previous job like an ex you are still infatuated with, and do not dump your whole CV on everyone you meet.
- Learn who the CEO, studio director, or owners are before they introduce themselves.
- Ask questions freely; "Sorry, I'm new, it's my first day" buys goodwill for roughly the first month only.
- Read all HR information you are given.
- Promptly request invites to relevant meetings, sprint planning, and communication channels.
- If your line manager, IT, and HR have not scheduled induction meetings, politely request them; cover expectations, best practices, goals, and responsibilities.
- Once settled, book time with direct peers over coffee to learn the team.
- Play the game. WHY: it is the fastest way to understand the project.
## Checklist
- Contract read and questions raised
- Referral contacts confirmed
- Visa/relocation discussed
- Start time confirmed, hardware/passwords received (remote)
- ID documents packed
- HR docs read, meeting invites requested
- Induction meetings scheduled or requested
- Project documentation read, game played
## Anti-patterns
- Signing without reading the contract
- Oversharing past employer stories
- Waiting passively for induction instead of requesting it
- Letting imposter syndrome stop you from asking for help — no one expects you to know everything, and colleagues often feel the same way

<!-- 10 Backup (pp. 155-168) -->
---
name: ui-ux-hiring-portfolio
topic: UI/UX hiring and portfolio
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 10 (pp. 155-168)"]
---
## Rules
- Lead the portfolio with a finished product or polished screen; hiring managers skim before reading process. WHY: they need a hook before investing time in wireframes.
- Include 2–3 strong pieces, not many weak ones; quality over quantity. WHY: interviewers judge presentation and attention to detail as much as the work.
- Show a broad range of art and game styles. WHY: proves adaptability across projects.
- Specialise: a UI/UX portfolio should contain game UI, not 3D art, code, or photography. WHY: generalist portfolios signal you want any job, not this one.
- If unsure between UI and UX, build separate portfolios per field. WHY: lets you apply to both and see which gets more responses.
- For each piece, state the rationale behind decisions and how it fits the game. WHY: hiring looks for reasoning, not just visuals.
- No professional work? Redesign an existing screen (e.g. an inventory or HUD) including art, layout and UX flow, and explain the changes. WHY: demonstrates the full process.
- Tailor portfolio pieces to the target studio's genre. WHY: designing with intent shows you researched the employer.
- Demonstrate ability to finish a project; a completed prototype or jam game outweighs a polished mockup. WHY: finishing is rare and teaches more than making something good.
- Learn engine basics (Unity, Unreal, Figma, shaders, scripting) and understand the wider dev process. WHY: lets you discuss implementation with engineers and producers.
- Use game jams, design briefs, and online challenges to generate portfolio work. WHY: self-motivated work stands out and fills an empty portfolio.
- Document jam and side projects in the portfolio afterwards. WHY: otherwise the learning and evidence are lost.
- Network genuinely: treat contacts like friends, ask questions they enjoy answering, keep professional boundaries. WHY: people detect transactional intent.
- Apply to roles matching your values and goals. WHY: reduces burnout and dissatisfaction.
- Keep learning after graduation via courses, talks (GDC, Games UX Summit, Game Accessibility Conference) and communities (We Can Fix It In UI, IGDA UX SIG). WHY: the field moves fast and gaps show.
- Protect your well-being; avoid comparing yourself to others. WHY: passion industries burn people out.
- Consider adjacent work (non-game UI, e-learning, serious games) as a stepping stone. WHY: skills transfer and it produces case studies.
## Checklist
- [ ] Portfolio opens with a finished, compelling piece
- [ ] 2–3 best pieces, varied styles
- [ ] Every piece states the "why" behind decisions
- [ ] Portfolio focused on game UI/UX, not unrelated disciplines
- [ ] At least one finished project or jam game
- [ ] Engine/tool familiarity demonstrated
- [ ] Resume and portfolio are skimmable, with the thesis up front
- [ ] Applied to roles aligned with your goals
## Anti-patterns
- Portfolio stuffed with 3D art, code, photography, or no game UI at all.
- Jack-of-all-trades positioning instead of specialist.
- Showing only mockups with no finished work.
- Text-only CV with no wireframes, prototypes, or sketches.
- Networking as stepping-stone hunting rather than relationship building.
- Assuming a job title means the same responsibilities at every studio.

---
name: game-ui-ux-core-principles
topic: Core UI/UX design principles for games
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 10 (pp. 155-168)"]
---
## Rules
- Balance entertainment and usability: decide when to teach, when to be playful, when to provoke emotion. WHY: games UI must sell the world and stay usable, unlike film UI or banking apps.
- Aim for "invisible UI": players intuit it without explanation. WHY: frictionless interfaces go unnoticed and feel natural.
- Establish a clear visual hierarchy: rank what players should see or do first, second, third. WHY: reduces cognitive load.
- Prioritise usability before adding flourishes. WHY: without intuitive UX the interface is worthless.
- Keep visual and interactive style consistent across fonts, colours, button layouts, iconography. WHY: familiar elements let players focus on gameplay.
- Design for a global audience: information should be digestible and interaction intuitive for anyone. WHY: broadens reach.
- Apply the three Fs: form (desirable), fit (fit for purpose), function (works as designed). WHY: all three must hold for good UX.
- Build accessibility in from the start, not as an add-on. WHY: retrofitting is costly and excludes players.
- Treat accessibility as a benefit to everyone (difficulty options, subtitles, adjustable reading time, comfortable input). WHY: there is no "average" player.
- Use personas and representation to build empathy with varied players. WHY: inclusivity increases relatability and player base.
- Understand game pillars, narrative and art aspirations, and feature designs before designing UI. WHY: solutions must reflect the game's identity and intended player impact.
- You may adjust feature design while keeping its essence, guided by user research and playtests. WHY: player fun outranks the original spec.
- Do competitor analysis at project start: capture screenshots/video of similar titles and note pros and cons. WHY: reveals trends and what works or fails.
- Review your own work with the same critical eye used in research; join playtests and ask why feedback was given. WHY: feedback only helps if you understand its cause.
- Remember games are not apps: friction, challenge and overcoming obstacles are the point. WHY: a frictionless game is a screensaver.
- UX is a team output, not one person's job; keep communication open across disciplines. WHY: great UX is the culmination of many people's work.
## Checklist
- [ ] Visual hierarchy defined for each screen
- [ ] Usability validated before decorative polish
- [ ] Style consistent across fonts, colours, buttons, icons
- [ ] Accessibility options planned from the start
- [ ] Personas cover non-average players
- [ ] Game pillars and narrative understood before UI design
- [ ] Competitor analysis documented
- [ ] Playtest feedback collected and its causes understood
## Anti-patterns
- Over-designing and removing every pain point until the game loses challenge.
- Experimental UI at the cost of a functional, accessible menu.
- Designing UI in isolation from game pillars, narrative, or feature design.
- Treating accessibility as a post-launch patch.
- Assuming your own taste equals the target player's taste ("everyone is a user, but not everyone is THE user").

---
name: ui-ux-role-expectations
topic: Role expectations and career fit in game UI/UX
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 10 (pp. 155-168)"]
---
## Rules
- Verify what a studio means by "UI" or "UX": responsibilities vary widely between studios. WHY: the same title can demand UI art, UX design, or both, and a bad fit leads to unhappiness.
- Look at portfolios of people already doing the target job and get your own portfolio reviewed by peers. WHY: the most valuable advice is specific to your work.
- Identify which part excites you most — design, art, or implementation. WHY: all need problem-solving but only one keeps you motivated long-term.
- If coming from web/app/frontend, expect to learn a game-specific design language and custom tools. WHY: game UI has its own conventions and pipelines.
- Analyse a favourite game's HUD using UX terminology in interviews. WHY: shows genuine passion and applied knowledge.
- Study established UX concepts: cognitive workload, game flow, signifiers, feedback, usability and engageability. WHY: gives a shared vocabulary and frameworks for pain points.
- Learn how to learn and stay tool-agnostic. WHY: game dev is a marathon and tools change.
- Expect a long path: it can take years and multiple adjacent roles before breaking in. WHY: patience and resilience keep you in the industry.
## Checklist
- [ ] Confirmed actual responsibilities of the target role at that studio
- [ ] Reviewed portfolios of people in that role
- [ ] Had your portfolio reviewed by peers
- [ ] Identified your preferred focus (design / art / implementation)
- [ ] Familiar with core UX terminology and frameworks
- [ ] Plan for adjacent or non-game roles as a stepping stone
## Anti-patterns
- Assuming a UI/UX title means identical duties everywhere.
- Rigidly following one design process learned from solo case studies.
- Treating a games job as a stop-gap until something better appears.
- Neglecting well-being and comparing yourself constantly to others.

> CHECK: The chapter is a collection of short interview excerpts; several named contributors (e.g. Ian Plater, Julie McConnell, Stephan Dube, François Savarimuthu, Cari Watterton, David Mariscal, Rachel Brett, Jonathan Tyler, Rami Majid, Gavin Marshall, Casia Dominguez, Braden League, Holly Hilson, Max Vizard, Georgeth Lyver, Nida Ahmad, Kylan Coats, Sarah Robinson, Edd Coates, Mary Yovina, Kemal Akay, Leah Chalkey, Jordan DeVries, Chris Johnson) are quoted only briefly. Verify whether any additional distinct advice was cut off by OCR before relying on this summary as complete.

<!-- 11 Between U and I (pp. 169-174) -->
---
name: ux-ui-invisible-design-goal
topic: Purpose of UX/UI in games
confidence: consensus
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Treat "the player never notices the UI" as the success condition: no one buys a game for its UI, so design for zero friction, not for praise.
- Make complex systems feel intuitive; make simple interactions feel polished. Both are UX/UI deliverables, not extras.
- Judge UI/UX work by player outcome (can anyone pick up a controller and play without help), not by visual novelty.
- Accept that praise for visuals/functionality is a bonus, not the target metric.
- Treat UX and UI as one intertwined discipline; do not split them into competing roles or tool camps.
## Checklist
- Can a first-time player complete the core loop without external explanation?
- Are accessibility needs (struggles, preferences, input differences) handled by default?
- Does the interface disappear during play and reappear only when needed?
## Anti-patterns
- Chasing "make it pretty" as the definition of UI work.
- Gatekeeping or arguing about which tools/methods are "real" UX vs UI instead of shipping craft.
- Designing UI to be noticed by peers rather than to serve players.

---
name: onboarding-into-studio-ux-culture
topic: Adapting to a new studio's UX maturity
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Assume studios differ wildly in UX maturity; spend the first weeks diagnosing the current before proposing change.
- Introduce new UX ideas gradually and in small increments; treat adoption itself as a UX problem to design for.
- Frame proposals around the team's existing biases and vocabulary rather than around unfamiliar UX terminology.
- Prioritise communication skill over tool mastery; communication is the highest-leverage UX/UI skill.
- Listen to understand, not to respond: people who feel understood become less defensive and more open to your ideas.
- Read non-verbal cues; confirm your message landed rather than assuming it did.
## Checklist
- Who are the decision-makers and what do they already believe about UX?
- What is the smallest first change that will succeed and build trust?
- Have I restated others' positions accurately before countering them?
- Am I dominating meetings/threads, or making space for input?
## Anti-patterns
- Arriving with a full UX overhaul and demanding immediate adoption.
- Winning arguments instead of opening minds.
- Equating loudness, speed of reply, or meeting dominance with good communication.

---
name: portfolio-first-impressions-for-ux-ui-roles
topic: Presenting yourself for UX/UI jobs
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Expect hiring teams to look at the portfolio first; a CV with no visible design effort raises doubt.
- Apply design craft to your own presentation: if your job is first impressions, your materials must demonstrate that.
- Make work stand out through clarity and quality, since the field is noisy and only genuinely strong work gets noticed.
## Checklist
- Does the portfolio show process and reasoning, not just final screens?
- Is the CV itself visually considered and consistent with the portfolio?
- Would a hiring designer call this "lovely UI" at a glance?
## Anti-patterns
- Submitting a plain, unformatted CV alongside a strong portfolio.
- Blending into the noise with generic template presentation.

---
name: kill-negativity-and-perfectionism
topic: Mindset and burnout prevention
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Treat perfectionism as a negative trait: perfect is the enemy of good; aim for progress, not perfection.
- Accept that output quality is capped by available time, resources, skills, and budget; ship within those limits.
- Fail fast: detect an unworkable approach early, cut losses, and redirect — this counters the sunk cost fallacy.
- Stop iterating once work is "right" (achieves the goal), not perfect; over-iteration becomes churn.
- Compete only with your own previous work, not with peers.
- Protect work-life balance deliberately: time with friends/family, exercise, mindfulness, and outside support.
- Focus only on what you are responsible for; trying to control everything guarantees unhappiness.
## Checklist
- Is this task blocked by a perfectionism standard I invented?
- Have I spent more than a reasonable slice of budget on an approach that isn't working?
- Does this feature meet the goal, even if it isn't flawless?
- Have I taken real rest time this week?
## Anti-patterns
- Worrying, complaining, gossiping, or assuming the worst as a default mode.
- Endless iteration on a feature that already meets its goal.
- Judging yourself by others' opinions or past failures.

---
name: leaving-comfort-zone-80-20-growth
topic: Deliberate skill growth
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Stay slightly uncomfortable to grow; imposter syndrome is a signal you are outside your comfort zone, not a verdict on your ability.
- Apply the 80:20 rule: ~80% of work on familiar skills, ~20% on new ones.
- Keep goals achievable; overwhelming yourself damages self-esteem and increases anxiety.
- Document growth continuously (e.g. a daily screenshot or video) and review it periodically to see progress.
- Measure success by proficiency demonstrated and by delivery, not by hours spent or energy burned.
- Ask for help and stay open to being wrong; being right is less valuable than learning.
## Checklist
- What is my 20% new-skill investment this month?
- Are my current goals achievable at my present skill level?
- Have I reviewed my growth log recently?
- Am I innovating, or coasting?
## Anti-patterns
- "Always play to your strengths" as a permanent strategy — it locks in your weaknesses.
- Setting limits on yourself and then never exceeding them.
- Fixating on promotion instead of on the work and its value.

---
name: self-review-and-professional-conduct
topic: Self-assessment and workplace behaviour
confidence: opinion
sources: ["The Pocket Mentor for Video Game UX UI, Simon Brewer, ch. 11 (pp. 169-174)"]
---
## Rules
- Run a periodic honest self-review against four questions: rapport/relationships, supportiveness/harmony, innovating vs coasting, advocating for self and others.
- Value yourself by the value you bring, not by your job title; recognition follows contribution.
- Accept that you only control yourself and your actions; treat others' opinions and your past failures as lessons, not definitions.
- Avoid people who belittle others or pull you down; treat others as you want to be treated.
- Act decisively on problems instead of making excuses; do today what can be done today.
- Take responsibility for changing conditions you don't accept, rather than only complaining about them.
- Be kind by default, even when others are not.
## Checklist
- Do I have good rapport and working relationships right now?
- Am I supporting others and working in harmony with the team?
- Am I advocating for myself and for others?
- Is there a problem I'm avoiding that needs a direct decision?
## Anti-patterns
- Procrastinating on important goals.
- Insisting on being right instead of being open to learning.
- Letting minor setbacks or small opportunities be dismissed as unimportant.
- Staying in a toxic environment and absorbing its negativity.
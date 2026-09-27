# {{game_name}}: game design document (source of truth for the agents)

> If this file and the code disagree, this file wins. If a rule needs to change, `game-designer` changes it here first.
> This is a skeleton. `game-designer` fills in the real rules, numbers and curves as the MVP takes shape — nothing here should be treated as final until they do.

## 1. Concept

{{pitch}}

- Genre / camera: {{genre}}
- Core loop (verbs): {{core_loop}}
- Platforms: {{platforms}}
- Session length: {{session_length}}
- Engine: Godot 4.3+ with GDScript.

## 2. Loop

TBD — `game-designer` diagrams the moment-to-moment loop here (what the player does, in what order, and what brings them back to the start of it).

## 3. Rules and systems

TBD — one subsection per system (movement, scoring, resources, enemies, progression, whatever the game needs). Every number quoted in code must trace back to a line here and a matching `Resource` in `data/`.

## 4. Progression / difficulty curve

TBD.

## 5. Economy

TBD — only if the game has one (currency, costs, rewards).

## 6. Art direction

{{art_direction}}

Palette and shape language go here once `technical-artist` defines them for greybox.

## 7. Narrative

{{narrative}}

## 8. Maps / levels

{{maps}}

## 9. Audio

{{audio}}

## 10. Languages

{{languages}}

## 11. Out of scope

{{out_of_scope}}

Nothing outside this MVP gets added without the user approving it first.

## 12. First checkpoint

{{first_checkpoint}}

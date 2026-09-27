from godot_kit_mcp import knowledge

PALETTES = """---
name: pixel-art-palettes
topic: pixel-art
confidence: consensus
sources: ["Pixel Logic, Michael Azzi, ch. 3 (pp. 40-52)"]
---
## Rules
- Use 3-5 shades per material ramp. WHY: fewer shades read clearly at small sizes.
## Checklist
- [ ] Silhouette readable in black
"""

CAMERA = """---
name: camera-look-ahead
topic: game-feel
confidence: opinion
---
## Rules
- Offset the camera toward the velocity by 20-30% of the screen. WHY: players see what comes.
"""


def _cards(tmp_path):
    (tmp_path / "pixel-art").mkdir()
    (tmp_path / "game-feel").mkdir()
    (tmp_path / "pixel-art/pixel-art-palettes.md").write_text(PALETTES, encoding="utf-8")
    (tmp_path / "game-feel/camera-look-ahead.md").write_text(CAMERA, encoding="utf-8")
    return knowledge.load_cards(tmp_path)


def test_parse_card():
    meta, body = knowledge.parse_card(PALETTES)
    assert meta["name"] == "pixel-art-palettes" and meta["topic"] == "pixel-art"
    assert body.startswith("## Rules")
    assert knowledge.parse_card("no front matter") == ({}, "no front matter")


def test_search_ranks_and_previews(tmp_path):
    hits = knowledge.search(_cards(tmp_path), "palette shades")
    assert hits[0]["name"] == "pixel-art-palettes"
    assert hits[0]["preview"].startswith("- Use 3-5 shades")
    assert len(hits) == 1


def test_search_topic_filter_and_empty(tmp_path):
    cards = _cards(tmp_path)
    assert knowledge.search(cards, "camera", topic="pixel-art") == []
    assert [h["name"] for h in knowledge.search(cards, "camera", topic="game-feel")] == ["camera-look-ahead"]
    assert knowledge.search(cards, "   ") == []


def test_get(tmp_path):
    cards = _cards(tmp_path)
    assert knowledge.get(cards, "camera-look-ahead").confidence == "opinion"
    assert knowledge.get(cards, "missing") is None

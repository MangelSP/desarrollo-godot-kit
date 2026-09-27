"""Keyword search over knowledge/cards (distilled, reviewed game-dev rules)."""

import re
from dataclasses import dataclass
from pathlib import Path

from . import config

WORD_RE = re.compile(r"[a-z0-9]{2,}")


@dataclass
class Card:
    name: str
    topic: str
    confidence: str
    path: Path
    body: str


def parse_card(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            meta = {}
            for line in lines[1:end]:
                key, sep, value = line.partition(":")
                if sep:
                    meta[key.strip()] = value.strip()
            return meta, "\n".join(lines[end + 1:]).lstrip("\n")
    return {}, text


def load_cards(root: Path) -> list[Card]:
    cards = []
    for path in sorted(root.rglob("*.md")):
        meta, body = parse_card(path.read_text(encoding="utf-8"))
        cards.append(Card(meta.get("name", path.stem), meta.get("topic", path.parent.name),
                          meta.get("confidence", ""), path, body))
    return cards


def _preview(body: str) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.lower().startswith("## rules") and i + 1 < len(lines):
            return lines[i + 1][:200]
    return (lines[0] if lines else "")[:200]


def search(cards: list[Card], query: str, topic: str = "", limit: int = 10) -> list[dict]:
    terms = set(WORD_RE.findall(query.lower()))
    if not terms:
        return []
    hits = []
    for card in cards:
        if topic and card.topic != topic:
            continue
        name, top, body = card.name.lower(), card.topic.lower(), card.body.lower()
        score = sum(3 * name.count(t) + 2 * top.count(t) + min(body.count(t), 5) for t in terms)
        if score:
            hits.append({"name": card.name, "topic": card.topic, "confidence": card.confidence,
                         "path": str(card.path), "preview": _preview(card.body), "score": score})
    hits.sort(key=lambda h: (-h["score"], h["name"]))
    return hits[:limit]


def get(cards: list[Card], name: str) -> Card | None:
    return next((c for c in cards if c.name == name), None)


def default_root() -> Path | None:
    kit = config.kit_root()
    folder = kit / "knowledge" / "cards" if kit else None
    return folder if folder and folder.is_dir() else None

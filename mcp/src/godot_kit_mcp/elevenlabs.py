"""ElevenLabs sound effects and music, guarded by a credit reserve and a ledger."""

import json
import math
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from . import config
from .result import fail, ok

API = "https://api.elevenlabs.io"
SFX_CREDITS_PER_S = 40
MUSIC_CREDITS_PER_S = 7  # measured 2026-09-25: 288 credits per ~42 s track
PENDING_WINDOW = timedelta(seconds=120)  # the balance takes ~60 s to show a charge
LEDGER = "docs/audio-ledger.md"
LEDGER_HEADER = (
    "# ElevenLabs ledger\n\n"
    "| time (UTC) | kind | file | seconds | estimate | balance before |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)
LIMITS = {"sfx": (0.5, 30.0), "music": (3.0, 300.0)}
TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

Http = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]


def default_http(method: str, url: str, headers: dict[str, str], body: bytes | None) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def estimate_sfx(seconds: float) -> int:
    return math.ceil(SFX_CREDITS_PER_S * seconds)


def estimate_music(seconds: float) -> int:
    return math.ceil(MUSIC_CREDITS_PER_S * seconds)


def balance(api_key: str, http: Http = default_http) -> int:
    status, body = http("GET", f"{API}/v1/user/subscription", {"xi-api-key": api_key}, None)
    if status != 200:
        raise RuntimeError(f"balance request failed with HTTP {status} (the key needs the user_read permission)")
    data = json.loads(body)
    return int(data["character_limit"]) - int(data["character_count"])


def pending_estimates(ledger_text: str, now: datetime) -> int:
    total = 0
    for line in ledger_text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            continue
        try:
            when = datetime.strptime(cells[0], TIME_FMT).replace(tzinfo=UTC)
            estimate = int(cells[4])
        except ValueError:
            continue
        if now - when < PENDING_WINDOW:
            total += estimate
    return total


def _request(kind: str, prompt: str, seconds: float, loop: bool) -> tuple[str, dict]:
    if kind == "sfx":
        return f"{API}/v1/sound-generation?output_format=mp3_44100_128", {
            "text": prompt, "duration_seconds": seconds, "loop": loop,
            "prompt_influence": 0.6, "model_id": "eleven_text_to_sound_v2",
        }
    return f"{API}/v1/music?output_format=mp3_44100_128", {
        "prompt": prompt, "music_length_ms": int(seconds * 1000),
        "model_id": "music_v1", "force_instrumental": True,
    }


def generate(kind: str, *, root: Path, out: str, prompt: str, seconds: float, reserve: int,
             api_key: str | None, loop: bool = False, http: Http = default_http,
             now: datetime | None = None) -> dict:
    if kind not in LIMITS:
        return fail(f"kind must be 'sfx' or 'music', got {kind!r}")
    low, high = LIMITS[kind]
    if not low <= seconds <= high:
        return fail(f"{kind} duration must be between {low:g} and {high:g} seconds")
    if not api_key:
        return fail("Set the ELEVENLABS_API_KEY environment variable (never put the key in a file).")
    try:
        target = config.resolve_inside(root, out)
    except ValueError as exc:
        return fail(str(exc))
    now = now or datetime.now(UTC)
    estimate = estimate_sfx(seconds) if kind == "sfx" else estimate_music(seconds)
    ledger_path = root / LEDGER
    ledger_text = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    before = balance(api_key, http)
    available = before - pending_estimates(ledger_text, now)
    if available - estimate < reserve:
        return fail(f"Refused: {available} credits available, this costs ~{estimate}, "
                    f"and the reserve is {reserve}.", balance=before, estimate=estimate)
    url, payload = _request(kind, prompt, seconds, loop)
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    status, body = http("POST", url, headers, json.dumps(payload).encode())
    if status != 200:
        return fail(f"ElevenLabs returned HTTP {status}: {body[:300].decode('utf-8', 'replace')}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    rel = target.relative_to(root.resolve()).as_posix()
    row = f"| {now.strftime(TIME_FMT)} | {kind} | {rel} | {seconds} | {estimate} | {before} |\n"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text((ledger_text or LEDGER_HEADER) + row, encoding="utf-8")
    return ok(f"Generated {rel} (~{estimate} credits, balance was {before})",
              path=str(target), estimate=estimate, balance_before=before)

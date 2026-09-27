import json
from datetime import UTC, datetime, timedelta

from godot_kit_mcp import elevenlabs

KEY = "sk_test_secret_value"
NOW = datetime(2026, 9, 25, 13, 0, 0, tzinfo=UTC)


class FakeHttp:
    def __init__(self, balances, status=200):
        self.balances, self.status, self.calls = list(balances), status, []

    def __call__(self, method, url, headers, body):
        self.calls.append({"method": method, "url": url, "headers": headers,
                           "json": json.loads(body) if body else None})
        if url.endswith("/v1/user/subscription"):
            left = self.balances.pop(0)
            return 200, json.dumps({"character_limit": 10000, "character_count": 10000 - left}).encode()
        return self.status, b"ID3-fake-audio"


def _gen(project, http, **kw):
    args = dict(root=project, out="assets/audio/sfx/horn.mp3", prompt="scooter horn, two short beeps",
                seconds=1.0, reserve=1500, api_key=KEY, http=http, now=NOW)
    args.update(kw)
    return elevenlabs.generate("sfx", **args)


def test_estimates():
    assert elevenlabs.estimate_sfx(1.2) == 48
    assert elevenlabs.estimate_music(42) == 294


def test_generates_writes_file_and_ledger(project):
    http = FakeHttp([4444])
    r = _gen(project, http)
    assert r["ok"], r
    assert (project / "assets/audio/sfx/horn.mp3").read_bytes() == b"ID3-fake-audio"
    ledger = (project / "docs/audio-ledger.md").read_text(encoding="utf-8")
    assert "| 2026-09-25T13:00:00Z | sfx | assets/audio/sfx/horn.mp3 | 1.0 | 40 | 4444 |" in ledger
    gen = http.calls[1]
    assert gen["url"].startswith("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128")
    assert gen["json"]["duration_seconds"] == 1.0 and gen["json"]["model_id"] == "eleven_text_to_sound_v2"
    assert gen["headers"]["xi-api-key"] == KEY
    assert KEY not in ledger and KEY not in json.dumps(r)


def test_refuses_below_reserve_without_calling_generation(project):
    http = FakeHttp([1520])
    r = _gen(project, http)
    assert r["ok"] is False and "reserve" in r["summary"]
    assert len(http.calls) == 1 and not (project / "assets/audio/sfx/horn.mp3").exists()


def test_recent_charges_count_against_balance(project):
    http = FakeHttp([1560, 1560])  # the API has not shown the first charge yet: 1560 - 40 pending - 40 < 1500
    assert _gen(project, http)["ok"]
    r = _gen(project, http, out="assets/audio/sfx/horn2.mp3", now=NOW + timedelta(seconds=30))
    assert r["ok"] is False and "reserve" in r["summary"]


def test_old_ledger_rows_do_not_count(project):
    http = FakeHttp([4444, 4404])
    assert _gen(project, http)["ok"]
    later = _gen(project, http, out="assets/audio/sfx/b.mp3", now=NOW + timedelta(minutes=5))
    assert later["ok"]


def test_missing_key_and_api_error(project):
    assert "ELEVENLABS_API_KEY" in _gen(project, FakeHttp([4444]), api_key=None)["summary"]
    r = _gen(project, FakeHttp([4444], status=401))
    assert r["ok"] is False and not (project / "docs/audio-ledger.md").exists()


def test_music_request_shape(project):
    http = FakeHttp([4444])
    r = elevenlabs.generate("music", root=project, out="assets/audio/music/a.mp3", prompt="instrumental merengue",
                            seconds=42, reserve=1500, api_key=KEY, http=http, now=NOW)
    assert r["ok"] and r["estimate"] == 294
    body = http.calls[1]["json"]
    assert body == {"prompt": "instrumental merengue", "music_length_ms": 42000,
                    "model_id": "music_v1", "force_instrumental": True}


def test_duration_limits(project):
    assert _gen(project, FakeHttp([4444]), seconds=31)["ok"] is False
    assert _gen(project, FakeHttp([4444]), seconds=0.2)["ok"] is False

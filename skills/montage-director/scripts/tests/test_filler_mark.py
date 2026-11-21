import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from filler_mark import flag_segments

SCRIPT = Path(__file__).resolve().parents[1] / "filler_mark.py"


def test_filler_word_flagged():
    segs = [{"id": 0, "start": 0.0, "end": 1.0, "text": "Ем, я хотів сказати"}]
    flags = flag_segments(segs)

    assert len(flags) == 1
    assert flags[0]["reason"] == "FILLER"
    assert flags[0]["segment_id"] == 0


def test_repeat_flagged():
    segs = [
        {"id": 0, "start": 0.0, "end": 1.0, "text": "Ми йдемо додому"},
        {"id": 1, "start": 1.0, "end": 2.0, "text": "ми йдемо додому!"},
    ]
    flags = flag_segments(segs)

    assert any(f["reason"] == "REPEAT" and f["segment_id"] == 1 for f in flags)


def test_clean_segments_no_flags():
    segs = [{"id": 0, "start": 0.0, "end": 1.0, "text": "Це повна змістовна фраза."}]
    assert flag_segments(segs) == []


def test_input_not_mutated():
    segs = [{"id": 0, "start": 0.0, "end": 1.0, "text": "Ем..."}]
    before = [dict(s) for s in segs]
    flag_segments(segs)
    assert segs == before


def test_cli_creates_sidecar_and_keeps_original(tmp_path):
    src = tmp_path / "transcript.json"
    payload = {
        "segments": [
            {"id": 0, "start": 0.0, "end": 1.0, "text": "Ем, починаємо"},
            {"id": 1, "start": 1.0, "end": 2.0, "text": "Це корисна фраза"},
        ]
    }
    src.write_text(json.dumps(payload), encoding="utf-8")
    before = src.read_text(encoding="utf-8")

    subprocess.run([sys.executable, str(SCRIPT), str(src)], check=True, capture_output=True)

    assert src.read_text(encoding="utf-8") == before
    sidecar = tmp_path / "transcript.flags.json"
    assert sidecar.exists()
    flags = json.loads(sidecar.read_text(encoding="utf-8"))
    assert any(f["reason"] == "FILLER" for f in flags)

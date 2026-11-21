import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inventory import probe_to_record

SCRIPT = Path(__file__).resolve().parents[1] / "inventory.py"


def test_probe_to_record_video_fixture():
    probe = {
        "format": {"duration": "12.500000", "size": "1024000"},
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "r_frame_rate": "30000/1001",
            },
            {"codec_type": "audio", "codec_name": "aac", "channels": 2},
        ],
    }
    rec = probe_to_record("clip.mp4", probe)

    assert rec["path"] == "clip.mp4"
    assert rec["duration"] == 12.5
    assert rec["width"] == 1920
    assert rec["height"] == 1080
    assert rec["fps"] == 29.97
    assert rec["has_audio"] is True
    assert rec["audio_channels"] == 2
    assert rec["video_codec"] == "h264"


def test_probe_to_record_audio_only():
    probe = {
        "format": {"duration": "3.000000"},
        "streams": [{"codec_type": "audio", "codec_name": "pcm_s16le", "channels": 1}],
    }
    rec = probe_to_record("voice.wav", probe)

    assert rec["width"] is None
    assert rec["height"] is None
    assert rec["fps"] is None
    assert rec["has_audio"] is True
    assert rec["audio_channels"] == 1


@pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg/ffprobe not available",
)
def test_cli_inventory_on_generated_fixture(tmp_path):
    media = tmp_path / "clip.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=blue:s=320x240:d=0.5",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=0.5",
            "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "aac",
            str(media),
        ],
        check=True,
        capture_output=True,
    )

    out = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(out.stdout)

    assert len(data["files"]) == 1
    record = data["files"][0]
    assert record["duration"] > 0
    assert record["width"] == 320
    assert record["height"] == 240
    assert record["has_audio"] is True

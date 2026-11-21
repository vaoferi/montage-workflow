import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from doctor import editor_definitions, render_report


def test_render_report_lists_tools_and_hints():
    report = {
        "tools": {
            "ffmpeg": {"path": "/usr/bin/ffmpeg", "version": "7.1"},
            "faster_whisper": {"path": None, "version": None},
        },
        "editors": [],
        "os": "linux",
    }
    text = render_report(report)

    assert "ffmpeg" in text
    assert "/usr/bin/ffmpeg" in text
    assert "faster-whisper" in text
    assert "pip install faster-whisper" in text
    assert "none found" in text


def test_editor_definitions_macos_contains_resolve():
    definitions = editor_definitions("darwin")
    names = [c["name"] for c in definitions]

    assert "DaVinci Resolve" in names
    assert "Final Cut Pro" in names


def test_editor_definitions_windows_contains_resolve():
    definitions = editor_definitions("win32")
    names = [c["name"] for c in definitions]

    assert "DaVinci Resolve" in names
    assert "Adobe Premiere Pro" in names

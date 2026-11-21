#!/usr/bin/env python3
"""Environment doctor: tools, transcriber, installed editors. Python 3.9+, stdlib only."""
import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

SYSTEM_TOOLS = ("ffmpeg", "ffprobe", "exiftool")

PIP_TOOLS = {
    "faster_whisper": "pip install faster-whisper",
    "whisper": "pip install openai-whisper",
}

EDITOR_PATHS = {
    "darwin": {
        "DaVinci Resolve": ["/Applications/DaVinci Resolve/DaVinci Resolve.app"],
        "Adobe Premiere Pro": [
            "/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app",
            "/Applications/Adobe Premiere Pro 2025/Adobe Premiere Pro 2025.app",
        ],
        "Final Cut Pro": ["/Applications/Final Cut Pro.app"],
        "FilmCraft": ["/Applications/FilmCraft.app"],
    },
    "linux": {
        "DaVinci Resolve": ["/opt/resolve/bin/resolve", "/usr/bin/resolve"],
        "FilmCraft": ["/usr/bin/filmcraft"],
    },
    "win32": {
        "DaVinci Resolve": [r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"],
        "Adobe Premiere Pro": [
            r"C:\Program Files\Adobe\Adobe Premiere Pro 2026\Adobe Premiere Pro.exe",
            r"C:\Program Files\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe",
        ],
    },
}


def tool_status(name):
    path = shutil.which(name)
    return {"path": path, "version": "installed" if path else None}


def module_status(module):
    installed = importlib.util.find_spec(module) is not None
    return {"path": "python-module" if installed else None, "version": "installed" if installed else None}


def editor_definitions(os_name):
    return [
        {"name": name, "path": path}
        for name, paths in EDITOR_PATHS.get(os_name, {}).items()
        for path in paths
    ]


def editor_candidates(os_name):
    return [c for c in editor_definitions(os_name) if Path(c["path"]).exists()]


def build_report(os_name=None):
    os_name = os_name or sys.platform
    tools = {name: tool_status(name) for name in SYSTEM_TOOLS}
    tools.update({name: module_status(name) for name in PIP_TOOLS})
    return {"tools": tools, "editors": editor_candidates(os_name), "os": os_name}


def render_report(report):
    lines = [f"os: {report['os']}", "tools:"]
    for name, status in report["tools"].items():
        display = name.replace("_", "-")
        if status["path"]:
            lines.append(f"  {display}: {status['path']}")
        else:
            hint = PIP_TOOLS.get(name, "install via system package manager (confirmation required)")
            lines.append(f"  {display}: NOT INSTALLED → {hint}")
    lines.append("editors:")
    if report["editors"]:
        for editor in report["editors"]:
            lines.append(f"  {editor['name']}: {editor['path']}")
    else:
        lines.append("  none found")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print(render_report(report))


if __name__ == "__main__":
    sys.exit(main())

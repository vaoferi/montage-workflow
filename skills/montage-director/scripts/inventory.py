"""Media inventory via ffprobe. Python 3.9+, stdlib only."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

MEDIA_EXTENSIONS = {
    ".mp4", ".mov", ".mkv", ".avi", ".mxf", ".mts", ".m4v", ".webm",
    ".wav", ".mp3", ".aiff", ".aif", ".flac", ".m4a",
    ".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff",
}


def probe_to_record(path, probe):
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)

    fps = None
    if video and video.get("r_frame_rate"):
        rate = video["r_frame_rate"]
        try:
            if "/" in rate:
                num, den = rate.split("/")
                fps = round(int(num) / int(den), 2) if int(den) else None
            else:
                fps = float(rate)
        except (ValueError, ZeroDivisionError):
            fps = None

    return {
        "path": path,
        "size_bytes": int(fmt["size"]) if fmt.get("size") else None,
        "duration": float(fmt["duration"]) if fmt.get("duration") else None,
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "fps": fps,
        "video_codec": video.get("codec_name") if video else None,
        "has_audio": audio is not None,
        "audio_channels": audio.get("channels") if audio else None,
    }


def probe_file(path):
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_format", "-show_streams",
            "-of", "json", str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def collect(root):
    root = Path(root)
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        try:
            records.append(probe_to_record(str(path), probe_file(path)))
        except Exception as exc:
            records.append({"path": str(path), "error": str(exc)})
    return {"root": str(root), "files": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="Directory to scan recursively")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    report = collect(args.directory)
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print(f"Found {len(report['files'])} media files under {report['root']}")
        for record in report["files"]:
            if "error" in record:
                print(f"  ERROR {record['path']}: {record['error']}")
            else:
                print(
                    f"  {record['path']}: {record['width']}x{record['height']} "
                    f"{record['fps']}fps {record['duration']}s "
                    f"audio={'yes' if record['has_audio'] else 'no'}"
                )


if __name__ == "__main__":
    sys.exit(main())

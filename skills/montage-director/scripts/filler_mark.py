#!/usr/bin/env python3
"""Flag repeats and filler words in a transcript. Writes sidecar, never mutates input.

Input: whisper-style JSON {"segments": [{"id", "start", "end", "text"}, ...]}
Output: <input>.flags.json — list of {segment_id, start, end, reason, detail}.
Python 3.9+, stdlib only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FILLERS = (
    "ем", "ее", "мм", "аа", "ээ", "ер", "хм",
    "uh", "um", "erm", "hmm", "mm", "ah", "eh",
)
FILLER_RE = re.compile(
    r"(?<![\w])(" + "|".join(re.escape(f) for f in FILLERS) + r")(?![\w])",
    re.IGNORECASE,
)


def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def flag_segments(segments):
    flags = []
    previous = None
    for segment in segments:
        text = segment.get("text", "")
        normalized = normalize(text)
        if normalized and normalized == previous:
            flags.append({
                "segment_id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "reason": "REPEAT",
                "detail": "Same normalized text as previous segment",
            })
        match = FILLER_RE.search(text)
        if match:
            flags.append({
                "segment_id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "reason": "FILLER",
                "detail": f"Filler word: {match.group(0)}",
            })
        previous = normalized or previous
    return flags


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", help="Path to transcript JSON")
    args = parser.parse_args()

    source = Path(args.transcript)
    payload = json.loads(source.read_text(encoding="utf-8"))
    segments = payload["segments"] if isinstance(payload, dict) else payload

    flags = flag_segments(segments)
    sidecar = source.with_suffix(".flags.json")
    sidecar.write_text(json.dumps(flags, ensure_ascii=False, indent=2), encoding="utf-8")

    by_reason = {}
    for flag in flags:
        by_reason[flag["reason"]] = by_reason.get(flag["reason"], 0) + 1
    summary = ", ".join(f"{reason}={count}" for reason, count in sorted(by_reason.items()))
    print(f"Wrote {sidecar} ({len(flags)} flags{': ' + summary if summary else ''})")


if __name__ == "__main__":
    sys.exit(main())

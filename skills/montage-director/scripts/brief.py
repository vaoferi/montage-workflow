#!/usr/bin/env python3
"""Assemble the whole canon into one briefing digest. Python 3.9+, stdlib only.

Usage:
    brief.py [--root REPO] [--out FILE]

Resolution order for the repo root: --root, MONTAGE_WORKFLOW_ROOT, walk up
from CWD until knowledge/canon exists. The digest is the mandatory reading
for any montage session; skipping it means working without the owner's rules.
"""
import argparse
import os
import sys
from pathlib import Path

CANON_REL = Path("knowledge") / "canon"


def find_canon_root(start):
    start = Path(start).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / CANON_REL / "index.md").exists():
            return candidate
    return None


def resolve_root(explicit=None):
    if explicit:
        root = Path(explicit).resolve()
        return root if (root / CANON_REL / "index.md").exists() else None
    env_root = os.environ.get("MONTAGE_WORKFLOW_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        return root if (root / CANON_REL / "index.md").exists() else None
    return find_canon_root(Path.cwd())


def build_digest(canon_root):
    canon_root = Path(canon_root)
    parts = []
    index = canon_root / "index.md"
    if index.exists():
        parts.append(index.read_text(encoding="utf-8").strip())
    for path in sorted(canon_root.rglob("*.md")):
        if path.name in ("index.md", "CHANGELOG.md") or path.name.startswith("._"):
            continue
        rel = path.relative_to(canon_root).as_posix()
        parts.append(f"# canon/{rel}\n\n{path.read_text(encoding='utf-8').strip()}")
    return "\n\n---\n\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Repository root containing knowledge/canon")
    parser.add_argument("--out", help="Write digest to this file instead of stdout")
    args = parser.parse_args()

    root = resolve_root(args.root)
    if root is None:
        print(
            "ERROR: knowledge/canon not found. Set MONTAGE_WORKFLOW_ROOT "
            "or clone vaoferi/montage-workflow and pass --root.",
            file=sys.stderr,
        )
        return 1

    digest = build_digest(root / CANON_REL)
    if args.out:
        out = Path(args.out)
        out.write_text(digest + "\n", encoding="utf-8")
        print(f"Canon brief written to {out} ({len(digest.splitlines())} lines)")
    else:
        print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

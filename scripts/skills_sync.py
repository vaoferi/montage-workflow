#!/usr/bin/env python3
"""Sync external Agent Skills from official repos into a local pool.

Clones missing repos and updates existing ones with a shallow fetch, then
records the exact commit SHA of every repo in a lock file (provenance).
Python 3.9+, stdlib only.

Usage:
    skills_sync.py [--registry FILE] [--pool DIR] [--lock FILE]
                   [--only owner/name,...] [--json]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_POOL = Path.home() / ".qoder" / "skill-pool"


def repo_dir_name(name):
    return name.replace("/", "__")


def run_git(args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    )


def sync_repo(entry, pool_dir):
    name = entry["name"]
    url = entry["url"]
    target = Path(pool_dir) / repo_dir_name(name)
    if target.exists():
        if target.is_symlink() or not (target / ".git").is_dir():
            raise ValueError("Pool target is not a managed clone: " + name)
        actual = run_git(["remote", "get-url", "origin"], cwd=target).stdout.strip()
        if actual != url:
            raise ValueError("Pool origin mismatch: " + name)
        if run_git(["status", "--porcelain", "--untracked-files=all"], cwd=target).stdout.strip():
            raise ValueError("Dirty pool checkout; preserve local changes: " + name)
        run_git(["fetch", "--depth", "1", "origin", "HEAD"], cwd=target)
        # Preserve any local branch instead of reset --hard. Review fetched SHA before executing.
        run_git(["checkout", "--detach", "FETCH_HEAD"], cwd=target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target)],
            check=True,
            capture_output=True,
            text=True,
        )
    sha = run_git(["rev-parse", "HEAD"], cwd=target).stdout.strip()
    return {"name": name, "url": url, "sha": sha, "path": str(target)}


def sync_all(registry_path, pool_dir, lock_path, only=None):
    registry = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    repos = registry.get("repos", [])
    if only:
        wanted = set(only)
        unknown = wanted - {r["name"] for r in repos}
        if unknown:
            raise ValueError("Unknown registry entries: " + ", ".join(sorted(unknown)))
        repos = [r for r in repos if r["name"] in wanted]
    else:
        repos = [r for r in repos if not r.get("optional", False)]
    results = [sync_repo(entry, pool_dir) for entry in repos]
    lock_path = Path(lock_path)
    previous = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {"repos": []}
    merged = {r["name"]: r for r in previous.get("repos", [])}
    merged.update({r["name"]: r for r in results})
    lock = {"repos": list(merged.values())}
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return lock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="skills/external/registry.json")
    parser.add_argument("--pool", default=str(DEFAULT_POOL))
    parser.add_argument("--lock", default="skills/external/lock.json")
    parser.add_argument("--only", help="Comma-separated repo names, e.g. owner/name")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    only = [n.strip() for n in args.only.split(",")] if args.only else None
    try:
        lock = sync_all(args.registry, args.pool, args.lock, only=only)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(lock, ensure_ascii=False))
    else:
        for repo in lock["repos"]:
            print(f"{repo['name']}: {repo['sha'][:12]} -> {repo['path']}")
        print(f"Lock written to {args.lock}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Read-only Git chronology for a weekly website showcase. No checkout, network, or writes.
Commit metadata is evidence of history, not of deployment or user benefit.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

def git(repo, *args, optional=False):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=45)
    if p.returncode:
        if optional:
            return None
        raise RuntimeError("git " + args[0] + " failed (" + str(p.returncode) + ")")
    return p.stdout.strip()

def date(value):
    d = dt.datetime.fromisoformat(value)
    if d.tzinfo is None:
        raise ValueError("Timestamp must have explicit UTC offset")
    return d

def sha(repo, ref):
    if not ref or ref.startswith("-"):
        raise ValueError("Invalid ref")
    value = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
    if not re.fullmatch(r"[0-9a-f]{40,64}", value):
        raise ValueError("Invalid commit")
    return value

def collect(repo, start, end, current="HEAD", baseline=None):
    start, end = date(start), date(end)
    if start >= end:
        raise ValueError("Start must precede end (exclusive)")
    tip = sha(repo, current)
    # First-parent traversal avoids treating merged feature branch timestamps as release dates.
    rows = git(repo, "log", "--first-parent", "--format=%H%x09%cI", tip).splitlines()
    commits = []
    inferred_base = None
    for row in rows:
        h, stamp = row.split("\t", 1)
        when = date(stamp)
        if start <= when < end:
            commits.append({"sha": h, "committed_at": stamp})
        if when < start and inferred_base is None:
            inferred_base = h
    base = sha(repo, baseline) if baseline else inferred_base
    changes = None
    if base:
        # Count only; raw filenames, diffs and commit messages can contain private information.
        counts = git(repo, "diff", "--shortstat", base, tip)
        changes = counts or "no tracked changes between selected revisions"
    tip_stamp = git(repo, "show", "-s", "--format=%cI", tip)
    warnings = ["Git chronology is not deployment evidence; verify deploy/source artifacts separately."]
    if date(tip_stamp) >= end:
        warnings.append("Selected current revision is outside the requested time window; choose an as-of-end ref or explain.")
    if not base:
        warnings.append("No pre-window ancestor found; obtain authentic external baseline or report missing.")
    if baseline:
        p = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", base, tip],
                           capture_output=True, timeout=45)
        if p.returncode != 0:
            warnings.append("Explicit baseline is not a confirmed ancestor; verify comparison provenance.")
    if git(repo, "status", "--porcelain", "--untracked-files=no"):
        warnings.append("Tracked working tree has local changes; selected commit does not represent them.")
    return {"period":{"start_inclusive":start.isoformat(),"end_exclusive":end.isoformat()},
            "current_sha":tip,"current_committed_at":tip_stamp,
            "baseline_sha":base,"baseline_method":"explicit" if baseline else "first-parent-pre-window",
            "commits_newest_first":commits,"tracked_diff_summary":changes,
            "deployment_status":"unverified","warnings":warnings}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--start", required=True, help="ISO datetime with offset")
    p.add_argument("--end", required=True, help="Exclusive ISO datetime with offset")
    p.add_argument("--current", default="HEAD")
    p.add_argument("--baseline")
    a = p.parse_args()
    try:
        print(json.dumps(collect(a.repo,a.start,a.end,a.current,a.baseline), indent=2))
        return 0
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as e:
        print("BLOCKED: " + str(e), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

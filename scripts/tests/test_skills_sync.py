import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skills_sync import sync_all

SCRIPT = Path(__file__).resolve().parents[1] / "skills_sync.py"


def git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def make_remote(path: Path, marker: str):
    path.mkdir(parents=True)
    git(["init", "-b", "main"], cwd=path)
    (path / "SKILL.md").write_text(marker, encoding="utf-8")
    git(["add", "."], cwd=path)
    git(["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "init"], cwd=path)


def write_registry(path: Path, remote: Path):
    path.write_text(json.dumps({
        "repos": [{"name": "owner/demo", "url": str(remote)}]
    }), encoding="utf-8")


def test_clone_then_update(tmp_path):
    remote = tmp_path / "remote"
    make_remote(remote, "v1")

    registry = tmp_path / "registry.json"
    write_registry(registry, remote)
    pool = tmp_path / "pool"
    lock = tmp_path / "lock.json"

    result = sync_all(registry, pool, lock)
    assert result["repos"][0]["name"] == "owner/demo"
    sha1 = result["repos"][0]["sha"]
    assert len(sha1) == 40
    cloned = pool / "owner__demo" / "SKILL.md"
    assert cloned.read_text(encoding="utf-8") == "v1"

    (remote / "SKILL.md").write_text("v2", encoding="utf-8")
    git(["add", "."], cwd=remote)
    git(["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "v2"], cwd=remote)

    result2 = sync_all(registry, pool, lock)
    assert result2["repos"][0]["sha"] != sha1
    assert cloned.read_text(encoding="utf-8") == "v2"
    assert json.loads(lock.read_text(encoding="utf-8"))["repos"][0]["sha"] == result2["repos"][0]["sha"]


def test_only_filter(tmp_path):
    remote_a = tmp_path / "a"
    remote_b = tmp_path / "b"
    make_remote(remote_a, "a")
    make_remote(remote_b, "b")
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"repos": [
        {"name": "owner/a", "url": str(remote_a)},
        {"name": "owner/b", "url": str(remote_b)},
    ]}), encoding="utf-8")

    result = sync_all(registry, tmp_path / "pool", tmp_path / "lock.json", only=["owner/a"])
    names = [r["name"] for r in result["repos"]]
    assert names == ["owner/a"]


@pytest.mark.skipif(
    subprocess.run(["git", "--version"], capture_output=True).returncode != 0,
    reason="git not available",
)
def test_cli_smoke(tmp_path):
    remote = tmp_path / "remote"
    make_remote(remote, "cli")
    registry = tmp_path / "registry.json"
    write_registry(registry, remote)

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--registry", str(registry),
         "--pool", str(tmp_path / "pool"), "--lock", str(tmp_path / "lock.json"), "--json"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(proc.stdout)
    assert data["repos"][0]["name"] == "owner/demo"

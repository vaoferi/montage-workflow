import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from brief import build_digest, find_canon_root

SCRIPT = Path(__file__).resolve().parents[1] / "brief.py"


def make_canon(root: Path):
    canon = root / "knowledge" / "canon"
    (canon / "style").mkdir(parents=True)
    (canon / "process").mkdir(parents=True)
    (canon / "index.md").write_text("# Канон — індекс\n", encoding="utf-8")
    (canon / "CHANGELOG.md").write_text("# CHANGELOG\n", encoding="utf-8")
    (canon / "style" / "grammar.md").write_text("# Граматика\nПравило A\n", encoding="utf-8")
    (canon / "process" / "verification.md").write_text("# Верифікація\nПравило B\n", encoding="utf-8")
    return canon


def test_find_canon_root_walks_up(tmp_path):
    make_canon(tmp_path)
    nested = tmp_path / "projects" / "demo"
    nested.mkdir(parents=True)
    assert find_canon_root(nested) == tmp_path


def test_build_digest_contains_rules_and_skips_meta(tmp_path):
    canon = make_canon(tmp_path)
    digest = build_digest(canon)

    assert "Правило A" in digest
    assert "Правило B" in digest
    assert "CHANGELOG" not in digest
    assert "style/grammar.md" in digest


def test_cli_writes_brief_file(tmp_path):
    make_canon(tmp_path)
    out = tmp_path / "brief.md"
    subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--out", str(out)],
        check=True,
        capture_output=True,
        text=True,
    )
    content = out.read_text(encoding="utf-8")
    assert "Правило A" in content


def test_cli_fails_without_canon(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "knowledge/canon" in (result.stderr + result.stdout)

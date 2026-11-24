import datetime as dt
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evidence", ROOT / "scripts/web_release_evidence.py")
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
    def git(self, *args, stamp=None):
        env = dict(os.environ)
        if stamp:
            env.update(GIT_AUTHOR_DATE=stamp,GIT_COMMITTER_DATE=stamp)
        return subprocess.check_output(["git","-C",str(self.repo),*args],env=env,text=True).strip()
    def commit(self, name, stamp):
        (self.repo / name).write_text(name)
        self.git("add", name)
        self.git("commit", "-qm", name, stamp=stamp)
        return self.git("rev-parse","HEAD")
    def test_range_and_no_mutation(self):
        old=self.commit("old","2026-11-17T12:00:00+02:00")
        tip=self.commit("new","2026-11-20T12:00:00+02:00")
        r=evidence.collect(self.repo,"2026-11-18T00:00:00+02:00","2026-11-25T00:00:00+02:00")
        self.assertEqual(r["baseline_sha"],old)
        self.assertEqual(r["current_sha"],tip)
        self.assertEqual([c["sha"] for c in r["commits_newest_first"]],[tip])
        self.assertEqual(r["deployment_status"],"unverified")
        self.assertEqual(self.git("status","--porcelain"),"")
        self.assertEqual(self.git("rev-parse","HEAD"),tip)
    def test_missing_base_and_outside_window(self):
        self.commit("new","2026-11-26T12:00:00+02:00")
        r=evidence.collect(self.repo,"2026-11-18T00:00:00+02:00","2026-11-25T00:00:00+02:00")
        self.assertIsNone(r["baseline_sha"])
        self.assertEqual(r["commits_newest_first"],[])
        self.assertTrue(any("outside" in w for w in r["warnings"]))
    def test_naive_date_rejected(self):
        with self.assertRaises(ValueError):
            evidence.date("2026-11-18T00:00:00")

if __name__ == "__main__":
    unittest.main()

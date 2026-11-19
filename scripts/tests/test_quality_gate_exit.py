#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for `quality_gate.py --cases` exit codes.

Run directly (stdlib only):
    python -X utf8 scripts/tests/test_quality_gate_exit.py

The test uses a deliberately wrong expectation to prove that a mismatch is
reported as exit code 1 instead of the old always-zero behaviour.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GATE = ROOT / "scripts" / "quality_gate.py"
CASES = ROOT / "scripts" / "fixtures" / "quality_gate_cases.md"


def run_cases(path):
    return subprocess.run(
        [sys.executable, str(GATE), "--cases", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class QualityGateExitTest(unittest.TestCase):
    def test_all_matching_cases_exit_zero(self):
        result = run_cases(CASES)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("agreement: 20/20", result.stdout)

    def test_mismatch_exits_one(self):
        fixture = (
            "# regression fixture\n"
            "<!-- CASE 01 EXPECTED=PASS -->\n"
            "```text\n"
            "女孩在雨夜便利店门口折纸鹤。\n"
            "```\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mismatch.md"
            path.write_text(fixture, encoding="utf-8")
            result = run_cases(path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("MISMATCH", result.stdout)
        self.assertIn("agreement: 0/1", result.stdout)

    def test_no_cases_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.md"
            path.write_text("# no cases here\n", encoding="utf-8")
            result = run_cases(path)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("no cases found", result.stderr)


if __name__ == "__main__":
    unittest.main()
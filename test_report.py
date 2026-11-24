"""Automated checks for the simulation test-results reporter."""

import tempfile
import unittest
from pathlib import Path

from report import build_report, summarize


class ReportTests(unittest.TestCase):
    def test_counts_mixed_results(self):
        results = [{"status": "PASS"}, {"status": "PASS"}, {"status": "FAIL"}]
        self.assertEqual(summarize(results), {"total": 3, "passed": 2, "failed": 1})

    def test_counts_empty_results(self):
        self.assertEqual(summarize([]), {"total": 0, "passed": 0, "failed": 0})

    def test_rejects_unknown_status(self):
        with self.assertRaisesRegex(ValueError, "Unknown test status"):
            summarize([{"status": "PENDING"}])

    def test_build_creates_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            source.write_text("scenario,status\nLane change,PASS\nBraking,FAIL\n", encoding="utf-8")
            output = Path(directory) / "site" / "index.html"
            build_report(output, source)
            page = output.read_text(encoding="utf-8")
        self.assertIn("<title>Simulation Test Report</title>", page)
        self.assertIn("<dt>Passed</dt><dd>1</dd>", page)
        self.assertIn('class="pass">PASS', page)
        self.assertIn('class="fail">FAIL', page)

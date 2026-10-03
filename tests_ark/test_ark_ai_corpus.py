"""Tests for corpus discovery, coverage, hidden-dir pruning, PDF gating."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arkoftheduck.ai.brain import Brain
from arkoftheduck.ai.corpus import coverage_report, discover_corpora
from arkoftheduck.ai.pdf_ingest import ingest_pdf_dir, pdf_extractor_available
from arkoftheduck.ai.retrieval import Retriever, ingest_markdown_dir
from arkoftheduck.model import Table


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class TestMultiCorpus(unittest.TestCase):
    def test_ingest_dirs_grows_index(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            _write(os.path.join(a, "one.md"), "# Water\nBoil water one minute to purify.")
            _write(os.path.join(b, "two.md"), "# Fire\nStop drop and roll to smother flames.")
            brain = Brain()
            n = brain.ingest_dirs([a, b])
            self.assertEqual(n, 2)
            self.assertGreaterEqual(len(brain.retriever), 2)
            hit = brain.retriever.search("purify water", k=1)
            self.assertTrue(hit and "boil" in hit[0].text.lower())

    def test_explicit_discover(self):
        with tempfile.TemporaryDirectory() as a:
            self.assertEqual(discover_corpora(explicit=[a]), [os.path.realpath(a)])


class TestHiddenDirPruning(unittest.TestCase):
    def test_git_dir_skipped(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, ".git"))
            _write(os.path.join(root, ".git", "COMMIT_EDITMSG.md"), "secret ref")
            _write(os.path.join(root, "real.md"), "# Real\nActual content here.")
            r = Retriever()
            n = ingest_markdown_dir(r, root)
            self.assertEqual(n, 1)  # only real.md, not the .git file


class TestCoverage(unittest.TestCase):
    def test_flags_stub(self):
        with tempfile.TemporaryDirectory() as kb:
            os.makedirs(os.path.join(kb, "water"))
            os.makedirs(os.path.join(kb, "chemistry"))
            _write(os.path.join(kb, "water", "guide.md"), "x" * 2000)
            _write(os.path.join(kb, "chemistry", "tiny.md"), "stub")
            doc = coverage_report(kb, stub_bytes=800)
            tables = [b for b in doc.blocks if isinstance(b, Table)]
            self.assertTrue(tables)
            flat = " ".join(" ".join(r) for r in tables[0].rows)
            self.assertIn("STUB", flat)


class TestPdfGating(unittest.TestCase):
    def test_pdf_extractor_probe_is_safe(self):
        val = pdf_extractor_available()
        self.assertTrue(val is None or isinstance(val, str))

    def test_invalid_pdf_does_not_crash(self):
        with tempfile.TemporaryDirectory() as d:
            _write(os.path.join(d, "bad.pdf"), "<html>not a pdf</html>")
            r = Retriever()
            indexed, skipped = ingest_pdf_dir(r, d)
            self.assertEqual(indexed, 0)
            self.assertGreaterEqual(skipped, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

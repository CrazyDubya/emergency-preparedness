"""Unit tests for the ark render-anywhere core. Stdlib only."""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ark import Document, Heading, Paragraph, Table, Checklist, ChecklistItem, KeyValues, render, registry
from ark.capabilities import Capabilities
from ark.sample import build_sample


def caps(color=False, unicode=True, target="terminal", width=80):
    return Capabilities(is_tty=color, color=color, unicode=unicode, width=width,
                        height=24, python_version=sys.version_info[:3],
                        optional=set(), target=target)


class TestSelection(unittest.TestCase):
    def test_terminal_no_color_selects_plaintext(self):
        r = registry.select(caps(color=False, target="terminal"))
        self.assertEqual(r.format_id, "plaintext")

    def test_terminal_color_selects_ansi(self):
        r = registry.select(caps(color=True, target="terminal"))
        self.assertEqual(r.format_id, "ansi")

    def test_web_target_selects_html(self):
        r = registry.select(caps(target="web"))
        self.assertEqual(r.format_id, "html")

    def test_unknown_prefer_falls_back_not_crash(self):
        out = render(build_sample(), fmt="does-not-exist", caps=caps(color=False))
        self.assertIn("EMERGENCY PREPAREDNESS SNAPSHOT", out)

    def test_prefer_wins_when_runnable(self):
        r = registry.select(caps(color=False, target="terminal"), prefer="html")
        self.assertEqual(r.format_id, "html")


class TestPlaintextAlwaysWorks(unittest.TestCase):
    def test_pure_ascii(self):
        out = registry.get("plaintext").render(build_sample(), caps(color=False))
        out.encode("ascii")  # must not raise
        self.assertNotIn("\033", out)  # no escape codes

    def test_contains_data(self):
        out = registry.get("plaintext").render(build_sample(), caps())
        self.assertIn("Earthquake", out)
        self.assertIn("[x]", out)
        self.assertIn("[ ]", out)


class TestFormats(unittest.TestCase):
    def setUp(self):
        self.doc = build_sample()
        self.c = caps()

    def test_json_roundtrip_structure(self):
        data = json.loads(registry.get("json").render(self.doc, self.c))
        self.assertEqual(data["title"], "Emergency Preparedness Snapshot")
        kinds = [b["kind"] for b in data["blocks"]]
        self.assertIn("table", kinds)
        self.assertIn("checklist", kinds)

    def test_html_escapes_and_structure(self):
        out = registry.get("html").render(
            Document(title="t", blocks=[Paragraph("a < b & c")]), self.c)
        self.assertIn("&lt;", out)
        self.assertIn("<!doctype html>", out)

    def test_markdown_table(self):
        out = registry.get("markdown").render(self.doc, self.c)
        self.assertIn("| Hazard | Probability | Impact | Priority |", out)
        self.assertIn("- [x]", out)

    def test_csv_rows(self):
        out = registry.get("csv").render(self.doc, self.c)
        self.assertIn("Earthquake,Medium,High,1", out)

    def test_ansi_has_color_when_capable(self):
        out = registry.get("ansi").render(self.doc, caps(color=True))
        self.assertIn("\033[", out)


class TestModelBuilder(unittest.TestCase):
    def test_fluent_add(self):
        d = Document(title="x").add(Heading("h")).add(Paragraph("p"))
        self.assertEqual(len(d.blocks), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

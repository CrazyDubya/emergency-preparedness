"""Tests for the arkoftheduck.ai tiered intelligence layer. Stdlib only."""

import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arkoftheduck import render
from arkoftheduck.ai import Brain, Passage, registry
from arkoftheduck.ai.engine import AI_TIER, Answer, Engine, EngineUnavailable
from arkoftheduck.ai.remote import RemoteLLMEngine
from arkoftheduck.ai.resources import ComputeResources, detect_resources
from arkoftheduck.ai.retrieval import ExtractiveEngine, Retriever


def make_brain():
    b = Brain()
    b.add("To purify water, bring it to a rolling boil for one minute to kill "
          "bacteria, viruses and parasites.", title="Water Purification", ref="w.md")
    b.add("Store three gallons of water per person for a 72 hour kit.",
          title="Water Storage", ref="s.md")
    b.add("Apply pressure to a bleeding wound and elevate the limb.",
          title="Bleeding Control", ref="fa.md")
    return b


class _FakeResp:
    def __init__(self, payload):
        self._data = json.dumps(payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def read(self):
        return self._data


class TestRetrieval(unittest.TestCase):
    def test_ranks_relevant_passage_first(self):
        b = make_brain()
        hits = b.retriever.search("how to purify water", k=3)
        self.assertTrue(hits)
        self.assertIn("boil", hits[0].text.lower())

    def test_no_hits_is_safe(self):
        r = Retriever()
        self.assertEqual(r.search("anything"), [])


class TestExtractiveFloor(unittest.TestCase):
    def test_always_available_and_answers(self):
        b = make_brain()
        ans = b.ask("purify water", res=ComputeResources())
        self.assertEqual(ans.engine, "extractive")
        self.assertEqual(ans.tier, AI_TIER["EXTRACTIVE"])
        self.assertIn("boil", ans.text.lower())
        self.assertTrue(ans.sources)

    def test_answer_renders_as_document(self):
        b = make_brain()
        ans = b.ask("purify water", res=ComputeResources())
        out = render(ans.to_document(), fmt="plaintext")
        out.encode("ascii")  # renders anywhere, pure ascii floor
        self.assertIn("ANSWER", out.upper())


class TestResources(unittest.TestCase):
    def test_offline_disables_remote(self):
        res = ComputeResources(remote_endpoint="http://x/v1", remote_key_present=True,
                               offline_only=True)
        self.assertFalse(res.has_remote)

    def test_remote_enabled_when_configured(self):
        res = ComputeResources(remote_endpoint="http://x/v1", remote_key_present=True)
        self.assertTrue(res.has_remote)

    def test_detect_returns_object(self):
        self.assertIsInstance(detect_resources(), ComputeResources)


class TestRemoteEngine(unittest.TestCase):
    def _res(self):
        return ComputeResources(remote_endpoint="http://fake/v1",
                                remote_model="test-model", remote_key_present=True)

    def test_generative_answer_via_mock(self):
        payload = {"choices": [{"message": {"content": "Boil water 1 minute."}}]}
        eng = RemoteLLMEngine(opener=lambda req, timeout=0: _FakeResp(payload))
        ans = eng.answer("purify water", [Passage(text="ctx", ref="w.md")], self._res())
        self.assertEqual(ans.mode, "generative")
        self.assertEqual(ans.tier, AI_TIER["REMOTE"])
        self.assertIn("Boil water", ans.text)

    def test_failure_degrades(self):
        def boom(req, timeout=0):
            raise OSError("network down")
        eng = RemoteLLMEngine(opener=boom)
        with self.assertRaises(EngineUnavailable):
            eng.answer("q", [], self._res())


class TestBrainTierSelection(unittest.TestCase):
    def setUp(self):
        # A fake high-tier engine we can toggle to succeed or fail.
        class FakeRemote(Engine):
            name = "fake-remote"
            tier = AI_TIER["REMOTE"]
            def __init__(self, fail):
                self.fail = fail
            def available(self, res):
                return True
            def answer(self, query, passages, res):
                if self.fail:
                    raise EngineUnavailable("nope")
                return Answer(query=query, text="BIG BRAIN", engine=self.name,
                              tier=self.tier, mode="generative")
        self.FakeRemote = FakeRemote

    def tearDown(self):
        registry._engines.pop("fake-remote", None)

    def test_uses_highest_tier_when_available(self):
        registry.register(self.FakeRemote(fail=False))
        ans = make_brain().ask("purify water", res=ComputeResources())
        self.assertEqual(ans.engine, "fake-remote")
        self.assertEqual(ans.text, "BIG BRAIN")

    def test_degrades_to_extractive_on_failure(self):
        registry.register(self.FakeRemote(fail=True))
        ans = make_brain().ask("purify water", res=ComputeResources())
        self.assertEqual(ans.engine, "extractive")
        self.assertIn("boil", ans.text.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

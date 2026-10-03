"""
Tiny, dependency-free retrieval engine — the "small functional AI".

A compact TF-IDF index over a corpus of passages, implemented with only the
Python standard library. It answers questions by finding and returning the most
relevant passages (extractive QA) with source citations. It needs no model, no
GPU, no network, and a trivial amount of RAM/CPU — so it runs on essentially
any machine and is always available. Higher tiers reuse its retrieved passages
as grounding context (RAG).
"""

import math
import os
import re
from collections import Counter
from typing import List

from .engine import AI_TIER, Answer, Engine, Passage

_TOKEN = re.compile(r"[a-z0-9]+")
# A small, generic stopword set keeps the index lean and improves ranking.
_STOP = frozenset(
    "a an the of to in on for and or is are be as at by it its this that with "
    "from your you我 how do does can what when where which who will if not no "
    "into out up down over under about more most less than then them they their "
    "i we he she his her our us me my".split()
)


def _tokenize(text: str) -> List[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]


class Retriever:
    """In-memory TF-IDF passage index."""

    def __init__(self) -> None:
        self._passages: List[Passage] = []
        self._tf: List[Counter] = []
        self._df: Counter = Counter()
        self._idf = {}
        self._dirty = True

    def add(self, text: str, title: str = "", ref: str = "") -> None:
        text = text.strip()
        if not text:
            return
        toks = _tokenize(text)
        if not toks:
            return
        self._passages.append(Passage(text=text, title=title, ref=ref))
        tf = Counter(toks)
        self._tf.append(tf)
        for term in tf:
            self._df[term] += 1
        self._dirty = True

    def _finalize(self) -> None:
        n = len(self._passages)
        self._idf = {t: math.log((1 + n) / (1 + df)) + 1.0 for t, df in self._df.items()}
        self._dirty = False

    def __len__(self) -> int:
        return len(self._passages)

    def search(self, query: str, k: int = 3) -> List[Passage]:
        if self._dirty:
            self._finalize()
        q_terms = _tokenize(query)
        if not q_terms or not self._passages:
            return []
        q_weights = {t: self._idf.get(t, 0.0) for t in set(q_terms)}
        scored = []
        for i, tf in enumerate(self._tf):
            length = sum(tf.values()) or 1
            score = 0.0
            for term, qw in q_weights.items():
                if term in tf:
                    score += (tf[term] / length) * self._idf.get(term, 0.0) * qw
            if score > 0:
                p = self._passages[i]
                scored.append(Passage(text=p.text, title=p.title, ref=p.ref, score=score))
        scored.sort(key=lambda p: p.score, reverse=True)
        return scored[:k]


def ingest_markdown_dir(retriever: Retriever, root: str, max_files: int = 500) -> int:
    """Split markdown files under `root` into passages and index them."""
    count = 0
    for dirpath, dirs, files in os.walk(root):
        # Skip hidden dirs (e.g. .git) and virtualenvs when ingesting a repo root.
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                   ("node_modules", "__pycache__", "venv")]
        for fn in sorted(files):
            if not fn.lower().endswith((".md", ".markdown", ".txt")):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except OSError:
                continue
            rel = os.path.relpath(path, root)
            # Build passages as heading + body sections so retrieved passages
            # carry real content (not bare heading lines).
            cur_title = fn
            cur_lines: List[str] = []

            def _flush():
                body = "\n".join(cur_lines).strip()
                if len(body) >= 2:
                    retriever.add(body, title=cur_title, ref=rel)

            for line in content.splitlines():
                heading = re.match(r"#+\s*(.+)", line)
                if heading:
                    _flush()
                    cur_title = heading.group(1).strip()
                    cur_lines = [cur_title]  # keep heading text as context
                else:
                    cur_lines.append(line)
            _flush()
            count += 1
            if count >= max_files:
                return count
    return count


class ExtractiveEngine(Engine):
    name = "extractive"
    tier = AI_TIER["EXTRACTIVE"]

    def available(self, res) -> bool:
        return True  # the floor: always works

    def answer(self, query: str, passages: List[Passage], res) -> Answer:
        if not passages:
            return Answer(
                query=query,
                text="No matching information found in the offline knowledge base.",
                engine=self.name, tier=self.tier, mode="extractive",
            )
        top = passages[0]
        # Present the single most relevant passage, trimmed, plus citations.
        body = top.text
        if len(body) > 700:
            body = body[:700].rsplit(" ", 1)[0] + " ..."
        return Answer(
            query=query,
            text=body,
            sources=passages,
            engine=self.name,
            tier=self.tier,
            mode="extractive",
            note="offline retrieval (no model required)",
        )

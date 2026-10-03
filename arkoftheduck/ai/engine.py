"""
Intelligence engine contract + registry.

An Engine turns a query plus retrieved context passages into an Answer. Each
engine declares a `tier` (capacity/quality) and `available(res)`; the registry
picks the highest-tier engine capacity permits and always keeps the tier-0
extractive engine as a guaranteed floor. The Brain additionally catches runtime
failures and degrades to the next lower engine — so intelligence, like
rendering, always works.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from ..model import Divider, Document, Heading, KeyValues, Paragraph

__all__ = ["Passage", "Answer", "Engine", "EngineUnavailable", "EngineRegistry",
           "registry", "AI_TIER"]

AI_TIER = {
    "EXTRACTIVE": 0,   # pure-stdlib retrieval; the guaranteed floor
    "LOCAL": 30,       # on-device small/quantized model
    "REMOTE": 60,      # larger hosted model, if reachable
}


class EngineUnavailable(Exception):
    """Raised by an engine at runtime so the Brain can degrade gracefully."""


@dataclass
class Passage:
    text: str
    title: str = ""
    ref: str = ""
    score: float = 0.0


@dataclass
class Answer:
    query: str
    text: str
    sources: List[Passage] = field(default_factory=list)
    engine: str = ""
    tier: int = 0
    mode: str = "extractive"  # or "generative"
    note: str = ""

    def to_document(self) -> Document:
        """Render the answer as an ark Document (renders in any format)."""
        doc = Document(
            title="Q: " + self.query,
            meta={"engine": self.engine, "tier": self.tier, "mode": self.mode},
        )
        doc.add(Heading("Answer", level=1))
        doc.add(Paragraph(self.text))
        if self.sources:
            doc.add(Heading("Sources", level=1))
            doc.add(KeyValues(pairs=[
                ("%.2f" % p.score, ("%s - %s" % (p.title, p.ref)).strip(" -"))
                for p in self.sources
            ]))
        doc.add(Divider())
        engine_line = "answered by %s (tier %d, %s)" % (self.engine, self.tier, self.mode)
        doc.add(Paragraph(engine_line + ((" | " + self.note) if self.note else "")))
        return doc


class Engine:
    name: str = "base"
    tier: int = AI_TIER["EXTRACTIVE"]

    def available(self, res) -> bool:
        return True

    def answer(self, query: str, passages: List[Passage], res) -> Answer:
        raise NotImplementedError


class EngineRegistry:
    def __init__(self) -> None:
        self._engines = {}

    def register(self, engine: Engine) -> Engine:
        self._engines[engine.name] = engine
        return engine

    def get(self, name: str) -> Optional[Engine]:
        return self._engines.get(name)

    def all(self) -> List[Engine]:
        return sorted(self._engines.values(), key=lambda e: e.tier, reverse=True)

    def available(self, res) -> List[Engine]:
        """Engines usable under `res`, highest tier first."""
        usable = [e for e in self._engines.values() if e.available(res)]
        return sorted(usable, key=lambda e: e.tier, reverse=True)


registry = EngineRegistry()

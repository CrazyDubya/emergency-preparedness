"""
Brain — orchestrates retrieval + the best available engine (RAG).

Flow: always retrieve grounding passages with the tiny offline retriever, then
ask the highest-tier engine that capacity permits to produce the answer. If an
engine fails at runtime, drop to the next lower one; the extractive engine is
the guaranteed floor. So you get the smartest answer the environment allows,
and never a failure.
"""

from typing import List, Optional

from .engine import Answer, EngineUnavailable, Passage, registry
from .resources import ComputeResources, detect_resources
from .retrieval import ExtractiveEngine, Retriever, ingest_markdown_dir

__all__ = ["Brain"]


class Brain:
    def __init__(self, retriever: Optional[Retriever] = None) -> None:
        self.retriever = retriever or Retriever()

    # ingestion -----------------------------------------------------------
    def ingest_dir(self, path: str) -> int:
        return ingest_markdown_dir(self.retriever, path)

    def add(self, text: str, title: str = "", ref: str = "") -> None:
        self.retriever.add(text, title=title, ref=ref)

    # querying ------------------------------------------------------------
    def ask(self, query: str, res: Optional[ComputeResources] = None,
            k: int = 3) -> Answer:
        res = res if res is not None else detect_resources()
        passages: List[Passage] = self.retriever.search(query, k=k)
        for engine in registry.available(res):
            try:
                return engine.answer(query, passages, res)
            except EngineUnavailable:
                continue
            except Exception:
                # Defensive: never let a higher-tier engine crash the answer.
                continue
        # Guaranteed floor.
        return ExtractiveEngine().answer(query, passages, res)

    def plan(self, res: Optional[ComputeResources] = None):
        """Return the ordered engines that would be tried for the given res."""
        res = res if res is not None else detect_resources()
        return [(e.name, e.tier) for e in registry.available(res)]

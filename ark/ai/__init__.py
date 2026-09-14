"""
ark.ai — tiered intelligence layer.

A tiny, dependency-free retrieval AI that always works offline, plus optional
higher tiers (on-device model, remote LLM) that engage only when capacity
permits. Answers are ark Documents, so they render in any format on any system.

    from ark.ai import Brain
    brain = Brain()
    brain.ingest_dir("knowledge_base")      # or brain.add(text, title, ref)
    answer = brain.ask("how do I purify water?")
    print(answer.text)                       # extractive/generative answer
    from ark import render
    print(render(answer.to_document()))      # render anywhere
"""

from .brain import Brain
from .engine import AI_TIER, Answer, Engine, EngineUnavailable, Passage, registry
from .local_model import LocalModelEngine
from .remote import RemoteLLMEngine
from .resources import ComputeResources, detect_resources
from .retrieval import ExtractiveEngine, Retriever, ingest_markdown_dir

# Register built-in engines (tier order handled by the registry).
for _e in (ExtractiveEngine(), LocalModelEngine(), RemoteLLMEngine()):
    registry.register(_e)

__all__ = [
    "Brain", "Answer", "Passage", "Engine", "EngineUnavailable", "registry",
    "AI_TIER", "ComputeResources", "detect_resources", "Retriever",
    "ExtractiveEngine", "LocalModelEngine", "RemoteLLMEngine",
    "ingest_markdown_dir",
]

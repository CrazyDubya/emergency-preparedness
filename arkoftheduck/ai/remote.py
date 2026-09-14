"""
Remote LLM engine (tier REMOTE) — connect to larger and larger AI.

Used only when an OpenAI-compatible endpoint (ARK_LLM_ENDPOINT) and API key
(ARK_LLM_API_KEY) are configured and offline mode is not forced. Calls the
chat-completions API over stdlib urllib (no third-party SDK). Any failure
(network, auth, timeout) raises EngineUnavailable so the Brain degrades to a
local or extractive answer. The bigger brain is a bonus, never a dependency.
"""

import json
import urllib.error
import urllib.request
from typing import List

from .engine import AI_TIER, Answer, Engine, EngineUnavailable, Passage

_SYSTEM = (
    "You are an emergency-preparedness assistant. Answer concisely and ground "
    "your answer in the provided context; note if the context is insufficient."
)


class RemoteLLMEngine(Engine):
    name = "remote-llm"
    tier = AI_TIER["REMOTE"]

    def __init__(self, timeout: float = 20.0, opener=None) -> None:
        # `opener` is injectable for testing (defaults to urllib.request.urlopen).
        self._timeout = timeout
        self._opener = opener or urllib.request.urlopen

    def available(self, res) -> bool:
        return res.has_remote

    def _messages(self, query: str, passages: List[Passage]):
        context = "\n\n".join(
            "[%s] %s" % (p.ref or p.title, p.text) for p in passages[:5]
        )
        user = "Context:\n%s\n\nQuestion: %s" % (context or "(none)", query)
        return [{"role": "system", "content": _SYSTEM},
                {"role": "user", "content": user}]

    def answer(self, query: str, passages: List[Passage], res) -> Answer:
        endpoint = res.remote_endpoint.rstrip("/") + "/chat/completions"
        payload = json.dumps({
            "model": res.remote_model,
            "messages": self._messages(query, passages),
            "temperature": 0.2,
            "max_tokens": 400,
        }).encode("utf-8")
        req = urllib.request.Request(
            endpoint, data=payload, method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + (res.remote_key_present and
                                               __import__("os").environ.get("ARK_LLM_API_KEY", "") or ""),
            },
        )
        try:
            with self._opener(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            text = data["choices"][0]["message"]["content"].strip()
        except (urllib.error.URLError, urllib.error.HTTPError, OSError,
                KeyError, ValueError, TimeoutError) as exc:
            raise EngineUnavailable("remote LLM failed: %s" % exc)
        if not text:
            raise EngineUnavailable("remote LLM returned no text")
        return Answer(
            query=query, text=text, sources=passages, engine=self.name,
            tier=self.tier, mode="generative",
            note="remote model %s" % res.remote_model,
        )

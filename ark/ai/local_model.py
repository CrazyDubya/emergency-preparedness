"""
Local on-device model engine (tier LOCAL).

Used only when BOTH an offline runtime (llama.cpp / ctransformers / gpt4all /
transformers) is importable AND a model file is configured via ARK_LOCAL_MODEL.
When present, it synthesizes an answer grounded in the retrieved passages (RAG).
When absent — or if loading/generation fails — it declines so the Brain falls
back to the extractive floor. This is "useful AI if capacity permits".
"""

from typing import List

from .engine import AI_TIER, Answer, Engine, EngineUnavailable, Passage

_PROMPT = (
    "You are an offline emergency-preparedness assistant. Answer the question "
    "concisely using ONLY the context. If the context is insufficient, say so.\n\n"
    "Context:\n{context}\n\nQuestion: {query}\nAnswer:"
)


class LocalModelEngine(Engine):
    name = "local-model"
    tier = AI_TIER["LOCAL"]

    def available(self, res) -> bool:
        return res.has_local_model

    def _build_prompt(self, query: str, passages: List[Passage]) -> str:
        context = "\n\n".join(
            "[%s] %s" % (p.ref or p.title, p.text) for p in passages[:4]
        )
        return _PROMPT.format(context=context or "(none)", query=query)

    def answer(self, query: str, passages: List[Passage], res) -> Answer:
        prompt = self._build_prompt(query, passages)
        text = None
        try:
            if "llama_cpp" in res.ml_runtimes:
                from llama_cpp import Llama  # type: ignore
                llm = Llama(model_path=res.local_model_path, n_ctx=2048, verbose=False)
                out = llm(prompt, max_tokens=256, stop=["\n\n"])
                text = out["choices"][0]["text"].strip()
            elif "ctransformers" in res.ml_runtimes:
                from ctransformers import AutoModelForCausalLM  # type: ignore
                llm = AutoModelForCausalLM.from_pretrained(res.local_model_path)
                text = llm(prompt, max_new_tokens=256).strip()
            elif "gpt4all" in res.ml_runtimes:
                from gpt4all import GPT4All  # type: ignore
                llm = GPT4All(res.local_model_path, allow_download=False)
                with llm.chat_session():
                    text = llm.generate(prompt, max_tokens=256).strip()
            else:
                raise EngineUnavailable("no supported local runtime")
        except EngineUnavailable:
            raise
        except Exception as exc:  # loading/inference failure -> degrade
            raise EngineUnavailable("local model failed: %s" % exc)

        if not text:
            raise EngineUnavailable("local model returned no text")
        return Answer(
            query=query, text=text, sources=passages, engine=self.name,
            tier=self.tier, mode="generative", note="on-device model (offline)",
        )

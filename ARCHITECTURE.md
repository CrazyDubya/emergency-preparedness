# ArkoftheDuck — render-anywhere architecture & merge plan

> One data core. Unlimited formats, systems, and compute tiers. It always works.
> The doomsday backup that renders on an x86 relic and a supercomputer alike —
> particularly well on command lines and GUIs today, with a path to 3D/AR later.

This document proposes how to merge the two repositories into a single
application built around a small, dependency-free rendering core (`arkoftheduck/`), and
how the existing code folds into it.

## 1. The core idea

Separate **what the data is** from **how it is shown**:

- **Data core (`arkoftheduck/model.py`)** — a semantic `Document` made of `Block`s
  (`Heading`, `Paragraph`, `Table`, `Checklist`, `KeyValues`, `Divider`, ...).
  Pure Python standard library, **zero third-party dependencies**. This is the
  part that must run *everywhere*.
- **Capabilities (`arkoftheduck/capabilities.py`)** — detects the current
  system/target: TTY? color? unicode? width? Python version? which optional
  rich libraries are importable?
- **Renderer registry (`arkoftheduck/renderer.py`)** — every output format/target is a
  `Renderer` plugin declaring a `tier` (richness), the `targets` it auto-applies
  to, and a `requires(caps)` gate. The registry picks the richest renderer the
  environment supports and **always falls back to plaintext**.

```
            +------------------- data sources -------------------+
            | preparedness system | knowledge base | disaster docs |
            +----------------------------┬----------------------- +
                                         v  (adapters build Documents)
                                +------------------+
                                |  ark.Document    |   <- stdlib-only core
                                +--------┬---------+
                                         v
                    capabilities ->  Renderer Registry  (auto-select + fallback)
   +----------+----------+-----------+-----------+-----------+-----------------+
   | plaintext|   json   |    csv    | markdown  |   ansi    |      html       |  ... 3D/AR
   |  tier 0  |  tier 10 |  tier 10  |  tier 20  |  tier 30  |     tier 40     |
   | ALWAYS   |  data    |  data     |  file     | terminal  |    web/gui      |
   +----------+----------+-----------+-----------+-----------+-----------------+
```

## 2. The "always works" invariant (degradation ladder)

Selection never fails; it degrades. For a given target, the registry chooses the
highest-tier renderer whose `requires(caps)` is true, and `plaintext` (tier 0)
is universal, so there is always an answer.

| Environment | Auto result |
| --- | --- |
| Dumb terminal / piped / `NO_COLOR` / ancient box | `plaintext` (pure ASCII) |
| Color terminal | `ansi` (color + unicode box; ASCII box if no unicode) |
| Web target | `html` (self-contained, offline) |
| Data/export target | `json` / `csv` |
| (future) rich TUI / GUI / 3D / AR | new tiers slot in above `WEB` |

New formats or targets are **new plugins**; the core never changes. That is how
"unlimited formats / unlimited systems" is realized in practice.

"Unlimited compute" = the same document costs almost nothing to render as text
on a 386-class machine, and can drive a GPU-heavy 3D scene on a workstation —
because compute lives entirely in the renderer tier, not in the data core.

## 3. Proof of concept (already in this branch)

`arkoftheduck/` is a working implementation:

- `python -m arkoftheduck` auto-selects for the current terminal.
- `python -m arkoftheduck --all` renders the sample in every format.
- `python -m arkoftheduck --list` / `--caps` show usable renderers and detected caps.
- `python -m arkoftheduck -f html -o out.html`, `-f markdown`, `-f json`, `-f csv`, `-f ansi`.
- `python -m arkoftheduck --input doc.json` renders any document authored in the JSON schema.

Validated: 13 unit tests pass, and the whole thing runs on the **bare system
`python3` with no site-packages** (`python3 -E -s -m arkoftheduck`), proving the
zero-dependency guarantee.

## 4. How the two existing apps fold in

Both current apps essentially re-implement formatting by hand. Under ArkoftheDuck they
become **adapters** (produce `Document`s) plus **renderers** (present them):

| Today | Under ArkoftheDuck |
| --- | --- |
| `disaster` repo: static markdown library | An ingest adapter turns each guide into a `Document`; the knowledge base is a corpus of `Document`s, renderable to CLI/web/etc. |
| `visualization_dashboard.py` (ASCII art) | A `Document` + the `ansi`/`plaintext` renderers (kills bespoke ASCII code) |
| `integrated_preparedness_system.py` CLI menus/reports | Build `Document`s; render with auto-select |
| `streamlit_gui.py` | A `web`/GUI target consuming the same `Document`s (later: an HTML/interactive renderer tier) |
| `api_server.py` responses | Already structured; expose `Document` JSON via the `json` renderer for any client |

Net effect: one canonical representation of preparedness data, presented
consistently across CLI, GUI, API, and files — no divergent formatting logic.

## 5. Repo merge plan (single repo, single application)

**Recommendation:** make `emergency-preparedness` the canonical monorepo (it
already holds the application), and bring the `disaster` markdown library in as
a knowledge/reference corpus consumed by an ingest adapter.

Proposed layout:

```
<repo root>/
  arkoftheduck/                      # render-anywhere core (this branch)
  apps/
    preparedness/           # former disaster/ application code
  knowledge/
    library/                # former `disaster` repo markdown (reference corpus)
    guides/                 # former emergency-preparedness/disaster/knowledge_base
  adapters/                 # data-source -> ark.Document
  tests/
```

Two ways to physically merge the history — **needs your call**:

1. **History-preserving (`git subtree add`)** — import the `disaster` repo as a
   subdirectory keeping its commit history. Best if history matters.
2. **Clean vendored import** — copy the markdown in as a snapshot with a
   provenance note. Simpler, smaller, loses granular history.

Either is a discrete, mostly-mechanical step. I did **not** perform it yet
because it is the one hard-to-reverse action and depends on the two choices
below.

## 5b. Intelligence layer (`arkoftheduck/ai/`) — same philosophy, applied to AI

The AI capability mirrors the renderer stack: a tiny engine that always works,
scaling up to bigger brains only when capacity permits, always degrading back.

- **Compute detection (`ai/resources.py`)** — CPU count, RAM, importable ML
  runtimes (llama.cpp / ctransformers / gpt4all / transformers), a configured
  local model (`ARK_LOCAL_MODEL`), and a remote endpoint+key
  (`ARK_LLM_ENDPOINT` / `ARK_LLM_API_KEY`). `ARK_AI_OFFLINE=1` is the doomsday
  switch that caps everything at the offline floor.
- **Engine registry (`ai/engine.py`)** — tiered `Engine`s; the Brain picks the
  highest tier capacity permits and catches runtime failures to drop down.
- **Tier 0 `extractive` (`ai/retrieval.py`)** — a pure-stdlib TF-IDF retriever
  over the knowledge base. Answers by returning the most relevant passages with
  citations. No model, no GPU, no network, negligible RAM/CPU — **always
  available**. This is the "small functional AI".
- **Tier `local` (`ai/local_model.py`)** — an on-device quantized model
  (llama.cpp / ctransformers / gpt4all), used only if a runtime + model file are
  present; synthesizes an answer grounded in retrieved passages (RAG).
- **Tier `remote` (`ai/remote.py`)** — an OpenAI-compatible endpoint over stdlib
  `urllib`, used only if configured and reachable; the biggest brain, purely a
  bonus.

Every answer is an `ark.Document`, so the same reply renders on a CLI, as
Markdown/JSON, or as a web page — intelligence and rendering share one core.

```
   query --> [ retrieve grounding passages (always) ] --> context
                                   |
             pick highest tier capacity permits (degrade on failure)
     remote-llm (tier 60) ---> local-model (tier 30) ---> extractive (tier 0, ALWAYS)
                                   |
                             ark.Document --> render anywhere
```

Validated end-to-end: extractive answers over the real 37-guide knowledge base
(814 passages) on the **bare system python3, zero dependencies**; RAG synthesis
via a mock OpenAI endpoint when configured; automatic fallback to extractive
when the endpoint is down; and `--offline` forcing the floor. 24 unit tests pass
(13 render + 11 AI). Try it:

```
python -m arkoftheduckoftheduck.ai "how do I purify drinking water"   # offline extractive
python -m arkoftheduckoftheduck.ai --plan          # show engine tiers available now
python -m arkoftheduckoftheduck.ai --caps          # detected compute resources
python -m arkoftheduckoftheduck.ai "..." --offline # force the doomsday floor
```

Honest limitation: tier-0 is keyword retrieval, so a query like "treat a burn"
can match DVD-"burning"; that is precisely the gap the local/remote tiers close
when capacity permits.

## 5c. Corpus & the sparsity problem

The offline floor is only as good as its corpus. Measuring the current one
surfaced three separate sparsity problems, now addressed:

- **Siloed library.** The app knowledge base is only ~137 KiB of actionable
  markdown; the richer `disaster` reference library (~410 KiB) lived in a
  separate repo and was not indexed. `ai/corpus.py:discover_corpora()` now finds
  and ingests both (index grew from 37 files/814 passages to 57 files/1650
  passages), and answers now cite library guides (`TOPIC_WATER.md`, etc.).
- **PDF dead weight.** ~30 MB of authoritative FEMA/CISA/Ready.gov material was
  locked in 11 PDFs the text retriever couldn't read. `ai/pdf_ingest.py` adds a
  **capability-gated** PDF tier: if an extractor (pypdf/PyPDF2/pdfminer) is
  importable it indexes them (all 11 in ~5 s), otherwise it skips cleanly — the
  zero-dependency floor is preserved.
- **Broken stubs.** `ai/corpus.py:coverage_report()` (rendered as an
  ArkoftheDuck Document) flags thin/PDF-only categories. It revealed that
  `chemistry`, `engineering`, and `survival` are **broken download placeholders**
  (404/HTML masquerading as `.pdf`), not real content.

CLI: `python -m arkoftheduck.ai --coverage`, `... --pdf`, `... --corpus DIR`,
`... --no-library`.

## 6. Roadmap

- **P0 — Core (done):** `arkoftheduck/` model + capabilities + registry + 6 renderers + CLI + tests.
- **P1 — Adapters:** preparedness data (risk matrix, supplies, drills, profile) and knowledge guides -> `Document`s.
- **P2 — Wire in:** replace `visualization_dashboard` ASCII, CLI reports, and API payloads with ArkoftheDuck; keep behavior.
- **P3 — Rich TUI tier:** optional `rich`-backed renderer (auto-detected; degrades to `ansi`/`plaintext`).
- **P4 — Web/interactive tier:** HTML+JS renderer; fold the Streamlit GUI onto shared `Document`s.
- **P5 — Spatial tier:** 3D/AR renderer plugins (e.g. WebGL/USD) consuming the exact same documents.
- **AI-P0 — Intelligence floor (done):** stdlib TF-IDF extractive engine + tiered registry + local/remote engines with graceful fallback (`arkoftheduck/ai/`).
- **AI-P1:** ship a small quantized on-device model as the default `local` tier (llama.cpp/gguf), auto-detected.
- **AI-P2:** better offline retrieval (BM25, embeddings if a runtime exists), semantic fallback so queries like "treat a burn" resolve correctly offline.
- **AI-P3:** tool/agent use over the same `Document` model (fill checklists, compute supplies) at higher tiers.

## 7. Open decisions (need your input)

1. **Canonical repo & name** — confirm `emergency-preparedness` as the monorepo, and the product/engine name (`ark` is a placeholder).
2. **History strategy** — `git subtree` (preserve) vs clean vendored import for the `disaster` library.
3. **Scope of first real integration** — which surface to convert first (I suggest `visualization_dashboard` -> ArkoftheDuck, highest bang for the buck).

## Status log

- 2026-09-14: Built and validated the `arkoftheduck/` core PoC (6 renderers, auto-select,
  plaintext fallback, 13 tests, zero-dependency run confirmed). Repo merge not
  yet performed pending decisions in §7.

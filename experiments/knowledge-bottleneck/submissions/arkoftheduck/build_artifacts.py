#!/usr/bin/env python3
"""
Deterministic builder for the ArkoftheDuck knowledge-bottleneck submission.

Method (Option B, model-generated primary layers):
- 1k.txt   : the hand-authored irreducible core (sources/core_1k.txt), verified
             to fit 1,024 bytes. No packing.
- 100k.txt : the authored operating manual (sources/manual.md) as the primary
             layer, then whole paragraphs of repository reference material are
             admitted (ASCII-normalized, de-duplicated, URLs stripped) until the
             102,400-byte ceiling is reached.
- 1m.txt   : the authored manual + the authored extended library
             (sources/library_extra.md) as primary layers, then more repository
             reference material to fill toward 1,048,576 bytes.

The authored operating layers always take precedence; packed repository text is
an explicitly labeled lower reference tier. The generated .txt artifacts stand
alone as plain ASCII/UTF-8 and require no decoder. This script is provenance
only; it is not needed to read the artifacts.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# repo root = experiments/knowledge-bottleneck/submissions/arkoftheduck -> up 4
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

KIB = 1024
BUDGET_1K = 1 * 1024
BUDGET_100K = 100 * 1024
BUDGET_1M = 1024 * 1024

# Repository corpora to draw reference material from (whatever is present).
SOURCE_DIRS = [
    os.path.join(REPO, "disaster", "knowledge_base"),
    os.path.join(REPO, "..", "disaster"),          # sibling reference library
    "/agent/repos/disaster",
]

_URL = re.compile(r"https?://\S+")
_WS = re.compile(r"[ \t]+")
_REPL = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u2022": "-",
    "\u00a0": " ", "\u00b0": " deg", "\u2265": ">=", "\u2264": "<=",
    "\ufeff": "",
}


def to_ascii(text):
    for k, v in _REPL.items():
        text = text.replace(k, v)
    text = _URL.sub("", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # normalize line-internal whitespace, keep paragraph breaks
    lines = [_WS.sub(" ", ln).rstrip() for ln in text.splitlines()]
    return "\n".join(lines)


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _pdf_reader():
    for name in ("pypdf", "PyPDF2"):
        try:
            return __import__(name)
        except ImportError:
            continue
    return None


def _emit_paragraphs(body, rel, seen):
    for para in re.split(r"\n\s*\n", body):
        para = para.strip()
        if not (40 <= len(para) <= 3000):
            continue
        key = re.sub(r"\W+", " ", para.lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        yield para, rel


def iter_source_paragraphs():
    """
    Yield (paragraph, source_ref) from repository markdown/text (highest value
    first), then, if a PDF extractor is available, from the reference PDFs
    (lower tier). De-duplicated across all sources.
    """
    seen = set()
    roots = []
    for d in SOURCE_DIRS:
        rp = os.path.realpath(d)
        if os.path.isdir(rp) and rp not in roots:
            roots.append(rp)

    # Tier 1: markdown / text
    for root in roots:
        for dp, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if not x.startswith(".") and
                       x not in ("node_modules", "__pycache__", "venv")]
            for fn in sorted(files):
                if not fn.lower().endswith((".md", ".markdown", ".txt")):
                    continue
                rel = os.path.relpath(os.path.join(dp, fn), root)
                for item in _emit_paragraphs(to_ascii(read(os.path.join(dp, fn))), rel, seen):
                    yield item

    # Tier 2: reference PDFs (only real %PDF files, only if an extractor exists)
    reader = _pdf_reader()
    if reader is None:
        return
    for root in roots:
        for dp, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if not x.startswith(".")]
            for fn in sorted(files):
                if not fn.lower().endswith(".pdf"):
                    continue
                path = os.path.join(dp, fn)
                try:
                    with open(path, "rb") as fh:
                        if fh.read(4) != b"%PDF":
                            continue  # skip HTML/404 placeholders
                    pages = reader.PdfReader(path).pages
                    text = "\n\n".join((p.extract_text() or "") for p in pages)
                except Exception:
                    continue
                rel = os.path.relpath(path, root)
                for item in _emit_paragraphs(to_ascii(text), rel, seen):
                    yield item


def pack(primary_text, budget, ref_header):
    """Primary authored text, then repo paragraphs until the byte budget."""
    parts = [primary_text.rstrip() + "\n"]
    used = len(parts[0].encode("utf-8"))
    header = "\n\n" + ref_header + "\n\n"
    header_added = False
    hb = len(header.encode("utf-8"))
    for para, ref in iter_source_paragraphs():
        block = ("[src: %s]\n%s\n\n" % (ref, para))
        bb = len(block.encode("utf-8"))
        extra = bb + (0 if header_added else hb)
        if used + extra > budget:
            continue  # try smaller later paragraphs; keep filling
        if not header_added:
            parts.append(header)
            used += hb
            header_added = True
        parts.append(block)
        used += bb
    return "".join(parts)


def write_exact(path, text, budget):
    data = text.encode("utf-8")
    if len(data) > budget:
        # Trim on a UTF-8 boundary just under the ceiling (should not trigger
        # for packed outputs, which fill conservatively).
        data = data[:budget]
        while True:
            try:
                data.decode("utf-8")
                break
            except UnicodeDecodeError:
                data = data[:-1]
    with open(path, "wb") as fh:
        fh.write(data)
    return len(data)


def main():
    core = to_ascii(read(os.path.join(HERE, "sources", "core_1k.txt"))).rstrip() + "\n"
    manual = to_ascii(read(os.path.join(HERE, "sources", "manual.md")))
    library = to_ascii(read(os.path.join(HERE, "sources", "library_extra.md")))

    ref = "==================== REPOSITORY REFERENCE LAYER (lower tier) ===================="

    out_1k = core
    out_100k = pack(manual, BUDGET_100K, ref)
    out_1m = pack(manual + "\n\n" + library, BUDGET_1M, ref)

    results = []
    for name, text, budget in (
        ("1k.txt", out_1k, BUDGET_1K),
        ("100k.txt", out_100k, BUDGET_100K),
        ("1m.txt", out_1m, BUDGET_1M),
    ):
        n = write_exact(os.path.join(HERE, name), text, budget)
        data = open(os.path.join(HERE, name), "rb").read()
        assert len(data) <= budget, "%s exceeds budget" % name
        data.decode("utf-8")  # must be valid UTF-8
        chars = len(data.decode("utf-8"))
        lines = data.count(b"\n")
        pct = 100.0 * n / budget
        results.append((name, budget, n, pct, chars, lines))

    w = 12
    print("%-9s %10s %10s %8s %9s %7s" %
          ("artifact", "budget", "bytes", "util%", "chars", "lines"))
    for name, budget, n, pct, chars, lines in results:
        print("%-9s %10d %10d %7.3f%% %9d %7d" % (name, budget, n, pct, chars, lines))


if __name__ == "__main__":
    main()

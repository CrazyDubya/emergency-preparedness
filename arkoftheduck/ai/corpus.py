"""
Corpus discovery + coverage analysis.

ArkoftheDuck's offline answers are only as good as the corpus behind them. This
module (a) locates every available markdown corpus — the app knowledge base AND
the sibling `disaster` reference library, which historically was siloed in a
separate repo — and (b) produces a coverage report (as an ArkoftheDuck Document)
that flags thin/stub categories and PDF-only material, quantifying sparsity.
"""

import os
from typing import List, Tuple

from ..model import Document, Heading, KeyValues, Paragraph, Table

__all__ = ["discover_corpora", "coverage_report"]

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))

# Markdown corpora we know how to find. Order matters only for reporting.
_APP_KB = [
    os.path.join(os.getcwd(), "knowledge_base"),
    os.path.join(_REPO, "disaster", "knowledge_base"),
    "/agent/repos/emergency-preparedness/disaster/knowledge_base",
    os.path.join(_REPO, "knowledge", "guides"),  # future monorepo layout
]
_LIBRARY = [
    os.path.join(_REPO, "..", "disaster"),        # sibling repo
    "/agent/repos/disaster",
    os.path.join(_REPO, "knowledge", "library"),  # future monorepo layout
]


def _first_existing(paths) -> List[str]:
    seen, out = set(), []
    for p in paths:
        try:
            rp = os.path.realpath(p)
        except OSError:
            continue
        if os.path.isdir(rp) and rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out


def discover_corpora(explicit: List[str] = None, include_library: bool = True) -> List[str]:
    """Return existing corpus directories: app KB (+ sibling library)."""
    if explicit:
        return _first_existing(explicit)
    found = _first_existing(_APP_KB)[:1]  # first matching app KB
    if include_library:
        found += _first_existing(_LIBRARY)[:1]
    return found


def _md_pdf_bytes(path: str) -> Tuple[int, int, int, int]:
    """Return (md_files, md_bytes, pdf_files, pdf_bytes) under path."""
    md_f = md_b = pdf_f = pdf_b = 0
    for dp, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            fp = os.path.join(dp, fn)
            try:
                size = os.path.getsize(fp)
            except OSError:
                continue
            low = fn.lower()
            if low.endswith((".md", ".markdown", ".txt")):
                md_f += 1
                md_b += size
            elif low.endswith(".pdf"):
                pdf_f += 1
                pdf_b += size
    return md_f, md_b, pdf_f, pdf_b


def coverage_report(kb_dir: str, stub_bytes: int = 800) -> Document:
    """Build a coverage report Document for a knowledge-base directory."""
    doc = Document(title="Knowledge Base Coverage", meta={"dir": kb_dir})
    if not os.path.isdir(kb_dir):
        doc.add(Paragraph("Knowledge base not found: %s" % kb_dir))
        return doc

    cats = sorted(
        d for d in os.listdir(kb_dir) if os.path.isdir(os.path.join(kb_dir, d))
    )
    rows = []
    total_md_b = stub_count = pdf_only = 0
    for c in cats:
        md_f, md_b, pdf_f, _pb = _md_pdf_bytes(os.path.join(kb_dir, c))
        total_md_b += md_b
        if md_b < stub_bytes and pdf_f == 0:
            status = "STUB"
            stub_count += 1
        elif md_b < stub_bytes and pdf_f > 0:
            status = "PDF-ONLY (needs PDF tier)"
            pdf_only += 1
        else:
            status = "ok"
        rows.append([c, str(md_f), "%d" % md_b, str(pdf_f), status])

    doc.add(Paragraph(
        "Actionable markdown totals ~%d KiB across %d categories. Categories "
        "under %d bytes of text are flagged; PDF-only categories need the "
        "capability-gated PDF ingest tier to become searchable."
        % (total_md_b // 1024, len(cats), stub_bytes)
    ))
    doc.add(Heading("Categories", level=1))
    doc.add(Table(
        headers=["Category", "md files", "md bytes", "pdfs", "status"],
        rows=rows,
        caption="Coverage by category",
    ))
    doc.add(KeyValues(title="Summary", pairs=[
        ("categories", str(len(cats))),
        ("actionable_md_kib", str(total_md_b // 1024)),
        ("stub_categories", str(stub_count)),
        ("pdf_only_categories", str(pdf_only)),
    ]))
    return doc

"""
Capability-gated PDF ingest.

The reference corpus includes large government PDFs (FEMA, CISA, Ready.gov) that
the stdlib text retriever cannot read. PDF text extraction needs a third-party
library, so — consistent with ArkoftheDuck's tiering — this is *optional*: if a
supported extractor (pypdf / PyPDF2 / pdfminer) is importable, PDFs are indexed;
otherwise they are skipped with a clear note and the offline floor is unaffected.
"""

import importlib.util
import os
from typing import Optional, Tuple

_EXTRACTORS = ("pypdf", "PyPDF2", "pdfminer")


def pdf_extractor_available() -> Optional[str]:
    for name in _EXTRACTORS:
        try:
            if importlib.util.find_spec(name) is not None:
                return name
        except (ImportError, ValueError):
            continue
    return None


def _extract_text(path: str) -> str:
    lib = pdf_extractor_available()
    if lib in ("pypdf", "PyPDF2"):
        mod = __import__(lib)
        reader = mod.PdfReader(path)
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(parts)
    if lib == "pdfminer":
        from pdfminer.high_level import extract_text  # type: ignore
        return extract_text(path) or ""
    return ""


def ingest_pdf_dir(retriever, root: str, max_files: int = 100,
                   max_chars_per_pdf: int = 200000) -> Tuple[int, int]:
    """
    Index PDFs under `root`. Returns (indexed, skipped). If no extractor is
    installed, returns (0, <n pdfs>) without error.
    """
    if pdf_extractor_available() is None:
        skipped = sum(
            1 for dp, _d, fs in os.walk(root) for f in fs if f.lower().endswith(".pdf")
        )
        return 0, skipped

    indexed = skipped = 0
    import re
    for dp, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if not fn.lower().endswith(".pdf"):
                continue
            path = os.path.join(dp, fn)
            try:
                text = _extract_text(path)[:max_chars_per_pdf]
            except Exception:
                skipped += 1
                continue
            if not text.strip():
                skipped += 1
                continue
            rel = os.path.relpath(path, root)
            # Split into paragraph-ish passages for retrieval.
            for chunk in re.split(r"\n\s*\n", text):
                chunk = chunk.strip()
                if len(chunk) >= 40:
                    retriever.add(chunk, title=fn, ref=rel)
            indexed += 1
            if indexed >= max_files:
                return indexed, skipped
    return indexed, skipped

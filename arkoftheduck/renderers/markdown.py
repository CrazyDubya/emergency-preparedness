"""Markdown renderer (tier 20) — portable rich text for docs, chat, wikis."""

from typing import List

from ..capabilities import Capabilities
from ..model import (
    Block, Checklist, Divider, Document, Heading, KeyValues, Paragraph, Table,
)
from ..renderer import TIER, Renderer


class MarkdownRenderer(Renderer):
    format_id = "markdown"
    name = "Markdown"
    tier = TIER["MARKUP"]
    targets = frozenset({"file", "data"})

    def requires(self, caps: Capabilities) -> bool:
        return True

    def render(self, doc: Document, caps: Capabilities) -> str:
        out: List[str] = []
        if doc.title:
            out.append("# " + doc.title)
            out.append("")
        for block in doc.blocks:
            out.extend(self._block(block))
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    def _block(self, block: Block) -> List[str]:
        if isinstance(block, Heading):
            return ["#" * (block.level + 1) + " " + block.text]
        if isinstance(block, Paragraph):
            return [block.text]
        if isinstance(block, Table):
            return self._table(block)
        if isinstance(block, Checklist):
            out = []
            if block.title:
                out.append("**" + block.title + "**")
            for item in block.items:
                box = "[x]" if item.done else "[ ]"
                prio = " _(%s)_" % item.priority if item.priority else ""
                out.append("- " + box + " " + item.text + prio)
            return out
        if isinstance(block, KeyValues):
            out = []
            if block.title:
                out.append("**" + block.title + "**")
            for k, v in block.pairs:
                out.append("- **%s:** %s" % (k, v))
            return out
        if isinstance(block, Divider):
            return ["---"]
        return [str(getattr(block, "text", block))]

    def _table(self, t: Table) -> List[str]:
        out: List[str] = []
        if t.caption:
            out.append("**" + t.caption + "**")
            out.append("")
        headers = t.headers or [""] * (len(t.rows[0]) if t.rows else 0)
        out.append("| " + " | ".join(self._esc(h) for h in headers) + " |")
        out.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in t.rows:
            cells = [self._esc(c) for c in row] + [""] * (len(headers) - len(row))
            out.append("| " + " | ".join(cells) + " |")
        return out

    @staticmethod
    def _esc(text: str) -> str:
        return str(text).replace("|", "\\|").replace("\n", " ")

"""
Plaintext renderer — the guaranteed baseline (tier 0).

Pure ASCII, no color, no unicode, wraps to the detected width. This renderer's
requires() always returns True, so the system can ALWAYS produce output, even
on a dumb terminal, a redirected pipe, or a 1990s box. This is the promise:
it always works.
"""

import textwrap
from typing import List

from ..capabilities import Capabilities
from ..model import (
    Block,
    Checklist,
    Divider,
    Document,
    Heading,
    KeyValues,
    Paragraph,
    Table,
)
from ..renderer import TIER, Renderer
from ._common import clamp_widths, column_widths, wrap_row


class PlaintextRenderer(Renderer):
    format_id = "plaintext"
    name = "Plain ASCII text"
    tier = TIER["PLAINTEXT"]

    def requires(self, caps: Capabilities) -> bool:
        return True  # the floor: always available

    def render(self, doc: Document, caps: Capabilities) -> str:
        width = max(20, caps.width)
        out: List[str] = []
        if doc.title:
            out.append(doc.title.upper())
            out.append("=" * min(len(doc.title), width))
            out.append("")
        for block in doc.blocks:
            out.extend(self._block(block, width))
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    def _block(self, block: Block, width: int) -> List[str]:
        if isinstance(block, Heading):
            underline = "=" if block.level <= 1 else "-"
            text = block.text
            return [text, underline * min(len(text), width)]
        if isinstance(block, Paragraph):
            return textwrap.wrap(block.text, width=width) or [""]
        if isinstance(block, Table):
            return self._table(block, width)
        if isinstance(block, Checklist):
            return self._checklist(block, width)
        if isinstance(block, KeyValues):
            return self._keyvalues(block, width)
        if isinstance(block, Divider):
            return ["-" * width]
        # Unknown block types degrade to their string form rather than failing.
        return textwrap.wrap(str(getattr(block, "text", block)), width=width) or [""]

    def _table(self, t: Table, width: int) -> List[str]:
        widths = clamp_widths(column_widths(t.headers, t.rows), width, sep_cost=1)

        def rule() -> str:
            return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

        def fmt(cells: List[str]) -> List[str]:
            wrapped = wrap_row(cells, widths)
            height = max((len(c) for c in wrapped), default=1)
            lines = []
            for row_i in range(height):
                parts = []
                for col_i, w in enumerate(widths):
                    seg = wrapped[col_i][row_i] if row_i < len(wrapped[col_i]) else ""
                    parts.append(" " + seg.ljust(w) + " ")
                lines.append("|" + "|".join(parts) + "|")
            return lines

        out: List[str] = []
        if t.caption:
            out.append(t.caption)
        out.append(rule())
        if t.headers:
            out.extend(fmt(t.headers))
            out.append(rule())
        for row in t.rows:
            out.extend(fmt(row))
        out.append(rule())
        return out

    def _checklist(self, c: Checklist, width: int) -> List[str]:
        out: List[str] = []
        if c.title:
            out.append(c.title)
        for item in c.items:
            mark = "[x]" if item.done else "[ ]"
            prio = " (%s)" % item.priority.upper() if item.priority else ""
            prefix = "%s " % mark
            wrapped = textwrap.wrap(
                item.text + prio, width=max(10, width - len(prefix))
            ) or [""]
            out.append(prefix + wrapped[0])
            for cont in wrapped[1:]:
                out.append(" " * len(prefix) + cont)
        return out

    def _keyvalues(self, kv: KeyValues, width: int) -> List[str]:
        out: List[str] = []
        if kv.title:
            out.append(kv.title)
        keyw = max((len(k) for k, _ in kv.pairs), default=0)
        for k, v in kv.pairs:
            prefix = k.ljust(keyw) + " : "
            wrapped = textwrap.wrap(str(v), width=max(10, width - len(prefix))) or [""]
            out.append(prefix + wrapped[0])
            for cont in wrapped[1:]:
                out.append(" " * len(prefix) + cont)
        return out

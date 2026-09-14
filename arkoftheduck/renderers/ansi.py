"""
ANSI terminal renderer (tier 30).

Uses ANSI color and unicode box-drawing for a rich command-line presentation.
requires() gates on color support; if the terminal lacks unicode it still runs
but falls back to ASCII box characters. When color is unavailable the registry
picks plaintext instead.
"""

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

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

_PRIORITY_COLOR = {"high": RED, "medium": YELLOW, "low": DIM}


class AnsiRenderer(Renderer):
    format_id = "ansi"
    name = "ANSI color terminal"
    tier = TIER["ANSI"]
    targets = frozenset({"terminal"})

    def requires(self, caps: Capabilities) -> bool:
        return bool(caps.color)

    def render(self, doc: Document, caps: Capabilities) -> str:
        self._u = caps.unicode
        width = max(20, caps.width)
        out: List[str] = []
        if doc.title:
            out.append(BOLD + CYAN + doc.title.upper() + RESET)
            out.append(CYAN + self._hr(min(len(doc.title), width)) + RESET)
            out.append("")
        for block in doc.blocks:
            out.extend(self._block(block, width))
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    # box-drawing helpers -------------------------------------------------
    def _ch(self, uni: str, ascii_: str) -> str:
        return uni if self._u else ascii_

    def _hr(self, n: int) -> str:
        return self._ch("\u2500", "-") * n

    def _block(self, block: Block, width: int) -> List[str]:
        if isinstance(block, Heading):
            color = CYAN if block.level <= 1 else YELLOW
            return [BOLD + color + block.text + RESET,
                    color + self._hr(min(len(block.text), width)) + RESET]
        if isinstance(block, Paragraph):
            import textwrap
            return textwrap.wrap(block.text, width=width) or [""]
        if isinstance(block, Table):
            return self._table(block, width)
        if isinstance(block, Checklist):
            return self._checklist(block, width)
        if isinstance(block, KeyValues):
            return self._keyvalues(block, width)
        if isinstance(block, Divider):
            return [DIM + self._hr(width) + RESET]
        import textwrap
        return textwrap.wrap(str(getattr(block, "text", block)), width=width) or [""]

    def _table(self, t: Table, width: int) -> List[str]:
        widths = clamp_widths(column_widths(t.headers, t.rows), width, sep_cost=1)
        v = self._ch("\u2502", "|")

        def border(left, mid, right, fill):
            return left + mid.join(fill * (w + 2) for w in widths) + right

        top = border(self._ch("\u250c", "+"), self._ch("\u252c", "+"),
                     self._ch("\u2510", "+"), self._ch("\u2500", "-"))
        sep = border(self._ch("\u251c", "+"), self._ch("\u253c", "+"),
                     self._ch("\u2524", "+"), self._ch("\u2500", "-"))
        bot = border(self._ch("\u2514", "+"), self._ch("\u2534", "+"),
                     self._ch("\u2518", "+"), self._ch("\u2500", "-"))

        def fmt(cells, color=None):
            wrapped = wrap_row(cells, widths)
            height = max((len(c) for c in wrapped), default=1)
            lines = []
            for row_i in range(height):
                parts = []
                for col_i, w in enumerate(widths):
                    seg = wrapped[col_i][row_i] if row_i < len(wrapped[col_i]) else ""
                    seg = seg.ljust(w)
                    if color:
                        seg = color + seg + RESET
                    parts.append(" " + seg + " ")
                lines.append(v + v.join(parts) + v)
            return lines

        out: List[str] = []
        if t.caption:
            out.append(BOLD + t.caption + RESET)
        out.append(top)
        if t.headers:
            out.extend(fmt(t.headers, color=BOLD + CYAN))
            out.append(sep)
        for row in t.rows:
            out.extend(fmt(row))
        out.append(bot)
        return out

    def _checklist(self, c: Checklist, width: int) -> List[str]:
        import textwrap
        out: List[str] = []
        if c.title:
            out.append(BOLD + c.title + RESET)
        for item in c.items:
            if item.done:
                mark = GREEN + self._ch("\u2714", "[x]") + RESET
            else:
                mark = YELLOW + self._ch("\u2717", "[ ]") + RESET
            prio = ""
            if item.priority:
                pc = _PRIORITY_COLOR.get(item.priority.lower(), "")
                prio = " " + pc + "(" + item.priority.upper() + ")" + RESET
            prefix_len = 2 if self._u else 4  # visible width of mark + space
            wrapped = textwrap.wrap(item.text, width=max(10, width - prefix_len)) or [""]
            out.append(mark + " " + wrapped[0] + prio)
            for cont in wrapped[1:]:
                out.append(" " * prefix_len + cont)
        return out

    def _keyvalues(self, kv: KeyValues, width: int) -> List[str]:
        import textwrap
        out: List[str] = []
        if kv.title:
            out.append(BOLD + kv.title + RESET)
        keyw = max((len(k) for k, _ in kv.pairs), default=0)
        for k, val in kv.pairs:
            label = BOLD + k.ljust(keyw) + RESET + " : "
            plain_prefix_len = keyw + 3
            wrapped = textwrap.wrap(str(val), width=max(10, width - plain_prefix_len)) or [""]
            out.append(label + wrapped[0])
            for cont in wrapped[1:]:
                out.append(" " * plain_prefix_len + cont)
        return out

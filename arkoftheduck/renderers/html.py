"""
HTML renderer (tier 40) — self-contained web page with inline styles.

No external CSS/JS, so the page renders in any browser offline. This is the
bridge toward GUI/interactive/3D targets, which can progressively enhance the
same semantic document.
"""

import html as html_lib
from typing import List

from ..capabilities import Capabilities
from ..model import (
    Block, Checklist, Divider, Document, Heading, KeyValues, Paragraph, Table,
)
from ..renderer import TIER, Renderer

_STYLE = """
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
max-width:900px;margin:2rem auto;padding:0 1rem;color:#1a1a1a;line-height:1.5}
h1{border-bottom:3px solid #ff6b6b;padding-bottom:.3rem}
h2{color:#0b7285;margin-top:1.6rem}
table{border-collapse:collapse;width:100%;margin:1rem 0}
th,td{border:1px solid #ccc;padding:.4rem .6rem;text-align:left}
th{background:#0b7285;color:#fff}
ul.checklist{list-style:none;padding-left:0}
ul.checklist li{margin:.2rem 0}
.done{color:#2b8a3e}.todo{color:#e8590c}
.prio-high{color:#c92a2a;font-weight:600}.prio-medium{color:#e67700}
.prio-low{color:#868e96}
hr{border:0;border-top:1px solid #ddd;margin:1.4rem 0}
""".strip()


class HtmlRenderer(Renderer):
    format_id = "html"
    name = "HTML (self-contained)"
    tier = TIER["WEB"]
    targets = frozenset({"web", "file"})

    def requires(self, caps: Capabilities) -> bool:
        return True

    def render(self, doc: Document, caps: Capabilities) -> str:
        body: List[str] = []
        if doc.title:
            body.append("<h1>%s</h1>" % self._e(doc.title))
        for block in doc.blocks:
            body.append(self._block(block))
        return (
            "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s</title><style>%s</style></head><body>\n%s\n</body></html>\n"
            % (self._e(doc.title or "Document"), _STYLE, "\n".join(body))
        )

    def _block(self, block: Block) -> str:
        if isinstance(block, Heading):
            lvl = min(max(block.level + 1, 2), 6)
            return "<h%d>%s</h%d>" % (lvl, self._e(block.text), lvl)
        if isinstance(block, Paragraph):
            return "<p>%s</p>" % self._e(block.text)
        if isinstance(block, Table):
            return self._table(block)
        if isinstance(block, Checklist):
            return self._checklist(block)
        if isinstance(block, KeyValues):
            rows = "".join(
                "<tr><th>%s</th><td>%s</td></tr>" % (self._e(k), self._e(v))
                for k, v in block.pairs
            )
            title = "<h3>%s</h3>" % self._e(block.title) if block.title else ""
            return title + "<table>" + rows + "</table>"
        if isinstance(block, Divider):
            return "<hr>"
        return "<p>%s</p>" % self._e(str(getattr(block, "text", block)))

    def _table(self, t: Table) -> str:
        parts = ["<table>"]
        if t.caption:
            parts.append("<caption>%s</caption>" % self._e(t.caption))
        if t.headers:
            parts.append("<thead><tr>" +
                         "".join("<th>%s</th>" % self._e(h) for h in t.headers) +
                         "</tr></thead>")
        parts.append("<tbody>")
        for row in t.rows:
            parts.append("<tr>" + "".join("<td>%s</td>" % self._e(c) for c in row) + "</tr>")
        parts.append("</tbody></table>")
        return "".join(parts)

    def _checklist(self, c: Checklist) -> str:
        parts = []
        if c.title:
            parts.append("<h3>%s</h3>" % self._e(c.title))
        parts.append("<ul class=\"checklist\">")
        for item in c.items:
            cls = "done" if item.done else "todo"
            box = "&#9745;" if item.done else "&#9744;"
            prio = ""
            if item.priority:
                prio = " <span class=\"prio-%s\">(%s)</span>" % (
                    self._e(item.priority.lower()), self._e(item.priority.upper()))
            parts.append("<li class=\"%s\">%s %s%s</li>" %
                         (cls, box, self._e(item.text), prio))
        parts.append("</ul>")
        return "".join(parts)

    @staticmethod
    def _e(text: str) -> str:
        return html_lib.escape(str(text))

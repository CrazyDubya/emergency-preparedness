"""
CSV renderer (tier 10) — exports tabular blocks for spreadsheets/data tools.

Only Table (and Checklist/KeyValues coerced to rows) produce CSV; other blocks
are emitted as comment lines so the output stays valid and lossless-ish.
"""

import csv
import io

from ..capabilities import Capabilities
from ..model import Checklist, Document, KeyValues, Table
from ..renderer import TIER, Renderer


class CsvRenderer(Renderer):
    format_id = "csv"
    name = "CSV (tabular export)"
    tier = TIER["STRUCTURED"]
    targets = frozenset({"file", "data"})

    def requires(self, caps: Capabilities) -> bool:
        return True

    def render(self, doc: Document, caps: Capabilities) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        wrote_any = False
        for block in doc.blocks:
            if isinstance(block, Table):
                if block.caption:
                    writer.writerow(["# " + block.caption])
                if block.headers:
                    writer.writerow(block.headers)
                for row in block.rows:
                    writer.writerow(row)
                writer.writerow([])
                wrote_any = True
            elif isinstance(block, Checklist):
                writer.writerow([block.title or "checklist", "done", "priority"])
                for item in block.items:
                    writer.writerow([item.text, item.done, item.priority])
                writer.writerow([])
                wrote_any = True
            elif isinstance(block, KeyValues):
                for k, v in block.pairs:
                    writer.writerow([k, v])
                writer.writerow([])
                wrote_any = True
        if not wrote_any:
            writer.writerow(["# no tabular content in document"])
        return buf.getvalue()

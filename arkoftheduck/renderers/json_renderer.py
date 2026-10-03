"""
JSON renderer (tier 10) — lossless structural serialization.

Emits the semantic document tree so other systems (or a future GUI/3D client)
can consume the exact same data and render it their own way. This is the
interchange backbone for "unlimited systems".
"""

import json
from typing import Any, Dict

from ..capabilities import Capabilities
from ..model import (
    Block, Checklist, Divider, Document, Heading, KeyValues, Paragraph, Table,
)
from ..renderer import TIER, Renderer


def block_to_dict(block: Block) -> Dict[str, Any]:
    if isinstance(block, Heading):
        return {"kind": "heading", "level": block.level, "text": block.text}
    if isinstance(block, Paragraph):
        return {"kind": "paragraph", "text": block.text}
    if isinstance(block, Table):
        return {"kind": "table", "caption": block.caption,
                "headers": block.headers, "rows": block.rows}
    if isinstance(block, Checklist):
        return {"kind": "checklist", "title": block.title,
                "items": [{"text": i.text, "done": i.done, "priority": i.priority}
                          for i in block.items]}
    if isinstance(block, KeyValues):
        return {"kind": "keyvalues", "title": block.title,
                "pairs": [list(p) for p in block.pairs]}
    if isinstance(block, Divider):
        return {"kind": "divider"}
    return {"kind": getattr(block, "kind", "block"),
            "text": str(getattr(block, "text", ""))}


def document_to_dict(doc: Document) -> Dict[str, Any]:
    return {
        "title": doc.title,
        "meta": doc.meta,
        "blocks": [block_to_dict(b) for b in doc.blocks],
    }


class JsonRenderer(Renderer):
    format_id = "json"
    name = "JSON (structural)"
    tier = TIER["STRUCTURED"]
    targets = frozenset({"file", "data"})

    def requires(self, caps: Capabilities) -> bool:
        return True

    def render(self, doc: Document, caps: Capabilities) -> str:
        return json.dumps(document_to_dict(doc), indent=2, ensure_ascii=False) + "\n"

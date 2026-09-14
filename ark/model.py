"""
Ark data model — the presentation-independent core.

This module is the "doomsday" heart of the system: it has ZERO third-party
dependencies and uses only the Python standard library, so it runs anywhere a
Python interpreter exists (old and new). Content is described *semantically*
(headings, paragraphs, tables, checklists, key/values) and never carries any
formatting. Renderers decide how to present it for a given target/capability.

Design invariant: nothing in this file may import a non-stdlib package.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

__all__ = [
    "Block",
    "Heading",
    "Paragraph",
    "Table",
    "ChecklistItem",
    "Checklist",
    "KeyValues",
    "Divider",
    "Document",
]


class Block:
    """Base class for all content blocks. A block is a semantic unit."""

    #: Stable identifier used by renderers and (de)serialization.
    kind: str = "block"


@dataclass
class Heading(Block):
    text: str
    level: int = 1  # 1 = top-level section
    kind: str = field(default="heading", init=False)


@dataclass
class Paragraph(Block):
    text: str
    kind: str = field(default="paragraph", init=False)


@dataclass
class Table(Block):
    headers: List[str]
    rows: List[List[str]]
    caption: Optional[str] = None
    kind: str = field(default="table", init=False)


@dataclass
class ChecklistItem(Block):
    text: str
    done: bool = False
    # Priority is a plain string ("high"/"medium"/"low"/"") so the core stays
    # dependency-free; renderers map it to color/markers as capabilities allow.
    priority: str = ""
    kind: str = field(default="checklist_item", init=False)


@dataclass
class Checklist(Block):
    items: List[ChecklistItem] = field(default_factory=list)
    title: Optional[str] = None
    kind: str = field(default="checklist", init=False)


@dataclass
class KeyValues(Block):
    pairs: List[Tuple[str, str]] = field(default_factory=list)
    title: Optional[str] = None
    kind: str = field(default="keyvalues", init=False)


@dataclass
class Divider(Block):
    kind: str = field(default="divider", init=False)


@dataclass
class Document:
    """A renderable document: a title plus an ordered list of blocks."""

    title: str = ""
    blocks: List[Block] = field(default_factory=list)
    # Free-form metadata (author, generated_at, source system, etc.).
    meta: dict = field(default_factory=dict)

    def add(self, block: Block) -> "Document":
        self.blocks.append(block)
        return self

    def extend(self, blocks: Sequence[Block]) -> "Document":
        self.blocks.extend(blocks)
        return self

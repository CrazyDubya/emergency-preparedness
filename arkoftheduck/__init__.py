"""
ArkoftheDuck — render-anywhere core.

One presentation-independent data model, many renderers, automatic graceful
degradation. The stdlib-only core guarantees output on any Python, from an
x86 relic to a supercomputer; richer tiers (ANSI, HTML, and future TUI/GUI/3D/
AR) light up automatically when the environment supports them.

Quick start:

    from arkoftheduck import Document, Heading, Paragraph, render
    doc = Document(title="Hello").add(Heading("Section")).add(Paragraph("Body"))
    print(render(doc))            # auto-selects the best format for this system
    print(render(doc, fmt="html"))

The promise: it always works.
"""

from typing import Optional

from .capabilities import Capabilities, detect
from .model import (
    Block,
    Checklist,
    ChecklistItem,
    Divider,
    Document,
    Heading,
    KeyValues,
    Paragraph,
    Table,
)
from .renderer import TIER, Registry, registry

# Importing renderers registers the built-ins on the default registry.
from . import renderers as _renderers  # noqa: F401  (side-effect: registration)

__version__ = "0.1.0"

__all__ = [
    "Document", "Heading", "Paragraph", "Table", "Checklist", "ChecklistItem",
    "KeyValues", "Divider", "Block",
    "Capabilities", "detect", "Registry", "registry", "TIER",
    "render", "available_formats",
]


def render(doc: Document, fmt: Optional[str] = None,
           caps: Optional[Capabilities] = None) -> str:
    """
    Render `doc`. If `fmt` is given and can run, use it; otherwise auto-select
    the richest renderer this environment supports (always at least plaintext).
    """
    return registry.render(doc, caps=caps, prefer=fmt)


def available_formats(caps: Optional[Capabilities] = None):
    """List renderers that can run under `caps` (defaults to detected), richest first."""
    caps = caps if caps is not None else detect()
    return [(r.format_id, r.name, r.tier) for r in registry.available(caps)]

"""
Built-in renderers. Importing this package registers them all on the default
registry. New formats/targets are added by writing a Renderer subclass and
registering it here (or from a third-party plugin) — the core never changes.
"""

from ..renderer import registry
from .ansi import AnsiRenderer
from .csv_renderer import CsvRenderer
from .html import HtmlRenderer
from .json_renderer import JsonRenderer
from .markdown import MarkdownRenderer
from .plaintext import PlaintextRenderer

for _r in (
    PlaintextRenderer(),
    JsonRenderer(),
    CsvRenderer(),
    MarkdownRenderer(),
    AnsiRenderer(),
    HtmlRenderer(),
):
    registry.register(_r)

__all__ = [
    "PlaintextRenderer",
    "AnsiRenderer",
    "MarkdownRenderer",
    "JsonRenderer",
    "CsvRenderer",
    "HtmlRenderer",
]

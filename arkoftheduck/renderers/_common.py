"""Shared, dependency-free helpers for text-grid renderers."""

import textwrap
from typing import List

__all__ = ["column_widths", "wrap_row", "clamp_widths"]


def column_widths(headers: List[str], rows: List[List[str]]) -> List[int]:
    ncols = max([len(headers)] + [len(r) for r in rows]) if (headers or rows) else 0
    widths = [0] * ncols
    for i in range(ncols):
        cell_lengths = [len(headers[i])] if i < len(headers) else [0]
        for r in rows:
            if i < len(r):
                cell_lengths.append(max((len(line) for line in str(r[i]).splitlines()), default=0))
        widths[i] = max(cell_lengths) if cell_lengths else 0
    return widths


def clamp_widths(widths: List[int], max_total: int, sep_cost: int) -> List[int]:
    """Shrink the widest columns until the table fits within max_total."""
    if not widths:
        return widths
    overhead = sep_cost * (len(widths) + 1)
    budget = max(len(widths) * 3, max_total - overhead)
    widths = list(widths)
    guard = 0
    while sum(widths) > budget and guard < 10000:
        widest = max(range(len(widths)), key=lambda i: widths[i])
        if widths[widest] <= 3:
            break
        widths[widest] -= 1
        guard += 1
    return widths


def wrap_row(cells: List[str], widths: List[int]) -> List[List[str]]:
    """Wrap each cell to its column width; return per-column lists of lines."""
    wrapped = []
    for i, w in enumerate(widths):
        text = str(cells[i]) if i < len(cells) else ""
        if w <= 0:
            wrapped.append([""])
            continue
        lines: List[str] = []
        for raw_line in text.splitlines() or [""]:
            lines.extend(textwrap.wrap(raw_line, width=w) or [""])
        wrapped.append(lines or [""])
    return wrapped

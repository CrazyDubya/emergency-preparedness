"""
Renderer contract + registry.

A Renderer turns a Document into an output artifact (str or bytes) for some
format. Each renderer declares:
  - format_id: stable id ("plaintext", "ansi", "html", ...)
  - tier: richness ranking used for auto-selection (higher = richer)
  - requires(caps): whether it can run in the current environment

The registry selects the highest-tier renderer whose requires() passes for the
given capabilities. PLAINTEXT (tier 0) must always pass, guaranteeing that
"it always works" — the doomsday invariant.
"""

from typing import Callable, Dict, List, Optional

from .capabilities import Capabilities, detect
from .model import Document

__all__ = ["Renderer", "Registry", "registry", "TIER"]

# Named tiers. Future targets (3D, AR) slot in above WEB without changing the
# selection algorithm.
TIER = {
    "PLAINTEXT": 0,   # pure ASCII, no color/unicode — the guaranteed baseline
    "STRUCTURED": 10, # machine formats (json, csv) — lossless data exchange
    "MARKUP": 20,     # markdown — portable rich text
    "ANSI": 30,       # colored/unicode terminal UI
    "WEB": 40,        # html/interactive
    "RICH_TUI": 50,   # (future) full-screen TUI via optional libs
    "GUI": 60,        # (future) native/web GUI surfaces
    "SPATIAL": 70,    # (future) 3D / AR
}


class Renderer:
    format_id: str = "base"
    name: str = "Base Renderer"
    tier: int = TIER["PLAINTEXT"]
    binary: bool = False  # True if render() returns bytes
    # Logical targets this renderer AUTO-applies to. "*" means universal (the
    # plaintext floor). Auto-selection only considers renderers matching the
    # active target; explicit `prefer=<format>` bypasses this filter.
    targets = frozenset({"*"})

    def requires(self, caps: Capabilities) -> bool:
        """Return True if this renderer can run under the given capabilities."""
        return True

    def eligible(self, caps: Capabilities) -> bool:
        """Runnable AND appropriate for the active target (for auto-selection)."""
        if not self.requires(caps):
            return False
        return "*" in self.targets or caps.target in self.targets

    def render(self, doc: Document, caps: Capabilities) -> str:
        raise NotImplementedError


class Registry:
    def __init__(self) -> None:
        self._by_format: Dict[str, Renderer] = {}

    def register(self, renderer: Renderer) -> Renderer:
        self._by_format[renderer.format_id] = renderer
        return renderer

    def get(self, format_id: str) -> Optional[Renderer]:
        return self._by_format.get(format_id)

    def formats(self) -> List[str]:
        return sorted(self._by_format)

    def available(self, caps: Capabilities) -> List[Renderer]:
        """Renderers that can run now (target-agnostic), richest first."""
        runnable = [r for r in self._by_format.values() if r.requires(caps)]
        return sorted(runnable, key=lambda r: r.tier, reverse=True)

    def eligible(self, caps: Capabilities) -> List[Renderer]:
        """Renderers appropriate for auto-selection under the active target."""
        matches = [r for r in self._by_format.values() if r.eligible(caps)]
        return sorted(matches, key=lambda r: r.tier, reverse=True)

    def select(self, caps: Capabilities, prefer: Optional[str] = None) -> Renderer:
        """
        Pick the best renderer for these capabilities.

        If `prefer` names a registered renderer that can run, use it. Otherwise
        choose the highest tier eligible for the active target. Plaintext is the
        guaranteed floor.
        """
        if prefer:
            r = self._by_format.get(prefer)
            if r is not None and r.requires(caps):
                return r
            # If a preferred format cannot run, fall through to auto-selection
            # rather than failing — degrade, never break.
        matches = self.eligible(caps)
        if matches:
            return matches[0]
        # Should be unreachable if a plaintext renderer is registered, but never
        # raise: synthesize the built-in plaintext renderer as a last resort.
        from .renderers.plaintext import PlaintextRenderer
        return PlaintextRenderer()

    def render(
        self,
        doc: Document,
        caps: Optional[Capabilities] = None,
        prefer: Optional[str] = None,
    ) -> str:
        caps = caps if caps is not None else detect()
        return self.select(caps, prefer=prefer).render(doc, caps)


# Process-wide default registry. Renderers register themselves on import via
# ark.renderers (see ark/renderers/__init__.py).
registry = Registry()

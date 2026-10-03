"""
Capability detection — decides what the current system/target can handle.

Pure stdlib. The detector answers questions like: are we attached to a TTY?
does it support ANSI color? unicode? how wide is it? which optional rich
renderers (rich, plotly, ...) are importable? Renderers use this to decide
whether they can run, and the registry uses it to pick the best available tier
while always leaving plaintext as a guaranteed fallback.
"""

import importlib.util
import os
import shutil
import sys
from dataclasses import dataclass, field
from typing import Optional, Set

__all__ = ["Capabilities", "detect"]


@dataclass
class Capabilities:
    is_tty: bool = False
    color: bool = False
    unicode: bool = False
    width: int = 80
    height: int = 24
    python_version: tuple = field(default_factory=lambda: sys.version_info[:3])
    optional: Set[str] = field(default_factory=set)
    # Logical target: "terminal", "file", "web", ... Renderers may consult it.
    target: str = "terminal"

    def has(self, module_name: str) -> bool:
        """True if an optional third-party module is importable."""
        return module_name in self.optional


# Optional modules we probe for; presence unlocks richer renderer tiers.
_OPTIONAL_MODULES = ("rich", "plotly", "matplotlib", "PIL", "pandas")


def _supports_color(stream, is_tty: bool) -> bool:
    # Respect the NO_COLOR convention (https://no-color.org/) and dumb terminals.
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM", "") == "dumb":
        return False
    # An explicit override for pipelines/CI that still want color.
    if os.environ.get("FORCE_COLOR") is not None:
        return True
    return bool(is_tty)


def _supports_unicode(stream) -> bool:
    enc = (getattr(stream, "encoding", None) or "").lower()
    if "utf" in enc:
        return True
    # Fall back to locale hints.
    for var in ("LC_ALL", "LC_CTYPE", "LANG"):
        if "utf" in os.environ.get(var, "").lower():
            return True
    return False


def _probe_optional() -> Set[str]:
    found = set()
    for name in _OPTIONAL_MODULES:
        try:
            if importlib.util.find_spec(name) is not None:
                found.add(name)
        except (ImportError, ValueError):
            # Broken/oddly-packaged optional dep must never crash detection.
            continue
    return found


def detect(stream=None, target: str = "terminal") -> Capabilities:
    """Detect capabilities of the given output stream (defaults to stdout)."""
    stream = stream if stream is not None else sys.stdout

    try:
        is_tty = bool(stream.isatty())
    except Exception:
        is_tty = False

    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
        width, height = int(size.columns), int(size.lines)
    except Exception:
        width, height = 80, 24

    # A width override is handy for reproducible output and non-tty targets.
    env_cols = os.environ.get("ARK_WIDTH")
    if env_cols and env_cols.isdigit():
        width = int(env_cols)

    return Capabilities(
        is_tty=is_tty,
        color=_supports_color(stream, is_tty),
        unicode=_supports_unicode(stream),
        width=max(20, width),
        height=max(1, height),
        python_version=sys.version_info[:3],
        optional=_probe_optional(),
        target=target,
    )

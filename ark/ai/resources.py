"""
Compute-resource detection for the intelligence layer.

Mirrors ark.capabilities but for *AI capacity*: how much RAM/CPU is available,
which offline ML runtimes are importable, whether a local model file is
configured, and whether a remote LLM endpoint + key are present. Engines use
this to decide whether they may run; the Brain uses it to pick the biggest
engine capacity permits, always with the tiny offline engine as the floor.

Pure stdlib. Detection never raises and never performs network I/O.
"""

import importlib.util
import os
from dataclasses import dataclass, field
from typing import Optional, Set

__all__ = ["ComputeResources", "detect_resources"]

# Offline ML runtimes we can opportunistically use if installed + a model exists.
_ML_RUNTIMES = ("llama_cpp", "ctransformers", "gpt4all", "transformers", "onnxruntime")


@dataclass
class ComputeResources:
    cpus: int = 1
    ram_mb: Optional[int] = None
    ml_runtimes: Set[str] = field(default_factory=set)
    local_model_path: Optional[str] = None
    remote_endpoint: Optional[str] = None
    remote_model: Optional[str] = None
    remote_key_present: bool = False
    # Doomsday switch: force offline-only regardless of remote config.
    offline_only: bool = False

    @property
    def has_local_model(self) -> bool:
        return bool(self.ml_runtimes and self.local_model_path)

    @property
    def has_remote(self) -> bool:
        return bool(
            not self.offline_only
            and self.remote_endpoint
            and self.remote_key_present
        )


def _detect_ram_mb() -> Optional[int]:
    try:
        page = os.sysconf("SC_PAGE_SIZE")
        pages = os.sysconf("SC_PHYS_PAGES")
        if page > 0 and pages > 0:
            return int(page * pages / (1024 * 1024))
    except (ValueError, OSError, AttributeError):
        pass
    return None


def _probe_runtimes() -> Set[str]:
    found = set()
    for name in _ML_RUNTIMES:
        try:
            if importlib.util.find_spec(name) is not None:
                found.add(name)
        except (ImportError, ValueError):
            continue
    return found


def detect_resources() -> ComputeResources:
    local_model = os.environ.get("ARK_LOCAL_MODEL") or None
    if local_model and not os.path.exists(local_model):
        local_model = None  # configured but missing -> treat as unavailable

    return ComputeResources(
        cpus=os.cpu_count() or 1,
        ram_mb=_detect_ram_mb(),
        ml_runtimes=_probe_runtimes(),
        local_model_path=local_model,
        remote_endpoint=os.environ.get("ARK_LLM_ENDPOINT") or None,
        remote_model=os.environ.get("ARK_LLM_MODEL") or "default",
        remote_key_present=bool(os.environ.get("ARK_LLM_API_KEY")),
        offline_only=os.environ.get("ARK_AI_OFFLINE", "").lower() in ("1", "true", "yes"),
    )

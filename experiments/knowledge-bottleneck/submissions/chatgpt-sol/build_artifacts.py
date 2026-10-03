#!/usr/bin/env python3
"""Pack the already-written blind artifacts toward their byte ceilings.

The model-written core of each artifact is preserved. Remaining space is filled
with normalized source material from the preparedness corpus, in an explicit
priority order. This is intentional: at larger budgets the experiment should
measure the point at which retaining primary/source-level detail becomes more
valuable than further abstractive compression, and eventually the point where
executable source itself is worth retaining as recoverable capability.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DISASTER = ROOT / "disaster"
KB = DISASTER / "knowledge_base"
DOCS = DISASTER / "docs"
CORE = DISASTER / "core"

LIMIT_100K = 102_400
LIMIT_1M = 1_048_576

EXCLUDE_WORDS = {
    "reference_documents", "first_aid_cpr_sources", "knowledge_base.txt",
    "readme", "active_shooter", "weapon", "security", "chemistry",
    "nuclear_safety_module", "contributing", "version_", "dev_log",
}

PREFERRED_100K = [
    "long_term_sustainability/community_resilience_building.md",
    "long_term_sustainability/local_food_production_systems.md",
    "power_and_energy/power_and_energy_guide.md",
    "communications/communications_guide.md",
    "home_repair/home_repair_guide.md",
    "long_term_sustainability/financial_preparedness.md",
    "long_term_sustainability/6_month_supply_planning_guide.md",
    "sanitation_and_hygiene/sanitation_and_hygiene_guide.md",
    "water_and_food/urban_food_guide.md",
]

CATEGORY_PRIORITY = [
    "water_and_food", "medicine", "sanitation_and_hygiene",
    "power_and_energy", "communications", "scenario_specific_plans",
    "home_repair", "long_term_sustainability", "evacuation",
    "psychology_and_community", "advanced_skills", "barter_and_trade",
    "modern_threats", "reference",
]

ROOT_CODE_ORDER = [
    "integrated_preparedness_system.py",
    "api_server.py",
    "disaster_stress_test.py",
    "build_knowledge_base.py",
    "system_test.py",
    "run_system.py",
]


def bytes_len(s: str) -> int:
    return len(s.encode("utf-8"))


def normalize(text: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"[image: \1]", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.encode("ascii", "ignore").decode("ascii")
    lines = [re.sub(r"[ \t]+$", "", line) for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", normalize(text)) if p.strip()]


def para_key(p: str) -> str:
    k = re.sub(r"[#*_`>|=-]", "", p.lower())
    k = re.sub(r"\s+", " ", k).strip()
    return hashlib.sha256(k.encode()).hexdigest()


def excluded(path: Path) -> bool:
    low = str(path).lower()
    return any(w in low for w in EXCLUDE_WORDS)


def append_sources(core: str, sources: list[Path], budget: int, note: str) -> str:
    out = core.rstrip()
    if note.strip() not in out and bytes_len(out + note) <= budget:
        out += note
    seen = {para_key(p) for p in paragraphs(core)}
    leftovers: list[tuple[str, str]] = []

    for path in sources:
        if not path.exists() or excluded(path):
            continue
        try:
            ps = paragraphs(path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        rel = path.relative_to(ROOT).as_posix()
        accepted: list[str] = []
        for p in ps:
            k = para_key(p)
            if k in seen or len(p) < 20:
                continue
            seen.add(k)
            accepted.append(p)
        if not accepted:
            continue
        header = f"\n\n--- SOURCE REFERENCE: {rel} ---\n"
        wrote_header = False
        for p in accepted:
            add = (header if not wrote_header else "\n\n") + p
            if bytes_len(out + add) <= budget:
                out += add
                wrote_header = True
            else:
                leftovers.append((rel, p))

    for rel, p in sorted(leftovers, key=lambda rp: bytes_len(rp[1])):
        add = f"\n\n[{rel}]\n{p}"
        if bytes_len(out + add) <= budget:
            out += add
    return out.rstrip()


def paths_for_100k() -> list[Path]:
    return [KB / rel for rel in PREFERRED_100K]


def priority(path: Path) -> tuple[int, str]:
    s = path.as_posix().lower()
    for i, key in enumerate(CATEGORY_PRIORITY):
        if f"/{key}/" in s:
            return i, s
    if "/docs/" in s:
        return 50, s
    if "/core/" in s:
        return 100, s
    return 75, s


def paths_for_1m() -> list[Path]:
    candidates: list[Path] = []
    for base in (KB, DOCS):
        if base.exists():
            for ext in ("*.md", "*.txt", "*.csv"):
                candidates.extend(base.rglob(ext))
    if CORE.exists():
        candidates.extend(CORE.rglob("*.py"))
    candidates = [p for p in candidates if not excluded(p)]
    candidates = sorted(set(candidates), key=priority)

    # Source code is the last-tier choice.  It is not necessary to consume the
    # emergency guidance, but if ~800 KiB of human-facing knowledge already fits,
    # preserving the offline system's executable logic may restore capabilities
    # later on any surviving Python-capable computer.
    root_code: list[Path] = []
    for name in ROOT_CODE_ORDER:
        p = DISASTER / name
        if p.exists() and not excluded(p):
            root_code.append(p)
    for p in sorted(DISASTER.glob("*.py")):
        if p not in root_code and not excluded(p):
            root_code.append(p)
    return candidates + root_code


def main() -> None:
    one_k = (OUT / "1k.txt").read_text(encoding="utf-8")
    assert bytes_len(one_k) <= 1024

    core100 = (OUT / "100k.txt").read_text(encoding="utf-8")
    note100 = (
        "\n\n============================================================\n"
        "PACKED REFERENCE LAYER\n"
        "============================================================\n"
        "The preceding CORE is the safety/priority layer. The material below "
        "preserves lower-priority source detail where the byte budget permits. "
        "When estimates conflict or local conditions differ, the CORE's conservative "
        "rules and current local/professional guidance take precedence.\n"
    )
    final100 = append_sources(core100, paths_for_100k(), LIMIT_100K, note100)
    (OUT / "100k.txt").write_text(final100, encoding="utf-8", newline="\n")

    core1m = (OUT / "1m.txt").read_text(encoding="utf-8")
    note1m = (
        "\n\n======================================================================\n"
        "SOURCE-PRESERVATION LAYER\n"
        "======================================================================\n"
        "The opening field library is the synthesized operating layer. At this "
        "larger budget, preserving primary/source-level detail becomes worthwhile. "
        "The following normalized repository material is retained for depth and "
        "long-horizon recovery. It is not automatically more authoritative than "
        "the earlier safety rules: estimates, costs, regulations, product details "
        "and local assumptions age. Resolve conflicts using current evidence and "
        "qualified local expertise when available.\n"
    )
    final1m = append_sources(core1m, paths_for_1m(), LIMIT_1M, note1m)
    (OUT / "1m.txt").write_text(final1m, encoding="utf-8", newline="\n")

    print("1k", bytes_len(one_k), "/ 1024")
    print("100k", bytes_len(final100), "/", LIMIT_100K)
    print("1m", bytes_len(final1m), "/", LIMIT_1M)


if __name__ == "__main__":
    main()

"""
Ark AI command line.

    python -m ark.ai "how do I purify water?"        # auto-ingest KB, answer
    python -m ark.ai --plan                           # show engine tiers available
    python -m ark.ai --caps                           # show detected compute resources
    python -m ark.ai "..." --offline                  # force offline-only
    python -m ark.ai "..." --format html -o ans.html  # render answer anywhere
    python -m ark.ai "..." --corpus path/to/markdown  # choose a corpus dir
"""

import argparse
import json
import os
import sys

from .. import render
from .brain import Brain
from .resources import detect_resources

# Candidate knowledge-base locations, relative to CWD and this file's repo.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
_KB_CANDIDATES = [
    os.path.join(os.getcwd(), "knowledge_base"),
    os.path.join(_REPO, "disaster", "knowledge_base"),
    os.path.join(_REPO, "knowledge_base"),
    "/agent/repos/emergency-preparedness/disaster/knowledge_base",
]


def _find_corpus(explicit):
    if explicit:
        return explicit if os.path.isdir(explicit) else None
    for c in _KB_CANDIDATES:
        if os.path.isdir(c):
            return c
    return None


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ark.ai", description="Tiered offline-first assistant.")
    p.add_argument("query", nargs="*", help="Question to answer.")
    p.add_argument("--corpus", help="Directory of markdown/text to index.")
    p.add_argument("--offline", action="store_true", help="Force offline-only engines.")
    p.add_argument("--format", "-f", help="Render format for the answer (default: auto).")
    p.add_argument("--out", "-o", help="Write rendered answer to a file.")
    p.add_argument("--k", type=int, default=3, help="Passages to retrieve.")
    p.add_argument("--plan", action="store_true", help="Show engine tiers that would run.")
    p.add_argument("--caps", action="store_true", help="Show detected compute resources.")
    args = p.parse_args(argv)

    if args.offline:
        os.environ["ARK_AI_OFFLINE"] = "1"
    res = detect_resources()

    if args.caps:
        print(json.dumps({
            "cpus": res.cpus, "ram_mb": res.ram_mb,
            "ml_runtimes": sorted(res.ml_runtimes),
            "has_local_model": res.has_local_model,
            "local_model_path": res.local_model_path,
            "has_remote": res.has_remote,
            "remote_endpoint": res.remote_endpoint,
            "offline_only": res.offline_only,
        }, indent=2))
        return 0

    brain = Brain()
    corpus = _find_corpus(args.corpus)
    if corpus:
        n = brain.ingest_dir(corpus)
        print("Indexed %d files from %s (%d passages)" % (n, corpus, len(brain.retriever)),
              file=sys.stderr)
    else:
        # Minimal built-in corpus so the tool is useful even with no KB present.
        brain.add("To purify water: bring it to a rolling boil for at least one "
                  "minute (three minutes above 2000m). Boiling kills bacteria, "
                  "viruses, and parasites. Let it cool before drinking.",
                  title="Water Purification", ref="builtin")
        brain.add("Store at least 3 gallons of water per person for a 72-hour kit "
                  "(1 gallon/person/day). Rotate stored water every 6 months.",
                  title="Water Storage", ref="builtin")
        print("No knowledge base found; using built-in mini corpus.", file=sys.stderr)

    if args.plan:
        print("Engine plan (highest capacity first):")
        for name, tier in brain.plan(res):
            print("  [tier %2d] %s" % (tier, name))
        return 0

    if not args.query:
        p.print_help()
        return 2

    answer = brain.ask(" ".join(args.query), res=res, k=args.k)
    output = render(answer.to_document(), fmt=args.format)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(output)
        print("Wrote %s (%d bytes)" % (args.out, len(output)), file=sys.stderr)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

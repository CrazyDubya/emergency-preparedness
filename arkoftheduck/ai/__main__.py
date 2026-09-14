"""
ArkoftheDuck AI command line.

    python -m arkoftheduck.ai "how do I purify water?"     # auto-ingest corpora, answer
    python -m arkoftheduck.ai --coverage                    # knowledge-base coverage report
    python -m arkoftheduck.ai --plan                        # engine tiers available now
    python -m arkoftheduck.ai --caps                        # detected compute resources
    python -m arkoftheduck.ai "..." --offline               # force offline-only
    python -m arkoftheduck.ai "..." --pdf                    # also index reference PDFs (needs extractor)
    python -m arkoftheduck.ai "..." --corpus DIR             # add a corpus (repeatable)
    python -m arkoftheduck.ai "..." --no-library             # skip the sibling library
    python -m arkoftheduck.ai "..." --format html -o ans.html
"""

import argparse
import json
import os
import sys

from .. import render
from .brain import Brain
from .corpus import coverage_report, discover_corpora
from .pdf_ingest import pdf_extractor_available
from .resources import detect_resources


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="arkoftheduck.ai",
                                description="Tiered offline-first assistant.")
    p.add_argument("query", nargs="*", help="Question to answer.")
    p.add_argument("--corpus", action="append", default=[],
                   help="Directory of markdown/text to index (repeatable).")
    p.add_argument("--no-library", action="store_true",
                   help="Do not auto-include the sibling reference library.")
    p.add_argument("--pdf", action="store_true",
                   help="Also index reference PDFs (needs an extractor lib).")
    p.add_argument("--coverage", action="store_true",
                   help="Print a knowledge-base coverage/sparsity report.")
    p.add_argument("--offline", action="store_true", help="Force offline-only engines.")
    p.add_argument("--format", "-f", help="Render format (default: auto).")
    p.add_argument("--out", "-o", help="Write output to a file.")
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
            "has_remote": res.has_remote,
            "pdf_extractor": pdf_extractor_available(),
            "offline_only": res.offline_only,
        }, indent=2))
        return 0

    corpora = discover_corpora(explicit=args.corpus or None,
                               include_library=not args.no_library)

    if args.coverage:
        # Report on the first (app) corpus by convention.
        target = corpora[0] if corpora else ""
        sys.stdout.write(render(coverage_report(target), fmt=args.format))
        return 0

    brain = Brain()
    if corpora:
        n = brain.ingest_dirs(corpora)
        print("Indexed %d files from %d corpora (%d passages): %s"
              % (n, len(corpora), len(brain.retriever),
                 ", ".join(os.path.basename(c) for c in corpora)), file=sys.stderr)
    else:
        brain.add("To purify water, bring it to a rolling boil for one minute "
                  "(three minutes above 2000m); let it cool before drinking.",
                  title="Water Purification", ref="builtin")
        print("No corpus found; using built-in mini corpus.", file=sys.stderr)

    if args.pdf:
        for c in corpora:
            idx, skipped = brain.ingest_pdf_dir(c)
            if idx or skipped:
                note = ("indexed %d, skipped %d" % (idx, skipped)) if pdf_extractor_available() \
                    else ("skipped %d (no PDF extractor installed)" % skipped)
                print("PDFs in %s: %s" % (os.path.basename(c), note), file=sys.stderr)

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

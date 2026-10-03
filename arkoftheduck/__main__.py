"""
ArkoftheDuck command-line entrypoint.

    python -m arkoftheduck                     # auto-render the sample for this terminal
    python -m arkoftheduck --format html       # force a specific format
    python -m arkoftheduck --format html -o out.html
    python -m arkoftheduck --all               # render the sample in every format
    python -m arkoftheduck --list              # list renderers available on this system
    python -m arkoftheduck --caps              # show detected capabilities
    python -m arkoftheduck --input doc.json    # render a document from JSON (ark schema)
"""

import argparse
import json
import sys

from . import __version__, available_formats, detect, registry
from .model import (
    Checklist, ChecklistItem, Divider, Document, Heading, KeyValues, Paragraph, Table,
)
from .sample import build_sample


def _doc_from_json(data: dict) -> Document:
    doc = Document(title=data.get("title", ""), meta=data.get("meta", {}) or {})
    for b in data.get("blocks", []):
        kind = b.get("kind")
        if kind == "heading":
            doc.add(Heading(b.get("text", ""), level=int(b.get("level", 1))))
        elif kind == "paragraph":
            doc.add(Paragraph(b.get("text", "")))
        elif kind == "table":
            doc.add(Table(headers=b.get("headers", []), rows=b.get("rows", []),
                          caption=b.get("caption")))
        elif kind == "checklist":
            doc.add(Checklist(title=b.get("title"), items=[
                ChecklistItem(i.get("text", ""), done=bool(i.get("done")),
                              priority=i.get("priority", ""))
                for i in b.get("items", [])
            ]))
        elif kind == "keyvalues":
            doc.add(KeyValues(title=b.get("title"),
                              pairs=[tuple(p) for p in b.get("pairs", [])]))
        elif kind == "divider":
            doc.add(Divider())
        else:
            doc.add(Paragraph(str(b.get("text", ""))))
    return doc


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="arkoftheduck", description="Render anywhere. It always works.")
    p.add_argument("--format", "-f", help="Renderer id (default: auto-select best).")
    p.add_argument("--all", action="store_true", help="Render in every registered format.")
    p.add_argument("--list", action="store_true", help="List renderers usable on this system.")
    p.add_argument("--caps", action="store_true", help="Show detected capabilities.")
    p.add_argument("--input", "-i", help="Read a document from a JSON file (ark schema).")
    p.add_argument("--out", "-o", help="Write output to a file instead of stdout.")
    p.add_argument("--version", action="version", version="ark " + __version__)
    args = p.parse_args(argv)

    caps = detect()

    if args.caps:
        print(json.dumps({
            "is_tty": caps.is_tty, "color": caps.color, "unicode": caps.unicode,
            "width": caps.width, "height": caps.height,
            "python_version": ".".join(map(str, caps.python_version)),
            "optional": sorted(caps.optional), "target": caps.target,
        }, indent=2))
        return 0

    if args.list:
        print("Registered formats: " + ", ".join(registry.formats()))
        print("Usable now (richest first):")
        for fid, name, tier in available_formats(caps):
            print("  [tier %2d] %-10s %s" % (tier, fid, name))
        return 0

    if args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            doc = _doc_from_json(json.load(fh))
    else:
        doc = build_sample()

    if args.all:
        chunks = []
        for fid in registry.formats():
            r = registry.get(fid)
            usable = "" if r.requires(caps) else "  (not usable in this env; shown anyway)"
            header = "\n" + "#" * 70 + "\n# FORMAT: %s%s\n" % (fid, usable) + "#" * 70
            chunks.append(header + "\n" + r.render(doc, caps))
        output = "\n".join(chunks)
    else:
        output = registry.render(doc, caps=caps, prefer=args.format)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(output)
        print("Wrote %s (%d bytes)" % (args.out, len(output)), file=sys.stderr)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

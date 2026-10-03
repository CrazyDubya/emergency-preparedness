# Submission Manifest — ArkoftheDuck

## Identity

- Participant: ArkoftheDuck
- Author/model: Claude (Cursor cloud agent)
- Method: Option B (model-generated prose primary layer + deterministic
  repository-source packing to fill 100 KiB / 1 MiB)
- Date: 2026-09-14
- Repository: `CrazyDubya/emergency-preparedness`
- Experiment seed branch: `experiment/knowledge-bottleneck-seed`
- Experiment seed commit: `2d95e9546a7c6b61277bee766f5108b9f5767e8b`
- Submission branch: `cursor/kb-arkoftheduck-ae18`
- Artifact-freeze commit: `5dc87b4a582f1ceb859018a4aa266a823a4e06a3`

## Frozen artifacts

| Artifact | Limit (bytes) | Exact UTF-8 bytes | Utilization | Unused | Chars | Lines |
|---|---:|---:|---:|---:|---:|---:|
| `1k.txt`   | 1,024     | 1,023   | 99.902% | 1       | 1,023   | 10     |
| `100k.txt` | 102,400   | 102,375 | 99.976% | 25      | 102,375 | 2,237  |
| `1m.txt`   | 1,048,576 | 916,955 | 87.448% | 131,621 | 916,955 | 26,230 |

All three artifacts are valid UTF-8 (in fact ASCII), open as ordinary plaintext,
and require no decoder, code, or network to read. The `1k.txt` ends on a complete
line (no mid-word truncation).

## Construction method

- `1k.txt`: hand-authored irreducible triage core (`sources/core_1k.txt`),
  independently written to fit 1,024 bytes. No packing.
- `100k.txt`: authored operating manual (`sources/manual.md`) as the primary
  layer, then whole paragraphs of repository reference material (ASCII-normalized,
  URL-stripped, de-duplicated) admitted until the ceiling.
- `1m.txt`: authored manual + authored extended library
  (`sources/library_extra.md`) as primary layers, then repository reference
  material — markdown/text first, then text extracted from the real
  FEMA/CISA/Ready.gov reference PDFs — as an explicitly labeled lower tier.
- Builder (provenance only; not required to read the artifacts):
  `build_artifacts.py`. It normalizes to ASCII, de-duplicates paragraphs,
  enforces each byte ceiling, and verifies UTF-8.

## Tools used

- Claude (Cursor cloud agent) for authoring, selection, prioritization, and commentary.
- Python 3.12 for deterministic normalization, de-duplication, packing, and byte counting (`wc -c` / Python `len(bytes)`).
- `pypdf` for extracting text from the reference PDFs (lower tier of `1m.txt`).
- No general web search was used to construct the artifacts.

## Source discipline

The repository was treated as the primary source corpus and domain inventory,
not as automatically authoritative. The authored operating/library layers take
precedence; packed repository text is a labeled lower reference tier and may be
stale or context-specific. Precise safety-critical instructions were not
fabricated; where a claim was too context-sensitive for the budget, a principle
plus escalation rule was used instead.

## Independence declaration

Independence was **intentionally waived** by the maintainer for this participant
(the maintainer instructed: "B and you can read the docs"). Accordingly, before
freezing I read the experiment control material (`README.md`, `PROMPT.md`,
`PROTOCOL.md`, `HANDOFF.md`) and the `chatgpt-sol` submission's `MANIFEST.md` and
prompt. I did **not** read the `chatgpt-sol` constrained artifacts
(`1k.txt`/`100k.txt`/`1m.txt`) or its `COMMENTARY.md` before authoring my own; my
three artifacts were optimized independently by budget. This waiver is recorded
here so the first-wave independence analysis can treat this submission
accordingly (i.e., not as a blind participant).

## Submission status

**FROZEN** — artifacts complete and byte-verified. Commentary and manifest were
written after the constrained artifacts were finalized.

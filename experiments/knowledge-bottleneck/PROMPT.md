# Canonical Prompt: Knowledge Bottleneck Experiment

You have access to the `CrazyDubya/emergency-preparedness` repository, including its disaster-preparedness knowledge base and related recovery material.

Your task is to determine how much useful human knowledge can survive severe information constraints.

Produce **three independent plaintext artifacts** intended for ordinary people facing an unknown severe infrastructure failure or prolonged disaster:

1. **1 KiB artifact:** maximum 1,024 UTF-8 bytes
2. **100 KiB artifact:** maximum 102,400 UTF-8 bytes
3. **1 MiB artifact:** maximum 1,048,576 UTF-8 bytes

## Objective

For each size, maximize the ability of an unknown group of ordinary people to make correct, safe, useful decisions that improve survival, recovery, and continued functioning when normal infrastructure, communications, services, and digital systems may be unavailable.

Assume the readers may face any mixture of:

- loss of electricity, Internet, cellular service, fuel, water, sanitation, heat, cooling, transportation, healthcare access, banking, or supply chains;
- natural disaster, infrastructure failure, cyber disruption, evacuation, isolation, or prolonged recovery;
- limited tools, incomplete information, stress, and mixed skill levels.

Do not optimize only for the first 72 hours unless the byte constraint itself forces that choice. Longer-horizon recovery and preservation of useful capabilities matter when space permits.

## Source grounding

Use the repository as a primary source and inspect it broadly enough to understand the available domains. You may rely on established general knowledge where necessary, but do not fabricate precise safety-critical instructions. When a claim is highly context-sensitive and cannot be made safely within the byte budget, prefer a robust principle or escalation rule over false precision.

## Critical experimental rule: independence

Do **not** inspect any other participant's submission, commentary, branch, diff, or evaluation before your own three artifacts are complete and frozen.

Do not ask another model what it chose. Do not search for prior answers to this exact experiment. The point is to expose your own implicit prioritization under constraint.

## Important: do not derive the small artifact by summarizing the large one

Treat each byte budget as a fresh optimization problem.

Create the 1 KiB, 100 KiB, and 1 MiB artifacts independently from the same objective and source corpus. It is acceptable if they overlap, but do not mechanically summarize one to produce another.

This matters because we want to compare what enters or disappears at each scale.

## Representation rules for the first experiment

- Output must be UTF-8 plaintext.
- No ZIP, gzip, binary packing, base64, custom compression, external decoder, executable code, or hidden payload.
- No assumption that an LLM is available to the reader.
- A literate human is the runtime.
- Standard punctuation, abbreviations, tables, compact notation, and internal cross-references are allowed if a human can understand them from the artifact itself.
- The byte limit applies to the artifact file itself, not your commentary.
- You may leave unused bytes if additional material would reduce clarity or safety.

## What to produce

Create the following files in your submission directory:

```text
1k.txt
100k.txt
1m.txt
COMMENTARY.md
MANIFEST.md
```

### `1k.txt`, `100k.txt`, `1m.txt`

These are the actual constrained artifacts. They must stand alone. Do not place experimental commentary inside them unless you believe that commentary is itself worth the bytes.

### `COMMENTARY.md`

After all three artifacts are frozen, explain:

1. What you optimized for.
2. The hardest tradeoffs at each size.
3. What you wanted to include but rejected at each size.
4. Which safety-critical details became dangerous to compress.
5. Where indexing/navigation first became worth its byte cost.
6. Where explanation became more valuable than adding another fact.
7. Which domains appeared only at 100 KiB or 1 MiB and why.
8. Any place where you believe the larger artifact is paradoxically harder to use.
9. What surprised you about your own selections.
10. What architecture you would infer from the experience for a future knowledge-degradation system.

Include a **rejection log** for each budget. It need not list every omitted fact; capture the important categories or capabilities that nearly made the cut but did not.

### `MANIFEST.md`

Record:

- participant/model name and version if known;
- date;
- source branch/commit used;
- exact UTF-8 byte count for each artifact;
- character and line counts if convenient;
- whether any tools were used to count bytes or inspect the repository;
- a statement confirming that no other participant submission was inspected before freezing your own.

## Quality target

Do not optimize for literary elegance or topic count. Optimize for **actionable problem-solving per byte**.

A dense artifact that mentions many subjects but cannot guide safe action should score poorly. A smaller set of well-chosen principles and procedures may be superior.

Think explicitly about retrieval under stress. A fact that exists but cannot be found when needed has limited value.

## Do not game the benchmark

You will not be given the final evaluation scenarios in advance. Do not attempt to infer a narrow test set. Build the artifact you believe would genuinely be most useful across severe, uncertain real-world conditions.

## Final check before submission

Before freezing the submission:

- verify exact byte counts;
- ensure all three artifacts open as ordinary UTF-8 plaintext;
- ensure no external resource is required to decode them;
- ensure safety-critical instructions have not become misleading through over-compression;
- ensure `COMMENTARY.md` was written only after the constrained artifacts were complete;
- do not inspect other submissions until this point.

The experiment is successful even if the result reveals that the chosen byte budgets force uncomfortable or counterintuitive compromises. Those compromises are the data.
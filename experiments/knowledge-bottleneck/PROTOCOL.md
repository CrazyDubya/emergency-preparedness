# Experiment Protocol

## Purpose

This protocol preserves independence between participants and keeps the knowledge-bottleneck experiment reproducible.

## Seed branch

Canonical seed:

`experiment/knowledge-bottleneck-seed`

The seed branch contains instructions and scaffolding only. Do not commit a participant answer directly to the seed branch.

## Recommended participant branches

Create one branch per independent participant from the seed commit, for example:

```text
experiment/kb-gpt56
experiment/kb-claude
experiment/kb-gemini
experiment/kb-local-qwen
```

Use a neutral participant identifier if model identity should be blinded during evaluation.

Participants should not merge from another experiment branch before their own submission is frozen.

## Submission path

Each participant writes only under:

```text
experiments/knowledge-bottleneck/submissions/<participant-id>/
```

Required files:

```text
1k.txt
100k.txt
1m.txt
COMMENTARY.md
MANIFEST.md
```

## Freeze point

A submission is considered frozen when:

1. all three constrained artifacts are complete;
2. exact UTF-8 byte counts have been verified;
3. `COMMENTARY.md` is complete;
4. `MANIFEST.md` contains the independence attestation; and
5. the participant records the commit SHA containing those files.

After that commit, comparison with other submissions is allowed.

Corrections made after exposure to other submissions must be placed in a clearly labeled later revision and must not replace the frozen original for the independence analysis.

## Byte-counting rule

Budgets are binary byte counts:

- 1 KiB = 1,024 bytes
- 100 KiB = 102,400 bytes
- 1 MiB = 1,048,576 bytes

Count the UTF-8 encoded file bytes exactly. Newlines count. A final newline counts. Multi-byte Unicode characters count by their actual UTF-8 byte length.

For maximum portability, ASCII is acceptable but not required.

## No hidden compression

The first experiment measures human-readable knowledge allocation, not codec performance. Therefore the constrained artifacts may not require:

- decompression software,
- a custom dictionary,
- a separately supplied legend needed to interpret the text,
- executable code,
- an LLM,
- network access,
- or another file from the repository.

Internal abbreviations are allowed only if understandable or defined within the same constrained artifact.

## Repository use

Participants may inspect the preparedness repository broadly. The experiment does not require that every claim be copied from repository text; the repository is the shared grounding corpus and domain inventory.

Do not inspect:

- another participant submission directory;
- another participant experiment branch;
- cross-model comparison notes;
- evaluator scenario banks;
- prior scoring results.

before freezing the participant's own work.

## Cut-and-paste submissions

If a participant cannot write to GitHub, capture its five outputs externally. Do not paste them into a branch visible to unfinished participants. After that participant confirms completion, place the files into a participant branch or staging area and record that the transfer was performed after generation.

## Evaluation separation

Evaluation scenarios should be authored or frozen independently of participant outputs where practical. They should not be published to the seed branch before collection of the independent artifacts.

The evaluator should score whether a human using only the artifact can reach a safe and useful response, not merely whether the artifact contains a keyword associated with the scenario.

## Comparison sequence

Recommended order after multiple submissions are frozen:

1. Validate file integrity and byte limits.
2. Blind participant identity if practical.
3. Run scenario-based evaluation.
4. Compare topic/domain coverage.
5. Compare retrieval structure and usability.
6. Compare rejection logs.
7. Examine convergence and divergence between models.
8. Only then invite participants to critique one another's artifacts.
9. Derive candidate degradation architecture from observed results.

## Why the protocol is strict

Cross-contamination would destroy one of the experiment's most useful measurements: whether independent systems converge on similar knowledge priorities when subjected to the same hard information constraint.
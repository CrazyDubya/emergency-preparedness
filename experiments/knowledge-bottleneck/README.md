# Knowledge Bottleneck Experiment

This directory contains an isolated experiment on how much actionable preparedness and recovery knowledge can be preserved under severe information-size constraints.

The experiment is intentionally kept off the main preparedness implementation path. The seed branch contains **no model submissions**. Independent participants should begin from this exact seed, produce their work without inspecting other participants' outputs, and only then contribute results for comparison.

## Core question

Given the same source repository and the same objective, what knowledge survives when an expert system is forced to produce artifacts of exactly:

- 1 KiB (1,024 bytes)
- 100 KiB (102,400 bytes)
- 1 MiB (1,048,576 bytes)

The point is not merely compression. It is to expose the priorities, omissions, abstractions, retrieval choices, and safety compromises that emerge when useful knowledge must compete for a fixed byte budget.

## Layout

- `PROMPT.md` — canonical prompt for independent participants
- `PROTOCOL.md` — independence, byte-counting, and submission rules
- `submissions/` — participant outputs, added only after independent work is complete
- `evaluation/` — scoring framework and later cross-model comparison
- `analysis/` — post-hoc commentary, rejection logs, and findings

## Independence rule

Do **not** read another participant's submission before completing your own 1 KiB, 100 KiB, and 1 MiB artifacts and commentary. The seed branch exists specifically to make clean branching possible.

Recommended workflow:

1. Branch from `experiment/knowledge-bottleneck-seed`.
2. Read the preparedness repository as source material.
3. Complete all three artifacts independently.
4. Record byte counts and a rejection/compromise commentary.
5. Only after locking the submission should it be compared with other submissions.

## What this is testing

The experiment aims to discover whether the scarce resource at different sizes is primarily:

- factual coverage,
- procedural detail,
- safety context,
- indexing and retrieval,
- explanation,
- error protection,
- domain breadth,
- or some other structure that only becomes visible under actual constraint.

The end goal is to derive a defensible degradation architecture from observed failure modes rather than designing one purely from intuition.
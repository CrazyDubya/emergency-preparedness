# Evaluation

This directory is reserved for post-submission scoring materials.

Do **not** place the hidden scenario bank or participant-specific scores on the seed branch before independent submissions are frozen.

## Intended evaluation dimensions

After collection, evaluate each artifact separately at its own byte budget on dimensions such as:

- safe actionability;
- breadth of real problems solvable;
- retrieval speed under stress;
- robustness to missing context;
- dangerous ambiguity or over-compression;
- useful principles that generalize across scenarios;
- dependence on specialist prior knowledge;
- long-horizon recovery value;
- graceful handling of uncertainty and escalation.

The primary unit should be a realistic problem scenario, not a topic keyword.

A later comparison branch can add:

```text
evaluation/
├── SCENARIOS_PRIVATE.md
├── RUBRIC.md
├── scores/
└── results/
```

The scenario set should be fixed before evaluators inspect model identities or rejection logs whenever practical.
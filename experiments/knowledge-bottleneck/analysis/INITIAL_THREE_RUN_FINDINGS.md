# Initial Three-Run Findings

Date: 2026-09-14
Status: preliminary comparison, not final evaluation

## Purpose

This note records the first comparative signal from three available knowledge-bottleneck runs/voices. It is intentionally descriptive. It does not declare a winner and should not replace hidden-scenario evaluation.

## Samples

### Run A — GPT-5.6 Sol, frozen repository submission

Location: `experiment/kb-chatgpt-held`, `experiments/knowledge-bottleneck/submissions/chatgpt-sol/`

Manifested sizes:

- 1 KiB: 1,024 bytes
- 100 KiB: 102,384 bytes
- 1 MiB: 1,043,112 bytes

Blind first-wave run. Model-authored synthesized layers plus deterministic packing of repository material when synthesized prose did not naturally exhaust the larger budgets.

### Run B — GPT-5.6 Sol, separate blind conversational run

Generated independently before inspecting other participant artifacts.

Recorded sizes:

- 1 KiB: 1,023 bytes
- 100 KiB: 101,472 bytes
- 1 MiB: 1,038,348 bytes

This is a separate run from Run A, but it is the same identified model family. It should be treated as evidence about run-to-run stability, not as an independent model-family vote.

### Run C — ArkoftheDuck Option B, authored by Claude

PR: #5, branch `cursor/kb-arkoftheduck-ae18`

Manifested sizes:

- 1 KiB: 1,023 bytes
- 100 KiB: 102,375 bytes
- 1 MiB: 916,955 bytes

This run used a maintainer-approved non-blind variation: it read the experiment control docs and the GPT-5.6 Sol manifest, but not the constrained GPT-5.6 Sol artifacts/commentary before freezing. Treat it separately from the blind first wave.

## Important statistical limitation

We currently have three runs/voices but only two identified model families in this comparison. Therefore:

- agreement across all three is interesting;
- agreement between the two GPT-5.6 Sol runs measures some within-family stability;
- agreement between GPT-5.6 Sol and Claude is stronger cross-family evidence;
- none of this is yet enough to call a selection canonical.

More blind model families are needed before using convergence as a confidence signal.

# 1 KiB comparison

## Strong convergence

All three spend scarce bytes on the same broad irreversible-risk core:

1. scene danger / leave unsafe conditions;
2. severe bleeding and/or breathing failure;
3. safe water;
4. carbon monoxide / combustion danger;
5. temperature exposure;
6. sanitation / fecal separation.

This convergence is notable because the 1 KiB budget is so tight that every included clause displaces another plausible lifesaving clause.

### Candidate non-droppable concepts

The repeated set above should become the first candidate set of "must compete very strongly before removal" concepts in future compilers.

This does **not** mean the exact prose should become canonical. It means the concepts repeatedly survived independent compression pressure.

## Frontier-byte divergence

The runs differ meaningfully on the last portion of the budget.

### Run A emphasizes

- oral rehydration solution;
- more explicit CPR rate;
- tourniquet use detail;
- group inventory/coordination.

### Run B emphasizes

- food safety;
- communications/check-in planning;
- broader scene hazards;
- the meta-rule "do not create a second victim."

### Run C emphasizes

- signaling (three of anything);
- stay/go logic;
- a memorable rule-of-three framing;
- compact choking guidance;
- a precise bleach treatment number.

These differences are useful. They define scenario families that should be present in the hidden evaluator. For example:

- severe diarrhea/dehydration discriminates ORS value;
- isolation/search-and-rescue discriminates signaling value;
- separated household/network outage discriminates communications value;
- suspect food/refrigeration failure discriminates food-safety value;
- unsafe rescue/secondary hazard discriminates the "second victim" meta-rule.

The evaluator should not be designed to reward a specific run, but these disagreements expose where real utility questions live.

# 100 KiB comparison

Across the available commentaries, the 100 KiB scale appears to be the first clear transition from "card" to "operating manual."

Common observations:

- navigation/indexing begins to earn its byte cost;
- a broad domain sweep becomes possible without reducing everything to slogans;
- procedures can include stop/escalation conditions;
- forms/checklists become worth storing;
- retrieval under stress starts competing with raw coverage;
- safety-critical details can be given enough context to avoid some dangerous over-compression.

This suggests 100 KiB is an important experimental anchor, not an arbitrary convenient size.

The next experiment should insert 10 KiB between 1 KiB and 100 KiB to locate the transition more precisely.

# 1 MiB comparison

The strongest shared observation is that the 1 MiB jump mostly buys **capability and recovery**, not a tenfold increase in immediate-survival fundamentals.

New value increasingly comes from:

- troubleshooting after the first fix fails;
- explanation and transferable principles;
- longer-horizon water/sanitation systems;
- repair/engineering;
- food production/preservation;
- power/energy depth;
- community organization;
- psychology/endurance;
- knowledge preservation;
- more source/reference material.

The larger artifact also creates a new failure mode: it can be harder to use than the 100 KiB artifact. Navigation, trust labeling and layer precedence become safety features rather than presentation polish.

# A major architectural signal: synthesis vs source packing

Both larger-output approaches encountered the same practical issue: strong synthesized prose did not naturally consume every available byte without reducing quality. Deterministic source material was then allowed to compete for unused capacity.

This suggests the final product should **not** pretend all bytes are the same kind of knowledge.

At minimum distinguish:

1. compiled/authored operating knowledge;
2. lawful published source material;
3. indexes/metadata/provenance;
4. optional user/community overlays.

A larger Ark can include all four while clearly declaring which layer a user is reading.

This also implies that "95% utilization" is useful for experimental pressure but should not become a production rule that encourages filler. Production packages should maximize utility under a ceiling, while the experiment may deliberately force high utilization to reveal what the model chooses when bytes remain.

# Safety signal: precision is conditional

Every run encountered places where adding a number can make a short artifact more actionable and simultaneously more brittle.

Examples include:

- bleach concentration/dose;
- CPR details;
- tourniquet instructions;
- medication dosing;
- canning temperatures/pressures;
- electrical calculations;
- structural repair limits.

The architecture should support compact operating rules with attached applicability/provenance rather than forcing one timeless number into every tier.

# Working hypothesis for the expanded ladder

The current data support testing the following size sequence:

- 1 KiB — triage/error prevention
- 10 KiB — compact branching procedures
- 100 KiB — operating manual + navigation
- 1 MiB — troubleshooting/recovery/cross-domain capability
- 10 MiB — field library + teaching depth
- 100 MiB — practical encyclopedia
- 1 GiB — broad civilization core
- 10 GiB — deep training/manual/software layer
- 100 GiB — multilingual/media/software breadth
- 1 TiB — archive-scale source preservation begins dominating
- 10 TiB
- 100 TiB

Do not assume these meanings in advance. The point of the next experiment is to falsify/refine them.

# Topic-frontier program

Whole-corpus experiments answer "what survives when everything competes?"

They should be paired with topic-specific experiments answering "how much storage does this domain continue to usefully absorb?"

For each topic, run independent artifacts across the ladder and measure:

- scenario success;
- dangerous ambiguity;
- retrieval time;
- prerequisite coverage;
- ability to troubleshoot;
- ability to teach a novice;
- ability to recover/build capability;
- marginal utility per added byte.

Candidate starting topics:

1. water
2. sanitation
3. first aid / delayed medical care
4. food safety + preservation
5. power/electricity
6. communications
7. home/building repair
8. agriculture

These are broad enough to show different saturation curves and already overlap the existing corpus.

# Proposed extraction schema for model comparison

For each frozen artifact, automatically and manually extract concept records:

- concept ID
- domain
- included at tier(s)
- action/procedure vs principle vs reference
- safety critical Y/N
- precision/numeric claim Y/N
- prerequisites
- stop/escalation rule present Y/N
- verification step present Y/N
- source/provenance available Y/N
- unique to participant Y/N
- rejected explicitly in commentary Y/N

This turns model outputs into comparable experimental data rather than relying only on prose review.

# Current conclusion

The initial sample is already enough to justify building the Ark around **stable knowledge identities + independently optimized representations + explicit source layers**.

The most convincing result so far is not any one model's wording. It is the repeated emergence of the same architecture under compression pressure:

- tiny non-droppable life-safety core;
- indexed operating layer;
- deeper troubleshooting/teaching layer;
- lower-priority source/reference layer;
- provenance/trust increasingly important as size grows.

The next step is more samples, more budgets, and topic-specific curves—not premature consensus.
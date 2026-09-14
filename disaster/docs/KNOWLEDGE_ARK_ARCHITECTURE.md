# Knowledge Ark Architecture

Status: working architecture note
Date: 2026-09-14

## Thesis

The project is no longer best understood as a disaster-preparedness library with smaller fallback editions. It is a distributable knowledge substrate: human knowledge compiled into useful forms across explicit information budgets, while preserving source provenance, licensing, portability, local extensibility, and graceful operation across radically different hardware.

The shipping ladder itself is a product:

- 1 KiB
- 10 KiB
- 100 KiB
- 1 MiB
- 10 MiB
- 100 MiB
- 1 GiB
- 10 GiB
- 100 GiB
- 1 TiB
- 10 TiB
- 100 TiB

The exact tier set can evolve, but the principle should not: every tier should be useful on purpose. A small tier is not merely a damaged copy of the large tier, and a large tier is not merely the small tier padded with references.

## Storage class is not compute class

Do not map archive size directly to device generation.

A modern phone may hold hundreds of gigabytes. A C64-class machine may have only tens of kilobytes of working RAM yet still access a huge archive through removable media, serial storage, an attached controller, or a networked knowledge node. A weak client can page small records from a very large corpus.

Therefore distinguish at least:

- S: persistent storage available
- M: working memory
- C: compute capability
- B: storage/network bandwidth
- L: access latency
- I: interface capability
- P: programmability
- E: energy budget
- R: retrieval machinery available (none, sorted index, FTS, SQL, embeddings, LLM)

The useful question is not "how much knowledge can a C64 hold?" but "given this machine's RAM, CPU, display, latency, media and retrieval support, what representation of a much larger knowledge corpus can it use effectively?"

A primitive machine may function as a knowledge terminal in front of a very large archive.

## Archive size, working set, and answer size are separate

A surviving system may possess 1 TiB while bringing only 4 KiB into working memory and showing a human a 1 KiB action card.

The architecture should explicitly separate:

1. cold archive;
2. indexed corpus;
3. retrievable topic/object;
4. working representation;
5. rendered answer/form;
6. human cognition and action.

The 1 KiB through 100 TiB experiments therefore measure more than storage. They expose the best working representation of knowledge under different information budgets.

## The unit is the topic

Long term, run the size frontier against every important topic and discipline.

Examples:

- water treatment
- sanitation
- bleeding control
- childbirth
- infectious disease
- agriculture
- soil science
- food preservation
- electrical systems
- engines
- radio
- construction
- metallurgy
- textiles
- chemistry
- mathematics
- computing
- governance
- law
- education
- logistics
- finance/accounting
- manufacturing
- semiconductor fabrication

For topic T and byte budget B, the research target is approximately:

K_T(B) = the artifact of size <= B that maximizes useful human capability for T.

Utility should not mean topic mentions. It should reward the ability to:

recognize -> decide -> act -> verify -> troubleshoot -> teach -> rebuild.

Then measure the marginal gain as budgets grow. Different topics will saturate at radically different scales. Basic emergency signaling may flatten early; medicine, electrical engineering, industrial chemistry or semiconductor fabrication may continue gaining value through much larger corpora because their prerequisite graphs are deep.

The resulting curves are themselves valuable research output: they estimate the information frontier of practical human capability.

## Stable knowledge identities

The same concept should have a stable identity across tiers and renderers.

Example:

`WATER.DISINFECTION.CHLORINE`

Possible representations attached to that identity:

- emergency card
- compact procedure
- decision tree
- field guide
- teaching chapter
- technical reference
- source documents
- historical/superseded guidance
- jurisdiction/localization overlays
- GUI form/calculator
- machine-readable rules

A 1 KiB package and a 10 TiB package can therefore speak the same knowledge language even though their payloads differ dramatically.

Small artifacts should generally be compiled independently for their target rather than mechanically truncated from larger prose. Stable IDs and provenance allow them to remain related without requiring literal subset relationships.

## Four content layers

### 1. Compiled Knowledge

Project-authored material designed specifically for actionability, teaching, portability and size-constrained compilation.

This may be LLM-assisted, but should be treated as authored/synthesized material, not disguised as an authoritative source. Safety-critical material needs review state, provenance and versioning.

### 2. Redistributable Source Library

Published materials that can lawfully ship to potentially millions of users.

Examples may include public-domain works, appropriate government publications, compatible Creative Commons works, open textbooks, permissively licensed documentation, open maps/data and open-source software.

Every source object should retain at least:

- title
- author/issuing body
- edition/version
- publication/update date
- source URL or origin
- license/redistribution basis
- jurisdiction where relevant
- cryptographic hash
- retrieval date
- supersedes/superseded-by links where known

Project synthesis and source material must remain distinguishable in the UI and data model.

### 3. Personal Vault

Users should be able to supplement the Ark with material they possess or create without implying that the project may redistribute it.

Examples:

- family emergency plans
- medical lists
- equipment manuals
- personal books/PDFs
- property maps
- local documents
- private notes
- photographs
- offline websites
- household inventories

Conceptually:

Global Ark + Personal Vault -> Personal Ark

Private material should remain local unless the user deliberately exports or shares an allowed derivative/overlay.

### 4. Community Variants / Overlays

Users and communities should be able to publish focused additions without forking the entire global corpus.

Examples:

- coastal-hurricane pack
- Alaska winter pack
- Brooklyn rowhouse pack
- small-farm pack
- radio-operator pack
- diabetes-care pack
- Spanish-language local pack
- marine/offshore pack

An overlay may add authored knowledge, localization, schemas, indexes, lawful source references and alternative prioritization. Variants should declare compatibility and stable knowledge IDs so they can merge predictably.

## Provenance and disagreement are first-class data

The water-disinfection review exposed why this matters. Multiple credible organizations can publish differing operational numbers at the same time. The Ark should not silently blend them into one pseudo-authoritative sentence.

A safety-critical fact object should be able to encode:

- claim/action
- source
- source date/version
- applicability conditions
- confidence/review state
- conflicting source(s)
- chosen canonical operating rule
- reason for canonical choice
- review-by date

This is "proof-carrying knowledge": the operational answer remains compact, while a larger tier can reveal why the answer exists and where it came from.

## GUI should be generated from knowledge where possible

Forms, calculators, checklists and small workflows should not exist only as one bespoke application implementation.

A knowledge object can declare a schema. Example patient-observation fields:

- name/identifier
- age
- timestamp
- mental status
- breathing observation
- temperature
- medications
- fluid intake
- urine/output
- notes/trend

Targets can render the same logical object differently:

- phone/web: graphical form
- desktop: richer form + history
- terminal: prompted text fields
- C64-class client: compact paged form
- paper: printable card

The record remains interoperable even when the GUI changes.

## Portable data layer, multiple database runtimes

SQLite is an excellent target, not the canonical ontology.

The canonical layer should be simple logical records with:

- stable IDs
- typed fields
- relations
- timestamps/version
- provenance
- validation rules

Possible physical targets:

- very small/old systems: flat records + sorted/precomputed indexes
- DOS/early PC: compact indexed/B-tree files
- modern phone: SQLite
- browser: IndexedDB/static indexes
- desktop/server: SQLite/Postgres/FTS/search engine
- paper: generated forms/index books

Do not make the survival of the knowledge depend on the survival of one database engine.

## Local server mode

Any capable Ark node should be able to become a local information institution when wider networks fail.

A phone, laptop or small server with a large corpus can expose browser-compatible local services over Wi-Fi/Ethernet without Internet:

- search
- current notices
- maps
- medical/water/repair knowledge
- forms/checklists
- inventory
- people/status records
- message board
- source library

Other devices need only a browser or extremely small client. This separates archive ownership from endpoint capability.

## Compression frontier vs archive frontier

The tier ladder should reveal qualitative transitions, not just larger documents.

Approximate hypotheses to test rather than assume:

- 1 KiB: irreversible-error prevention / triage
- 10 KiB: compact procedures and branching rules
- 100 KiB: operational manual; navigation starts paying for itself
- 1 MiB: troubleshooting, recovery, explanation and cross-domain capability
- 10 MiB: genuine field library and training depth
- 100 MiB: practical encyclopedia with richer diagrams/manuals/local variants
- 1 GiB: broad civilization core; teaching new specialists becomes realistic
- 10 GiB: "university in a box" territory; software/toolchains/maps/textbooks become normal
- 100 GiB: broad multilingual/media/software coverage; retrieval/provenance dominate
- 1 TiB+: storage increasingly ceases to be the main constraint; power, indexing, formats, hardware replacement, replication and institutional competence dominate
- 10-100 TiB: archive-scale preservation, rich media, datasets, history and redundancy; marginal operational knowledge per byte may fall sharply

These are hypotheses. The project should empirically discover where each topic actually bends.

## Model ensemble as measurement instrument

Do not use multiple models merely to vote on wording. Their disagreements are experiment data.

For each topic x budget:

1. generate independently across multiple model families/runs;
2. freeze artifacts before cross-reading;
3. extract included concepts/procedures and rejected concepts;
4. measure convergence and divergence;
5. test against hidden scenarios;
6. adjudicate safety-critical disagreements against sources/domain review;
7. derive a canonical compiled candidate;
8. preserve minority selections as possible blind-spot signals rather than deleting them automatically.

Items repeatedly selected independently at very small budgets are evidence of structural importance. Items that appear only at larger budgets show where explanation, troubleshooting, teaching or specialist capability starts earning its storage cost.

## Initial three-run signal

The first available sample already suggests a strong core, while remaining too small to establish a canonical answer.

The three available runs/voices are:

1. a frozen GPT-5.6 Sol repository submission (`submissions/chatgpt-sol/`);
2. a separate blind GPT-5.6 Sol conversational run generated before inspecting other submissions;
3. ArkoftheDuck Option B, authored by Claude in PR #5 (explicitly non-blind under the maintainer-approved protocol variation).

Important methodological note: these are three runs but only two identified model families in the evidence currently captured here. Treat convergence as preliminary, not a three-family consensus.

At 1 KiB all three independently prioritize most of the same irreversible hazards:

- immediate scene danger / leave unsafe conditions
- breathing and/or severe bleeding
- safe water
- carbon monoxide / indoor combustion
- temperature/exposure
- sanitation / fecal separation

The scarce frontier bytes diverge:

- one run spends them on oral rehydration and more tourniquet/CPR specificity;
- one spends them on communications, food and "do not create a second victim";
- Claude/ArkoftheDuck spends them on signaling, stay/go logic and a compact rule-of-three framing.

That is exactly the desired output of the experiment. The common set is a candidate non-droppable core. The divergent set defines what hidden scenario testing should discriminate.

At 100 KiB and 1 MiB, the existing run commentaries independently converge on several architectural observations:

- indexing/navigation begins to justify its byte cost around the 100 KiB scale;
- safety-critical precision becomes dangerous when context is stripped;
- the larger artifact can become harder to use if trust layers and navigation are poor;
- much of the jump from 100 KiB to 1 MiB buys recovery/capability/troubleshooting rather than additional immediate-survival fundamentals;
- filling large budgets naturally tempts a deterministic source-packing layer, which suggests the product should explicitly separate authored operating knowledge from lawful reference-source packing rather than pretend they are the same thing.

## Near-term build direction

1. Keep collecting blind independent submissions.
2. Extend the experiment to 10 KiB, 10 MiB and eventually the full 1 KiB -> 100 TiB ladder.
3. Start topic-specific frontier experiments instead of only whole-disaster-corpus experiments.
4. Define a stable knowledge-object ID and provenance schema before large-scale compilation.
5. Separate authored compiled knowledge, redistributable sources, personal vaults and community overlays in the repository/data model.
6. Build one schema-driven form end to end and render it in browser, terminal, SQLite-backed modern runtime and a deliberately constrained flat-file runtime.
7. Build target profiles around actual device constraints (RAM/CPU/interface/bandwidth/power), not assumed storage size.
8. Establish license scanning and source-manifest generation before source-library growth accelerates.
9. Preserve source conflicts and dates; never flatten disagreement silently.
10. Treat the current disaster corpus as the first domain testbed, not the final scope of the Ark.

## Product principle

The goal is not one giant survival drive.

The goal is a lossy-to-lossless hierarchy of human knowledge that can be shipped at explicit sizes, legally redistributed, privately extended, publicly overlaid, rendered across wildly different machines, served locally when networks fail, and traced back to its evidence.

A 1 KiB Ark and a 100 TiB Ark should remain recognizably the same system.
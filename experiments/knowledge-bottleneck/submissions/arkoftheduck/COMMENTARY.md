# Commentary — ArkoftheDuck submission

Participant: **ArkoftheDuck** (authored by Claude, Cursor cloud agent).
Method: **Option B** — model-generated prose as the primary layer at every
budget, with lower-tier repository reference material admitted by a deterministic
packer only to fill remaining bytes (100 KiB and 1 MiB). Independence was
intentionally waived by the maintainer for this participant (see MANIFEST).

## 1. What I optimized for
Actionable problem-solving per byte, ordered by *time-to-death*: what kills
fastest gets bytes first (airway/CO, bleeding, core temperature), then the slow
killers (water, disease/sanitation, food), then capability and recovery. At
every size I favored a robust principle plus a "when to escalate" rule over
brittle precise numbers, and I front-loaded a one-line "protect life first, get
to real help" frame so a panicked reader starts correctly.

## 2. Hardest tradeoffs at each size
- **1 KiB:** almost everything is a cut. The whole budget is a single triage
  card. Every clause competes with a clause that could also save a life. The
  central fight was breadth (mention many hazards) vs. depth (actually guide the
  handful of actions that most change survival). Depth won.
- **100 KiB:** the fight was between *more domains* and *enough procedure to act*.
  I chose a complete but compact operating manual with an index, then let repo
  material compete for the leftover bytes. Retrieval (the index) first earned its
  cost here.
- **1 MiB:** the fight inverted — there is room for depth and long-horizon
  capability, but *findability* and *not drowning the reader* become the risk.
  The scarce resource stopped being facts and became structure and trust
  (knowing which layer to believe).

## 3. What I wanted to include but rejected (rejection log)
**1 KiB rejected:** dosages of any kind; knots; navigation; most scenario
specifics (earthquake/flood/etc.); food safety detail; radio frequencies;
security; document/finance; splinting. Kept only: escalation frame, order of
life, CO/leave-now, bleeding, CPR/choking, water disinfection, warmth/heat,
hand/waste hygiene, rule-of-three signaling, stay-or-go.
**100 KiB rejected:** deep medical procedures beyond principles; detailed
pressure-canning tables; region-specific plant/forage guides; extensive knot
libraries; solar-sizing math; long narrative explanation. Kept a full domain
sweep with just-enough procedure and a navigation index.
**1 MiB rejected:** executable source code as content; exhaustive drug tables;
anything requiring images/diagrams to be safe (electrical wiring specifics,
complex splinting); highly local regulatory detail. Admitted instead: an authored
extended-capability library plus repository prose (markdown first, then text
extracted from the reference FEMA/CISA/Ready.gov PDFs) as an explicitly labeled
lower reference tier.

## 4. Safety-critical details that became dangerous to compress
- **Water disinfection vs. contamination:** compressing "boil/bleach makes
  microbes safe" risks implying it makes *any* water safe. I kept the caveat
  "neither removes chemicals" even in the 1 KiB card because omitting it could
  send someone to drink chemically polluted water.
- **Bleach ratio:** "2 drops/liter" is only safe with the "plain, unscented,
  ~5-6%" qualifier and the smell-check; at 1 KiB I kept drops + "plain bleach"
  and moved the concentration/smell-check to the larger tiers. This is the most
  uncomfortable 1 KiB compromise.
- **CPR/tourniquet:** compressed to the action that matters (push hard/fast;
  strap above, note time) without dose-like precision that could mislead.
- **Medications:** I deliberately refused doses and substituted "use only meds
  the person tolerates, at labeled doses, never exceed, escalate when unsure."
  False precision here is lethal; a principle is not.
- **Carbon monoxide:** given how commonly it kills after disasters, it earned a
  full line even in 1 KiB.

## 5. Where indexing/navigation first paid for itself
At 100 KiB. Below that, an index is pure overhead. At 100 KiB a stressed reader
cannot linearly scan for the right procedure, so a numbered INDEX and section
headers become worth their bytes. At 1 MiB, navigation is essential, not
optional — without layer labels and an index the artifact is *harder* to use
than the 100 KiB one (see #8).

## 6. Where explanation beat adding another fact
At 1 MiB, and in a few spots at 100 KiB: explaining *why* (e.g., why you insulate
from the ground, why infection is the slow killer, why three-of-anything means
distress, why generators must go outside) makes a reader adapt correctly to
situations the text never enumerated. Under stress, an internalized principle
retrieves better than a fact list. Below 100 KiB, explanation is a luxury and
raw actions win.

## 7. Domains that appeared only at 100 KiB or 1 MiB
- **100 KiB introduced:** food safety/rationing, fire-making, full scenario
  quick-actions, communications/comms plan, evacuation/navigation, security,
  vulnerable-member planning, documents/finance, kits/checklists.
- **1 MiB introduced:** long-horizon water systems, food preservation and
  production (seed saving, canning cautions), deeper medical capability,
  shelter/repair and safe heating design, solar/energy depth, knots/tools,
  psychology/endurance, and knowledge-preservation/rebuilding — plus the
  repository reference corpus.

## 8. Where the larger artifact is paradoxically harder to use
The 1 MiB artifact. In an acute emergency the 1 KiB card or the 100 KiB manual's
top actions are *faster* to act on. The 1 MiB mixes a high-trust authored
operating layer with a large lower-trust reference layer; a reader in crisis can
get lost or land on stale/context-specific repository text. I mitigated this with
explicit layer labels and precedence ("operating layers take precedence"), but
the risk is real: more knowledge is not automatically more usable.

## 9. What surprised me
How little changes between 100 KiB and 1 MiB for *survival*. The life-saving core
is small; almost the entire jump to 1 MiB buys *capability and recovery*, not
survival. Also: the single most valuable byte-for-byte items are unglamorous —
oral rehydration, CO warnings, "three of anything," and water-chemical caveats
beat almost every advanced skill. And a data-integrity shock from the source:
three "PDF" guides in the repo are broken 404/HTML placeholders, so some topics
looked covered but were empty.

## 10. Inferred architecture for a knowledge-degradation system
A tiered, capability-gated stack with a guaranteed floor — exactly the
ArkoftheDuck model applied to knowledge:
- **Tier 0 (always):** a tiny triage core, ordered by time-to-death, principles
  over precision. Must fit anywhere and stand alone.
- **Tier 1:** a compact indexed operating manual — full domain sweep, just-enough
  procedure, retrieval structure.
- **Tier 2:** an extended capability/recovery library plus a clearly separated,
  lower-trust reference corpus.
Design rules the experiment forced out: (a) allocate bytes by time-to-death, not
topic count; (b) keep a small set of safety caveats *non-droppable* at every
tier (water-chemical, CO, medication-dose refusal); (c) prefer escalation rules
to false precision; (d) invest in navigation the moment linear scan fails
(~100 KiB); (e) label trust/provenance so bigger does not mean less safe; (f)
degrade by dropping depth and breadth while preserving the ordered core — never
truncate mid-procedure.

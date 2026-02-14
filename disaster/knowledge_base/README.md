# Emergency Preparedness Knowledge Base (V3)

Single combined knowledge base for the Emergency Preparedness System. Search and indexing use this entire tree.

## Categories

| Path | Contents |
|------|----------|
| **scenario_specific_plans/** | Earthquake, power failure, winter storm, flood, hurricane, tornado, extreme heat, tsunami, landslide, pandemic, active shooter, commuter emergency plan |
| **water_and_food/** | Urban water guide, urban food guide |
| **medicine/** | Advanced first aid, sprains and pain, first aid CPR sources |
| **evacuation/** | Bug-out bag guide |
| **communications/** | Communications guide |
| **power_and_energy/** | Power and energy guide |
| **security/** | Security guide |
| **sanitation_and_hygiene/** | Sanitation and hygiene guide |
| **psychology_and_community/** | Psychology and community guide |
| **long_term_sustainability/** | 6-month supply planning, community resilience, local food production, financial preparedness |
| **modern_threats/** | Cyber (offline backup, manual operations), EMP (Faraday cage), nuclear (radiation detection) |
| **barter_and_trade/** | Barter and trade guide |
| **home_repair/** | Home repair guide |
| **reference/** | REFERENCE_DOCUMENTS.md (catalog of Ready.gov, FEMA, CDC, CISA links) |
| **vulnerable_people/** | Vulnerable people guide |
| **advanced_skills/** | Essential knots guide |

## Scenario Plans (scenario_specific_plans/)

- `earthquake_plan.md`
- `power_failure_plan.md`
- `winter_storm_preparedness.md`
- `flood_safety.md`
- `hurricane_preparedness.md`
- `tornado_preparedness.md`
- `extreme_heat_preparedness.md`
- `tsunami_preparedness.md`
- `landslide_preparedness.md`
- `pandemic_preparedness.md`
- `active_shooter_response.md`
- `commuter_emergency_plan.md`

## Reference Catalog

- `reference/REFERENCE_DOCUMENTS.md` — Catalog of free PDFs and official links (Ready.gov, FEMA, CDC, CISA, NOAA)

## File Count

- **~40** guides and PDFs (traditional + modern threats + long-term + scenario plans + reference).

## Indexing

- `knowledge_base_search.py` and `build_knowledge_base.py` (optional vector store) index all `.md` and `.pdf` under this directory. Keep one canonical copy of each file; do not split back into separate base vs v2 trees.

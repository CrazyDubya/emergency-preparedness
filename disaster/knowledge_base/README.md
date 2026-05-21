# Emergency Preparedness Knowledge Base (V3)

Single combined knowledge base for the Emergency Preparedness System. Search and indexing use this entire tree.

## Categories

| Path | Contents |
|------|----------|
| **Traditional** | Water & food, medicine, security, communications, evacuation, home repair, power, sanitation, psychology, barter, vulnerable people, advanced skills, scenario-specific plans (earthquake, power failure, winter storm), survival and reference PDFs |
| **modern_threats/** | Cyber (offline backup, manual operations), EMP (Faraday cage), nuclear (radiation detection) |
| **long_term_sustainability/** | 6-month supply planning, community resilience, local food production |

## File count

- **~30** guides and PDFs (traditional + modern threats + long-term).
- **V1-only** assets included: `scenario_specific_plans/winter_storm_preparedness.md`, `home_repair/frozen_pipes_guide.pdf`.

## Indexing

- `knowledge_base_search.py` and `build_knowledge_base.py` (optional vector store) index all `.md` and `.pdf` under this directory. Keep one canonical copy of each file; do not split back into separate base vs v2 trees.

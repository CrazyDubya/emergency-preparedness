# Emergency Preparedness System – Version 3.0 Refactor

**Date:** February 2026  
**Status:** Unified codebase (V1 + V2 merged into V3)

## What Changed in V3

1. **Single codebase** – All code lives under `disaster/v3/`. No more separate `disaster/` (v1) and `disaster/claude-disaster/` (v2) trees.
2. **Single knowledge base** – One `knowledge_base/` directory containing:
   - Traditional guides (water, food, medicine, security, communications, evacuation, etc.)
   - V2 modern threats (cyber, EMP, nuclear)
   - V2 long-term sustainability (6-month supply, local food, community resilience)
   - V1-only assets: `winter_storm_preparedness.md`, `home_repair/frozen_pipes_guide.pdf`
3. **Unified docs** – One set in `docs/`: README (combined original + enhanced), CONTRIBUTING, VERSION_1_RELEASE, VERSION_2_ARCHITECTURE, stress test and scenario docs, plus DOC_COMPARISON and this file.
4. **Path rename** – Code references `knowledge_base` (no longer `disaster_knowledge_base` or `v2_knowledge_base`). Build and search use the single directory.
5. **KB improvements** – `knowledge_base/README.md` added; `winter_storm_preparedness.md` moved to `scenario_specific_plans/`; cross-link to frozen pipes guide added.
6. **Repo refactor** – Root `README.md` points to v3; `disaster/` and `disaster/claude-disaster/` marked legacy (banner in README + `README_LEGACY.md` in each).

## V1 vs V2 Document Comparison

- **Identical in both:** README.md, CONTRIBUTING.md, VERSION_1_RELEASE.md, VERSION_2_ARCHITECTURE.md, stress_test_analysis.md, scenario_planning_top10.md, scenario_based_planning.md, family_preparedness_checklist.md, disaster_kit_research.md, disaster_analysis_report.md, deep_dive_health_risks.md.
- **V2-only:** README_ENHANCED.md (CLI, API, GUI, backups, profiles). Its content is merged into the main V3 README.
- See `docs/DOC_COMPARISON.md` for the full table and KB merge details.

## How to Run V3

From `disaster/v3/`:

```bash
# Dependencies
pip install -r requirements.txt

# Interactive CLI
python integrated_preparedness_system.py
# or
python run_system.py

# Direct commands
python integrated_preparedness_system.py --status --risk-assessment --backup --drill earthquake

# API
python api_server.py   # http://localhost:8000/docs

# Web GUI
streamlit run streamlit_gui.py   # http://localhost:8501

# Tests
python system_test.py
```

## Backward Compatibility

- **Data:** Uses same `preparedness_data/` layout and SQLite DBs. Point the app at an existing data dir if needed.
- **Imports:** All module names unchanged; only the knowledge base directory name and doc locations changed.

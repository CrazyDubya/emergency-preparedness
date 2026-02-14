# Development Log

Supplement to git commits for ongoing work.

## 2025-02-14 (kjp worktree)

### Plan Implementation: UI/UX, Features, Knowledge Expansion

**Phase 3 – Scenario quick-help API + UI**
- Added `KnowledgeBaseSearch.get_scenario_guide(name)` and `list_scenario_guides()` in `core/knowledge_base_search.py`
- API: `GET /api/knowledge/scenario/{name}`, `GET /api/knowledge/scenarios`
- Streamlit Knowledge Base page: "Scenario Quick Help" selectbox; selecting a scenario loads and displays the guide

**Phase 3 – Profile switcher**
- API: `GET /api/profiles`, `PUT /api/profile/switch` with `ProfileSwitchRequest`
- Streamlit sidebar: profile selectbox; switching triggers API or `load_profile()` in direct mode
- Added `APIClient.put()` for PUT requests

**Phase 4 – Knowledge base expansion**
- New scenario guides: `flood_safety.md`, `hurricane_preparedness.md`, `tornado_preparedness.md`, `extreme_heat_preparedness.md`, `tsunami_preparedness.md`, `landslide_preparedness.md`, `pandemic_preparedness.md`
- Supporting guides: `long_term_sustainability/financial_preparedness.md`, `medicine/first_aid_cpr_sources.md`
- Reference catalog: `reference/REFERENCE_DOCUMENTS.md` with Ready.gov, FEMA, CDC, CISA links
- Cross-links added in winter_storm, communications, offline_backup, financial, pandemic, extreme_heat guides

### Earlier: Verification & Remaining Fixes

**Test path fix (run_tests.py)**
- Added `disaster/core` to `sys.path` before project root so tests can import `emergency_drill_simulator`, `exceptions`, `resilience`, `security` from core
- All 97 tests pass

**Drill history wiring (Streamlit + API)**
- API `GET /api/drills/history`: now uses `drill_simulator.get_performance_history(participant)` (source of truth: drill_results DB) instead of profile activities
- Added query param `participant` (default "User") for history lookup
- Streamlit: added `get_drill_history_data(participant)` helper (API + direct mode)
- Training & Drills page drill history section now shows real data from drill DB; empty state message when no drills completed

# emergency-preparedness

A disaster preparedness system for households and neighbourhoods — risk assessment, supply planning, contacts, drills, and a searchable knowledge base.

The code lives under `disaster/`, which has its own detailed README.

## What's here

- `disaster/core/` — sixteen modules: `disaster_probability_matrix.py` and `interactive_risk_assessment.py` for risk; `materials_calculator.py` and `data_manager.py` for supplies; `emergency_contacts_manager.py` and `communication_emergency_plan.py` for coordination; `emergency_drill_simulator.py` for practice; `financial_emergency_planning.py`, `neighborhood_coordination.py`, `intuitive_building_guide.py`, `alert_monitoring_system.py`, `knowledge_base_search.py` and others.
- `disaster/build_knowledge_base.py` — assembles the guide corpus.
- `disaster/api_server.py` — HTTP interface to the modules.

## Running it

```bash
python3 disaster/system_test.py    # verify the install
python3 disaster/run_system.py     # main interface
```

## Related

The public `disaster` repository holds the same subject matter as a markdown research library (shelter, medical, water, food, 72-hour timeline). This repository is the software; that one is the reference material.

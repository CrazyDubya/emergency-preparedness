# emergency-preparedness

A disaster preparedness system. The code is under `disaster/`, which has its own README describing it as a "professional-grade disaster preparedness platform for families and communities" with 16 integrated modules.

## What's here

`disaster/core/` holds those modules. Among them:

- Risk — `disaster_probability_matrix.py`, `interactive_risk_assessment.py`, `deep_dive_risk_categories.py`
- Supplies — `materials_calculator.py`, `data_manager.py`
- Coordination — `emergency_contacts_manager.py`, `communication_emergency_plan.py`, `neighborhood_coordination.py`
- Practice — `emergency_drill_simulator.py`
- Also — `financial_emergency_planning.py`, `intuitive_building_guide.py`, `alert_monitoring_system.py`, `knowledge_base_search.py`, `enhanced_visualizations.py`, `backup_manager.py`, `resilience.py`

Plus `disaster/build_knowledge_base.py` and `disaster/api_server.py`.

## Running it

From `disaster/README.md`:

```bash
python3 system_test.py
python3 run_system.py
```

## Related

The public `disaster` repository holds markdown reference material on the same subject — shelter, medical, water, food, a 72-hour timeline. That one is the library; this one is the software.

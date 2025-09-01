#!/usr/bin/env python3
"""
Scenario-Specific Risk Profiles - Version 3.0
Detailed risk profiles for 20 comprehensive disaster scenarios
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from .advanced_risk_engine import AdvancedRiskEngine

class ScenarioRiskProfiles:
    """
    Comprehensive risk profiles for all 20 stress test scenarios
    with detailed analysis and response protocols
    """
    
    def __init__(self, db_path: str = "scenario_profiles.db"):
        """Initialize Scenario Risk Profiles system"""
        self.risk_engine = AdvancedRiskEngine(db_path)
        self._initialize_all_profiles()
    
    def _initialize_all_profiles(self):
        """Create detailed risk profiles for all 20 scenarios"""
        
        self.scenario_profiles = {
            "major_earthquake": {
                "name": "Major Earthquake (7.2 Magnitude)",
                "type": "earthquake",
                "base_characteristics": {
                    "duration": "minutes",
                    "warning_time": 0,
                    "severity": 9,
                    "affected_area": "city_wide",
                    "occurrence_probability": 2.5
                },
                "cascading_effects": {
                    "power_outage": 0.85,
                    "water_disruption": 0.80,
                    "building_damage": 0.70,
                    "road_closure": 0.65,
                    "gas_leak": 0.45,
                    "fire": 0.35,
                    "tsunami": 0.15
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "minimal",
                    "recovery_timeline": "6-12 months"
                },
                "regional_variations": {
                    "california": 2.5,
                    "midwest": 0.3,
                    "east_coast": 0.5,
                    "pacific_northwest": 1.8
                },
                "critical_needs": [
                    "Immediate shelter",
                    "Search and rescue",
                    "Medical care",
                    "Structural assessment",
                    "Utilities restoration"
                ],
                "response_phases": {
                    "0-1_hour": ["Drop, cover, hold", "Check injuries", "Evacuate if unsafe"],
                    "1-24_hours": ["Locate family", "Assess damage", "Secure shelter"],
                    "1-7_days": ["Obtain supplies", "Document damage", "Contact insurance"],
                    "1-4_weeks": ["Begin repairs", "File claims", "Seek assistance"],
                    "1-6_months": ["Rebuild", "Recovery support", "Mental health care"]
                }
            },
            
            "category_4_hurricane": {
                "name": "Category 4 Hurricane",
                "type": "hurricane",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 72,
                    "severity": 8,
                    "affected_area": "regional",
                    "occurrence_probability": 5.0
                },
                "cascading_effects": {
                    "flooding": 0.90,
                    "power_outage": 0.95,
                    "supply_disruption": 0.85,
                    "evacuation": 0.70,
                    "storm_surge": 0.80,
                    "wind_damage": 0.90,
                    "infrastructure_failure": 0.60
                },
                "temporal_factors": {
                    "worst_time": "high_tide",
                    "seasonal_variation": "June-November",
                    "recovery_timeline": "3-6 months"
                },
                "regional_variations": {
                    "gulf_coast": 2.0,
                    "atlantic_coast": 1.8,
                    "inland": 0.3,
                    "west_coast": 0.1
                },
                "critical_needs": [
                    "Evacuation transportation",
                    "Emergency shelter",
                    "Storm supplies",
                    "Communication systems",
                    "Post-storm security"
                ],
                "response_phases": {
                    "72_hours_before": ["Monitor forecasts", "Prepare property", "Stock supplies"],
                    "48_hours_before": ["Decide evacuation", "Secure home", "Fuel vehicles"],
                    "24_hours_before": ["Final preparations", "Evacuate if ordered", "Shelter in place"],
                    "during_storm": ["Stay indoors", "Monitor alerts", "Avoid windows"],
                    "post_storm": ["Assess damage", "Check on neighbors", "Begin cleanup"]
                }
            },
            
            "house_fire": {
                "name": "House Fire",
                "type": "fire",
                "base_characteristics": {
                    "duration": "minutes",
                    "warning_time": 0,
                    "severity": 10,
                    "affected_area": "single_building",
                    "occurrence_probability": 8.0
                },
                "cascading_effects": {
                    "smoke_inhalation": 0.90,
                    "structure_loss": 0.60,
                    "displacement": 0.80,
                    "property_loss": 0.70,
                    "emotional_trauma": 0.85
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "higher in winter",
                    "recovery_timeline": "3-6 months"
                },
                "regional_variations": {
                    "urban": 1.2,
                    "suburban": 1.0,
                    "rural": 0.8
                },
                "critical_needs": [
                    "Immediate evacuation",
                    "Fire suppression",
                    "Temporary shelter",
                    "Document recovery",
                    "Insurance processing"
                ],
                "response_phases": {
                    "0-2_minutes": ["Alert everyone", "Evacuate immediately", "Call 911"],
                    "2-10_minutes": ["Meet at safe location", "Account for everyone", "Do not re-enter"],
                    "10-60_minutes": ["Talk to fire dept", "Contact insurance", "Find shelter"],
                    "1-24_hours": ["Secure property", "Inventory losses", "Contact family"],
                    "1-7_days": ["Begin recovery", "Work with adjusters", "Replace documents"]
                }
            },
            
            "extended_power_failure": {
                "name": "Extended Power Grid Failure",
                "type": "power_outage",
                "base_characteristics": {
                    "duration": "weeks",
                    "warning_time": 0,
                    "severity": 6,
                    "affected_area": "multi_state",
                    "occurrence_probability": 15.0
                },
                "cascading_effects": {
                    "food_spoilage": 0.95,
                    "heating_loss": 0.90,
                    "communication_loss": 0.75,
                    "fuel_shortage": 0.70,
                    "water_system_failure": 0.60,
                    "medical_equipment_failure": 0.50,
                    "social_unrest": 0.40
                },
                "temporal_factors": {
                    "worst_time": "extreme_weather",
                    "seasonal_variation": "critical in winter/summer",
                    "recovery_timeline": "1-4 weeks"
                },
                "regional_variations": {
                    "texas": 1.5,
                    "california": 1.3,
                    "northeast": 1.2,
                    "midwest": 1.0
                },
                "critical_needs": [
                    "Alternative power",
                    "Food preservation",
                    "Heating/cooling",
                    "Water access",
                    "Communication methods"
                ],
                "response_phases": {
                    "0-4_hours": ["Check circuit breakers", "Unplug appliances", "Preserve food"],
                    "4-24_hours": ["Start generator", "Ration resources", "Check neighbors"],
                    "1-3_days": ["Establish routines", "Conserve fuel", "Seek updates"],
                    "3-7_days": ["Find resources", "Community coordination", "Health monitoring"],
                    "1-2_weeks": ["Adapt lifestyle", "Alternative solutions", "Recovery planning"]
                }
            },
            
            "cyber_attack_infrastructure": {
                "name": "Cyber Attack on Infrastructure",
                "type": "cyber_attack",
                "base_characteristics": {
                    "duration": "weeks",
                    "warning_time": 0,
                    "severity": 7,
                    "affected_area": "national",
                    "occurrence_probability": 12.0
                },
                "cascading_effects": {
                    "banking_disruption": 0.85,
                    "supply_chain_failure": 0.80,
                    "communication_loss": 0.70,
                    "power_grid_impact": 0.60,
                    "transportation_disruption": 0.65,
                    "panic_buying": 0.75,
                    "economic_impact": 0.90
                },
                "temporal_factors": {
                    "worst_time": "business_hours",
                    "seasonal_variation": "minimal",
                    "recovery_timeline": "2-8 weeks"
                },
                "regional_variations": {
                    "major_cities": 1.5,
                    "tech_hubs": 1.8,
                    "rural": 0.7,
                    "government_centers": 2.0
                },
                "critical_needs": [
                    "Cash reserves",
                    "Offline backups",
                    "Alternative communication",
                    "Physical supplies",
                    "Security measures"
                ],
                "response_phases": {
                    "immediate": ["Disconnect devices", "Switch to cash", "Verify information"],
                    "0-24_hours": ["Secure accounts", "Document issues", "Find alternatives"],
                    "1-7_days": ["Adapt systems", "Manual processes", "Community support"],
                    "1-4_weeks": ["Monitor recovery", "Rebuild digital", "Learn lessons"]
                }
            },
            
            "pandemic_lockdown": {
                "name": "Pandemic Lockdown",
                "type": "pandemic",
                "base_characteristics": {
                    "duration": "months",
                    "warning_time": 168,
                    "severity": 6,
                    "affected_area": "global",
                    "occurrence_probability": 3.0
                },
                "cascading_effects": {
                    "supply_shortage": 0.70,
                    "economic_disruption": 0.90,
                    "social_isolation": 0.95,
                    "healthcare_overwhelm": 0.80,
                    "education_disruption": 0.85,
                    "mental_health_crisis": 0.75
                },
                "temporal_factors": {
                    "worst_time": "winter",
                    "seasonal_variation": "worse in cold months",
                    "recovery_timeline": "12-24 months"
                },
                "regional_variations": {
                    "urban": 1.5,
                    "suburban": 1.0,
                    "rural": 0.7
                },
                "critical_needs": [
                    "Medical supplies",
                    "Food stockpile",
                    "Remote work capability",
                    "Mental health support",
                    "Financial reserves"
                ],
                "response_phases": {
                    "pre_lockdown": ["Stock supplies", "Prepare remote work", "Medical preparations"],
                    "week_1-2": ["Establish routines", "Connect virtually", "Monitor health"],
                    "month_1-3": ["Maintain discipline", "Support network", "Adapt lifestyle"],
                    "month_3-6": ["Long-term planning", "Skills development", "Health focus"],
                    "recovery": ["Gradual reintegration", "Economic recovery", "Lessons learned"]
                }
            },
            
            "ef4_tornado": {
                "name": "EF4 Tornado",
                "type": "tornado",
                "base_characteristics": {
                    "duration": "minutes",
                    "warning_time": 0.25,
                    "severity": 9,
                    "affected_area": "corridor",
                    "occurrence_probability": 2.5
                },
                "cascading_effects": {
                    "building_destruction": 0.80,
                    "debris_field": 0.95,
                    "power_outage": 0.90,
                    "injury_risk": 0.70,
                    "vehicle_damage": 0.85,
                    "infrastructure_damage": 0.75
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "March-June peak",
                    "recovery_timeline": "6-12 months"
                },
                "regional_variations": {
                    "tornado_alley": 2.5,
                    "southeast": 1.8,
                    "midwest": 1.5,
                    "other": 0.3
                },
                "critical_needs": [
                    "Immediate shelter",
                    "Warning systems",
                    "Search and rescue",
                    "Medical response",
                    "Debris clearance"
                ],
                "response_phases": {
                    "warning": ["Seek shelter immediately", "Lowest floor, center room", "Protect head"],
                    "during": ["Stay in shelter", "Cover with mattress/blankets", "Avoid windows"],
                    "immediate_after": ["Check injuries", "Exit carefully", "Watch for hazards"],
                    "0-24_hours": ["Account for everyone", "Document damage", "Secure property"],
                    "recovery": ["Work with FEMA", "Insurance claims", "Rebuild stronger"]
                }
            },
            
            "flash_flooding": {
                "name": "Flash Flooding",
                "type": "flood",
                "base_characteristics": {
                    "duration": "hours",
                    "warning_time": 2,
                    "severity": 7,
                    "affected_area": "local",
                    "occurrence_probability": 10.0
                },
                "cascading_effects": {
                    "water_contamination": 0.85,
                    "road_washout": 0.70,
                    "property_damage": 0.75,
                    "vehicle_loss": 0.60,
                    "sewage_backup": 0.65,
                    "electrical_hazards": 0.80
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "spring/summer",
                    "recovery_timeline": "1-3 months"
                },
                "regional_variations": {
                    "desert_southwest": 1.8,
                    "urban_areas": 1.5,
                    "river_valleys": 2.0,
                    "coastal": 1.3
                },
                "critical_needs": [
                    "High ground evacuation",
                    "Swift water rescue",
                    "Clean water supply",
                    "Sanitation",
                    "Mold prevention"
                ],
                "response_phases": {
                    "warning": ["Monitor alerts", "Prepare to evacuate", "Move valuables up"],
                    "imminent": ["Evacuate if ordered", "Avoid low areas", "Never drive through water"],
                    "during": ["Seek high ground", "Avoid moving water", "Call for rescue if trapped"],
                    "post_flood": ["Document damage", "Avoid contaminated water", "Begin cleanup"],
                    "recovery": ["Sanitize property", "Prevent mold", "Restore utilities"]
                }
            },
            
            "chemical_spill": {
                "name": "Hazardous Chemical Spill",
                "type": "hazmat",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 0.5,
                    "severity": 7,
                    "affected_area": "local",
                    "occurrence_probability": 4.0
                },
                "cascading_effects": {
                    "air_contamination": 0.80,
                    "water_contamination": 0.60,
                    "evacuation": 0.85,
                    "health_impacts": 0.70,
                    "environmental_damage": 0.75,
                    "property_contamination": 0.50
                },
                "temporal_factors": {
                    "worst_time": "calm_weather",
                    "seasonal_variation": "worse in summer heat",
                    "recovery_timeline": "weeks to months"
                },
                "regional_variations": {
                    "industrial_areas": 2.0,
                    "transport_corridors": 1.5,
                    "rural": 0.5,
                    "urban": 1.2
                },
                "critical_needs": [
                    "Immediate evacuation",
                    "Shelter in place supplies",
                    "Decontamination",
                    "Medical monitoring",
                    "Environmental cleanup"
                ],
                "response_phases": {
                    "immediate": ["Evacuate or shelter", "Close windows/vents", "Monitor alerts"],
                    "0-2_hours": ["Follow official orders", "Avoid contaminated areas", "Decontaminate if exposed"],
                    "2-24_hours": ["Stay informed", "Medical attention if symptoms", "Document exposure"],
                    "1-7_days": ["Follow return instructions", "Health monitoring", "Property assessment"],
                    "long_term": ["Medical follow-up", "Legal documentation", "Environmental monitoring"]
                }
            },
            
            "economic_collapse": {
                "name": "Economic Collapse/Bank Run",
                "type": "economic",
                "base_characteristics": {
                    "duration": "months",
                    "warning_time": 24,
                    "severity": 7,
                    "affected_area": "national",
                    "occurrence_probability": 5.0
                },
                "cascading_effects": {
                    "bank_failures": 0.70,
                    "currency_devaluation": 0.80,
                    "supply_shortage": 0.75,
                    "unemployment": 0.85,
                    "social_unrest": 0.60,
                    "crime_increase": 0.65
                },
                "temporal_factors": {
                    "worst_time": "any",
                    "seasonal_variation": "minimal",
                    "recovery_timeline": "years"
                },
                "regional_variations": {
                    "financial_centers": 1.8,
                    "urban": 1.5,
                    "suburban": 1.0,
                    "rural": 0.8
                },
                "critical_needs": [
                    "Cash reserves",
                    "Barterable goods",
                    "Food security",
                    "Community networks",
                    "Alternative economy"
                ],
                "response_phases": {
                    "early_warning": ["Diversify assets", "Stock supplies", "Build networks"],
                    "crisis_begins": ["Secure cash", "Protect assets", "Community coordination"],
                    "acute_phase": ["Barter systems", "Local economy", "Security measures"],
                    "stabilization": ["Rebuild systems", "New opportunities", "Lessons learned"]
                }
            },
            
            "terrorist_attack": {
                "name": "Terrorist Attack (Bombing)",
                "type": "terrorism",
                "base_characteristics": {
                    "duration": "minutes",
                    "warning_time": 0,
                    "severity": 8,
                    "affected_area": "local",
                    "occurrence_probability": 0.5
                },
                "cascading_effects": {
                    "mass_casualties": 0.60,
                    "panic": 0.90,
                    "transportation_shutdown": 0.80,
                    "economic_impact": 0.70,
                    "security_response": 1.0,
                    "psychological_trauma": 0.85
                },
                "temporal_factors": {
                    "worst_time": "rush_hour",
                    "seasonal_variation": "minimal",
                    "recovery_timeline": "months to years"
                },
                "regional_variations": {
                    "major_cities": 2.0,
                    "symbolic_targets": 2.5,
                    "transport_hubs": 1.8,
                    "rural": 0.3
                },
                "critical_needs": [
                    "Immediate evacuation",
                    "Medical response",
                    "Security lockdown",
                    "Family reunification",
                    "Psychological support"
                ],
                "response_phases": {
                    "immediate": ["Run, hide, fight", "Evacuate area", "Call 911"],
                    "0-1_hour": ["Follow authorities", "Avoid area", "Check in with family"],
                    "1-24_hours": ["Shelter in place", "Monitor news", "Cooperate with authorities"],
                    "days_after": ["Mental health support", "Community solidarity", "Vigilance"]
                }
            },
            
            "nuclear_accident": {
                "name": "Nuclear Power Plant Accident",
                "type": "nuclear",
                "base_characteristics": {
                    "duration": "weeks",
                    "warning_time": 2,
                    "severity": 9,
                    "affected_area": "regional",
                    "occurrence_probability": 0.1
                },
                "cascading_effects": {
                    "radiation_exposure": 0.70,
                    "evacuation": 0.90,
                    "agricultural_impact": 0.80,
                    "water_contamination": 0.75,
                    "long_term_health": 0.60,
                    "economic_devastation": 0.85
                },
                "temporal_factors": {
                    "worst_time": "any",
                    "seasonal_variation": "wind dependent",
                    "recovery_timeline": "decades"
                },
                "regional_variations": {
                    "near_plants": 3.0,
                    "10_mile_radius": 2.0,
                    "50_mile_radius": 1.0,
                    "100+_miles": 0.3
                },
                "critical_needs": [
                    "Immediate evacuation",
                    "Radiation protection",
                    "Potassium iodide",
                    "Decontamination",
                    "Long-term relocation"
                ],
                "response_phases": {
                    "alert": ["Monitor emergency broadcasts", "Prepare to evacuate", "Close windows"],
                    "evacuation_order": ["Evacuate immediately", "Follow designated routes", "Go to reception center"],
                    "shelter_in_place": ["Seal room", "Monitor radio", "Take potassium iodide if directed"],
                    "post_release": ["Decontamination", "Medical screening", "Avoid contaminated areas"],
                    "long_term": ["Health monitoring", "Relocation planning", "Compensation claims"]
                }
            },
            
            "severe_ice_storm": {
                "name": "Severe Ice Storm",
                "type": "ice_storm",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 48,
                    "severity": 6,
                    "affected_area": "regional",
                    "occurrence_probability": 8.0
                },
                "cascading_effects": {
                    "power_lines_down": 0.85,
                    "tree_damage": 0.90,
                    "transportation_impossible": 0.95,
                    "heating_loss": 0.70,
                    "water_pipe_freeze": 0.60,
                    "roof_collapse": 0.30
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "winter only",
                    "recovery_timeline": "1-2 weeks"
                },
                "regional_variations": {
                    "northeast": 1.5,
                    "midwest": 1.3,
                    "south": 1.8,
                    "west": 0.5
                },
                "critical_needs": [
                    "Heat source",
                    "Power generation",
                    "Food that doesn't require cooking",
                    "Water supply",
                    "Safe shelter"
                ],
                "response_phases": {
                    "pre_storm": ["Stock supplies", "Prepare heating", "Protect pipes"],
                    "during_storm": ["Stay indoors", "Conserve heat", "Monitor conditions"],
                    "power_loss": ["Alternative heating", "Prevent pipe freezing", "Check CO detectors"],
                    "post_storm": ["Clear ice carefully", "Check for damage", "Help neighbors"],
                    "recovery": ["Restore utilities", "Repair damage", "Restock supplies"]
                }
            },
            
            "wildfire_evacuation": {
                "name": "Wildfire Evacuation",
                "type": "wildfire",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 6,
                    "severity": 8,
                    "affected_area": "regional",
                    "occurrence_probability": 6.0
                },
                "cascading_effects": {
                    "air_quality_crisis": 0.95,
                    "property_loss": 0.60,
                    "evacuation_chaos": 0.70,
                    "infrastructure_damage": 0.65,
                    "ecological_damage": 0.90,
                    "mudslide_risk": 0.50
                },
                "temporal_factors": {
                    "worst_time": "dry_season",
                    "seasonal_variation": "summer/fall peak",
                    "recovery_timeline": "months to years"
                },
                "regional_variations": {
                    "california": 2.5,
                    "mountain_west": 2.0,
                    "southwest": 1.8,
                    "other": 0.5
                },
                "critical_needs": [
                    "Evacuation routes",
                    "Air filtration",
                    "Go bags",
                    "Animal evacuation",
                    "Documentation"
                ],
                "response_phases": {
                    "fire_watch": ["Monitor conditions", "Prepare to leave", "Pack essentials"],
                    "evacuation_warning": ["Load vehicles", "Prepare property", "Alert network"],
                    "evacuation_order": ["Leave immediately", "Follow routes", "Check in at shelter"],
                    "during_evacuation": ["Monitor fire updates", "Stay at safe location", "Document for insurance"],
                    "return": ["Wait for all-clear", "Document damage", "Begin recovery"]
                }
            },
            
            "water_contamination": {
                "name": "Water System Contamination",
                "type": "water_crisis",
                "base_characteristics": {
                    "duration": "weeks",
                    "warning_time": 12,
                    "severity": 6,
                    "affected_area": "city_wide",
                    "occurrence_probability": 5.0
                },
                "cascading_effects": {
                    "health_crisis": 0.70,
                    "bottled_water_shortage": 0.90,
                    "business_closure": 0.60,
                    "sanitation_issues": 0.80,
                    "economic_impact": 0.65,
                    "social_tension": 0.50
                },
                "temporal_factors": {
                    "worst_time": "summer",
                    "seasonal_variation": "worse in hot weather",
                    "recovery_timeline": "2-6 weeks"
                },
                "regional_variations": {
                    "aging_infrastructure": 1.8,
                    "industrial_areas": 1.5,
                    "agricultural_regions": 1.3,
                    "pristine_areas": 0.5
                },
                "critical_needs": [
                    "Safe water source",
                    "Water purification",
                    "Storage containers",
                    "Sanitation alternatives",
                    "Medical monitoring"
                ],
                "response_phases": {
                    "detection": ["Stop using tap water", "Secure bottled water", "Follow advisories"],
                    "acute_phase": ["Boil water if advised", "Use alternatives", "Conserve safe water"],
                    "ongoing": ["Establish routines", "Community sharing", "Monitor health"],
                    "resolution": ["Flush system as directed", "Test before using", "Replace filters"]
                }
            },
            
            "solar_flare_emp": {
                "name": "Solar Flare/EMP Event",
                "type": "emp",
                "base_characteristics": {
                    "duration": "weeks",
                    "warning_time": 1,
                    "severity": 8,
                    "affected_area": "continental",
                    "occurrence_probability": 2.0
                },
                "cascading_effects": {
                    "electronics_destroyed": 0.70,
                    "power_grid_collapse": 0.90,
                    "communication_loss": 0.95,
                    "vehicle_failure": 0.60,
                    "supply_chain_collapse": 0.85,
                    "social_breakdown": 0.50
                },
                "temporal_factors": {
                    "worst_time": "any",
                    "seasonal_variation": "solar cycle dependent",
                    "recovery_timeline": "months to years"
                },
                "regional_variations": {
                    "high_latitude": 1.5,
                    "mid_latitude": 1.0,
                    "equatorial": 0.7
                },
                "critical_needs": [
                    "Faraday cage protection",
                    "Non-electronic tools",
                    "Manual systems",
                    "Community coordination",
                    "Analog communication"
                ],
                "response_phases": {
                    "warning": ["Disconnect electronics", "Protect critical items", "Fill containers"],
                    "impact": ["Check what works", "Assess damage", "Establish communication"],
                    "immediate_after": ["Community organization", "Resource pooling", "Security measures"],
                    "adaptation": ["Manual processes", "Barter economy", "Local solutions"],
                    "long_term": ["Rebuild infrastructure", "Hardened systems", "Preparedness improvement"]
                }
            },
            
            "civil_unrest": {
                "name": "Civil Unrest/Riots",
                "type": "civil_disorder",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 6,
                    "severity": 6,
                    "affected_area": "city_wide",
                    "occurrence_probability": 4.0
                },
                "cascading_effects": {
                    "violence": 0.60,
                    "looting": 0.70,
                    "transportation_blocked": 0.80,
                    "business_closure": 0.85,
                    "supply_disruption": 0.65,
                    "property_damage": 0.60
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "summer peak",
                    "recovery_timeline": "weeks to months"
                },
                "regional_variations": {
                    "major_cities": 2.0,
                    "urban": 1.5,
                    "suburban": 0.8,
                    "rural": 0.3
                },
                "critical_needs": [
                    "Personal security",
                    "Safe shelter",
                    "Avoid confrontation",
                    "Communication",
                    "Supply stockpile"
                ],
                "response_phases": {
                    "tension_rising": ["Monitor news", "Avoid areas", "Prepare to shelter"],
                    "active_unrest": ["Stay home", "Secure property", "Avoid engagement"],
                    "peak_violence": ["Defend if necessary", "Community watch", "Document events"],
                    "de_escalation": ["Cautious movement", "Assess damage", "Community support"],
                    "recovery": ["Rebuild trust", "Economic recovery", "Lesson learned"]
                }
            },
            
            "massive_blizzard": {
                "name": "Massive Snowstorm/Blizzard",
                "type": "blizzard",
                "base_characteristics": {
                    "duration": "days",
                    "warning_time": 72,
                    "severity": 7,
                    "affected_area": "regional",
                    "occurrence_probability": 10.0
                },
                "cascading_effects": {
                    "transportation_halt": 0.95,
                    "power_outage": 0.60,
                    "heating_challenges": 0.50,
                    "roof_collapse": 0.30,
                    "supply_shortage": 0.70,
                    "medical_emergency_delay": 0.80
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "winter only",
                    "recovery_timeline": "3-7 days"
                },
                "regional_variations": {
                    "northeast": 1.5,
                    "midwest": 1.3,
                    "mountain_states": 1.8,
                    "south": 0.3
                },
                "critical_needs": [
                    "Heat source",
                    "Food supply",
                    "Snow removal",
                    "Emergency access",
                    "Roof monitoring"
                ],
                "response_phases": {
                    "pre_storm": ["Stock supplies", "Fuel vehicles", "Prepare heat sources"],
                    "storm_arrival": ["Stay indoors", "Monitor conditions", "Conserve heat"],
                    "during_storm": ["Clear vents", "Check roof", "Maintain warmth"],
                    "post_storm": ["Clear exits", "Check neighbors", "Remove snow"],
                    "recovery": ["Restore travel", "Restock supplies", "Repair damage"]
                }
            },
            
            "supply_chain_collapse": {
                "name": "Supply Chain Collapse",
                "type": "supply_crisis",
                "base_characteristics": {
                    "duration": "months",
                    "warning_time": 48,
                    "severity": 6,
                    "affected_area": "national",
                    "occurrence_probability": 8.0
                },
                "cascading_effects": {
                    "food_shortage": 0.80,
                    "medicine_shortage": 0.75,
                    "fuel_shortage": 0.70,
                    "economic_impact": 0.85,
                    "social_tension": 0.60,
                    "black_market": 0.65
                },
                "temporal_factors": {
                    "worst_time": "any",
                    "seasonal_variation": "minimal",
                    "recovery_timeline": "3-6 months"
                },
                "regional_variations": {
                    "remote_areas": 1.8,
                    "islands": 2.0,
                    "urban": 1.3,
                    "agricultural": 0.7
                },
                "critical_needs": [
                    "Food stockpile",
                    "Essential medicines",
                    "Alternative suppliers",
                    "Local production",
                    "Barter networks"
                ],
                "response_phases": {
                    "early_warning": ["Stock essentials", "Identify alternatives", "Build networks"],
                    "shortage_begins": ["Ration supplies", "Share resources", "Find substitutes"],
                    "acute_phase": ["Community coordination", "Local production", "Barter systems"],
                    "adaptation": ["New supply chains", "Changed habits", "Self-sufficiency"],
                    "recovery": ["System rebuilding", "Stockpile renewal", "Resilience improvement"]
                }
            },
            
            "dam_failure": {
                "name": "Dam Failure/Burst",
                "type": "dam_failure",
                "base_characteristics": {
                    "duration": "hours",
                    "warning_time": 0.5,
                    "severity": 9,
                    "affected_area": "downstream_corridor",
                    "occurrence_probability": 1.0
                },
                "cascading_effects": {
                    "catastrophic_flooding": 0.95,
                    "destruction": 0.90,
                    "mass_casualties": 0.70,
                    "infrastructure_loss": 0.85,
                    "long_term_displacement": 0.80,
                    "environmental_damage": 0.75
                },
                "temporal_factors": {
                    "worst_time": "night",
                    "seasonal_variation": "spring high water",
                    "recovery_timeline": "years"
                },
                "regional_variations": {
                    "below_dams": 3.0,
                    "river_valleys": 2.0,
                    "highlands": 0.1
                },
                "critical_needs": [
                    "Immediate evacuation",
                    "High ground access",
                    "Swift water rescue",
                    "Emergency shelter",
                    "Long-term housing"
                ],
                "response_phases": {
                    "warning": ["Evacuate immediately", "Move to high ground", "Abandon property"],
                    "failure": ["Get as high as possible", "Call for rescue", "Signal location"],
                    "flood_wave": ["Hold on", "Stay together", "Wait for rescue"],
                    "immediate_after": ["Seek medical care", "Register as safe", "Find shelter"],
                    "long_term": ["Temporary housing", "Insurance claims", "Community rebuilding"]
                }
            }
        }
        
        # Create profiles in the risk engine database
        for key, profile in self.scenario_profiles.items():
            self.risk_engine.create_scenario_risk_profile(
                scenario_name=profile["name"],
                disaster_type=profile["type"],
                severity=profile["base_characteristics"]["severity"],
                warning_time=profile["base_characteristics"]["warning_time"],
                seasonal_factors=profile.get("temporal_factors", {}),
                regional_factors=profile.get("regional_variations", {}),
                cascading_risks=profile.get("cascading_effects", {}),
                mitigation_factors=profile.get("critical_needs", [])
            )
    
    def get_scenario_profile(self, scenario_name: str) -> Dict[str, Any]:
        """Get detailed profile for a specific scenario"""
        
        # Find matching profile
        for key, profile in self.scenario_profiles.items():
            if scenario_name.lower() in profile["name"].lower():
                return profile
        
        return None
    
    def assess_scenario(self, scenario_name: str, 
                       location: str = "suburban",
                       current_conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive assessment of a specific scenario
        
        Args:
            scenario_name: Name of the scenario to assess
            location: Location type
            current_conditions: Current environmental conditions
            
        Returns:
            Comprehensive assessment with profile and risk analysis
        """
        
        profile = self.get_scenario_profile(scenario_name)
        
        if not profile:
            return {"error": f"Scenario profile not found for: {scenario_name}"}
        
        # Create scenario dict for risk engine
        scenario = {
            "name": profile["name"],
            "type": profile["type"],
            "duration": profile["base_characteristics"]["duration"],
            "warning_time": profile["base_characteristics"]["warning_time"],
            "severity": profile["base_characteristics"]["severity"],
            "cascading_effects": list(profile.get("cascading_effects", {}).keys()),
            "primary_needs": profile.get("critical_needs", []),
            "affected_area": profile["base_characteristics"]["affected_area"]
        }
        
        # Get risk assessment
        risk_assessment = self.risk_engine.calculate_comprehensive_risk(
            scenario, location, current_conditions
        )
        
        # Combine with profile data
        comprehensive_assessment = {
            "profile": profile,
            "risk_assessment": risk_assessment,
            "response_guidance": self._generate_response_guidance(profile, risk_assessment),
            "resource_checklist": self._generate_resource_checklist(profile),
            "timeline": self._generate_response_timeline(profile, risk_assessment)
        }
        
        return comprehensive_assessment
    
    def _generate_response_guidance(self, profile: Dict[str, Any], 
                                   risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific response guidance based on profile and risk"""
        
        guidance = {
            "immediate_actions": [],
            "preparation_steps": [],
            "during_event": [],
            "post_event": [],
            "critical_decisions": []
        }
        
        # Extract from response phases
        phases = profile.get("response_phases", {})
        
        # Immediate actions based on time to impact
        time_to_impact = risk_assessment.get("time_to_impact", "Unknown")
        
        if time_to_impact == "Immediate":
            guidance["immediate_actions"] = phases.get(list(phases.keys())[0], []) if phases else []
        elif "hours" in str(time_to_impact):
            guidance["preparation_steps"] = phases.get(list(phases.keys())[0], []) if phases else []
        
        # During event actions
        for phase_name, actions in phases.items():
            if "during" in phase_name.lower():
                guidance["during_event"].extend(actions)
        
        # Post event actions
        for phase_name, actions in phases.items():
            if "after" in phase_name.lower() or "post" in phase_name.lower():
                guidance["post_event"].extend(actions)
        
        # Critical decisions based on risk level
        if risk_assessment["adjusted_risk_score"] > 70:
            guidance["critical_decisions"] = [
                "Evacuate vs shelter in place",
                "Resource allocation priorities",
                "Family separation contingencies",
                "Property protection vs personal safety"
            ]
        
        return guidance
    
    def _generate_resource_checklist(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate resource checklist for the scenario"""
        
        checklist = []
        critical_needs = profile.get("critical_needs", [])
        
        # Map needs to specific resources
        resource_mapping = {
            "Immediate shelter": ["Tent", "Tarps", "Sleeping bags", "Emergency blankets"],
            "Search and rescue": ["Whistle", "Flashlight", "First aid kit", "Rope"],
            "Medical care": ["First aid supplies", "Medications", "Emergency contacts", "Medical records"],
            "Evacuation transportation": ["Full gas tank", "Maps", "Cash", "Go bags"],
            "Emergency shelter": ["Shelter locations", "Bedding", "Clothing", "Toiletries"],
            "Storm supplies": ["Water", "Non-perishable food", "Batteries", "Radio"],
            "Alternative power": ["Generator", "Fuel", "Solar chargers", "Batteries"],
            "Heat source": ["Fireplace supplies", "Blankets", "Warm clothing", "Sleeping bags"],
            "Cash reserves": ["Small bills", "Coins", "Precious metals", "Barter items"],
            "Safe water source": ["Water filters", "Purification tablets", "Storage containers", "Boiling equipment"]
        }
        
        for need in critical_needs:
            resources = resource_mapping.get(need, [need])
            checklist.append({
                "category": need,
                "items": resources,
                "priority": "Critical" if profile["base_characteristics"]["severity"] > 7 else "Important"
            })
        
        return checklist
    
    def _generate_response_timeline(self, profile: Dict[str, Any], 
                                   risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate response timeline for the scenario"""
        
        timeline = []
        phases = profile.get("response_phases", {})
        
        for phase_name, actions in phases.items():
            timeline.append({
                "phase": phase_name,
                "actions": actions,
                "duration": self._estimate_phase_duration(phase_name),
                "priority": self._determine_phase_priority(phase_name, risk_assessment)
            })
        
        return timeline
    
    def _estimate_phase_duration(self, phase_name: str) -> str:
        """Estimate duration of a response phase"""
        
        if "immediate" in phase_name.lower() or "0-" in phase_name:
            return "Minutes"
        elif "hour" in phase_name.lower():
            return "Hours"
        elif "day" in phase_name.lower():
            return "Days"
        elif "week" in phase_name.lower():
            return "Weeks"
        elif "month" in phase_name.lower():
            return "Months"
        else:
            return "Variable"
    
    def _determine_phase_priority(self, phase_name: str, 
                                 risk_assessment: Dict[str, Any]) -> str:
        """Determine priority of a response phase"""
        
        if "immediate" in phase_name.lower() or "warning" in phase_name.lower():
            return "CRITICAL"
        elif "during" in phase_name.lower():
            return "HIGH"
        elif risk_assessment["adjusted_risk_score"] > 70:
            return "HIGH"
        else:
            return "MODERATE"
    
    def generate_all_profiles_report(self) -> str:
        """Generate comprehensive report of all scenario profiles"""
        
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE SCENARIO RISK PROFILES")
        report.append("=" * 80)
        report.append(f"Total Scenarios Profiled: {len(self.scenario_profiles)}")
        report.append("")
        
        # Sort by severity
        sorted_profiles = sorted(
            self.scenario_profiles.values(),
            key=lambda x: x["base_characteristics"]["severity"],
            reverse=True
        )
        
        for profile in sorted_profiles:
            report.append(f"{'='*60}")
            report.append(f"SCENARIO: {profile['name']}")
            report.append(f"{'='*60}")
            
            base = profile["base_characteristics"]
            report.append(f"Type: {profile['type'].upper()}")
            report.append(f"Severity: {base['severity']}/10")
            report.append(f"Duration: {base['duration']}")
            report.append(f"Warning Time: {base['warning_time']} hours")
            report.append(f"Affected Area: {base['affected_area']}")
            report.append(f"Annual Probability: {base['occurrence_probability']}%")
            
            report.append("\nTop Cascading Risks:")
            cascading = profile.get("cascading_effects", {})
            top_cascading = sorted(cascading.items(), key=lambda x: x[1], reverse=True)[:3]
            for effect, probability in top_cascading:
                report.append(f"  • {effect}: {probability*100:.0f}%")
            
            report.append("\nCritical Needs:")
            for need in profile.get("critical_needs", [])[:3]:
                report.append(f"  • {need}")
            
            report.append("\nResponse Phases:")
            phases = profile.get("response_phases", {})
            for phase_name in list(phases.keys())[:3]:
                report.append(f"  • {phase_name}")
            
            report.append("")
        
        report.append("=" * 80)
        report.append("END OF PROFILES REPORT")
        
        return "\n".join(report)
    
    def close(self):
        """Close connections"""
        self.risk_engine.close()


def main():
    """Test the Scenario Risk Profiles system"""
    
    print("🎯 Scenario-Specific Risk Profiles System")
    print("=" * 60)
    
    # Initialize profiles
    profiles = ScenarioRiskProfiles("test_scenario_profiles.db")
    
    # Test specific scenario assessment
    print("\n📊 Testing Major Earthquake Assessment")
    print("-" * 60)
    
    assessment = profiles.assess_scenario(
        "Major Earthquake",
        location="urban",
        current_conditions={"seismic_activity": 2.5}
    )
    
    if "error" not in assessment:
        risk = assessment["risk_assessment"]
        print(f"Scenario: {risk['scenario']}")
        print(f"Risk Score: {risk['adjusted_risk_score']:.1f}%")
        print(f"Probability: {risk['probability']:.1f}%")
        print(f"Action Priority: {risk['action_priority']}")
        
        print("\nResponse Guidance:")
        guidance = assessment["response_guidance"]
        if guidance["immediate_actions"]:
            print("Immediate Actions:")
            for action in guidance["immediate_actions"][:3]:
                print(f"  • {action}")
    
    # Generate summary report
    print("\n📑 Generating All Profiles Summary...")
    print("-" * 60)
    
    # Just show profile count
    print(f"Total Scenarios Profiled: {len(profiles.scenario_profiles)}")
    print("\nScenario Types:")
    types = set(p["type"] for p in profiles.scenario_profiles.values())
    for scenario_type in sorted(types):
        print(f"  • {scenario_type}")
    
    profiles.close()
    
    # Cleanup
    import os
    if os.path.exists("test_scenario_profiles.db"):
        os.remove("test_scenario_profiles.db")
    if os.path.exists("test_risk_engine.db"):
        os.remove("test_risk_engine.db")


if __name__ == "__main__":
    main()
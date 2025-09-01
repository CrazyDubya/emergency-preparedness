#!/usr/bin/env python3
"""
Local Production Capabilities Module - Version 2.0 Phase 2B
Enables long-term sustainability through local food production, water systems, 
energy generation, and essential manufacturing capabilities.
"""

import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional

class LocalProductionCapabilities:
    """
    Manages assessment and planning of local production capabilities for
    long-term disaster preparedness and community resilience.
    """
    
    def __init__(self, db_path: str = "local_production.db"):
        """Initialize the Local Production Capabilities system."""
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Create necessary database tables for production tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Production assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_date TEXT NOT NULL,
                household_size INTEGER NOT NULL,
                property_size REAL,
                property_type TEXT,
                assessment_data TEXT,
                overall_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Production systems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_systems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                system_type TEXT NOT NULL,
                system_name TEXT NOT NULL,
                capacity REAL,
                investment_cost REAL,
                ongoing_cost REAL,
                payback_period INTEGER,
                difficulty_level INTEGER,
                space_required REAL,
                system_details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Production goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_type TEXT NOT NULL,
                target_percentage REAL,
                timeline_months INTEGER,
                investment_budget REAL,
                progress_tracking TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Local resource inventory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_type TEXT NOT NULL,
                availability TEXT NOT NULL,
                seasonal_factors TEXT,
                acquisition_method TEXT,
                sustainability_score REAL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def assess_production_potential(self, household_size: int, property_size: float, 
                                 property_type: str) -> Dict[str, Any]:
        """
        Comprehensive assessment of local production potential across all categories.
        """
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'household_size': household_size,
            'property_size': property_size,
            'property_type': property_type,
            'food_production': self._assess_food_production(property_size, property_type),
            'water_systems': self._assess_water_systems(property_type, property_size),
            'energy_systems': self._assess_energy_systems(property_size, property_type),
            'manufacturing': self._assess_manufacturing_capabilities(property_size),
            'overall_score': 0,
            'priority_recommendations': [],
            'investment_timeline': {}
        }
        
        # Calculate overall production capability score
        subsystem_scores = [
            assessment['food_production']['overall_score'],
            assessment['water_systems']['overall_score'], 
            assessment['energy_systems']['overall_score'],
            assessment['manufacturing']['overall_score']
        ]
        
        assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        # Generate priority recommendations
        assessment['priority_recommendations'] = self._generate_priority_recommendations(assessment)
        
        # Create investment timeline
        assessment['investment_timeline'] = self._create_investment_timeline(assessment, household_size)
        
        # Store assessment in database
        self._store_assessment(assessment)
        
        return assessment
    
    def _assess_food_production(self, property_size: float, property_type: str) -> Dict[str, Any]:
        """Assess food production potential and capabilities."""
        
        food_assessment = {
            'vegetable_garden': {},
            'fruit_trees': {},
            'livestock': {},
            'preservation': {},
            'indoor_growing': {},
            'foraging': {},
            'overall_score': 0,
            'annual_yield_estimate': 0,
            'food_security_months': 0
        }
        
        # Vegetable garden assessment
        if property_type == "rural" and property_size >= 0.25:
            garden_space = min(property_size * 0.1, 0.5)  # Up to half acre for vegetables
            food_assessment['vegetable_garden'] = {
                'feasible_area': garden_space,
                'yield_per_sqft': 0.5,  # pounds per square foot annual average
                'annual_yield_lbs': garden_space * 43560 * 0.5,  # Convert acres to sq ft
                'investment_cost': garden_space * 43560 * 0.10,  # $0.10 per sq ft setup
                'ongoing_cost': garden_space * 43560 * 0.05,  # $0.05 per sq ft annually
                'difficulty': 3,
                'score': 9
            }
        elif property_type in ["suburban", "urban"] and property_size >= 0.05:
            garden_space = min(property_size * 0.2, 0.1)  # Up to 0.1 acres
            food_assessment['vegetable_garden'] = {
                'feasible_area': garden_space,
                'yield_per_sqft': 0.75,  # Higher yield with intensive methods
                'annual_yield_lbs': garden_space * 43560 * 0.75,
                'investment_cost': garden_space * 43560 * 0.15,
                'ongoing_cost': garden_space * 43560 * 0.08,
                'difficulty': 4,
                'score': 7
            }
        else:
            food_assessment['vegetable_garden'] = {
                'feasible_area': 0,
                'yield_per_sqft': 0,
                'annual_yield_lbs': 0,
                'investment_cost': 0,
                'ongoing_cost': 0,
                'difficulty': 0,
                'score': 0,
                'limitation': 'Insufficient space for traditional garden'
            }
        
        # Fruit tree assessment
        if property_size >= 0.1:
            tree_count = min(int(property_size * 20), 50)  # Max 50 trees
            food_assessment['fruit_trees'] = {
                'recommended_trees': tree_count,
                'mature_yield_lbs': tree_count * 100,  # 100 lbs per tree average
                'years_to_production': 3,
                'investment_cost': tree_count * 35,  # $35 per tree
                'ongoing_cost': tree_count * 15,  # $15 annual maintenance
                'difficulty': 2,
                'score': 8
            }
        else:
            food_assessment['fruit_trees'] = {
                'recommended_trees': 0,
                'mature_yield_lbs': 0,
                'years_to_production': 0,
                'investment_cost': 0,
                'ongoing_cost': 0,
                'difficulty': 0,
                'score': 1,
                'limitation': 'Space too small for fruit trees'
            }
        
        # Livestock assessment (chickens focus for most properties)
        if property_type == "rural" and property_size >= 0.25:
            food_assessment['livestock'] = {
                'chickens': {
                    'recommended_count': 25,
                    'egg_production_annual': 25 * 250,  # 250 eggs per hen
                    'meat_production_lbs': 25 * 4,  # 4 lbs per bird annually
                    'investment_cost': 2500,  # Coop, fencing, initial birds
                    'ongoing_cost': 750,  # Feed and care
                    'difficulty': 4,
                    'score': 8
                },
                'rabbits': {
                    'recommended_count': 10,
                    'meat_production_lbs': 10 * 5 * 6,  # 5 lbs per rabbit, 6 litters
                    'investment_cost': 800,
                    'ongoing_cost': 400,
                    'difficulty': 5,
                    'score': 7
                }
            }
        elif property_type == "suburban" and property_size >= 0.05:
            food_assessment['livestock'] = {
                'chickens': {
                    'recommended_count': 6,
                    'egg_production_annual': 6 * 250,
                    'meat_production_lbs': 0,  # Urban restrictions
                    'investment_cost': 800,
                    'ongoing_cost': 300,
                    'difficulty': 3,
                    'score': 6
                }
            }
        else:
            food_assessment['livestock'] = {
                'score': 2,
                'limitation': 'Space or regulations prevent livestock'
            }
        
        # Food preservation capabilities
        food_assessment['preservation'] = {
            'canning_capacity': {
                'jars_per_season': 200,
                'investment_cost': 400,
                'difficulty': 3,
                'score': 8
            },
            'dehydrating': {
                'lbs_per_month': 50,
                'investment_cost': 200,
                'difficulty': 2,
                'score': 9
            },
            'root_cellar': {
                'feasible': property_type == "rural",
                'capacity_lbs': 1000 if property_type == "rural" else 0,
                'investment_cost': 2000 if property_type == "rural" else 0,
                'difficulty': 6 if property_type == "rural" else 0,
                'score': 7 if property_type == "rural" else 3
            },
            'fermentation': {
                'capacity_gallons': 20,
                'investment_cost': 150,
                'difficulty': 4,
                'score': 7
            }
        }
        
        # Indoor growing systems
        food_assessment['indoor_growing'] = {
            'hydroponics': {
                'yield_lbs_annual': 200,
                'investment_cost': 1500,
                'ongoing_cost': 600,
                'difficulty': 6,
                'score': 6
            },
            'microgreens': {
                'yield_lbs_annual': 50,
                'investment_cost': 200,
                'ongoing_cost': 100,
                'difficulty': 3,
                'score': 8
            },
            'mushrooms': {
                'yield_lbs_annual': 100,
                'investment_cost': 300,
                'ongoing_cost': 150,
                'difficulty': 5,
                'score': 7
            }
        }
        
        # Foraging and wild food
        food_assessment['foraging'] = {
            'skill_required': 7,
            'seasonal_availability': 6,
            'legal_considerations': True,
            'safety_concerns': True,
            'yield_potential': 50,  # lbs per year with skill
            'score': 4
        }
        
        # Calculate total annual food production
        total_yield = 0
        if 'annual_yield_lbs' in food_assessment['vegetable_garden']:
            total_yield += food_assessment['vegetable_garden']['annual_yield_lbs']
        if 'mature_yield_lbs' in food_assessment['fruit_trees']:
            total_yield += food_assessment['fruit_trees']['mature_yield_lbs']
        
        # Add livestock yields
        if 'chickens' in food_assessment['livestock']:
            total_yield += food_assessment['livestock']['chickens'].get('meat_production_lbs', 0)
        
        # Add indoor growing
        total_yield += food_assessment['indoor_growing']['hydroponics']['yield_lbs_annual']
        total_yield += food_assessment['indoor_growing']['microgreens']['yield_lbs_annual'] 
        total_yield += food_assessment['indoor_growing']['mushrooms']['yield_lbs_annual']
        
        food_assessment['annual_yield_estimate'] = total_yield
        
        # Calculate food security months (assuming 2 lbs per person per day)
        daily_food_need = 2  # lbs per person
        if total_yield > 0:
            food_assessment['food_security_months'] = (total_yield / (daily_food_need * 365)) * 12
        
        # Calculate overall food production score
        subsystem_scores = []
        for system in ['vegetable_garden', 'fruit_trees', 'livestock']:
            if system in food_assessment and 'score' in food_assessment[system]:
                subsystem_scores.append(food_assessment[system]['score'])
        
        # Add preservation and indoor growing scores
        preservation_avg = sum([food_assessment['preservation'][k]['score'] 
                              for k in food_assessment['preservation']]) / len(food_assessment['preservation'])
        subsystem_scores.append(preservation_avg)
        
        indoor_avg = sum([food_assessment['indoor_growing'][k]['score'] 
                         for k in food_assessment['indoor_growing']]) / len(food_assessment['indoor_growing'])
        subsystem_scores.append(indoor_avg)
        
        subsystem_scores.append(food_assessment['foraging']['score'])
        
        food_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return food_assessment
    
    def _assess_water_systems(self, property_type: str, property_size: float) -> Dict[str, Any]:
        """Assess water production and management capabilities."""
        
        water_assessment = {
            'rainwater_harvesting': {},
            'well_water': {},
            'greywater_recycling': {},
            'blackwater_treatment': {},
            'storage_systems': {},
            'purification': {},
            'overall_score': 0,
            'daily_capacity_gallons': 0,
            'water_security_days': 0
        }
        
        # Rainwater harvesting assessment
        roof_area = 1500 if property_type == "suburban" else 2500 if property_type == "rural" else 800
        annual_rainfall = 30  # inches average
        harvestable_gallons = roof_area * annual_rainfall * 0.623 * 0.8  # 80% efficiency
        
        water_assessment['rainwater_harvesting'] = {
            'roof_area_sqft': roof_area,
            'annual_capacity_gallons': harvestable_gallons,
            'daily_average_gallons': harvestable_gallons / 365,
            'investment_cost': roof_area * 0.75,  # $0.75 per sq ft
            'storage_tanks_needed': math.ceil(harvestable_gallons * 0.1 / 275),  # 10% storage
            'difficulty': 4,
            'score': 8
        }
        
        # Well water assessment
        if property_type == "rural" and property_size >= 0.5:
            water_assessment['well_water'] = {
                'feasibility': 'high',
                'estimated_depth': 150,
                'daily_capacity_gallons': 1000,
                'investment_cost': 8000,
                'ongoing_cost': 200,
                'difficulty': 7,
                'score': 9,
                'backup_power_required': True
            }
        elif property_type == "suburban":
            water_assessment['well_water'] = {
                'feasibility': 'medium',
                'estimated_depth': 200,
                'daily_capacity_gallons': 500,
                'investment_cost': 12000,
                'ongoing_cost': 150,
                'difficulty': 8,
                'score': 6,
                'backup_power_required': True,
                'permit_required': True
            }
        else:
            water_assessment['well_water'] = {
                'feasibility': 'low',
                'score': 2,
                'limitation': 'Space or urban restrictions prevent well drilling'
            }
        
        # Greywater recycling
        water_assessment['greywater_recycling'] = {
            'sources': ['shower', 'sink', 'washing_machine'],
            'daily_capacity_gallons': 100,
            'uses': ['irrigation', 'toilet_flushing'],
            'investment_cost': 2500,
            'ongoing_cost': 100,
            'water_savings_percent': 30,
            'difficulty': 6,
            'score': 7
        }
        
        # Blackwater treatment (composting toilets)
        if property_type in ["rural", "suburban"]:
            water_assessment['blackwater_treatment'] = {
                'composting_toilets': {
                    'units_needed': 2,
                    'water_savings_gallons_daily': 24,  # 3 gallons per flush * 8 flushes
                    'investment_cost': 3000,
                    'maintenance_cost': 200,
                    'difficulty': 5,
                    'score': 6
                },
                'septic_system': {
                    'feasible': property_type == "rural",
                    'investment_cost': 8000 if property_type == "rural" else 0,
                    'score': 7 if property_type == "rural" else 4
                }
            }
        else:
            water_assessment['blackwater_treatment'] = {
                'score': 3,
                'limitation': 'Urban regulations limit blackwater treatment options'
            }
        
        # Water storage systems
        storage_capacity = 2000 if property_type == "rural" else 1000
        water_assessment['storage_systems'] = {
            'tank_capacity_gallons': storage_capacity,
            'tank_cost': storage_capacity * 1.5,
            'distribution_system_cost': 1500,
            'gravity_fed': property_type == "rural",
            'pump_required': property_type != "rural",
            'difficulty': 5,
            'score': 8
        }
        
        # Water purification systems
        water_assessment['purification'] = {
            'multi_stage_filter': {
                'capacity_gallons_daily': 500,
                'investment_cost': 800,
                'filter_replacement_cost': 200,
                'difficulty': 3,
                'score': 9
            },
            'uv_sterilization': {
                'capacity_gallons_daily': 1000,
                'investment_cost': 400,
                'ongoing_cost': 50,
                'difficulty': 4,
                'score': 8
            },
            'distillation': {
                'capacity_gallons_daily': 20,
                'investment_cost': 600,
                'energy_intensive': True,
                'difficulty': 5,
                'score': 6
            }
        }
        
        # Calculate total daily water capacity
        daily_capacity = water_assessment['rainwater_harvesting']['daily_average_gallons']
        if 'daily_capacity_gallons' in water_assessment['well_water']:
            daily_capacity += water_assessment['well_water']['daily_capacity_gallons']
        daily_capacity += water_assessment['greywater_recycling']['daily_capacity_gallons']
        
        water_assessment['daily_capacity_gallons'] = daily_capacity
        
        # Calculate water security days (50 gallons per person per day need)
        storage_total = water_assessment['storage_systems']['tank_capacity_gallons']
        daily_use = 50  # gallons per person
        if storage_total > 0 and daily_capacity > 0:
            # Days of stored water plus production capability
            water_assessment['water_security_days'] = storage_total / daily_use
        
        # Calculate overall water system score
        subsystem_scores = [
            water_assessment['rainwater_harvesting']['score'],
            water_assessment['well_water']['score'],
            water_assessment['greywater_recycling']['score'],
            water_assessment['storage_systems']['score']
        ]
        
        # Add blackwater and purification scores
        if 'score' in water_assessment['blackwater_treatment']:
            subsystem_scores.append(water_assessment['blackwater_treatment']['score'])
        
        purification_avg = sum([water_assessment['purification'][k]['score'] 
                               for k in water_assessment['purification']]) / len(water_assessment['purification'])
        subsystem_scores.append(purification_avg)
        
        water_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return water_assessment
    
    def _assess_energy_systems(self, property_size: float, property_type: str) -> Dict[str, Any]:
        """Assess energy production and storage capabilities."""
        
        energy_assessment = {
            'solar_power': {},
            'wind_power': {},
            'micro_hydro': {},
            'biomass': {},
            'battery_storage': {},
            'backup_generators': {},
            'energy_efficiency': {},
            'overall_score': 0,
            'daily_generation_kwh': 0,
            'energy_independence_percent': 0
        }
        
        # Solar power assessment
        roof_area = 1500 if property_type == "suburban" else 2500 if property_type == "rural" else 800
        usable_roof = roof_area * 0.7  # 70% usable for solar
        solar_capacity_kw = usable_roof / 100  # 1 kW per 100 sq ft
        daily_solar_kwh = solar_capacity_kw * 5  # 5 hours peak sun average
        
        energy_assessment['solar_power'] = {
            'usable_roof_area': usable_roof,
            'system_capacity_kw': solar_capacity_kw,
            'daily_generation_kwh': daily_solar_kwh,
            'annual_generation_kwh': daily_solar_kwh * 365,
            'investment_cost': solar_capacity_kw * 3000,  # $3000 per kW installed
            'battery_cost': solar_capacity_kw * 1500,  # $1500 per kW storage
            'payback_years': 8,
            'difficulty': 6,
            'score': 9
        }
        
        # Wind power assessment
        if property_type == "rural" and property_size >= 1.0:
            wind_capacity_kw = 5  # Small residential turbine
            energy_assessment['wind_power'] = {
                'feasible': True,
                'system_capacity_kw': wind_capacity_kw,
                'daily_generation_kwh': wind_capacity_kw * 6,  # 6 hours average wind
                'investment_cost': wind_capacity_kw * 4000,
                'zoning_requirements': True,
                'difficulty': 8,
                'score': 6
            }
        else:
            energy_assessment['wind_power'] = {
                'feasible': False,
                'score': 2,
                'limitation': 'Insufficient space or wind resources'
            }
        
        # Micro hydro assessment
        if property_type == "rural" and property_size >= 2.0:
            energy_assessment['micro_hydro'] = {
                'water_source_required': True,
                'system_capacity_kw': 2,
                'daily_generation_kwh': 48,  # 24/7 generation
                'investment_cost': 10000,
                'environmental_permits': True,
                'difficulty': 9,
                'score': 8,
                'limitation': 'Requires permanent water source with elevation drop'
            }
        else:
            energy_assessment['micro_hydro'] = {
                'feasible': False,
                'score': 1,
                'limitation': 'No suitable water source available'
            }
        
        # Biomass/wood energy
        if property_type == "rural":
            energy_assessment['biomass'] = {
                'wood_stove_heating': {
                    'btu_capacity': 80000,
                    'cords_needed_annually': 4,
                    'investment_cost': 3000,
                    'ongoing_cost': 800,
                    'difficulty': 4,
                    'score': 8
                },
                'wood_gasification': {
                    'electrical_output_kw': 10,
                    'daily_generation_kwh': 20,
                    'investment_cost': 15000,
                    'fuel_cost': 1000,
                    'difficulty': 9,
                    'score': 6
                }
            }
        elif property_type == "suburban":
            energy_assessment['biomass'] = {
                'wood_stove_heating': {
                    'btu_capacity': 40000,
                    'cords_needed_annually': 2,
                    'investment_cost': 2000,
                    'ongoing_cost': 600,
                    'difficulty': 3,
                    'score': 6,
                    'restrictions': 'May have local burning restrictions'
                }
            }
        else:
            energy_assessment['biomass'] = {
                'score': 2,
                'limitation': 'Urban restrictions prevent wood burning'
            }
        
        # Battery storage systems
        battery_capacity_kwh = solar_capacity_kw * 10  # 10 hours storage
        energy_assessment['battery_storage'] = {
            'lithium_system': {
                'capacity_kwh': battery_capacity_kwh,
                'days_autonomy': 2,
                'investment_cost': battery_capacity_kwh * 800,
                'replacement_years': 10,
                'difficulty': 5,
                'score': 8
            },
            'lead_acid_system': {
                'capacity_kwh': battery_capacity_kwh * 0.5,  # Lower usable capacity
                'days_autonomy': 1,
                'investment_cost': battery_capacity_kwh * 300,
                'replacement_years': 5,
                'difficulty': 4,
                'score': 6
            }
        }
        
        # Backup generators
        energy_assessment['backup_generators'] = {
            'propane_generator': {
                'capacity_kw': 20,
                'runtime_hours': 200,  # At 50% load
                'investment_cost': 4000,
                'fuel_cost_per_day': 25,
                'difficulty': 3,
                'score': 7
            },
            'diesel_generator': {
                'capacity_kw': 30,
                'runtime_hours': 300,
                'investment_cost': 6000,
                'fuel_cost_per_day': 35,
                'difficulty': 4,
                'score': 8,
                'fuel_storage_required': 500  # gallons
            }
        }
        
        # Energy efficiency measures
        energy_assessment['energy_efficiency'] = {
            'insulation_upgrade': {
                'energy_savings_percent': 30,
                'investment_cost': 5000,
                'payback_years': 5,
                'difficulty': 6,
                'score': 9
            },
            'led_lighting': {
                'energy_savings_percent': 75,
                'investment_cost': 500,
                'payback_years': 1,
                'difficulty': 1,
                'score': 10
            },
            'efficient_appliances': {
                'energy_savings_percent': 40,
                'investment_cost': 3000,
                'payback_years': 7,
                'difficulty': 2,
                'score': 8
            }
        }
        
        # Calculate total daily energy generation
        daily_generation = daily_solar_kwh
        if energy_assessment['wind_power']['feasible']:
            daily_generation += energy_assessment['wind_power']['daily_generation_kwh']
        if energy_assessment['micro_hydro']['feasible']:
            daily_generation += energy_assessment['micro_hydro']['daily_generation_kwh']
        
        energy_assessment['daily_generation_kwh'] = daily_generation
        
        # Calculate energy independence percentage
        typical_daily_use = 30  # kWh per day average home
        if daily_generation > 0:
            energy_assessment['energy_independence_percent'] = min((daily_generation / typical_daily_use) * 100, 100)
        
        # Calculate overall energy system score
        subsystem_scores = [
            energy_assessment['solar_power']['score'],
            energy_assessment['wind_power']['score'],
            energy_assessment['battery_storage']['lithium_system']['score'],
            energy_assessment['backup_generators']['propane_generator']['score']
        ]
        
        # Add biomass score
        if 'wood_stove_heating' in energy_assessment['biomass']:
            subsystem_scores.append(energy_assessment['biomass']['wood_stove_heating']['score'])
        else:
            subsystem_scores.append(energy_assessment['biomass']['score'])
        
        # Add efficiency average
        efficiency_avg = sum([energy_assessment['energy_efficiency'][k]['score'] 
                             for k in energy_assessment['energy_efficiency']]) / len(energy_assessment['energy_efficiency'])
        subsystem_scores.append(efficiency_avg)
        
        energy_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return energy_assessment
    
    def _assess_manufacturing_capabilities(self, property_size: float) -> Dict[str, Any]:
        """Assess local manufacturing and repair capabilities."""
        
        manufacturing = {
            'workshop_space': {},
            'tools_equipment': {},
            'raw_materials': {},
            'repair_capabilities': {},
            'production_capabilities': {},
            'skill_requirements': {},
            'overall_score': 0
        }
        
        # Workshop space assessment
        if property_size >= 0.25:
            workshop_sqft = min(property_size * 43560 * 0.02, 800)  # 2% of land or 800 sq ft max
            manufacturing['workshop_space'] = {
                'available_space_sqft': workshop_sqft,
                'climate_controlled': True,
                'power_requirements_kw': 10,
                'investment_cost': workshop_sqft * 60,  # $60 per sq ft
                'difficulty': 5,
                'score': 8
            }
        else:
            manufacturing['workshop_space'] = {
                'available_space_sqft': 100,  # Garage corner
                'climate_controlled': False,
                'power_requirements_kw': 3,
                'investment_cost': 2000,
                'difficulty': 3,
                'score': 4,
                'limitation': 'Limited to basic repair work'
            }
        
        # Tools and equipment assessment
        manufacturing['tools_equipment'] = {
            'basic_hand_tools': {
                'investment_cost': 1000,
                'capability_level': 7,
                'maintenance_cost': 100,
                'difficulty': 2,
                'score': 9
            },
            'power_tools': {
                'investment_cost': 3000,
                'capability_level': 8,
                'maintenance_cost': 300,
                'power_requirements_kw': 2,
                'difficulty': 4,
                'score': 8
            },
            'welding_equipment': {
                'investment_cost': 2000,
                'capability_level': 9,
                'maintenance_cost': 200,
                'power_requirements_kw': 5,
                'difficulty': 7,
                'score': 7,
                'skill_intensive': True
            },
            '3d_printer': {
                'investment_cost': 800,
                'capability_level': 6,
                'maintenance_cost': 200,
                'material_cost': 500,
                'difficulty': 6,
                'score': 6
            },
            'lathe_mill': {
                'investment_cost': 8000,
                'capability_level': 10,
                'maintenance_cost': 800,
                'power_requirements_kw': 8,
                'difficulty': 9,
                'score': 5,
                'space_required_sqft': 200
            }
        }
        
        # Raw materials storage and sourcing
        manufacturing['raw_materials'] = {
            'metal_stock': {
                'steel_aluminum_inventory': 500,  # lbs
                'storage_cost': 800,
                'ongoing_cost': 300,
                'score': 7
            },
            'lumber_inventory': {
                'board_feet': 1000,
                'storage_cost': 500,
                'ongoing_cost': 400,
                'score': 8
            },
            'fasteners_hardware': {
                'variety_score': 8,
                'inventory_cost': 600,
                'ongoing_cost': 200,
                'score': 9
            },
            'plastics_composites': {
                'filament_resin_inventory': 100,  # lbs
                'storage_cost': 300,
                'ongoing_cost': 250,
                'score': 6
            }
        }
        
        # Repair capabilities
        manufacturing['repair_capabilities'] = {
            'electronics_repair': {
                'capability_level': 6,
                'tool_investment': 800,
                'skill_level_required': 8,
                'score': 6
            },
            'mechanical_repair': {
                'capability_level': 8,
                'tool_investment': 2000,
                'skill_level_required': 6,
                'score': 8
            },
            'plumbing_electrical': {
                'capability_level': 7,
                'tool_investment': 1200,
                'skill_level_required': 5,
                'score': 7
            },
            'textile_repair': {
                'capability_level': 5,
                'tool_investment': 300,
                'skill_level_required': 4,
                'score': 8
            }
        }
        
        # Production capabilities
        manufacturing['production_capabilities'] = {
            'furniture_construction': {
                'output_pieces_per_month': 2,
                'market_value': 800,
                'material_cost': 200,
                'difficulty': 6,
                'score': 7
            },
            'tool_fabrication': {
                'output_tools_per_month': 10,
                'market_value': 300,
                'material_cost': 100,
                'difficulty': 8,
                'score': 6
            },
            'food_processing_equipment': {
                'capability_level': 5,
                'value_to_community': 9,
                'difficulty': 7,
                'score': 7
            },
            'building_components': {
                'output_value_per_month': 1000,
                'material_cost': 400,
                'difficulty': 8,
                'score': 6
            }
        }
        
        # Skill requirements and development
        manufacturing['skill_requirements'] = {
            'metalworking': {
                'current_skill_level': 3,  # Beginner
                'target_skill_level': 7,
                'training_time_hours': 200,
                'training_cost': 1500,
                'score': 4
            },
            'woodworking': {
                'current_skill_level': 5,  # Intermediate
                'target_skill_level': 8,
                'training_time_hours': 150,
                'training_cost': 800,
                'score': 6
            },
            'electronics': {
                'current_skill_level': 2,  # Basic
                'target_skill_level': 6,
                'training_time_hours': 300,
                'training_cost': 2000,
                'score': 3
            },
            'mechanical_systems': {
                'current_skill_level': 6,  # Good
                'target_skill_level': 8,
                'training_time_hours': 100,
                'training_cost': 600,
                'score': 7
            }
        }
        
        # Calculate overall manufacturing score
        subsystem_scores = []
        
        # Workshop and tools
        subsystem_scores.append(manufacturing['workshop_space']['score'])
        
        # Average tool scores
        tool_avg = sum([manufacturing['tools_equipment'][k]['score'] 
                       for k in manufacturing['tools_equipment']]) / len(manufacturing['tools_equipment'])
        subsystem_scores.append(tool_avg)
        
        # Materials and repair capabilities
        materials_avg = sum([manufacturing['raw_materials'][k]['score'] 
                           for k in manufacturing['raw_materials']]) / len(manufacturing['raw_materials'])
        subsystem_scores.append(materials_avg)
        
        repair_avg = sum([manufacturing['repair_capabilities'][k]['score'] 
                         for k in manufacturing['repair_capabilities']]) / len(manufacturing['repair_capabilities'])
        subsystem_scores.append(repair_avg)
        
        production_avg = sum([manufacturing['production_capabilities'][k]['score'] 
                            for k in manufacturing['production_capabilities']]) / len(manufacturing['production_capabilities'])
        subsystem_scores.append(production_avg)
        
        skills_avg = sum([manufacturing['skill_requirements'][k]['score'] 
                         for k in manufacturing['skill_requirements']]) / len(manufacturing['skill_requirements'])
        subsystem_scores.append(skills_avg)
        
        manufacturing['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return manufacturing
    
    def _generate_priority_recommendations(self, assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate priority recommendations based on assessment results."""
        
        recommendations = []
        
        # Analyze each subsystem for improvement opportunities
        subsystems = {
            'Food Production': assessment['food_production'],
            'Water Systems': assessment['water_systems'],
            'Energy Systems': assessment['energy_systems'],
            'Manufacturing': assessment['manufacturing']
        }
        
        # Sort subsystems by score (lowest first for priority)
        sorted_systems = sorted(subsystems.items(), key=lambda x: x[1]['overall_score'])
        
        for system_name, system_data in sorted_systems:
            if system_data['overall_score'] < 7:  # Systems needing improvement
                recommendations.extend(self._get_system_recommendations(system_name, system_data))
        
        # Sort recommendations by ROI and impact
        recommendations.sort(key=lambda x: (x['impact'], -x['cost'], -x['difficulty']), reverse=True)
        
        return recommendations[:10]  # Top 10 recommendations
    
    def _get_system_recommendations(self, system_name: str, system_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get specific recommendations for a system based on assessment."""
        
        recommendations = []
        
        if system_name == "Food Production":
            if system_data.get('vegetable_garden', {}).get('score', 0) < 5:
                recommendations.append({
                    'category': 'Food Production',
                    'title': 'Establish Vegetable Garden',
                    'description': 'Start with raised beds and intensive growing methods',
                    'cost': system_data.get('vegetable_garden', {}).get('investment_cost', 2000),
                    'time_to_implement': 30,  # days
                    'difficulty': 3,
                    'impact': 8,
                    'payback_months': 6
                })
            
            if system_data.get('fruit_trees', {}).get('score', 0) < 6:
                recommendations.append({
                    'category': 'Food Production',
                    'title': 'Plant Fruit Trees',
                    'description': 'Focus on fast-producing varieties like apple, pear, cherry',
                    'cost': system_data.get('fruit_trees', {}).get('investment_cost', 1000),
                    'time_to_implement': 14,
                    'difficulty': 2,
                    'impact': 7,
                    'payback_months': 36
                })
        
        elif system_name == "Water Systems":
            if system_data.get('rainwater_harvesting', {}).get('score', 0) < 7:
                recommendations.append({
                    'category': 'Water Systems',
                    'title': 'Install Rainwater Harvesting',
                    'description': 'Gutters, downspouts, and storage tanks for roof water collection',
                    'cost': system_data.get('rainwater_harvesting', {}).get('investment_cost', 3000),
                    'time_to_implement': 14,
                    'difficulty': 4,
                    'impact': 9,
                    'payback_months': 24
                })
        
        elif system_name == "Energy Systems":
            if system_data.get('solar_power', {}).get('score', 0) < 8:
                recommendations.append({
                    'category': 'Energy Systems',
                    'title': 'Install Solar Power System',
                    'description': 'Start with grid-tie system, add battery backup later',
                    'cost': system_data.get('solar_power', {}).get('investment_cost', 15000),
                    'time_to_implement': 60,
                    'difficulty': 6,
                    'impact': 9,
                    'payback_months': 96
                })
        
        elif system_name == "Manufacturing":
            if system_data.get('workshop_space', {}).get('score', 0) < 6:
                recommendations.append({
                    'category': 'Manufacturing',
                    'title': 'Establish Workshop Space',
                    'description': 'Dedicated space with basic tools and power supply',
                    'cost': system_data.get('workshop_space', {}).get('investment_cost', 5000),
                    'time_to_implement': 30,
                    'difficulty': 5,
                    'impact': 8,
                    'payback_months': 48
                })
        
        return recommendations
    
    def _create_investment_timeline(self, assessment: Dict[str, Any], 
                                  household_size: int) -> Dict[str, Any]:
        """Create a phased investment timeline for production capabilities."""
        
        timeline = {
            'phase_1_immediate': {
                'timeframe': '0-6 months',
                'budget': 5000,
                'projects': [],
                'expected_roi': {}
            },
            'phase_2_short_term': {
                'timeframe': '6-18 months', 
                'budget': 15000,
                'projects': [],
                'expected_roi': {}
            },
            'phase_3_medium_term': {
                'timeframe': '18-36 months',
                'budget': 25000,
                'projects': [],
                'expected_roi': {}
            },
            'phase_4_long_term': {
                'timeframe': '3-5 years',
                'budget': 40000,
                'projects': [],
                'expected_roi': {}
            },
            'total_investment': 85000,
            'projected_annual_savings': 0,
            'payback_period_years': 0
        }
        
        # Phase 1: Immediate low-cost high-impact projects
        phase_1_projects = [
            {
                'name': 'Basic vegetable garden setup',
                'cost': 800,
                'impact': 'Fresh vegetables for 4-6 months annually',
                'savings': 1200
            },
            {
                'name': 'Rainwater collection barrels',
                'cost': 400,
                'impact': '200-500 gallons storage capacity',
                'savings': 240
            },
            {
                'name': 'Basic hand tool kit',
                'cost': 600,
                'impact': 'Repair capability for common issues',
                'savings': 800
            },
            {
                'name': 'Food preservation supplies',
                'cost': 300,
                'impact': 'Extend harvest storage 6+ months',
                'savings': 600
            }
        ]
        timeline['phase_1_immediate']['projects'] = phase_1_projects
        timeline['phase_1_immediate']['expected_roi']['annual_savings'] = 2840
        
        # Phase 2: Short-term infrastructure
        phase_2_projects = [
            {
                'name': 'Expanded garden with fruit trees',
                'cost': 2500,
                'impact': '50% household vegetable/fruit needs',
                'savings': 2400
            },
            {
                'name': 'Rainwater harvesting system',
                'cost': 4000,
                'impact': '2000+ gallon annual collection',
                'savings': 800
            },
            {
                'name': 'Backup power system',
                'cost': 6000,
                'impact': '3-day power outage capability',
                'savings': 600
            },
            {
                'name': 'Workshop setup',
                'cost': 2500,
                'impact': 'Advanced repair and production capability',
                'savings': 1500
            }
        ]
        timeline['phase_2_short_term']['projects'] = phase_2_projects
        timeline['phase_2_short_term']['expected_roi']['annual_savings'] = 5300
        
        # Phase 3: Medium-term production systems
        phase_3_projects = [
            {
                'name': 'Solar power system',
                'cost': 15000,
                'impact': '80% energy independence',
                'savings': 2400
            },
            {
                'name': 'Livestock system (chickens)',
                'cost': 3000,
                'impact': 'Eggs and meat production',
                'savings': 1800
            },
            {
                'name': 'Advanced water systems',
                'cost': 7000,
                'impact': 'Complete water independence',
                'savings': 1200
            }
        ]
        timeline['phase_3_medium_term']['projects'] = phase_3_projects
        timeline['phase_3_medium_term']['expected_roi']['annual_savings'] = 5400
        
        # Phase 4: Long-term advanced systems
        phase_4_projects = [
            {
                'name': 'Advanced manufacturing setup',
                'cost': 20000,
                'impact': 'Local production and community services',
                'savings': 3000
            },
            {
                'name': 'Well water system',
                'cost': 12000,
                'impact': 'Unlimited clean water supply',
                'savings': 1500
            },
            {
                'name': 'Advanced food production',
                'cost': 8000,
                'impact': '90% food self-sufficiency',
                'savings': 4000
            }
        ]
        timeline['phase_4_long_term']['projects'] = phase_4_projects
        timeline['phase_4_long_term']['expected_roi']['annual_savings'] = 8500
        
        # Calculate total projected savings and payback
        total_annual_savings = 2840 + 5300 + 5400 + 8500
        timeline['projected_annual_savings'] = total_annual_savings
        
        if total_annual_savings > 0:
            timeline['payback_period_years'] = timeline['total_investment'] / total_annual_savings
        
        return timeline
    
    def _store_assessment(self, assessment: Dict[str, Any]):
        """Store the production assessment in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO production_assessments 
            (assessment_date, household_size, property_size, property_type, 
             assessment_data, overall_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            assessment['timestamp'],
            assessment['household_size'],
            assessment['property_size'],
            assessment['property_type'],
            json.dumps(assessment),
            assessment['overall_score']
        ))
        
        conn.commit()
        conn.close()
    
    def create_production_plan(self, assessment: Dict[str, Any], 
                             budget: float, timeframe_months: int) -> Dict[str, Any]:
        """
        Create a detailed production implementation plan based on assessment and constraints.
        """
        
        plan = {
            'plan_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'created_date': datetime.now().isoformat(),
            'budget_available': budget,
            'timeframe_months': timeframe_months,
            'selected_projects': [],
            'project_timeline': {},
            'resource_requirements': {},
            'expected_outcomes': {},
            'risk_assessment': {},
            'success_metrics': {}
        }
        
        # Select projects based on budget and timeframe constraints
        available_projects = self._extract_feasible_projects(assessment, budget, timeframe_months)
        
        # Prioritize projects by ROI and impact
        prioritized_projects = sorted(available_projects, 
                                    key=lambda x: (x['roi'], x['impact']), reverse=True)
        
        # Select projects within budget
        selected_projects = []
        remaining_budget = budget
        
        for project in prioritized_projects:
            if project['cost'] <= remaining_budget:
                selected_projects.append(project)
                remaining_budget -= project['cost']
        
        plan['selected_projects'] = selected_projects
        
        # Create detailed timeline
        plan['project_timeline'] = self._create_detailed_timeline(selected_projects, timeframe_months)
        
        # Calculate resource requirements
        plan['resource_requirements'] = self._calculate_resource_requirements(selected_projects)
        
        # Project expected outcomes
        plan['expected_outcomes'] = self._project_outcomes(selected_projects, assessment)
        
        # Assess risks
        plan['risk_assessment'] = self._assess_project_risks(selected_projects)
        
        # Define success metrics
        plan['success_metrics'] = self._define_success_metrics(selected_projects, assessment)
        
        return plan
    
    def _extract_feasible_projects(self, assessment: Dict[str, Any], 
                                 budget: float, timeframe_months: int) -> List[Dict[str, Any]]:
        """Extract all feasible projects from assessment data."""
        
        projects = []
        
        # Food production projects
        food_data = assessment['food_production']
        if 'vegetable_garden' in food_data and food_data['vegetable_garden'].get('investment_cost', 0) > 0:
            projects.append({
                'category': 'Food Production',
                'name': 'Vegetable Garden System',
                'cost': food_data['vegetable_garden']['investment_cost'],
                'time_months': 2,
                'difficulty': food_data['vegetable_garden']['difficulty'],
                'impact': 8,
                'roi': food_data['vegetable_garden'].get('annual_yield_lbs', 0) * 3 / food_data['vegetable_garden']['investment_cost'],
                'annual_savings': food_data['vegetable_garden'].get('annual_yield_lbs', 0) * 3,
                'space_required': food_data['vegetable_garden'].get('feasible_area', 0)
            })
        
        if 'fruit_trees' in food_data and food_data['fruit_trees'].get('investment_cost', 0) > 0:
            projects.append({
                'category': 'Food Production',
                'name': 'Fruit Tree Orchard',
                'cost': food_data['fruit_trees']['investment_cost'],
                'time_months': 6,
                'difficulty': food_data['fruit_trees']['difficulty'],
                'impact': 7,
                'roi': food_data['fruit_trees'].get('mature_yield_lbs', 0) * 2 / food_data['fruit_trees']['investment_cost'],
                'annual_savings': food_data['fruit_trees'].get('mature_yield_lbs', 0) * 2,
                'space_required': food_data['fruit_trees'].get('recommended_trees', 0) * 100
            })
        
        # Water system projects
        water_data = assessment['water_systems']
        if 'rainwater_harvesting' in water_data:
            projects.append({
                'category': 'Water Systems',
                'name': 'Rainwater Harvesting System',
                'cost': water_data['rainwater_harvesting']['investment_cost'],
                'time_months': 1,
                'difficulty': water_data['rainwater_harvesting']['difficulty'],
                'impact': 9,
                'roi': 1200 / water_data['rainwater_harvesting']['investment_cost'],  # Water bill savings
                'annual_savings': 1200,
                'space_required': 200
            })
        
        if water_data['well_water'].get('feasibility') == 'high':
            projects.append({
                'category': 'Water Systems',
                'name': 'Well Water System',
                'cost': water_data['well_water']['investment_cost'],
                'time_months': 3,
                'difficulty': water_data['well_water']['difficulty'],
                'impact': 9,
                'roi': 2000 / water_data['well_water']['investment_cost'],
                'annual_savings': 2000,
                'space_required': 100
            })
        
        # Energy system projects
        energy_data = assessment['energy_systems']
        if 'solar_power' in energy_data:
            projects.append({
                'category': 'Energy Systems',
                'name': 'Solar Power System',
                'cost': energy_data['solar_power']['investment_cost'],
                'time_months': 4,
                'difficulty': energy_data['solar_power']['difficulty'],
                'impact': 9,
                'roi': 2400 / energy_data['solar_power']['investment_cost'],  # Electric bill savings
                'annual_savings': 2400,
                'space_required': energy_data['solar_power']['usable_roof_area']
            })
        
        # Manufacturing projects
        manufacturing_data = assessment['manufacturing']
        if 'workshop_space' in manufacturing_data:
            projects.append({
                'category': 'Manufacturing',
                'name': 'Workshop Setup',
                'cost': manufacturing_data['workshop_space']['investment_cost'],
                'time_months': 2,
                'difficulty': manufacturing_data['workshop_space']['difficulty'],
                'impact': 7,
                'roi': 1500 / manufacturing_data['workshop_space']['investment_cost'],  # Repair savings
                'annual_savings': 1500,
                'space_required': manufacturing_data['workshop_space']['available_space_sqft']
            })
        
        # Filter projects by budget and timeframe
        feasible_projects = [p for p in projects 
                           if p['cost'] <= budget and p['time_months'] <= timeframe_months]
        
        return feasible_projects
    
    def _create_detailed_timeline(self, selected_projects: List[Dict[str, Any]], 
                                timeframe_months: int) -> Dict[str, Any]:
        """Create detailed timeline for selected projects."""
        
        timeline = {
            'total_duration_months': timeframe_months,
            'project_schedule': [],
            'monthly_breakdown': {},
            'critical_path': [],
            'resource_conflicts': []
        }
        
        # Sort projects by priority (ROI and dependencies)
        sorted_projects = sorted(selected_projects, 
                               key=lambda x: (x['impact'], x['roi']), reverse=True)
        
        current_month = 0
        for project in sorted_projects:
            start_month = current_month
            end_month = current_month + project['time_months']
            
            timeline['project_schedule'].append({
                'project_name': project['name'],
                'category': project['category'],
                'start_month': start_month,
                'end_month': end_month,
                'duration_months': project['time_months'],
                'cost': project['cost'],
                'dependencies': []
            })
            
            # Add to monthly breakdown
            for month in range(start_month, end_month):
                if month not in timeline['monthly_breakdown']:
                    timeline['monthly_breakdown'][month] = []
                
                timeline['monthly_breakdown'][month].append({
                    'project': project['name'],
                    'activity': f"Implementation - Month {month - start_month + 1}",
                    'cost': project['cost'] / project['time_months']
                })
            
            current_month += project['time_months']
            
            # Ensure we don't exceed timeframe
            if current_month >= timeframe_months:
                break
        
        return timeline
    
    def _calculate_resource_requirements(self, selected_projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total resource requirements for selected projects."""
        
        requirements = {
            'total_budget': sum([p['cost'] for p in selected_projects]),
            'labor_hours': {},
            'materials': {},
            'equipment': {},
            'permits_licenses': {},
            'ongoing_costs': {}
        }
        
        # Estimate labor requirements by category
        labor_multipliers = {
            'Food Production': 20,  # hours per $1000
            'Water Systems': 15,
            'Energy Systems': 10,  # More professional installation
            'Manufacturing': 25
        }
        
        for project in selected_projects:
            category = project['category']
            if category in labor_multipliers:
                hours = (project['cost'] / 1000) * labor_multipliers[category]
                if category not in requirements['labor_hours']:
                    requirements['labor_hours'][category] = 0
                requirements['labor_hours'][category] += hours
        
        # Common materials needed
        requirements['materials'] = {
            'concrete_bags': 20,
            'lumber_board_feet': 500,
            'plumbing_fittings': 150,
            'electrical_supplies': 300,
            'hardware_fasteners': 100,
            'estimated_material_cost': sum([p['cost'] * 0.4 for p in selected_projects])
        }
        
        # Equipment that may need rental or purchase
        requirements['equipment'] = {
            'excavator_rental_days': 3,
            'concrete_mixer_rental_days': 5,
            'specialized_tools_purchase': 1200,
            'safety_equipment': 400
        }
        
        # Permits and licenses
        requirements['permits_licenses'] = {
            'building_permits': 500,
            'electrical_permits': 200,
            'plumbing_permits': 150,
            'well_drilling_permits': 300 if any('Well' in p['name'] for p in selected_projects) else 0
        }
        
        # Ongoing costs (annual)
        requirements['ongoing_costs'] = {
            'maintenance_annual': sum([p['cost'] * 0.05 for p in selected_projects]),
            'insurance_increase': sum([p['cost'] * 0.02 for p in selected_projects]),
            'consumables_annual': 800,
            'utilities_change': -1200  # Savings from reduced utility bills
        }
        
        return requirements
    
    def _project_outcomes(self, selected_projects: List[Dict[str, Any]], 
                         assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Project expected outcomes from selected projects."""
        
        outcomes = {
            'production_improvements': {},
            'cost_savings': {},
            'resilience_improvements': {},
            'timeline_to_benefits': {},
            'long_term_projections': {}
        }
        
        # Production improvements
        total_food_production = sum([p['annual_savings'] for p in selected_projects 
                                   if p['category'] == 'Food Production'])
        total_energy_production = sum([p['annual_savings'] for p in selected_projects 
                                     if p['category'] == 'Energy Systems'])
        
        outcomes['production_improvements'] = {
            'food_self_sufficiency_percent': min((total_food_production / 8000) * 100, 90),  # $8000 annual food cost
            'energy_independence_percent': min((total_energy_production / 3000) * 100, 95),  # $3000 annual electric
            'water_independence_percent': 80 if any('Water' in p['category'] for p in selected_projects) else 20,
            'manufacturing_capability_score': 8 if any('Manufacturing' in p['category'] for p in selected_projects) else 3
        }
        
        # Annual cost savings
        outcomes['cost_savings'] = {
            'year_1': sum([p['annual_savings'] * 0.5 for p in selected_projects]),  # Partial first year
            'year_2': sum([p['annual_savings'] for p in selected_projects]),
            'year_5': sum([p['annual_savings'] * 1.2 for p in selected_projects]),  # 20% efficiency gains
            'year_10': sum([p['annual_savings'] * 1.5 for p in selected_projects]),  # 50% efficiency gains
            'total_10_year_savings': sum([p['annual_savings'] * 12 for p in selected_projects])
        }
        
        # Resilience improvements
        outcomes['resilience_improvements'] = {
            'power_outage_duration_days': 14 if any('Energy' in p['category'] for p in selected_projects) else 1,
            'water_shortage_duration_days': 60 if any('Water' in p['category'] for p in selected_projects) else 3,
            'food_shortage_duration_days': 120 if any('Food' in p['category'] for p in selected_projects) else 14,
            'supply_chain_independence_percent': 65,
            'community_value_score': 8
        }
        
        # Timeline to benefits
        outcomes['timeline_to_benefits'] = {
            'immediate_benefits': ['Reduced grocery bills', 'Lower utility costs', 'Increased self-reliance'],
            'short_term_benefits': ['Significant cost savings', 'Emergency preparedness', 'Skill development'],
            'long_term_benefits': ['Complete system integration', 'Community leadership', 'Wealth building'],
            'break_even_months': 24,
            'full_roi_years': 5
        }
        
        # Long-term projections (10 years)
        total_investment = sum([p['cost'] for p in selected_projects])
        total_savings = outcomes['cost_savings']['total_10_year_savings']
        
        outcomes['long_term_projections'] = {
            'net_financial_benefit': total_savings - total_investment,
            'annual_roi_percent': ((total_savings / 10) / total_investment) * 100,
            'property_value_increase': total_investment * 0.7,  # 70% of investment adds to property value
            'emergency_preparedness_score': 85,  # Out of 100
            'sustainability_score': 75  # Out of 100
        }
        
        return outcomes
    
    def _assess_project_risks(self, selected_projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess risks associated with selected projects."""
        
        risks = {
            'financial_risks': {},
            'technical_risks': {},
            'timeline_risks': {},
            'regulatory_risks': {},
            'market_risks': {},
            'mitigation_strategies': {}
        }
        
        total_investment = sum([p['cost'] for p in selected_projects])
        
        # Financial risks
        risks['financial_risks'] = {
            'cost_overrun_probability': 0.3,
            'expected_cost_overrun_percent': 15,
            'financing_challenges': total_investment > 25000,
            'cash_flow_impact': 'moderate' if total_investment < 50000 else 'high',
            'roi_uncertainty': 'low' if len(selected_projects) <= 3 else 'moderate'
        }
        
        # Technical risks
        risks['technical_risks'] = {
            'skill_gap_challenges': max([p['difficulty'] for p in selected_projects]) > 7,
            'equipment_failure_risk': 'moderate',
            'maintenance_complexity': 'low' if max([p['difficulty'] for p in selected_projects]) < 6 else 'high',
            'integration_challenges': len(set([p['category'] for p in selected_projects])) > 2
        }
        
        # Timeline risks  
        risks['timeline_risks'] = {
            'weather_delays': any('outdoor' in p.get('type', '') for p in selected_projects),
            'permit_delays': any('permit' in p.get('requirements', []) for p in selected_projects),
            'supply_chain_delays': 0.2,
            'contractor_availability': 'seasonal_concern'
        }
        
        # Regulatory risks
        risks['regulatory_risks'] = {
            'zoning_compliance': any(p['category'] == 'Manufacturing' for p in selected_projects),
            'building_code_changes': 'low',
            'environmental_regulations': any('Water' in p['category'] for p in selected_projects),
            'utility_interconnection': any('Energy' in p['category'] for p in selected_projects)
        }
        
        # Market risks
        risks['market_risks'] = {
            'utility_rate_changes': 'moderate',
            'food_price_volatility': 'moderate',
            'technology_obsolescence': 'low_5_year_horizon',
            'resale_value_uncertainty': 'low'
        }
        
        # Mitigation strategies
        risks['mitigation_strategies'] = {
            'financial': [
                'Maintain 20% contingency budget',
                'Phase projects to spread costs',
                'Investigate grants and tax incentives'
            ],
            'technical': [
                'Start with lower-difficulty projects',
                'Invest in training and education',
                'Build relationships with contractors'
            ],
            'timeline': [
                'Plan projects during optimal seasons',
                'Submit permits early',
                'Maintain flexible scheduling'
            ],
            'regulatory': [
                'Research all requirements before starting',
                'Maintain good relationships with inspectors',
                'Consider professional assistance for complex projects'
            ],
            'market': [
                'Focus on projects with stable returns',
                'Diversify across multiple benefit categories',
                'Monitor policy changes that could affect returns'
            ]
        }
        
        return risks
    
    def _define_success_metrics(self, selected_projects: List[Dict[str, Any]], 
                              assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Define specific success metrics for the production plan."""
        
        metrics = {
            'financial_metrics': {},
            'production_metrics': {},
            'resilience_metrics': {},
            'sustainability_metrics': {},
            'milestone_tracking': {},
            'measurement_methods': {}
        }
        
        # Financial metrics
        total_investment = sum([p['cost'] for p in selected_projects])
        annual_savings = sum([p['annual_savings'] for p in selected_projects])
        
        metrics['financial_metrics'] = {
            'total_investment_budget': total_investment,
            'annual_cost_savings_target': annual_savings,
            'break_even_timeline_months': (total_investment / (annual_savings / 12)) if annual_savings > 0 else 999,
            'roi_3_year_target': 150,  # 150% return over 3 years
            'property_value_increase_target': total_investment * 0.7
        }
        
        # Production metrics
        metrics['production_metrics'] = {
            'food_production_lbs_annual': sum([p['annual_savings'] / 3 for p in selected_projects 
                                             if p['category'] == 'Food Production']),
            'energy_production_kwh_annual': 8000 if any('Energy' in p['category'] for p in selected_projects) else 0,
            'water_collection_gallons_annual': 5000 if any('Water' in p['category'] for p in selected_projects) else 0,
            'manufacturing_projects_annual': 12 if any('Manufacturing' in p['category'] for p in selected_projects) else 0
        }
        
        # Resilience metrics
        metrics['resilience_metrics'] = {
            'power_outage_preparedness_days': 7,
            'water_shortage_preparedness_days': 30,
            'food_shortage_preparedness_days': 90,
            'supply_chain_independence_score': 70,
            'emergency_response_time_minutes': 15
        }
        
        # Sustainability metrics
        metrics['sustainability_metrics'] = {
            'carbon_footprint_reduction_percent': 40,
            'waste_reduction_percent': 60,
            'local_resource_utilization_percent': 80,
            'renewable_energy_percent': 75,
            'water_conservation_percent': 50
        }
        
        # Milestone tracking
        metrics['milestone_tracking'] = {
            'month_3': {
                'projects_completed': 1,
                'budget_spent_percent': 25,
                'systems_operational': ['Basic food production']
            },
            'month_6': {
                'projects_completed': 2,
                'budget_spent_percent': 50,
                'systems_operational': ['Food production', 'Water collection']
            },
            'month_12': {
                'projects_completed': len(selected_projects),
                'budget_spent_percent': 100,
                'systems_operational': 'All planned systems',
                'savings_realized_percent': 75
            },
            'month_24': {
                'roi_achievement_percent': 100,
                'system_optimization_complete': True,
                'community_integration_level': 'High'
            }
        }
        
        # Measurement methods
        metrics['measurement_methods'] = {
            'financial_tracking': 'Monthly expense/savings spreadsheet with receipts',
            'production_tracking': 'Weekly harvest/output logs with weights and quantities',
            'energy_monitoring': 'Smart meter readings and production monitoring systems',
            'water_monitoring': 'Flow meters and storage level indicators',
            'resilience_testing': 'Quarterly emergency simulation exercises',
            'sustainability_assessment': 'Annual third-party sustainability audit'
        }
        
        return metrics
    
    def generate_production_report(self, assessment_data: Dict[str, Any] = None) -> str:
        """Generate a comprehensive ASCII report of production capabilities."""
        
        if not assessment_data:
            # Get most recent assessment from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT assessment_data FROM production_assessments ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return "No assessment data available. Run assess_production_potential() first."
            
            assessment_data = json.loads(result[0])
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                        LOCAL PRODUCTION CAPABILITIES REPORT                 ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        report.append("")
        
        # Assessment overview
        report.append("📊 ASSESSMENT OVERVIEW")
        report.append("=" * 80)
        report.append(f"Assessment Date: {assessment_data['timestamp'][:10]}")
        report.append(f"Household Size: {assessment_data['household_size']} people")
        report.append(f"Property Size: {assessment_data['property_size']} acres")
        report.append(f"Property Type: {assessment_data['property_type'].title()}")
        report.append(f"Overall Score: {assessment_data['overall_score']:.1f}/10")
        report.append("")
        
        # Create score bar
        score = assessment_data['overall_score']
        filled_bars = int(score)
        empty_bars = 10 - filled_bars
        score_bar = "█" * filled_bars + "░" * empty_bars
        report.append(f"Production Readiness: [{score_bar}] {score:.1f}/10")
        report.append("")
        
        # Subsystem scores
        subsystems = [
            ("🥕 Food Production", assessment_data['food_production']['overall_score']),
            ("💧 Water Systems", assessment_data['water_systems']['overall_score']),
            ("⚡ Energy Systems", assessment_data['energy_systems']['overall_score']),
            ("🔧 Manufacturing", assessment_data['manufacturing']['overall_score'])
        ]
        
        report.append("🎯 SUBSYSTEM PERFORMANCE")
        report.append("=" * 80)
        for name, score in subsystems:
            filled = int(score)
            empty = 10 - filled
            bar = "█" * filled + "░" * empty
            report.append(f"{name:<20} [{bar}] {score:.1f}/10")
        report.append("")
        
        # Food production details
        food_data = assessment_data['food_production']
        report.append("🥕 FOOD PRODUCTION ANALYSIS")
        report.append("=" * 80)
        report.append(f"Annual Yield Estimate: {food_data['annual_yield_estimate']:.0f} lbs")
        report.append(f"Food Security Duration: {food_data['food_security_months']:.1f} months")
        report.append("")
        
        # Food production breakdown
        if 'vegetable_garden' in food_data and 'annual_yield_lbs' in food_data['vegetable_garden']:
            garden = food_data['vegetable_garden']
            report.append(f"Vegetable Garden: {garden['feasible_area']:.2f} acres → {garden['annual_yield_lbs']:.0f} lbs/year")
        
        if 'fruit_trees' in food_data and 'mature_yield_lbs' in food_data['fruit_trees']:
            trees = food_data['fruit_trees']
            report.append(f"Fruit Trees: {trees['recommended_trees']} trees → {trees['mature_yield_lbs']:.0f} lbs/year")
        
        if 'livestock' in food_data and 'chickens' in food_data['livestock']:
            chickens = food_data['livestock']['chickens']
            report.append(f"Chickens: {chickens['recommended_count']} birds → {chickens['egg_production_annual']} eggs/year")
        report.append("")
        
        # Water systems details
        water_data = assessment_data['water_systems']
        report.append("💧 WATER SYSTEMS ANALYSIS")
        report.append("=" * 80)
        report.append(f"Daily Capacity: {water_data['daily_capacity_gallons']:.0f} gallons")
        report.append(f"Water Security: {water_data['water_security_days']:.0f} days storage")
        report.append("")
        
        # Water system breakdown
        if 'rainwater_harvesting' in water_data:
            rain = water_data['rainwater_harvesting']
            report.append(f"Rainwater Harvest: {rain['annual_capacity_gallons']:.0f} gal/year from {rain['roof_area_sqft']} sq ft roof")
        
        if water_data['well_water'].get('feasibility') == 'high':
            well = water_data['well_water']
            report.append(f"Well Water: {well['daily_capacity_gallons']} gal/day capacity")
        report.append("")
        
        # Energy systems details
        energy_data = assessment_data['energy_systems']
        report.append("⚡ ENERGY SYSTEMS ANALYSIS")
        report.append("=" * 80)
        report.append(f"Daily Generation: {energy_data['daily_generation_kwh']:.1f} kWh")
        report.append(f"Energy Independence: {energy_data['energy_independence_percent']:.1f}%")
        report.append("")
        
        # Energy system breakdown
        if 'solar_power' in energy_data:
            solar = energy_data['solar_power']
            report.append(f"Solar System: {solar['system_capacity_kw']:.1f} kW → {solar['daily_generation_kwh']:.1f} kWh/day")
        
        if energy_data['wind_power']['feasible']:
            wind = energy_data['wind_power']
            report.append(f"Wind System: {wind['system_capacity_kw']:.1f} kW → {wind['daily_generation_kwh']:.1f} kWh/day")
        report.append("")
        
        # Manufacturing capabilities
        manufacturing_data = assessment_data['manufacturing']
        report.append("🔧 MANUFACTURING ANALYSIS")
        report.append("=" * 80)
        
        workshop = manufacturing_data['workshop_space']
        report.append(f"Workshop Space: {workshop['available_space_sqft']:.0f} sq ft")
        report.append(f"Power Available: {workshop.get('power_requirements_kw', 0)} kW")
        report.append("")
        
        # Priority recommendations
        if 'priority_recommendations' in assessment_data:
            report.append("🎯 PRIORITY RECOMMENDATIONS")
            report.append("=" * 80)
            
            for i, rec in enumerate(assessment_data['priority_recommendations'][:5], 1):
                report.append(f"{i}. {rec['title']} (${rec['cost']:,.0f})")
                report.append(f"   {rec['description']}")
                report.append(f"   Impact: {rec['impact']}/10 | Difficulty: {rec['difficulty']}/10 | ROI: {rec['payback_months']} months")
                report.append("")
        
        # Investment timeline
        if 'investment_timeline' in assessment_data:
            timeline = assessment_data['investment_timeline']
            report.append("💰 INVESTMENT TIMELINE")
            report.append("=" * 80)
            
            phases = [
                ("Phase 1 (0-6 months)", timeline['phase_1_immediate']),
                ("Phase 2 (6-18 months)", timeline['phase_2_short_term']),
                ("Phase 3 (18-36 months)", timeline['phase_3_medium_term']),
                ("Phase 4 (3-5 years)", timeline['phase_4_long_term'])
            ]
            
            for phase_name, phase_data in phases:
                report.append(f"{phase_name}: ${phase_data['budget']:,}")
                for project in phase_data['projects'][:2]:  # Show first 2 projects
                    report.append(f"  • {project['name']} (${project['cost']:,})")
                report.append("")
            
            report.append(f"Total Investment: ${timeline['total_investment']:,}")
            report.append(f"Projected Annual Savings: ${timeline['projected_annual_savings']:,}")
            report.append(f"Payback Period: {timeline['payback_period_years']:.1f} years")
        
        report.append("")
        report.append("━" * 80)
        report.append("🎯 NEXT STEPS: Review recommendations and select Phase 1 projects to begin implementation")
        report.append("━" * 80)
        
        return "\n".join(report)

# Example usage and testing
if __name__ == "__main__":
    print("Local Production Capabilities Module - Test Suite")
    print("=" * 60)
    
    # Initialize the system
    production_system = LocalProductionCapabilities("test_local_production.db")
    
    # Test assessment for different property types
    test_scenarios = [
        {"household_size": 4, "property_size": 0.25, "property_type": "suburban"},
        {"household_size": 2, "property_size": 2.0, "property_type": "rural"},
        {"household_size": 6, "property_size": 0.1, "property_type": "urban"}
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 TEST SCENARIO {i}: {scenario['property_type'].title()} Property")
        print("-" * 50)
        
        assessment = production_system.assess_production_potential(
            scenario['household_size'],
            scenario['property_size'],
            scenario['property_type']
        )
        
        print(f"Overall Score: {assessment['overall_score']:.1f}/10")
        print(f"Food Production: {assessment['food_production']['overall_score']:.1f}/10")
        print(f"Water Systems: {assessment['water_systems']['overall_score']:.1f}/10")
        print(f"Energy Systems: {assessment['energy_systems']['overall_score']:.1f}/10")
        print(f"Manufacturing: {assessment['manufacturing']['overall_score']:.1f}/10")
        
        # Test production plan creation
        plan = production_system.create_production_plan(assessment, 15000, 18)
        print(f"\nProduction Plan: {len(plan['selected_projects'])} projects selected")
        print(f"Total Investment: ${plan['resource_requirements']['total_budget']:,.0f}")
        print(f"Expected Break-even: {plan['expected_outcomes']['timeline_to_benefits']['break_even_months']} months")
        
        if i == 1:  # Generate full report for first scenario
            print(f"\n📊 FULL ASSESSMENT REPORT")
            print("=" * 80)
            report = production_system.generate_production_report(assessment)
            print(report)
    
    print(f"\n✅ Local Production Capabilities Module test completed successfully!")
    print("🎯 Module ready for integration with main preparedness system")
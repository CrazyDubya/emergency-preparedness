#!/usr/bin/env python3
"""
Extended Supply Planning Module - Version 2.0
Long-term sustainability planning beyond traditional 72-hour preparations

Target: Improve long-term scenario planning from 51% to 70%+
"""

import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import calendar

class ExtendedSupplyPlanningModule:
    def __init__(self, db_path: str = "long_term_sustainability.db"):
        """Initialize Extended Supply Planning Module for 6+ month scenarios"""
        self.db_path = db_path
        self.init_database()
        self.load_long_term_scenarios()
        self.initialize_supply_systems()
    
    def init_database(self):
        """Initialize database for extended supply planning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Long-term supply calculations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS long_term_supplies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supply_category TEXT NOT NULL,
                item_name TEXT NOT NULL,
                daily_consumption REAL,
                monthly_consumption REAL,
                seasonal_factor REAL,
                storage_method TEXT,
                shelf_life_months INTEGER,
                rotation_frequency TEXT,
                cost_per_unit REAL,
                bulk_discount_threshold INTEGER,
                local_source_available BOOLEAN,
                notes TEXT
            )
        ''')
        
        # Seasonal planning adjustments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seasonal_planning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT NOT NULL,
                supply_category TEXT,
                consumption_multiplier REAL,
                availability_factor REAL,
                storage_considerations TEXT,
                special_requirements TEXT,
                preparation_timeline TEXT
            )
        ''')
        
        # Storage optimization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage_systems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                storage_type TEXT NOT NULL,
                capacity_cubic_feet REAL,
                climate_control BOOLEAN,
                pest_protection BOOLEAN,
                access_frequency TEXT,
                cost_estimate REAL,
                maintenance_schedule TEXT,
                suitable_items TEXT,
                installation_requirements TEXT
            )
        ''')
        
        # Resource sharing networks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_type TEXT NOT NULL,
                network_name TEXT,
                member_count INTEGER,
                resource_categories TEXT,
                sharing_protocols TEXT,
                coordination_method TEXT,
                trust_level INTEGER,
                geographic_range TEXT,
                emergency_contacts TEXT
            )
        ''')
        
        # Supply chain alternatives
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS supply_alternatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                standard_item TEXT NOT NULL,
                alternative_source TEXT,
                alternative_item TEXT,
                availability_rating INTEGER,
                cost_comparison REAL,
                quality_comparison INTEGER,
                procurement_method TEXT,
                lead_time TEXT,
                minimum_quantity INTEGER
            )
        ''')
        
        # Long-term scenarios tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scenario_planning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_name TEXT NOT NULL,
                duration_months INTEGER,
                affected_systems TEXT,
                supply_disruption_percent INTEGER,
                resource_priorities TEXT,
                adaptation_strategies TEXT,
                success_metrics TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_long_term_scenarios(self):
        """Load scenarios requiring long-term sustainability"""
        self.long_term_scenarios = {
            "economic_collapse": {
                "duration_months": 24,
                "supply_disruption": 80,
                "affected_systems": ["banking", "supply_chains", "employment", "currency"],
                "critical_needs": ["food_production", "barter_goods", "skill_trading", "local_currency"],
                "timeline": "Years to full recovery"
            },
            "supply_chain_failure": {
                "duration_months": 18,
                "supply_disruption": 90,
                "affected_systems": ["food_distribution", "fuel_delivery", "medical_supplies", "manufacturing"],
                "critical_needs": ["local_production", "resource_pooling", "alternative_suppliers", "rationing"],
                "timeline": "Multiple seasons affected"
            },
            "extended_power_outage": {
                "duration_months": 6,
                "supply_disruption": 60,
                "affected_systems": ["refrigeration", "heating", "water_pumps", "communications"],
                "critical_needs": ["food_preservation", "manual_systems", "fuel_reserves", "medical_needs"],
                "timeline": "Infrastructure rebuild required"
            },
            "pandemic_isolation": {
                "duration_months": 18,
                "supply_disruption": 50,
                "affected_systems": ["social_contact", "work", "schools", "healthcare"],
                "critical_needs": ["mental_health", "education", "income_alternatives", "medical_care"],
                "timeline": "Social and economic recovery"
            },
            "climate_disruption": {
                "duration_months": 60,
                "supply_disruption": 70,
                "affected_systems": ["agriculture", "water_supply", "weather_patterns", "migration"],
                "critical_needs": ["food_security", "water_management", "climate_adaptation", "relocation"],
                "timeline": "Permanent lifestyle changes"
            }
        }
        
        # Consumption patterns for different timeframes
        self.consumption_patterns = {
            "food": {
                "daily_calories": 2200,
                "storage_forms": ["canned", "dried", "frozen", "fresh", "preserved"],
                "preservation_methods": ["dehydration", "fermentation", "smoking", "canning", "root_cellar"],
                "seasonal_variations": {"winter": 1.1, "spring": 0.9, "summer": 0.8, "fall": 1.0}
            },
            "water": {
                "daily_gallons": 1.5,  # Drinking/cooking only
                "hygiene_gallons": 2.5,
                "cleaning_gallons": 5.0,
                "sources": ["stored", "collected", "purified", "well", "municipal"],
                "seasonal_variations": {"winter": 0.8, "spring": 1.0, "summer": 1.3, "fall": 1.0}
            },
            "energy": {
                "daily_kwh": 15,  # Reduced consumption
                "heating_therms": 2.0,
                "transportation_gallons": 0.5,
                "sources": ["solar", "wind", "generator", "battery", "manual"],
                "seasonal_variations": {"winter": 1.5, "spring": 0.9, "summer": 1.1, "fall": 1.0}
            },
            "medical": {
                "prescription_days": 90,
                "otc_medicine": "monthly",
                "first_aid": "quarterly",
                "sources": ["pharmacy", "online", "natural", "veterinary", "international"],
                "seasonal_variations": {"winter": 1.2, "spring": 1.0, "summer": 0.9, "fall": 1.1}
            }
        }
    
    def initialize_supply_systems(self):
        """Initialize comprehensive long-term supply systems"""
        self.supply_systems = {
            "food_categories": {
                "grains": {"rice": 365, "wheat": 365, "oats": 180, "pasta": 730},
                "proteins": {"beans": 1095, "lentils": 1095, "canned_meat": 1460, "nuts": 365},
                "fats": {"oil": 730, "butter_powder": 730, "coconut_oil": 1095},
                "vegetables": {"canned": 1095, "dehydrated": 1825, "frozen": 365},
                "fruits": {"canned": 1095, "dried": 365, "frozen": 365},
                "dairy": {"powdered_milk": 730, "cheese_powder": 365, "canned": 1095},
                "seasonings": {"salt": 3650, "sugar": 1460, "spices": 1095},
                "beverages": {"coffee": 365, "tea": 1095, "cocoa": 730}
            },
            "storage_methods": {
                "mylar_bags": {"capacity": "5-50 lbs", "lifespan": "25+ years", "suitable": ["grains", "beans", "sugar"]},
                "food_grade_buckets": {"capacity": "35-50 lbs", "lifespan": "20+ years", "suitable": ["bulk_items"]},
                "mason_jars": {"capacity": "1-2 lbs", "lifespan": "indefinite", "suitable": ["spices", "small_items"]},
                "root_cellar": {"capacity": "1000+ lbs", "lifespan": "seasonal", "suitable": ["vegetables", "fruits"]},
                "freezer": {"capacity": "200-700 lbs", "lifespan": "12 months", "suitable": ["meat", "vegetables"]},
                "pantry": {"capacity": "100-500 lbs", "lifespan": "varies", "suitable": ["canned_goods", "dry_goods"]}
            },
            "preservation_equipment": {
                "dehydrator": {"cost": 200, "capacity": "10 lbs/batch", "power": "500W", "preservation": "years"},
                "pressure_canner": {"cost": 150, "capacity": "20 jars", "power": "none", "preservation": "25+ years"},
                "vacuum_sealer": {"cost": 100, "capacity": "unlimited", "power": "100W", "preservation": "5x longer"},
                "grain_mill": {"cost": 300, "capacity": "50 lbs/hour", "power": "manual", "preservation": "fresh_flour"},
                "fermentation_vessels": {"cost": 50, "capacity": "5 gallons", "power": "none", "preservation": "months"}
            }
        }
    
    def calculate_extended_supplies(self, family_size: int = 4, duration_months: int = 6, 
                                   scenario: str = "general") -> Dict:
        """Calculate comprehensive supply requirements for extended scenarios"""
        calculation = {
            "calculation_date": datetime.now().isoformat(),
            "family_size": family_size,
            "duration_months": duration_months,
            "scenario": scenario,
            "supply_categories": {},
            "total_cost": 0,
            "storage_requirements": {},
            "seasonal_adjustments": {},
            "procurement_timeline": {}
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate for each supply category
        categories = ["food", "water", "energy", "medical", "hygiene", "tools", "fuel", "seeds"]
        
        for category in categories:
            category_calc = self._calculate_category_needs(category, family_size, duration_months, scenario)
            calculation["supply_categories"][category] = category_calc
            calculation["total_cost"] += category_calc.get("total_cost", 0)
            
            # Store in database
            for item_name, details in category_calc.get("items", {}).items():
                cursor.execute('''
                    INSERT OR REPLACE INTO long_term_supplies
                    (supply_category, item_name, daily_consumption, monthly_consumption,
                     seasonal_factor, storage_method, shelf_life_months, cost_per_unit)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (category, item_name, details.get("daily", 0), 
                      details.get("monthly", 0), details.get("seasonal", 1.0),
                      details.get("storage", "standard"), details.get("shelf_life", 12),
                      details.get("cost_per_unit", 0)))
        
        conn.commit()
        conn.close()
        
        # Calculate storage requirements
        calculation["storage_requirements"] = self._calculate_storage_needs(calculation["supply_categories"])
        
        # Add seasonal adjustments
        calculation["seasonal_adjustments"] = self._calculate_seasonal_adjustments(duration_months)
        
        # Create procurement timeline
        calculation["procurement_timeline"] = self._create_procurement_timeline(calculation["supply_categories"], duration_months)
        
        # Add sustainability metrics
        calculation["sustainability_metrics"] = {
            "self_sufficiency_months": min(duration_months, self._calculate_self_sufficiency(calculation)),
            "resupply_frequency": self._calculate_resupply_needs(calculation),
            "storage_utilization": self._calculate_storage_efficiency(calculation),
            "cost_per_month": calculation["total_cost"] / duration_months
        }
        
        return calculation
    
    def _calculate_category_needs(self, category: str, family_size: int, 
                                duration_months: int, scenario: str) -> Dict:
        """Calculate needs for specific supply category"""
        category_data = {
            "category": category,
            "items": {},
            "total_quantity": 0,
            "total_cost": 0,
            "storage_volume": 0,
            "seasonal_variation": 1.0
        }
        
        if category == "food":
            # Food calculations based on caloric needs
            daily_calories = 2200 * family_size
            monthly_calories = daily_calories * 30
            total_calories = monthly_calories * duration_months
            
            # Break down by food categories
            food_breakdown = {
                "grains": {"percent": 0.40, "cost_per_1000_cal": 0.50},
                "proteins": {"percent": 0.25, "cost_per_1000_cal": 2.00},
                "fats": {"percent": 0.15, "cost_per_1000_cal": 1.50},
                "vegetables": {"percent": 0.10, "cost_per_1000_cal": 1.00},
                "fruits": {"percent": 0.05, "cost_per_1000_cal": 1.25},
                "dairy": {"percent": 0.03, "cost_per_1000_cal": 1.75},
                "seasonings": {"percent": 0.02, "cost_per_1000_cal": 3.00}
            }
            
            for food_type, data in food_breakdown.items():
                calories_needed = total_calories * data["percent"]
                cost = (calories_needed / 1000) * data["cost_per_1000_cal"]
                
                category_data["items"][food_type] = {
                    "calories": calories_needed,
                    "daily": calories_needed / (duration_months * 30),
                    "monthly": calories_needed / duration_months,
                    "total_cost": cost,
                    "storage": self._get_optimal_storage(food_type),
                    "shelf_life": self._get_shelf_life(food_type)
                }
                
                category_data["total_cost"] += cost
        
        elif category == "water":
            # Water calculations - multiple use categories
            daily_drinking = 1.0 * family_size  # gallons
            daily_cooking = 0.5 * family_size
            daily_hygiene = 2.0 * family_size
            daily_cleaning = 3.0 * family_size
            
            total_daily = daily_drinking + daily_cooking + daily_hygiene + daily_cleaning
            total_needed = total_daily * duration_months * 30
            
            # Storage and purification costs
            storage_cost = (total_needed / 55) * 15  # 55-gal drums at $15 each
            purification_cost = 500  # Filtration and purification equipment
            
            category_data["items"]["stored_water"] = {
                "gallons": total_needed * 0.3,  # 30% stored
                "daily": total_daily * 0.3,
                "monthly": total_daily * 30 * 0.3,
                "total_cost": storage_cost,
                "storage": "water_barrels",
                "shelf_life": 6
            }
            
            category_data["items"]["purification_system"] = {
                "gallons": total_needed * 0.7,  # 70% purified
                "daily": total_daily * 0.7,
                "monthly": total_daily * 30 * 0.7,
                "total_cost": purification_cost,
                "storage": "equipment",
                "shelf_life": 120
            }
            
            category_data["total_cost"] = storage_cost + purification_cost
        
        elif category == "energy":
            # Energy calculations - electricity, heating, transportation
            daily_kwh = 15 * family_size * 0.6  # Reduced consumption
            daily_heating = 2.0 if duration_months >= 3 else 0.5  # Therms
            daily_fuel = 0.5 * family_size  # Gallons for transportation
            
            # Solar system for electricity
            solar_cost = daily_kwh * 365 * 2.0  # $2 per kWh capacity
            battery_cost = daily_kwh * 500  # $500 per kWh storage
            
            category_data["items"]["solar_system"] = {
                "kwh_capacity": daily_kwh,
                "daily": daily_kwh,
                "monthly": daily_kwh * 30,
                "total_cost": solar_cost + battery_cost,
                "storage": "equipment",
                "shelf_life": 300  # 25 years
            }
            
            # Fuel reserves
            total_fuel = daily_fuel * duration_months * 30
            fuel_cost = total_fuel * 3.50  # $3.50 per gallon
            
            category_data["items"]["fuel_reserves"] = {
                "gallons": total_fuel,
                "daily": daily_fuel,
                "monthly": daily_fuel * 30,
                "total_cost": fuel_cost,
                "storage": "fuel_containers",
                "shelf_life": 12
            }
            
            category_data["total_cost"] = solar_cost + battery_cost + fuel_cost
        
        elif category == "medical":
            # Medical supplies for extended periods
            base_cost_per_person = 200  # Basic medical kit
            prescription_cost = 500 * family_size  # 6+ months prescriptions
            advanced_supplies = 300  # Surgical/dental supplies
            
            category_data["items"]["basic_medical"] = {
                "kits": family_size,
                "total_cost": base_cost_per_person * family_size,
                "storage": "medical_cabinet",
                "shelf_life": 60
            }
            
            category_data["items"]["prescriptions"] = {
                "months_supply": duration_months * 1.5,  # 50% buffer
                "total_cost": prescription_cost,
                "storage": "refrigerated",
                "shelf_life": duration_months
            }
            
            category_data["total_cost"] = (base_cost_per_person * family_size) + prescription_cost + advanced_supplies
        
        # Add scenario-specific adjustments
        if scenario == "economic_collapse":
            category_data["total_cost"] *= 1.5  # Higher costs, limited availability
        elif scenario == "supply_chain_failure":
            category_data["total_cost"] *= 1.3  # Some price increases
        elif scenario == "extended_power_outage":
            if category == "energy":
                category_data["total_cost"] *= 2.0  # Critical need for alternatives
        
        return category_data
    
    def _calculate_storage_needs(self, supply_categories: Dict) -> Dict:
        """Calculate total storage requirements"""
        storage = {
            "total_cubic_feet": 0,
            "storage_types": {},
            "climate_controlled": 0,
            "pest_protected": 0,
            "accessible": 0,
            "long_term": 0
        }
        
        # Estimate storage volumes by category
        volume_estimates = {
            "food": 1.5,  # cubic feet per person per month
            "water": 7.5,  # 1 gallon = 0.134 cubic feet
            "energy": 10,  # Equipment and fuel storage
            "medical": 2,   # Compact but climate controlled
            "hygiene": 1,   # Relatively compact
            "tools": 5,     # Bulky items
            "fuel": 15,     # Large volume requirements
            "seeds": 0.5    # Very compact
        }
        
        for category, data in supply_categories.items():
            if category in volume_estimates:
                volume = volume_estimates[category] * data.get("total_quantity", 1)
                storage["total_cubic_feet"] += volume
                storage["storage_types"][category] = volume
        
        return storage
    
    def _calculate_seasonal_adjustments(self, duration_months: int) -> Dict:
        """Calculate seasonal consumption adjustments"""
        adjustments = {}
        
        current_month = datetime.now().month
        for month_offset in range(duration_months):
            month = ((current_month + month_offset - 1) % 12) + 1
            season = self._get_season(month)
            
            adjustments[f"month_{month_offset + 1}"] = {
                "month": calendar.month_name[month],
                "season": season,
                "heating_factor": self._get_heating_factor(month),
                "cooling_factor": self._get_cooling_factor(month),
                "food_availability": self._get_food_availability(month),
                "weather_challenges": self._get_weather_challenges(month)
            }
        
        return adjustments
    
    def _create_procurement_timeline(self, supply_categories: Dict, duration_months: int) -> Dict:
        """Create timeline for acquiring long-term supplies"""
        timeline = {
            "immediate": [],  # 0-1 months
            "short_term": [],  # 1-3 months
            "medium_term": [],  # 3-6 months
            "long_term": []  # 6+ months
        }
        
        # Prioritize by shelf life and criticality
        for category, data in supply_categories.items():
            for item, details in data.get("items", {}).items():
                shelf_life = details.get("shelf_life", 12)
                cost = details.get("total_cost", 0)
                
                priority_score = self._calculate_procurement_priority(category, item, shelf_life, cost)
                
                if priority_score >= 9 or category in ["medical", "water"]:
                    timeline["immediate"].append({
                        "item": f"{category}: {item}",
                        "cost": cost,
                        "priority": priority_score,
                        "reason": "Critical/high priority"
                    })
                elif priority_score >= 7 or shelf_life <= 6:
                    timeline["short_term"].append({
                        "item": f"{category}: {item}",
                        "cost": cost,
                        "priority": priority_score,
                        "reason": "Important/limited shelf life"
                    })
                elif priority_score >= 5:
                    timeline["medium_term"].append({
                        "item": f"{category}: {item}",
                        "cost": cost,
                        "priority": priority_score,
                        "reason": "Standard priority"
                    })
                else:
                    timeline["long_term"].append({
                        "item": f"{category}: {item}",
                        "cost": cost,
                        "priority": priority_score,
                        "reason": "Low priority/very long shelf life"
                    })
        
        # Sort each timeline by priority
        for period in timeline:
            timeline[period].sort(key=lambda x: x["priority"], reverse=True)
        
        return timeline
    
    def create_seasonal_plan(self, duration_months: int = 12) -> Dict:
        """Create comprehensive seasonal preparedness plan"""
        plan = {
            "plan_date": datetime.now().isoformat(),
            "duration_months": duration_months,
            "seasonal_cycles": {},
            "growing_seasons": {},
            "preservation_schedule": {},
            "weather_preparations": {},
            "resource_availability": {}
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Plan for each season
        seasons = ["spring", "summer", "fall", "winter"]
        for season in seasons:
            season_plan = {
                "months": self._get_season_months(season),
                "preparations": self._get_seasonal_preparations(season),
                "challenges": self._get_seasonal_challenges(season),
                "opportunities": self._get_seasonal_opportunities(season),
                "resource_priorities": self._get_seasonal_priorities(season)
            }
            
            plan["seasonal_cycles"][season] = season_plan
            
            # Store in database
            cursor.execute('''
                INSERT OR REPLACE INTO seasonal_planning
                (season, supply_category, consumption_multiplier, availability_factor,
                 storage_considerations, special_requirements, preparation_timeline)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (season, "general", season_plan.get("consumption_multiplier", 1.0),
                  season_plan.get("availability_factor", 1.0),
                  json.dumps(season_plan.get("storage_considerations", [])),
                  json.dumps(season_plan.get("special_requirements", [])),
                  json.dumps(season_plan.get("preparation_timeline", []))))
        
        conn.commit()
        conn.close()
        
        # Growing seasons for food production
        plan["growing_seasons"] = {
            "spring_planting": {
                "crops": ["lettuce", "spinach", "peas", "radishes", "carrots"],
                "start_date": "March 15",
                "harvest_date": "May-June",
                "yield_estimate": "50-100 lbs per family"
            },
            "summer_planting": {
                "crops": ["tomatoes", "peppers", "squash", "beans", "corn"],
                "start_date": "May 15",
                "harvest_date": "July-September",
                "yield_estimate": "200-400 lbs per family"
            },
            "fall_planting": {
                "crops": ["kale", "cabbage", "brussels_sprouts", "turnips"],
                "start_date": "August 15",
                "harvest_date": "October-December",
                "yield_estimate": "100-200 lbs per family"
            },
            "winter_storage": {
                "crops": ["potatoes", "onions", "garlic", "winter_squash"],
                "storage_method": "root_cellar",
                "storage_duration": "3-6 months",
                "yield_estimate": "300-500 lbs per family"
            }
        }
        
        # Preservation schedule
        plan["preservation_schedule"] = {
            "spring": ["dehydrate_greens", "ferment_vegetables", "freeze_herbs"],
            "summer": ["can_tomatoes", "dehydrate_fruits", "freeze_vegetables", "make_preserves"],
            "fall": ["can_applesauce", "dehydrate_peppers", "cure_meats", "ferment_cabbage"],
            "winter": ["maintain_stores", "rotate_inventory", "plan_next_year"]
        }
        
        return plan
    
    def design_storage_system(self, total_volume: float, budget: float = 2000) -> Dict:
        """Design optimal storage system for long-term supplies"""
        design = {
            "design_date": datetime.now().isoformat(),
            "total_volume": total_volume,
            "budget": budget,
            "storage_solutions": {},
            "total_cost": 0,
            "optimization_score": 0,
            "maintenance_schedule": {}
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Storage solution options
        storage_options = [
            {
                "type": "basement_shelving",
                "capacity": 200,  # cubic feet
                "cost": 300,
                "climate_control": False,
                "pest_protection": True,
                "accessibility": "excellent",
                "suitable_items": ["canned_goods", "dry_goods", "tools"]
            },
            {
                "type": "food_grade_buckets",
                "capacity": 2,  # cubic feet each
                "cost": 25,
                "climate_control": False,
                "pest_protection": True,
                "accessibility": "good",
                "suitable_items": ["grains", "beans", "sugar", "salt"]
            },
            {
                "type": "chest_freezer",
                "capacity": 25,
                "cost": 400,
                "climate_control": True,
                "pest_protection": True,
                "accessibility": "good",
                "suitable_items": ["meat", "vegetables", "prepared_foods"]
            },
            {
                "type": "root_cellar",
                "capacity": 100,
                "cost": 1500,
                "climate_control": "natural",
                "pest_protection": True,
                "accessibility": "fair",
                "suitable_items": ["vegetables", "fruits", "preserves"]
            },
            {
                "type": "garage_shelving",
                "capacity": 300,
                "cost": 200,
                "climate_control": False,
                "pest_protection": False,
                "accessibility": "excellent",
                "suitable_items": ["tools", "fuel", "equipment"]
            }
        ]
        
        # Optimize storage allocation
        remaining_volume = total_volume
        remaining_budget = budget
        
        for option in sorted(storage_options, key=lambda x: x["cost"] / x["capacity"]):
            if remaining_volume <= 0 or remaining_budget <= 0:
                break
            
            if remaining_budget >= option["cost"]:
                if option["capacity"] >= 2:  # Can get multiple units
                    units_needed = min(int(remaining_volume / option["capacity"]), 
                                     int(remaining_budget / option["cost"]))
                    if units_needed > 0:
                        total_capacity = units_needed * option["capacity"]
                        total_cost = units_needed * option["cost"]
                        
                        design["storage_solutions"][option["type"]] = {
                            "units": units_needed,
                            "capacity_per_unit": option["capacity"],
                            "total_capacity": total_capacity,
                            "cost_per_unit": option["cost"],
                            "total_cost": total_cost,
                            "suitable_items": option["suitable_items"]
                        }
                        
                        remaining_volume -= total_capacity
                        remaining_budget -= total_cost
                        design["total_cost"] += total_cost
                        
                        # Store in database
                        cursor.execute('''
                            INSERT INTO storage_systems
                            (storage_type, capacity_cubic_feet, climate_control,
                             pest_protection, cost_estimate, suitable_items)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (option["type"], total_capacity, 
                              option["climate_control"], option["pest_protection"],
                              total_cost, json.dumps(option["suitable_items"])))
        
        conn.commit()
        conn.close()
        
        # Calculate optimization metrics
        volume_utilized = total_volume - remaining_volume
        design["optimization_score"] = (volume_utilized / total_volume) * 100
        design["budget_utilized"] = budget - remaining_budget
        design["cost_per_cubic_foot"] = design["total_cost"] / volume_utilized if volume_utilized > 0 else 0
        
        # Maintenance schedule
        design["maintenance_schedule"] = {
            "weekly": ["Check temperatures", "Rotate accessible items"],
            "monthly": ["Inventory check", "Pest inspection", "Climate monitoring"],
            "quarterly": ["Deep cleaning", "Equipment maintenance", "Reorganization"],
            "annually": ["Full audit", "Upgrade planning", "Pest control treatment"]
        }
        
        return design
    
    def calculate_resupply_networks(self, supply_categories: Dict) -> Dict:
        """Calculate and plan resupply network requirements"""
        networks = {
            "calculation_date": datetime.now().isoformat(),
            "local_sources": {},
            "regional_sources": {},
            "community_networks": {},
            "alternative_suppliers": {},
            "risk_assessment": {}
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Local sources (within 25 miles)
        local_categories = {
            "food": {
                "farmers_markets": {"reliability": 8, "seasonal": True, "cost_factor": 1.2},
                "local_farms": {"reliability": 9, "seasonal": True, "cost_factor": 1.0},
                "community_gardens": {"reliability": 6, "seasonal": True, "cost_factor": 0.5},
                "food_co_ops": {"reliability": 7, "seasonal": False, "cost_factor": 0.9}
            },
            "water": {
                "local_wells": {"reliability": 9, "seasonal": False, "cost_factor": 0.1},
                "natural_springs": {"reliability": 8, "seasonal": False, "cost_factor": 0.0},
                "rainwater_collection": {"reliability": 6, "seasonal": True, "cost_factor": 0.0}
            },
            "energy": {
                "local_solar_installers": {"reliability": 8, "seasonal": False, "cost_factor": 1.0},
                "firewood_suppliers": {"reliability": 9, "seasonal": True, "cost_factor": 1.0},
                "used_equipment_dealers": {"reliability": 6, "seasonal": False, "cost_factor": 0.7}
            },
            "medical": {
                "local_pharmacy": {"reliability": 9, "seasonal": False, "cost_factor": 1.0},
                "veterinary_supplies": {"reliability": 7, "seasonal": False, "cost_factor": 0.8},
                "herb_growers": {"reliability": 5, "seasonal": True, "cost_factor": 0.6}
            }
        }
        
        for category, sources in local_categories.items():
            networks["local_sources"][category] = {}
            for source, data in sources.items():
                networks["local_sources"][category][source] = {
                    "reliability_score": data["reliability"],
                    "seasonal_availability": data["seasonal"],
                    "cost_factor": data["cost_factor"],
                    "risk_level": self._assess_source_risk(source, "local")
                }
        
        # Community networks
        network_types = [
            {
                "type": "neighborhood_cooperative",
                "members": 12,
                "resources": ["bulk_buying", "tool_sharing", "skill_exchange"],
                "coordination": "monthly_meetings",
                "trust_level": 8,
                "geographic_range": "2_mile_radius"
            },
            {
                "type": "prepper_group",
                "members": 25,
                "resources": ["knowledge_sharing", "group_purchases", "mutual_aid"],
                "coordination": "online_forum",
                "trust_level": 7,
                "geographic_range": "county_wide"
            },
            {
                "type": "religious_community",
                "members": 150,
                "resources": ["food_bank", "volunteer_labor", "financial_assistance"],
                "coordination": "weekly_services",
                "trust_level": 9,
                "geographic_range": "local_area"
            },
            {
                "type": "professional_network",
                "members": 40,
                "resources": ["specialized_skills", "equipment_access", "connections"],
                "coordination": "professional_meetings",
                "trust_level": 6,
                "geographic_range": "regional"
            }
        ]
        
        for network in network_types:
            # Store in database
            cursor.execute('''
                INSERT OR REPLACE INTO resource_networks
                (network_type, network_name, member_count, resource_categories,
                 coordination_method, trust_level, geographic_range)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (network["type"], network["type"].replace("_", " ").title(),
                  network["members"], json.dumps(network["resources"]),
                  network["coordination"], network["trust_level"],
                  network["geographic_range"]))
            
            networks["community_networks"][network["type"]] = {
                "member_count": network["members"],
                "available_resources": network["resources"],
                "reliability": network["trust_level"],
                "activation_method": network["coordination"]
            }
        
        conn.commit()
        conn.close()
        
        # Risk assessment
        networks["risk_assessment"] = {
            "single_point_failures": self._identify_single_points(networks),
            "seasonal_vulnerabilities": self._assess_seasonal_risks(networks),
            "distance_dependencies": self._assess_distance_risks(networks),
            "economic_vulnerabilities": self._assess_economic_risks(networks),
            "mitigation_strategies": self._generate_mitigation_strategies(networks)
        }
        
        return networks
    
    def generate_long_term_report(self, family_size: int = 4, duration_months: int = 12) -> Dict:
        """Generate comprehensive long-term sustainability report"""
        report = {
            "report_date": datetime.now().isoformat(),
            "module_version": "2.0.0",
            "family_size": family_size,
            "planning_duration": duration_months,
            "sections": {}
        }
        
        # Extended supply planning
        report["sections"]["supply_planning"] = self.calculate_extended_supplies(family_size, duration_months, "general")
        
        # Seasonal planning
        report["sections"]["seasonal_planning"] = self.create_seasonal_plan(duration_months)
        
        # Storage system design
        total_volume = report["sections"]["supply_planning"]["storage_requirements"]["total_cubic_feet"]
        report["sections"]["storage_system"] = self.design_storage_system(total_volume, 2000)
        
        # Resupply networks
        report["sections"]["resupply_networks"] = self.calculate_resupply_networks(
            report["sections"]["supply_planning"]["supply_categories"])
        
        # Overall sustainability score
        sustainability_factors = {
            "supply_adequacy": min(100, (duration_months / 12) * 100),
            "storage_efficiency": report["sections"]["storage_system"]["optimization_score"],
            "seasonal_adaptation": 85,  # Based on planning completeness
            "network_resilience": self._calculate_network_score(report["sections"]["resupply_networks"]),
            "cost_efficiency": max(0, 100 - (report["sections"]["supply_planning"]["total_cost"] / (family_size * 1000)))
        }
        
        report["overall_sustainability_score"] = sum(sustainability_factors.values()) / len(sustainability_factors)
        report["sustainability_level"] = self._get_sustainability_level(report["overall_sustainability_score"])
        report["sustainability_factors"] = sustainability_factors
        
        return report
    
    # Helper methods
    def _get_optimal_storage(self, item_type: str) -> str:
        """Get optimal storage method for item type"""
        storage_map = {
            "grains": "mylar_bags",
            "proteins": "mylar_bags", 
            "fats": "sealed_containers",
            "vegetables": "canned",
            "fruits": "dehydrated",
            "dairy": "powdered",
            "seasonings": "mason_jars"
        }
        return storage_map.get(item_type, "standard")
    
    def _get_shelf_life(self, item_type: str) -> int:
        """Get shelf life in months for item type"""
        shelf_life_map = {
            "grains": 300,  # 25 years in mylar
            "proteins": 240, # 20 years
            "fats": 60,     # 5 years
            "vegetables": 36, # 3 years canned
            "fruits": 24,   # 2 years dried
            "dairy": 24,    # 2 years powdered
            "seasonings": 60 # 5 years
        }
        return shelf_life_map.get(item_type, 24)
    
    def _get_season(self, month: int) -> str:
        """Get season for given month"""
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "fall"
        else:
            return "winter"
    
    def _get_heating_factor(self, month: int) -> float:
        """Get heating factor for month"""
        heating_months = {1: 1.5, 2: 1.4, 3: 1.1, 4: 0.8, 5: 0.5,
                         6: 0.2, 7: 0.1, 8: 0.1, 9: 0.3, 10: 0.7,
                         11: 1.2, 12: 1.4}
        return heating_months.get(month, 1.0)
    
    def _get_cooling_factor(self, month: int) -> float:
        """Get cooling factor for month"""
        cooling_months = {1: 0.1, 2: 0.1, 3: 0.2, 4: 0.5, 5: 0.8,
                         6: 1.3, 7: 1.5, 8: 1.4, 9: 1.0, 10: 0.6,
                         11: 0.3, 12: 0.1}
        return cooling_months.get(month, 1.0)
    
    def _calculate_procurement_priority(self, category: str, item: str, 
                                      shelf_life: int, cost: float) -> int:
        """Calculate procurement priority score (1-10)"""
        priority = 5  # Base priority
        
        # Category weights
        if category in ["medical", "water"]:
            priority += 3
        elif category in ["food", "energy"]:
            priority += 2
        elif category in ["tools", "fuel"]:
            priority += 1
        
        # Shelf life adjustments
        if shelf_life < 6:
            priority += 2
        elif shelf_life < 12:
            priority += 1
        elif shelf_life > 120:
            priority -= 1
        
        # Cost considerations
        if cost > 1000:
            priority -= 1
        elif cost < 100:
            priority += 1
        
        return max(1, min(10, priority))
    
    def _get_sustainability_level(self, score: float) -> str:
        """Determine sustainability level from score"""
        if score >= 85:
            return "EXCELLENT - Comprehensive long-term sustainability"
        elif score >= 70:
            return "GOOD - Strong long-term preparedness"
        elif score >= 55:
            return "MODERATE - Basic long-term planning"
        elif score >= 40:
            return "POOR - Insufficient long-term preparation"
        else:
            return "CRITICAL - No meaningful long-term sustainability"


def main():
    """Test the Extended Supply Planning Module"""
    print("📦 EXTENDED SUPPLY PLANNING MODULE v2.0")
    print("=" * 50)
    
    # Initialize module
    supply_module = ExtendedSupplyPlanningModule()
    
    # Calculate extended supplies
    print("\n📊 Calculating Extended Supply Requirements...")
    supplies = supply_module.calculate_extended_supplies(4, 6, "general")
    print(f"Total Cost: ${supplies['total_cost']:,.2f}")
    print(f"Storage Required: {supplies['storage_requirements']['total_cubic_feet']:.1f} cubic feet")
    print(f"Self-Sufficiency: {supplies['sustainability_metrics']['self_sufficiency_months']} months")
    
    # Create seasonal plan
    print("\n📅 Creating Seasonal Plan...")
    seasonal = supply_module.create_seasonal_plan(12)
    print(f"Seasonal cycles planned: {len(seasonal['seasonal_cycles'])}")
    print(f"Growing seasons: {len(seasonal['growing_seasons'])}")
    
    # Design storage system
    print("\n🏠 Designing Storage System...")
    storage = supply_module.design_storage_system(supplies['storage_requirements']['total_cubic_feet'], 2000)
    print(f"Storage solutions: {len(storage['storage_solutions'])}")
    print(f"Optimization score: {storage['optimization_score']:.1f}%")
    print(f"Total cost: ${storage['total_cost']:,.2f}")
    
    # Calculate resupply networks
    print("\n🌐 Planning Resupply Networks...")
    networks = supply_module.calculate_resupply_networks(supplies['supply_categories'])
    print(f"Local sources: {len(networks['local_sources'])}")
    print(f"Community networks: {len(networks['community_networks'])}")
    
    # Generate comprehensive report
    print("\n📋 Generating Long-term Sustainability Report...")
    report = supply_module.generate_long_term_report(4, 12)
    print(f"Overall Sustainability Score: {report['overall_sustainability_score']:.1f}%")
    print(f"Level: {report['sustainability_level']}")
    
    print("\n✅ Extended Supply Planning Module initialized successfully!")
    print("Ready to improve long-term scenario planning from 51% to 70%+")


if __name__ == "__main__":
    main()
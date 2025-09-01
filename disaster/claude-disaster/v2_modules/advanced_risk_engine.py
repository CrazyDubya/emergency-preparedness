#!/usr/bin/env python3
"""
Advanced Risk Calculation Engine - Version 3.0
Multi-factor risk scoring with real-time adjustments and historical data integration
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import math
import random
from pathlib import Path

class AdvancedRiskEngine:
    """
    Sophisticated risk assessment system with multi-factor analysis,
    historical data integration, and real-time risk adjustments.
    """
    
    def __init__(self, db_path: str = "risk_engine.db"):
        """Initialize the Advanced Risk Calculation Engine"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_database()
        self._load_historical_data()
        self._initialize_risk_factors()
        
    def _initialize_database(self):
        """Create database tables for risk assessment data"""
        
        # Historical disaster data table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_disasters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disaster_type TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT,
                severity INTEGER,
                casualties INTEGER,
                economic_impact REAL,
                duration_hours INTEGER,
                warning_time_hours INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Risk profiles table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_name TEXT UNIQUE NOT NULL,
                base_probability REAL,
                impact_severity INTEGER,
                warning_time_avg INTEGER,
                seasonal_factors TEXT,
                regional_factors TEXT,
                cascading_risks TEXT,
                mitigation_factors TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Location risk factors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS location_risks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                disaster_type TEXT NOT NULL,
                risk_multiplier REAL,
                historical_frequency REAL,
                last_occurrence TEXT,
                infrastructure_vulnerability REAL,
                population_density REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Real-time conditions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS realtime_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition_type TEXT NOT NULL,
                current_value REAL,
                risk_impact REAL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _load_historical_data(self):
        """Load historical disaster patterns and statistics"""
        
        # Sample historical data for common disasters
        historical_patterns = [
            # Earthquakes
            ("earthquake", "2024-01-15", "California", 6.2, 0, 500000, 1, 0),
            ("earthquake", "2023-09-08", "Morocco", 6.8, 2900, 7000000, 2, 0),
            ("earthquake", "2023-02-06", "Turkey", 7.8, 50000, 84000000, 48, 0),
            
            # Hurricanes
            ("hurricane", "2024-07-08", "Texas", 2, 0, 14000000, 72, 120),
            ("hurricane", "2023-08-30", "Florida", 3, 4, 50000000, 96, 96),
            ("hurricane", "2022-09-28", "Florida", 4, 150, 113000000, 120, 72),
            
            # Wildfires
            ("wildfire", "2024-08-01", "California", 7, 0, 2000000, 240, 12),
            ("wildfire", "2023-08-08", "Hawaii", 9, 100, 5500000, 168, 2),
            
            # Floods
            ("flood", "2024-05-15", "Texas", 6, 5, 1000000, 48, 6),
            ("flood", "2023-07-16", "Vermont", 7, 2, 2100000, 72, 12),
            
            # Power outages
            ("power_outage", "2024-02-13", "Multi-State", 5, 0, 500000, 96, 1),
            ("power_outage", "2023-12-18", "Northeast", 6, 0, 1000000, 72, 2),
            
            # Cyber attacks
            ("cyber_attack", "2024-03-22", "National", 7, 0, 10000000, 168, 0),
            ("cyber_attack", "2023-11-08", "Healthcare", 8, 0, 25000000, 336, 0),
        ]
        
        for pattern in historical_patterns:
            self.cursor.execute('''
                INSERT OR IGNORE INTO historical_disasters 
                (disaster_type, date, location, severity, casualties, economic_impact, 
                 duration_hours, warning_time_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', pattern)
        
        self.conn.commit()
    
    def _initialize_risk_factors(self):
        """Initialize comprehensive risk factors for various scenarios"""
        
        self.risk_factors = {
            "time_of_day": {
                "night": 1.3,      # Higher risk at night
                "early_morning": 1.1,
                "morning": 0.9,
                "afternoon": 0.95,
                "evening": 1.05
            },
            "season": {
                "winter": {"blizzard": 2.0, "ice_storm": 2.5, "heating_failure": 1.8},
                "spring": {"tornado": 2.2, "flood": 1.8, "severe_storm": 1.6},
                "summer": {"hurricane": 2.0, "wildfire": 2.5, "heat_wave": 2.2},
                "fall": {"hurricane": 1.5, "wildfire": 1.8, "early_winter_storm": 1.3}
            },
            "infrastructure_age": {
                "new": 0.7,        # <5 years
                "moderate": 1.0,   # 5-20 years
                "aging": 1.3,      # 20-40 years
                "critical": 1.8    # 40+ years
            },
            "population_density": {
                "rural": 0.8,
                "suburban": 1.0,
                "urban": 1.3,
                "metropolitan": 1.5
            },
            "preparedness_level": {
                "none": 1.5,
                "basic": 1.2,
                "moderate": 1.0,
                "advanced": 0.7,
                "expert": 0.5
            }
        }
    
    def calculate_comprehensive_risk(self, scenario: Dict[str, Any], 
                                    location: str = "suburban",
                                    current_conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive risk assessment for a given scenario
        
        Args:
            scenario: Disaster scenario dictionary
            location: Location type (urban, suburban, rural)
            current_conditions: Current environmental conditions
            
        Returns:
            Comprehensive risk assessment with scores and recommendations
        """
        
        risk_assessment = {
            "scenario": scenario.get("name", "Unknown"),
            "timestamp": datetime.now().isoformat(),
            "base_risk_score": 0,
            "adjusted_risk_score": 0,
            "probability": 0,
            "impact_severity": 0,
            "time_to_impact": None,
            "confidence_level": 0,
            "risk_factors": {},
            "mitigation_available": [],
            "action_priority": "",
            "detailed_analysis": {}
        }
        
        # Step 1: Calculate base risk from historical data
        base_risk = self._calculate_base_risk(scenario)
        risk_assessment["base_risk_score"] = base_risk
        
        # Step 2: Apply location-based modifiers
        location_modifier = self._calculate_location_risk(scenario, location)
        
        # Step 3: Apply temporal factors
        temporal_modifier = self._calculate_temporal_risk(scenario)
        
        # Step 4: Apply current condition modifiers
        condition_modifier = 1.0
        if current_conditions:
            condition_modifier = self._calculate_condition_risk(scenario, current_conditions)
        
        # Step 5: Calculate probability based on multiple factors
        probability = self._calculate_probability(scenario, location, current_conditions)
        risk_assessment["probability"] = probability
        
        # Step 6: Assess impact severity
        impact = self._assess_impact_severity(scenario)
        risk_assessment["impact_severity"] = impact
        
        # Step 7: Calculate adjusted risk score
        adjusted_risk = base_risk * location_modifier * temporal_modifier * condition_modifier
        adjusted_risk = min(100, adjusted_risk)  # Cap at 100
        risk_assessment["adjusted_risk_score"] = round(adjusted_risk, 1)
        
        # Step 8: Determine time to impact
        risk_assessment["time_to_impact"] = self._estimate_time_to_impact(scenario, current_conditions)
        
        # Step 9: Calculate confidence level
        risk_assessment["confidence_level"] = self._calculate_confidence(scenario)
        
        # Step 10: Identify risk factors
        risk_assessment["risk_factors"] = {
            "location": location_modifier,
            "temporal": temporal_modifier,
            "conditions": condition_modifier,
            "historical_frequency": self._get_historical_frequency(scenario),
            "cascading_potential": self._assess_cascading_risks(scenario)
        }
        
        # Step 11: Identify available mitigations
        risk_assessment["mitigation_available"] = self._identify_mitigations(scenario, adjusted_risk)
        
        # Step 12: Set action priority
        risk_assessment["action_priority"] = self._determine_action_priority(
            adjusted_risk, 
            probability, 
            risk_assessment["time_to_impact"]
        )
        
        # Step 13: Provide detailed analysis
        risk_assessment["detailed_analysis"] = self._generate_detailed_analysis(
            scenario, 
            risk_assessment
        )
        
        return risk_assessment
    
    def _calculate_base_risk(self, scenario: Dict[str, Any]) -> float:
        """Calculate base risk score from historical data"""
        
        disaster_type = scenario.get("type", "unknown")
        severity = scenario.get("severity", 5)
        
        # Query historical data for similar disasters
        self.cursor.execute('''
            SELECT AVG(severity), AVG(casualties), AVG(economic_impact),
                   COUNT(*), AVG(duration_hours)
            FROM historical_disasters
            WHERE disaster_type = ?
        ''', (disaster_type,))
        
        result = self.cursor.fetchone()
        
        if result and result[0]:
            avg_severity, avg_casualties, avg_impact, frequency, avg_duration = result
            
            # Calculate base risk using weighted factors
            severity_weight = (severity / 10) * 30  # 30% weight
            historical_weight = (avg_severity / 10) * 20 if avg_severity else 10  # 20% weight
            frequency_weight = min(30, frequency * 3)  # 30% weight, max 30
            duration_weight = min(20, avg_duration / 24 * 5) if avg_duration else 10  # 20% weight
            
            base_risk = severity_weight + historical_weight + frequency_weight + duration_weight
        else:
            # No historical data, use scenario severity
            base_risk = severity * 10
        
        return min(100, base_risk)
    
    def _calculate_location_risk(self, scenario: Dict[str, Any], location: str) -> float:
        """Calculate location-based risk modifier"""
        
        disaster_type = scenario.get("type", "unknown")
        
        # Location-specific risk modifiers
        location_risks = {
            "earthquake": {"urban": 1.5, "suburban": 1.2, "rural": 0.8},
            "hurricane": {"coastal": 2.0, "inland": 0.5, "urban": 1.3},
            "wildfire": {"rural": 1.8, "suburban": 1.5, "urban": 0.7},
            "flood": {"riverside": 2.0, "coastal": 1.8, "urban": 1.2},
            "tornado": {"rural": 1.5, "suburban": 1.3, "urban": 1.0},
            "cyber_attack": {"urban": 1.5, "suburban": 1.2, "rural": 0.9},
            "power_outage": {"rural": 1.3, "suburban": 1.0, "urban": 0.9}
        }
        
        if disaster_type in location_risks:
            return location_risks[disaster_type].get(location, 1.0)
        
        # Default location modifiers
        return self.risk_factors["population_density"].get(location, 1.0)
    
    def _calculate_temporal_risk(self, scenario: Dict[str, Any]) -> float:
        """Calculate time-based risk modifiers"""
        
        current_hour = datetime.now().hour
        current_month = datetime.now().month
        
        # Time of day modifier
        if 0 <= current_hour < 6:
            time_modifier = self.risk_factors["time_of_day"]["night"]
        elif 6 <= current_hour < 9:
            time_modifier = self.risk_factors["time_of_day"]["early_morning"]
        elif 9 <= current_hour < 12:
            time_modifier = self.risk_factors["time_of_day"]["morning"]
        elif 12 <= current_hour < 17:
            time_modifier = self.risk_factors["time_of_day"]["afternoon"]
        else:
            time_modifier = self.risk_factors["time_of_day"]["evening"]
        
        # Seasonal modifier
        if current_month in [12, 1, 2]:
            season = "winter"
        elif current_month in [3, 4, 5]:
            season = "spring"
        elif current_month in [6, 7, 8]:
            season = "summer"
        else:
            season = "fall"
        
        disaster_type = scenario.get("type", "unknown")
        seasonal_modifier = 1.0
        
        if season in self.risk_factors["season"]:
            season_risks = self.risk_factors["season"][season]
            for risk_type, multiplier in season_risks.items():
                if risk_type in disaster_type.lower():
                    seasonal_modifier = multiplier
                    break
        
        return (time_modifier + seasonal_modifier) / 2
    
    def _calculate_condition_risk(self, scenario: Dict[str, Any], 
                                 conditions: Dict[str, Any]) -> float:
        """Calculate risk modifier based on current conditions"""
        
        disaster_type = scenario.get("type", "unknown")
        modifier = 1.0
        
        # Weather-related conditions
        if "temperature" in conditions:
            temp = conditions["temperature"]
            if disaster_type == "wildfire" and temp > 95:
                modifier *= 1.5
            elif disaster_type == "ice_storm" and temp < 32:
                modifier *= 1.8
        
        if "humidity" in conditions:
            humidity = conditions["humidity"]
            if disaster_type == "wildfire" and humidity < 20:
                modifier *= 1.4
        
        if "wind_speed" in conditions:
            wind = conditions["wind_speed"]
            if disaster_type in ["hurricane", "tornado"] and wind > 40:
                modifier *= 1.6
            elif disaster_type == "wildfire" and wind > 25:
                modifier *= 1.5
        
        # Infrastructure conditions
        if "power_grid_stress" in conditions:
            if disaster_type == "power_outage" and conditions["power_grid_stress"] > 80:
                modifier *= 2.0
        
        if "cyber_threat_level" in conditions:
            if disaster_type == "cyber_attack" and conditions["cyber_threat_level"] > 7:
                modifier *= 1.8
        
        return modifier
    
    def _calculate_probability(self, scenario: Dict[str, Any], 
                              location: str, conditions: Dict[str, Any]) -> float:
        """Calculate probability of scenario occurring"""
        
        disaster_type = scenario.get("type", "unknown")
        
        # Base probabilities (annual percentage chance)
        base_probabilities = {
            "earthquake": 2.0,
            "hurricane": 5.0,
            "wildfire": 3.0,
            "flood": 10.0,
            "tornado": 2.5,
            "power_outage": 15.0,
            "cyber_attack": 8.0,
            "pandemic": 1.0,
            "nuclear_accident": 0.1,
            "terrorism": 0.5
        }
        
        base_prob = base_probabilities.get(disaster_type, 1.0)
        
        # Adjust for location
        location_adjustment = self._calculate_location_risk(scenario, location)
        
        # Adjust for current conditions
        condition_adjustment = 1.0
        if conditions:
            condition_adjustment = self._calculate_condition_risk(scenario, conditions)
        
        # Calculate final probability (capped at 95%)
        final_probability = min(95, base_prob * location_adjustment * condition_adjustment)
        
        return round(final_probability, 1)
    
    def _assess_impact_severity(self, scenario: Dict[str, Any]) -> int:
        """Assess potential impact severity (1-10 scale)"""
        
        base_severity = scenario.get("severity", 5)
        cascading_effects = scenario.get("cascading_effects", [])
        affected_area = scenario.get("affected_area", "local")
        
        # Adjust for cascading effects
        severity = base_severity + (len(cascading_effects) * 0.3)
        
        # Adjust for affected area
        area_multipliers = {
            "single_building": 0.7,
            "neighborhood": 0.9,
            "local": 1.0,
            "city_wide": 1.2,
            "regional": 1.4,
            "multi_state": 1.6,
            "national": 1.8,
            "global": 2.0
        }
        
        severity *= area_multipliers.get(affected_area, 1.0)
        
        return min(10, round(severity))
    
    def _estimate_time_to_impact(self, scenario: Dict[str, Any], 
                                conditions: Dict[str, Any]) -> Optional[str]:
        """Estimate time until potential impact"""
        
        warning_time = scenario.get("warning_time", 0)  # in hours
        
        if warning_time == 0:
            return "Immediate"
        elif warning_time < 1:
            return f"{int(warning_time * 60)} minutes"
        elif warning_time < 24:
            return f"{warning_time} hours"
        elif warning_time < 168:
            return f"{warning_time // 24} days"
        else:
            return f"{warning_time // 168} weeks"
    
    def _calculate_confidence(self, scenario: Dict[str, Any]) -> float:
        """Calculate confidence level in the risk assessment"""
        
        disaster_type = scenario.get("type", "unknown")
        
        # Check historical data availability
        self.cursor.execute('''
            SELECT COUNT(*) FROM historical_disasters
            WHERE disaster_type = ?
        ''', (disaster_type,))
        
        data_points = self.cursor.fetchone()[0]
        
        # Base confidence on data availability
        if data_points >= 10:
            confidence = 90
        elif data_points >= 5:
            confidence = 75
        elif data_points >= 2:
            confidence = 60
        else:
            confidence = 40
        
        # Adjust for scenario specificity
        if scenario.get("severity") and scenario.get("duration"):
            confidence += 5
        if scenario.get("cascading_effects"):
            confidence += 5
        
        return min(95, confidence)
    
    def _get_historical_frequency(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Get historical frequency data for the scenario"""
        
        disaster_type = scenario.get("type", "unknown")
        
        self.cursor.execute('''
            SELECT COUNT(*), 
                   AVG(JULIANDAY('now') - JULIANDAY(date)) as avg_days_ago,
                   MIN(JULIANDAY('now') - JULIANDAY(date)) as last_occurrence
            FROM historical_disasters
            WHERE disaster_type = ?
        ''', (disaster_type,))
        
        result = self.cursor.fetchone()
        
        if result and result[0]:
            count, avg_days, last_days = result
            return {
                "total_occurrences": count,
                "average_interval_days": round(avg_days / count) if count > 1 else None,
                "days_since_last": round(last_days) if last_days else None,
                "annual_frequency": round((count / (avg_days / 365)), 2) if avg_days else 0
            }
        
        return {
            "total_occurrences": 0,
            "average_interval_days": None,
            "days_since_last": None,
            "annual_frequency": 0
        }
    
    def _assess_cascading_risks(self, scenario: Dict[str, Any]) -> Dict[str, float]:
        """Assess potential cascading risks from the scenario"""
        
        cascading_effects = scenario.get("cascading_effects", [])
        disaster_type = scenario.get("type", "unknown")
        
        # Cascading risk probabilities
        cascade_probabilities = {
            "power_outage": {
                "food_spoilage": 0.8,
                "water_system_failure": 0.6,
                "communication_loss": 0.7,
                "heating_cooling_loss": 0.9,
                "medical_equipment_failure": 0.5
            },
            "flood": {
                "water_contamination": 0.9,
                "sewage_backup": 0.7,
                "mold_growth": 0.8,
                "structural_damage": 0.6,
                "disease_outbreak": 0.3
            },
            "earthquake": {
                "gas_leak": 0.4,
                "fire": 0.3,
                "tsunami": 0.2,
                "landslide": 0.3,
                "dam_failure": 0.1
            },
            "cyber_attack": {
                "financial_system_failure": 0.7,
                "supply_chain_disruption": 0.8,
                "identity_theft": 0.6,
                "critical_infrastructure_failure": 0.5
            }
        }
        
        cascading_risks = {}
        
        # Get primary cascading risks
        if disaster_type in cascade_probabilities:
            cascading_risks.update(cascade_probabilities[disaster_type])
        
        # Add scenario-specific cascading effects
        for effect in cascading_effects:
            if effect not in cascading_risks:
                cascading_risks[effect] = 0.5  # Default 50% probability
        
        return cascading_risks
    
    def _identify_mitigations(self, scenario: Dict[str, Any], risk_score: float) -> List[str]:
        """Identify available mitigation strategies"""
        
        disaster_type = scenario.get("type", "unknown")
        mitigations = []
        
        # Universal mitigations
        if risk_score > 30:
            mitigations.extend([
                "Review and update emergency contacts",
                "Check emergency supply levels",
                "Review evacuation routes"
            ])
        
        # Disaster-specific mitigations
        mitigation_strategies = {
            "earthquake": [
                "Secure heavy furniture and appliances",
                "Practice drop, cover, and hold drills",
                "Store emergency supplies in multiple locations",
                "Identify safe spots in each room"
            ],
            "hurricane": [
                "Board up windows and doors",
                "Fill bathtubs with water",
                "Charge all electronic devices",
                "Move to interior rooms away from windows"
            ],
            "wildfire": [
                "Create defensible space around property",
                "Prepare go-bags for rapid evacuation",
                "Close all windows and vents",
                "Have N95 masks ready"
            ],
            "flood": [
                "Move valuables to upper floors",
                "Sandbag potential water entry points",
                "Turn off utilities if instructed",
                "Document belongings for insurance"
            ],
            "power_outage": [
                "Start generator if available",
                "Unplug sensitive electronics",
                "Keep refrigerator/freezer closed",
                "Use battery-powered lighting"
            ],
            "cyber_attack": [
                "Disconnect from internet if suspicious activity",
                "Use offline backups",
                "Monitor financial accounts",
                "Change passwords on critical accounts"
            ]
        }
        
        if disaster_type in mitigation_strategies:
            # Select top mitigations based on risk score
            available = mitigation_strategies[disaster_type]
            num_mitigations = min(len(available), max(2, int(risk_score / 20)))
            mitigations.extend(available[:num_mitigations])
        
        return mitigations
    
    def _determine_action_priority(self, risk_score: float, probability: float, 
                                  time_to_impact: str) -> str:
        """Determine action priority level"""
        
        # Calculate urgency score
        urgency = risk_score * (probability / 100)
        
        # Adjust for time to impact
        if time_to_impact == "Immediate":
            urgency *= 2
        elif "minutes" in str(time_to_impact):
            urgency *= 1.8
        elif "hours" in str(time_to_impact):
            urgency *= 1.5
        elif "days" in str(time_to_impact):
            urgency *= 1.2
        
        # Determine priority level
        if urgency >= 80:
            return "CRITICAL - Immediate action required"
        elif urgency >= 60:
            return "HIGH - Begin preparations immediately"
        elif urgency >= 40:
            return "MODERATE - Monitor and prepare"
        elif urgency >= 20:
            return "LOW - Review preparedness plans"
        else:
            return "MINIMAL - Maintain awareness"
    
    def _generate_detailed_analysis(self, scenario: Dict[str, Any], 
                                   assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed risk analysis and recommendations"""
        
        analysis = {
            "risk_summary": "",
            "key_vulnerabilities": [],
            "strength_areas": [],
            "critical_actions": [],
            "timeline": "",
            "resource_requirements": [],
            "success_factors": []
        }
        
        # Risk summary
        risk_level = "extreme" if assessment["adjusted_risk_score"] > 80 else \
                    "high" if assessment["adjusted_risk_score"] > 60 else \
                    "moderate" if assessment["adjusted_risk_score"] > 40 else "low"
        
        analysis["risk_summary"] = (
            f"The {scenario.get('name', 'scenario')} presents a {risk_level} risk "
            f"with a {assessment['probability']}% probability of occurrence. "
            f"Impact severity is estimated at {assessment['impact_severity']}/10."
        )
        
        # Identify vulnerabilities
        if assessment["risk_factors"]["location"] > 1.2:
            analysis["key_vulnerabilities"].append("Location increases risk exposure")
        if assessment["risk_factors"]["temporal"] > 1.2:
            analysis["key_vulnerabilities"].append("Current time period elevates risk")
        if assessment["risk_factors"]["cascading_potential"]:
            high_cascade = [k for k, v in assessment["risk_factors"]["cascading_potential"].items() if v > 0.7]
            if high_cascade:
                analysis["key_vulnerabilities"].append(f"High cascading risk: {', '.join(high_cascade)}")
        
        # Identify strengths
        if assessment["confidence_level"] > 75:
            analysis["strength_areas"].append("High confidence in assessment accuracy")
        if len(assessment["mitigation_available"]) > 3:
            analysis["strength_areas"].append("Multiple mitigation strategies available")
        if assessment["time_to_impact"] and "days" in assessment["time_to_impact"]:
            analysis["strength_areas"].append("Adequate warning time for preparation")
        
        # Critical actions based on priority
        if "CRITICAL" in assessment["action_priority"]:
            analysis["critical_actions"] = [
                "Activate emergency response plan immediately",
                "Notify all family members",
                "Implement highest priority mitigations",
                "Prepare for immediate evacuation if needed"
            ]
        elif "HIGH" in assessment["action_priority"]:
            analysis["critical_actions"] = [
                "Begin active preparations",
                "Review and test emergency systems",
                "Stock additional supplies",
                "Confirm evacuation routes"
            ]
        else:
            analysis["critical_actions"] = [
                "Monitor situation closely",
                "Review emergency plans",
                "Check supply levels",
                "Update emergency contacts"
            ]
        
        # Timeline
        analysis["timeline"] = f"Estimated time to impact: {assessment['time_to_impact']}"
        
        # Resource requirements
        analysis["resource_requirements"] = self._identify_resource_needs(scenario)
        
        # Success factors
        analysis["success_factors"] = [
            "Early warning system activation",
            "Family communication plan execution",
            "Pre-positioned emergency supplies",
            "Practiced response procedures"
        ]
        
        return analysis
    
    def _identify_resource_needs(self, scenario: Dict[str, Any]) -> List[str]:
        """Identify resource requirements for scenario response"""
        
        disaster_type = scenario.get("type", "unknown")
        duration = scenario.get("duration", "hours")
        
        resources = []
        
        # Basic resources for all scenarios
        resources.extend([
            "Water (1 gallon/person/day)",
            "Non-perishable food",
            "First aid supplies",
            "Flashlights and batteries",
            "Battery-powered radio"
        ])
        
        # Duration-specific resources
        if duration in ["weeks", "months"]:
            resources.extend([
                "Extended food supplies (2+ weeks)",
                "Alternative cooking methods",
                "Prescription medication reserves",
                "Cash reserves",
                "Fuel reserves"
            ])
        
        # Disaster-specific resources
        specific_resources = {
            "earthquake": ["Sturdy shoes", "Work gloves", "Dust masks", "Crowbar"],
            "hurricane": ["Plywood/boards", "Plastic sheeting", "Duct tape", "Sandbags"],
            "wildfire": ["N95 masks", "Fire extinguisher", "Evacuation bags", "Important documents"],
            "flood": ["Waterproof containers", "Bleach for sanitizing", "Rubber boots", "Sump pump"],
            "power_outage": ["Generator", "Solar chargers", "Coolers with ice", "Manual can opener"],
            "cyber_attack": ["Offline backups", "Cash", "Paper records", "Alternative communication"],
            "pandemic": ["Face masks", "Hand sanitizer", "Disinfectants", "Thermometer", "Medications"]
        }
        
        if disaster_type in specific_resources:
            resources.extend(specific_resources[disaster_type])
        
        return resources[:10]  # Return top 10 most relevant resources
    
    def create_scenario_risk_profile(self, scenario_name: str, 
                                    disaster_type: str,
                                    severity: int = 5,
                                    warning_time: int = 24,
                                    **kwargs) -> bool:
        """
        Create a detailed risk profile for a specific scenario
        
        Args:
            scenario_name: Name of the scenario
            disaster_type: Type of disaster
            severity: Severity level (1-10)
            warning_time: Average warning time in hours
            **kwargs: Additional scenario-specific parameters
            
        Returns:
            Success status
        """
        
        try:
            # Calculate base probability from historical data
            self.cursor.execute('''
                SELECT COUNT(*), AVG(severity) 
                FROM historical_disasters
                WHERE disaster_type = ?
            ''', (disaster_type,))
            
            result = self.cursor.fetchone()
            base_probability = 5.0  # Default
            
            if result and result[0]:
                count, avg_severity = result
                # Higher frequency = higher probability
                base_probability = min(30, count * 2.5)
            
            # Prepare profile data
            profile_data = {
                "scenario_name": scenario_name,
                "base_probability": base_probability,
                "impact_severity": severity,
                "warning_time_avg": warning_time,
                "seasonal_factors": json.dumps(kwargs.get("seasonal_factors", {})),
                "regional_factors": json.dumps(kwargs.get("regional_factors", {})),
                "cascading_risks": json.dumps(kwargs.get("cascading_risks", [])),
                "mitigation_factors": json.dumps(kwargs.get("mitigation_factors", []))
            }
            
            # Insert or update profile
            self.cursor.execute('''
                INSERT OR REPLACE INTO risk_profiles
                (scenario_name, base_probability, impact_severity, warning_time_avg,
                 seasonal_factors, regional_factors, cascading_risks, mitigation_factors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(profile_data.values()))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error creating risk profile: {e}")
            return False
    
    def get_real_time_risk_update(self, location: str = "suburban") -> Dict[str, Any]:
        """
        Get real-time risk assessment for current conditions
        
        Returns:
            Current risk levels for various disaster types
        """
        
        current_risks = {
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "risk_levels": {},
            "active_warnings": [],
            "recommended_actions": []
        }
        
        # Check each disaster type
        disaster_types = [
            "earthquake", "hurricane", "wildfire", "flood", "tornado",
            "power_outage", "cyber_attack", "pandemic"
        ]
        
        for disaster_type in disaster_types:
            # Create scenario for assessment
            scenario = {
                "name": f"Potential {disaster_type}",
                "type": disaster_type,
                "severity": 5,  # Default medium severity
                "duration": "hours",
                "warning_time": 24,
                "cascading_effects": [],
                "affected_area": "local"
            }
            
            # Get current conditions (simulated for now)
            current_conditions = self._simulate_current_conditions()
            
            # Calculate risk
            risk_assessment = self.calculate_comprehensive_risk(
                scenario, 
                location, 
                current_conditions
            )
            
            current_risks["risk_levels"][disaster_type] = {
                "risk_score": risk_assessment["adjusted_risk_score"],
                "probability": risk_assessment["probability"],
                "priority": risk_assessment["action_priority"]
            }
            
            # Add warnings for high-risk scenarios
            if risk_assessment["adjusted_risk_score"] > 60:
                current_risks["active_warnings"].append({
                    "type": disaster_type,
                    "level": "HIGH" if risk_assessment["adjusted_risk_score"] > 80 else "MODERATE",
                    "message": f"Elevated {disaster_type} risk detected"
                })
        
        # Generate recommended actions based on highest risks
        high_risks = sorted(
            current_risks["risk_levels"].items(),
            key=lambda x: x[1]["risk_score"],
            reverse=True
        )[:3]
        
        for risk_type, risk_data in high_risks:
            if risk_data["risk_score"] > 40:
                current_risks["recommended_actions"].append(
                    f"Review {risk_type} preparedness plan (Risk: {risk_data['risk_score']:.1f}%)"
                )
        
        return current_risks
    
    def _simulate_current_conditions(self) -> Dict[str, Any]:
        """Simulate current environmental conditions for testing"""
        
        # In production, this would connect to real weather/threat APIs
        return {
            "temperature": random.uniform(20, 100),
            "humidity": random.uniform(10, 90),
            "wind_speed": random.uniform(0, 50),
            "precipitation": random.uniform(0, 2),
            "power_grid_stress": random.uniform(30, 95),
            "cyber_threat_level": random.randint(1, 10),
            "seismic_activity": random.uniform(0, 3),
            "air_quality_index": random.randint(0, 300)
        }
    
    def generate_risk_report(self, scenarios: List[Dict[str, Any]], 
                           location: str = "suburban") -> str:
        """
        Generate comprehensive risk report for multiple scenarios
        
        Args:
            scenarios: List of disaster scenarios to assess
            location: Location type
            
        Returns:
            Formatted risk report
        """
        
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE RISK ASSESSMENT REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Location Type: {location.upper()}")
        report.append("")
        
        # Assess each scenario
        assessments = []
        for scenario in scenarios:
            assessment = self.calculate_comprehensive_risk(scenario, location)
            assessments.append(assessment)
        
        # Sort by risk score
        assessments.sort(key=lambda x: x["adjusted_risk_score"], reverse=True)
        
        # High risk scenarios
        report.append("HIGH RISK SCENARIOS (>60%)")
        report.append("-" * 40)
        high_risk = [a for a in assessments if a["adjusted_risk_score"] > 60]
        if high_risk:
            for assessment in high_risk:
                report.append(f"🔴 {assessment['scenario']}")
                report.append(f"   Risk Score: {assessment['adjusted_risk_score']:.1f}%")
                report.append(f"   Probability: {assessment['probability']:.1f}%")
                report.append(f"   Priority: {assessment['action_priority']}")
                report.append("")
        else:
            report.append("No high-risk scenarios identified")
            report.append("")
        
        # Moderate risk scenarios
        report.append("MODERATE RISK SCENARIOS (40-60%)")
        report.append("-" * 40)
        moderate_risk = [a for a in assessments if 40 < a["adjusted_risk_score"] <= 60]
        if moderate_risk:
            for assessment in moderate_risk:
                report.append(f"🟡 {assessment['scenario']}")
                report.append(f"   Risk Score: {assessment['adjusted_risk_score']:.1f}%")
                report.append(f"   Probability: {assessment['probability']:.1f}%")
                report.append("")
        else:
            report.append("No moderate-risk scenarios identified")
            report.append("")
        
        # Summary statistics
        report.append("SUMMARY STATISTICS")
        report.append("-" * 40)
        avg_risk = sum(a["adjusted_risk_score"] for a in assessments) / len(assessments)
        max_risk = max(a["adjusted_risk_score"] for a in assessments)
        min_risk = min(a["adjusted_risk_score"] for a in assessments)
        
        report.append(f"Average Risk Score: {avg_risk:.1f}%")
        report.append(f"Highest Risk: {max_risk:.1f}%")
        report.append(f"Lowest Risk: {min_risk:.1f}%")
        report.append(f"Scenarios Assessed: {len(assessments)}")
        
        # Top recommendations
        report.append("")
        report.append("TOP RECOMMENDATIONS")
        report.append("-" * 40)
        
        # Aggregate all mitigations
        all_mitigations = []
        for assessment in assessments[:5]:  # Top 5 risks
            all_mitigations.extend(assessment["mitigation_available"])
        
        # Get unique mitigations
        unique_mitigations = list(set(all_mitigations))[:5]
        for i, mitigation in enumerate(unique_mitigations, 1):
            report.append(f"{i}. {mitigation}")
        
        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        
        return "\n".join(report)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics"""
        
        # Count historical data
        self.cursor.execute("SELECT COUNT(*) FROM historical_disasters")
        historical_count = self.cursor.fetchone()[0]
        
        # Count risk profiles
        self.cursor.execute("SELECT COUNT(*) FROM risk_profiles")
        profile_count = self.cursor.fetchone()[0]
        
        # Get disaster type coverage
        self.cursor.execute("SELECT DISTINCT disaster_type FROM historical_disasters")
        disaster_types = [row[0] for row in self.cursor.fetchall()]
        
        return {
            "system_name": "Advanced Risk Calculation Engine v3.0",
            "status": "operational",
            "historical_data_points": historical_count,
            "risk_profiles": profile_count,
            "disaster_types_covered": disaster_types,
            "last_updated": datetime.now().isoformat(),
            "capabilities": [
                "Multi-factor risk assessment",
                "Historical data analysis",
                "Real-time condition monitoring",
                "Location-based risk profiling",
                "Cascading risk analysis",
                "Mitigation recommendations",
                "Probability calculations",
                "Time-to-impact estimation"
            ]
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Test the Advanced Risk Calculation Engine"""
    
    print("🚀 Advanced Risk Calculation Engine v3.0")
    print("=" * 60)
    
    # Initialize engine
    engine = AdvancedRiskEngine("test_risk_engine.db")
    
    # Test scenario
    test_scenario = {
        "name": "Category 4 Hurricane",
        "type": "hurricane",
        "duration": "days",
        "warning_time": 72,
        "severity": 8,
        "cascading_effects": ["flooding", "power_outage", "supply_disruption"],
        "primary_needs": ["evacuation", "shelter", "food", "water"],
        "seasonal_factor": "summer",
        "affected_area": "regional"
    }
    
    # Calculate risk
    print("\n📊 Comprehensive Risk Assessment")
    print("-" * 60)
    
    risk_assessment = engine.calculate_comprehensive_risk(
        test_scenario,
        location="coastal",
        current_conditions={"wind_speed": 45, "humidity": 85}
    )
    
    print(f"Scenario: {risk_assessment['scenario']}")
    print(f"Base Risk Score: {risk_assessment['base_risk_score']:.1f}%")
    print(f"Adjusted Risk Score: {risk_assessment['adjusted_risk_score']:.1f}%")
    print(f"Probability: {risk_assessment['probability']:.1f}%")
    print(f"Impact Severity: {risk_assessment['impact_severity']}/10")
    print(f"Time to Impact: {risk_assessment['time_to_impact']}")
    print(f"Confidence Level: {risk_assessment['confidence_level']:.1f}%")
    print(f"Action Priority: {risk_assessment['action_priority']}")
    
    print("\n🛡️ Available Mitigations:")
    for mitigation in risk_assessment["mitigation_available"]:
        print(f"  • {mitigation}")
    
    print("\n📈 Real-Time Risk Update")
    print("-" * 60)
    
    current_risks = engine.get_real_time_risk_update("suburban")
    print(f"Location: {current_risks['location']}")
    print("\nCurrent Risk Levels:")
    
    for disaster, risk_data in sorted(
        current_risks["risk_levels"].items(),
        key=lambda x: x[1]["risk_score"],
        reverse=True
    )[:5]:
        risk_score = risk_data["risk_score"]
        if risk_score > 60:
            indicator = "🔴"
        elif risk_score > 40:
            indicator = "🟡"
        else:
            indicator = "🟢"
        print(f"  {indicator} {disaster}: {risk_score:.1f}%")
    
    print("\n✅ System Status")
    print("-" * 60)
    status = engine.get_system_status()
    print(f"System: {status['system_name']}")
    print(f"Status: {status['status']}")
    print(f"Historical Data Points: {status['historical_data_points']}")
    print(f"Risk Profiles: {status['risk_profiles']}")
    print(f"Disaster Types: {', '.join(status['disaster_types_covered'])}")
    
    engine.close()
    
    import os
    if os.path.exists("test_risk_engine.db"):
        os.remove("test_risk_engine.db")


if __name__ == "__main__":
    main()
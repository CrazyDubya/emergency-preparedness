#!/usr/bin/env python3
"""
Scenario-Based Drill Generator - Version 3.0
Comprehensive drill system for all 20 disaster scenarios with progressive difficulty
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import math

class ScenarioDrillGenerator:
    """
    Advanced drill generator that creates customized drills for all disaster scenarios
    with progressive difficulty, family-specific customization, and performance tracking
    """
    
    def __init__(self, db_path: str = "scenario_drills.db"):
        """Initialize the Scenario-Based Drill Generator"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_database()
        self._initialize_drill_templates()
        self._initialize_family_profiles()
    
    def _initialize_database(self):
        """Create database tables for drill management"""
        
        # Drill templates table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drill_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT UNIQUE NOT NULL,
                disaster_type TEXT NOT NULL,
                difficulty_level INTEGER,
                duration_minutes INTEGER,
                drill_objectives TEXT,
                scenario_elements TEXT,
                success_criteria TEXT,
                equipment_needed TEXT,
                safety_considerations TEXT,
                learning_outcomes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Drill executions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drill_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drill_id TEXT UNIQUE NOT NULL,
                template_name TEXT NOT NULL,
                family_profile TEXT,
                difficulty_level INTEGER,
                execution_date TEXT,
                duration_minutes INTEGER,
                participants TEXT,
                scenario_customizations TEXT,
                performance_metrics TEXT,
                success_score REAL,
                areas_for_improvement TEXT,
                next_drill_recommendations TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Family profiles table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS family_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_name TEXT UNIQUE NOT NULL,
                family_size INTEGER,
                age_ranges TEXT,
                special_needs TEXT,
                living_situation TEXT,
                previous_experience TEXT,
                skill_levels TEXT,
                available_equipment TEXT,
                time_constraints TEXT,
                learning_preferences TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance tracking table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                family_profile TEXT NOT NULL,
                disaster_type TEXT NOT NULL,
                difficulty_level INTEGER,
                drill_count INTEGER,
                average_score REAL,
                best_score REAL,
                latest_score REAL,
                improvement_trend REAL,
                mastery_level INTEGER,
                recommended_next_level INTEGER,
                last_drill_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Drill feedback table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drill_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drill_id TEXT NOT NULL,
                participant_name TEXT,
                difficulty_rating INTEGER,
                realism_rating INTEGER,
                usefulness_rating INTEGER,
                suggestions TEXT,
                confidence_improvement INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _initialize_drill_templates(self):
        """Initialize comprehensive drill templates for all 20 scenarios"""
        
        drill_templates = [
            # Earthquake Drills
            {
                "template_name": "Earthquake Drop-Cover-Hold Basic",
                "disaster_type": "earthquake",
                "difficulty_level": 1,
                "duration_minutes": 10,
                "drill_objectives": json.dumps([
                    "Practice immediate drop, cover, and hold response",
                    "Identify safe spots in each room",
                    "Learn to protect head and neck",
                    "Practice staying calm during shaking"
                ]),
                "scenario_elements": json.dumps([
                    "Sudden earthquake alarm",
                    "10-15 seconds of simulated shaking",
                    "Aftershock warnings",
                    "Check for injuries phase"
                ]),
                "success_criteria": json.dumps([
                    "Drop within 5 seconds of alarm",
                    "Take cover under sturdy furniture",
                    "Hold position until shaking stops",
                    "Remain calm and follow instructions"
                ]),
                "equipment_needed": json.dumps([
                    "Earthquake alarm app", "Timer", "Pillows for protection"
                ]),
                "learning_outcomes": json.dumps([
                    "Automatic drop-cover-hold response",
                    "Identification of safe spots",
                    "Understanding of earthquake basics"
                ])
            },
            {
                "template_name": "Earthquake Family Coordination Advanced",
                "disaster_type": "earthquake",
                "difficulty_level": 3,
                "duration_minutes": 45,
                "drill_objectives": json.dumps([
                    "Coordinate family response during earthquake",
                    "Practice post-earthquake evacuation",
                    "Test family communication plan",
                    "Assess building damage safely"
                ]),
                "scenario_elements": json.dumps([
                    "Major earthquake (7.0+) scenario",
                    "Family members in different rooms",
                    "Simulated building damage",
                    "Communication systems disrupted"
                ]),
                "equipment_needed": json.dumps([
                    "Emergency kits", "First aid supplies", "Flashlights", "Battery radio"
                ])
            },
            
            # Fire Drills
            {
                "template_name": "House Fire Evacuation Basic",
                "disaster_type": "fire",
                "difficulty_level": 1,
                "duration_minutes": 8,
                "drill_objectives": json.dumps([
                    "Practice rapid evacuation",
                    "Test smoke alarm response",
                    "Learn to stay low in smoke",
                    "Use alternate escape routes"
                ]),
                "scenario_elements": json.dumps([
                    "Smoke alarm activation",
                    "Simulated smoke (safe fog)",
                    "Blocked primary exit",
                    "Meeting point assembly"
                ]),
                "equipment_needed": json.dumps([
                    "Smoke alarm", "Safe fog machine", "Timer", "Flashlight"
                ])
            },
            {
                "template_name": "Multi-Room Fire Emergency Advanced",
                "disaster_type": "fire",
                "difficulty_level": 4,
                "duration_minutes": 20,
                "drill_objectives": json.dumps([
                    "Coordinate family evacuation",
                    "Practice fire suppression decisions",
                    "Test backup escape plans",
                    "Simulate night-time scenario"
                ]),
                "scenario_elements": json.dumps([
                    "Fire in multiple rooms",
                    "Nighttime/darkness conditions",
                    "Door temperature checks",
                    "Emergency services interaction"
                ])
            },
            
            # Hurricane/Storm Drills
            {
                "template_name": "Hurricane Preparation Basic",
                "disaster_type": "hurricane",
                "difficulty_level": 2,
                "duration_minutes": 60,
                "drill_objectives": json.dumps([
                    "Practice hurricane preparation checklist",
                    "Secure property efficiently",
                    "Test emergency supplies",
                    "Practice evacuation decision-making"
                ]),
                "scenario_elements": json.dumps([
                    "72-hour hurricane warning",
                    "Weather updates and track changes",
                    "Evacuation zone decisions",
                    "Supply chain disruptions"
                ]),
                "equipment_needed": json.dumps([
                    "Weather radio", "Plywood/boards", "Emergency supplies", "Vehicle fuel"
                ])
            },
            
            # Tornado Drills
            {
                "template_name": "Tornado Shelter Basic",
                "disaster_type": "tornado",
                "difficulty_level": 2,
                "duration_minutes": 15,
                "drill_objectives": json.dumps([
                    "Practice immediate shelter response",
                    "Identify best shelter locations",
                    "Test tornado warning systems",
                    "Practice protective positioning"
                ]),
                "scenario_elements": json.dumps([
                    "Tornado watch escalates to warning",
                    "15-minute warning time",
                    "Seek lowest floor, interior room",
                    "Protect from flying debris"
                ]),
                "equipment_needed": json.dumps([
                    "Weather radio", "Helmets/protection", "Mattresses", "Flashlights"
                ])
            },
            
            # Flood Drills
            {
                "template_name": "Flash Flood Response Basic",
                "disaster_type": "flood",
                "difficulty_level": 2,
                "duration_minutes": 25,
                "drill_objectives": json.dumps([
                    "Practice rapid evacuation to high ground",
                    "Learn flood safety basics",
                    "Test communication during flood",
                    "Practice vehicle flood procedures"
                ]),
                "scenario_elements": json.dumps([
                    "Flash flood warning",
                    "Rising water simulation",
                    "Vehicle stranded scenario",
                    "Power outage complications"
                ]),
                "equipment_needed": json.dumps([
                    "Life jackets", "Waterproof bags", "Emergency radio", "Whistle"
                ])
            },
            
            # Power Outage Drills
            {
                "template_name": "Extended Power Outage Basic",
                "disaster_type": "power_outage",
                "difficulty_level": 2,
                "duration_minutes": 90,
                "drill_objectives": json.dumps([
                    "Practice power outage procedures",
                    "Test backup power systems",
                    "Practice food preservation",
                    "Test communication alternatives"
                ]),
                "scenario_elements": json.dumps([
                    "Sudden power loss",
                    "Generator startup procedures",
                    "Food spoilage timeline",
                    "Heat/cooling alternatives"
                ]),
                "equipment_needed": json.dumps([
                    "Generator", "Flashlights", "Battery radio", "Coolers", "Alternative heating"
                ])
            },
            
            # Cyber Attack Drills
            {
                "template_name": "Cyber Attack Response Basic",
                "disaster_type": "cyber_attack",
                "difficulty_level": 3,
                "duration_minutes": 30,
                "drill_objectives": json.dumps([
                    "Practice digital disconnection",
                    "Test offline backup systems",
                    "Practice cash-only transactions",
                    "Test alternative communication"
                ]),
                "scenario_elements": json.dumps([
                    "Banking systems down",
                    "Internet connectivity lost",
                    "Digital payment systems failed",
                    "Social media compromised"
                ]),
                "equipment_needed": json.dumps([
                    "Offline backup drives", "Cash reserves", "Paper maps", "Land-line phone"
                ])
            },
            
            # Pandemic Drills
            {
                "template_name": "Pandemic Lockdown Basic",
                "disaster_type": "pandemic",
                "difficulty_level": 2,
                "duration_minutes": 180,
                "drill_objectives": json.dumps([
                    "Practice extended home isolation",
                    "Test remote work/school setup",
                    "Practice supply rationing",
                    "Test mental health support"
                ]),
                "scenario_elements": json.dumps([
                    "Lockdown announcement",
                    "Supply chain disruptions",
                    "Remote work requirements",
                    "Social isolation challenges"
                ]),
                "equipment_needed": json.dumps([
                    "Extended food supplies", "Remote work setup", "Entertainment options", "Exercise equipment"
                ])
            },
            
            # Nuclear/Chemical Drills
            {
                "template_name": "Nuclear Alert Shelter-in-Place",
                "disaster_type": "nuclear",
                "difficulty_level": 4,
                "duration_minutes": 120,
                "drill_objectives": json.dumps([
                    "Practice immediate shelter-in-place",
                    "Test room sealing procedures",
                    "Practice decontamination basics",
                    "Test emergency supply access"
                ]),
                "scenario_elements": json.dumps([
                    "Nuclear power plant alert",
                    "Radiation plume modeling",
                    "Shelter-in-place order",
                    "Decontamination procedures"
                ]),
                "equipment_needed": json.dumps([
                    "Plastic sheeting", "Duct tape", "Potassium iodide", "Radiation detector", "Sealed food/water"
                ])
            },
            
            # Terrorism/Active Threat Drills
            {
                "template_name": "Active Threat Response Basic",
                "disaster_type": "terrorism",
                "difficulty_level": 3,
                "duration_minutes": 20,
                "drill_objectives": json.dumps([
                    "Practice Run-Hide-Fight protocol",
                    "Test lockdown procedures",
                    "Practice silent communication",
                    "Test emergency contact systems"
                ]),
                "scenario_elements": json.dumps([
                    "Active threat alert",
                    "Lockdown announcement",
                    "Escape route evaluation",
                    "Law enforcement response"
                ]),
                "equipment_needed": json.dumps([
                    "Barricading materials", "Silent communication devices", "Emergency whistle"
                ])
            },
            
            # Comprehensive Multi-Scenario Drills
            {
                "template_name": "Multi-Hazard Response Advanced",
                "disaster_type": "general",
                "difficulty_level": 5,
                "duration_minutes": 240,
                "drill_objectives": json.dumps([
                    "Practice cascading disaster response",
                    "Test decision-making under pressure",
                    "Coordinate multiple response plans",
                    "Test resource prioritization"
                ]),
                "scenario_elements": json.dumps([
                    "Primary disaster triggers secondary",
                    "Multiple simultaneous threats",
                    "Resource constraints",
                    "Communication disruptions"
                ]),
                "equipment_needed": json.dumps([
                    "All emergency equipment", "Decision-making aids", "Communication systems"
                ])
            }
        ]
        
        # Insert drill templates
        for template in drill_templates:
            self.cursor.execute('''
                INSERT OR REPLACE INTO drill_templates
                (template_name, disaster_type, difficulty_level, duration_minutes,
                 drill_objectives, scenario_elements, success_criteria, equipment_needed, learning_outcomes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                template["template_name"],
                template["disaster_type"],
                template["difficulty_level"],
                template["duration_minutes"],
                template["drill_objectives"],
                template["scenario_elements"],
                template.get("success_criteria", "[]"),
                template.get("equipment_needed", "[]"),
                template.get("learning_outcomes", "[]")
            ))
        
        self.conn.commit()
    
    def _initialize_family_profiles(self):
        """Initialize default family profile configurations"""
        
        profiles = [
            {
                "profile_name": "Default Family",
                "family_size": 4,
                "age_ranges": json.dumps(["adult", "adult", "teen", "child"]),
                "special_needs": json.dumps([]),
                "living_situation": "suburban_house",
                "previous_experience": json.dumps({"earthquake": 1, "fire": 2, "storm": 2}),
                "skill_levels": json.dumps({"first_aid": 3, "emergency_prep": 2, "technical": 3}),
                "available_equipment": json.dumps([
                    "basic_emergency_kit", "fire_extinguisher", "first_aid_kit", 
                    "flashlights", "battery_radio", "generator"
                ]),
                "time_constraints": json.dumps({"weekend": "flexible", "weekday": "limited"}),
                "learning_preferences": json.dumps(["hands_on", "visual", "step_by_step"])
            }
        ]
        
        for profile in profiles:
            self.cursor.execute('''
                INSERT OR REPLACE INTO family_profiles
                (profile_name, family_size, age_ranges, special_needs, living_situation,
                 previous_experience, skill_levels, available_equipment, time_constraints, learning_preferences)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(profile.values()))
        
        self.conn.commit()
    
    def generate_drill(self, disaster_type: str, 
                      family_profile: str = "Default Family",
                      difficulty_level: int = None,
                      duration_preference: int = None,
                      specific_objectives: List[str] = None) -> Dict[str, Any]:
        """
        Generate a customized drill for a specific scenario
        
        Args:
            disaster_type: Type of disaster to drill for
            family_profile: Family configuration to customize for
            difficulty_level: Override difficulty (1-5)
            duration_preference: Preferred duration in minutes
            specific_objectives: Custom objectives to include
            
        Returns:
            Generated drill specification
        """
        
        # Get family profile
        self.cursor.execute('''
            SELECT * FROM family_profiles WHERE profile_name = ?
        ''', (family_profile,))
        
        profile_row = self.cursor.fetchone()
        if not profile_row:
            return {"error": f"Family profile '{family_profile}' not found"}
        
        profile = {
            "name": profile_row[1],
            "size": profile_row[2],
            "age_ranges": json.loads(profile_row[3]),
            "special_needs": json.loads(profile_row[4]),
            "living_situation": profile_row[5],
            "experience": json.loads(profile_row[6]),
            "skill_levels": json.loads(profile_row[7]),
            "equipment": json.loads(profile_row[8]),
            "time_constraints": json.loads(profile_row[9]),
            "learning_preferences": json.loads(profile_row[10])
        }
        
        # Determine appropriate difficulty level
        if difficulty_level is None:
            experience_level = profile["experience"].get(disaster_type, 0)
            avg_skill = sum(profile["skill_levels"].values()) / len(profile["skill_levels"])
            difficulty_level = min(5, max(1, int(experience_level + avg_skill / 2)))
        
        # Get suitable drill templates
        self.cursor.execute('''
            SELECT * FROM drill_templates
            WHERE disaster_type = ? AND difficulty_level <= ?
            ORDER BY difficulty_level DESC
        ''', (disaster_type, difficulty_level))
        
        templates = self.cursor.fetchall()
        if not templates:
            return {"error": f"No drill templates found for {disaster_type}"}
        
        # Select best template
        template_row = templates[0]  # Highest difficulty within range
        
        # Create drill specification
        drill_id = f"DRILL_{disaster_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Customize objectives
        base_objectives = json.loads(template_row[5])
        if specific_objectives:
            base_objectives.extend(specific_objectives)
        
        # Customize scenario elements based on family profile
        scenario_elements = json.loads(template_row[6])
        customized_elements = self._customize_scenario(scenario_elements, profile, disaster_type)
        
        # Adjust duration if requested
        base_duration = template_row[4]
        if duration_preference:
            adjusted_duration = duration_preference
        else:
            # Adjust based on family size and age ranges
            duration_modifier = 1.0
            if profile["size"] > 4:
                duration_modifier += 0.2
            if "elderly" in profile["age_ranges"] or "special_needs" in profile["special_needs"]:
                duration_modifier += 0.3
            adjusted_duration = int(base_duration * duration_modifier)
        
        # Generate equipment checklist
        base_equipment = json.loads(template_row[8])
        available_equipment = profile["equipment"]
        equipment_status = self._check_equipment_availability(base_equipment, available_equipment)
        
        # Create performance metrics framework
        performance_metrics = self._generate_performance_metrics(disaster_type, difficulty_level)
        
        drill_spec = {
            "drill_id": drill_id,
            "template_name": template_row[1],
            "disaster_type": disaster_type,
            "difficulty_level": difficulty_level,
            "estimated_duration": adjusted_duration,
            "family_profile": family_profile,
            "objectives": base_objectives,
            "scenario_elements": customized_elements,
            "success_criteria": json.loads(template_row[7]),
            "equipment_checklist": equipment_status,
            "performance_metrics": performance_metrics,
            "safety_considerations": self._generate_safety_considerations(disaster_type, profile),
            "learning_outcomes": json.loads(template_row[10]),
            "customizations": {
                "family_size_adjustments": profile["size"] != 4,
                "special_needs_accommodations": len(profile["special_needs"]) > 0,
                "equipment_substitutions": len([e for e in equipment_status if not e["available"]]) > 0,
                "difficulty_reasoning": f"Level {difficulty_level} based on experience and skills"
            },
            "execution_guide": self._generate_execution_guide(customized_elements, adjusted_duration),
            "created_at": datetime.now().isoformat()
        }
        
        # Store drill specification
        self.cursor.execute('''
            INSERT INTO drill_executions
            (drill_id, template_name, family_profile, difficulty_level,
             duration_minutes, scenario_customizations, performance_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            drill_id,
            template_row[1],
            family_profile,
            difficulty_level,
            adjusted_duration,
            json.dumps(drill_spec["customizations"]),
            json.dumps(performance_metrics)
        ))
        
        self.conn.commit()
        
        return drill_spec
    
    def _customize_scenario(self, base_elements: List[str], 
                           profile: Dict[str, Any], 
                           disaster_type: str) -> List[Dict[str, Any]]:
        """Customize scenario elements based on family profile"""
        
        customized = []
        
        for element in base_elements:
            custom_element = {
                "element": element,
                "adaptations": []
            }
            
            # Family size adaptations
            if profile["size"] > 4:
                custom_element["adaptations"].append(f"Account for {profile['size']} family members")
            
            # Age-specific adaptations
            if "elderly" in profile["age_ranges"]:
                custom_element["adaptations"].append("Allow extra time for elderly participants")
            if "child" in profile["age_ranges"]:
                custom_element["adaptations"].append("Include child-safe procedures")
            
            # Living situation adaptations
            if profile["living_situation"] == "apartment":
                if "evacuation" in element.lower():
                    custom_element["adaptations"].append("Practice stairwell evacuation")
            elif profile["living_situation"] == "mobile_home":
                if disaster_type in ["tornado", "hurricane"]:
                    custom_element["adaptations"].append("Identify community shelter location")
            
            # Special needs adaptations
            for need in profile["special_needs"]:
                if need == "mobility":
                    custom_element["adaptations"].append("Ensure wheelchair accessible routes")
                elif need == "hearing":
                    custom_element["adaptations"].append("Use visual alert signals")
                elif need == "cognitive":
                    custom_element["adaptations"].append("Simplify instructions and repeat frequently")
            
            customized.append(custom_element)
        
        return customized
    
    def _check_equipment_availability(self, required: List[str], 
                                    available: List[str]) -> List[Dict[str, Any]]:
        """Check availability of required equipment"""
        
        equipment_status = []
        
        for item in required:
            is_available = any(avail in item.lower() or item.lower() in avail for avail in available)
            
            status = {
                "item": item,
                "available": is_available,
                "substitutions": []
            }
            
            # Suggest substitutions for missing items
            if not is_available:
                status["substitutions"] = self._suggest_equipment_substitutions(item)
            
            equipment_status.append(status)
        
        return equipment_status
    
    def _suggest_equipment_substitutions(self, missing_item: str) -> List[str]:
        """Suggest substitutions for missing equipment"""
        
        substitutions = {
            "smoke alarm": ["Smartphone alarm", "Manual alarm"],
            "weather radio": ["Weather app", "Emergency alert system"],
            "generator": ["Battery bank", "Solar charger", "Car inverter"],
            "life jackets": ["Flotation devices", "Pool noodles", "Inflatable items"],
            "helmet": ["Hard hat", "Bicycle helmet", "Cushions for head protection"],
            "plastic sheeting": ["Tarps", "Large garbage bags", "Shower curtains"],
            "duct tape": ["Masking tape", "Electrical tape", "String/rope"]
        }
        
        for key, subs in substitutions.items():
            if key in missing_item.lower():
                return subs
        
        return ["Creative improvisation needed"]
    
    def _generate_performance_metrics(self, disaster_type: str, 
                                    difficulty_level: int) -> Dict[str, Any]:
        """Generate performance metrics framework for the drill"""
        
        base_metrics = {
            "response_time": {
                "measure": "Time from alert to first action",
                "target": "< 60 seconds",
                "weight": 30
            },
            "procedure_accuracy": {
                "measure": "Correct execution of procedures",
                "target": "90%+ steps completed correctly",
                "weight": 25
            },
            "family_coordination": {
                "measure": "Effectiveness of family communication",
                "target": "All members accounted for",
                "weight": 20
            },
            "resource_utilization": {
                "measure": "Proper use of emergency resources",
                "target": "Equipment used correctly",
                "weight": 15
            },
            "stress_management": {
                "measure": "Calm and controlled responses",
                "target": "Minimal panic, clear thinking",
                "weight": 10
            }
        }
        
        # Disaster-specific metrics
        disaster_specific = {
            "earthquake": {
                "protection_positioning": {
                    "measure": "Drop, cover, hold execution",
                    "target": "Proper position within 5 seconds",
                    "weight": 35
                }
            },
            "fire": {
                "evacuation_speed": {
                    "measure": "Time to exit building",
                    "target": "< 2 minutes",
                    "weight": 40
                }
            },
            "tornado": {
                "shelter_selection": {
                    "measure": "Choice of safest shelter location",
                    "target": "Lowest floor, interior room",
                    "weight": 30
                }
            },
            "cyber_attack": {
                "digital_disconnection": {
                    "measure": "Speed of disconnecting systems",
                    "target": "< 3 minutes",
                    "weight": 25
                }
            }
        }
        
        # Combine base and specific metrics
        all_metrics = base_metrics.copy()
        if disaster_type in disaster_specific:
            all_metrics.update(disaster_specific[disaster_type])
        
        # Adjust targets based on difficulty level
        for metric in all_metrics.values():
            if difficulty_level >= 4:
                # Make targets more stringent for advanced drills
                if "seconds" in metric["target"]:
                    time_value = int(metric["target"].split()[1])
                    metric["target"] = metric["target"].replace(str(time_value), str(int(time_value * 0.8)))
                elif "%" in metric["target"]:
                    perc_value = int(metric["target"].split("%")[0])
                    metric["target"] = metric["target"].replace(f"{perc_value}%", f"{min(99, perc_value + 5)}%")
        
        return all_metrics
    
    def _generate_safety_considerations(self, disaster_type: str, 
                                      profile: Dict[str, Any]) -> List[str]:
        """Generate safety considerations for the drill"""
        
        general_safety = [
            "Ensure all participants understand this is a drill",
            "Have first aid kit readily available",
            "Stop drill immediately if anyone is injured",
            "Designate a drill safety observer"
        ]
        
        disaster_safety = {
            "fire": [
                "Use only safe smoke simulation methods",
                "Ensure all exits remain actually accessible",
                "Have fire extinguisher ready",
                "No actual fire or dangerous heat sources"
            ],
            "earthquake": [
                "Clear area of breakable objects before starting",
                "Use soft materials for 'debris' simulation",
                "Ensure furniture is actually stable",
                "Practice on single level only"
            ],
            "flood": [
                "No actual water in living spaces",
                "Use only marked safe areas for 'high ground'",
                "Ensure all 'evacuation' routes are safe",
                "Supervise children closely during water safety discussions"
            ],
            "tornado": [
                "Ensure shelter spaces are actually safe",
                "Use soft materials for 'debris' protection",
                "Avoid outdoor tornado shelter practice",
                "Clear hallways and shelter areas"
            ],
            "power_outage": [
                "Keep main power connected for safety",
                "Use battery-powered lighting only",
                "Ensure generator is properly ventilated if used",
                "Keep refrigerated medications properly stored"
            ]
        }
        
        safety_considerations = general_safety.copy()
        
        if disaster_type in disaster_safety:
            safety_considerations.extend(disaster_safety[disaster_type])
        
        # Add family-specific safety considerations
        if "child" in profile["age_ranges"]:
            safety_considerations.append("Provide extra supervision for children")
            safety_considerations.append("Explain drill nature clearly to avoid fear")
        
        if "elderly" in profile["age_ranges"]:
            safety_considerations.append("Allow extra time and assistance for elderly participants")
            safety_considerations.append("Ensure no fall hazards during movement")
        
        for need in profile["special_needs"]:
            if need == "mobility":
                safety_considerations.append("Ensure wheelchair accessible drill areas")
            elif need == "hearing":
                safety_considerations.append("Use visual signals for hearing-impaired participants")
            elif need == "medical":
                safety_considerations.append("Keep medical equipment and medications accessible")
        
        return safety_considerations
    
    def _generate_execution_guide(self, scenario_elements: List[Dict[str, Any]], 
                                 duration: int) -> Dict[str, Any]:
        """Generate step-by-step execution guide for the drill"""
        
        # Divide drill into phases
        phases = {
            "preparation": {
                "time_allocation": "10%",
                "duration_minutes": max(2, int(duration * 0.1)),
                "activities": [
                    "Brief all participants on drill objectives",
                    "Set up any required simulation equipment",
                    "Assign roles and responsibilities",
                    "Review safety guidelines",
                    "Ensure all emergency equipment is accessible"
                ]
            },
            "trigger": {
                "time_allocation": "5%",
                "duration_minutes": max(1, int(duration * 0.05)),
                "activities": [
                    "Activate drill trigger (alarm, announcement)",
                    "Begin timing response",
                    "Observer begins noting responses"
                ]
            },
            "response": {
                "time_allocation": "70%",
                "duration_minutes": int(duration * 0.7),
                "activities": []
            },
            "debrief": {
                "time_allocation": "15%",
                "duration_minutes": int(duration * 0.15),
                "activities": [
                    "Gather all participants",
                    "Review performance against objectives",
                    "Discuss what went well",
                    "Identify areas for improvement",
                    "Record lessons learned"
                ]
            }
        }
        
        # Populate response phase from scenario elements
        for element in scenario_elements:
            phases["response"]["activities"].append(element["element"])
            for adaptation in element["adaptations"]:
                phases["response"]["activities"].append(f"  → {adaptation}")
        
        # Create timeline
        timeline = []
        current_time = 0
        
        for phase_name, phase_data in phases.items():
            timeline.append({
                "phase": phase_name.title(),
                "start_time": current_time,
                "duration": phase_data["duration_minutes"],
                "activities": phase_data["activities"]
            })
            current_time += phase_data["duration_minutes"]
        
        return {
            "total_duration": duration,
            "phases": phases,
            "timeline": timeline,
            "key_timing": {
                "trigger_to_response": "< 60 seconds",
                "peak_activity": f"{int(duration * 0.3)}-{int(duration * 0.8)} minutes",
                "debrief_start": f"{int(duration * 0.85)} minutes"
            }
        }
    
    def execute_drill(self, drill_id: str, participants: List[str]) -> Dict[str, Any]:
        """
        Begin execution of a drill
        
        Args:
            drill_id: ID of drill to execute
            participants: List of participant names
            
        Returns:
            Drill execution tracker
        """
        
        # Get drill specification
        self.cursor.execute('''
            SELECT * FROM drill_executions WHERE drill_id = ?
        ''', (drill_id,))
        
        drill_row = self.cursor.fetchone()
        if not drill_row:
            return {"error": f"Drill '{drill_id}' not found"}
        
        # Update execution record
        self.cursor.execute('''
            UPDATE drill_executions
            SET execution_date = ?, participants = ?, completed = 0
            WHERE drill_id = ?
        ''', (datetime.now().isoformat(), json.dumps(participants), drill_id))
        
        self.conn.commit()
        
        return {
            "drill_id": drill_id,
            "status": "in_progress",
            "start_time": datetime.now().isoformat(),
            "participants": participants,
            "template_name": drill_row[2],
            "difficulty_level": drill_row[4],
            "estimated_duration": drill_row[6],
            "instructions": "Follow the execution guide step by step",
            "next_phase": "Preparation - Brief participants and set up equipment"
        }
    
    def complete_drill(self, drill_id: str, performance_scores: Dict[str, float],
                      duration_actual: int, notes: str = None) -> Dict[str, Any]:
        """
        Complete a drill execution and record results
        
        Args:
            drill_id: ID of drill that was executed
            performance_scores: Scores for each performance metric
            duration_actual: Actual duration in minutes
            notes: Optional notes about the execution
            
        Returns:
            Drill completion summary with recommendations
        """
        
        # Calculate overall success score
        overall_score = sum(performance_scores.values()) / len(performance_scores)
        
        # Get drill details
        self.cursor.execute('''
            SELECT * FROM drill_executions WHERE drill_id = ?
        ''', (drill_id,))
        
        drill_row = self.cursor.fetchone()
        if not drill_row:
            return {"error": f"Drill '{drill_id}' not found"}
        
        # Generate improvement recommendations
        improvements = self._generate_improvement_recommendations(
            performance_scores, 
            drill_row[3],  # disaster_type from template
            drill_row[4]   # difficulty_level
        )
        
        # Generate next drill recommendations
        next_drill = self._recommend_next_drill(
            drill_row[3],  # disaster_type
            overall_score,
            drill_row[4]   # current difficulty
        )
        
        # Update drill record
        self.cursor.execute('''
            UPDATE drill_executions
            SET duration_minutes = ?, performance_metrics = ?, success_score = ?,
                areas_for_improvement = ?, next_drill_recommendations = ?, completed = 1
            WHERE drill_id = ?
        ''', (
            duration_actual,
            json.dumps(performance_scores),
            overall_score,
            json.dumps(improvements),
            json.dumps(next_drill),
            drill_id
        ))
        
        # Update performance tracking
        self._update_performance_tracking(
            drill_row[3],  # family_profile
            drill_row[2],  # disaster_type
            drill_row[4],  # difficulty_level
            overall_score
        )
        
        self.conn.commit()
        
        return {
            "drill_id": drill_id,
            "completion_status": "completed",
            "overall_score": round(overall_score, 1),
            "performance_breakdown": performance_scores,
            "duration_actual": duration_actual,
            "duration_target": drill_row[6],
            "time_efficiency": round((drill_row[6] / max(1, duration_actual)) * 100, 1),
            "areas_for_improvement": improvements,
            "next_drill_recommendations": next_drill,
            "skill_level_assessment": self._assess_skill_level(overall_score),
            "mastery_progress": self._calculate_mastery_progress(drill_row[3], drill_row[2])
        }
    
    def _generate_improvement_recommendations(self, scores: Dict[str, float],
                                           disaster_type: str, 
                                           difficulty_level: int) -> List[str]:
        """Generate specific improvement recommendations based on performance"""
        
        recommendations = []
        
        # Identify weakest areas
        weak_areas = [(metric, score) for metric, score in scores.items() if score < 70]
        weak_areas.sort(key=lambda x: x[1])  # Sort by score, lowest first
        
        # Generate recommendations for weak areas
        for metric, score in weak_areas[:3]:  # Top 3 weakest areas
            if metric == "response_time":
                recommendations.append("Practice immediate response drills to improve reaction time")
                recommendations.append("Keep emergency supplies in easily accessible locations")
            elif metric == "procedure_accuracy":
                recommendations.append("Review emergency procedures more frequently")
                recommendations.append("Practice specific steps that were missed or incorrect")
            elif metric == "family_coordination":
                recommendations.append("Develop clear family communication protocols")
                recommendations.append("Practice family meeting points and contact methods")
            elif metric == "resource_utilization":
                recommendations.append("Familiarize family with all emergency equipment")
                recommendations.append("Label emergency supplies clearly for quick identification")
            elif metric == "stress_management":
                recommendations.append("Practice breathing techniques during drills")
                recommendations.append("Focus on calm, clear communication under pressure")
        
        # Add disaster-specific recommendations
        if disaster_type == "earthquake" and scores.get("protection_positioning", 100) < 70:
            recommendations.append("Practice Drop-Cover-Hold technique daily until automatic")
        elif disaster_type == "fire" and scores.get("evacuation_speed", 100) < 70:
            recommendations.append("Time evacuation routes regularly to build speed")
        
        # Add difficulty-specific recommendations
        if difficulty_level >= 3 and sum(scores.values()) / len(scores) < 75:
            recommendations.append("Consider practicing at lower difficulty until fundamentals are solid")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _recommend_next_drill(self, disaster_type: str, score: float, 
                            current_difficulty: int) -> Dict[str, Any]:
        """Recommend next drill based on performance"""
        
        recommendations = {
            "same_scenario": None,
            "progression": None,
            "alternative": None
        }
        
        # Same scenario recommendations
        if score < 75:
            recommendations["same_scenario"] = {
                "type": disaster_type,
                "difficulty": current_difficulty,
                "reason": "Repeat to improve fundamentals",
                "focus_areas": ["accuracy", "speed"]
            }
        elif score >= 85 and current_difficulty < 5:
            recommendations["progression"] = {
                "type": disaster_type,
                "difficulty": current_difficulty + 1,
                "reason": "Ready for increased difficulty",
                "new_challenges": ["time pressure", "complications"]
            }
        
        # Alternative scenario recommendations
        related_scenarios = {
            "earthquake": ["fire", "power_outage"],
            "fire": ["earthquake", "tornado"],
            "hurricane": ["flood", "power_outage"],
            "tornado": ["hurricane", "thunderstorm"],
            "flood": ["hurricane", "dam_failure"],
            "power_outage": ["cyber_attack", "winter_storm"],
            "cyber_attack": ["power_outage", "economic_crisis"]
        }
        
        if disaster_type in related_scenarios:
            alt_type = random.choice(related_scenarios[disaster_type])
            recommendations["alternative"] = {
                "type": alt_type,
                "difficulty": max(1, current_difficulty - 1),
                "reason": "Build skills in related scenario",
                "benefits": ["cross_training", "comprehensive_preparedness"]
            }
        
        return recommendations
    
    def _assess_skill_level(self, score: float) -> str:
        """Assess overall skill level based on score"""
        
        if score >= 90:
            return "Expert - Exceptional preparedness and response"
        elif score >= 80:
            return "Advanced - Strong skills with minor areas for improvement"
        elif score >= 70:
            return "Proficient - Good fundamental skills"
        elif score >= 60:
            return "Developing - Basic skills present, needs practice"
        else:
            return "Novice - Significant improvement needed"
    
    def _calculate_mastery_progress(self, family_profile: str, 
                                  disaster_type: str) -> Dict[str, Any]:
        """Calculate mastery progress for a specific disaster type"""
        
        # Get performance history
        self.cursor.execute('''
            SELECT AVG(success_score), COUNT(*), MAX(difficulty_level)
            FROM drill_executions
            WHERE family_profile = ? AND template_name LIKE ? AND completed = 1
        ''', (family_profile, f"%{disaster_type}%"))
        
        result = self.cursor.fetchone()
        
        if result[1] == 0:  # No previous drills
            return {
                "mastery_level": "Beginner",
                "progress_percentage": 0,
                "drills_completed": 0,
                "next_milestone": "Complete first drill"
            }
        
        avg_score, drill_count, max_difficulty = result
        
        # Calculate mastery level
        mastery_levels = [
            (90, "Master", "Exceptional skill across all scenarios"),
            (80, "Expert", "Advanced skill with consistent performance"),
            (70, "Proficient", "Solid fundamental skills"),
            (60, "Developing", "Basic competency established"),
            (0, "Novice", "Learning foundational skills")
        ]
        
        mastery_level = "Novice"
        description = ""
        for threshold, level, desc in mastery_levels:
            if avg_score >= threshold:
                mastery_level = level
                description = desc
                break
        
        # Calculate progress percentage
        progress = min(100, (avg_score + (drill_count * 5) + (max_difficulty * 10)) / 1.5)
        
        # Determine next milestone
        if mastery_level == "Novice":
            next_milestone = "Achieve 60% average score"
        elif mastery_level == "Developing":
            next_milestone = "Achieve 70% average score"
        elif mastery_level == "Proficient":
            next_milestone = "Achieve 80% average score"
        elif mastery_level == "Expert":
            next_milestone = "Master advanced scenarios"
        else:
            next_milestone = "Teach others and refine skills"
        
        return {
            "mastery_level": mastery_level,
            "description": description,
            "progress_percentage": round(progress, 1),
            "drills_completed": drill_count,
            "average_score": round(avg_score, 1),
            "max_difficulty_completed": max_difficulty,
            "next_milestone": next_milestone
        }
    
    def _update_performance_tracking(self, family_profile: str, disaster_type: str,
                                   difficulty_level: int, score: float):
        """Update performance tracking records"""
        
        # Get existing tracking record
        self.cursor.execute('''
            SELECT * FROM performance_tracking
            WHERE family_profile = ? AND disaster_type = ?
        ''', (family_profile, disaster_type))
        
        existing = self.cursor.fetchone()
        
        if existing:
            # Update existing record
            drill_count = existing[4] + 1
            avg_score = (existing[5] * existing[4] + score) / drill_count
            best_score = max(existing[6], score)
            
            # Calculate improvement trend
            improvement_trend = score - existing[7]  # vs last score
            
            self.cursor.execute('''
                UPDATE performance_tracking
                SET drill_count = ?, average_score = ?, best_score = ?, latest_score = ?,
                    improvement_trend = ?, last_drill_date = ?
                WHERE family_profile = ? AND disaster_type = ?
            ''', (
                drill_count, avg_score, best_score, score, improvement_trend,
                datetime.now().isoformat(), family_profile, disaster_type
            ))
        else:
            # Create new tracking record
            self.cursor.execute('''
                INSERT INTO performance_tracking
                (family_profile, disaster_type, difficulty_level, drill_count,
                 average_score, best_score, latest_score, improvement_trend, last_drill_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                family_profile, disaster_type, difficulty_level, 1,
                score, score, score, 0, datetime.now().isoformat()
            ))
    
    def get_available_drills(self, disaster_type: str = None, 
                           difficulty_range: Tuple[int, int] = None) -> List[Dict[str, Any]]:
        """Get list of available drill templates"""
        
        query = "SELECT * FROM drill_templates"
        params = []
        conditions = []
        
        if disaster_type:
            conditions.append("disaster_type = ?")
            params.append(disaster_type)
        
        if difficulty_range:
            conditions.append("difficulty_level BETWEEN ? AND ?")
            params.extend(difficulty_range)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY disaster_type, difficulty_level"
        
        self.cursor.execute(query, params)
        
        drills = []
        for row in self.cursor.fetchall():
            drills.append({
                "template_name": row[1],
                "disaster_type": row[2],
                "difficulty_level": row[3],
                "duration_minutes": row[4],
                "objectives_count": len(json.loads(row[5])),
                "equipment_needed_count": len(json.loads(row[8])),
                "description": f"Level {row[3]} {row[2]} drill ({row[4]} minutes)"
            })
        
        return drills
    
    def get_performance_history(self, family_profile: str = "Default Family",
                              disaster_type: str = None) -> Dict[str, Any]:
        """Get performance history and progress tracking"""
        
        query = '''
            SELECT disaster_type, difficulty_level, drill_count, average_score,
                   best_score, latest_score, improvement_trend, last_drill_date
            FROM performance_tracking
            WHERE family_profile = ?
        '''
        params = [family_profile]
        
        if disaster_type:
            query += " AND disaster_type = ?"
            params.append(disaster_type)
        
        query += " ORDER BY average_score DESC"
        
        self.cursor.execute(query, params)
        
        performance_data = []
        for row in self.cursor.fetchall():
            performance_data.append({
                "disaster_type": row[0],
                "difficulty_level": row[1],
                "drills_completed": row[2],
                "average_score": round(row[3], 1),
                "best_score": round(row[4], 1),
                "latest_score": round(row[5], 1),
                "improvement_trend": round(row[6], 1),
                "last_drill": row[7],
                "mastery_level": self._assess_skill_level(row[3])
            })
        
        # Calculate overall stats
        if performance_data:
            overall_avg = sum(p["average_score"] for p in performance_data) / len(performance_data)
            total_drills = sum(p["drills_completed"] for p in performance_data)
            best_category = max(performance_data, key=lambda x: x["average_score"])
        else:
            overall_avg = 0
            total_drills = 0
            best_category = None
        
        return {
            "family_profile": family_profile,
            "overall_average": round(overall_avg, 1),
            "total_drills_completed": total_drills,
            "categories_trained": len(performance_data),
            "best_category": best_category,
            "performance_by_disaster": performance_data,
            "overall_mastery": self._assess_skill_level(overall_avg)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get drill system status and statistics"""
        
        # Count templates
        self.cursor.execute("SELECT COUNT(*) FROM drill_templates")
        template_count = self.cursor.fetchone()[0]
        
        # Count completed drills
        self.cursor.execute("SELECT COUNT(*) FROM drill_executions WHERE completed = 1")
        completed_drills = self.cursor.fetchone()[0]
        
        # Count family profiles
        self.cursor.execute("SELECT COUNT(*) FROM family_profiles")
        profile_count = self.cursor.fetchone()[0]
        
        # Get average performance
        self.cursor.execute("SELECT AVG(success_score) FROM drill_executions WHERE completed = 1")
        avg_performance = self.cursor.fetchone()[0] or 0
        
        return {
            "system_name": "Scenario-Based Drill Generator v3.0",
            "status": "operational",
            "drill_templates": template_count,
            "completed_drills": completed_drills,
            "family_profiles": profile_count,
            "average_performance": round(avg_performance, 1),
            "disaster_types_covered": [
                "earthquake", "fire", "hurricane", "tornado", "flood",
                "power_outage", "cyber_attack", "pandemic", "nuclear", "terrorism"
            ],
            "difficulty_levels": "1-5 (Beginner to Expert)",
            "last_updated": datetime.now().isoformat(),
            "capabilities": [
                "Custom drill generation",
                "Progressive difficulty",
                "Family-specific adaptation",
                "Performance tracking",
                "Improvement recommendations",
                "Multi-scenario coverage",
                "Safety-first design"
            ]
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Test the Scenario-Based Drill Generator"""
    
    print("🎯 Scenario-Based Drill Generator v3.0")
    print("=" * 60)
    
    # Initialize drill generator
    drill_gen = ScenarioDrillGenerator("test_scenario_drills.db")
    
    # Show available drills
    print("\n📋 Available Drill Templates:")
    templates = drill_gen.get_available_drills()
    for template in templates[:5]:
        print(f"  • {template['template_name']}")
        print(f"    Type: {template['disaster_type']}, Level: {template['difficulty_level']}")
        print(f"    Duration: {template['duration_minutes']} min, Objectives: {template['objectives_count']}")
    
    # Generate a custom drill
    print("\n🔧 Generating Custom Earthquake Drill:")
    drill_spec = drill_gen.generate_drill(
        disaster_type="earthquake",
        family_profile="Default Family",
        duration_preference=15
    )
    
    if "error" not in drill_spec:
        print(f"  Drill ID: {drill_spec['drill_id'][-8:]}")
        print(f"  Difficulty: Level {drill_spec['difficulty_level']}")
        print(f"  Duration: {drill_spec['estimated_duration']} minutes")
        print(f"  Objectives: {len(drill_spec['objectives'])}")
        print(f"  Equipment Status: {len([e for e in drill_spec['equipment_checklist'] if e['available']])}/{len(drill_spec['equipment_checklist'])} available")
        
        # Simulate drill execution
        print("\n▶️ Simulating Drill Execution:")
        execution = drill_gen.execute_drill(drill_spec['drill_id'], ["Adult 1", "Adult 2", "Teen", "Child"])
        print(f"  Status: {execution['status']}")
        print(f"  Participants: {len(execution['participants'])}")
        
        # Simulate drill completion
        print("\n✅ Simulating Drill Completion:")
        performance_scores = {
            "response_time": 85,
            "procedure_accuracy": 78,
            "family_coordination": 92,
            "resource_utilization": 80,
            "stress_management": 75
        }
        
        completion = drill_gen.complete_drill(
            drill_spec['drill_id'],
            performance_scores,
            duration_actual=18,
            notes="Family performed well with good coordination"
        )
        
        print(f"  Overall Score: {completion['overall_score']}%")
        print(f"  Skill Level: {completion['skill_level_assessment']}")
        print(f"  Time Efficiency: {completion['time_efficiency']}%")
        print(f"  Improvements: {len(completion['areas_for_improvement'])}")
    
    # Show performance history
    print("\n📈 Performance History:")
    history = drill_gen.get_performance_history("Default Family")
    print(f"  Overall Average: {history['overall_average']}%")
    print(f"  Total Drills: {history['total_drills_completed']}")
    print(f"  Categories Trained: {history['categories_trained']}")
    print(f"  Overall Mastery: {history['overall_mastery']}")
    
    # System status
    print("\n🎮 System Status:")
    status = drill_gen.get_system_status()
    print(f"  Templates: {status['drill_templates']}")
    print(f"  Completed Drills: {status['completed_drills']}")
    print(f"  Average Performance: {status['average_performance']}%")
    print(f"  Disaster Types: {len(status['disaster_types_covered'])}")
    
    drill_gen.close()
    
    # Cleanup
    import os
    if os.path.exists("test_scenario_drills.db"):
        os.remove("test_scenario_drills.db")


if __name__ == "__main__":
    main()
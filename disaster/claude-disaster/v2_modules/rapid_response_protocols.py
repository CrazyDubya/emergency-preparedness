#!/usr/bin/env python3
"""
Rapid Response Protocol System - Version 3.0
Automated response protocols with sub-5 minute activation for sudden disasters
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import threading
import time
from pathlib import Path

class RapidResponseProtocols:
    """
    Rapid response system with automated protocols for immediate
    disaster response, pre-staged actions, and emergency cache activation
    """
    
    def __init__(self, db_path: str = "rapid_response.db"):
        """Initialize the Rapid Response Protocol System"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_database()
        self._initialize_protocols()
        self.active_responses = {}
        self.response_lock = threading.Lock()
    
    def _initialize_database(self):
        """Create database tables for response protocols"""
        
        # Response protocols table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_protocols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocol_name TEXT UNIQUE NOT NULL,
                disaster_type TEXT NOT NULL,
                trigger_conditions TEXT,
                response_level INTEGER,
                activation_time_target INTEGER,
                protocol_steps TEXT,
                resource_requirements TEXT,
                success_criteria TEXT,
                dependencies TEXT,
                priority INTEGER,
                enabled INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Protocol activations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS protocol_activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocol_name TEXT NOT NULL,
                trigger_event TEXT,
                activation_time TEXT,
                completion_time TEXT,
                response_time_seconds INTEGER,
                status TEXT,
                steps_completed INTEGER,
                total_steps INTEGER,
                success_rate REAL,
                issues_encountered TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Emergency caches table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_caches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_name TEXT NOT NULL,
                cache_type TEXT NOT NULL,
                location TEXT,
                contents TEXT,
                capacity_percentage REAL,
                last_checked TEXT,
                access_method TEXT,
                activation_triggers TEXT,
                priority_level INTEGER,
                status TEXT DEFAULT 'ready',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Family notification system
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_name TEXT NOT NULL,
                relationship TEXT,
                primary_phone TEXT,
                secondary_phone TEXT,
                email TEXT,
                social_media TEXT,
                location TEXT,
                priority INTEGER,
                notification_methods TEXT,
                emergency_role TEXT,
                last_contacted TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Response checklists table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_checklists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checklist_name TEXT NOT NULL,
                disaster_type TEXT,
                time_window TEXT,
                checklist_items TEXT,
                estimated_time INTEGER,
                critical_path INTEGER DEFAULT 0,
                dependencies TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _initialize_protocols(self):
        """Initialize pre-defined response protocols"""
        
        protocols = [
            {
                "protocol_name": "Earthquake Immediate Response",
                "disaster_type": "earthquake",
                "trigger_conditions": json.dumps({
                    "magnitude": ">= 4.0",
                    "distance": "<= 50 miles",
                    "warning_time": "0 minutes"
                }),
                "response_level": 1,
                "activation_time_target": 60,  # 1 minute
                "protocol_steps": json.dumps([
                    {"step": "Drop, Cover, Hold On", "time": 0, "duration": 60},
                    {"step": "Check for injuries", "time": 60, "duration": 120},
                    {"step": "Turn off gas if safe", "time": 180, "duration": 60},
                    {"step": "Check building damage", "time": 240, "duration": 180},
                    {"step": "Locate emergency kit", "time": 420, "duration": 60},
                    {"step": "Contact family members", "time": 480, "duration": 300}
                ]),
                "resource_requirements": json.dumps([
                    "Emergency kit", "Flashlight", "First aid supplies", "Battery radio"
                ]),
                "priority": 10
            },
            {
                "protocol_name": "Fire Emergency Evacuation",
                "disaster_type": "fire",
                "trigger_conditions": json.dumps({
                    "fire_detected": True,
                    "evacuation_order": True,
                    "warning_time": "0-10 minutes"
                }),
                "response_level": 1,
                "activation_time_target": 30,  # 30 seconds
                "protocol_steps": json.dumps([
                    {"step": "Alert everyone in building", "time": 0, "duration": 30},
                    {"step": "Grab emergency bag", "time": 30, "duration": 30},
                    {"step": "Exit via primary route", "time": 60, "duration": 120},
                    {"step": "Meet at designated location", "time": 180, "duration": 60},
                    {"step": "Call 911", "time": 240, "duration": 60},
                    {"step": "Account for all persons", "time": 300, "duration": 180}
                ]),
                "resource_requirements": json.dumps([
                    "Go bags", "Important documents", "Phone chargers"
                ]),
                "priority": 10
            },
            {
                "protocol_name": "Tornado/Severe Weather Shelter",
                "disaster_type": "tornado",
                "trigger_conditions": json.dumps({
                    "tornado_warning": True,
                    "severe_weather": True,
                    "warning_time": "0-15 minutes"
                }),
                "response_level": 1,
                "activation_time_target": 120,  # 2 minutes
                "protocol_steps": json.dumps([
                    {"step": "Gather family in safe room", "time": 0, "duration": 60},
                    {"step": "Grab weather radio", "time": 60, "duration": 30},
                    {"step": "Get helmet/protection", "time": 90, "duration": 30},
                    {"step": "Monitor weather updates", "time": 120, "duration": 1800},
                    {"step": "Stay sheltered until all-clear", "time": 1920, "duration": 300}
                ]),
                "resource_requirements": json.dumps([
                    "Weather radio", "Helmets", "Blankets", "Water"
                ]),
                "priority": 9
            },
            {
                "protocol_name": "Flood/Dam Failure Evacuation",
                "disaster_type": "flood",
                "trigger_conditions": json.dumps({
                    "flood_warning": True,
                    "dam_failure": True,
                    "water_rising": True
                }),
                "response_level": 1,
                "activation_time_target": 180,  # 3 minutes
                "protocol_steps": json.dumps([
                    {"step": "Move to highest floor", "time": 0, "duration": 60},
                    {"step": "Gather emergency supplies", "time": 60, "duration": 120},
                    {"step": "Shut off utilities if time permits", "time": 180, "duration": 60},
                    {"step": "Evacuate to high ground", "time": 240, "duration": 300},
                    {"step": "Signal location if trapped", "time": 540, "duration": 600}
                ]),
                "resource_requirements": json.dumps([
                    "Life jackets", "Waterproof bags", "Signaling devices"
                ]),
                "priority": 10
            },
            {
                "protocol_name": "Power Outage Extended Response",
                "disaster_type": "power_outage",
                "trigger_conditions": json.dumps({
                    "power_out": True,
                    "duration_estimate": "> 4 hours",
                    "temperature": "extreme"
                }),
                "response_level": 2,
                "activation_time_target": 300,  # 5 minutes
                "protocol_steps": json.dumps([
                    {"step": "Unplug sensitive electronics", "time": 0, "duration": 60},
                    {"step": "Start backup generator", "time": 60, "duration": 120},
                    {"step": "Check refrigerator/freezer", "time": 180, "duration": 60},
                    {"step": "Set up alternative lighting", "time": 240, "duration": 120},
                    {"step": "Contact utility company", "time": 360, "duration": 180},
                    {"step": "Check on neighbors", "time": 540, "duration": 300}
                ]),
                "resource_requirements": json.dumps([
                    "Generator", "Fuel", "Flashlights", "Battery radio"
                ]),
                "priority": 7
            },
            {
                "protocol_name": "Cyber Attack Response",
                "disaster_type": "cyber_attack",
                "trigger_conditions": json.dumps({
                    "cyber_threat": True,
                    "system_compromise": True,
                    "banking_affected": True
                }),
                "response_level": 2,
                "activation_time_target": 180,  # 3 minutes
                "protocol_steps": json.dumps([
                    {"step": "Disconnect from internet", "time": 0, "duration": 30},
                    {"step": "Switch to offline backups", "time": 30, "duration": 120},
                    {"step": "Monitor financial accounts", "time": 150, "duration": 300},
                    {"step": "Use cash for transactions", "time": 450, "duration": 60},
                    {"step": "Change passwords", "time": 510, "duration": 600}
                ]),
                "resource_requirements": json.dumps([
                    "Offline backup drives", "Cash reserves", "Paper records"
                ]),
                "priority": 8
            },
            {
                "protocol_name": "Nuclear/Chemical Emergency",
                "disaster_type": "nuclear",
                "trigger_conditions": json.dumps({
                    "nuclear_alert": True,
                    "chemical_spill": True,
                    "radiation_detected": True
                }),
                "response_level": 1,
                "activation_time_target": 120,  # 2 minutes
                "protocol_steps": json.dumps([
                    {"step": "Shelter in place immediately", "time": 0, "duration": 60},
                    {"step": "Seal room (windows, vents)", "time": 60, "duration": 180},
                    {"step": "Turn off HVAC system", "time": 240, "duration": 60},
                    {"step": "Take potassium iodide if directed", "time": 300, "duration": 60},
                    {"step": "Monitor emergency broadcasts", "time": 360, "duration": 1800}
                ]),
                "resource_requirements": json.dumps([
                    "Plastic sheeting", "Duct tape", "Potassium iodide", "Emergency radio"
                ]),
                "priority": 10
            },
            {
                "protocol_name": "Terrorist Attack/Active Shooter",
                "disaster_type": "terrorism",
                "trigger_conditions": json.dumps({
                    "active_threat": True,
                    "violence_nearby": True,
                    "lockdown_order": True
                }),
                "response_level": 1,
                "activation_time_target": 30,  # 30 seconds
                "protocol_steps": json.dumps([
                    {"step": "Run if safe to do so", "time": 0, "duration": 60},
                    {"step": "Hide if cannot run", "time": 60, "duration": 300},
                    {"step": "Fight only as last resort", "time": 360, "duration": 300},
                    {"step": "Call 911 when safe", "time": 660, "duration": 120},
                    {"step": "Follow law enforcement orders", "time": 780, "duration": 600}
                ]),
                "resource_requirements": json.dumps([
                    "Cell phone", "Improvised barriers", "Emergency whistle"
                ]),
                "priority": 10
            },
            {
                "protocol_name": "Medical Emergency Response",
                "disaster_type": "medical",
                "trigger_conditions": json.dumps({
                    "medical_emergency": True,
                    "pandemic_alert": True,
                    "mass_casualty": True
                }),
                "response_level": 2,
                "activation_time_target": 90,  # 1.5 minutes
                "protocol_steps": json.dumps([
                    {"step": "Assess situation/triage", "time": 0, "duration": 60},
                    {"step": "Call 911/medical emergency", "time": 60, "duration": 120},
                    {"step": "Administer first aid", "time": 180, "duration": 600},
                    {"step": "Prepare for evacuation", "time": 780, "duration": 300},
                    {"step": "Document and follow up", "time": 1080, "duration": 600}
                ]),
                "resource_requirements": json.dumps([
                    "First aid kit", "AED", "Medications", "Emergency contacts"
                ]),
                "priority": 9
            },
            {
                "protocol_name": "Family Reunification",
                "disaster_type": "general",
                "trigger_conditions": json.dumps({
                    "family_separated": True,
                    "major_disaster": True,
                    "communication_disrupted": True
                }),
                "response_level": 2,
                "activation_time_target": 300,  # 5 minutes
                "protocol_steps": json.dumps([
                    {"step": "Account for immediate family", "time": 0, "duration": 180},
                    {"step": "Use family communication plan", "time": 180, "duration": 300},
                    {"step": "Contact out-of-state contact", "time": 480, "duration": 180},
                    {"step": "Go to family meeting location", "time": 660, "duration": 600},
                    {"step": "Register with Red Cross", "time": 1260, "duration": 300}
                ]),
                "resource_requirements": json.dumps([
                    "Family communication plan", "Emergency contact cards", "Transportation"
                ]),
                "priority": 8
            }
        ]
        
        # Insert protocols
        for protocol in protocols:
            self.cursor.execute('''
                INSERT OR REPLACE INTO response_protocols
                (protocol_name, disaster_type, trigger_conditions, response_level,
                 activation_time_target, protocol_steps, resource_requirements, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                protocol["protocol_name"],
                protocol["disaster_type"],
                protocol["trigger_conditions"],
                protocol["response_level"],
                protocol["activation_time_target"],
                protocol["protocol_steps"],
                protocol["resource_requirements"],
                protocol["priority"]
            ))
        
        # Initialize emergency caches
        self._initialize_emergency_caches()
        
        # Initialize notification contacts
        self._initialize_notification_system()
        
        self.conn.commit()
    
    def _initialize_emergency_caches(self):
        """Initialize emergency cache locations and contents"""
        
        caches = [
            {
                "cache_name": "Primary Emergency Kit",
                "cache_type": "survival",
                "location": "Master Bedroom Closet",
                "contents": json.dumps([
                    "Water (1 gallon per person per day - 3 days)",
                    "Non-perishable food (3 days)",
                    "First aid kit",
                    "Flashlights and batteries",
                    "Battery radio",
                    "Medications",
                    "Cash and credit cards",
                    "Important documents (copies)"
                ]),
                "capacity_percentage": 90.0,
                "access_method": "Immediate access",
                "activation_triggers": json.dumps(["any_emergency"]),
                "priority_level": 1
            },
            {
                "cache_name": "Vehicle Emergency Kit",
                "cache_type": "mobile",
                "location": "Car Trunk",
                "contents": json.dumps([
                    "Water and snacks",
                    "First aid kit",
                    "Flashlight and batteries",
                    "Emergency blanket",
                    "Multi-tool",
                    "Jumper cables",
                    "Emergency phone charger"
                ]),
                "capacity_percentage": 80.0,
                "access_method": "Vehicle access required",
                "activation_triggers": json.dumps(["evacuation", "stranded"]),
                "priority_level": 2
            },
            {
                "cache_name": "Workplace Emergency Supplies",
                "cache_type": "workplace",
                "location": "Office Desk Drawer",
                "contents": json.dumps([
                    "Energy bars",
                    "Water bottles",
                    "Basic first aid",
                    "Flashlight",
                    "Comfortable shoes",
                    "Emergency contact list"
                ]),
                "capacity_percentage": 70.0,
                "access_method": "During work hours",
                "activation_triggers": json.dumps(["workplace_emergency"]),
                "priority_level": 3
            },
            {
                "cache_name": "Extended Supply Cache",
                "cache_type": "long_term",
                "location": "Basement Storage",
                "contents": json.dumps([
                    "Extended food supply (30 days)",
                    "Water filtration system",
                    "Generator and fuel",
                    "Tools and supplies",
                    "Medical supplies",
                    "Communication equipment"
                ]),
                "capacity_percentage": 95.0,
                "access_method": "Home access required",
                "activation_triggers": json.dumps(["extended_emergency", "supply_shortage"]),
                "priority_level": 2
            },
            {
                "cache_name": "Neighborhood Resource Hub",
                "cache_type": "community",
                "location": "Community Center",
                "contents": json.dumps([
                    "Bulk emergency supplies",
                    "Communication equipment",
                    "Medical station",
                    "Tool library",
                    "Community coordination center"
                ]),
                "capacity_percentage": 60.0,
                "access_method": "Community coordination",
                "activation_triggers": json.dumps(["community_emergency", "mass_casualty"]),
                "priority_level": 4
            }
        ]
        
        for cache in caches:
            self.cursor.execute('''
                INSERT OR REPLACE INTO emergency_caches
                (cache_name, cache_type, location, contents, capacity_percentage,
                 access_method, activation_triggers, priority_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cache["cache_name"],
                cache["cache_type"],
                cache["location"],
                cache["contents"],
                cache["capacity_percentage"],
                cache["access_method"],
                cache["activation_triggers"],
                cache["priority_level"]
            ))
    
    def _initialize_notification_system(self):
        """Initialize family notification contacts"""
        
        # Sample contacts (in real use, these would be user-configured)
        contacts = [
            {
                "contact_name": "Primary Emergency Contact",
                "relationship": "spouse",
                "priority": 1,
                "notification_methods": json.dumps(["call", "text", "email"]),
                "emergency_role": "coordination"
            },
            {
                "contact_name": "Out-of-State Contact",
                "relationship": "family",
                "priority": 2,
                "notification_methods": json.dumps(["call", "email"]),
                "emergency_role": "relay_point"
            },
            {
                "contact_name": "Local Emergency Contact",
                "relationship": "neighbor",
                "priority": 3,
                "notification_methods": json.dumps(["call", "text"]),
                "emergency_role": "local_check"
            },
            {
                "contact_name": "Workplace Emergency",
                "relationship": "workplace",
                "priority": 4,
                "notification_methods": json.dumps(["call", "email"]),
                "emergency_role": "workplace_coord"
            },
            {
                "contact_name": "Children's School",
                "relationship": "school",
                "priority": 2,
                "notification_methods": json.dumps(["call"]),
                "emergency_role": "child_safety"
            }
        ]
        
        for contact in contacts:
            self.cursor.execute('''
                INSERT OR REPLACE INTO notification_contacts
                (contact_name, relationship, priority, notification_methods, emergency_role)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                contact["contact_name"],
                contact["relationship"],
                contact["priority"],
                contact["notification_methods"],
                contact["emergency_role"]
            ))
    
    def activate_protocol(self, protocol_name: str, trigger_event: str = None) -> Dict[str, Any]:
        """
        Activate a rapid response protocol
        
        Args:
            protocol_name: Name of protocol to activate
            trigger_event: Description of triggering event
            
        Returns:
            Protocol activation details
        """
        
        activation_time = datetime.now()
        
        # Get protocol details
        self.cursor.execute('''
            SELECT * FROM response_protocols WHERE protocol_name = ? AND enabled = 1
        ''', (protocol_name,))
        
        protocol_row = self.cursor.fetchone()
        if not protocol_row:
            return {"error": f"Protocol '{protocol_name}' not found or disabled"}
        
        protocol = {
            "name": protocol_row[1],
            "disaster_type": protocol_row[2],
            "response_level": protocol_row[4],
            "target_time": protocol_row[5],
            "steps": json.loads(protocol_row[6]),
            "resources": json.loads(protocol_row[7])
        }
        
        # Create activation record
        activation_id = f"{protocol_name}_{activation_time.timestamp()}"
        
        with self.response_lock:
            self.active_responses[activation_id] = {
                "protocol": protocol,
                "activation_time": activation_time,
                "trigger_event": trigger_event,
                "status": "activated",
                "current_step": 0,
                "completed_steps": [],
                "remaining_steps": protocol["steps"].copy(),
                "issues": []
            }
        
        # Log activation
        self.cursor.execute('''
            INSERT INTO protocol_activations
            (protocol_name, trigger_event, activation_time, status, total_steps)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            protocol_name,
            trigger_event,
            activation_time.isoformat(),
            "activated",
            len(protocol["steps"])
        ))
        
        self.conn.commit()
        
        # Auto-activate emergency caches if applicable
        activated_caches = self._activate_emergency_caches(protocol["disaster_type"])
        
        # Send notifications
        notifications_sent = self._send_emergency_notifications(protocol, trigger_event)
        
        return {
            "activation_id": activation_id,
            "protocol_name": protocol_name,
            "activation_time": activation_time.isoformat(),
            "target_completion_time": (activation_time + timedelta(seconds=protocol["target_time"])).isoformat(),
            "total_steps": len(protocol["steps"]),
            "activated_caches": activated_caches,
            "notifications_sent": notifications_sent,
            "status": "activated",
            "next_action": self._get_next_action(activation_id)
        }
    
    def _activate_emergency_caches(self, disaster_type: str) -> List[str]:
        """Activate relevant emergency caches for disaster type"""
        
        activated = []
        
        # Get caches that should be activated
        self.cursor.execute('''
            SELECT cache_name, activation_triggers FROM emergency_caches
            WHERE status = 'ready'
        ''')
        
        for cache_name, triggers_json in self.cursor.fetchall():
            triggers = json.loads(triggers_json)
            
            if "any_emergency" in triggers or disaster_type in triggers:
                # Mark cache as activated
                self.cursor.execute('''
                    UPDATE emergency_caches
                    SET status = 'activated', last_checked = ?
                    WHERE cache_name = ?
                ''', (datetime.now().isoformat(), cache_name))
                
                activated.append(cache_name)
        
        self.conn.commit()
        return activated
    
    def _send_emergency_notifications(self, protocol: Dict[str, Any], 
                                    trigger_event: str) -> List[str]:
        """Send emergency notifications to contacts"""
        
        sent = []
        
        # Get priority contacts
        self.cursor.execute('''
            SELECT contact_name, notification_methods, emergency_role
            FROM notification_contacts
            ORDER BY priority
        ''')
        
        for contact_name, methods_json, role in self.cursor.fetchall()[:3]:
            methods = json.loads(methods_json)
            
            # Simulate sending notifications
            message = f"EMERGENCY: {protocol['name']} activated. {trigger_event or 'Emergency response in progress.'}"
            
            for method in methods:
                # In production, this would send actual notifications
                sent.append(f"{contact_name} via {method}")
                
                # Update last contacted
                self.cursor.execute('''
                    UPDATE notification_contacts
                    SET last_contacted = ?
                    WHERE contact_name = ?
                ''', (datetime.now().isoformat(), contact_name))
        
        self.conn.commit()
        return sent
    
    def _get_next_action(self, activation_id: str) -> Dict[str, Any]:
        """Get next action for an active protocol"""
        
        if activation_id not in self.active_responses:
            return {"error": "Activation not found"}
        
        response = self.active_responses[activation_id]
        
        if response["current_step"] >= len(response["protocol"]["steps"]):
            return {"action": "Protocol complete", "status": "completed"}
        
        current_step = response["protocol"]["steps"][response["current_step"]]
        activation_time = response["activation_time"]
        step_start_time = activation_time + timedelta(seconds=current_step["time"])
        
        return {
            "step_number": response["current_step"] + 1,
            "action": current_step["step"],
            "start_time": step_start_time.isoformat(),
            "duration_seconds": current_step["duration"],
            "status": "pending" if datetime.now() < step_start_time else "active"
        }
    
    def complete_step(self, activation_id: str, step_number: int, 
                     success: bool = True, notes: str = None) -> Dict[str, Any]:
        """
        Mark a protocol step as completed
        
        Args:
            activation_id: Protocol activation ID
            step_number: Step number (1-based)
            success: Whether step completed successfully
            notes: Optional completion notes
            
        Returns:
            Updated protocol status
        """
        
        if activation_id not in self.active_responses:
            return {"error": "Activation not found"}
        
        response = self.active_responses[activation_id]
        step_index = step_number - 1
        
        if step_index >= len(response["protocol"]["steps"]):
            return {"error": "Invalid step number"}
        
        with self.response_lock:
            # Mark step as completed
            step = response["protocol"]["steps"][step_index]
            completion_record = {
                "step_number": step_number,
                "action": step["step"],
                "completed_at": datetime.now().isoformat(),
                "success": success,
                "notes": notes
            }
            
            response["completed_steps"].append(completion_record)
            response["current_step"] = max(response["current_step"], step_number)
            
            if not success and notes:
                response["issues"].append(f"Step {step_number}: {notes}")
            
            # Check if protocol is complete
            if response["current_step"] >= len(response["protocol"]["steps"]):
                response["status"] = "completed"
                response["completion_time"] = datetime.now()
                
                # Update database
                response_time = (response["completion_time"] - response["activation_time"]).total_seconds()
                success_rate = len([s for s in response["completed_steps"] if s["success"]]) / len(response["completed_steps"])
                
                self.cursor.execute('''
                    UPDATE protocol_activations
                    SET completion_time = ?, response_time_seconds = ?, status = ?,
                        steps_completed = ?, success_rate = ?
                    WHERE protocol_name = ? AND activation_time = ?
                ''', (
                    response["completion_time"].isoformat(),
                    int(response_time),
                    "completed",
                    len(response["completed_steps"]),
                    success_rate,
                    response["protocol"]["name"],
                    response["activation_time"].isoformat()
                ))
                
                self.conn.commit()
        
        return {
            "activation_id": activation_id,
            "step_completed": step_number,
            "total_steps": len(response["protocol"]["steps"]),
            "protocol_status": response["status"],
            "success_rate": len([s for s in response["completed_steps"] if s["success"]]) / len(response["completed_steps"]),
            "next_action": self._get_next_action(activation_id) if response["status"] != "completed" else None
        }
    
    def get_protocol_status(self, activation_id: str) -> Dict[str, Any]:
        """Get current status of an active protocol"""
        
        if activation_id not in self.active_responses:
            return {"error": "Activation not found"}
        
        response = self.active_responses[activation_id]
        current_time = datetime.now()
        elapsed_time = (current_time - response["activation_time"]).total_seconds()
        
        return {
            "activation_id": activation_id,
            "protocol_name": response["protocol"]["name"],
            "status": response["status"],
            "activation_time": response["activation_time"].isoformat(),
            "elapsed_time_seconds": int(elapsed_time),
            "target_time_seconds": response["protocol"]["target_time"],
            "on_schedule": elapsed_time <= response["protocol"]["target_time"],
            "current_step": response["current_step"],
            "total_steps": len(response["protocol"]["steps"]),
            "completed_steps": len(response["completed_steps"]),
            "success_rate": len([s for s in response["completed_steps"] if s["success"]]) / max(1, len(response["completed_steps"])),
            "issues": response["issues"],
            "next_action": self._get_next_action(activation_id)
        }
    
    def get_available_protocols(self, disaster_type: str = None) -> List[Dict[str, Any]]:
        """Get list of available protocols, optionally filtered by disaster type"""
        
        query = "SELECT * FROM response_protocols WHERE enabled = 1"
        params = []
        
        if disaster_type:
            query += " AND disaster_type = ?"
            params.append(disaster_type)
        
        query += " ORDER BY priority DESC, activation_time_target ASC"
        
        self.cursor.execute(query, params)
        
        protocols = []
        for row in self.cursor.fetchall():
            protocols.append({
                "name": row[1],
                "disaster_type": row[2],
                "response_level": row[4],
                "target_time_minutes": row[5] / 60,
                "priority": row[10],
                "steps_count": len(json.loads(row[6])),
                "description": f"Level {row[4]} response for {row[2]} disasters"
            })
        
        return protocols
    
    def get_emergency_caches(self, cache_type: str = None) -> List[Dict[str, Any]]:
        """Get list of emergency caches"""
        
        query = "SELECT * FROM emergency_caches"
        params = []
        
        if cache_type:
            query += " WHERE cache_type = ?"
            params.append(cache_type)
        
        query += " ORDER BY priority_level, capacity_percentage DESC"
        
        self.cursor.execute(query, params)
        
        caches = []
        for row in self.cursor.fetchall():
            caches.append({
                "name": row[1],
                "type": row[2],
                "location": row[3],
                "capacity": f"{row[5]:.0f}%",
                "status": row[10],
                "priority": row[9],
                "contents_count": len(json.loads(row[4]))
            })
        
        return caches
    
    def check_cache_status(self, cache_name: str) -> Dict[str, Any]:
        """Check status and contents of a specific cache"""
        
        self.cursor.execute('''
            SELECT * FROM emergency_caches WHERE cache_name = ?
        ''', (cache_name,))
        
        cache_row = self.cursor.fetchone()
        if not cache_row:
            return {"error": f"Cache '{cache_name}' not found"}
        
        contents = json.loads(cache_row[4])
        
        return {
            "name": cache_row[1],
            "type": cache_row[2],
            "location": cache_row[3],
            "contents": contents,
            "capacity_percentage": cache_row[5],
            "last_checked": cache_row[6],
            "access_method": cache_row[7],
            "status": cache_row[10],
            "ready_for_activation": cache_row[10] == "ready" and cache_row[5] > 50
        }
    
    def generate_response_timeline(self, protocol_name: str) -> List[Dict[str, Any]]:
        """Generate detailed response timeline for a protocol"""
        
        self.cursor.execute('''
            SELECT protocol_steps FROM response_protocols WHERE protocol_name = ?
        ''', (protocol_name,))
        
        result = self.cursor.fetchone()
        if not result:
            return []
        
        steps = json.loads(result[0])
        timeline = []
        
        for i, step in enumerate(steps):
            start_time = step["time"]
            end_time = start_time + step["duration"]
            
            timeline.append({
                "step_number": i + 1,
                "action": step["step"],
                "start_time_seconds": start_time,
                "duration_seconds": step["duration"],
                "end_time_seconds": end_time,
                "start_time_display": f"T+{start_time//60:02d}:{start_time%60:02d}",
                "duration_display": f"{step['duration']//60}min {step['duration']%60}sec",
                "urgency": "CRITICAL" if start_time < 300 else "HIGH" if start_time < 900 else "MODERATE"
            })
        
        return timeline
    
    def test_protocol(self, protocol_name: str) -> Dict[str, Any]:
        """Test a protocol without full activation"""
        
        self.cursor.execute('''
            SELECT * FROM response_protocols WHERE protocol_name = ?
        ''', (protocol_name,))
        
        protocol_row = self.cursor.fetchone()
        if not protocol_row:
            return {"error": f"Protocol '{protocol_name}' not found"}
        
        steps = json.loads(protocol_row[6])
        resources = json.loads(protocol_row[7])
        
        # Check resource availability (simulated)
        resource_check = []
        for resource in resources:
            available = True  # In production, this would check actual availability
            resource_check.append({
                "resource": resource,
                "available": available,
                "status": "✅ Available" if available else "❌ Missing"
            })
        
        # Estimate completion time
        total_time = max(step["time"] + step["duration"] for step in steps)
        target_time = protocol_row[5]
        
        return {
            "protocol_name": protocol_name,
            "disaster_type": protocol_row[2],
            "total_steps": len(steps),
            "estimated_completion_time": total_time,
            "target_time": target_time,
            "time_assessment": "On target" if total_time <= target_time else f"Over by {total_time - target_time} seconds",
            "resource_availability": resource_check,
            "readiness_score": sum(1 for r in resource_check if r["available"]) / len(resource_check) * 100,
            "test_status": "Ready for activation" if all(r["available"] for r in resource_check) else "Missing resources"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        
        # Count protocols
        self.cursor.execute("SELECT COUNT(*) FROM response_protocols WHERE enabled = 1")
        active_protocols = self.cursor.fetchone()[0]
        
        # Count caches
        self.cursor.execute("SELECT COUNT(*) FROM emergency_caches WHERE status = 'ready'")
        ready_caches = self.cursor.fetchone()[0]
        
        # Count contacts
        self.cursor.execute("SELECT COUNT(*) FROM notification_contacts")
        notification_contacts = self.cursor.fetchone()[0]
        
        # Recent activations
        self.cursor.execute('''
            SELECT COUNT(*) FROM protocol_activations
            WHERE datetime(activation_time) > datetime('now', '-24 hours')
        ''')
        recent_activations = self.cursor.fetchone()[0]
        
        return {
            "system_name": "Rapid Response Protocol System v3.0",
            "status": "operational",
            "active_protocols": active_protocols,
            "ready_caches": ready_caches,
            "notification_contacts": notification_contacts,
            "active_responses": len(self.active_responses),
            "recent_activations_24h": recent_activations,
            "average_response_time": self._get_average_response_time(),
            "last_updated": datetime.now().isoformat(),
            "capabilities": [
                "Sub-5 minute activation",
                "Automated cache activation",
                "Family notification system",
                "Real-time progress tracking",
                "Multi-disaster protocols",
                "Resource verification",
                "Performance analytics"
            ]
        }
    
    def _get_average_response_time(self) -> Optional[float]:
        """Calculate average response time for completed protocols"""
        
        self.cursor.execute('''
            SELECT AVG(response_time_seconds) FROM protocol_activations
            WHERE status = 'completed' AND response_time_seconds IS NOT NULL
        ''')
        
        result = self.cursor.fetchone()[0]
        return result if result else None
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Test the Rapid Response Protocol System"""
    
    print("⚡ Rapid Response Protocol System v3.0")
    print("=" * 60)
    
    # Initialize system
    response_system = RapidResponseProtocols("test_rapid_response.db")
    
    # Show available protocols
    print("\n📋 Available Protocols:")
    protocols = response_system.get_available_protocols()
    for protocol in protocols[:5]:
        print(f"  • {protocol['name']} ({protocol['disaster_type']})")
        print(f"    Target Time: {protocol['target_time_minutes']:.1f} minutes, Steps: {protocol['steps_count']}")
    
    # Test a protocol
    print("\n🧪 Testing Earthquake Protocol:")
    test_result = response_system.test_protocol("Earthquake Immediate Response")
    print(f"  Readiness Score: {test_result.get('readiness_score', 0):.0f}%")
    print(f"  Status: {test_result.get('test_status', 'Unknown')}")
    
    # Simulate activation
    print("\n🚨 Simulating Protocol Activation:")
    activation = response_system.activate_protocol(
        "Fire Emergency Evacuation",
        "Smoke detected in kitchen"
    )
    
    if "error" not in activation:
        print(f"  Activation ID: {activation['activation_id'][-8:]}")
        print(f"  Target Completion: {activation['target_completion_time']}")
        print(f"  Caches Activated: {len(activation['activated_caches'])}")
        print(f"  Notifications Sent: {len(activation['notifications_sent'])}")
        
        # Check next action
        next_action = activation['next_action']
        print(f"  Next Action: {next_action.get('action', 'Unknown')}")
        
        # Simulate completing first step
        completion = response_system.complete_step(
            activation['activation_id'], 
            1, 
            success=True, 
            notes="All occupants alerted"
        )
        print(f"  Step 1 Completed: {completion.get('success_rate', 0)*100:.0f}% success rate")
    
    # Show emergency caches
    print("\n📦 Emergency Caches:")
    caches = response_system.get_emergency_caches()
    for cache in caches[:3]:
        print(f"  • {cache['name']} ({cache['type']})")
        print(f"    Location: {cache['location']}, Capacity: {cache['capacity']}")
    
    # System status
    print("\n✅ System Status:")
    status = response_system.get_system_status()
    print(f"  Active Protocols: {status['active_protocols']}")
    print(f"  Ready Caches: {status['ready_caches']}")
    print(f"  Notification Contacts: {status['notification_contacts']}")
    print(f"  Active Responses: {status['active_responses']}")
    
    response_system.close()
    
    # Cleanup
    import os
    if os.path.exists("test_rapid_response.db"):
        os.remove("test_rapid_response.db")


if __name__ == "__main__":
    main()
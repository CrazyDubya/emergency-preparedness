#!/usr/bin/env python3
"""
Multi-Source Alert Aggregator - Version 3.0
Comprehensive alert monitoring from multiple sources with intelligent prioritization
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import threading
import time
from pathlib import Path

class MultiSourceAlertAggregator:
    """
    Advanced alert aggregation system that monitors multiple sources,
    prioritizes alerts, and provides real-time emergency notifications
    """
    
    def __init__(self, db_path: str = "alert_aggregator.db"):
        """Initialize the Multi-Source Alert Aggregator"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_database()
        self._initialize_alert_sources()
        self.active_alerts = []
        self.alert_history = []
        self.monitoring_active = False
    
    def _initialize_database(self):
        """Create database tables for alert management"""
        
        # Alert sources configuration
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT UNIQUE NOT NULL,
                source_type TEXT NOT NULL,
                api_endpoint TEXT,
                update_frequency INTEGER,
                reliability_score REAL,
                last_check TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Active alerts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                location TEXT,
                effective_time TEXT,
                expiry_time TEXT,
                priority_score REAL,
                action_required TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                acknowledged INTEGER DEFAULT 0
            )
        ''')
        
        # Alert history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id TEXT NOT NULL,
                source TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity INTEGER,
                title TEXT NOT NULL,
                received_at TEXT,
                expired_at TEXT,
                response_time INTEGER,
                action_taken TEXT,
                outcome TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alert rules and thresholds
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT UNIQUE NOT NULL,
                alert_type TEXT,
                condition TEXT,
                threshold_value REAL,
                action TEXT,
                priority_modifier REAL,
                enabled INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alert subscriptions for notifications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_name TEXT NOT NULL,
                contact_method TEXT NOT NULL,
                contact_details TEXT NOT NULL,
                alert_types TEXT,
                severity_threshold INTEGER,
                location_filter TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _initialize_alert_sources(self):
        """Initialize and configure alert sources"""
        
        # Define alert sources (in production, these would be real API endpoints)
        alert_sources = [
            {
                "source_name": "NOAA Weather Service",
                "source_type": "weather",
                "api_endpoint": "https://api.weather.gov/alerts/active",
                "update_frequency": 300,  # 5 minutes
                "reliability_score": 0.95
            },
            {
                "source_name": "USGS Earthquake Monitor",
                "source_type": "seismic",
                "api_endpoint": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson",
                "update_frequency": 60,  # 1 minute
                "reliability_score": 0.98
            },
            {
                "source_name": "Local Emergency Management",
                "source_type": "local",
                "api_endpoint": "local_emergency_api",
                "update_frequency": 180,  # 3 minutes
                "reliability_score": 0.90
            },
            {
                "source_name": "Social Media Disaster Detection",
                "source_type": "social",
                "api_endpoint": "twitter_disaster_api",
                "update_frequency": 120,  # 2 minutes
                "reliability_score": 0.70
            },
            {
                "source_name": "Fire Department Scanner",
                "source_type": "fire",
                "api_endpoint": "fire_scanner_api",
                "update_frequency": 30,  # 30 seconds
                "reliability_score": 0.85
            },
            {
                "source_name": "Power Grid Monitor",
                "source_type": "utility",
                "api_endpoint": "power_grid_api",
                "update_frequency": 600,  # 10 minutes
                "reliability_score": 0.88
            },
            {
                "source_name": "CDC Health Alerts",
                "source_type": "health",
                "api_endpoint": "https://emergency.cdc.gov/han/",
                "update_frequency": 3600,  # 1 hour
                "reliability_score": 0.92
            },
            {
                "source_name": "Cyber Threat Intelligence",
                "source_type": "cyber",
                "api_endpoint": "cisa_threat_api",
                "update_frequency": 900,  # 15 minutes
                "reliability_score": 0.87
            },
            {
                "source_name": "Traffic and Transportation",
                "source_type": "transport",
                "api_endpoint": "traffic_api",
                "update_frequency": 300,  # 5 minutes
                "reliability_score": 0.82
            },
            {
                "source_name": "Air Quality Monitor",
                "source_type": "environmental",
                "api_endpoint": "airnow_api",
                "update_frequency": 1800,  # 30 minutes
                "reliability_score": 0.89
            }
        ]
        
        # Insert or update sources
        for source in alert_sources:
            self.cursor.execute('''
                INSERT OR REPLACE INTO alert_sources
                (source_name, source_type, api_endpoint, update_frequency, reliability_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (source["source_name"], source["source_type"], source["api_endpoint"],
                 source["update_frequency"], source["reliability_score"]))
        
        self.conn.commit()
    
    def fetch_alerts_from_source(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch alerts from a specific source
        
        Args:
            source: Source configuration dictionary
            
        Returns:
            List of alerts from the source
        """
        
        # In production, this would make actual API calls
        # For testing, simulate alerts based on source type
        
        alerts = []
        source_type = source["source_type"]
        
        # Simulate different alert types based on source
        if source_type == "weather":
            if random.random() < 0.3:  # 30% chance of weather alert
                alerts.append({
                    "id": f"WX-{datetime.now().timestamp()}",
                    "type": random.choice(["tornado", "thunderstorm", "flood", "winter_storm"]),
                    "severity": random.randint(3, 8),
                    "title": "Severe Weather Warning",
                    "description": "Severe weather conditions expected in your area",
                    "location": "Local Area",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=random.randint(2, 12))).isoformat()
                })
        
        elif source_type == "seismic":
            if random.random() < 0.05:  # 5% chance of earthquake alert
                magnitude = round(random.uniform(3.0, 7.5), 1)
                alerts.append({
                    "id": f"EQ-{datetime.now().timestamp()}",
                    "type": "earthquake",
                    "severity": min(10, int(magnitude * 1.3)),
                    "title": f"Earthquake Alert: M{magnitude}",
                    "description": f"Magnitude {magnitude} earthquake detected",
                    "location": f"{random.randint(10, 100)} miles away",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=1)).isoformat()
                })
        
        elif source_type == "local":
            if random.random() < 0.15:  # 15% chance of local alert
                alerts.append({
                    "id": f"LOCAL-{datetime.now().timestamp()}",
                    "type": random.choice(["evacuation", "shelter", "road_closure", "boil_water"]),
                    "severity": random.randint(4, 7),
                    "title": "Local Emergency Alert",
                    "description": "Local authorities have issued an emergency alert",
                    "location": "Your County",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=random.randint(4, 24))).isoformat()
                })
        
        elif source_type == "fire":
            if random.random() < 0.1:  # 10% chance of fire alert
                alerts.append({
                    "id": f"FIRE-{datetime.now().timestamp()}",
                    "type": "fire",
                    "severity": random.randint(5, 9),
                    "title": "Fire Emergency",
                    "description": "Active fire reported in area",
                    "location": f"{random.randint(1, 10)} miles away",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=random.randint(1, 6))).isoformat()
                })
        
        elif source_type == "utility":
            if random.random() < 0.2:  # 20% chance of utility alert
                alerts.append({
                    "id": f"UTIL-{datetime.now().timestamp()}",
                    "type": "power_outage",
                    "severity": random.randint(3, 6),
                    "title": "Power Outage Alert",
                    "description": f"Power outage affecting {random.randint(100, 10000)} customers",
                    "location": "Service Area",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=random.randint(2, 8))).isoformat()
                })
        
        elif source_type == "cyber":
            if random.random() < 0.08:  # 8% chance of cyber alert
                alerts.append({
                    "id": f"CYBER-{datetime.now().timestamp()}",
                    "type": "cyber_threat",
                    "severity": random.randint(4, 8),
                    "title": "Cyber Security Alert",
                    "description": "Active cyber threat detected",
                    "location": "Digital Infrastructure",
                    "effective": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=random.randint(12, 48))).isoformat()
                })
        
        return alerts
    
    def calculate_priority_score(self, alert: Dict[str, Any], source_reliability: float) -> float:
        """
        Calculate priority score for an alert based on multiple factors
        
        Args:
            alert: Alert dictionary
            source_reliability: Reliability score of the source
            
        Returns:
            Priority score (0-100)
        """
        
        # Base priority from severity
        severity = alert.get("severity", 5)
        base_priority = severity * 10
        
        # Adjust for source reliability
        reliability_factor = source_reliability
        
        # Time sensitivity factor
        expires = alert.get("expires")
        time_factor = 1.0
        if expires:
            try:
                expiry_time = datetime.fromisoformat(expires)
                time_remaining = (expiry_time - datetime.now()).total_seconds() / 3600
                if time_remaining < 1:
                    time_factor = 2.0  # Double priority for alerts expiring soon
                elif time_remaining < 6:
                    time_factor = 1.5
                elif time_remaining < 24:
                    time_factor = 1.2
            except:
                pass
        
        # Location proximity factor (simulated)
        location = alert.get("location", "")
        proximity_factor = 1.0
        if "miles away" in location:
            try:
                miles = int(location.split()[0])
                if miles < 5:
                    proximity_factor = 1.5
                elif miles < 10:
                    proximity_factor = 1.3
                elif miles < 25:
                    proximity_factor = 1.1
            except:
                pass
        
        # Alert type criticality
        alert_type = alert.get("type", "")
        type_multipliers = {
            "earthquake": 1.8,
            "tornado": 1.7,
            "fire": 1.6,
            "evacuation": 1.5,
            "flood": 1.4,
            "cyber_threat": 1.3,
            "power_outage": 1.1,
            "road_closure": 0.9
        }
        type_factor = type_multipliers.get(alert_type, 1.0)
        
        # Calculate final priority
        priority = base_priority * reliability_factor * time_factor * proximity_factor * type_factor
        
        return min(100, priority)
    
    def process_alert(self, alert: Dict[str, Any], source: Dict[str, Any]) -> bool:
        """
        Process and store a new alert
        
        Args:
            alert: Alert data
            source: Source information
            
        Returns:
            Success status
        """
        
        try:
            # Calculate priority
            priority = self.calculate_priority_score(alert, source["reliability_score"])
            
            # Determine action required
            action_required = self._determine_action(alert, priority)
            
            # Store alert
            self.cursor.execute('''
                INSERT OR REPLACE INTO active_alerts
                (alert_id, source, alert_type, severity, title, description,
                 location, effective_time, expiry_time, priority_score, action_required, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert["id"],
                source["source_name"],
                alert["type"],
                alert["severity"],
                alert["title"],
                alert.get("description", ""),
                alert.get("location", ""),
                alert.get("effective", ""),
                alert.get("expires", ""),
                priority,
                action_required,
                json.dumps(alert)
            ))
            
            self.conn.commit()
            
            # Add to active alerts list
            self.active_alerts.append({
                "alert_id": alert["id"],
                "source": source["source_name"],
                "priority": priority,
                "action": action_required,
                "alert": alert
            })
            
            return True
            
        except Exception as e:
            print(f"Error processing alert: {e}")
            return False
    
    def _determine_action(self, alert: Dict[str, Any], priority: float) -> str:
        """Determine required action based on alert and priority"""
        
        alert_type = alert.get("type", "")
        severity = alert.get("severity", 5)
        
        # Critical actions (priority > 80)
        if priority > 80:
            if alert_type in ["earthquake", "tornado", "fire"]:
                return "EVACUATE IMMEDIATELY"
            elif alert_type == "evacuation":
                return "EVACUATE AS DIRECTED"
            elif alert_type == "flood":
                return "MOVE TO HIGH GROUND"
            else:
                return "TAKE IMMEDIATE ACTION"
        
        # High priority actions (priority 60-80)
        elif priority > 60:
            if alert_type == "power_outage":
                return "PREPARE BACKUP POWER"
            elif alert_type == "cyber_threat":
                return "SECURE DIGITAL ASSETS"
            elif alert_type in ["thunderstorm", "winter_storm"]:
                return "SHELTER IN PLACE"
            else:
                return "PREPARE FOR IMPACT"
        
        # Moderate priority actions (priority 40-60)
        elif priority > 40:
            return "MONITOR SITUATION"
        
        # Low priority actions
        else:
            return "STAY INFORMED"
    
    def aggregate_alerts(self) -> Dict[str, Any]:
        """
        Aggregate alerts from all sources and prioritize
        
        Returns:
            Aggregated alert summary
        """
        
        # Get all active sources
        self.cursor.execute('''
            SELECT * FROM alert_sources WHERE status = 'active'
        ''')
        sources = self.cursor.fetchall()
        
        new_alerts = []
        
        for source_row in sources:
            source = {
                "source_name": source_row[1],
                "source_type": source_row[2],
                "api_endpoint": source_row[3],
                "update_frequency": source_row[4],
                "reliability_score": source_row[5]
            }
            
            # Check if update is needed
            last_check = source_row[6]
            if last_check:
                try:
                    last_check_time = datetime.fromisoformat(last_check)
                    if (datetime.now() - last_check_time).total_seconds() < source["update_frequency"]:
                        continue  # Skip if recently checked
                except:
                    pass
            
            # Fetch alerts from source
            alerts = self.fetch_alerts_from_source(source)
            
            # Process each alert
            for alert in alerts:
                if self.process_alert(alert, source):
                    new_alerts.append(alert)
            
            # Update last check time
            self.cursor.execute('''
                UPDATE alert_sources SET last_check = ? WHERE source_name = ?
            ''', (datetime.now().isoformat(), source["source_name"]))
        
        self.conn.commit()
        
        # Clean expired alerts
        self._clean_expired_alerts()
        
        # Get current active alerts
        self.cursor.execute('''
            SELECT * FROM active_alerts 
            WHERE acknowledged = 0
            ORDER BY priority_score DESC
        ''')
        active_alerts = self.cursor.fetchall()
        
        # Prepare summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_active_alerts": len(active_alerts),
            "new_alerts": len(new_alerts),
            "critical_alerts": [],
            "high_priority_alerts": [],
            "moderate_alerts": [],
            "low_priority_alerts": [],
            "by_type": {},
            "required_actions": []
        }
        
        # Categorize alerts
        for alert_row in active_alerts:
            alert_data = {
                "id": alert_row[1],
                "source": alert_row[2],
                "type": alert_row[3],
                "severity": alert_row[4],
                "title": alert_row[5],
                "priority": alert_row[10],
                "action": alert_row[11]
            }
            
            # Categorize by priority
            if alert_data["priority"] > 80:
                summary["critical_alerts"].append(alert_data)
            elif alert_data["priority"] > 60:
                summary["high_priority_alerts"].append(alert_data)
            elif alert_data["priority"] > 40:
                summary["moderate_alerts"].append(alert_data)
            else:
                summary["low_priority_alerts"].append(alert_data)
            
            # Count by type
            alert_type = alert_data["type"]
            if alert_type not in summary["by_type"]:
                summary["by_type"][alert_type] = 0
            summary["by_type"][alert_type] += 1
            
            # Collect unique actions
            if alert_data["action"] not in summary["required_actions"]:
                summary["required_actions"].append(alert_data["action"])
        
        # Sort required actions by urgency
        action_order = [
            "EVACUATE IMMEDIATELY",
            "EVACUATE AS DIRECTED",
            "MOVE TO HIGH GROUND",
            "TAKE IMMEDIATE ACTION",
            "SHELTER IN PLACE",
            "PREPARE BACKUP POWER",
            "SECURE DIGITAL ASSETS",
            "PREPARE FOR IMPACT",
            "MONITOR SITUATION",
            "STAY INFORMED"
        ]
        
        summary["required_actions"].sort(
            key=lambda x: action_order.index(x) if x in action_order else 999
        )
        
        return summary
    
    def _clean_expired_alerts(self):
        """Move expired alerts to history"""
        
        # Find expired alerts
        self.cursor.execute('''
            SELECT * FROM active_alerts
            WHERE expiry_time < ? AND expiry_time != ''
        ''', (datetime.now().isoformat(),))
        
        expired = self.cursor.fetchall()
        
        for alert in expired:
            # Move to history
            self.cursor.execute('''
                INSERT INTO alert_history
                (alert_id, source, alert_type, severity, title, received_at, expired_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (alert[1], alert[2], alert[3], alert[4], alert[5], alert[13], datetime.now().isoformat()))
            
            # Remove from active
            self.cursor.execute('''
                DELETE FROM active_alerts WHERE alert_id = ?
            ''', (alert[1],))
        
        self.conn.commit()
    
    def get_alert_by_location(self, location: str) -> List[Dict[str, Any]]:
        """Get alerts relevant to a specific location"""
        
        self.cursor.execute('''
            SELECT * FROM active_alerts
            WHERE location LIKE ? OR location = 'National' OR location = 'Global'
            ORDER BY priority_score DESC
        ''', (f'%{location}%',))
        
        alerts = []
        for row in self.cursor.fetchall():
            alerts.append({
                "id": row[1],
                "type": row[3],
                "severity": row[4],
                "title": row[5],
                "description": row[6],
                "priority": row[10],
                "action": row[11]
            })
        
        return alerts
    
    def get_alert_timeline(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get timeline of alerts for specified hours"""
        
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        self.cursor.execute('''
            SELECT alert_id, source, alert_type, severity, title, created_at
            FROM active_alerts
            WHERE created_at > ?
            UNION ALL
            SELECT alert_id, source, alert_type, severity, title, received_at
            FROM alert_history
            WHERE received_at > ?
            ORDER BY created_at DESC
        ''', (cutoff_time, cutoff_time))
        
        timeline = []
        for row in self.cursor.fetchall():
            timeline.append({
                "id": row[0],
                "source": row[1],
                "type": row[2],
                "severity": row[3],
                "title": row[4],
                "time": row[5]
            })
        
        return timeline
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark an alert as acknowledged"""
        
        try:
            self.cursor.execute('''
                UPDATE active_alerts
                SET acknowledged = 1
                WHERE alert_id = ?
            ''', (alert_id,))
            
            self.conn.commit()
            return True
        except:
            return False
    
    def subscribe_to_alerts(self, contact_name: str, contact_method: str,
                          contact_details: str, alert_types: List[str] = None,
                          severity_threshold: int = 5) -> bool:
        """
        Subscribe to alert notifications
        
        Args:
            contact_name: Name of contact
            contact_method: Method (email, sms, push)
            contact_details: Contact details
            alert_types: List of alert types to subscribe to
            severity_threshold: Minimum severity for notifications
            
        Returns:
            Success status
        """
        
        try:
            alert_types_str = json.dumps(alert_types) if alert_types else "all"
            
            self.cursor.execute('''
                INSERT INTO alert_subscriptions
                (contact_name, contact_method, contact_details, alert_types, severity_threshold)
                VALUES (?, ?, ?, ?, ?)
            ''', (contact_name, contact_method, contact_details, alert_types_str, severity_threshold))
            
            self.conn.commit()
            return True
        except:
            return False
    
    def get_notification_list(self, alert: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get list of subscribers to notify for an alert"""
        
        self.cursor.execute('''
            SELECT * FROM alert_subscriptions
            WHERE active = 1 AND severity_threshold <= ?
        ''', (alert.get("severity", 5),))
        
        notifications = []
        for row in self.cursor.fetchall():
            # Check if alert type matches subscription
            alert_types = json.loads(row[4]) if row[4] != "all" else None
            if alert_types and alert.get("type") not in alert_types:
                continue
            
            notifications.append({
                "contact_name": row[1],
                "method": row[2],
                "details": row[3]
            })
        
        return notifications
    
    def generate_alert_report(self) -> str:
        """Generate comprehensive alert status report"""
        
        report = []
        report.append("=" * 80)
        report.append("MULTI-SOURCE ALERT AGGREGATOR REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Get summary
        summary = self.aggregate_alerts()
        
        report.append("ALERT SUMMARY")
        report.append("-" * 40)
        report.append(f"Total Active Alerts: {summary['total_active_alerts']}")
        report.append(f"New Alerts: {summary['new_alerts']}")
        report.append("")
        
        # Critical alerts
        if summary["critical_alerts"]:
            report.append("🔴 CRITICAL ALERTS")
            report.append("-" * 40)
            for alert in summary["critical_alerts"][:5]:
                report.append(f"• {alert['title']} (Priority: {alert['priority']:.1f})")
                report.append(f"  Action: {alert['action']}")
                report.append(f"  Source: {alert['source']}")
                report.append("")
        
        # High priority alerts
        if summary["high_priority_alerts"]:
            report.append("🟠 HIGH PRIORITY ALERTS")
            report.append("-" * 40)
            for alert in summary["high_priority_alerts"][:3]:
                report.append(f"• {alert['title']} (Priority: {alert['priority']:.1f})")
                report.append(f"  Action: {alert['action']}")
                report.append("")
        
        # Alert types
        if summary["by_type"]:
            report.append("ALERTS BY TYPE")
            report.append("-" * 40)
            for alert_type, count in sorted(summary["by_type"].items(), key=lambda x: x[1], reverse=True):
                report.append(f"• {alert_type}: {count}")
            report.append("")
        
        # Required actions
        if summary["required_actions"]:
            report.append("REQUIRED ACTIONS")
            report.append("-" * 40)
            for i, action in enumerate(summary["required_actions"][:5], 1):
                report.append(f"{i}. {action}")
            report.append("")
        
        # Source status
        report.append("SOURCE STATUS")
        report.append("-" * 40)
        
        self.cursor.execute('''
            SELECT source_name, source_type, last_check, reliability_score
            FROM alert_sources
            WHERE status = 'active'
            ORDER BY reliability_score DESC
        ''')
        
        for source in self.cursor.fetchall()[:5]:
            status = "✅" if source[2] else "⚠️"
            report.append(f"{status} {source[0]} ({source[1]}) - Reliability: {source[3]*100:.0f}%")
        
        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        
        return "\n".join(report)
    
    def start_monitoring(self, interval: int = 60):
        """
        Start continuous monitoring in background thread
        
        Args:
            interval: Update interval in seconds
        """
        
        def monitor():
            self.monitoring_active = True
            while self.monitoring_active:
                self.aggregate_alerts()
                time.sleep(interval)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        
        # Count active alerts
        self.cursor.execute("SELECT COUNT(*) FROM active_alerts WHERE acknowledged = 0")
        active_count = self.cursor.fetchone()[0]
        
        # Count sources
        self.cursor.execute("SELECT COUNT(*) FROM alert_sources WHERE status = 'active'")
        source_count = self.cursor.fetchone()[0]
        
        # Count subscriptions
        self.cursor.execute("SELECT COUNT(*) FROM alert_subscriptions WHERE active = 1")
        subscription_count = self.cursor.fetchone()[0]
        
        # Get highest priority alert
        self.cursor.execute('''
            SELECT title, priority_score FROM active_alerts
            WHERE acknowledged = 0
            ORDER BY priority_score DESC
            LIMIT 1
        ''')
        highest_priority = self.cursor.fetchone()
        
        return {
            "system_name": "Multi-Source Alert Aggregator v3.0",
            "status": "monitoring" if self.monitoring_active else "standby",
            "active_alerts": active_count,
            "active_sources": source_count,
            "subscriptions": subscription_count,
            "highest_priority_alert": {
                "title": highest_priority[0] if highest_priority else None,
                "priority": highest_priority[1] if highest_priority else 0
            },
            "last_updated": datetime.now().isoformat(),
            "capabilities": [
                "Multi-source monitoring",
                "Intelligent prioritization",
                "Real-time aggregation",
                "Location-based filtering",
                "Subscription management",
                "Historical tracking",
                "Automated notifications"
            ]
        }
    
    def close(self):
        """Close database connection"""
        self.stop_monitoring()
        self.conn.close()


def main():
    """Test the Multi-Source Alert Aggregator"""
    
    print("🚨 Multi-Source Alert Aggregator v3.0")
    print("=" * 60)
    
    # Initialize aggregator
    aggregator = MultiSourceAlertAggregator("test_alert_aggregator.db")
    
    # Subscribe to alerts
    print("\n📧 Setting up alert subscription...")
    aggregator.subscribe_to_alerts(
        "Test User",
        "email",
        "user@example.com",
        ["earthquake", "fire", "evacuation"],
        severity_threshold=5
    )
    
    # Aggregate alerts
    print("\n📡 Aggregating alerts from all sources...")
    summary = aggregator.aggregate_alerts()
    
    print(f"\nAlert Summary:")
    print(f"  Total Active: {summary['total_active_alerts']}")
    print(f"  Critical: {len(summary['critical_alerts'])}")
    print(f"  High Priority: {len(summary['high_priority_alerts'])}")
    
    if summary['critical_alerts']:
        print("\n🔴 Critical Alerts:")
        for alert in summary['critical_alerts'][:3]:
            print(f"  • {alert['title']}")
            print(f"    Action: {alert['action']}")
            print(f"    Priority: {alert['priority']:.1f}")
    
    if summary['required_actions']:
        print("\n⚡ Required Actions:")
        for action in summary['required_actions'][:3]:
            print(f"  • {action}")
    
    # Generate report
    print("\n📊 Generating Full Report...")
    print("-" * 60)
    report = aggregator.generate_alert_report()
    print(report[:1000] + "..." if len(report) > 1000 else report)
    
    # System status
    print("\n✅ System Status")
    print("-" * 60)
    status = aggregator.get_system_status()
    print(f"Status: {status['status']}")
    print(f"Active Alerts: {status['active_alerts']}")
    print(f"Active Sources: {status['active_sources']}")
    if status['highest_priority_alert']['title']:
        print(f"Highest Priority: {status['highest_priority_alert']['title']}")
    
    aggregator.close()
    
    # Cleanup
    import os
    if os.path.exists("test_alert_aggregator.db"):
        os.remove("test_alert_aggregator.db")


if __name__ == "__main__":
    main()
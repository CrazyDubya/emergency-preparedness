#!/usr/bin/env python3
"""
Drill Automation & Scheduling System - Version 3.0
Automated drill scheduling with gamification elements and performance tracking
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import threading
import time
from calendar import monthrange

class DrillAutomationScheduler:
    """
    Advanced drill scheduling system with automated drill generation,
    intelligent scheduling, gamification elements, and performance analytics
    """
    
    def __init__(self, db_path: str = "drill_scheduler.db"):
        """Initialize the Drill Automation & Scheduling System"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_database()
        self._initialize_schedules()
        self._initialize_gamification()
        self.scheduler_active = False
        self.scheduler_lock = threading.Lock()
    
    def _initialize_database(self):
        """Create database tables for drill scheduling"""
        
        # Drill schedules table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drill_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_name TEXT UNIQUE NOT NULL,
                family_profile TEXT NOT NULL,
                schedule_type TEXT NOT NULL,
                frequency_days INTEGER,
                preferred_times TEXT,
                disaster_rotation TEXT,
                difficulty_progression TEXT,
                seasonal_adjustments TEXT,
                surprise_drills_enabled INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scheduled drills table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_drills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_id INTEGER,
                drill_type TEXT NOT NULL,
                scheduled_date TEXT NOT NULL,
                scheduled_time TEXT NOT NULL,
                difficulty_level INTEGER,
                estimated_duration INTEGER,
                drill_status TEXT DEFAULT 'scheduled',
                notification_sent INTEGER DEFAULT 0,
                completion_date TEXT,
                performance_score REAL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (schedule_id) REFERENCES drill_schedules (id)
            )
        ''')
        
        # Gamification profiles table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamification_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                family_profile TEXT UNIQUE NOT NULL,
                total_points INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                experience_points INTEGER DEFAULT 0,
                badges_earned TEXT DEFAULT '[]',
                achievement_streaks TEXT DEFAULT '[]',
                challenge_completions INTEGER DEFAULT 0,
                monthly_goals TEXT DEFAULT '[]',
                preferred_rewards TEXT DEFAULT '[]',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Achievement system table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_name TEXT UNIQUE NOT NULL,
                achievement_type TEXT NOT NULL,
                description TEXT,
                requirements TEXT,
                points_value INTEGER,
                badge_icon TEXT,
                unlock_condition TEXT,
                rarity_level TEXT,
                category TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Drill analytics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drill_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                family_profile TEXT NOT NULL,
                analysis_date TEXT NOT NULL,
                total_drills_month INTEGER,
                average_performance REAL,
                improvement_rate REAL,
                consistency_score REAL,
                readiness_level INTEGER,
                recommendations TEXT,
                trend_analysis TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Notification preferences table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                family_profile TEXT UNIQUE NOT NULL,
                reminder_advance_hours INTEGER DEFAULT 24,
                notification_methods TEXT DEFAULT '["app", "email"]',
                quiet_hours_start TEXT DEFAULT '22:00',
                quiet_hours_end TEXT DEFAULT '07:00',
                weekend_preference TEXT DEFAULT 'flexible',
                surprise_drill_consent INTEGER DEFAULT 0,
                motivation_style TEXT DEFAULT 'encouraging',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _initialize_schedules(self):
        """Initialize default schedule templates"""
        
        schedule_templates = [
            {
                "schedule_name": "Family Safety Basic",
                "family_profile": "Default Family",
                "schedule_type": "regular",
                "frequency_days": 30,  # Monthly
                "preferred_times": json.dumps(["Saturday 10:00", "Sunday 14:00"]),
                "disaster_rotation": json.dumps([
                    "earthquake", "fire", "power_outage", "severe_weather"
                ]),
                "difficulty_progression": json.dumps({
                    "start_level": 1,
                    "increment_every": 3,  # Every 3 successful drills
                    "max_level": 5
                }),
                "seasonal_adjustments": json.dumps({
                    "winter": ["power_outage", "heating_failure", "ice_storm"],
                    "spring": ["tornado", "flood", "severe_weather"],
                    "summer": ["wildfire", "hurricane", "heat_emergency"],
                    "fall": ["hurricane", "power_outage", "emergency_prep"]
                }),
                "surprise_drills_enabled": 1
            },
            {
                "schedule_name": "Intensive Preparedness",
                "family_profile": "Default Family",
                "schedule_type": "intensive",
                "frequency_days": 14,  # Bi-weekly
                "preferred_times": json.dumps(["Saturday 09:00", "Sunday 15:00", "Wednesday 19:00"]),
                "disaster_rotation": json.dumps([
                    "earthquake", "fire", "tornado", "flood", "power_outage",
                    "cyber_attack", "pandemic", "nuclear", "terrorism"
                ]),
                "difficulty_progression": json.dumps({
                    "start_level": 2,
                    "increment_every": 2,
                    "max_level": 5
                }),
                "seasonal_adjustments": json.dumps({
                    "winter": ["power_outage", "heating_failure"],
                    "spring": ["tornado", "flood"],
                    "summer": ["fire", "heat_emergency"],
                    "fall": ["hurricane", "emergency_prep"]
                }),
                "surprise_drills_enabled": 1
            },
            {
                "schedule_name": "Beginner Friendly",
                "family_profile": "Default Family",
                "schedule_type": "gentle",
                "frequency_days": 45,  # Every 6 weeks
                "preferred_times": json.dumps(["Saturday 11:00", "Sunday 13:00"]),
                "disaster_rotation": json.dumps([
                    "fire", "earthquake", "power_outage"
                ]),
                "difficulty_progression": json.dumps({
                    "start_level": 1,
                    "increment_every": 5,
                    "max_level": 3
                }),
                "seasonal_adjustments": json.dumps({
                    "winter": ["power_outage"],
                    "spring": ["fire"],
                    "summer": ["fire"],
                    "fall": ["earthquake"]
                }),
                "surprise_drills_enabled": 0
            }
        ]
        
        for schedule in schedule_templates:
            self.cursor.execute('''
                INSERT OR REPLACE INTO drill_schedules
                (schedule_name, family_profile, schedule_type, frequency_days,
                 preferred_times, disaster_rotation, difficulty_progression,
                 seasonal_adjustments, surprise_drills_enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(schedule.values()))
        
        self.conn.commit()
    
    def _initialize_gamification(self):
        """Initialize gamification system with achievements and badges"""
        
        achievements = [
            # Completion Achievements
            {
                "achievement_name": "First Steps",
                "achievement_type": "milestone",
                "description": "Complete your first emergency drill",
                "requirements": json.dumps({"drills_completed": 1}),
                "points_value": 100,
                "badge_icon": "🎯",
                "rarity_level": "common",
                "category": "milestone"
            },
            {
                "achievement_name": "Drill Sergeant",
                "achievement_type": "milestone",
                "description": "Complete 10 emergency drills",
                "requirements": json.dumps({"drills_completed": 10}),
                "points_value": 500,
                "badge_icon": "🏆",
                "rarity_level": "uncommon",
                "category": "milestone"
            },
            {
                "achievement_name": "Emergency Expert",
                "achievement_type": "milestone",
                "description": "Complete 50 emergency drills",
                "requirements": json.dumps({"drills_completed": 50}),
                "points_value": 2000,
                "badge_icon": "🥇",
                "rarity_level": "rare",
                "category": "milestone"
            },
            
            # Performance Achievements
            {
                "achievement_name": "Perfect Response",
                "achievement_type": "performance",
                "description": "Score 100% on any drill",
                "requirements": json.dumps({"perfect_score": 1}),
                "points_value": 300,
                "badge_icon": "⭐",
                "rarity_level": "uncommon",
                "category": "performance"
            },
            {
                "achievement_name": "Consistency Champion",
                "achievement_type": "performance",
                "description": "Score 80%+ on 5 consecutive drills",
                "requirements": json.dumps({"consecutive_high_scores": 5, "threshold": 80}),
                "points_value": 750,
                "badge_icon": "🔥",
                "rarity_level": "rare",
                "category": "performance"
            },
            {
                "achievement_name": "Speed Demon",
                "achievement_type": "performance",
                "description": "Complete a drill 25% faster than target time",
                "requirements": json.dumps({"speed_improvement": 25}),
                "points_value": 400,
                "badge_icon": "⚡",
                "rarity_level": "uncommon",
                "category": "performance"
            },
            
            # Diversity Achievements
            {
                "achievement_name": "Multi-Threat Ready",
                "achievement_type": "diversity",
                "description": "Complete drills for 5 different disaster types",
                "requirements": json.dumps({"disaster_types": 5}),
                "points_value": 600,
                "badge_icon": "🌟",
                "rarity_level": "uncommon",
                "category": "diversity"
            },
            {
                "achievement_name": "All-Hazards Prepared",
                "achievement_type": "diversity",
                "description": "Complete drills for all 10 disaster types",
                "requirements": json.dumps({"disaster_types": 10}),
                "points_value": 1500,
                "badge_icon": "🛡️",
                "rarity_level": "epic",
                "category": "diversity"
            },
            
            # Streak Achievements
            {
                "achievement_name": "Weekly Warrior",
                "achievement_type": "streak",
                "description": "Complete scheduled drills for 4 consecutive weeks",
                "requirements": json.dumps({"weekly_streak": 4}),
                "points_value": 400,
                "badge_icon": "📅",
                "rarity_level": "uncommon",
                "category": "consistency"
            },
            {
                "achievement_name": "Monthly Master",
                "achievement_type": "streak",
                "description": "Complete scheduled drills for 3 consecutive months",
                "requirements": json.dumps({"monthly_streak": 3}),
                "points_value": 1000,
                "badge_icon": "🗓️",
                "rarity_level": "rare",
                "category": "consistency"
            },
            
            # Special Achievements
            {
                "achievement_name": "Night Owl",
                "achievement_type": "special",
                "description": "Complete a drill during evening hours (after 8 PM)",
                "requirements": json.dumps({"evening_drill": 1}),
                "points_value": 200,
                "badge_icon": "🦉",
                "rarity_level": "common",
                "category": "special"
            },
            {
                "achievement_name": "Surprise Success",
                "achievement_type": "special",
                "description": "Successfully complete a surprise drill",
                "requirements": json.dumps({"surprise_drill": 1}),
                "points_value": 500,
                "badge_icon": "🎲",
                "rarity_level": "rare",
                "category": "special"
            },
            {
                "achievement_name": "Team Leader",
                "achievement_type": "special",
                "description": "Lead family coordination in 5 drills",
                "requirements": json.dumps({"leadership_role": 5}),
                "points_value": 800,
                "badge_icon": "👑",
                "rarity_level": "rare",
                "category": "leadership"
            }
        ]
        
        for achievement in achievements:
            self.cursor.execute('''
                INSERT OR REPLACE INTO achievements
                (achievement_name, achievement_type, description, requirements,
                 points_value, badge_icon, rarity_level, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(achievement.values()))
        
        # Initialize default gamification profile
        self.cursor.execute('''
            INSERT OR REPLACE INTO gamification_profiles
            (family_profile, total_points, current_level, experience_points)
            VALUES (?, ?, ?, ?)
        ''', ("Default Family", 0, 1, 0))
        
        self.conn.commit()
    
    def create_schedule(self, schedule_name: str, family_profile: str,
                       frequency_days: int, preferred_times: List[str],
                       disaster_types: List[str], **kwargs) -> Dict[str, Any]:
        """
        Create a new drill schedule
        
        Args:
            schedule_name: Name for the schedule
            family_profile: Family profile to schedule for
            frequency_days: Days between drills
            preferred_times: List of preferred times (e.g., ["Saturday 10:00"])
            disaster_types: List of disaster types to rotate through
            **kwargs: Additional schedule options
            
        Returns:
            Schedule creation result
        """
        
        try:
            # Set defaults
            schedule_type = kwargs.get("schedule_type", "regular")
            difficulty_progression = kwargs.get("difficulty_progression", {
                "start_level": 1,
                "increment_every": 3,
                "max_level": 5
            })
            seasonal_adjustments = kwargs.get("seasonal_adjustments", {})
            surprise_drills = kwargs.get("surprise_drills_enabled", 0)
            
            # Insert schedule
            self.cursor.execute('''
                INSERT INTO drill_schedules
                (schedule_name, family_profile, schedule_type, frequency_days,
                 preferred_times, disaster_rotation, difficulty_progression,
                 seasonal_adjustments, surprise_drills_enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                schedule_name,
                family_profile,
                schedule_type,
                frequency_days,
                json.dumps(preferred_times),
                json.dumps(disaster_types),
                json.dumps(difficulty_progression),
                json.dumps(seasonal_adjustments),
                surprise_drills
            ))
            
            schedule_id = self.cursor.lastrowid
            self.conn.commit()
            
            # Generate initial scheduled drills
            initial_drills = self._generate_upcoming_drills(schedule_id, 90)  # Next 3 months
            
            return {
                "schedule_id": schedule_id,
                "schedule_name": schedule_name,
                "status": "created",
                "next_drill": initial_drills[0] if initial_drills else None,
                "upcoming_drills": len(initial_drills),
                "frequency": f"Every {frequency_days} days",
                "disaster_types": disaster_types
            }
            
        except Exception as e:
            return {"error": f"Failed to create schedule: {e}"}
    
    def _generate_upcoming_drills(self, schedule_id: int, days_ahead: int = 90) -> List[Dict[str, Any]]:
        """Generate upcoming scheduled drills"""
        
        # Get schedule details
        self.cursor.execute('''
            SELECT * FROM drill_schedules WHERE id = ?
        ''', (schedule_id,))
        
        schedule_row = self.cursor.fetchone()
        if not schedule_row:
            return []
        
        schedule = {
            "id": schedule_row[0],
            "name": schedule_row[1],
            "family_profile": schedule_row[2],
            "frequency_days": schedule_row[4],
            "preferred_times": json.loads(schedule_row[5]),
            "disaster_rotation": json.loads(schedule_row[6]),
            "difficulty_progression": json.loads(schedule_row[7]),
            "seasonal_adjustments": json.loads(schedule_row[8]),
            "surprise_drills": schedule_row[9]
        }
        
        # Get last scheduled drill date
        self.cursor.execute('''
            SELECT MAX(scheduled_date) FROM scheduled_drills WHERE schedule_id = ?
        ''', (schedule_id,))
        
        last_date = self.cursor.fetchone()[0]
        if last_date:
            start_date = datetime.fromisoformat(last_date) + timedelta(days=schedule["frequency_days"])
        else:
            start_date = datetime.now() + timedelta(days=1)  # Start tomorrow
        
        # Generate drills
        generated_drills = []
        current_date = start_date
        end_date = datetime.now() + timedelta(days=days_ahead)
        disaster_index = 0
        drill_count = 0
        
        while current_date <= end_date:
            # Determine disaster type
            disaster_type = self._select_disaster_type(
                schedule["disaster_rotation"],
                schedule["seasonal_adjustments"],
                current_date,
                disaster_index
            )
            
            # Determine difficulty level
            difficulty = self._calculate_difficulty_level(
                schedule["difficulty_progression"],
                drill_count
            )
            
            # Select preferred time
            preferred_time = self._select_drill_time(
                schedule["preferred_times"],
                current_date
            )
            
            # Estimate duration based on disaster type and difficulty
            duration = self._estimate_drill_duration(disaster_type, difficulty)
            
            # Create scheduled drill
            drill_data = {
                "schedule_id": schedule_id,
                "drill_type": disaster_type,
                "scheduled_date": current_date.date().isoformat(),
                "scheduled_time": preferred_time,
                "difficulty_level": difficulty,
                "estimated_duration": duration
            }
            
            # Insert into database
            self.cursor.execute('''
                INSERT INTO scheduled_drills
                (schedule_id, drill_type, scheduled_date, scheduled_time,
                 difficulty_level, estimated_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', tuple(drill_data.values()))
            
            generated_drills.append(drill_data)
            
            # Move to next drill date
            current_date += timedelta(days=schedule["frequency_days"])
            disaster_index = (disaster_index + 1) % len(schedule["disaster_rotation"])
            drill_count += 1
        
        self.conn.commit()
        
        # Generate surprise drills if enabled
        if schedule["surprise_drills"]:
            surprise_drills = self._generate_surprise_drills(schedule_id, days_ahead)
            generated_drills.extend(surprise_drills)
        
        return generated_drills
    
    def _select_disaster_type(self, rotation: List[str], seasonal: Dict[str, List[str]],
                            date: datetime, index: int) -> str:
        """Select disaster type considering rotation and seasonal factors"""
        
        # Get season
        month = date.month
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "fall"
        
        # Check if seasonal adjustments apply
        if season in seasonal and random.random() < 0.3:  # 30% chance of seasonal drill
            return random.choice(seasonal[season])
        
        # Use rotation
        return rotation[index % len(rotation)]
    
    def _calculate_difficulty_level(self, progression: Dict[str, int], drill_count: int) -> int:
        """Calculate difficulty level based on progression settings"""
        
        start_level = progression.get("start_level", 1)
        increment_every = progression.get("increment_every", 3)
        max_level = progression.get("max_level", 5)
        
        level = start_level + (drill_count // increment_every)
        return min(level, max_level)
    
    def _select_drill_time(self, preferred_times: List[str], date: datetime) -> str:
        """Select appropriate drill time for the date"""
        
        day_name = date.strftime("%A")
        
        # Filter times for this day of week
        matching_times = [t for t in preferred_times if day_name in t or "any" in t.lower()]
        
        if matching_times:
            time_str = random.choice(matching_times)
            # Extract time portion
            if " " in time_str:
                return time_str.split(" ")[-1]
        
        # Default times if no match
        if date.weekday() < 5:  # Weekday
            return random.choice(["07:00", "19:00"])
        else:  # Weekend
            return random.choice(["10:00", "14:00", "16:00"])
    
    def _estimate_drill_duration(self, disaster_type: str, difficulty: int) -> int:
        """Estimate drill duration based on type and difficulty"""
        
        base_durations = {
            "earthquake": 15,
            "fire": 10,
            "tornado": 20,
            "hurricane": 60,
            "flood": 30,
            "power_outage": 45,
            "cyber_attack": 25,
            "pandemic": 90,
            "nuclear": 60,
            "terrorism": 15
        }
        
        base = base_durations.get(disaster_type, 30)
        
        # Adjust for difficulty
        duration = base * (1 + (difficulty - 1) * 0.3)
        
        return int(duration)
    
    def _generate_surprise_drills(self, schedule_id: int, days_ahead: int) -> List[Dict[str, Any]]:
        """Generate surprise drills for the schedule"""
        
        surprise_drills = []
        
        # Get schedule details
        self.cursor.execute('''
            SELECT disaster_rotation, frequency_days FROM drill_schedules WHERE id = ?
        ''', (schedule_id,))
        
        result = self.cursor.fetchone()
        if not result:
            return surprise_drills
        
        disaster_rotation = json.loads(result[0])
        frequency_days = result[1]
        
        # Generate 1-2 surprise drills per month
        num_surprises = max(1, days_ahead // 30)
        
        for _ in range(num_surprises):
            # Random date within the period
            random_days = random.randint(7, days_ahead - 7)
            surprise_date = datetime.now() + timedelta(days=random_days)
            
            # Random time (avoid quiet hours)
            hour = random.choice([9, 10, 11, 14, 15, 16, 19, 20])
            minute = random.choice([0, 15, 30, 45])
            surprise_time = f"{hour:02d}:{minute:02d}"
            
            # Random disaster type
            disaster_type = random.choice(disaster_rotation)
            
            drill_data = {
                "schedule_id": schedule_id,
                "drill_type": f"SURPRISE_{disaster_type}",
                "scheduled_date": surprise_date.date().isoformat(),
                "scheduled_time": surprise_time,
                "difficulty_level": random.randint(1, 3),  # Keep surprises easier
                "estimated_duration": self._estimate_drill_duration(disaster_type, 2)
            }
            
            # Insert surprise drill
            self.cursor.execute('''
                INSERT INTO scheduled_drills
                (schedule_id, drill_type, scheduled_date, scheduled_time,
                 difficulty_level, estimated_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', tuple(drill_data.values()))
            
            surprise_drills.append(drill_data)
        
        return surprise_drills
    
    def get_upcoming_drills(self, family_profile: str = "Default Family",
                           days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Get upcoming scheduled drills"""
        
        end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
        
        self.cursor.execute('''
            SELECT sd.*, ds.schedule_name
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE ds.family_profile = ? AND sd.scheduled_date <= ? AND sd.drill_status = 'scheduled'
            ORDER BY sd.scheduled_date, sd.scheduled_time
        ''', (family_profile, end_date))
        
        upcoming = []
        for row in self.cursor.fetchall():
            drill_datetime = datetime.fromisoformat(f"{row[3]} {row[4]}")
            
            upcoming.append({
                "drill_id": row[0],
                "schedule_name": row[-1],
                "drill_type": row[2],
                "scheduled_datetime": drill_datetime.isoformat(),
                "difficulty_level": row[5],
                "estimated_duration": row[6],
                "is_surprise": "SURPRISE_" in row[2],
                "days_until": (drill_datetime.date() - datetime.now().date()).days,
                "status": row[7]
            })
        
        return upcoming
    
    def complete_scheduled_drill(self, drill_id: int, performance_score: float,
                               actual_duration: int, notes: str = None) -> Dict[str, Any]:
        """Complete a scheduled drill and update tracking"""
        
        completion_time = datetime.now()
        
        # Update drill record
        self.cursor.execute('''
            UPDATE scheduled_drills
            SET drill_status = 'completed', completion_date = ?,
                performance_score = ?, notes = ?
            WHERE id = ?
        ''', (completion_time.isoformat(), performance_score, notes, drill_id))
        
        # Get drill details for gamification
        self.cursor.execute('''
            SELECT sd.*, ds.family_profile
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE sd.id = ?
        ''', (drill_id,))
        
        drill_row = self.cursor.fetchone()
        if not drill_row:
            return {"error": "Drill not found"}
        
        family_profile = drill_row[-1]
        drill_type = drill_row[2]
        difficulty = drill_row[5]
        is_surprise = "SURPRISE_" in drill_type
        
        # Update gamification
        gamification_result = self._update_gamification(
            family_profile, performance_score, drill_type, difficulty, is_surprise
        )
        
        # Update analytics
        self._update_drill_analytics(family_profile)
        
        self.conn.commit()
        
        return {
            "drill_id": drill_id,
            "completion_status": "completed",
            "performance_score": performance_score,
            "gamification": gamification_result,
            "next_drill": self._get_next_scheduled_drill(family_profile)
        }
    
    def _update_gamification(self, family_profile: str, score: float,
                           drill_type: str, difficulty: int, is_surprise: bool) -> Dict[str, Any]:
        """Update gamification profile and check for achievements"""
        
        # Calculate points earned
        base_points = 50
        difficulty_bonus = difficulty * 10
        performance_bonus = int((score - 50) / 10) * 5  # Extra points for good performance
        surprise_bonus = 25 if is_surprise else 0
        
        total_points = max(10, base_points + difficulty_bonus + performance_bonus + surprise_bonus)
        
        # Get current gamification profile
        self.cursor.execute('''
            SELECT * FROM gamification_profiles WHERE family_profile = ?
        ''', (family_profile,))
        
        profile_row = self.cursor.fetchone()
        if not profile_row:
            # Create new profile
            self.cursor.execute('''
                INSERT INTO gamification_profiles (family_profile, total_points, experience_points)
                VALUES (?, ?, ?)
            ''', (family_profile, total_points, total_points))
            profile_data = {
                "total_points": total_points,
                "current_level": 1,
                "experience_points": total_points,
                "badges_earned": []
            }
        else:
            # Update existing profile
            new_total = profile_row[2] + total_points
            new_exp = profile_row[4] + total_points
            
            # Calculate new level
            new_level = self._calculate_level(new_exp)
            level_up = new_level > profile_row[3]
            
            # Update database
            self.cursor.execute('''
                UPDATE gamification_profiles
                SET total_points = ?, current_level = ?, experience_points = ?
                WHERE family_profile = ?
            ''', (new_total, new_level, new_exp, family_profile))
            
            profile_data = {
                "total_points": new_total,
                "current_level": new_level,
                "experience_points": new_exp,
                "level_up": level_up,
                "badges_earned": json.loads(profile_row[5])
            }
        
        # Check for new achievements
        new_achievements = self._check_achievements(family_profile, score, drill_type, is_surprise)
        
        profile_data.update({
            "points_earned": total_points,
            "new_achievements": new_achievements
        })
        
        return profile_data
    
    def _calculate_level(self, experience_points: int) -> int:
        """Calculate level based on experience points"""
        
        # Level progression: 100, 250, 500, 1000, 1750, 2750, 4000, 5500, 7250, 9250, ...
        level = 1
        points_needed = 100
        
        while experience_points >= points_needed:
            experience_points -= points_needed
            level += 1
            points_needed = int(points_needed * 1.5)  # Exponential growth
        
        return level
    
    def _check_achievements(self, family_profile: str, score: float,
                          drill_type: str, is_surprise: bool) -> List[Dict[str, Any]]:
        """Check for newly earned achievements"""
        
        new_achievements = []
        
        # Get current achievements
        self.cursor.execute('''
            SELECT badges_earned FROM gamification_profiles WHERE family_profile = ?
        ''', (family_profile,))
        
        result = self.cursor.fetchone()
        current_badges = json.loads(result[0]) if result and result[0] else []
        
        # Get drill statistics for achievement checking
        self.cursor.execute('''
            SELECT COUNT(*), AVG(performance_score), 
                   COUNT(DISTINCT drill_type), MAX(performance_score)
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE ds.family_profile = ? AND sd.drill_status = 'completed'
        ''', (family_profile,))
        
        stats = self.cursor.fetchone()
        total_drills = stats[0] if stats else 0
        avg_score = stats[1] if stats else 0
        unique_types = stats[2] if stats else 0
        max_score = stats[3] if stats else 0
        
        # Check each achievement
        self.cursor.execute('SELECT * FROM achievements')
        all_achievements = self.cursor.fetchall()
        
        for achievement_row in all_achievements:
            achievement_name = achievement_row[1]
            
            # Skip if already earned
            if achievement_name in current_badges:
                continue
            
            requirements = json.loads(achievement_row[4])
            earned = False
            
            # Check requirements
            if "drills_completed" in requirements:
                if total_drills >= requirements["drills_completed"]:
                    earned = True
            
            if "perfect_score" in requirements and score == 100:
                earned = True
            
            if "disaster_types" in requirements:
                if unique_types >= requirements["disaster_types"]:
                    earned = True
            
            if "surprise_drill" in requirements and is_surprise:
                earned = True
            
            if "evening_drill" in requirements:
                # Check if current time is evening (simplified)
                current_hour = datetime.now().hour
                if current_hour >= 20:
                    earned = True
            
            # Add more achievement checks as needed
            
            if earned:
                new_achievements.append({
                    "name": achievement_name,
                    "description": achievement_row[3],
                    "points": achievement_row[5],
                    "badge": achievement_row[6],
                    "rarity": achievement_row[8]
                })
                current_badges.append(achievement_name)
        
        # Update badges in database
        if new_achievements:
            self.cursor.execute('''
                UPDATE gamification_profiles
                SET badges_earned = ?
                WHERE family_profile = ?
            ''', (json.dumps(current_badges), family_profile))
        
        return new_achievements
    
    def _update_drill_analytics(self, family_profile: str):
        """Update monthly drill analytics"""
        
        current_month = datetime.now().replace(day=1).date().isoformat()
        
        # Get this month's drill statistics
        self.cursor.execute('''
            SELECT COUNT(*), AVG(performance_score), 
                   MIN(performance_score), MAX(performance_score)
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE ds.family_profile = ? 
                AND sd.drill_status = 'completed'
                AND date(sd.completion_date) >= ?
        ''', (family_profile, current_month))
        
        month_stats = self.cursor.fetchone()
        
        if month_stats and month_stats[0] > 0:
            total_drills = month_stats[0]
            avg_performance = month_stats[1]
            
            # Calculate improvement rate (vs last month)
            last_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).date().isoformat()
            
            self.cursor.execute('''
                SELECT AVG(performance_score)
                FROM scheduled_drills sd
                JOIN drill_schedules ds ON sd.schedule_id = ds.id
                WHERE ds.family_profile = ? 
                    AND sd.drill_status = 'completed'
                    AND date(sd.completion_date) >= ?
                    AND date(sd.completion_date) < ?
            ''', (family_profile, last_month, current_month))
            
            last_month_avg = self.cursor.fetchone()[0] or avg_performance
            improvement_rate = ((avg_performance - last_month_avg) / last_month_avg) * 100 if last_month_avg > 0 else 0
            
            # Calculate consistency score
            consistency_score = max(0, 100 - (month_stats[3] - month_stats[2]))  # Lower variance = higher consistency
            
            # Calculate readiness level
            readiness_level = min(5, max(1, int(avg_performance / 20)))
            
            # Generate recommendations
            recommendations = self._generate_analytics_recommendations(
                total_drills, avg_performance, improvement_rate, consistency_score
            )
            
            # Update or insert analytics
            self.cursor.execute('''
                INSERT OR REPLACE INTO drill_analytics
                (family_profile, analysis_date, total_drills_month, average_performance,
                 improvement_rate, consistency_score, readiness_level, recommendations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                family_profile, current_month, total_drills, avg_performance,
                improvement_rate, consistency_score, readiness_level, json.dumps(recommendations)
            ))
    
    def _generate_analytics_recommendations(self, total_drills: int, avg_score: float,
                                         improvement_rate: float, consistency: float) -> List[str]:
        """Generate analytics-based recommendations"""
        
        recommendations = []
        
        if total_drills < 2:
            recommendations.append("Increase drill frequency to build muscle memory")
        
        if avg_score < 70:
            recommendations.append("Focus on fundamental emergency procedures")
            recommendations.append("Consider starting with easier difficulty levels")
        
        if improvement_rate < 0:
            recommendations.append("Review and practice areas where performance decreased")
        
        if consistency < 70:
            recommendations.append("Work on consistent performance across different scenarios")
        
        if avg_score > 85 and consistency > 80:
            recommendations.append("Consider increasing difficulty level for new challenges")
            recommendations.append("You're ready for advanced multi-scenario drills")
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _get_next_scheduled_drill(self, family_profile: str) -> Optional[Dict[str, Any]]:
        """Get the next scheduled drill for a family"""
        
        self.cursor.execute('''
            SELECT sd.*, ds.schedule_name
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE ds.family_profile = ? AND sd.drill_status = 'scheduled'
                AND datetime(sd.scheduled_date || ' ' || sd.scheduled_time) > datetime('now')
            ORDER BY sd.scheduled_date, sd.scheduled_time
            LIMIT 1
        ''', (family_profile,))
        
        result = self.cursor.fetchone()
        if result:
            drill_datetime = datetime.fromisoformat(f"{result[3]} {result[4]}")
            return {
                "drill_id": result[0],
                "schedule_name": result[-1],
                "drill_type": result[2],
                "scheduled_datetime": drill_datetime.isoformat(),
                "days_until": (drill_datetime.date() - datetime.now().date()).days
            }
        
        return None
    
    def start_scheduler(self):
        """Start the automated drill scheduler"""
        
        def scheduler_loop():
            self.scheduler_active = True
            while self.scheduler_active:
                with self.scheduler_lock:
                    self._check_drill_notifications()
                    self._check_schedule_maintenance()
                
                # Check every hour
                time.sleep(3600)
        
        scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the automated drill scheduler"""
        self.scheduler_active = False
    
    def _check_drill_notifications(self):
        """Check for drills needing notifications"""
        
        # Get drills in the next 24-48 hours that haven't been notified
        notification_window = datetime.now() + timedelta(hours=24)
        
        self.cursor.execute('''
            SELECT sd.*, ds.family_profile
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE datetime(sd.scheduled_date || ' ' || sd.scheduled_time) <= ?
                AND sd.drill_status = 'scheduled'
                AND sd.notification_sent = 0
        ''', (notification_window.isoformat(),))
        
        for drill_row in self.cursor.fetchall():
            # Send notification (simulated)
            drill_datetime = datetime.fromisoformat(f"{drill_row[3]} {drill_row[4]}")
            time_until = drill_datetime - datetime.now()
            
            notification = {
                "family_profile": drill_row[-1],
                "drill_type": drill_row[2],
                "scheduled_time": drill_datetime.isoformat(),
                "time_until": str(time_until),
                "message": f"Upcoming {drill_row[2]} drill in {time_until}"
            }
            
            # In production, this would send actual notifications
            print(f"📱 Notification: {notification['message']}")
            
            # Mark as notified
            self.cursor.execute('''
                UPDATE scheduled_drills SET notification_sent = 1 WHERE id = ?
            ''', (drill_row[0],))
        
        self.conn.commit()
    
    def _check_schedule_maintenance(self):
        """Perform schedule maintenance tasks"""
        
        # Generate new drills for schedules that are running low
        self.cursor.execute('''
            SELECT DISTINCT ds.id
            FROM drill_schedules ds
            WHERE ds.active = 1
                AND (SELECT COUNT(*) FROM scheduled_drills sd 
                     WHERE sd.schedule_id = ds.id 
                     AND sd.drill_status = 'scheduled'
                     AND date(sd.scheduled_date) > date('now')) < 3
        ''')
        
        for (schedule_id,) in self.cursor.fetchall():
            self._generate_upcoming_drills(schedule_id, 90)
    
    def get_gamification_status(self, family_profile: str = "Default Family") -> Dict[str, Any]:
        """Get current gamification status"""
        
        self.cursor.execute('''
            SELECT * FROM gamification_profiles WHERE family_profile = ?
        ''', (family_profile,))
        
        profile_row = self.cursor.fetchone()
        if not profile_row:
            return {"error": "Profile not found"}
        
        # Calculate points to next level
        current_exp = profile_row[4]
        current_level = profile_row[3]
        
        level_exp = 100
        for _ in range(current_level - 1):
            level_exp = int(level_exp * 1.5)
        
        next_level_exp = int(level_exp * 1.5)
        progress_to_next = (current_exp % level_exp) / level_exp * 100
        
        # Get recent achievements
        badges_earned = json.loads(profile_row[5])
        
        return {
            "family_profile": family_profile,
            "total_points": profile_row[2],
            "current_level": current_level,
            "experience_points": current_exp,
            "progress_to_next_level": round(progress_to_next, 1),
            "points_to_next_level": next_level_exp - (current_exp % level_exp),
            "badges_earned": badges_earned,
            "total_badges": len(badges_earned),
            "challenge_completions": profile_row[6]
        }
    
    def get_analytics_report(self, family_profile: str = "Default Family") -> Dict[str, Any]:
        """Get comprehensive analytics report"""
        
        # Get latest analytics
        self.cursor.execute('''
            SELECT * FROM drill_analytics 
            WHERE family_profile = ?
            ORDER BY analysis_date DESC
            LIMIT 1
        ''', (family_profile,))
        
        analytics_row = self.cursor.fetchone()
        
        # Get overall statistics
        self.cursor.execute('''
            SELECT COUNT(*), AVG(performance_score), 
                   COUNT(DISTINCT drill_type), MAX(difficulty_level)
            FROM scheduled_drills sd
            JOIN drill_schedules ds ON sd.schedule_id = ds.id
            WHERE ds.family_profile = ? AND sd.drill_status = 'completed'
        ''', (family_profile,))
        
        overall_stats = self.cursor.fetchone()
        
        report = {
            "family_profile": family_profile,
            "report_date": datetime.now().isoformat(),
            "overall_statistics": {
                "total_drills_completed": overall_stats[0] if overall_stats else 0,
                "overall_average_score": round(overall_stats[1], 1) if overall_stats and overall_stats[1] else 0,
                "disaster_types_practiced": overall_stats[2] if overall_stats else 0,
                "highest_difficulty_completed": overall_stats[3] if overall_stats else 0
            }
        }
        
        if analytics_row:
            report["monthly_analysis"] = {
                "analysis_month": analytics_row[2],
                "drills_this_month": analytics_row[3],
                "average_performance": round(analytics_row[4], 1),
                "improvement_rate": round(analytics_row[5], 1),
                "consistency_score": round(analytics_row[6], 1),
                "readiness_level": analytics_row[7],
                "recommendations": json.loads(analytics_row[8]) if analytics_row[8] else []
            }
        
        return report
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get drill scheduler system status"""
        
        # Count active schedules
        self.cursor.execute("SELECT COUNT(*) FROM drill_schedules WHERE active = 1")
        active_schedules = self.cursor.fetchone()[0]
        
        # Count scheduled drills
        self.cursor.execute("SELECT COUNT(*) FROM scheduled_drills WHERE drill_status = 'scheduled'")
        scheduled_drills = self.cursor.fetchone()[0]
        
        # Count completed drills
        self.cursor.execute("SELECT COUNT(*) FROM scheduled_drills WHERE drill_status = 'completed'")
        completed_drills = self.cursor.fetchone()[0]
        
        # Count achievements
        self.cursor.execute("SELECT COUNT(*) FROM achievements")
        total_achievements = self.cursor.fetchone()[0]
        
        return {
            "system_name": "Drill Automation & Scheduling System v3.0",
            "status": "monitoring" if self.scheduler_active else "standby",
            "active_schedules": active_schedules,
            "scheduled_drills": scheduled_drills,
            "completed_drills": completed_drills,
            "total_achievements": total_achievements,
            "scheduler_active": self.scheduler_active,
            "last_updated": datetime.now().isoformat(),
            "capabilities": [
                "Automated drill scheduling",
                "Intelligent time selection",
                "Progressive difficulty",
                "Gamification system",
                "Performance analytics",
                "Achievement tracking",
                "Surprise drill generation",
                "Family customization"
            ]
        }
    
    def close(self):
        """Close database connection"""
        self.stop_scheduler()
        self.conn.close()


def main():
    """Test the Drill Automation & Scheduling System"""
    
    print("🤖 Drill Automation & Scheduling System v3.0")
    print("=" * 60)
    
    # Initialize scheduler
    scheduler = DrillAutomationScheduler("test_drill_scheduler.db")
    
    # Create a custom schedule
    print("\n📅 Creating Custom Schedule:")
    schedule_result = scheduler.create_schedule(
        schedule_name="Test Family Schedule",
        family_profile="Default Family",
        frequency_days=21,  # Every 3 weeks
        preferred_times=["Saturday 10:00", "Sunday 14:00"],
        disaster_types=["earthquake", "fire", "power_outage", "tornado"],
        surprise_drills_enabled=1
    )
    
    if "error" not in schedule_result:
        print(f"  Schedule Created: {schedule_result['schedule_name']}")
        print(f"  Frequency: {schedule_result['frequency']}")
        print(f"  Upcoming Drills: {schedule_result['upcoming_drills']}")
        
        if schedule_result['next_drill']:
            print(f"  Next Drill: {schedule_result['next_drill']['drill_type']}")
    
    # Get upcoming drills
    print("\n📋 Upcoming Drills:")
    upcoming = scheduler.get_upcoming_drills("Default Family", days_ahead=60)
    for drill in upcoming[:5]:
        print(f"  • {drill['drill_type']} (Level {drill['difficulty_level']})")
        print(f"    Date: {drill['scheduled_datetime'][:16]}, Duration: {drill['estimated_duration']} min")
        if drill['is_surprise']:
            print(f"    🎲 SURPRISE DRILL")
    
    # Simulate completing a drill
    if upcoming:
        print("\n✅ Simulating Drill Completion:")
        completion = scheduler.complete_scheduled_drill(
            upcoming[0]['drill_id'],
            performance_score=85.0,
            actual_duration=22,
            notes="Family performed well with good coordination"
        )
        
        if "error" not in completion:
            print(f"  Drill Completed: Score {completion['performance_score']}%")
            
            # Show gamification results
            gamification = completion['gamification']
            print(f"  Points Earned: {gamification['points_earned']}")
            print(f"  Current Level: {gamification['current_level']}")
            
            if gamification.get('level_up'):
                print(f"  🎉 LEVEL UP!")
            
            if gamification['new_achievements']:
                print(f"  🏆 New Achievements:")
                for achievement in gamification['new_achievements']:
                    print(f"    {achievement['badge']} {achievement['name']}")
    
    # Show gamification status
    print("\n🎮 Gamification Status:")
    gam_status = scheduler.get_gamification_status("Default Family")
    print(f"  Level: {gam_status['current_level']}")
    print(f"  Total Points: {gam_status['total_points']}")
    print(f"  Badges Earned: {gam_status['total_badges']}")
    print(f"  Progress to Next Level: {gam_status['progress_to_next_level']:.1f}%")
    
    # Show analytics
    print("\n📊 Analytics Report:")
    analytics = scheduler.get_analytics_report("Default Family")
    overall = analytics['overall_statistics']
    print(f"  Total Drills: {overall['total_drills_completed']}")
    print(f"  Average Score: {overall['overall_average_score']}%")
    print(f"  Disaster Types: {overall['disaster_types_practiced']}")
    
    # System status
    print("\n🔧 System Status:")
    status = scheduler.get_system_status()
    print(f"  Status: {status['status']}")
    print(f"  Active Schedules: {status['active_schedules']}")
    print(f"  Scheduled Drills: {status['scheduled_drills']}")
    print(f"  Completed Drills: {status['completed_drills']}")
    print(f"  Total Achievements: {status['total_achievements']}")
    
    scheduler.close()
    
    # Cleanup
    import os
    if os.path.exists("test_drill_scheduler.db"):
        os.remove("test_drill_scheduler.db")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
User Profile Manager - Persistent State Management
Handles user profiles, preferences, and cached assessments
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
import hashlib
import shutil


class UserProfileManager:
    """Manage user profiles with persistent state and intelligent caching"""
    
    def __init__(self, data_dir: str = "preparedness_data"):
        """Initialize the user profile manager"""
        self.data_dir = Path(data_dir)
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_profile = None
        self.profile_path = None
        self.profile_data = {}
        
        # Cache expiry times (in days)
        self.cache_expiry = {
            'risk_assessment': 30,  # Re-assess monthly
            'contacts': 90,  # Verify quarterly
            'supplies': 7,  # Check weekly
            'drills': 14,  # Practice bi-weekly
            'location': 365,  # Update annually
            'family': 180  # Update semi-annually
        }
    
    def list_profiles(self) -> List[str]:
        """List all available user profiles"""
        profiles = []
        for profile_file in self.profiles_dir.glob("*.json"):
            if profile_file.stem != "template":
                profiles.append(profile_file.stem)
        return profiles
    
    def load_profile(self, profile_name: str = "default") -> Dict[str, Any]:
        """Load an existing user profile or create new one"""
        self.current_profile = profile_name
        self.profile_path = self.profiles_dir / f"{profile_name}.json"
        
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    self.profile_data = json.load(f)
                print(f"✅ Loaded profile: {profile_name}")
                
                # Check for required updates
                self._check_updates_needed()
                
            except json.JSONDecodeError:
                print(f"⚠️ Profile corrupted, creating backup and new profile")
                self._backup_corrupted_profile()
                self.profile_data = self._create_default_profile()
        else:
            print(f"📝 Creating new profile: {profile_name}")
            self.profile_data = self._create_default_profile()
            self.save_profile()
        
        return self.profile_data
    
    def save_profile(self) -> bool:
        """Save current profile to disk"""
        if not self.profile_path:
            return False
        
        try:
            # Update last modified timestamp
            self.profile_data['meta']['last_modified'] = datetime.now().isoformat()
            
            # Create backup before saving
            if self.profile_path.exists():
                self._create_backup()
            
            # Save profile
            with open(self.profile_path, 'w') as f:
                json.dump(self.profile_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"❌ Error saving profile: {e}")
            return False
    
    def update_profile(self, section: str, data: Dict[str, Any], 
                      force: bool = False) -> bool:
        """Update a specific section of the profile"""
        if not self.profile_data:
            return False
        
        # Check if update is needed or forced
        if not force and not self.is_update_needed(section):
            print(f"ℹ️ {section} data is still current, skipping update")
            return False
        
        # Update the section
        if section not in self.profile_data:
            self.profile_data[section] = {}
        
        self.profile_data[section].update(data)
        self.profile_data[section]['last_updated'] = datetime.now().isoformat()
        
        # Save changes
        return self.save_profile()
    
    def is_update_needed(self, section: str) -> bool:
        """Check if a section needs updating based on cache expiry"""
        if section not in self.profile_data:
            return True
        
        section_data = self.profile_data.get(section, {})
        last_updated = section_data.get('last_updated')
        
        if not last_updated:
            return True
        
        # Parse last updated time
        try:
            last_update_time = datetime.fromisoformat(last_updated)
            expiry_days = self.cache_expiry.get(section, 30)
            expiry_date = last_update_time + timedelta(days=expiry_days)
            
            return datetime.now() > expiry_date
        except:
            return True
    
    def get_cached_data(self, section: str) -> Optional[Dict[str, Any]]:
        """Get cached data for a section if still valid"""
        if not self.is_update_needed(section):
            return self.profile_data.get(section, {})
        return None
    
    def get_risk_assessment(self) -> Optional[Dict[str, Any]]:
        """Get cached risk assessment if still valid"""
        return self.get_cached_data('risk_assessment')
    
    def save_risk_assessment(self, assessment_data: Dict[str, Any]) -> bool:
        """Save risk assessment results"""
        return self.update_profile('risk_assessment', assessment_data)
    
    def get_family_info(self) -> Dict[str, Any]:
        """Get family information"""
        return self.profile_data.get('family', {})
    
    def save_family_info(self, family_data: Dict[str, Any]) -> bool:
        """Save family information"""
        return self.update_profile('family', family_data)
    
    def get_location_info(self) -> Dict[str, Any]:
        """Get location information"""
        return self.profile_data.get('location', {})
    
    def save_location_info(self, location_data: Dict[str, Any]) -> bool:
        """Save location information"""
        return self.update_profile('location', location_data)
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences"""
        return self.profile_data.get('preferences', {})
    
    def save_preferences(self, preferences: Dict[str, Any]) -> bool:
        """Save user preferences"""
        return self.update_profile('preferences', preferences)
    
    def get_last_activity(self, activity_type: str) -> Optional[str]:
        """Get timestamp of last activity of a specific type"""
        activities = self.profile_data.get('activities', {})
        return activities.get(activity_type)
    
    def record_activity(self, activity_type: str, details: Dict[str, Any] = None) -> bool:
        """Record an activity with timestamp"""
        if 'activities' not in self.profile_data:
            self.profile_data['activities'] = {}
        
        activity_record = {
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        self.profile_data['activities'][activity_type] = activity_record
        return self.save_profile()
    
    def _create_default_profile(self) -> Dict[str, Any]:
        """Create a default profile structure"""
        return {
            'meta': {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'profile_id': self._generate_profile_id()
            },
            'family': {
                'adults': 0,
                'children': 0,
                'pets': 0,
                'special_needs': [],
                'last_updated': None
            },
            'location': {
                'type': None,  # urban/suburban/rural
                'housing': None,  # house/apartment/condo
                'ownership': None,  # own/rent
                'geographic_risks': [],
                'last_updated': None
            },
            'risk_assessment': {
                'matrix': None,
                'top_risks': [],
                'preparedness_score': 0,
                'last_updated': None
            },
            'supplies': {
                'inventory_status': {},
                'shopping_list': [],
                'expiry_alerts': [],
                'last_updated': None
            },
            'contacts': {
                'emergency_contacts': [],
                'verified': False,
                'last_updated': None
            },
            'drills': {
                'completed': [],
                'scheduled': [],
                'performance_history': [],
                'last_updated': None
            },
            'preferences': {
                'notification_frequency': 'weekly',
                'drill_difficulty': 'intermediate',
                'report_format': 'detailed',
                'auto_backup': True,
                'last_updated': None
            },
            'activities': {}
        }
    
    def _check_updates_needed(self) -> None:
        """Check which sections need updating and notify user"""
        updates_needed = []
        
        for section, expiry_days in self.cache_expiry.items():
            if self.is_update_needed(section):
                updates_needed.append(section)
        
        if updates_needed:
            print(f"\n⚠️ The following sections need updating:")
            for section in updates_needed:
                print(f"  • {section.replace('_', ' ').title()}")
            print("\nConsider updating these sections for accurate preparedness assessment.\n")
    
    def _create_backup(self) -> None:
        """Create a backup of current profile"""
        if not self.profile_path.exists():
            return
        
        backup_dir = self.profiles_dir / "backups" / self.current_profile
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Keep only last 5 backups
        existing_backups = sorted(backup_dir.glob("*.json"))
        if len(existing_backups) >= 5:
            existing_backups[0].unlink()  # Delete oldest
        
        # Create new backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{self.current_profile}_{timestamp}.json"
        shutil.copy2(self.profile_path, backup_path)
    
    def _backup_corrupted_profile(self) -> None:
        """Backup a corrupted profile"""
        if not self.profile_path.exists():
            return
        
        corrupted_dir = self.profiles_dir / "corrupted"
        corrupted_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        corrupted_path = corrupted_dir / f"{self.current_profile}_corrupted_{timestamp}.json"
        shutil.move(str(self.profile_path), str(corrupted_path))
        print(f"  Corrupted profile backed up to: {corrupted_path}")
    
    def _generate_profile_id(self) -> str:
        """Generate a unique profile ID"""
        unique_string = f"{self.current_profile}_{datetime.now().isoformat()}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def export_profile(self, export_path: str = None) -> str:
        """Export profile to a file"""
        if not export_path:
            export_path = f"{self.current_profile}_export_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(export_path, 'w') as f:
            json.dump(self.profile_data, f, indent=2, default=str)
        
        return export_path
    
    def import_profile(self, import_path: str, profile_name: str = None) -> bool:
        """Import a profile from a file"""
        try:
            with open(import_path, 'r') as f:
                imported_data = json.load(f)
            
            if profile_name:
                self.current_profile = profile_name
                self.profile_path = self.profiles_dir / f"{profile_name}.json"
            
            self.profile_data = imported_data
            self.profile_data['meta']['last_modified'] = datetime.now().isoformat()
            
            return self.save_profile()
        except Exception as e:
            print(f"❌ Error importing profile: {e}")
            return False
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get a summary of the current profile"""
        if not self.profile_data:
            return {}
        
        return {
            'profile_name': self.current_profile,
            'created': self.profile_data['meta'].get('created'),
            'last_modified': self.profile_data['meta'].get('last_modified'),
            'family_size': (self.profile_data['family'].get('adults', 0) + 
                          self.profile_data['family'].get('children', 0)),
            'location_type': self.profile_data['location'].get('type'),
            'preparedness_score': self.profile_data['risk_assessment'].get('preparedness_score', 0),
            'sections_needing_update': [s for s in self.cache_expiry if self.is_update_needed(s)]
        }


if __name__ == "__main__":
    # Test the profile manager
    manager = UserProfileManager()
    
    # List existing profiles
    profiles = manager.list_profiles()
    print(f"Existing profiles: {profiles}")
    
    # Load or create default profile
    profile = manager.load_profile("test_user")
    
    # Get summary
    summary = manager.get_profile_summary()
    print(f"\nProfile Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test saving family info
    family_info = {
        'adults': 2,
        'children': 1,
        'pets': 1,
        'special_needs': ['medication_dependent']
    }
    manager.save_family_info(family_info)
    
    # Test activity recording
    manager.record_activity('drill_completed', {'type': 'earthquake', 'score': 85})
    
    print(f"\n✅ Profile manager test complete!")
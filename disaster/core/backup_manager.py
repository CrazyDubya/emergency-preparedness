#!/usr/bin/env python3
"""
Backup Manager - Comprehensive Backup and Restore System
Handles automatic backups, versioning, and data recovery
"""

import os
import json
import shutil
import sqlite3
import zipfile
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import glob


class BackupManager:
    """Manage comprehensive backups of all preparedness data"""
    
    def __init__(self, data_dir: str = "preparedness_data"):
        """Initialize the backup manager"""
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup configuration
        self.config = {
            'max_backups': 10,  # Keep last 10 backups
            'auto_backup_interval': 24,  # Hours between auto-backups
            'compression': True,  # Compress backups
            'include_databases': True,
            'include_profiles': True,
            'include_configs': True,
            'verify_integrity': True
        }
        
        self.last_backup_time = self._get_last_backup_time()
    
    def create_backup(self, backup_name: str = None, 
                     description: str = None) -> Tuple[bool, str]:
        """Create a comprehensive backup of all data"""
        try:
            # Generate backup name if not provided
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}"
            
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)
            
            print(f"📦 Creating backup: {backup_name}")
            
            # Create backup manifest
            manifest = {
                'backup_name': backup_name,
                'timestamp': datetime.now().isoformat(),
                'description': description or "Manual backup",
                'version': '1.0',
                'contents': {},
                'checksums': {}
            }
            
            # Backup all databases
            if self.config['include_databases']:
                db_backup_dir = backup_path / "databases"
                db_backup_dir.mkdir(exist_ok=True)
                db_count = self._backup_databases(db_backup_dir, manifest)
                print(f"  ✓ Backed up {db_count} databases")
            
            # Backup all profiles
            if self.config['include_profiles']:
                profiles_backup_dir = backup_path / "profiles"
                if (self.data_dir / "profiles").exists():
                    shutil.copytree(
                        self.data_dir / "profiles",
                        profiles_backup_dir,
                        dirs_exist_ok=True
                    )
                    profile_count = len(list(profiles_backup_dir.glob("*.json")))
                    manifest['contents']['profiles'] = profile_count
                    print(f"  ✓ Backed up {profile_count} profiles")
            
            # Backup configuration files
            if self.config['include_configs']:
                config_backup_dir = backup_path / "configs"
                config_backup_dir.mkdir(exist_ok=True)
                config_count = self._backup_configs(config_backup_dir, manifest)
                print(f"  ✓ Backed up {config_count} configuration files")
            
            # Save manifest
            manifest_path = backup_path / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2, default=str)
            
            # Compress if configured
            if self.config['compression']:
                zip_path = self._compress_backup(backup_path, backup_name)
                shutil.rmtree(backup_path)  # Remove uncompressed version
                print(f"  ✓ Compressed backup to {zip_path.name}")
                final_path = str(zip_path)
            else:
                final_path = str(backup_path)
            
            # Verify integrity if configured
            if self.config['verify_integrity']:
                if self.verify_backup(backup_name):
                    print(f"  ✓ Backup integrity verified")
                else:
                    print(f"  ⚠️ Backup integrity check failed")
            
            # Clean old backups
            self._cleanup_old_backups()
            
            # Update last backup time
            self.last_backup_time = datetime.now()
            
            print(f"✅ Backup completed: {final_path}")
            return True, final_path
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False, str(e)
    
    def restore_backup(self, backup_name: str, 
                      restore_path: str = None,
                      selective: Dict[str, bool] = None) -> bool:
        """Restore data from a backup"""
        try:
            print(f"🔄 Restoring backup: {backup_name}")
            
            # Find backup
            backup_path = self._find_backup(backup_name)
            if not backup_path:
                print(f"❌ Backup not found: {backup_name}")
                return False
            
            # Extract if compressed
            if backup_path.suffix == '.zip':
                temp_dir = self.backup_dir / "temp_restore"
                temp_dir.mkdir(exist_ok=True)
                with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                backup_path = temp_dir / backup_name
            
            # Load manifest
            manifest_path = backup_path / "manifest.json"
            if not manifest_path.exists():
                print(f"❌ Backup manifest not found")
                return False
            
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Set restore path
            if not restore_path:
                restore_path = self.data_dir
            else:
                restore_path = Path(restore_path)
            
            # Determine what to restore
            if not selective:
                selective = {
                    'databases': True,
                    'profiles': True,
                    'configs': True
                }
            
            # Create backup of current data before restore
            print("  Creating safety backup of current data...")
            self.create_backup("pre_restore_safety", "Safety backup before restore")
            
            # Restore databases
            if selective.get('databases', True):
                db_source = backup_path / "databases"
                if db_source.exists():
                    self._restore_databases(db_source, restore_path)
                    print(f"  ✓ Restored databases")
            
            # Restore profiles
            if selective.get('profiles', True):
                profiles_source = backup_path / "profiles"
                if profiles_source.exists():
                    profiles_dest = restore_path / "profiles"
                    profiles_dest.mkdir(parents=True, exist_ok=True)
                    for profile in profiles_source.glob("*.json"):
                        shutil.copy2(profile, profiles_dest / profile.name)
                    print(f"  ✓ Restored profiles")
            
            # Restore configs
            if selective.get('configs', True):
                configs_source = backup_path / "configs"
                if configs_source.exists():
                    self._restore_configs(configs_source, restore_path)
                    print(f"  ✓ Restored configuration files")
            
            # Clean up temp directory if exists
            if 'temp_restore' in str(backup_path):
                shutil.rmtree(backup_path.parent)
            
            print(f"✅ Restore completed from: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, any]]:
        """List all available backups with details"""
        backups = []
        
        # Check for compressed backups
        for backup_file in self.backup_dir.glob("backup_*.zip"):
            try:
                # Extract manifest from zip
                with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                    with zip_ref.open('manifest.json') as manifest_file:
                        manifest = json.load(manifest_file)
                
                backups.append({
                    'name': backup_file.stem,
                    'path': str(backup_file),
                    'size': backup_file.stat().st_size,
                    'timestamp': manifest.get('timestamp'),
                    'description': manifest.get('description'),
                    'compressed': True
                })
            except:
                continue
        
        # Check for uncompressed backups
        for backup_dir in self.backup_dir.glob("backup_*"):
            if backup_dir.is_dir():
                manifest_path = backup_dir / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    
                    # Calculate directory size
                    size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                    
                    backups.append({
                        'name': backup_dir.name,
                        'path': str(backup_dir),
                        'size': size,
                        'timestamp': manifest.get('timestamp'),
                        'description': manifest.get('description'),
                        'compressed': False
                    })
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return backups
    
    def verify_backup(self, backup_name: str) -> bool:
        """Verify backup integrity"""
        try:
            backup_path = self._find_backup(backup_name)
            if not backup_path:
                return False
            
            # Extract if compressed
            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                    # Test zip integrity
                    bad_files = zip_ref.testzip()
                    if bad_files:
                        print(f"  ⚠️ Corrupted files in backup: {bad_files}")
                        return False
            else:
                # Check if manifest exists
                manifest_path = backup_path / "manifest.json"
                if not manifest_path.exists():
                    return False
                
                # Verify manifest is valid JSON
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                # Check if listed contents exist
                if 'databases' in manifest.get('contents', {}):
                    db_dir = backup_path / "databases"
                    if not db_dir.exists():
                        return False
            
            return True
            
        except Exception:
            return False
    
    def auto_backup_needed(self) -> bool:
        """Check if automatic backup is needed"""
        if not self.last_backup_time:
            return True
        
        hours_since_backup = (datetime.now() - self.last_backup_time).total_seconds() / 3600
        return hours_since_backup >= self.config['auto_backup_interval']
    
    def perform_auto_backup(self) -> bool:
        """Perform automatic backup if needed"""
        if self.auto_backup_needed():
            success, _ = self.create_backup(
                description="Automatic scheduled backup"
            )
            return success
        return False
    
    def _backup_databases(self, db_backup_dir: Path, manifest: Dict) -> int:
        """Backup all SQLite databases"""
        count = 0
        manifest['contents']['databases'] = {}
        
        for db_file in self.data_dir.glob("*.db"):
            try:
                # Create backup using SQLite backup API
                source_conn = sqlite3.connect(db_file)
                backup_db_path = db_backup_dir / db_file.name
                backup_conn = sqlite3.connect(backup_db_path)
                
                with backup_conn:
                    source_conn.backup(backup_conn)
                
                source_conn.close()
                backup_conn.close()
                
                # Calculate checksum
                checksum = self._calculate_checksum(backup_db_path)
                manifest['checksums'][db_file.name] = checksum
                manifest['contents']['databases'][db_file.name] = backup_db_path.stat().st_size
                
                count += 1
            except Exception as e:
                print(f"    ⚠️ Failed to backup {db_file.name}: {e}")
        
        return count
    
    def _restore_databases(self, db_source: Path, restore_path: Path) -> None:
        """Restore SQLite databases"""
        for db_file in db_source.glob("*.db"):
            dest_path = restore_path / db_file.name
            shutil.copy2(db_file, dest_path)
    
    def _backup_configs(self, config_backup_dir: Path, manifest: Dict) -> int:
        """Backup configuration files"""
        count = 0
        config_patterns = ['*.json', '*.yaml', '*.yml', '*.ini', '*.conf']
        
        for pattern in config_patterns:
            for config_file in self.data_dir.glob(pattern):
                if config_file.name != 'manifest.json':  # Skip manifest files
                    shutil.copy2(config_file, config_backup_dir / config_file.name)
                    count += 1
        
        manifest['contents']['configs'] = count
        return count
    
    def _restore_configs(self, config_source: Path, restore_path: Path) -> None:
        """Restore configuration files"""
        for config_file in config_source.glob("*"):
            if config_file.is_file():
                shutil.copy2(config_file, restore_path / config_file.name)
    
    def _compress_backup(self, backup_path: Path, backup_name: str) -> Path:
        """Compress backup directory to zip file"""
        zip_path = self.backup_dir / f"{backup_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in backup_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(backup_path.parent)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    def _cleanup_old_backups(self) -> None:
        """Remove old backups exceeding max_backups limit"""
        backups = self.list_backups()
        
        if len(backups) > self.config['max_backups']:
            # Remove oldest backups
            for backup in backups[self.config['max_backups']:]:
                backup_path = Path(backup['path'])
                if backup_path.exists():
                    if backup_path.is_dir():
                        shutil.rmtree(backup_path)
                    else:
                        backup_path.unlink()
                    print(f"  Removed old backup: {backup['name']}")
    
    def _find_backup(self, backup_name: str) -> Optional[Path]:
        """Find backup by name"""
        # Check for compressed backup
        zip_path = self.backup_dir / f"{backup_name}.zip"
        if zip_path.exists():
            return zip_path
        
        # Check for uncompressed backup
        dir_path = self.backup_dir / backup_name
        if dir_path.exists():
            return dir_path
        
        return None
    
    def _get_last_backup_time(self) -> Optional[datetime]:
        """Get timestamp of last backup"""
        backups = self.list_backups()
        if backups:
            try:
                return datetime.fromisoformat(backups[0]['timestamp'])
            except:
                pass
        return None
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of a file"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()
    
    def export_backup(self, backup_name: str, export_path: str) -> bool:
        """Export a backup to external location"""
        try:
            backup_path = self._find_backup(backup_name)
            if not backup_path:
                print(f"❌ Backup not found: {backup_name}")
                return False
            
            shutil.copy2(backup_path, export_path)
            print(f"✅ Backup exported to: {export_path}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False


if __name__ == "__main__":
    # Test the backup manager
    manager = BackupManager()
    
    # List existing backups
    print("📋 Existing backups:")
    backups = manager.list_backups()
    for backup in backups[:5]:  # Show only first 5
        size_mb = backup['size'] / 1024 / 1024
        print(f"  • {backup['name']} ({size_mb:.2f} MB) - {backup['description']}")
    
    # Create a test backup
    print("\nCreating test backup...")
    success, path = manager.create_backup("test_backup", "Test backup for verification")
    
    if success:
        # Verify the backup
        print("\nVerifying backup...")
        if manager.verify_backup("test_backup"):
            print("✅ Backup verification passed")
        else:
            print("❌ Backup verification failed")
    
    print("\n✅ Backup manager test complete!")
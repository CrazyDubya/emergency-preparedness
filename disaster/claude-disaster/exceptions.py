#!/usr/bin/env python3
"""
Custom exceptions for the Emergency Preparedness System
Provides a comprehensive hierarchy of exceptions for proper error handling
"""

from typing import Optional, Dict, Any
from datetime import datetime


class EmergencySystemError(Exception):
    """Base exception for all Emergency Preparedness System errors"""

    def __init__(self, message: str, error_code: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/API responses"""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "timestamp": self.timestamp
        }


# Database Exceptions
class DatabaseError(EmergencySystemError):
    """Base exception for database-related errors"""

    def __init__(self, message: str, db_path: Optional[str] = None,
                 operation: Optional[str] = None):
        super().__init__(
            message,
            error_code="DB_ERROR",
            details={"db_path": db_path, "operation": operation}
        )


class DatabaseConnectionError(DatabaseError):
    """Failed to connect to database"""

    def __init__(self, db_path: str, original_error: Optional[Exception] = None):
        super().__init__(
            f"Failed to connect to database: {db_path}",
            db_path=db_path,
            operation="connect"
        )
        self.error_code = "DB_CONNECTION_ERROR"
        self.details["original_error"] = str(original_error) if original_error else None


class DatabaseQueryError(DatabaseError):
    """Database query execution failed"""

    def __init__(self, query: str, db_path: Optional[str] = None,
                 original_error: Optional[Exception] = None):
        # Truncate query for safety
        safe_query = query[:200] + "..." if len(query) > 200 else query
        super().__init__(
            f"Query execution failed: {safe_query}",
            db_path=db_path,
            operation="query"
        )
        self.error_code = "DB_QUERY_ERROR"
        self.details["original_error"] = str(original_error) if original_error else None


class DatabaseIntegrityError(DatabaseError):
    """Database integrity constraint violation"""

    def __init__(self, constraint: str, db_path: Optional[str] = None):
        super().__init__(
            f"Integrity constraint violated: {constraint}",
            db_path=db_path,
            operation="integrity_check"
        )
        self.error_code = "DB_INTEGRITY_ERROR"


# API and Network Exceptions
class NetworkError(EmergencySystemError):
    """Base exception for network-related errors"""

    def __init__(self, message: str, url: Optional[str] = None,
                 status_code: Optional[int] = None):
        super().__init__(
            message,
            error_code="NETWORK_ERROR",
            details={"url": url, "status_code": status_code}
        )


class APIConnectionError(NetworkError):
    """Failed to connect to external API"""

    def __init__(self, api_name: str, url: str,
                 original_error: Optional[Exception] = None):
        super().__init__(
            f"Failed to connect to {api_name} API: {url}",
            url=url
        )
        self.error_code = "API_CONNECTION_ERROR"
        self.details["api_name"] = api_name
        self.details["original_error"] = str(original_error) if original_error else None


class APITimeoutError(NetworkError):
    """API request timed out"""

    def __init__(self, api_name: str, url: str, timeout_seconds: float):
        super().__init__(
            f"{api_name} API request timed out after {timeout_seconds}s",
            url=url
        )
        self.error_code = "API_TIMEOUT_ERROR"
        self.details["api_name"] = api_name
        self.details["timeout_seconds"] = timeout_seconds


class APIResponseError(NetworkError):
    """Invalid or unexpected API response"""

    def __init__(self, api_name: str, status_code: int,
                 response_body: Optional[str] = None):
        super().__init__(
            f"{api_name} API returned error status: {status_code}",
            status_code=status_code
        )
        self.error_code = "API_RESPONSE_ERROR"
        self.details["api_name"] = api_name
        # Truncate response body for safety
        if response_body:
            self.details["response_body"] = response_body[:500]


class OfflineModeError(NetworkError):
    """System is in offline mode, network operation not available"""

    def __init__(self, operation: str):
        super().__init__(
            f"Cannot perform '{operation}' - system is in offline mode"
        )
        self.error_code = "OFFLINE_MODE_ERROR"
        self.details["operation"] = operation


# Drill and Simulation Exceptions
class DrillError(EmergencySystemError):
    """Base exception for drill-related errors"""

    def __init__(self, message: str, drill_type: Optional[str] = None,
                 scenario_id: Optional[int] = None):
        super().__init__(
            message,
            error_code="DRILL_ERROR",
            details={"drill_type": drill_type, "scenario_id": scenario_id}
        )


class DrillScenarioNotFoundError(DrillError):
    """Drill scenario not found in database"""

    def __init__(self, scenario_id: int):
        super().__init__(
            f"Drill scenario not found: ID {scenario_id}",
            scenario_id=scenario_id
        )
        self.error_code = "DRILL_SCENARIO_NOT_FOUND"


class DrillAlreadyRunningError(DrillError):
    """A drill is already in progress"""

    def __init__(self, current_drill_type: str):
        super().__init__(
            f"A {current_drill_type} drill is already in progress",
            drill_type=current_drill_type
        )
        self.error_code = "DRILL_ALREADY_RUNNING"


class DrillValidationError(DrillError):
    """Drill parameters validation failed"""

    def __init__(self, message: str, invalid_field: Optional[str] = None):
        super().__init__(message)
        self.error_code = "DRILL_VALIDATION_ERROR"
        self.details["invalid_field"] = invalid_field


# Configuration and Profile Exceptions
class ConfigurationError(EmergencySystemError):
    """Configuration-related errors"""

    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message,
            error_code="CONFIG_ERROR",
            details={"config_key": config_key}
        )


class ProfileError(EmergencySystemError):
    """Profile management errors"""

    def __init__(self, message: str, profile_name: Optional[str] = None):
        super().__init__(
            message,
            error_code="PROFILE_ERROR",
            details={"profile_name": profile_name}
        )


class ProfileNotFoundError(ProfileError):
    """User profile not found"""

    def __init__(self, profile_name: str):
        super().__init__(
            f"Profile not found: {profile_name}",
            profile_name=profile_name
        )
        self.error_code = "PROFILE_NOT_FOUND"


class ProfileCorruptedError(ProfileError):
    """User profile data is corrupted"""

    def __init__(self, profile_name: str, reason: Optional[str] = None):
        super().__init__(
            f"Profile corrupted: {profile_name}" + (f" - {reason}" if reason else ""),
            profile_name=profile_name
        )
        self.error_code = "PROFILE_CORRUPTED"
        self.details["reason"] = reason


# Supply and Inventory Exceptions
class SupplyError(EmergencySystemError):
    """Supply management errors"""

    def __init__(self, message: str, item_id: Optional[int] = None,
                 category: Optional[str] = None):
        super().__init__(
            message,
            error_code="SUPPLY_ERROR",
            details={"item_id": item_id, "category": category}
        )


class SupplyNotFoundError(SupplyError):
    """Supply item not found"""

    def __init__(self, item_id: int):
        super().__init__(
            f"Supply item not found: ID {item_id}",
            item_id=item_id
        )
        self.error_code = "SUPPLY_NOT_FOUND"


class InsufficientSupplyError(SupplyError):
    """Insufficient supply quantity"""

    def __init__(self, item_name: str, required: float, available: float):
        super().__init__(
            f"Insufficient {item_name}: need {required}, have {available}"
        )
        self.error_code = "INSUFFICIENT_SUPPLY"
        self.details["item_name"] = item_name
        self.details["required"] = required
        self.details["available"] = available


# Alert and Monitoring Exceptions
class AlertError(EmergencySystemError):
    """Alert system errors"""

    def __init__(self, message: str, alert_type: Optional[str] = None):
        super().__init__(
            message,
            error_code="ALERT_ERROR",
            details={"alert_type": alert_type}
        )


class AlertFetchError(AlertError):
    """Failed to fetch alerts from external source"""

    def __init__(self, source: str, original_error: Optional[Exception] = None):
        super().__init__(
            f"Failed to fetch alerts from {source}"
        )
        self.error_code = "ALERT_FETCH_ERROR"
        self.details["source"] = source
        self.details["original_error"] = str(original_error) if original_error else None


# Authentication and Security Exceptions
class AuthenticationError(EmergencySystemError):
    """Authentication-related errors"""

    def __init__(self, message: str):
        super().__init__(message, error_code="AUTH_ERROR")


class InvalidAPIKeyError(AuthenticationError):
    """Invalid or missing API key"""

    def __init__(self):
        super().__init__("Invalid or missing API key")
        self.error_code = "INVALID_API_KEY"


class TokenExpiredError(AuthenticationError):
    """Authentication token has expired"""

    def __init__(self):
        super().__init__("Authentication token has expired")
        self.error_code = "TOKEN_EXPIRED"


class PermissionDeniedError(AuthenticationError):
    """User lacks permission for requested operation"""

    def __init__(self, operation: str, required_role: Optional[str] = None):
        super().__init__(f"Permission denied for operation: {operation}")
        self.error_code = "PERMISSION_DENIED"
        self.details["operation"] = operation
        self.details["required_role"] = required_role


# Backup and Recovery Exceptions
class BackupError(EmergencySystemError):
    """Backup operation errors"""

    def __init__(self, message: str, backup_path: Optional[str] = None):
        super().__init__(
            message,
            error_code="BACKUP_ERROR",
            details={"backup_path": backup_path}
        )


class BackupNotFoundError(BackupError):
    """Backup file not found"""

    def __init__(self, backup_path: str):
        super().__init__(
            f"Backup not found: {backup_path}",
            backup_path=backup_path
        )
        self.error_code = "BACKUP_NOT_FOUND"


class BackupCorruptedError(BackupError):
    """Backup file is corrupted"""

    def __init__(self, backup_path: str, reason: Optional[str] = None):
        super().__init__(
            f"Backup corrupted: {backup_path}" + (f" - {reason}" if reason else ""),
            backup_path=backup_path
        )
        self.error_code = "BACKUP_CORRUPTED"
        self.details["reason"] = reason


class RestoreError(BackupError):
    """Failed to restore from backup"""

    def __init__(self, backup_path: str, reason: str):
        super().__init__(
            f"Failed to restore from {backup_path}: {reason}",
            backup_path=backup_path
        )
        self.error_code = "RESTORE_ERROR"
        self.details["reason"] = reason


# Knowledge Base Exceptions
class KnowledgeBaseError(EmergencySystemError):
    """Knowledge base related errors"""

    def __init__(self, message: str, query: Optional[str] = None):
        super().__init__(
            message,
            error_code="KB_ERROR",
            details={"query": query}
        )


class SearchError(KnowledgeBaseError):
    """Search operation failed"""

    def __init__(self, query: str, reason: Optional[str] = None):
        super().__init__(
            f"Search failed for query: {query}" + (f" - {reason}" if reason else ""),
            query=query
        )
        self.error_code = "SEARCH_ERROR"
        self.details["reason"] = reason


class IndexError(KnowledgeBaseError):
    """Index operation failed"""

    def __init__(self, operation: str, reason: str):
        super().__init__(f"Index {operation} failed: {reason}")
        self.error_code = "INDEX_ERROR"
        self.details["operation"] = operation
        self.details["reason"] = reason

#!/usr/bin/env python3
"""
Unit tests for the exceptions module
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from datetime import datetime

from exceptions import (
    EmergencySystemError,
    DatabaseError, DatabaseConnectionError, DatabaseQueryError,
    NetworkError, APIConnectionError, APITimeoutError, APIResponseError,
    OfflineModeError,
    DrillError, DrillScenarioNotFoundError, DrillAlreadyRunningError,
    DrillValidationError,
    ProfileError, ProfileNotFoundError, ProfileCorruptedError,
    SupplyError, SupplyNotFoundError, InsufficientSupplyError,
    AlertError, AlertFetchError,
    AuthenticationError, InvalidAPIKeyError, TokenExpiredError,
    PermissionDeniedError,
    BackupError, BackupNotFoundError, BackupCorruptedError,
    KnowledgeBaseError, SearchError
)


class TestBaseException(unittest.TestCase):
    """Test base EmergencySystemError"""

    def test_basic_creation(self):
        """Test basic exception creation"""
        error = EmergencySystemError("Test error")
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.error_code, "UNKNOWN_ERROR")
        self.assertEqual(error.details, {})
        self.assertIsNotNone(error.timestamp)

    def test_with_error_code(self):
        """Test exception with custom error code"""
        error = EmergencySystemError("Test error", error_code="CUSTOM_ERROR")
        self.assertEqual(error.error_code, "CUSTOM_ERROR")

    def test_with_details(self):
        """Test exception with details"""
        details = {"key": "value", "number": 42}
        error = EmergencySystemError("Test error", details=details)
        self.assertEqual(error.details, details)

    def test_to_dict(self):
        """Test conversion to dictionary"""
        error = EmergencySystemError(
            "Test error",
            error_code="TEST_CODE",
            details={"foo": "bar"}
        )
        result = error.to_dict()

        self.assertEqual(result["error"], "EmergencySystemError")
        self.assertEqual(result["message"], "Test error")
        self.assertEqual(result["error_code"], "TEST_CODE")
        self.assertEqual(result["details"]["foo"], "bar")
        self.assertIn("timestamp", result)

    def test_str_representation(self):
        """Test string representation"""
        error = EmergencySystemError("Test error message")
        self.assertEqual(str(error), "Test error message")


class TestDatabaseExceptions(unittest.TestCase):
    """Test database-related exceptions"""

    def test_database_connection_error(self):
        """Test DatabaseConnectionError"""
        error = DatabaseConnectionError("/path/to/db.sqlite")
        self.assertIn("/path/to/db.sqlite", error.message)
        self.assertEqual(error.error_code, "DB_CONNECTION_ERROR")
        self.assertEqual(error.details["db_path"], "/path/to/db.sqlite")

    def test_database_connection_with_original_error(self):
        """Test DatabaseConnectionError with original exception"""
        original = Exception("Original error")
        error = DatabaseConnectionError("/path/to/db.sqlite", original)
        self.assertEqual(error.details["original_error"], "Original error")

    def test_database_query_error(self):
        """Test DatabaseQueryError"""
        error = DatabaseQueryError("SELECT * FROM users", "/path/to/db.sqlite")
        self.assertEqual(error.error_code, "DB_QUERY_ERROR")
        self.assertIn("SELECT * FROM users", error.message)

    def test_database_query_error_truncates_long_query(self):
        """Test that long queries are truncated"""
        long_query = "SELECT " + "x" * 300
        error = DatabaseQueryError(long_query)
        self.assertLessEqual(len(error.message), 250)  # Truncated


class TestNetworkExceptions(unittest.TestCase):
    """Test network-related exceptions"""

    def test_api_connection_error(self):
        """Test APIConnectionError"""
        error = APIConnectionError("Weather API", "https://api.example.com")
        self.assertIn("Weather API", error.message)
        self.assertEqual(error.details["api_name"], "Weather API")
        self.assertEqual(error.details["url"], "https://api.example.com")

    def test_api_timeout_error(self):
        """Test APITimeoutError"""
        error = APITimeoutError("NWS", "https://api.weather.gov", 10.0)
        self.assertIn("timed out", error.message)
        self.assertEqual(error.details["timeout_seconds"], 10.0)

    def test_api_response_error(self):
        """Test APIResponseError"""
        error = APIResponseError("Test API", 500, "Internal Server Error")
        self.assertEqual(error.details["status_code"], 500)
        self.assertIn("500", error.message)

    def test_offline_mode_error(self):
        """Test OfflineModeError"""
        error = OfflineModeError("fetch_weather")
        self.assertIn("offline mode", error.message)
        self.assertEqual(error.details["operation"], "fetch_weather")


class TestDrillExceptions(unittest.TestCase):
    """Test drill-related exceptions"""

    def test_drill_scenario_not_found(self):
        """Test DrillScenarioNotFoundError"""
        error = DrillScenarioNotFoundError(42)
        self.assertIn("42", error.message)
        self.assertEqual(error.error_code, "DRILL_SCENARIO_NOT_FOUND")
        self.assertEqual(error.details["scenario_id"], 42)

    def test_drill_already_running(self):
        """Test DrillAlreadyRunningError"""
        error = DrillAlreadyRunningError("earthquake")
        self.assertIn("earthquake", error.message)
        self.assertEqual(error.error_code, "DRILL_ALREADY_RUNNING")

    def test_drill_validation_error(self):
        """Test DrillValidationError"""
        error = DrillValidationError("Invalid duration", "duration")
        self.assertEqual(error.details["invalid_field"], "duration")


class TestProfileExceptions(unittest.TestCase):
    """Test profile-related exceptions"""

    def test_profile_not_found(self):
        """Test ProfileNotFoundError"""
        error = ProfileNotFoundError("test_profile")
        self.assertIn("test_profile", error.message)
        self.assertEqual(error.error_code, "PROFILE_NOT_FOUND")

    def test_profile_corrupted(self):
        """Test ProfileCorruptedError"""
        error = ProfileCorruptedError("test_profile", "Invalid JSON")
        self.assertIn("Invalid JSON", error.message)
        self.assertEqual(error.details["reason"], "Invalid JSON")


class TestSupplyExceptions(unittest.TestCase):
    """Test supply-related exceptions"""

    def test_supply_not_found(self):
        """Test SupplyNotFoundError"""
        error = SupplyNotFoundError(123)
        self.assertIn("123", error.message)
        self.assertEqual(error.error_code, "SUPPLY_NOT_FOUND")

    def test_insufficient_supply(self):
        """Test InsufficientSupplyError"""
        error = InsufficientSupplyError("Water", required=10.0, available=5.0)
        self.assertIn("Water", error.message)
        self.assertEqual(error.details["required"], 10.0)
        self.assertEqual(error.details["available"], 5.0)


class TestAuthenticationExceptions(unittest.TestCase):
    """Test authentication-related exceptions"""

    def test_invalid_api_key(self):
        """Test InvalidAPIKeyError"""
        error = InvalidAPIKeyError()
        self.assertEqual(error.error_code, "INVALID_API_KEY")

    def test_token_expired(self):
        """Test TokenExpiredError"""
        error = TokenExpiredError()
        self.assertEqual(error.error_code, "TOKEN_EXPIRED")

    def test_permission_denied(self):
        """Test PermissionDeniedError"""
        error = PermissionDeniedError("delete_user", "admin")
        self.assertIn("delete_user", error.message)
        self.assertEqual(error.details["required_role"], "admin")


class TestBackupExceptions(unittest.TestCase):
    """Test backup-related exceptions"""

    def test_backup_not_found(self):
        """Test BackupNotFoundError"""
        error = BackupNotFoundError("/path/to/backup.zip")
        self.assertIn("/path/to/backup.zip", error.message)

    def test_backup_corrupted(self):
        """Test BackupCorruptedError"""
        error = BackupCorruptedError("/path/to/backup.zip", "CRC mismatch")
        self.assertIn("CRC mismatch", error.message)


class TestKnowledgeBaseExceptions(unittest.TestCase):
    """Test knowledge base exceptions"""

    def test_search_error(self):
        """Test SearchError"""
        error = SearchError("water purification", "Index not found")
        self.assertIn("water purification", error.message)
        self.assertEqual(error.details["reason"], "Index not found")


if __name__ == "__main__":
    unittest.main()

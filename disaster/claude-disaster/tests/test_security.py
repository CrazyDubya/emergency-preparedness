#!/usr/bin/env python3
"""
Unit tests for the security module
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import tempfile
import shutil
import os
from datetime import datetime, timedelta
from unittest.mock import patch

from security import (
    SecureConfig, APIKeyConfig, JWTManager, RateLimiter,
    get_secure_config, get_rate_limiter
)
from exceptions import InvalidAPIKeyError, TokenExpiredError, AuthenticationError


class TestAPIKeyConfig(unittest.TestCase):
    """Test APIKeyConfig dataclass"""

    def test_default_values(self):
        """Test default configuration values"""
        config = APIKeyConfig(
            key_hash="abc123",
            user_id="test_user",
            role="user"
        )

        self.assertEqual(config.key_hash, "abc123")
        self.assertEqual(config.user_id, "test_user")
        self.assertEqual(config.role, "user")
        self.assertEqual(config.profile, "default")
        self.assertEqual(config.rate_limit, 100)
        self.assertTrue(config.enabled)
        self.assertEqual(config.permissions, [])

    def test_custom_values(self):
        """Test custom configuration values"""
        config = APIKeyConfig(
            key_hash="xyz789",
            user_id="admin_user",
            role="admin",
            profile="admin_profile",
            rate_limit=1000,
            enabled=True,
            permissions=["read", "write", "delete"]
        )

        self.assertEqual(config.rate_limit, 1000)
        self.assertEqual(config.permissions, ["read", "write", "delete"])


class TestSecureConfig(unittest.TestCase):
    """Test SecureConfig class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        # Clear environment variables
        for key in ["EMERGENCY_API_SECRET_KEY", "EMERGENCY_API_KEYS_FILE",
                    "EMERGENCY_ALLOWED_ORIGINS", "EMERGENCY_DEBUG_MODE"]:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generates_secret_key_if_not_set(self):
        """Test that secret key is generated if not in environment"""
        config = SecureConfig(config_dir=self.temp_dir)

        self.assertIsNotNone(config.secret_key)
        self.assertGreater(len(config.secret_key), 20)

    def test_uses_environment_secret_key(self):
        """Test that environment secret key is used"""
        os.environ["EMERGENCY_API_SECRET_KEY"] = "test_secret_key_123"

        config = SecureConfig(config_dir=self.temp_dir)
        self.assertEqual(config.secret_key, "test_secret_key_123")

        del os.environ["EMERGENCY_API_SECRET_KEY"]

    def test_hash_api_key(self):
        """Test API key hashing"""
        hash1 = SecureConfig.hash_api_key("test_key_123")
        hash2 = SecureConfig.hash_api_key("test_key_123")
        hash3 = SecureConfig.hash_api_key("different_key")

        # Same key produces same hash
        self.assertEqual(hash1, hash2)
        # Different key produces different hash
        self.assertNotEqual(hash1, hash3)
        # Hash is a valid hex string
        self.assertEqual(len(hash1), 64)  # SHA-256 produces 64 hex chars

    def test_generate_api_key(self):
        """Test API key generation"""
        config = SecureConfig(config_dir=self.temp_dir)

        plain_key = config.generate_api_key("test_user", "user")

        # Key should be a valid string
        self.assertIsNotNone(plain_key)
        self.assertGreater(len(plain_key), 20)

    def test_validate_api_key_success(self):
        """Test successful API key validation"""
        config = SecureConfig(config_dir=self.temp_dir)

        plain_key = config.generate_api_key("test_user", "admin", permissions=["*"])
        result = config.validate_api_key(plain_key)

        self.assertEqual(result.user_id, "test_user")
        self.assertEqual(result.role, "admin")
        self.assertEqual(result.permissions, ["*"])

    def test_validate_api_key_invalid(self):
        """Test invalid API key validation"""
        config = SecureConfig(config_dir=self.temp_dir)

        with self.assertRaises(InvalidAPIKeyError):
            config.validate_api_key("invalid_key_12345")

    def test_validate_api_key_disabled(self):
        """Test disabled API key validation"""
        config = SecureConfig(config_dir=self.temp_dir)

        plain_key = config.generate_api_key("test_user", "user")

        # Disable the key
        for key_id, key_config in config._api_keys.items():
            if key_config.user_id == "test_user":
                key_config.enabled = False
                break

        with self.assertRaises(InvalidAPIKeyError):
            config.validate_api_key(plain_key)

    def test_validate_api_key_expired(self):
        """Test expired API key validation"""
        config = SecureConfig(config_dir=self.temp_dir)

        # Generate key that expires in -1 days (already expired)
        plain_key = config.generate_api_key("test_user", "user", expires_days=-1)

        # Manually set expiration to past
        for key_id, key_config in config._api_keys.items():
            if key_config.user_id == "test_user":
                key_config.expires_at = (datetime.now() - timedelta(days=1)).isoformat()
                break

        with self.assertRaises(InvalidAPIKeyError):
            config.validate_api_key(plain_key)

    def test_allowed_origins_from_environment(self):
        """Test allowed origins from environment"""
        os.environ["EMERGENCY_ALLOWED_ORIGINS"] = "http://localhost:3000,https://example.com"

        config = SecureConfig(config_dir=self.temp_dir)
        origins = config.allowed_origins

        self.assertIn("http://localhost:3000", origins)
        self.assertIn("https://example.com", origins)

        del os.environ["EMERGENCY_ALLOWED_ORIGINS"]

    def test_debug_mode_from_environment(self):
        """Test debug mode from environment"""
        config = SecureConfig(config_dir=self.temp_dir)
        self.assertFalse(config.is_debug_mode)

        os.environ["EMERGENCY_DEBUG_MODE"] = "true"
        config2 = SecureConfig(config_dir=os.path.join(self.temp_dir, "config2"))
        self.assertTrue(config2.is_debug_mode)

        del os.environ["EMERGENCY_DEBUG_MODE"]


class TestJWTManager(unittest.TestCase):
    """Test JWTManager class"""

    def setUp(self):
        """Set up test fixtures"""
        try:
            self.jwt_manager = JWTManager(
                secret_key="test_secret_key_for_testing",
                access_token_expire_minutes=60,
                refresh_token_expire_days=7
            )
            self.jwt_available = True
        except Exception:
            self.jwt_available = False

    def test_create_access_token(self):
        """Test access token creation"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        token = self.jwt_manager.create_access_token(
            user_id="test_user",
            role="admin",
            permissions=["read", "write"]
        )

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 50)

    def test_create_refresh_token(self):
        """Test refresh token creation"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        token = self.jwt_manager.create_refresh_token("test_user")

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)

    def test_verify_access_token(self):
        """Test access token verification"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        token = self.jwt_manager.create_access_token(
            user_id="test_user",
            role="admin"
        )

        payload = self.jwt_manager.verify_token(token, "access")

        self.assertEqual(payload["sub"], "test_user")
        self.assertEqual(payload["role"], "admin")
        self.assertEqual(payload["type"], "access")

    def test_verify_refresh_token(self):
        """Test refresh token verification"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        token = self.jwt_manager.create_refresh_token("test_user")

        payload = self.jwt_manager.verify_token(token, "refresh")

        self.assertEqual(payload["sub"], "test_user")
        self.assertEqual(payload["type"], "refresh")

    def test_verify_wrong_token_type_raises(self):
        """Test that wrong token type raises error"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        access_token = self.jwt_manager.create_access_token(
            user_id="test_user",
            role="user"
        )

        with self.assertRaises(AuthenticationError):
            self.jwt_manager.verify_token(access_token, "refresh")

    def test_verify_invalid_token_raises(self):
        """Test that invalid token raises error"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        with self.assertRaises(AuthenticationError):
            self.jwt_manager.verify_token("invalid.token.here", "access")

    def test_refresh_access_token(self):
        """Test refreshing access token"""
        if not self.jwt_available:
            self.skipTest("JWT library not available")

        refresh_token = self.jwt_manager.create_refresh_token("test_user")

        new_access_token = self.jwt_manager.refresh_access_token(
            refresh_token,
            role="user",
            permissions=["read"]
        )

        payload = self.jwt_manager.verify_token(new_access_token, "access")
        self.assertEqual(payload["sub"], "test_user")


class TestRateLimiter(unittest.TestCase):
    """Test RateLimiter class"""

    def setUp(self):
        """Set up test fixtures"""
        self.limiter = RateLimiter()

    def test_allows_requests_under_limit(self):
        """Test that requests under limit are allowed"""
        for i in range(5):
            self.assertTrue(self.limiter.is_allowed("user1", limit=10))

    def test_blocks_requests_over_limit(self):
        """Test that requests over limit are blocked"""
        for i in range(10):
            self.limiter.is_allowed("user2", limit=10)

        self.assertFalse(self.limiter.is_allowed("user2", limit=10))

    def test_different_keys_tracked_separately(self):
        """Test that different keys are tracked separately"""
        # Use up user1's limit
        for i in range(10):
            self.limiter.is_allowed("user1", limit=10)

        # user2 should still be allowed
        self.assertTrue(self.limiter.is_allowed("user2", limit=10))

    def test_get_remaining(self):
        """Test getting remaining requests"""
        initial = self.limiter.get_remaining("user3", limit=10)
        self.assertEqual(initial, 10)

        self.limiter.is_allowed("user3", limit=10)
        remaining = self.limiter.get_remaining("user3", limit=10)
        self.assertEqual(remaining, 9)

    def test_requests_expire_after_window(self):
        """Test that requests expire after time window"""
        import time

        # Use up the limit
        for i in range(5):
            self.limiter.is_allowed("user4", limit=5, window_seconds=1)

        self.assertFalse(self.limiter.is_allowed("user4", limit=5, window_seconds=1))

        # Wait for window to expire
        time.sleep(1.1)

        # Should be allowed again
        self.assertTrue(self.limiter.is_allowed("user4", limit=5, window_seconds=1))


if __name__ == "__main__":
    unittest.main()

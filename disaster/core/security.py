#!/usr/bin/env python3
"""
Security Configuration and Authentication
Provides secure API key management, JWT handling, and CORS configuration
"""

import os
import secrets
import hashlib
import hmac
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from functools import wraps

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

from exceptions import (
    AuthenticationError, InvalidAPIKeyError, TokenExpiredError,
    PermissionDeniedError, ConfigurationError
)

logger = logging.getLogger(__name__)


@dataclass
class APIKeyConfig:
    """Configuration for an API key"""
    key_hash: str  # Hashed API key (never store plain text)
    user_id: str
    role: str
    profile: str = "default"
    rate_limit: int = 100  # Requests per minute
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expires_at: Optional[str] = None
    enabled: bool = True
    permissions: List[str] = field(default_factory=list)


class SecureConfig:
    """
    Secure configuration management for API keys and secrets.

    Security features:
    - API keys are hashed (never stored in plaintext)
    - Secrets loaded from environment variables
    - Support for key rotation
    - Rate limiting configuration
    """

    # Environment variable names
    ENV_SECRET_KEY = "EMERGENCY_API_SECRET_KEY"
    ENV_API_KEYS_FILE = "EMERGENCY_API_KEYS_FILE"
    ENV_ALLOWED_ORIGINS = "EMERGENCY_ALLOWED_ORIGINS"
    ENV_DEBUG_MODE = "EMERGENCY_DEBUG_MODE"

    def __init__(self, config_dir: str = ".secure_config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._api_keys: Dict[str, APIKeyConfig] = {}
        self._secret_key: Optional[str] = None
        self._load_config()

    def _load_config(self):
        """Load configuration from environment and files"""
        # Load secret key from environment
        self._secret_key = os.environ.get(self.ENV_SECRET_KEY)

        if not self._secret_key:
            # Generate a new secret key if not set (for development only)
            secret_file = self.config_dir / "secret.key"
            if secret_file.exists():
                self._secret_key = secret_file.read_text().strip()
                logger.warning("Using stored secret key - set EMERGENCY_API_SECRET_KEY in production")
            else:
                self._secret_key = secrets.token_urlsafe(32)
                secret_file.write_text(self._secret_key)
                logger.warning(f"Generated new secret key - set EMERGENCY_API_SECRET_KEY in production")

        # Load API keys from file if specified
        api_keys_file = os.environ.get(self.ENV_API_KEYS_FILE)
        if api_keys_file and Path(api_keys_file).exists():
            self._load_api_keys_from_file(api_keys_file)
        else:
            # Load from default location
            default_keys_file = self.config_dir / "api_keys.json"
            if default_keys_file.exists():
                self._load_api_keys_from_file(str(default_keys_file))
            else:
                # Create default development keys
                self._create_default_keys()

    def _load_api_keys_from_file(self, filepath: str):
        """Load API keys from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            for key_id, key_data in data.get("api_keys", {}).items():
                self._api_keys[key_id] = APIKeyConfig(
                    key_hash=key_data["key_hash"],
                    user_id=key_data["user_id"],
                    role=key_data.get("role", "user"),
                    profile=key_data.get("profile", "default"),
                    rate_limit=key_data.get("rate_limit", 100),
                    created_at=key_data.get("created_at", datetime.now().isoformat()),
                    expires_at=key_data.get("expires_at"),
                    enabled=key_data.get("enabled", True),
                    permissions=key_data.get("permissions", [])
                )

            logger.info(f"Loaded {len(self._api_keys)} API keys from {filepath}")

        except Exception as e:
            logger.error(f"Failed to load API keys from {filepath}: {e}")
            raise ConfigurationError(f"Failed to load API keys: {e}")

    def _create_default_keys(self):
        """Create default development API keys"""
        logger.warning("Creating default development API keys - NOT FOR PRODUCTION")

        # Generate development keys
        dev_keys = {
            "dev_admin": self.generate_api_key("admin", "admin", permissions=["*"]),
            "dev_user": self.generate_api_key("user", "user", permissions=["read", "drill", "supply"]),
            "dev_gui": self.generate_api_key("gui", "user", permissions=["read", "drill", "supply", "alert"])
        }

        # Save keys to file for development use
        self._save_api_keys()

        # Log the plain text keys ONCE for development
        logger.warning("Development API keys created. Store these securely:")
        for key_id, plain_key in dev_keys.items():
            logger.warning(f"  {key_id}: {plain_key}")

    def _save_api_keys(self):
        """Save API keys to file (hashed)"""
        keys_file = self.config_dir / "api_keys.json"
        data = {
            "api_keys": {
                key_id: {
                    "key_hash": config.key_hash,
                    "user_id": config.user_id,
                    "role": config.role,
                    "profile": config.profile,
                    "rate_limit": config.rate_limit,
                    "created_at": config.created_at,
                    "expires_at": config.expires_at,
                    "enabled": config.enabled,
                    "permissions": config.permissions
                }
                for key_id, config in self._api_keys.items()
            },
            "updated_at": datetime.now().isoformat()
        }

        with open(keys_file, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    def generate_api_key(self, user_id: str, role: str = "user",
                        permissions: Optional[List[str]] = None,
                        rate_limit: int = 100,
                        expires_days: Optional[int] = None) -> str:
        """
        Generate a new API key

        Args:
            user_id: User identifier
            role: User role (admin, user, readonly)
            permissions: List of specific permissions
            rate_limit: Requests per minute
            expires_days: Days until expiration (None = never)

        Returns:
            Plain text API key (only returned once!)
        """
        # Generate secure random key
        plain_key = secrets.token_urlsafe(32)
        key_hash = self.hash_api_key(plain_key)
        key_id = f"{user_id}_{secrets.token_hex(4)}"

        expires_at = None
        if expires_days:
            expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat()

        self._api_keys[key_id] = APIKeyConfig(
            key_hash=key_hash,
            user_id=user_id,
            role=role,
            permissions=permissions or [],
            rate_limit=rate_limit,
            expires_at=expires_at
        )

        self._save_api_keys()
        logger.info(f"Generated new API key for user {user_id} (key_id: {key_id})")

        return plain_key

    def validate_api_key(self, api_key: str) -> APIKeyConfig:
        """
        Validate an API key and return its configuration

        Args:
            api_key: Plain text API key to validate

        Returns:
            APIKeyConfig if valid

        Raises:
            InvalidAPIKeyError: If key is invalid or expired
        """
        key_hash = self.hash_api_key(api_key)

        for key_id, config in self._api_keys.items():
            if hmac.compare_digest(config.key_hash, key_hash):
                # Check if enabled
                if not config.enabled:
                    logger.warning(f"Disabled API key used: {key_id}")
                    raise InvalidAPIKeyError()

                # Check expiration
                if config.expires_at:
                    if datetime.fromisoformat(config.expires_at) < datetime.now():
                        logger.warning(f"Expired API key used: {key_id}")
                        raise InvalidAPIKeyError()

                return config

        raise InvalidAPIKeyError()

    def revoke_api_key(self, key_id: str):
        """Revoke an API key"""
        if key_id in self._api_keys:
            self._api_keys[key_id].enabled = False
            self._save_api_keys()
            logger.info(f"Revoked API key: {key_id}")
        else:
            raise ConfigurationError(f"API key not found: {key_id}")

    @property
    def secret_key(self) -> str:
        """Get the JWT secret key"""
        return self._secret_key

    @property
    def allowed_origins(self) -> List[str]:
        """Get allowed CORS origins"""
        origins = os.environ.get(self.ENV_ALLOWED_ORIGINS, "")
        if origins:
            return [o.strip() for o in origins.split(",")]

        # Default to localhost only in development
        if os.environ.get(self.ENV_DEBUG_MODE, "false").lower() == "true":
            return ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"]

        # In production, require explicit configuration
        logger.warning("No CORS origins configured - defaulting to same-origin only")
        return []

    @property
    def is_debug_mode(self) -> bool:
        """Check if running in debug mode"""
        return os.environ.get(self.ENV_DEBUG_MODE, "false").lower() == "true"


class JWTManager:
    """
    JWT token management for authentication
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256",
                 access_token_expire_minutes: int = 60,
                 refresh_token_expire_days: int = 7):
        if not JWT_AVAILABLE:
            raise ConfigurationError("PyJWT library not installed")

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)

    def create_access_token(self, user_id: str, role: str,
                           permissions: List[str] = None,
                           additional_claims: Dict[str, Any] = None) -> str:
        """Create a new access token"""
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "role": role,
            "permissions": permissions or [],
            "iat": now,
            "exp": now + self.access_token_expire,
            "type": "access"
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token for obtaining new access tokens"""
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + self.refresh_token_expire,
            "type": "refresh",
            "jti": secrets.token_hex(16)  # Unique token ID
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """
        Verify and decode a JWT token

        Args:
            token: JWT token string
            token_type: Expected token type (access or refresh)

        Returns:
            Decoded token payload

        Raises:
            TokenExpiredError: If token has expired
            AuthenticationError: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if payload.get("type") != token_type:
                raise AuthenticationError(f"Invalid token type: expected {token_type}")

            return payload

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            raise AuthenticationError(f"Invalid token: {e}")

    def refresh_access_token(self, refresh_token: str, role: str,
                            permissions: List[str] = None) -> str:
        """Create a new access token using a refresh token"""
        payload = self.verify_token(refresh_token, "refresh")
        return self.create_access_token(payload["sub"], role, permissions)


def require_permission(permission: str):
    """
    Decorator to require a specific permission for an endpoint

    Usage:
        @require_permission("admin")
        def admin_endpoint():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This would be integrated with FastAPI dependencies
            # For now, it's a placeholder for the permission check logic
            return func(*args, **kwargs)
        return wrapper
    return decorator


class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use Redis-based rate limiting
    """

    def __init__(self):
        self._requests: Dict[str, List[datetime]] = {}
        self._lock = None
        try:
            import threading
            self._lock = threading.Lock()
        except ImportError:
            pass

    def is_allowed(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        """
        Check if request is allowed under rate limit

        Args:
            key: Identifier for rate limiting (e.g., API key hash)
            limit: Maximum requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if request is allowed
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)

        if self._lock:
            with self._lock:
                return self._check_and_update(key, limit, window_start, now)
        else:
            return self._check_and_update(key, limit, window_start, now)

    def _check_and_update(self, key: str, limit: int,
                         window_start: datetime, now: datetime) -> bool:
        """Internal method to check and update rate limit"""
        if key not in self._requests:
            self._requests[key] = []

        # Remove old requests outside window
        self._requests[key] = [
            ts for ts in self._requests[key] if ts > window_start
        ]

        if len(self._requests[key]) >= limit:
            return False

        self._requests[key].append(now)
        return True

    def get_remaining(self, key: str, limit: int, window_seconds: int = 60) -> int:
        """Get remaining requests in current window"""
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)

        if key not in self._requests:
            return limit

        current_requests = len([
            ts for ts in self._requests[key] if ts > window_start
        ])

        return max(0, limit - current_requests)


# Global instances
_secure_config: Optional[SecureConfig] = None
_rate_limiter: Optional[RateLimiter] = None


def get_secure_config() -> SecureConfig:
    """Get global secure configuration instance"""
    global _secure_config
    if _secure_config is None:
        _secure_config = SecureConfig()
    return _secure_config


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter

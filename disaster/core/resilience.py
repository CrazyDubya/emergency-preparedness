#!/usr/bin/env python3
"""
API Resilience and Network Utilities
Provides retry logic, circuit breaker, offline mode, and caching for external API calls
"""

import time
import json
import hashlib
import logging
import functools
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, TypeVar, Union
from dataclasses import dataclass, field
from enum import Enum

try:
    import requests
    from requests.exceptions import RequestException, Timeout, ConnectionError
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    RequestException = Exception
    Timeout = Exception
    ConnectionError = Exception

from exceptions import (
    NetworkError, APIConnectionError, APITimeoutError,
    APIResponseError, OfflineModeError
)

logger = logging.getLogger(__name__)

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5      # Failures before opening circuit
    recovery_timeout: int = 60      # Seconds before trying again
    half_open_requests: int = 3     # Requests to test in half-open state


@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_retries: int = 3
    initial_delay: float = 1.0      # Initial delay in seconds
    max_delay: float = 30.0         # Maximum delay between retries
    exponential_base: float = 2.0   # Base for exponential backoff
    jitter: bool = True             # Add randomness to delays


class CircuitBreaker:
    """
    Circuit breaker pattern implementation to prevent cascading failures
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self._lock = threading.Lock()

    def can_execute(self) -> bool:
        """Check if request can be executed"""
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:
                # Check if recovery timeout has passed
                if self.last_failure_time:
                    elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                    if elapsed >= self.config.recovery_timeout:
                        self.state = CircuitState.HALF_OPEN
                        self.success_count = 0
                        logger.info(f"Circuit breaker '{self.name}' entering half-open state")
                        return True
                return False

            # Half-open state - allow limited requests
            return True

    def record_success(self):
        """Record successful request"""
        with self._lock:
            self.failure_count = 0
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.half_open_requests:
                    self.state = CircuitState.CLOSED
                    logger.info(f"Circuit breaker '{self.name}' closed - service recovered")

    def record_failure(self):
        """Record failed request"""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit breaker '{self.name}' reopened after half-open failure")
            elif self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit breaker '{self.name}' opened after {self.failure_count} failures")

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }


class ResponseCache:
    """
    Simple file-based cache for API responses
    """

    def __init__(self, cache_dir: str = ".api_cache", default_ttl: int = 300):
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

    def _get_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from URL and parameters"""
        key_data = url + json.dumps(params or {}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Get cached response if valid"""
        cache_key = self._get_cache_key(url, params)

        # Check memory cache first
        if cache_key in self._memory_cache:
            entry = self._memory_cache[cache_key]
            if datetime.fromisoformat(entry["expires"]) > datetime.now():
                logger.debug(f"Cache hit (memory): {url}")
                return entry["data"]

        # Check file cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    entry = json.load(f)
                if datetime.fromisoformat(entry["expires"]) > datetime.now():
                    # Store in memory cache for faster access
                    self._memory_cache[cache_key] = entry
                    logger.debug(f"Cache hit (file): {url}")
                    return entry["data"]
                else:
                    # Expired - remove file
                    cache_file.unlink(missing_ok=True)
            except (json.JSONDecodeError, KeyError):
                cache_file.unlink(missing_ok=True)

        return None

    def set(self, url: str, data: Any, params: Optional[Dict] = None,
            ttl: Optional[int] = None):
        """Cache response data"""
        cache_key = self._get_cache_key(url, params)
        ttl = ttl or self.default_ttl

        entry = {
            "url": url,
            "data": data,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(seconds=ttl)).isoformat()
        }

        # Store in memory
        self._memory_cache[cache_key] = entry

        # Store in file
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(entry, f)
        except Exception as e:
            logger.warning(f"Failed to write cache file: {e}")

    def clear(self):
        """Clear all cached data"""
        self._memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink(missing_ok=True)
        logger.info("Cache cleared")


class OfflineModeManager:
    """
    Manages offline mode detection and fallback data
    """

    def __init__(self, fallback_data_dir: str = ".offline_data"):
        self.fallback_data_dir = Path(fallback_data_dir)
        self.fallback_data_dir.mkdir(parents=True, exist_ok=True)
        self._offline_mode = False
        self._last_connectivity_check: Optional[datetime] = None
        self._connectivity_check_interval = 60  # seconds

    @property
    def is_offline(self) -> bool:
        """Check if system is in offline mode"""
        # Check periodically if we can go back online
        if self._offline_mode and self._last_connectivity_check:
            elapsed = (datetime.now() - self._last_connectivity_check).total_seconds()
            if elapsed >= self._connectivity_check_interval:
                self.check_connectivity()
        return self._offline_mode

    def check_connectivity(self, test_url: str = "https://api.weather.gov") -> bool:
        """Check internet connectivity"""
        if not REQUESTS_AVAILABLE:
            self._offline_mode = True
            return False

        try:
            response = requests.head(test_url, timeout=5)
            self._offline_mode = False
            logger.info("Connectivity restored")
            return True
        except Exception:
            self._offline_mode = True
            self._last_connectivity_check = datetime.now()
            logger.warning("No internet connectivity - entering offline mode")
            return False

    def set_offline(self, offline: bool = True):
        """Manually set offline mode"""
        self._offline_mode = offline
        logger.info(f"Offline mode: {'enabled' if offline else 'disabled'}")

    def save_fallback_data(self, key: str, data: Any):
        """Save data for offline fallback"""
        fallback_file = self.fallback_data_dir / f"{key}.json"
        try:
            with open(fallback_file, 'w') as f:
                json.dump({
                    "data": data,
                    "saved_at": datetime.now().isoformat()
                }, f)
            logger.debug(f"Saved fallback data: {key}")
        except Exception as e:
            logger.warning(f"Failed to save fallback data: {e}")

    def get_fallback_data(self, key: str) -> Optional[Any]:
        """Get fallback data for offline mode"""
        fallback_file = self.fallback_data_dir / f"{key}.json"
        if fallback_file.exists():
            try:
                with open(fallback_file, 'r') as f:
                    entry = json.load(f)
                logger.info(f"Using fallback data for {key} (saved: {entry.get('saved_at', 'unknown')})")
                return entry.get("data")
            except Exception as e:
                logger.warning(f"Failed to load fallback data: {e}")
        return None


class ResilientAPIClient:
    """
    API client with built-in resilience features:
    - Automatic retries with exponential backoff
    - Circuit breaker pattern
    - Response caching
    - Offline mode support
    """

    # Class-level circuit breakers and cache (shared across instances)
    _circuit_breakers: Dict[str, CircuitBreaker] = {}
    _cache: Optional[ResponseCache] = None
    _offline_manager: Optional[OfflineModeManager] = None

    def __init__(self,
                 base_url: str,
                 api_name: str,
                 retry_config: Optional[RetryConfig] = None,
                 circuit_config: Optional[CircuitBreakerConfig] = None,
                 enable_cache: bool = True,
                 cache_ttl: int = 300,
                 timeout: float = 10.0):

        self.base_url = base_url.rstrip('/')
        self.api_name = api_name
        self.retry_config = retry_config or RetryConfig()
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self.enable_cache = enable_cache

        # Initialize or get shared circuit breaker for this API
        if api_name not in self._circuit_breakers:
            self._circuit_breakers[api_name] = CircuitBreaker(
                api_name, circuit_config or CircuitBreakerConfig()
            )
        self.circuit_breaker = self._circuit_breakers[api_name]

        # Initialize shared cache and offline manager
        if self._cache is None:
            ResilientAPIClient._cache = ResponseCache()
        if self._offline_manager is None:
            ResilientAPIClient._offline_manager = OfflineModeManager()

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt with exponential backoff"""
        import random

        delay = self.retry_config.initial_delay * (
            self.retry_config.exponential_base ** attempt
        )
        delay = min(delay, self.retry_config.max_delay)

        if self.retry_config.jitter:
            delay *= (0.5 + random.random())  # 50-150% of calculated delay

        return delay

    def request(self,
                method: str,
                endpoint: str,
                params: Optional[Dict] = None,
                data: Optional[Dict] = None,
                headers: Optional[Dict] = None,
                use_cache: Optional[bool] = None,
                fallback_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Make a resilient API request

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (appended to base_url)
            params: Query parameters
            data: Request body (for POST/PUT)
            headers: Additional headers
            use_cache: Override instance cache setting
            fallback_key: Key for offline fallback data

        Returns:
            API response as dictionary

        Raises:
            OfflineModeError: If in offline mode with no fallback
            APIConnectionError: If connection fails after retries
            APIResponseError: If API returns error status
        """
        if not REQUESTS_AVAILABLE:
            raise NetworkError("requests library not available")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        use_cache = use_cache if use_cache is not None else self.enable_cache

        # Check cache first (only for GET requests)
        if method.upper() == "GET" and use_cache and self._cache:
            cached = self._cache.get(url, params)
            if cached is not None:
                return cached

        # Check offline mode
        if self._offline_manager and self._offline_manager.is_offline:
            if fallback_key:
                fallback = self._offline_manager.get_fallback_data(fallback_key)
                if fallback is not None:
                    return fallback
            raise OfflineModeError(f"{self.api_name} API request")

        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            logger.warning(f"Circuit breaker open for {self.api_name}")
            if fallback_key and self._offline_manager:
                fallback = self._offline_manager.get_fallback_data(fallback_key)
                if fallback is not None:
                    return fallback
            raise APIConnectionError(
                self.api_name, url,
                Exception("Circuit breaker open - too many failures")
            )

        # Make request with retries
        last_exception: Optional[Exception] = None

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )

                # Check for HTTP errors
                if response.status_code >= 400:
                    if response.status_code < 500:
                        # Client error - don't retry
                        raise APIResponseError(
                            self.api_name, response.status_code, response.text
                        )
                    else:
                        # Server error - may retry
                        raise APIResponseError(
                            self.api_name, response.status_code, response.text
                        )

                # Success!
                self.circuit_breaker.record_success()
                result = response.json()

                # Cache successful GET responses
                if method.upper() == "GET" and use_cache and self._cache:
                    self._cache.set(url, result, params, self.cache_ttl)

                # Save as fallback data if key provided
                if fallback_key and self._offline_manager:
                    self._offline_manager.save_fallback_data(fallback_key, result)

                return result

            except Timeout as e:
                last_exception = APITimeoutError(self.api_name, url, self.timeout)
                logger.warning(f"Timeout on attempt {attempt + 1}: {url}")

            except ConnectionError as e:
                last_exception = APIConnectionError(self.api_name, url, e)
                logger.warning(f"Connection error on attempt {attempt + 1}: {url}")

            except APIResponseError as e:
                if e.details.get("status_code", 0) >= 500:
                    last_exception = e
                    logger.warning(f"Server error on attempt {attempt + 1}: {url}")
                else:
                    # Client error - don't retry
                    self.circuit_breaker.record_failure()
                    raise

            except RequestException as e:
                last_exception = APIConnectionError(self.api_name, url, e)
                logger.warning(f"Request error on attempt {attempt + 1}: {url}")

            # Wait before retry (except on last attempt)
            if attempt < self.retry_config.max_retries:
                delay = self._calculate_delay(attempt)
                logger.info(f"Retrying in {delay:.1f}s...")
                time.sleep(delay)

        # All retries exhausted
        self.circuit_breaker.record_failure()

        # Try fallback data
        if fallback_key and self._offline_manager:
            fallback = self._offline_manager.get_fallback_data(fallback_key)
            if fallback is not None:
                logger.info(f"Using fallback data after API failure: {fallback_key}")
                return fallback

        # Check if we should enter offline mode
        if self._offline_manager:
            self._offline_manager.check_connectivity()

        raise last_exception or APIConnectionError(self.api_name, url)

    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for GET requests"""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for POST requests"""
        return self.request("POST", endpoint, **kwargs)


def with_retry(retry_config: Optional[RetryConfig] = None):
    """
    Decorator for adding retry logic to any function

    Usage:
        @with_retry(RetryConfig(max_retries=3))
        def my_api_call():
            ...
    """
    config = retry_config or RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            import random
            last_exception: Optional[Exception] = None

            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.initial_delay * (config.exponential_base ** attempt)
                        delay = min(delay, config.max_delay)
                        if config.jitter:
                            delay *= (0.5 + random.random())
                        logger.warning(f"Retry {attempt + 1}/{config.max_retries} for {func.__name__}: {e}")
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator


# Global instances for easy access
_global_cache: Optional[ResponseCache] = None
_global_offline_manager: Optional[OfflineModeManager] = None


def get_cache() -> ResponseCache:
    """Get global cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = ResponseCache()
    return _global_cache


def get_offline_manager() -> OfflineModeManager:
    """Get global offline mode manager"""
    global _global_offline_manager
    if _global_offline_manager is None:
        _global_offline_manager = OfflineModeManager()
    return _global_offline_manager


def is_offline() -> bool:
    """Check if system is in offline mode"""
    return get_offline_manager().is_offline


def set_offline_mode(offline: bool = True):
    """Set offline mode manually"""
    get_offline_manager().set_offline(offline)

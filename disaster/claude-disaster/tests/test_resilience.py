#!/usr/bin/env python3
"""
Unit tests for the resilience module
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import time
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from resilience import (
    CircuitState, CircuitBreakerConfig, RetryConfig,
    CircuitBreaker, ResponseCache, OfflineModeManager,
    ResilientAPIClient, with_retry
)


class TestCircuitBreaker(unittest.TestCase):
    """Test CircuitBreaker class"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=1,  # 1 second for fast tests
            half_open_requests=2
        )
        self.breaker = CircuitBreaker("test", self.config)

    def test_initial_state_is_closed(self):
        """Test that initial state is closed"""
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_can_execute_when_closed(self):
        """Test that requests are allowed when closed"""
        self.assertTrue(self.breaker.can_execute())

    def test_opens_after_threshold_failures(self):
        """Test that circuit opens after reaching failure threshold"""
        for _ in range(3):
            self.breaker.record_failure()

        self.assertEqual(self.breaker.state, CircuitState.OPEN)
        self.assertFalse(self.breaker.can_execute())

    def test_success_resets_failure_count(self):
        """Test that success resets failure count"""
        self.breaker.record_failure()
        self.breaker.record_failure()
        self.breaker.record_success()

        self.assertEqual(self.breaker.failure_count, 0)
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_transitions_to_half_open_after_recovery_timeout(self):
        """Test transition to half-open after recovery timeout"""
        # Open the circuit
        for _ in range(3):
            self.breaker.record_failure()

        self.assertEqual(self.breaker.state, CircuitState.OPEN)

        # Wait for recovery timeout
        time.sleep(1.1)

        # Should transition to half-open
        self.assertTrue(self.breaker.can_execute())
        self.assertEqual(self.breaker.state, CircuitState.HALF_OPEN)

    def test_closes_after_successful_half_open_requests(self):
        """Test that circuit closes after successful half-open requests"""
        # Open and transition to half-open
        for _ in range(3):
            self.breaker.record_failure()
        time.sleep(1.1)
        self.breaker.can_execute()

        # Successful requests in half-open
        self.breaker.record_success()
        self.breaker.record_success()

        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_reopens_on_half_open_failure(self):
        """Test that circuit reopens on failure in half-open state"""
        # Open and transition to half-open
        for _ in range(3):
            self.breaker.record_failure()
        time.sleep(1.1)
        self.breaker.can_execute()

        # Failure in half-open
        self.breaker.record_failure()

        self.assertEqual(self.breaker.state, CircuitState.OPEN)

    def test_get_status(self):
        """Test status reporting"""
        status = self.breaker.get_status()

        self.assertEqual(status["name"], "test")
        self.assertEqual(status["state"], "closed")
        self.assertEqual(status["failure_count"], 0)


class TestResponseCache(unittest.TestCase):
    """Test ResponseCache class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = ResponseCache(cache_dir=self.temp_dir, default_ttl=2)

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_miss_returns_none(self):
        """Test that cache miss returns None"""
        result = self.cache.get("http://example.com/api")
        self.assertIsNone(result)

    def test_cache_set_and_get(self):
        """Test setting and getting cached data"""
        data = {"key": "value", "number": 42}
        self.cache.set("http://example.com/api", data)

        result = self.cache.get("http://example.com/api")
        self.assertEqual(result, data)

    def test_cache_with_params(self):
        """Test caching with different parameters"""
        self.cache.set("http://example.com/api", {"a": 1}, params={"page": 1})
        self.cache.set("http://example.com/api", {"b": 2}, params={"page": 2})

        result1 = self.cache.get("http://example.com/api", params={"page": 1})
        result2 = self.cache.get("http://example.com/api", params={"page": 2})

        self.assertEqual(result1, {"a": 1})
        self.assertEqual(result2, {"b": 2})

    def test_cache_expiration(self):
        """Test that cached data expires"""
        self.cache.set("http://example.com/api", {"data": "test"}, ttl=1)

        # Should be cached
        self.assertIsNotNone(self.cache.get("http://example.com/api"))

        # Wait for expiration
        time.sleep(1.1)

        # Should be expired
        self.assertIsNone(self.cache.get("http://example.com/api"))

    def test_cache_clear(self):
        """Test clearing cache"""
        self.cache.set("http://example.com/api1", {"a": 1})
        self.cache.set("http://example.com/api2", {"b": 2})

        self.cache.clear()

        self.assertIsNone(self.cache.get("http://example.com/api1"))
        self.assertIsNone(self.cache.get("http://example.com/api2"))


class TestOfflineModeManager(unittest.TestCase):
    """Test OfflineModeManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = OfflineModeManager(fallback_data_dir=self.temp_dir)

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initial_state_is_online(self):
        """Test that initial state is online"""
        self.assertFalse(self.manager._offline_mode)

    def test_set_offline_mode(self):
        """Test setting offline mode"""
        self.manager.set_offline(True)
        self.assertTrue(self.manager.is_offline)

        self.manager.set_offline(False)
        self.assertFalse(self.manager.is_offline)

    def test_save_and_get_fallback_data(self):
        """Test saving and retrieving fallback data"""
        data = {"weather": "sunny", "temp": 72}
        self.manager.save_fallback_data("weather_data", data)

        result = self.manager.get_fallback_data("weather_data")
        self.assertEqual(result, data)

    def test_get_nonexistent_fallback_returns_none(self):
        """Test that missing fallback data returns None"""
        result = self.manager.get_fallback_data("nonexistent")
        self.assertIsNone(result)

    @patch('resilience.REQUESTS_AVAILABLE', True)
    @patch('resilience.requests')
    def test_check_connectivity_success(self, mock_requests):
        """Test connectivity check success"""
        mock_requests.head.return_value = Mock(status_code=200)

        result = self.manager.check_connectivity()
        self.assertTrue(result)
        self.assertFalse(self.manager.is_offline)

    @patch('resilience.REQUESTS_AVAILABLE', True)
    @patch('resilience.requests')
    def test_check_connectivity_failure(self, mock_requests):
        """Test connectivity check failure"""
        mock_requests.head.side_effect = Exception("Network error")

        result = self.manager.check_connectivity()
        self.assertFalse(result)
        self.assertTrue(self.manager.is_offline)


class TestRetryConfig(unittest.TestCase):
    """Test RetryConfig dataclass"""

    def test_default_values(self):
        """Test default configuration values"""
        config = RetryConfig()

        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.initial_delay, 1.0)
        self.assertEqual(config.max_delay, 30.0)
        self.assertEqual(config.exponential_base, 2.0)
        self.assertTrue(config.jitter)

    def test_custom_values(self):
        """Test custom configuration values"""
        config = RetryConfig(
            max_retries=5,
            initial_delay=0.5,
            max_delay=60.0,
            exponential_base=3.0,
            jitter=False
        )

        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.initial_delay, 0.5)
        self.assertEqual(config.max_delay, 60.0)


class TestWithRetryDecorator(unittest.TestCase):
    """Test with_retry decorator"""

    def test_successful_function_returns_immediately(self):
        """Test that successful function returns without retry"""
        call_count = 0

        @with_retry(RetryConfig(max_retries=3, initial_delay=0.01))
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_func()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)

    def test_retries_on_failure(self):
        """Test that function retries on failure"""
        call_count = 0

        @with_retry(RetryConfig(max_retries=3, initial_delay=0.01))
        def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"

        result = failing_then_success()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_raises_after_max_retries(self):
        """Test that exception is raised after max retries"""
        call_count = 0

        @with_retry(RetryConfig(max_retries=2, initial_delay=0.01))
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise Exception("Always fails")

        with self.assertRaises(Exception) as ctx:
            always_fails()

        self.assertEqual(str(ctx.exception), "Always fails")
        self.assertEqual(call_count, 3)  # Initial + 2 retries


class TestResilientAPIClient(unittest.TestCase):
    """Test ResilientAPIClient class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        # Reset class-level state
        ResilientAPIClient._circuit_breakers.clear()
        ResilientAPIClient._cache = None
        ResilientAPIClient._offline_manager = None

    def test_client_creation(self):
        """Test client creation"""
        client = ResilientAPIClient(
            base_url="https://api.example.com",
            api_name="Test API"
        )

        self.assertEqual(client.base_url, "https://api.example.com")
        self.assertEqual(client.api_name, "Test API")

    def test_circuit_breaker_shared_per_api(self):
        """Test that circuit breaker is shared per API name"""
        client1 = ResilientAPIClient(
            base_url="https://api1.example.com",
            api_name="SharedAPI"
        )
        client2 = ResilientAPIClient(
            base_url="https://api2.example.com",
            api_name="SharedAPI"
        )

        self.assertIs(client1.circuit_breaker, client2.circuit_breaker)

    @patch('resilience.REQUESTS_AVAILABLE', True)
    @patch('resilience.requests')
    def test_successful_request(self, mock_requests):
        """Test successful API request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_requests.request.return_value = mock_response

        client = ResilientAPIClient(
            base_url="https://api.example.com",
            api_name="Test API",
            enable_cache=False
        )

        result = client.get("/endpoint")
        self.assertEqual(result, {"data": "test"})

    @patch('resilience.REQUESTS_AVAILABLE', False)
    def test_raises_when_requests_unavailable(self):
        """Test that error is raised when requests library unavailable"""
        from exceptions import NetworkError

        client = ResilientAPIClient(
            base_url="https://api.example.com",
            api_name="Test API"
        )

        with self.assertRaises(NetworkError):
            client.get("/endpoint")


if __name__ == "__main__":
    unittest.main()

"""
Production Hardening Utilities for Helix Collective v17.

Circuit breakers, retry logic, and graceful degradation for external services.
Ensures system stability when Discord, Notion, Zapier, or other services are down.

Author: Claude Opus (Production Hardening Sprint - Dec 2025)
"""
import asyncio
import functools
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)

# Type variable for generic return types
T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation, requests flow through
    OPEN = "open"          # Failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5        # Failures before opening circuit
    success_threshold: int = 2        # Successes to close from half-open
    timeout: float = 30.0             # Seconds before trying half-open
    excluded_exceptions: tuple = ()   # Exceptions that don't count as failures


@dataclass
class CircuitBreakerState:
    """Tracks circuit breaker state."""
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None


class CircuitBreaker:
    """
    Circuit breaker pattern for external service calls.

    Prevents cascade failures by stopping calls to failing services.

    Usage:
        breaker = CircuitBreaker("discord")

        @breaker
        async def call_discord():
            # ... make Discord API call
    """

    _instances: Dict[str, 'CircuitBreaker'] = {}

    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitBreakerState()
        self._lock = asyncio.Lock()

        # Register instance for monitoring
        CircuitBreaker._instances[name] = self

    @classmethod
    def get_all_states(cls) -> Dict[str, Dict[str, Any]]:
        """Get status of all circuit breakers for health checks."""
        return {
            name: {
                "state": breaker._state.state.value,
                "failure_count": breaker._state.failure_count,
                "last_failure": (
                    breaker._state.last_failure_time.isoformat()
                    if breaker._state.last_failure_time else None
                ),
            }
            for name, breaker in cls._instances.items()
        }

    async def _should_allow_request(self) -> bool:
        """Check if request should be allowed through."""
        async with self._lock:
            if self._state.state == CircuitState.CLOSED:
                return True

            if self._state.state == CircuitState.OPEN:
                # Check if timeout has passed
                if self._state.last_failure_time:
                    elapsed = datetime.utcnow() - self._state.last_failure_time
                    if elapsed.total_seconds() >= self.config.timeout:
                        self._state.state = CircuitState.HALF_OPEN
                        self._state.success_count = 0
                        logger.info(f"Circuit {self.name}: OPEN → HALF_OPEN")
                        return True
                return False

            # HALF_OPEN: allow limited requests
            return True

    async def _record_success(self):
        """Record successful call."""
        async with self._lock:
            self._state.last_success_time = datetime.utcnow()

            if self._state.state == CircuitState.HALF_OPEN:
                self._state.success_count += 1
                if self._state.success_count >= self.config.success_threshold:
                    self._state.state = CircuitState.CLOSED
                    self._state.failure_count = 0
                    logger.info(f"Circuit {self.name}: HALF_OPEN → CLOSED")

            elif self._state.state == CircuitState.CLOSED:
                # Reset failure count on success
                self._state.failure_count = 0

    async def _record_failure(self, exc: Exception):
        """Record failed call."""
        # Don't count excluded exceptions
        if isinstance(exc, self.config.excluded_exceptions):
            return

        async with self._lock:
            self._state.failure_count += 1
            self._state.last_failure_time = datetime.utcnow()

            if self._state.state == CircuitState.HALF_OPEN:
                # Any failure in half-open goes back to open
                self._state.state = CircuitState.OPEN
                logger.warning(f"Circuit {self.name}: HALF_OPEN → OPEN")

            elif self._state.state == CircuitState.CLOSED:
                if self._state.failure_count >= self.config.failure_threshold:
                    self._state.state = CircuitState.OPEN
                    logger.warning(
                        f"Circuit {self.name}: CLOSED → OPEN "
                        f"(failures: {self._state.failure_count})"
                    )

    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap async functions with circuit breaker."""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not await self._should_allow_request():
                logger.warning(f"Circuit {self.name} is OPEN - request blocked")
                raise CircuitOpenError(f"Circuit breaker {self.name} is open")

            try:
                result = await func(*args, **kwargs)
                await self._record_success()
                return result
            except Exception as e:
                await self._record_failure(e)
                raise

        return wrapper


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable] = None,
):
    """
    Retry decorator with exponential backoff.

    Usage:
        @retry_with_backoff(max_retries=3, base_delay=1.0)
        async def call_external_api():
            # ... make API call

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff (2.0 = double each time)
        exceptions: Tuple of exceptions to retry on
        on_retry: Optional callback(attempt, exception, delay) on each retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            f"{func.__name__} failed after {max_retries + 1} "
                            f"attempts: {e}"
                        )
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )

                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    if on_retry:
                        on_retry(attempt + 1, e, delay)

                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper
    return decorator


@dataclass
class ServiceHealth:
    """Health status of an external service."""
    name: str
    healthy: bool
    last_check: datetime
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    circuit_state: Optional[str] = None


class DependencyHealthChecker:
    """
    Checks health of external dependencies.

    Usage:
        checker = DependencyHealthChecker()
        checker.register("discord", discord_health_check)
        checker.register("notion", notion_health_check)

        status = await checker.check_all()
    """

    def __init__(self):
        self._checks: Dict[str, Callable] = {}
        self._last_results: Dict[str, ServiceHealth] = {}

    def register(self, name: str, check_func: Callable):
        """Register a health check function."""
        self._checks[name] = check_func

    async def check(self, name: str) -> ServiceHealth:
        """Run a single health check."""
        if name not in self._checks:
            return ServiceHealth(
                name=name,
                healthy=False,
                last_check=datetime.utcnow(),
                error="Health check not registered"
            )

        start_time = time.time()
        try:
            await asyncio.wait_for(self._checks[name](), timeout=10.0)
            response_time = (time.time() - start_time) * 1000

            # Get circuit breaker state if exists
            circuit_state = None
            if name in CircuitBreaker._instances:
                circuit_state = CircuitBreaker._instances[name]._state.state.value

            result = ServiceHealth(
                name=name,
                healthy=True,
                last_check=datetime.utcnow(),
                response_time_ms=round(response_time, 2),
                circuit_state=circuit_state,
            )
        except asyncio.TimeoutError:
            result = ServiceHealth(
                name=name,
                healthy=False,
                last_check=datetime.utcnow(),
                error="Health check timed out (>10s)"
            )
        except Exception as e:
            result = ServiceHealth(
                name=name,
                healthy=False,
                last_check=datetime.utcnow(),
                error=str(e)
            )

        self._last_results[name] = result
        return result

    async def check_all(self) -> Dict[str, ServiceHealth]:
        """Run all health checks concurrently."""
        tasks = [self.check(name) for name in self._checks]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            name: (
                result if isinstance(result, ServiceHealth)
                else ServiceHealth(
                    name=name,
                    healthy=False,
                    last_check=datetime.utcnow(),
                    error=str(result)
                )
            )
            for name, result in zip(self._checks.keys(), results)
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all health checks."""
        healthy_count = sum(
            1 for r in self._last_results.values() if r.healthy
        )
        total = len(self._last_results)

        return {
            "overall_healthy": healthy_count == total if total > 0 else True,
            "healthy_count": healthy_count,
            "total_services": total,
            "services": {
                name: {
                    "healthy": result.healthy,
                    "response_time_ms": result.response_time_ms,
                    "error": result.error,
                    "circuit_state": result.circuit_state,
                }
                for name, result in self._last_results.items()
            },
            "circuit_breakers": CircuitBreaker.get_all_states(),
        }


# Pre-configured circuit breakers for common services
discord_breaker = CircuitBreaker(
    "discord",
    CircuitBreakerConfig(failure_threshold=3, timeout=60.0)
)

notion_breaker = CircuitBreaker(
    "notion",
    CircuitBreakerConfig(failure_threshold=5, timeout=30.0)
)

zapier_breaker = CircuitBreaker(
    "zapier",
    CircuitBreakerConfig(failure_threshold=3, timeout=45.0)
)

openai_breaker = CircuitBreaker(
    "openai",
    CircuitBreakerConfig(failure_threshold=5, timeout=30.0)
)

anthropic_breaker = CircuitBreaker(
    "anthropic",
    CircuitBreakerConfig(failure_threshold=5, timeout=30.0)
)


# Global health checker instance
health_checker = DependencyHealthChecker()


def graceful_degradation(
    fallback_value: Any = None,
    fallback_func: Optional[Callable] = None,
    log_level: str = "warning",
):
    """
    Decorator for graceful degradation when service calls fail.

    Usage:
        @graceful_degradation(fallback_value={"status": "degraded"})
        async def get_external_data():
            # ... call external service

    Args:
        fallback_value: Static value to return on failure
        fallback_func: Function to call for dynamic fallback (receives exception)
        log_level: Log level for degradation messages
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log_func = getattr(logger, log_level, logger.warning)
                log_func(
                    f"{func.__name__} degraded due to error: {e}. "
                    f"Using fallback."
                )

                if fallback_func:
                    return fallback_func(e)
                return fallback_value

        return wrapper
    return decorator

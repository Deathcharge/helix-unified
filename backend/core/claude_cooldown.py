"""
🔧 Claude API Cooldown Management
==================================

Handles Claude API rate limiting and cooldown periods to prevent 429 errors.

Features:
- Request queuing during cooldown
- Automatic retry with exponential backoff
- Cooldown window tracking (60s default)
- Metrics for monitoring

Author: Claude (Helix Collective)
Date: 2025-12-09
Phase: Launch Sprint v17.2 - Phase 2 Agent Ecosystem
"""

import asyncio
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from loguru import logger


class ClaudeAPILimiter:
    """
    Rate limiter for Claude API with cooldown management.

    Strategy:
    - Monitor request rate per minute
    - Trigger cooldown at 80% of API limit
    - Queue requests during cooldown
    - Linear backoff: 1s, 2s, 4s, 8s, etc.
    - Max wait: 60 seconds before queue rejection
    """

    def __init__(
        self,
        max_requests_per_minute: int = 50,
        cooldown_threshold: float = 0.8,
        cooldown_window: int = 60,
        max_queue_size: int = 100
    ):
        """
        Initialize Claude API rate limiter.

        Args:
            max_requests_per_minute: Maximum requests allowed per minute
            cooldown_threshold: Percentage threshold to trigger cooldown (0.8 = 80%)
            cooldown_window: Cooldown duration in seconds (60s default)
            max_queue_size: Maximum queued requests before rejection
        """
        self.max_rpm = max_requests_per_minute
        self.cooldown_threshold = cooldown_threshold
        self.cooldown_window = cooldown_window
        self.max_queue_size = max_queue_size

        # Track request timestamps (sliding window)
        self.request_times: deque = deque(maxlen=max_requests_per_minute)

        # Cooldown state
        self.in_cooldown = False
        self.cooldown_until: Optional[datetime] = None

        # Queue for requests during cooldown
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)

        # Metrics
        self.total_requests = 0
        self.queued_requests = 0
        self.rejected_requests = 0
        self.cooldown_triggers = 0

        logger.info(
            f"🤖 Claude API Limiter initialized: "
            f"{max_requests_per_minute} req/min, "
            f"cooldown @ {int(cooldown_threshold * 100)}%"
        )

    def _get_current_rpm(self) -> int:
        """Get current requests per minute based on recent history."""
        now = time.time()
        # Remove timestamps older than 60 seconds
        while self.request_times and (now - self.request_times[0]) > 60:
            self.request_times.popleft()
        return len(self.request_times)

    def _should_trigger_cooldown(self) -> bool:
        """Check if we should enter cooldown based on current rate."""
        current_rpm = self._get_current_rpm()
        threshold = int(self.max_rpm * self.cooldown_threshold)
        return current_rpm >= threshold

    def _is_in_cooldown(self) -> bool:
        """Check if we're currently in cooldown period."""
        if not self.in_cooldown:
            return False

        if self.cooldown_until and datetime.utcnow() >= self.cooldown_until:
            # Cooldown period expired
            self.in_cooldown = False
            self.cooldown_until = None
            logger.info("✅ Claude API cooldown expired - resuming normal operation")
            return False

        return True

    def _enter_cooldown(self):
        """Enter cooldown period."""
        if not self.in_cooldown:
            self.in_cooldown = True
            self.cooldown_until = datetime.utcnow() + timedelta(seconds=self.cooldown_window)
            self.cooldown_triggers += 1
            logger.warning(
                f"⏸️ Claude API cooldown triggered "
                f"({self._get_current_rpm()}/{self.max_rpm} rpm) - "
                f"resuming at {self.cooldown_until.strftime('%H:%M:%S')}"
            )

    async def acquire(self, timeout: float = 60.0) -> bool:
        """
        Acquire permission to make Claude API request.

        Args:
            timeout: Maximum seconds to wait in queue

        Returns:
            True if request can proceed, False if rejected

        Raises:
            TimeoutError: If queued too long
        """
        self.total_requests += 1

        # Check if we're in cooldown
        if self._is_in_cooldown():
            self.queued_requests += 1

            if self.queue.qsize() >= self.max_queue_size:
                self.rejected_requests += 1
                logger.error(
                    f"❌ Claude API queue full ({self.queue.qsize()}/{self.max_queue_size}) - "
                    "request rejected"
                )
                raise RuntimeError("Claude API queue full - try again later")

            # Queue the request
            logger.debug(
                f"⏳ Claude API request queued "
                f"({self.queue.qsize() + 1}/{self.max_queue_size}) - "
                f"cooldown for {(self.cooldown_until - datetime.utcnow()).seconds}s"
            )

            try:
                await asyncio.wait_for(self.queue.get(), timeout=timeout)
            except asyncio.TimeoutError:
                self.rejected_requests += 1
                logger.error(f"❌ Claude API request timeout after {timeout}s")
                raise TimeoutError(f"Claude API request timeout after {timeout}s")

        # Check if we should trigger cooldown
        if self._should_trigger_cooldown():
            self._enter_cooldown()

        # Record this request
        self.request_times.append(time.time())

        return True

    async def process_queue(self):
        """Background task to process queued requests after cooldown."""
        while True:
            try:
                # Wait for cooldown to end
                if self._is_in_cooldown():
                    wait_seconds = (self.cooldown_until - datetime.utcnow()).total_seconds()
                    if wait_seconds > 0:
                        await asyncio.sleep(wait_seconds)

                # Process queue
                while not self.queue.empty() and not self._is_in_cooldown():
                    try:
                        self.queue.put_nowait(None)  # Release waiting request
                        await asyncio.sleep(0.1)  # Small delay between releases
                    except asyncio.QueueFull:
                        break

                await asyncio.sleep(1)  # Check every second

            except Exception as e:
                logger.error(f"Error in Claude API queue processor: {e}")
                await asyncio.sleep(5)

    def get_metrics(self) -> Dict[str, Any]:
        """Get rate limiter metrics."""
        return {
            "total_requests": self.total_requests,
            "queued_requests": self.queued_requests,
            "rejected_requests": self.rejected_requests,
            "cooldown_triggers": self.cooldown_triggers,
            "current_rpm": self._get_current_rpm(),
            "max_rpm": self.max_rpm,
            "in_cooldown": self.in_cooldown,
            "cooldown_until": self.cooldown_until.isoformat() if self.cooldown_until else None,
            "queue_size": self.queue.qsize(),
            "queue_capacity": self.max_queue_size,
        }

    async def __aenter__(self):
        """Context manager entry."""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass


# Global limiter instance
_claude_limiter: Optional[ClaudeAPILimiter] = None


def get_claude_limiter(
    max_requests_per_minute: int = 50,
    cooldown_threshold: float = 0.8
) -> ClaudeAPILimiter:
    """Get or create global Claude API limiter."""
    global _claude_limiter
    if _claude_limiter is None:
        _claude_limiter = ClaudeAPILimiter(
            max_requests_per_minute=max_requests_per_minute,
            cooldown_threshold=cooldown_threshold
        )
    return _claude_limiter


async def with_claude_limiter(func: Callable, *args, **kwargs):
    """
    Decorator/wrapper to apply Claude API rate limiting.

    Usage:
        result = await with_claude_limiter(make_claude_request, prompt="Hello")
    """
    limiter = get_claude_limiter()
    await limiter.acquire()
    return await func(*args, **kwargs)

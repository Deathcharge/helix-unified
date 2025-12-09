"""
🔄 Webhook Retry Logic
=====================

Implements exponential backoff retry logic for webhook calls.

Features:
- Configurable retry attempts (default: 3)
- Exponential backoff (1s, 2s, 4s, 8s, etc.)
- Error logging and metrics
- Timeout handling

Author: Claude (Helix Collective)
Date: 2025-12-09
Phase: Launch Sprint v17.2 - Phase 2 Agent Ecosystem
"""

import asyncio
from typing import Any, Dict, Optional

import httpx
from loguru import logger


class WebhookRetryPolicy:
    """
    Retry policy for webhook calls with exponential backoff.

    Example:
        policy = WebhookRetryPolicy(max_attempts=3)
        result = await policy.execute(
            url="https://hooks.zapier.com/...",
            payload={"data": "test"}
        )
    """

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        timeout: float = 10.0,
    ):
        """
        Initialize webhook retry policy.

        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay in seconds (doubles each retry)
            max_delay: Maximum delay between retries
            timeout: HTTP timeout for each attempt
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.timeout = timeout

        # Metrics
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_retries = 0

    async def execute(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
    ) -> Dict[str, Any]:
        """
        Execute webhook call with retry logic.

        Args:
            url: Webhook URL
            payload: JSON payload to send
            headers: Optional HTTP headers
            method: HTTP method (default: POST)

        Returns:
            Response data with status and metrics

        Raises:
            httpx.HTTPError: If all retries fail
        """
        self.total_calls += 1

        if headers is None:
            headers = {"Content-Type": "application/json"}

        attempt = 0
        delay = self.initial_delay
        last_error = None

        while attempt < self.max_attempts:
            attempt += 1

            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    if method.upper() == "POST":
                        response = await client.post(url, json=payload, headers=headers)
                    elif method.upper() == "GET":
                        response = await client.get(url, params=payload, headers=headers)
                    elif method.upper() == "PUT":
                        response = await client.put(url, json=payload, headers=headers)
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")

                    response.raise_for_status()

                    # Success!
                    if attempt > 1:
                        self.total_retries += (attempt - 1)
                        logger.info(
                            f"✅ Webhook succeeded after {attempt} attempts: "
                            f"{url[:50]}..."
                        )
                    else:
                        logger.debug(f"✅ Webhook succeeded: {url[:50]}...")

                    self.successful_calls += 1

                    return {
                        "success": True,
                        "status_code": response.status_code,
                        "attempt": attempt,
                        "response": response.json() if response.text else {},
                    }

            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_error = e
                error_type = type(e).__name__

                if attempt < self.max_attempts:
                    logger.warning(
                        f"⚠️ Webhook attempt {attempt}/{self.max_attempts} failed "
                        f"({error_type}) - retrying in {delay}s: {url[:50]}..."
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self.max_delay)  # Exponential backoff
                else:
                    logger.error(
                        f"❌ Webhook failed after {attempt} attempts "
                        f"({error_type}): {url[:50]}... - {str(e)}"
                    )

        # All attempts failed
        self.failed_calls += 1
        self.total_retries += (attempt - 1)

        return {
            "success": False,
            "error": str(last_error),
            "attempts": attempt,
            "status_code": getattr(last_error, "response", {}).get("status_code") if hasattr(last_error, "response") else None,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get webhook retry metrics."""
        success_rate = (
            (self.successful_calls / self.total_calls * 100)
            if self.total_calls > 0
            else 0
        )
        avg_retries = (
            (self.total_retries / self.total_calls)
            if self.total_calls > 0
            else 0
        )

        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "total_retries": self.total_retries,
            "success_rate": round(success_rate, 2),
            "average_retries_per_call": round(avg_retries, 2),
        }


# Global webhook retry instance
_webhook_retry: Optional[WebhookRetryPolicy] = None


def get_webhook_retry(
    max_attempts: int = 3,
    timeout: float = 10.0
) -> WebhookRetryPolicy:
    """Get or create global webhook retry policy."""
    global _webhook_retry
    if _webhook_retry is None:
        _webhook_retry = WebhookRetryPolicy(
            max_attempts=max_attempts,
            timeout=timeout
        )
    return _webhook_retry


async def send_webhook_with_retry(
    url: str,
    payload: Dict[str, Any],
    max_attempts: int = 3,
    timeout: float = 10.0,
) -> Dict[str, Any]:
    """
    Convenience function to send webhook with retry logic.

    Usage:
        result = await send_webhook_with_retry(
            url="https://hooks.zapier.com/...",
            payload={"event": "test"}
        )

        if result["success"]:
            print("Webhook sent successfully!")
        else:
            print(f"Webhook failed: {result['error']}")
    """
    policy = get_webhook_retry(max_attempts=max_attempts, timeout=timeout)
    return await policy.execute(url, payload)

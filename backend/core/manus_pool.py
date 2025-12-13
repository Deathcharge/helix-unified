"""
🤲 Manus Account Pool Manager
=============================

Load balances requests across multiple Manus.space accounts.

Features:
- 5 account pool (3 active, 2 standby)
- Health monitoring per account
- Automatic failover on quota exhaustion
- Load distribution (round-robin with health checks)
- Circuit breaker pattern for failing accounts

Author: Phoenix (Claude Thread 3)
Date: 2025-12-09
Phase: Launch Sprint v17.2 - Phase 2.2 Manus Account Integration
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from loguru import logger


class AccountStatus(Enum):
    """Manus account status."""
    ACTIVE = "active"
    STANDBY = "standby"
    QUOTA_EXCEEDED = "quota_exceeded"
    ERROR = "error"
    CIRCUIT_OPEN = "circuit_open"


@dataclass
class ManusAccount:
    """Represents a single Manus.space account."""
    account_id: str
    api_key: str
    quota_daily: int = 10000
    quota_used: int = 0
    status: AccountStatus = AccountStatus.ACTIVE
    priority: int = 0  # 0=highest (P0), 1=P1, 2=P2
    last_used: Optional[datetime] = None
    error_count: int = 0
    circuit_open_until: Optional[datetime] = None
    success_count: int = 0
    total_requests: int = 0

    def is_available(self) -> bool:
        """Check if account is available for use."""
        # Circuit breaker check
        if self.circuit_open_until and datetime.utcnow() < self.circuit_open_until:
            return False

        # Status check
        if self.status in [AccountStatus.QUOTA_EXCEEDED, AccountStatus.ERROR]:
            return False

        # Quota check
        if self.quota_used >= self.quota_daily:
            self.status = AccountStatus.QUOTA_EXCEEDED
            return False

        return True

    def quota_percentage(self) -> float:
        """Get quota usage percentage."""
        return (self.quota_used / self.quota_daily * 100) if self.quota_daily > 0 else 0

    def success_rate(self) -> float:
        """Get success rate percentage."""
        return (self.success_count / self.total_requests * 100) if self.total_requests > 0 else 0


class ManusAccountPool:
    """
    Manages pool of Manus.space accounts with load balancing and failover.

    Strategy:
    - Round-robin selection among healthy accounts
    - Automatic failover to standby on quota exhaustion
    - Circuit breaker for failing accounts (5 errors = 5min timeout)
    - Health monitoring and metrics
    """

    def __init__(self, accounts: List[ManusAccount]):
        """Initialize account pool."""
        self.accounts = accounts
        self.current_index = 0
        self.circuit_breaker_threshold = 5  # Errors before circuit opens
        self.circuit_breaker_timeout = 300  # 5 minutes

        # Sort by priority (P0 first)
        self.accounts.sort(key=lambda a: a.priority)

        logger.info(f"🤲 Manus Account Pool initialized with {len(accounts)} accounts")
        for account in accounts:
            logger.info(
                f"  Account {account.account_id}: {account.status.value} "
                f"(P{account.priority}, {account.quota_daily} quota/day)"
            )

    def get_next_account(self) -> Optional[ManusAccount]:
        """
        Get next available account using round-robin + health checks.

        Returns:
            Account if available, None if all accounts unavailable
        """
        attempts = 0
        max_attempts = len(self.accounts)

        while attempts < max_attempts:
            account = self.accounts[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.accounts)
            attempts += 1

            # Check if circuit breaker expired
            if account.circuit_open_until and datetime.utcnow() >= account.circuit_open_until:
                account.circuit_open_until = None
                account.error_count = 0
                account.status = AccountStatus.ACTIVE
                logger.info(f"🔄 Account {account.account_id} circuit breaker reset")

            if account.is_available():
                account.last_used = datetime.utcnow()
                logger.debug(f"✅ Selected account {account.account_id} (quota: {account.quota_percentage():.1f}%)")
                return account

        # All accounts unavailable
        logger.error("❌ No Manus accounts available - all exhausted or failed")
        return None

    def record_success(self, account: ManusAccount):
        """Record successful request."""
        account.success_count += 1
        account.total_requests += 1
        account.quota_used += 1
        account.error_count = max(0, account.error_count - 1)  # Decay errors on success

        if account.quota_used >= account.quota_daily:
            account.status = AccountStatus.QUOTA_EXCEEDED
            logger.warning(
                f"⚠️ Account {account.account_id} quota exhausted "
                f"({account.quota_used}/{account.quota_daily})"
            )

    def record_failure(self, account: ManusAccount, error: Exception):
        """Record failed request and check circuit breaker."""
        account.error_count += 1
        account.total_requests += 1

        logger.warning(
            f"⚠️ Account {account.account_id} error ({account.error_count}/{self.circuit_breaker_threshold}): {error}"
        )

        # Circuit breaker
        if account.error_count >= self.circuit_breaker_threshold:
            account.status = AccountStatus.CIRCUIT_OPEN
            account.circuit_open_until = datetime.utcnow() + timedelta(seconds=self.circuit_breaker_timeout)
            logger.error(
                f"🔴 Account {account.account_id} circuit breaker OPEN "
                f"(timeout: {self.circuit_breaker_timeout}s)"
            )

    async def execute_with_retry(
        self,
        func: callable,
        *args,
        max_retries: int = 3,
        **kwargs
    ) -> Any:
        """
        Execute function with automatic account failover.

        Args:
            func: Async function to execute (receives account as first arg)
            max_retries: Maximum retry attempts with different accounts
            *args, **kwargs: Additional arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If all retries exhausted
        """
        last_error = None

        for attempt in range(max_retries):
            account = self.get_next_account()

            if not account:
                raise RuntimeError("No Manus accounts available")

            try:
                # Execute function with selected account
                result = await func(account, *args, **kwargs)

                # Record success
                self.record_success(account)

                if attempt > 0:
                    logger.info(f"✅ Request succeeded after {attempt + 1} attempts")

                return result

            except Exception as e:
                last_error = e
                self.record_failure(account, e)

                if attempt < max_retries - 1:
                    logger.info(f"🔄 Retrying with different account ({attempt + 1}/{max_retries})...")
                    await asyncio.sleep(0.5)  # Brief delay before retry

        # All retries exhausted
        raise RuntimeError(f"All Manus account retries exhausted: {last_error}")

    def get_pool_status(self) -> Dict[str, Any]:
        """Get comprehensive pool status and metrics."""
        available_accounts = [a for a in self.accounts if a.is_available()]
        total_quota_used = sum(a.quota_used for a in self.accounts)
        total_quota_available = sum(a.quota_daily for a in self.accounts)

        status = {
            "total_accounts": len(self.accounts),
            "available_accounts": len(available_accounts),
            "quota_used": total_quota_used,
            "quota_available": total_quota_available,
            "quota_percentage": (total_quota_used / total_quota_available * 100) if total_quota_available > 0 else 0,
            "accounts": []
        }

        for account in self.accounts:
            status["accounts"].append({
                "account_id": account.account_id,
                "status": account.status.value,
                "priority": f"P{account.priority}",
                "quota_used": account.quota_used,
                "quota_daily": account.quota_daily,
                "quota_percentage": account.quota_percentage(),
                "success_rate": account.success_rate(),
                "total_requests": account.total_requests,
                "error_count": account.error_count,
                "circuit_open": account.circuit_open_until is not None,
                "last_used": account.last_used.isoformat() if account.last_used else None
            })

        return status

    def reset_daily_quotas(self):
        """Reset all account quotas (call daily at midnight UTC)."""
        for account in self.accounts:
            account.quota_used = 0
            if account.status == AccountStatus.QUOTA_EXCEEDED:
                account.status = AccountStatus.ACTIVE

        logger.info("🔄 All Manus account quotas reset")


# ============================================================================
# GLOBAL POOL INSTANCE
# ============================================================================

_manus_pool: Optional[ManusAccountPool] = None


def initialize_manus_pool(account_configs: List[Dict[str, Any]]) -> ManusAccountPool:
    """
    Initialize global Manus account pool from configuration.

    Args:
        account_configs: List of account configurations
            [{"account_id": "manus1", "api_key": "...", "priority": 0}, ...]

    Returns:
        Initialized ManusAccountPool
    """
    global _manus_pool

    accounts = []
    for config in account_configs:
        account = ManusAccount(
            account_id=config["account_id"],
            api_key=config["api_key"],
            quota_daily=config.get("quota_daily", 10000),
            priority=config.get("priority", 2),
            status=AccountStatus(config.get("status", "active"))
        )
        accounts.append(account)

    _manus_pool = ManusAccountPool(accounts)
    return _manus_pool


def get_manus_pool() -> Optional[ManusAccountPool]:
    """Get global Manus account pool instance."""
    return _manus_pool


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_manus_request(account: ManusAccount, prompt: str) -> Dict:
    """
    Example function showing how to use an account from the pool.

    Args:
        account: ManusAccount from pool
        prompt: Request prompt

    Returns:
        Response from Manus API
    """
    # Simulate Manus API call
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.manus.space/v1/completion",
            headers={"Authorization": f"Bearer {account.api_key}"},
            json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()


async def demo():
    """Demo of Manus account pool usage."""
    # Initialize pool
    pool = initialize_manus_pool([
        {"account_id": "manus_primary", "api_key": "key1", "priority": 0},
        {"account_id": "manus_secondary", "api_key": "key2", "priority": 0},
        {"account_id": "manus_tertiary", "api_key": "key3", "priority": 1},
        {"account_id": "manus_reserve1", "api_key": "key4", "priority": 2},
        {"account_id": "manus_reserve2", "api_key": "key5", "priority": 2},
    ])

    # Execute request with automatic failover
    try:
        result = await pool.execute_with_retry(
            example_manus_request,
            prompt="Hello, Manus!"
        )
        print("✅ Request succeeded:", result)
    except RuntimeError as e:
        print("❌ All accounts failed:", e)

    # Check pool status
    status = pool.get_pool_status()
    print("\n📊 Pool Status:")
    print(f"Available: {status['available_accounts']}/{status['total_accounts']}")
    print(f"Quota: {status['quota_percentage']:.1f}%")


if __name__ == "__main__":
    asyncio.run(demo())

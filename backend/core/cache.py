"""
🚀 Redis Caching Service
High-performance caching for expensive operations
"""

import json
import os
from typing import Any, Callable, Optional, Union

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from loguru import logger
from redis import asyncio as aioredis


# Cache TTL configurations (in seconds)
class CacheTTL:
    """Cache Time-To-Live configurations"""

    # Hot data (1-5 minutes)
    UCF_STATE = 60  # 1 minute
    AGENT_STATUS = 120  # 2 minutes
    LIVE_METRICS = 60  # 1 minute

    # Warm data (15-60 minutes)
    USER_PROFILE = 900  # 15 minutes
    SUBSCRIPTION_STATUS = 1800  # 30 minutes
    API_KEY_VALIDATION = 3600  # 1 hour

    # Cold data (1-24 hours)
    AGENT_PROFILES = 3600  # 1 hour
    MARKETPLACE_LISTINGS = 7200  # 2 hours
    ANALYTICS_AGGREGATIONS = 86400  # 24 hours


class CacheService:
    """Redis caching service"""

    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.enabled = False
        self.prefix = "helix:"

    async def initialize(self, redis_url: Optional[str] = None):
        """
        Initialize Redis connection and FastAPI cache.

        Args:
            redis_url: Redis connection URL (default: from env)

        Example:
            >>> cache_service = CacheService()
            >>> await cache_service.initialize()
        """
        try:
            redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")

            # Connect to Redis
            self.redis = await aioredis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )

            # Test connection
            await self.redis.ping()

            # Initialize FastAPI cache
            FastAPICache.init(
                RedisBackend(self.redis),
                prefix=self.prefix
            )

            self.enabled = True
            logger.info(f"✅ Redis cache initialized: {redis_url}")

        except Exception as e:
            logger.warning(f"⚠️ Redis cache initialization failed: {e}")
            logger.info("📝 Continuing without cache (will use in-memory fallback)")
            self.enabled = False

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            logger.info("👋 Redis connection closed")

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found

        Example:
            >>> value = await cache_service.get("user:123")
        """
        if not self.enabled or not self.redis:
            return None

        try:
            value = await self.redis.get(f"{self.prefix}{key}")
            if value:
                logger.debug(f"🎯 Cache HIT: {key}")
                return json.loads(value)
            else:
                logger.debug(f"❌ Cache MISS: {key}")
                return None
        except Exception as e:
            logger.error(f"❌ Cache get error for {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = CacheTTL.USER_PROFILE
    ) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            True if successful

        Example:
            >>> await cache_service.set("user:123", user_data, ttl=900)
        """
        if not self.enabled or not self.redis:
            return False

        try:
            serialized = json.dumps(value, default=str)
            await self.redis.setex(
                f"{self.prefix}{key}",
                ttl,
                serialized
            )
            logger.debug(f"💾 Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"❌ Cache set error for {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if successful

        Example:
            >>> await cache_service.delete("user:123")
        """
        if not self.enabled or not self.redis:
            return False

        try:
            await self.redis.delete(f"{self.prefix}{key}")
            logger.debug(f"🗑️ Cache DELETE: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Cache delete error for {key}: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern.

        Args:
            pattern: Key pattern (e.g., "user:*")

        Returns:
            Number of keys deleted

        Example:
            >>> deleted = await cache_service.clear_pattern("user:*")
        """
        if not self.enabled or not self.redis:
            return 0

        try:
            keys = []
            async for key in self.redis.scan_iter(f"{self.prefix}{pattern}"):
                keys.append(key)

            if keys:
                deleted = await self.redis.delete(*keys)
                logger.info(f"🗑️ Cache CLEAR: {pattern} ({deleted} keys)")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"❌ Cache clear error for {pattern}: {e}")
            return 0

    async def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats

        Example:
            >>> stats = await cache_service.get_stats()
        """
        if not self.enabled or not self.redis:
            return {"enabled": False}

        try:
            info = await self.redis.info("stats")
            return {
                "enabled": True,
                "total_connections": info.get("total_connections_received", 0),
                "total_commands": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.error(f"❌ Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}

    @staticmethod
    def _calculate_hit_rate(hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage"""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)


# Global cache service instance
cache_service = CacheService()


def cache_key(*args, **kwargs) -> str:
    """
    Generate cache key from function arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Cache key string

    Example:
        >>> key = cache_key("user", user_id=123)
        'user:user_id=123'
    """
    parts = [str(arg) for arg in args]
    parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return ":".join(parts)


def cached(
    ttl: int = CacheTTL.USER_PROFILE,
    key_builder: Optional[Callable] = None
):
    """
    Decorator for caching function results.

    Args:
        ttl: Time-to-live in seconds
        key_builder: Optional custom key builder function

    Example:
        @cached(ttl=CacheTTL.AGENT_PROFILES)
        async def get_agent_profile(agent_id: str):
            # Expensive operation
            return await fetch_agent_profile(agent_id)
    """
    return cache(expire=ttl, key_builder=key_builder)


# Convenience functions for common cache operations
async def cache_ucf_state(state: dict) -> bool:
    """Cache UCF state"""
    return await cache_service.set("ucf:state", state, CacheTTL.UCF_STATE)


async def get_cached_ucf_state() -> Optional[dict]:
    """Get cached UCF state"""
    return await cache_service.get("ucf:state")


async def cache_agent_status(agent_id: str, status: dict) -> bool:
    """Cache agent status"""
    return await cache_service.set(
        f"agent:status:{agent_id}",
        status,
        CacheTTL.AGENT_STATUS
    )


async def get_cached_agent_status(agent_id: str) -> Optional[dict]:
    """Get cached agent status"""
    return await cache_service.get(f"agent:status:{agent_id}")


async def cache_user_profile(user_id: str, profile: dict) -> bool:
    """Cache user profile"""
    return await cache_service.set(
        f"user:profile:{user_id}",
        profile,
        CacheTTL.USER_PROFILE
    )


async def get_cached_user_profile(user_id: str) -> Optional[dict]:
    """Get cached user profile"""
    return await cache_service.get(f"user:profile:{user_id}")


async def invalidate_user_cache(user_id: str) -> int:
    """Invalidate all user-related cache"""
    return await cache_service.clear_pattern(f"user:*:{user_id}")


# Export
__all__ = [
    "CacheService",
    "CacheTTL",
    "cache_service",
    "cache_key",
    "cached",
    "cache_ucf_state",
    "get_cached_ucf_state",
    "cache_agent_status",
    "get_cached_agent_status",
    "cache_user_profile",
    "get_cached_user_profile",
    "invalidate_user_cache"
]

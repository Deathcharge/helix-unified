"""
🌀 Helix Collective v17.0 - Core Optimization Module
backend/core/__init__.py

Core performance optimization utilities for Railway backend:
- Response caching with TTL
- State management with file watching
- Webhook routing with circuit breaker
- Performance metrics collection
"""

from .cache_manager import ResponseCache, cached_response, get_cache
from .state_manager import UCFStateManager, get_state_manager
from .webhook_router import WebhookRouter, CircuitBreaker
from .metrics import MetricsCollector, get_metrics_collector

__all__ = [
    "ResponseCache",
    "cached_response",
    "get_cache",
    "UCFStateManager",
    "get_state_manager",
    "WebhookRouter",
    "CircuitBreaker",
    "MetricsCollector",
    "get_metrics_collector",
]

__version__ = "17.0.0"

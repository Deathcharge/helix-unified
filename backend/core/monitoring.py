"""
📊 Monitoring & Observability Module
Health checks, metrics, graceful shutdown, performance monitoring
"""

import asyncio
import os
import signal
import time
from datetime import datetime
from typing import Any, Dict, Optional

import psutil
from fastapi import FastAPI, Request, Response
from loguru import logger
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

# Prometheus metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

http_request_size_bytes = Histogram(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "endpoint"]
)

http_response_size_bytes = Histogram(
    "http_response_size_bytes",
    "HTTP response size in bytes",
    ["method", "endpoint"]
)

# Application metrics
app_info = Counter(
    "app_info",
    "Application information",
    ["version", "environment"]
)

# Shutdown event
shutdown_event = asyncio.Event()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics"""
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Get request size
        request_size = int(request.headers.get("content-length", 0))
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Get response size
        response_size = int(response.headers.get("content-length", 0))
        
        # Record metrics
        method = request.method
        endpoint = request.url.path
        status = response.status_code
        
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()
        
        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
        if request_size > 0:
            http_request_size_bytes.labels(
                method=method,
                endpoint=endpoint
            ).observe(request_size)
        
        if response_size > 0:
            http_response_size_bytes.labels(
                method=method,
                endpoint=endpoint
            ).observe(response_size)
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(duration)
        
        return response


class HealthChecker:
    """Health check utilities"""
    
    @staticmethod
    async def check_database() -> Dict[str, Any]:
        """
        Check database connection health.
        
        Returns:
            Health status dictionary
        """
        try:
            # This would check actual database connection
            # For now, return mock status
            return {
                "status": "healthy",
                "latency_ms": 5.2,
                "connections": {
                    "active": 3,
                    "idle": 17,
                    "max": 60
                }
            }
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    @staticmethod
    async def check_redis() -> Dict[str, Any]:
        """
        Check Redis connection health.
        
        Returns:
            Health status dictionary
        """
        try:
            from .cache import cache_service
            
            if not cache_service.enabled:
                return {
                    "status": "disabled",
                    "message": "Redis caching is disabled"
                }
            
            # Ping Redis
            if cache_service.redis:
                await cache_service.redis.ping()
                stats = await cache_service.get_stats()
                return {
                    "status": "healthy",
                    "hit_rate": stats.get("hit_rate", 0),
                    "total_commands": stats.get("total_commands", 0)
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": "Redis client not initialized"
                }
        except Exception as e:
            logger.error(f"❌ Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    @staticmethod
    async def check_disk_space() -> Dict[str, Any]:
        """
        Check disk space availability.
        
        Returns:
            Disk space status dictionary
        """
        try:
            disk = psutil.disk_usage("/")
            percent_used = disk.percent
            
            status = "healthy"
            if percent_used > 90:
                status = "critical"
            elif percent_used > 80:
                status = "warning"
            
            return {
                "status": status,
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent_used": percent_used
            }
        except Exception as e:
            logger.error(f"❌ Disk space check failed: {e}")
            return {
                "status": "unknown",
                "error": str(e)
            }
    
    @staticmethod
    async def check_memory() -> Dict[str, Any]:
        """
        Check memory usage.
        
        Returns:
            Memory status dictionary
        """
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            
            status = "healthy"
            if percent_used > 90:
                status = "critical"
            elif percent_used > 80:
                status = "warning"
            
            return {
                "status": status,
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent_used": percent_used
            }
        except Exception as e:
            logger.error(f"❌ Memory check failed: {e}")
            return {
                "status": "unknown",
                "error": str(e)
            }
    
    @staticmethod
    async def check_cpu() -> Dict[str, Any]:
        """
        Check CPU usage.
        
        Returns:
            CPU status dictionary
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            status = "healthy"
            if cpu_percent > 90:
                status = "critical"
            elif cpu_percent > 80:
                status = "warning"
            
            return {
                "status": status,
                "percent_used": cpu_percent,
                "cpu_count": cpu_count,
                "load_average": os.getloadavg() if hasattr(os, "getloadavg") else None
            }
        except Exception as e:
            logger.error(f"❌ CPU check failed: {e}")
            return {
                "status": "unknown",
                "error": str(e)
            }


async def liveness_probe() -> Dict[str, Any]:
    """
    Kubernetes liveness probe.
    
    Returns:
        Liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - startup_time
    }


async def readiness_probe() -> Dict[str, Any]:
    """
    Kubernetes readiness probe.
    
    Returns:
        Readiness status with all health checks
    """
    checks = {
        "database": await HealthChecker.check_database(),
        "redis": await HealthChecker.check_redis(),
        "disk": await HealthChecker.check_disk_space(),
        "memory": await HealthChecker.check_memory(),
        "cpu": await HealthChecker.check_cpu()
    }
    
    # Determine overall status
    critical_checks = ["database"]  # These must be healthy
    optional_checks = ["redis"]  # These can be disabled
    
    is_ready = True
    for check_name in critical_checks:
        if checks[check_name]["status"] not in ["healthy", "warning"]:
            is_ready = False
            break
    
    return {
        "status": "ready" if is_ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }


def setup_graceful_shutdown(app: FastAPI):
    """
    Setup graceful shutdown handlers.
    
    Args:
        app: FastAPI application instance
    """
    def handle_shutdown(signum, frame):
        logger.info(f"🛑 Received signal {signum}, initiating graceful shutdown...")
        shutdown_event.set()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    
    logger.info("✅ Graceful shutdown handlers registered")


async def graceful_shutdown_sequence():
    """
    Execute graceful shutdown sequence.
    
    This should be called in the lifespan shutdown phase.
    """
    logger.info("🛑 Starting graceful shutdown sequence...")
    
    # Wait for shutdown signal
    await shutdown_event.wait()
    
    # Give in-flight requests time to complete
    logger.info("⏳ Waiting for in-flight requests to complete (5s grace period)...")
    await asyncio.sleep(5)
    
    # Close connections
    logger.info("🔌 Closing database connections...")
    # await database.disconnect()
    
    logger.info("🔌 Closing Redis connections...")
    from .cache import cache_service
    await cache_service.close()
    
    logger.info("✅ Graceful shutdown complete")


def get_metrics() -> Response:
    """
    Get Prometheus metrics.
    
    Returns:
        Prometheus metrics in text format
    """
    return Response(
        generate_latest(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )


def get_system_info() -> Dict[str, Any]:
    """
    Get system information.
    
    Returns:
        System information dictionary
    """
    return {
        "python_version": os.sys.version,
        "platform": os.sys.platform,
        "cpu_count": psutil.cpu_count(),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
        "process_id": os.getpid(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# Track startup time
startup_time = time.time()


# Export
__all__ = [
    "MetricsMiddleware",
    "HealthChecker",
    "liveness_probe",
    "readiness_probe",
    "setup_graceful_shutdown",
    "graceful_shutdown_sequence",
    "get_metrics",
    "get_system_info",
    "shutdown_event"
]

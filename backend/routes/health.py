"""
🏥 Health Check Routes
Kubernetes liveness/readiness probes, system metrics
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from ..core.monitoring import (
    get_metrics,
    get_system_info,
    liveness_probe,
    readiness_probe
)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
async def health_liveness():
    """
    Kubernetes liveness probe.
    
    Returns 200 if the application is alive.
    This endpoint should always return 200 unless the process is completely dead.
    
    ## Response
    - **status**: "alive"
    - **timestamp**: Current UTC timestamp
    - **uptime_seconds**: Application uptime in seconds
    
    ## Example Response
    ```json
    {
      "status": "alive",
      "timestamp": "2025-12-08T10:30:00.000Z",
      "uptime_seconds": 3600.5
    }
    ```
    """
    return await liveness_probe()


@router.get("/ready")
async def health_readiness():
    """
    Kubernetes readiness probe.
    
    Returns 200 if the application is ready to serve traffic.
    Returns 503 if any critical dependency is unavailable.
    
    ## Checks Performed
    - **database**: PostgreSQL connection health
    - **redis**: Redis cache connection (optional)
    - **disk**: Disk space availability
    - **memory**: Memory usage
    - **cpu**: CPU usage
    
    ## Response
    - **status**: "ready" or "not_ready"
    - **timestamp**: Current UTC timestamp
    - **checks**: Health status of each dependency
    
    ## Example Response
    ```json
    {
      "status": "ready",
      "timestamp": "2025-12-08T10:30:00.000Z",
      "checks": {
        "database": {
          "status": "healthy",
          "latency_ms": 5.2,
          "connections": {"active": 3, "idle": 17, "max": 60}
        },
        "redis": {
          "status": "healthy",
          "hit_rate": 85.3,
          "total_commands": 12450
        },
        "disk": {
          "status": "healthy",
          "total_gb": 100.0,
          "used_gb": 45.2,
          "free_gb": 54.8,
          "percent_used": 45.2
        },
        "memory": {
          "status": "healthy",
          "total_gb": 16.0,
          "used_gb": 8.5,
          "available_gb": 7.5,
          "percent_used": 53.1
        },
        "cpu": {
          "status": "healthy",
          "percent_used": 35.2,
          "cpu_count": 8
        }
      }
    }
    ```
    """
    result = await readiness_probe()
    
    if result["status"] == "not_ready":
        raise HTTPException(
            status_code=503,
            detail=result
        )
    
    return result


@router.get("/startup")
async def health_startup():
    """
    Kubernetes startup probe.
    
    Returns 200 once the application has completed initialization.
    This is useful for slow-starting applications.
    
    ## Response
    Same as /health/ready
    """
    return await health_readiness()


@router.get("/metrics")
async def health_metrics():
    """
    Prometheus metrics endpoint.
    
    Returns metrics in Prometheus text format for scraping.
    
    ## Metrics Exposed
    - **http_requests_total**: Total HTTP requests by method, endpoint, status
    - **http_request_duration_seconds**: HTTP request duration histogram
    - **http_request_size_bytes**: HTTP request size histogram
    - **http_response_size_bytes**: HTTP response size histogram
    - **app_info**: Application version and environment
    
    ## Example Usage
    ```yaml
    # prometheus.yml
    scrape_configs:
      - job_name: 'helix-api'
        static_configs:
          - targets: ['localhost:8000']
        metrics_path: '/health/metrics'
    ```
    """
    return get_metrics()


@router.get("/info")
async def health_info():
    """
    System information endpoint.
    
    Returns detailed system and application information.
    
    ## Response
    - **python_version**: Python version
    - **platform**: Operating system platform
    - **cpu_count**: Number of CPU cores
    - **memory_total_gb**: Total system memory in GB
    - **disk_total_gb**: Total disk space in GB
    - **process_id**: Current process ID
    - **environment**: Current environment (development/production)
    
    ## Example Response
    ```json
    {
      "python_version": "3.11.5",
      "platform": "linux",
      "cpu_count": 8,
      "memory_total_gb": 16.0,
      "disk_total_gb": 100.0,
      "process_id": 12345,
      "environment": "production"
    }
    ```
    """
    return get_system_info()


@router.get("/ping")
async def health_ping():
    """
    Simple ping endpoint.
    
    Returns "pong" immediately. Useful for basic connectivity tests.
    
    ## Response
    ```json
    {
      "status": "pong"
    }
    ```
    """
    return {"status": "pong"}


# Export router
__all__ = ["router"]

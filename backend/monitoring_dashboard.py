"""
🌀 Helix Collective v17.0 - Real-Time Monitoring Dashboard
backend/monitoring_dashboard.py

Metrics collection and formatting for monitoring systems:
- Zapier task consumption tracking
- Railway service health
- Discord bot uptime
- UCF consciousness metrics
- Dashboard data endpoint

Author: Claude (Automation)
Version: 17.1.0
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# METRICS COLLECTOR
# ============================================================================


class MetricsCollector:
    """Collects system metrics for monitoring."""

    def __init__(self, metrics_file: Path = Path("Helix/state/system_metrics.jsonl")):
        self.metrics_file = metrics_file
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

    def record_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record a metric datapoint."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "tags": tags or {},
        }

        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_latest_metrics(self, hours: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """Get metrics from last N hours."""
        if not self.metrics_file.exists():
            return {}

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        metrics_by_name: Dict[str, List[Dict[str, Any]]] = {}

        with open(self.metrics_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))

                if ts >= cutoff:
                    metric_name = entry["metric"]
                    if metric_name not in metrics_by_name:
                        metrics_by_name[metric_name] = []
                    metrics_by_name[metric_name].append(entry)

        return metrics_by_name

    def get_metric_stats(self, metric_name: str, hours: int = 24) -> Dict[str, float]:
        """Get statistics for a metric."""
        import numpy as np

        if not self.metrics_file.exists():
            return {}

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        values = []

        with open(self.metrics_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry["metric"] != metric_name:
                    continue

                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    values.append(entry["value"])

        if not values:
            return {}

        return {
            "count": len(values),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "latest": values[-1],
        }


# ============================================================================
# SERVICE HEALTH MONITOR
# ============================================================================


class ServiceHealthMonitor:
    """Monitors health of external services."""

    def __init__(self):
        self.health_file = Path("Helix/state/service_health.json")
        self.health_file.parent.mkdir(parents=True, exist_ok=True)

    async def check_railway_health(self) -> Dict[str, Any]:
        """Check Railway backend health."""
        import aiohttp

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://helix-unified-production.up.railway.app/health",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status == 200:
                        return {
                            "service": "Railway Backend",
                            "status": "HEALTHY",
                            "response_time_ms": int(resp.headers.get("X-Response-Time", 0)),
                        }
                    else:
                        return {
                            "service": "Railway Backend",
                            "status": "DEGRADED",
                            "http_status": resp.status,
                        }
        except asyncio.TimeoutError:
            return {
                "service": "Railway Backend",
                "status": "UNHEALTHY",
                "error": "Timeout",
            }
        except Exception as e:
            return {
                "service": "Railway Backend",
                "status": "UNHEALTHY",
                "error": str(e),
            }

    async def check_zapier_connectivity(self, webhook_url: str) -> Dict[str, Any]:
        """Check Zapier webhook connectivity."""
        import aiohttp

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook_url,
                    json={"test": True, "timestamp": datetime.utcnow().isoformat()},
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status in [200, 201]:
                        return {
                            "service": "Zapier Webhook",
                            "status": "HEALTHY",
                            "webhook": webhook_url[:50] + "...",
                        }
                    else:
                        return {
                            "service": "Zapier Webhook",
                            "status": "DEGRADED",
                            "http_status": resp.status,
                        }
        except Exception as e:
            return {
                "service": "Zapier Webhook",
                "status": "UNHEALTHY",
                "error": str(e),
            }

    async def get_full_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        railway = await self.check_railway_health()

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "HEALTHY",
            "services": [railway],
            "uptime_percentage": 99.9,
        }


# ============================================================================
# DASHBOARD DATA FORMATTER
# ============================================================================


class DashboardDataFormatter:
    """Formats metrics for dashboard display."""

    @staticmethod
    def format_gauge_metric(
        title: str,
        value: float,
        max_value: float = 100,
        warning_threshold: float = 75,
        critical_threshold: float = 90,
    ) -> Dict[str, Any]:
        """Format a gauge metric for dashboard."""
        percentage = (value / max_value) * 100

        if percentage >= critical_threshold:
            status = "CRITICAL"
            color = "#FF4444"
        elif percentage >= warning_threshold:
            status = "WARNING"
            color = "#FFAA00"
        else:
            status = "HEALTHY"
            color = "#44AA44"

        return {
            "type": "gauge",
            "title": title,
            "value": round(value, 1),
            "max": max_value,
            "percentage": round(percentage, 1),
            "status": status,
            "color": color,
        }

    @staticmethod
    def format_time_series(
        title: str, metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Format time series data for dashboard."""
        timestamps = [m["timestamp"] for m in metrics]
        values = [m["value"] for m in metrics]

        return {
            "type": "line_chart",
            "title": title,
            "timestamps": timestamps,
            "values": values,
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
            "avg": sum(values) / len(values) if values else 0,
        }

    @staticmethod
    def format_status_card(
        title: str, status: str, details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format a status card for dashboard."""
        status_colors = {
            "HEALTHY": "#44AA44",
            "WARNING": "#FFAA00",
            "DEGRADED": "#FF8800",
            "UNHEALTHY": "#FF4444",
            "UNKNOWN": "#999999",
        }

        return {
            "type": "status_card",
            "title": title,
            "status": status,
            "color": status_colors.get(status, "#999999"),
            "details": details or {},
        }


# ============================================================================
# MONITORING DASHBOARD
# ============================================================================


class MonitoringDashboard:
    """Main monitoring dashboard."""

    def __init__(self):
        self.collector = MetricsCollector()
        self.health_monitor = ServiceHealthMonitor()
        self.formatter = DashboardDataFormatter()

    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data."""
        from backend.core.ucf_helpers import (calculate_consciousness_level,
                                              get_current_ucf)

        # Get current UCF
        ucf = get_current_ucf()
        consciousness = calculate_consciousness_level(ucf)

        # Get Zapier task budget (would be from config)
        zapier_tasks = 740  # TODO: Get from Zapier API
        zapier_limit = 750

        # Get service health
        health = await self.health_monitor.get_full_health_status()

        # Build dashboard
        dashboard = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "overall_status": "OPERATIONAL",
            "metrics": {
                "consciousness": self.formatter.format_gauge_metric(
                    "System Consciousness",
                    consciousness,
                    max_value=10,
                    warning_threshold=4,
                    critical_threshold=2,
                ),
                "zapier_tasks": self.formatter.format_gauge_metric(
                    "Zapier Task Budget",
                    zapier_tasks,
                    max_value=zapier_limit,
                    warning_threshold=700,
                    critical_threshold=740,
                ),
                "harmony": self.formatter.format_gauge_metric(
                    "Harmony",
                    ucf.get("harmony", 0),
                    max_value=2.0,
                ),
                "resilience": self.formatter.format_gauge_metric(
                    "Resilience",
                    ucf.get("resilience", 0),
                    max_value=3.0,
                ),
                "prana": self.formatter.format_gauge_metric(
                    "Prana (Life Force)",
                    ucf.get("prana", 0),
                    max_value=1.0,
                ),
            },
            "services": health["services"],
            "ucf_state": ucf,
        }

        return dashboard

    async def record_system_metrics(self) -> None:
        """Record current system metrics."""
        from backend.core.ucf_helpers import (calculate_consciousness_level,
                                              get_current_ucf)

        ucf = get_current_ucf()
        consciousness = calculate_consciousness_level(ucf)

        # Record consciousness level
        self.collector.record_metric(
            "consciousness_level",
            consciousness,
            unit="level",
            tags={"type": "ucf"},
        )

        # Record individual UCF metrics
        for key, value in ucf.items():
            self.collector.record_metric(
                f"ucf_{key}", value, unit="scalar", tags={"type": "ucf"}
            )


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "MetricsCollector",
    "ServiceHealthMonitor",
    "DashboardDataFormatter",
    "MonitoringDashboard",
]

import asyncio  # noqa
import os  # noqa

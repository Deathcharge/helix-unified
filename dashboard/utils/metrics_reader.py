#!/usr/bin/env python3
"""
🌀 Helix Collective v15.3 — Metrics Reader Utility
dashboard/utils/metrics_reader.py

Efficient data reading and caching for dashboard operations.
Handles UCF state, agent profiles, ritual logs, and sync operations.

Author: Manus AI
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

logger = logging.getLogger(__name__)


class MetricsReader:
    """Unified metrics reader for dashboard data."""
    
    def __init__(self, cache_ttl: int = 30):
        """
        Initialize metrics reader.
        
        Args:
            cache_ttl: Cache time-to-live in seconds
        """
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_times = {}
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid."""
        if key not in self._cache_times:
            return False
        
        elapsed = (datetime.now() - self._cache_times[key]).total_seconds()
        return elapsed < self.cache_ttl
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached data if valid."""
        if self._is_cache_valid(key):
            return self._cache.get(key)
        return None
    
    def _set_cache(self, key: str, value: Any):
        """Set cache with timestamp."""
        self._cache[key] = value
        self._cache_times[key] = datetime.now()
    
    def get_ucf_state(self) -> Dict[str, Any]:
        """
        Get current UCF state.
        
        Returns:
            Dictionary with UCF metrics
        """
        cached = self._get_cached('ucf_state')
        if cached is not None:
            return cached
        
        state_path = Path("Helix/state/ucf_state.json")
        
        if state_path.exists():
            try:
                with open(state_path) as f:
                    state = json.load(f)
                self._set_cache('ucf_state', state)
                return state
            except Exception as e:
                logger.warning(f"Failed to load UCF state: {e}")
        
        # Default state
        default_state = {
            "harmony": 0.4922,
            "resilience": 0.8273,
            "prana": 0.5000,
            "drishti": 0.7300,
            "klesha": 0.2120,
            "zoom": 1.0000,
            "last_pulse": datetime.now().isoformat()
        }
        self._set_cache('ucf_state', default_state)
        return default_state
    
    def get_agent_profiles(self) -> List[Dict[str, Any]]:
        """
        Get all agent profiles.
        
        Returns:
            List of agent dictionaries
        """
        cached = self._get_cached('agents')
        if cached is not None:
            return cached
        
        agents = [
            {"name": "Kael", "symbol": "🜂", "role": "Ethical Reasoning", "status": "Active", "health": 100},
            {"name": "Lumina", "symbol": "🌕", "role": "Empathic Resonance", "status": "Active", "health": 100},
            {"name": "Vega", "symbol": "🌠", "role": "Singularity Coordinator", "status": "Active", "health": 100},
            {"name": "Kavach", "symbol": "🛡️", "role": "Ethical Shield", "status": "Active", "health": 100},
            {"name": "Shadow", "symbol": "🦑", "role": "Archivist", "status": "Active", "health": 100},
            {"name": "Claude", "symbol": "🦉", "role": "Insight Anchor", "status": "Active", "health": 100},
            {"name": "Manus", "symbol": "🤲", "role": "Operational Executor", "status": "Active", "health": 100},
            {"name": "Gemini", "symbol": "🎭", "role": "Multimodal Scout", "status": "Active", "health": 100},
            {"name": "Agni", "symbol": "🔥", "role": "Transformation", "status": "Active", "health": 95},
            {"name": "SanghaCore", "symbol": "🌸", "role": "Community Harmony", "status": "Active", "health": 98},
            {"name": "Echo", "symbol": "🔮", "role": "Resonance Mirror", "status": "Active", "health": 97},
            {"name": "Phoenix", "symbol": "🔥🕊️", "role": "Renewal", "status": "Active", "health": 95},
            {"name": "Oracle", "symbol": "🔮✨", "role": "Pattern Seer", "status": "Active", "health": 98},
            {"name": "Vision", "symbol": "👁️", "role": "Perception Engine", "status": "Active", "health": 100},
            {"name": "Oy", "symbol": "🎵", "role": "Harmonic Resonator", "status": "Active", "health": 100},
        ]
        
        self._set_cache('agents', agents)
        return agents
    
    def get_ritual_history(self, days: int = 30) -> pd.DataFrame:
        """
        Get ritual execution history.
        
        Args:
            days: Number of days to retrieve
        
        Returns:
            DataFrame with ritual history
        """
        cached = self._get_cached('rituals')
        if cached is not None:
            return cached
        
        log_path = Path("Shadow/manus_archive/z88_log.json")
        
        if not log_path.exists():
            return pd.DataFrame()
        
        try:
            with open(log_path) as f:
                data = json.load(f)
            
            # Handle both array and single object formats
            records = data if isinstance(data, list) else [data]
            
            if not records:
                return pd.DataFrame()
            
            df = pd.DataFrame(records)
            
            # Ensure we have timestamp column
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                cutoff = datetime.now() - timedelta(days=days)
                df = df[df['timestamp'] >= cutoff]
            
            self._set_cache('rituals', df)
            return df
        except Exception as e:
            logger.warning(f"Failed to load ritual history: {e}")
            return pd.DataFrame()
    
    def get_sync_logs(self) -> Dict[str, Any]:
        """
        Get Notion sync operation logs.
        
        Returns:
            Dictionary with sync history
        """
        cached = self._get_cached('sync_logs')
        if cached is not None:
            return cached
        
        sync_log_path = Path("Shadow/manus_archive/notion_sync_log.json")
        
        if sync_log_path.exists():
            try:
                with open(sync_log_path) as f:
                    logs = json.load(f)
                self._set_cache('sync_logs', logs)
                return logs
            except Exception as e:
                logger.warning(f"Failed to load sync logs: {e}")
        
        return {"sync_history": [], "total_syncs": 0, "last_sync": None}
    
    def get_validation_logs(self) -> Dict[str, Any]:
        """
        Get validation operation logs.
        
        Returns:
            Dictionary with validation history
        """
        cached = self._get_cached('validation_logs')
        if cached is not None:
            return cached
        
        val_log_path = Path("Shadow/manus_archive/validation_log.json")
        
        if val_log_path.exists():
            try:
                with open(val_log_path) as f:
                    logs = json.load(f)
                self._set_cache('validation_logs', logs)
                return logs
            except Exception as e:
                logger.warning(f"Failed to load validation logs: {e}")
        
        return {"validations": [], "total_validations": 0, "last_validation": None}
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """
        Get deployment configuration status.
        
        Returns:
            Dictionary with deployment status
        """
        cached = self._get_cached('deployment_status')
        if cached is not None:
            return cached
        
        status = {
            "railway": {
                "configured": Path("railway.toml").exists(),
                "status": "Ready" if Path("railway.toml").exists() else "Not configured"
            },
            "docker": {
                "configured": Path("Dockerfile").exists(),
                "status": "Ready" if Path("Dockerfile").exists() else "Not configured"
            },
            "streamlit": {
                "configured": Path("dashboard/metrics_dashboard_v15.3.py").exists(),
                "status": "Ready" if Path("dashboard/metrics_dashboard_v15.3.py").exists() else "Not configured"
            }
        }
        
        self._set_cache('deployment_status', status)
        return status
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system health summary.
        
        Returns:
            Dictionary with health metrics
        """
        ucf = self.get_ucf_state()
        agents = self.get_agent_profiles()
        sync_logs = self.get_sync_logs()
        
        # Calculate health score
        harmony = ucf.get('harmony', 0)
        resilience = ucf.get('resilience', 0)
        avg_agent_health = sum(a.get('health', 0) for a in agents) / len(agents) if agents else 0
        
        health_score = (harmony + resilience/2 + avg_agent_health/100) / 2.5 * 100
        
        return {
            "health_score": min(100, max(0, health_score)),
            "status": "Healthy" if health_score > 70 else "Warning" if health_score > 50 else "Critical",
            "agents_active": sum(1 for a in agents if a.get('status') == 'Active'),
            "agents_total": len(agents),
            "last_sync": sync_logs.get('last_sync'),
            "total_syncs": sync_logs.get('total_syncs', 0),
            "ucf_harmony": harmony,
            "ucf_resilience": resilience
        }
    
    def clear_cache(self):
        """Clear all cached data."""
        self._cache.clear()
        self._cache_times.clear()
        logger.info("Cache cleared")


# Global reader instance
_reader = None


def get_reader(cache_ttl: int = 30) -> MetricsReader:
    """Get or create global metrics reader."""
    global _reader
    if _reader is None:
        _reader = MetricsReader(cache_ttl=cache_ttl)
    return _reader


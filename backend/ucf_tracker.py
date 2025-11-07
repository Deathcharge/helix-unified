"""
UCF Tracker - Historical Harmony Data and Trend Analysis
Helix Collective v15.3 Dual Resonance

Tracks UCF metrics over time, analyzes trends, and provides predictions
for harmony evolution. Enables proactive maintenance and ritual scheduling.
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import statistics


class UCFTracker:
    """
    Tracks and analyzes UCF metrics over time.
    """
    
    def __init__(self, db_path: str = "backend/state/ucf_history.db"):
        """
        Initialize UCF tracker with database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ucf_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                harmony REAL NOT NULL,
                resilience REAL NOT NULL,
                prana REAL NOT NULL,
                drishti REAL NOT NULL,
                klesha REAL NOT NULL,
                zoom REAL NOT NULL,
                phase TEXT NOT NULL,
                context TEXT,
                agent TEXT
            )
        """)
        
        # Create rituals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rituals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ritual_name TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                intention TEXT,
                harmony_before REAL NOT NULL,
                harmony_after REAL NOT NULL,
                success INTEGER NOT NULL
            )
        """)
        
        # Create index on timestamp for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_timestamp 
            ON ucf_metrics(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rituals_timestamp 
            ON rituals(timestamp)
        """)
        
        conn.commit()
        conn.close()
    
    def record_metrics(
        self,
        harmony: float,
        resilience: float,
        prana: float,
        drishti: float,
        klesha: float,
        zoom: float,
        phase: str,
        context: Optional[str] = None,
        agent: Optional[str] = None
    ) -> int:
        """
        Record UCF metrics to database.
        
        Args:
            harmony: System coherence
            resilience: Recovery capability
            prana: Energy level
            drishti: Clarity
            klesha: Suffering
            zoom: Perspective
            phase: UCF phase
            context: Optional context
            agent: Optional agent name
        
        Returns:
            Record ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO ucf_metrics 
            (timestamp, harmony, resilience, prana, drishti, klesha, zoom, phase, context, agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, harmony, resilience, prana, drishti, klesha, zoom, phase, context, agent))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def record_ritual(
        self,
        ritual_name: str,
        agent_name: str,
        harmony_before: float,
        harmony_after: float,
        success: bool,
        intention: Optional[str] = None
    ) -> int:
        """
        Record ritual execution to database.
        
        Args:
            ritual_name: Name of the ritual
            agent_name: Agent performing ritual
            harmony_before: Harmony before ritual
            harmony_after: Harmony after ritual
            success: Whether ritual succeeded
            intention: Optional ritual intention
        
        Returns:
            Record ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO rituals 
            (timestamp, ritual_name, agent_name, intention, harmony_before, harmony_after, success)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, ritual_name, agent_name, intention, harmony_before, harmony_after, int(success)))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_recent_metrics(self, limit: int = 100) -> List[Dict]:
        """
        Get recent UCF metrics.
        
        Args:
            limit: Maximum number of records to return
        
        Returns:
            List of metric dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, harmony, resilience, prana, drishti, klesha, zoom, phase, context, agent
            FROM ucf_metrics
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        metrics = []
        for row in rows:
            metrics.append({
                "timestamp": row[0],
                "harmony": row[1],
                "resilience": row[2],
                "prana": row[3],
                "drishti": row[4],
                "klesha": row[5],
                "zoom": row[6],
                "phase": row[7],
                "context": row[8],
                "agent": row[9]
            })
        
        return metrics
    
    def get_metrics_in_range(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict]:
        """
        Get UCF metrics within a time range.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
        
        Returns:
            List of metric dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, harmony, resilience, prana, drishti, klesha, zoom, phase, context, agent
            FROM ucf_metrics
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_time.isoformat(), end_time.isoformat()))
        
        rows = cursor.fetchall()
        conn.close()
        
        metrics = []
        for row in rows:
            metrics.append({
                "timestamp": row[0],
                "harmony": row[1],
                "resilience": row[2],
                "prana": row[3],
                "drishti": row[4],
                "klesha": row[5],
                "zoom": row[6],
                "phase": row[7],
                "context": row[8],
                "agent": row[9]
            })
        
        return metrics
    
    def get_harmony_trend(self, hours: int = 24) -> Dict:
        """
        Analyze harmony trend over specified hours.
        
        Args:
            hours: Number of hours to analyze
        
        Returns:
            Trend analysis dictionary
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        metrics = self.get_metrics_in_range(start_time, end_time)
        
        if not metrics:
            return {
                "trend": "UNKNOWN",
                "direction": "STABLE",
                "current": 0.0,
                "average": 0.0,
                "min": 0.0,
                "max": 0.0,
                "change": 0.0,
                "data_points": 0
            }
        
        harmony_values = [m["harmony"] for m in metrics]
        
        current = harmony_values[-1] if harmony_values else 0.0
        average = statistics.mean(harmony_values) if harmony_values else 0.0
        min_val = min(harmony_values) if harmony_values else 0.0
        max_val = max(harmony_values) if harmony_values else 0.0
        
        # Calculate change from first to last
        change = harmony_values[-1] - harmony_values[0] if len(harmony_values) > 1 else 0.0
        
        # Determine direction
        if change > 0.01:
            direction = "RISING"
        elif change < -0.01:
            direction = "FALLING"
        else:
            direction = "STABLE"
        
        # Determine trend
        if current >= 0.60:
            trend = "HARMONIOUS"
        elif current >= 0.45:
            trend = "COHERENT"
        elif current >= 0.30:
            trend = "UNSTABLE"
        else:
            trend = "CRITICAL"
        
        return {
            "trend": trend,
            "direction": direction,
            "current": current,
            "average": average,
            "min": min_val,
            "max": max_val,
            "change": change,
            "data_points": len(harmony_values),
            "timespan_hours": hours
        }
    
    def predict_harmony(self, hours_ahead: int = 24) -> Dict:
        """
        Predict future harmony using simple linear regression.
        
        Args:
            hours_ahead: Hours to predict ahead
        
        Returns:
            Prediction dictionary
        """
        # Get last 48 hours of data
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=48)
        
        metrics = self.get_metrics_in_range(start_time, end_time)
        
        if len(metrics) < 2:
            return {
                "predicted_harmony": 0.0,
                "confidence": "LOW",
                "hours_ahead": hours_ahead,
                "data_points": len(metrics)
            }
        
        # Simple linear regression
        harmony_values = [m["harmony"] for m in metrics]
        n = len(harmony_values)
        
        # Calculate slope
        x_values = list(range(n))
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(harmony_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, harmony_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # Predict future value
        future_x = n + (hours_ahead / (48 / n))  # Scale to data point spacing
        predicted = slope * future_x + intercept
        
        # Clamp to valid range
        predicted = max(0.0, min(1.0, predicted))
        
        # Calculate confidence based on data variance
        variance = statistics.variance(harmony_values) if len(harmony_values) > 1 else 1.0
        
        if variance < 0.01:
            confidence = "HIGH"
        elif variance < 0.05:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        return {
            "predicted_harmony": predicted,
            "confidence": confidence,
            "hours_ahead": hours_ahead,
            "data_points": n,
            "slope": slope,
            "current": harmony_values[-1]
        }
    
    def get_ritual_history(self, limit: int = 50) -> List[Dict]:
        """
        Get recent ritual history.
        
        Args:
            limit: Maximum number of records
        
        Returns:
            List of ritual dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, ritual_name, agent_name, intention, 
                   harmony_before, harmony_after, success
            FROM rituals
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        rituals = []
        for row in rows:
            rituals.append({
                "timestamp": row[0],
                "ritual_name": row[1],
                "agent_name": row[2],
                "intention": row[3],
                "harmony_before": row[4],
                "harmony_after": row[5],
                "success": bool(row[6]),
                "delta": row[5] - row[4]
            })
        
        return rituals
    
    def get_ritual_effectiveness(self, ritual_name: str) -> Dict:
        """
        Analyze effectiveness of a specific ritual.
        
        Args:
            ritual_name: Name of the ritual
        
        Returns:
            Effectiveness analysis dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT harmony_before, harmony_after, success
            FROM rituals
            WHERE ritual_name = ?
        """, (ritual_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {
                "ritual_name": ritual_name,
                "executions": 0,
                "success_rate": 0.0,
                "average_delta": 0.0,
                "effectiveness": "UNKNOWN"
            }
        
        deltas = [after - before for before, after, _ in rows]
        successes = sum(1 for _, _, success in rows if success)
        
        executions = len(rows)
        success_rate = successes / executions if executions > 0 else 0.0
        average_delta = statistics.mean(deltas) if deltas else 0.0
        
        # Determine effectiveness
        if success_rate >= 0.8 and average_delta >= 0.05:
            effectiveness = "HIGHLY EFFECTIVE"
        elif success_rate >= 0.6 and average_delta >= 0.02:
            effectiveness = "EFFECTIVE"
        elif success_rate >= 0.4:
            effectiveness = "MODERATELY EFFECTIVE"
        else:
            effectiveness = "LOW EFFECTIVENESS"
        
        return {
            "ritual_name": ritual_name,
            "executions": executions,
            "success_rate": success_rate,
            "average_delta": average_delta,
            "effectiveness": effectiveness,
            "min_delta": min(deltas) if deltas else 0.0,
            "max_delta": max(deltas) if deltas else 0.0
        }
    
    def should_trigger_ritual(self, harmony_threshold: float = 0.40) -> Tuple[bool, str]:
        """
        Determine if a ritual should be triggered based on harmony.
        
        Args:
            harmony_threshold: Threshold below which to trigger ritual
        
        Returns:
            Tuple of (should_trigger, reason)
        """
        recent = self.get_recent_metrics(limit=1)
        
        if not recent:
            return False, "No recent metrics available"
        
        current_harmony = recent[0]["harmony"]
        
        if current_harmony < harmony_threshold:
            return True, f"Harmony {current_harmony:.4f} below threshold {harmony_threshold:.4f}"
        
        # Check trend
        trend = self.get_harmony_trend(hours=6)
        
        if trend["direction"] == "FALLING" and trend["change"] < -0.05:
            return True, f"Harmony falling rapidly (change: {trend['change']:.4f})"
        
        # Check prediction
        prediction = self.predict_harmony(hours_ahead=12)
        
        if prediction["predicted_harmony"] < harmony_threshold:
            return True, f"Predicted harmony {prediction['predicted_harmony']:.4f} below threshold"
        
        return False, "System stable"


# Example usage
if __name__ == "__main__":
    tracker = UCFTracker()
    
    # Record some test metrics
    print("Recording test metrics...")
    tracker.record_metrics(
        harmony=0.4922,
        resilience=1.1191,
        prana=0.5075,
        drishti=0.5023,
        klesha=0.011,
        zoom=1.0228,
        phase="COHERENT",
        context="System initialization",
        agent="Omega Zero"
    )
    
    # Get recent metrics
    print("\nRecent metrics:")
    recent = tracker.get_recent_metrics(limit=5)
    for metric in recent:
        print(f"  {metric['timestamp']}: harmony={metric['harmony']:.4f}, phase={metric['phase']}")
    
    # Analyze trend
    print("\nHarmony trend (24h):")
    trend = tracker.get_harmony_trend(hours=24)
    for key, value in trend.items():
        print(f"  {key}: {value}")
    
    # Check if ritual should be triggered
    print("\nRitual trigger check:")
    should_trigger, reason = tracker.should_trigger_ritual(harmony_threshold=0.50)
    print(f"  Should trigger: {should_trigger}")
    print(f"  Reason: {reason}")


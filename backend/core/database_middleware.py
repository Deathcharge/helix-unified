"""
🗄️ Database Middleware Module
Query logging, slow query detection, connection health monitoring
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from loguru import logger

# Configuration
SLOW_QUERY_THRESHOLD_MS = 100  # Log queries slower than 100ms
ENABLE_QUERY_LOGGING = True  # Set to False in production for performance

# Metrics
query_count = 0
slow_query_count = 0
total_query_time = 0.0


class DatabaseMetrics:
    """Track database query metrics"""
    
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.slow_queries: List[Dict[str, Any]] = []
        
    def record_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        duration_ms: float = 0.0,
        success: bool = True,
        error: Optional[str] = None
    ):
        """Record a database query execution"""
        global query_count, slow_query_count, total_query_time
        
        query_count += 1
        total_query_time += duration_ms
        
        query_info = {
            "query": query[:200],  # Truncate long queries
            "params": str(params)[:100] if params else None,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            "error": error,
            "timestamp": time.time()
        }
        
        # Log slow queries
        if duration_ms > SLOW_QUERY_THRESHOLD_MS:
            slow_query_count += 1
            self.slow_queries.append(query_info)
            logger.warning(
                f"🐌 Slow query detected ({duration_ms:.2f}ms): {query[:100]}..."
            )
        
        # Store recent queries (keep last 100)
        self.queries.append(query_info)
        if len(self.queries) > 100:
            self.queries.pop(0)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database query statistics"""
        avg_query_time = (
            total_query_time / query_count if query_count > 0 else 0
        )
        
        return {
            "total_queries": query_count,
            "slow_queries": slow_query_count,
            "avg_query_time_ms": round(avg_query_time, 2),
            "total_query_time_ms": round(total_query_time, 2),
            "recent_queries": len(self.queries),
            "recent_slow_queries": len(self.slow_queries)
        }
    
    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent slow queries"""
        return self.slow_queries[-limit:]


# Global metrics instance
db_metrics = DatabaseMetrics()


@asynccontextmanager
async def query_logger(query: str, params: Optional[tuple] = None):
    """
    Context manager for logging database queries.
    
    Usage:
        async with query_logger("SELECT * FROM users WHERE id = $1", (user_id,)):
            result = await db.fetchrow(query, user_id)
    """
    start_time = time.time()
    error = None
    success = True
    
    try:
        if ENABLE_QUERY_LOGGING:
            logger.debug(f"🗄️ Executing query: {query[:100]}...")
        yield
    except Exception as e:
        success = False
        error = str(e)
        logger.error(f"❌ Query failed: {query[:100]}... Error: {error}")
        raise
    finally:
        duration_ms = (time.time() - start_time) * 1000
        db_metrics.record_query(query, params, duration_ms, success, error)


def sanitize_query_for_logging(query: str, params: Optional[tuple] = None) -> str:
    """
    Sanitize query for logging (remove sensitive data).
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        Sanitized query string safe for logging
    """
    # Replace sensitive parameter values with placeholders
    if params:
        sanitized_params = []
        for param in params:
            if isinstance(param, str) and len(param) > 50:
                sanitized_params.append(f"<string:{len(param)} chars>")
            elif isinstance(param, (bytes, bytearray)):
                sanitized_params.append(f"<binary:{len(param)} bytes>")
            else:
                sanitized_params.append(str(param)[:50])
        
        return f"{query[:200]} | Params: {sanitized_params}"
    
    return query[:200]


async def check_database_health() -> Dict[str, Any]:
    """
    Check database connection health.
    
    Returns:
        Health status dictionary
    """
    try:
        # This would be implemented with actual database connection
        # For now, return metrics
        stats = db_metrics.get_stats()
        
        return {
            "status": "healthy",
            "metrics": stats,
            "slow_query_threshold_ms": SLOW_QUERY_THRESHOLD_MS
        }
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def detect_sql_injection_patterns(query: str) -> List[str]:
    """
    Detect potential SQL injection patterns in queries.
    
    This is a safety check - all queries should use parameterized queries.
    
    Args:
        query: SQL query string
        
    Returns:
        List of detected suspicious patterns
    """
    suspicious_patterns = []
    
    # Check for string concatenation in query
    if "+" in query or "||" in query:
        suspicious_patterns.append("String concatenation detected")
    
    # Check for f-strings or % formatting
    if "{" in query or "%" in query:
        suspicious_patterns.append("String formatting detected")
    
    # Check for common SQL injection keywords
    dangerous_keywords = [
        "'; DROP", "'; DELETE", "'; UPDATE", "'; INSERT",
        "UNION SELECT", "OR 1=1", "OR '1'='1"
    ]
    
    for keyword in dangerous_keywords:
        if keyword.upper() in query.upper():
            suspicious_patterns.append(f"Dangerous keyword: {keyword}")
    
    if suspicious_patterns:
        logger.critical(
            f"🚨 POTENTIAL SQL INJECTION DETECTED: {query[:100]}... "
            f"Patterns: {suspicious_patterns}"
        )
    
    return suspicious_patterns


class QueryValidator:
    """Validate queries before execution"""
    
    @staticmethod
    def validate_parameterized(query: str, params: Optional[tuple] = None) -> bool:
        """
        Validate that query uses parameterized queries.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            True if query is properly parameterized
        """
        # Check for parameter placeholders ($1, $2, etc.)
        import re
        param_placeholders = re.findall(r'\$\d+', query)
        
        if params and len(param_placeholders) != len(params):
            logger.warning(
                f"⚠️ Parameter count mismatch: "
                f"Query has {len(param_placeholders)} placeholders, "
                f"but {len(params)} params provided"
            )
            return False
        
        # Check for SQL injection patterns
        injection_patterns = detect_sql_injection_patterns(query)
        if injection_patterns:
            logger.critical(
                f"🚨 Query failed validation: {injection_patterns}"
            )
            return False
        
        return True


# Export utilities
__all__ = [
    "query_logger",
    "db_metrics",
    "DatabaseMetrics",
    "check_database_health",
    "detect_sql_injection_patterns",
    "QueryValidator",
    "sanitize_query_for_logging"
]

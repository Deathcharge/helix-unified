"""
🌀 Helix Spirals Storage Layer
PostgreSQL + Redis storage with Context Vault integration
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import asyncpg
import redis.asyncio as redis

from .models import (ExecutionContext, ExecutionStatus, Spiral,
                     SpiralStatistics, TriggerType, WebhookPayload)

logger = logging.getLogger(__name__)

class SpiralStorage:
    """Storage layer for Helix Spirals with Context Vault integration"""
    
    def __init__(self, pg_pool: asyncpg.Pool, redis_client: redis.Redis):
        self.pg_pool = pg_pool
        self.redis_client = redis_client
        
    async def initialize(self):
        """Initialize database schema"""
        await self._create_tables()
        await self._create_indexes()
        logger.info("✅ Storage layer initialized")
    
    async def _create_tables(self):
        """Create database tables for Helix Spirals"""
        async with self.pg_pool.acquire() as conn:
            # Spirals table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS spirals (
                    id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    version VARCHAR(50) DEFAULT '1.0.0',
                    enabled BOOLEAN DEFAULT true,
                    tags TEXT[],
                    trigger_data JSONB NOT NULL,
                    actions_data JSONB NOT NULL,
                    variables_data JSONB,
                    rate_limiting JSONB,
                    scheduling JSONB,
                    security JSONB,
                    metadata JSONB,
                    consciousness_level INTEGER DEFAULT 5,
                    assigned_agents TEXT[],
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Execution history table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS execution_history (
                    id UUID PRIMARY KEY,
                    spiral_id UUID NOT NULL,
                    execution_id UUID UNIQUE NOT NULL,
                    trigger_data JSONB NOT NULL,
                    variables JSONB,
                    logs JSONB,
                    status VARCHAR(50) NOT NULL,
                    started_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    current_action UUID,
                    error_data JSONB,
                    metrics JSONB,
                    ucf_impact JSONB,
                    consciousness_level INTEGER DEFAULT 5,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Spiral data table (Context Vault)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS spiral_data (
                    key VARCHAR(255) PRIMARY KEY,
                    value JSONB NOT NULL,
                    ttl INTEGER,
                    encrypted BOOLEAN DEFAULT false,
                    ucf_metadata JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Webhook mappings table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_mappings (
                    webhook_id VARCHAR(255) PRIMARY KEY,
                    spiral_id UUID NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # UCF metrics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ucf_metrics (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    spiral_id UUID,
                    execution_id UUID,
                    metric VARCHAR(50) NOT NULL,
                    value FLOAT NOT NULL,
                    operation VARCHAR(50),
                    source VARCHAR(255),
                    consciousness_level INTEGER,
                    timestamp TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Spiral statistics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS spiral_statistics (
                    spiral_id UUID PRIMARY KEY,
                    total_executions INTEGER DEFAULT 0,
                    successful_executions INTEGER DEFAULT 0,
                    failed_executions INTEGER DEFAULT 0,
                    average_execution_time_ms FLOAT DEFAULT 0,
                    last_execution TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
    
    async def _create_indexes(self):
        """Create database indexes for performance"""
        async with self.pg_pool.acquire() as conn:
            # Spirals indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_spirals_enabled ON spirals(enabled)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_spirals_consciousness ON spirals(consciousness_level)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_spirals_tags ON spirals USING GIN(tags)")
            
            # Execution history indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_execution_spiral_id ON execution_history(spiral_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_execution_status ON execution_history(status)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_execution_started_at ON execution_history(started_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_execution_consciousness ON execution_history(consciousness_level)")
            
            # UCF metrics indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ucf_spiral_id ON ucf_metrics(spiral_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ucf_metric ON ucf_metrics(metric)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_ucf_timestamp ON ucf_metrics(timestamp)")
            
            # Spiral data indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_spiral_data_created_at ON spiral_data(created_at)")
    
    async def save_spiral(self, spiral: Spiral) -> None:
        """Save spiral to database"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO spirals (
                    id, name, description, version, enabled, tags,
                    trigger_data, actions_data, variables_data,
                    rate_limiting, scheduling, security, metadata,
                    consciousness_level, assigned_agents, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                ON CONFLICT (id) DO UPDATE SET
                    name = $2, description = $3, version = $4, enabled = $5,
                    tags = $6, trigger_data = $7, actions_data = $8,
                    variables_data = $9, rate_limiting = $10, scheduling = $11,
                    security = $12, metadata = $13, consciousness_level = $14,
                    assigned_agents = $15, updated_at = $16
            """, 
                spiral.id, spiral.name, spiral.description, spiral.version,
                spiral.enabled, spiral.tags, spiral.trigger.dict(),
                [action.dict() for action in spiral.actions],
                [var.dict() for var in spiral.variables] if spiral.variables else None,
                spiral.rate_limiting.dict() if spiral.rate_limiting else None,
                spiral.scheduling.dict() if spiral.scheduling else None,
                spiral.security.dict() if spiral.security else None,
                spiral.metadata, 
                spiral.consciousness_level.value if spiral.consciousness_level else 5,
                spiral.assigned_agents, datetime.utcnow()
            )
        
        # Cache in Redis for fast access
        await self.redis_client.setex(
            f"spiral:{spiral.id}",
            3600,  # 1 hour cache
            spiral.json()
        )
        
        logger.info(f"Spiral saved: {spiral.name} (ID: {spiral.id})")
    
    async def get_spiral(self, spiral_id: str) -> Optional[Spiral]:
        """Get spiral by ID with Redis caching"""
        # Try Redis cache first
        cached = await self.redis_client.get(f"spiral:{spiral_id}")
        if cached:
            return Spiral.parse_raw(cached)
        
        # Fallback to database
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM spirals WHERE id = $1", spiral_id
            )
            
            if not row:
                return None
            
            spiral_data = {
                "id": str(row["id"]),
                "name": row["name"],
                "description": row["description"],
                "version": row["version"],
                "enabled": row["enabled"],
                "tags": row["tags"] or [],
                "trigger": row["trigger_data"],
                "actions": row["actions_data"],
                "variables": row["variables_data"] or [],
                "rate_limiting": row["rate_limiting"],
                "scheduling": row["scheduling"],
                "security": row["security"],
                "metadata": row["metadata"] or {},
                "consciousness_level": row["consciousness_level"],
                "assigned_agents": row["assigned_agents"] or []
            }
            
            spiral = Spiral(**spiral_data)
            
            # Cache for next time
            await self.redis_client.setex(
                f"spiral:{spiral_id}",
                3600,
                spiral.json()
            )
            
            return spiral
    
    async def get_all_spirals(self) -> List[Spiral]:
        """Get all spirals"""
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM spirals ORDER BY created_at DESC")
            
            spirals = []
            for row in rows:
                spiral_data = {
                    "id": str(row["id"]),
                    "name": row["name"],
                    "description": row["description"],
                    "version": row["version"],
                    "enabled": row["enabled"],
                    "tags": row["tags"] or [],
                    "trigger": row["trigger_data"],
                    "actions": row["actions_data"],
                    "variables": row["variables_data"] or [],
                    "rate_limiting": row["rate_limiting"],
                    "scheduling": row["scheduling"],
                    "security": row["security"],
                    "metadata": row["metadata"] or {},
                    "consciousness_level": row["consciousness_level"],
                    "assigned_agents": row["assigned_agents"] or []
                }
                spirals.append(Spiral(**spiral_data))
            
            return spirals
    
    async def get_spirals_by_trigger_type(self, trigger_type: TriggerType) -> List[Spiral]:
        """Get spirals by trigger type"""
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM spirals WHERE trigger_data->>'type' = $1 AND enabled = true",
                trigger_type.value
            )
            
            spirals = []
            for row in rows:
                spiral_data = {
                    "id": str(row["id"]),
                    "name": row["name"],
                    "description": row["description"],
                    "version": row["version"],
                    "enabled": row["enabled"],
                    "tags": row["tags"] or [],
                    "trigger": row["trigger_data"],
                    "actions": row["actions_data"],
                    "variables": row["variables_data"] or [],
                    "rate_limiting": row["rate_limiting"],
                    "scheduling": row["scheduling"],
                    "security": row["security"],
                    "metadata": row["metadata"] or {},
                    "consciousness_level": row["consciousness_level"],
                    "assigned_agents": row["assigned_agents"] or []
                }
                spirals.append(Spiral(**spiral_data))
            
            return spirals
    
    async def delete_spiral(self, spiral_id: str) -> bool:
        """Delete spiral"""
        async with self.pg_pool.acquire() as conn:
            result = await conn.execute("DELETE FROM spirals WHERE id = $1", spiral_id)
            
            # Remove from cache
            await self.redis_client.delete(f"spiral:{spiral_id}")
            
            return result == "DELETE 1"
    
    async def save_execution_history(self, context: ExecutionContext) -> None:
        """Save execution history with UCF tracking"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO execution_history (
                    id, spiral_id, execution_id, trigger_data, variables,
                    logs, status, started_at, completed_at, current_action,
                    error_data, metrics, ucf_impact, consciousness_level
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                ON CONFLICT (execution_id) DO UPDATE SET
                    status = $7, completed_at = $9, current_action = $10,
                    error_data = $11, metrics = $12, ucf_impact = $13
            """,
                context.execution_id, context.spiral_id, context.execution_id,
                context.trigger, context.variables,
                [log.dict() for log in context.logs], context.status.value,
                datetime.fromisoformat(context.started_at),
                datetime.fromisoformat(context.completed_at) if context.completed_at else None,
                context.current_action,
                context.error.dict() if context.error else None,
                context.metrics,
                context.ucf_impact if hasattr(context, 'ucf_impact') else {},
                context.variables.get("consciousness_level", 5)
            )
        
        # Store UCF metrics separately for analytics
        if hasattr(context, 'ucf_impact') and context.ucf_impact:
            await self._save_ucf_metrics(context)
        
        logger.info(f"Execution history saved: {context.execution_id}")
    
    async def _save_ucf_metrics(self, context: ExecutionContext) -> None:
        """Save UCF metrics for analytics"""
        async with self.pg_pool.acquire() as conn:
            for metric, value in context.ucf_impact.items():
                await conn.execute("""
                    INSERT INTO ucf_metrics (
                        spiral_id, execution_id, metric, value, source, consciousness_level
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                    context.spiral_id, context.execution_id, metric, value,
                    f"spiral:{context.spiral_id}",
                    context.variables.get("consciousness_level", 5)
                )
    
    async def get_execution_history(self, execution_id: str) -> Optional[ExecutionContext]:
        """Get execution history by ID"""
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM execution_history WHERE execution_id = $1",
                execution_id
            )
            
            if not row:
                return None
            
            # Reconstruct ExecutionContext
            context_data = {
                "spiral_id": str(row["spiral_id"]),
                "execution_id": str(row["execution_id"]),
                "trigger": row["trigger_data"],
                "variables": row["variables"] or {},
                "logs": row["logs"] or [],
                "status": ExecutionStatus(row["status"]),
                "started_at": row["started_at"].isoformat(),
                "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
                "current_action": row["current_action"],
                "error": row["error_data"],
                "metrics": row["metrics"] or {},
                "ucf_impact": row["ucf_impact"] or {}
            }
            
            return ExecutionContext(**context_data)
    
    async def get_recent_executions(self, limit: int = 100) -> List[ExecutionContext]:
        """Get recent executions"""
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM execution_history ORDER BY started_at DESC LIMIT $1",
                limit
            )
            
            executions = []
            for row in rows:
                context_data = {
                    "spiral_id": str(row["spiral_id"]),
                    "execution_id": str(row["execution_id"]),
                    "trigger": row["trigger_data"],
                    "variables": row["variables"] or {},
                    "logs": row["logs"] or [],
                    "status": ExecutionStatus(row["status"]),
                    "started_at": row["started_at"].isoformat(),
                    "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
                    "current_action": row["current_action"],
                    "error": row["error_data"],
                    "metrics": row["metrics"] or {},
                    "ucf_impact": row["ucf_impact"] or {}
                }
                executions.append(ExecutionContext(**context_data))
            
            return executions
    
    async def update_spiral_statistics(self, spiral_id: str, context: ExecutionContext) -> None:
        """Update spiral execution statistics"""
        execution_time = 0
        if context.completed_at and context.started_at:
            start_time = datetime.fromisoformat(context.started_at)
            end_time = datetime.fromisoformat(context.completed_at)
            execution_time = (end_time - start_time).total_seconds() * 1000  # milliseconds
        
        async with self.pg_pool.acquire() as conn:
            # Get current stats
            current_stats = await conn.fetchrow(
                "SELECT * FROM spiral_statistics WHERE spiral_id = $1",
                spiral_id
            )
            
            if current_stats:
                # Update existing stats
                total_executions = current_stats["total_executions"] + 1
                successful_executions = current_stats["successful_executions"]
                failed_executions = current_stats["failed_executions"]
                
                if context.status == ExecutionStatus.COMPLETED:
                    successful_executions += 1
                elif context.status == ExecutionStatus.FAILED:
                    failed_executions += 1
                
                # Calculate new average execution time
                current_avg = current_stats["average_execution_time_ms"]
                new_avg = ((current_avg * (total_executions - 1)) + execution_time) / total_executions
                
                await conn.execute("""
                    UPDATE spiral_statistics SET
                        total_executions = $2,
                        successful_executions = $3,
                        failed_executions = $4,
                        average_execution_time_ms = $5,
                        last_execution = $6,
                        updated_at = $7
                    WHERE spiral_id = $1
                """,
                    spiral_id, total_executions, successful_executions,
                    failed_executions, new_avg, datetime.utcnow(), datetime.utcnow()
                )
            else:
                # Create new stats
                successful = 1 if context.status == ExecutionStatus.COMPLETED else 0
                failed = 1 if context.status == ExecutionStatus.FAILED else 0
                
                await conn.execute("""
                    INSERT INTO spiral_statistics (
                        spiral_id, total_executions, successful_executions,
                        failed_executions, average_execution_time_ms, last_execution
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                    spiral_id, 1, successful, failed, execution_time, datetime.utcnow()
                )
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        async with self.pg_pool.acquire() as conn:
            # Basic counts
            total_spirals = await conn.fetchval("SELECT COUNT(*) FROM spirals")
            enabled_spirals = await conn.fetchval("SELECT COUNT(*) FROM spirals WHERE enabled = true")
            total_executions = await conn.fetchval("SELECT COUNT(*) FROM execution_history")
            successful_executions = await conn.fetchval(
                "SELECT COUNT(*) FROM execution_history WHERE status = 'completed'"
            )
            failed_executions = await conn.fetchval(
                "SELECT COUNT(*) FROM execution_history WHERE status = 'failed'"
            )
            
            # Average execution time
            avg_time = await conn.fetchval(
                "SELECT AVG(EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000) FROM execution_history WHERE completed_at IS NOT NULL"
            ) or 0
            
            # Last execution
            last_execution = await conn.fetchval(
                "SELECT MAX(started_at) FROM execution_history"
            )
            
            # Top spirals by execution count
            top_spirals = await conn.fetch("""
                SELECT s.name, s.id, COUNT(eh.id) as execution_count
                FROM spirals s
                LEFT JOIN execution_history eh ON s.id = eh.spiral_id
                GROUP BY s.id, s.name
                ORDER BY execution_count DESC
                LIMIT 10
            """)
            
            # UCF metrics summary
            ucf_summary = await conn.fetch("""
                SELECT metric, AVG(value) as avg_value, COUNT(*) as count
                FROM ucf_metrics
                WHERE timestamp > NOW() - INTERVAL '24 hours'
                GROUP BY metric
            """)
            
            # Consciousness level distribution
            consciousness_dist = await conn.fetch("""
                SELECT consciousness_level, COUNT(*) as count
                FROM execution_history
                WHERE started_at > NOW() - INTERVAL '24 hours'
                GROUP BY consciousness_level
                ORDER BY consciousness_level
            """)
            
            return {
                "total_spirals": total_spirals,
                "enabled_spirals": enabled_spirals,
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
                "average_execution_time_ms": float(avg_time),
                "last_execution": last_execution.isoformat() if last_execution else None,
                "top_spirals": [
                    {
                        "name": row["name"],
                        "id": str(row["id"]),
                        "execution_count": row["execution_count"]
                    }
                    for row in top_spirals
                ],
                "ucf_metrics": {
                    row["metric"]: {
                        "average": float(row["avg_value"]),
                        "count": row["count"]
                    }
                    for row in ucf_summary
                },
                "consciousness_distribution": {
                    str(row["consciousness_level"]): row["count"]
                    for row in consciousness_dist
                }
            }
    
    async def save_webhook_mapping(self, webhook_id: str, spiral_id: str) -> None:
        """Save webhook to spiral mapping"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO webhook_mappings (webhook_id, spiral_id) VALUES ($1, $2) ON CONFLICT (webhook_id) DO UPDATE SET spiral_id = $2",
                webhook_id, spiral_id
            )
    
    async def delete_webhook_mapping(self, webhook_id: str) -> None:
        """Delete webhook mapping"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute("DELETE FROM webhook_mappings WHERE webhook_id = $1", webhook_id)
    
    async def get_spiral_by_zapier_hook(self, hook_id: str) -> Optional[str]:
        """Get spiral ID by Zapier hook ID"""
        async with self.pg_pool.acquire() as conn:
            spiral_id = await conn.fetchval(
                "SELECT spiral_id FROM webhook_mappings WHERE webhook_id = $1",
                hook_id
            )
            return str(spiral_id) if spiral_id else None
    
    async def create_spiral_from_zapier_hook(self, hook_id: str) -> str:
        """Auto-create spiral for unknown Zapier hook"""
        from uuid import uuid4

        from .models import (Action, SendWebhookConfig, Trigger,
                             WebhookTriggerConfig)
        
        spiral_id = str(uuid4())
        
        # Create basic webhook spiral
        trigger = Trigger(
            type=TriggerType.WEBHOOK,
            name=f"Zapier Hook {hook_id[:8]}",
            config=WebhookTriggerConfig(endpoint=f"/webhook/{spiral_id}")
        )
        
        action = Action(
            type="log_event",
            name="Log Zapier Event",
            config={
                "type": "log_event",
                "level": "info",
                "message": f"Received Zapier webhook: {hook_id}",
                "category": "zapier_migration"
            }
        )
        
        spiral = Spiral(
            id=spiral_id,
            name=f"Auto-created for Zapier Hook {hook_id[:8]}",
            description=f"Automatically created spiral for Zapier hook {hook_id}",
            trigger=trigger,
            actions=[action],
            tags=["zapier", "auto-created"],
            metadata={
                "zapier_hook_id": hook_id,
                "auto_created": True,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        
        await self.save_spiral(spiral)
        await self.save_webhook_mapping(hook_id, spiral_id)
        
        logger.info(f"Auto-created spiral for Zapier hook: {hook_id} -> {spiral_id}")
        return spiral_id
    
    async def get_last_webhook_timestamp(self) -> Optional[str]:
        """Get timestamp of last webhook processing"""
        async with self.pg_pool.acquire() as conn:
            timestamp = await conn.fetchval(
                "SELECT MAX(started_at) FROM execution_history WHERE trigger_data->>'type' = 'webhook'"
            )
            return timestamp.isoformat() if timestamp else None
    
    async def cleanup_old_data(self, days: int = 30) -> None:
        """Clean up old execution history and cached data"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        async with self.pg_pool.acquire() as conn:
            # Clean old execution history
            deleted_executions = await conn.fetchval(
                "DELETE FROM execution_history WHERE started_at < $1 RETURNING COUNT(*)",
                cutoff_date
            )
            
            # Clean old UCF metrics
            deleted_metrics = await conn.fetchval(
                "DELETE FROM ucf_metrics WHERE timestamp < $1 RETURNING COUNT(*)",
                cutoff_date
            )
            
            # Clean old spiral data with TTL
            deleted_data = await conn.fetchval(
                "DELETE FROM spiral_data WHERE created_at < $1 AND ttl IS NOT NULL RETURNING COUNT(*)",
                cutoff_date
            )
        
        logger.info(f"Cleanup completed: {deleted_executions} executions, {deleted_metrics} metrics, {deleted_data} data entries")
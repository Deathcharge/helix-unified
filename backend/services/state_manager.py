# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/services/state_manager.py — Redis + PostgreSQL State Manager
# Author: Andrew John Ward (Architect)

import redis.asyncio as redis
import json
import asyncpg
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# ============================================================================
# STATE MANAGER
# ============================================================================

class StateManager:
    """Manages UCF state with Redis caching and PostgreSQL persistence."""
    
    def __init__(self, redis_url: str = None, db_url: str = None):
        self.redis_url = redis_url or "redis://localhost:6379"
        self.db_url = db_url
        self.redis = None
        self.db_pool = None
    
    async def connect(self):
        """Initialize Redis and PostgreSQL connections."""
        try:
            self.redis = await redis.from_url(self.redis_url, decode_responses=True)
            print(f"✅ Redis connected: {self.redis_url}")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            self.redis = None
        
        if self.db_url:
            try:
                self.db_pool = await asyncpg.create_pool(self.db_url)
                print("✅ PostgreSQL connected")
            except Exception as e:
                print(f"⚠ PostgreSQL connection failed: {e}")
                self.db_pool = None
    
    async def disconnect(self):
        """Close connections."""
        if self.redis:
            await self.redis.close()
        if self.db_pool:
            await self.db_pool.close()
    
    # ========================================================================
    # UCF STATE OPERATIONS
    # ========================================================================
    
    async def set_ucf_state(self, state: Dict[str, Any], ttl: int = 3600):
        """Cache UCF state in Redis with TTL."""
        if not self.redis:
            return False
        
        try:
            await self.redis.setex(
                'ucf:current',
                ttl,
                json.dumps(state)
            )
            
            # Also persist to file as fallback
            state_path = Path("Helix/state/ucf_state.json")
            state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(state_path, "w") as f:
                json.dump(state, f, indent=2)
            
            return True
        except Exception as e:
            print(f"⚠ Error setting UCF state: {e}")
            return False
    
    async def get_ucf_state(self) -> Dict[str, Any]:
        """Retrieve cached UCF state from Redis or file."""
        # Try Redis first
        if self.redis:
            try:
                data = await self.redis.get('ucf:current')
                if data:
                    return json.loads(data)
            except Exception as e:
                print(f"⚠ Redis get error: {e}")
        
        # Fall back to file
        state_path = Path("Helix/state/ucf_state.json")
        if state_path.exists():
            try:
                with open(state_path) as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Return default
        return {
            "zoom": 1.0228,
            "harmony": 0.355,
            "resilience": 1.1191,
            "prana": 0.5175,
            "drishti": 0.5023,
            "klesha": 0.010
        }
    
    async def publish_ucf_update(self, metrics: Dict[str, Any]):
        """Broadcast UCF updates to all subscribers."""
        if not self.redis:
            return False
        
        try:
            await self.redis.publish('ucf_updates', json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": metrics
            }))
            return True
        except Exception as e:
            print(f"⚠ Error publishing UCF update: {e}")
            return False
    
    async def subscribe_ucf_events(self):
        """Subscribe to UCF update events."""
        if not self.redis:
            return None
        
        try:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe('ucf_updates')
            return pubsub
        except Exception as e:
            print(f"⚠ Error subscribing to UCF events: {e}")
            return None
    
    # ========================================================================
    # DIRECTIVE OPERATIONS
    # ========================================================================
    
    async def queue_directive(self, directive: Dict[str, Any]):
        """Queue a directive for Manus execution."""
        if not self.redis:
            return False
        
        try:
            directive_id = directive.get("directive_id", "unknown")
            await self.redis.lpush('manus:directives', json.dumps(directive))
            await self.redis.setex(f'directive:{directive_id}', 3600, json.dumps({
                "status": "queued",
                "timestamp": datetime.utcnow().isoformat()
            }))
            return True
        except Exception as e:
            print(f"⚠ Error queuing directive: {e}")
            return False
    
    async def get_next_directive(self) -> Optional[Dict[str, Any]]:
        """Get next directive from queue."""
        if not self.redis:
            return None
        
        try:
            data = await self.redis.rpop('manus:directives')
            return json.loads(data) if data else None
        except Exception as e:
            print(f"⚠ Error getting directive: {e}")
            return None
    
    async def update_directive_status(self, directive_id: str, status: str, result: Dict[str, Any] = None):
        """Update directive execution status."""
        if not self.redis:
            return False
        
        try:
            status_data = {
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "result": result or {}
            }
            await self.redis.setex(f'directive:{directive_id}', 3600, json.dumps(status_data))
            return True
        except Exception as e:
            print(f"⚠ Error updating directive status: {e}")
            return False
    
    # ========================================================================
    # MEMORY & LOGGING
    # ========================================================================
    
    async def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log event to Redis stream."""
        if not self.redis:
            return False
        
        try:
            await self.redis.xadd('helix:events', {
                'type': event_type,
                'data': json.dumps(data),
                'timestamp': datetime.utcnow().isoformat()
            })
            return True
        except Exception as e:
            print(f"⚠ Error logging event: {e}")
            return False
    
    async def get_recent_events(self, count: int = 20) -> list:
        """Get recent events from Redis stream."""
        if not self.redis:
            return []
        
        try:
            events = await self.redis.xrevrange('helix:events', count=count)
            return events
        except Exception as e:
            print(f"⚠ Error getting events: {e}")
            return []
    
    # ========================================================================
    # AGENT MEMORY
    # ========================================================================
    
    async def save_agent_memory(self, agent_name: str, memory: list):
        """Save agent memory to Redis."""
        if not self.redis:
            return False
        
        try:
            await self.redis.setex(
                f'agent:{agent_name}:memory',
                86400,  # 24 hour TTL
                json.dumps(memory)
            )
            return True
        except Exception as e:
            print(f"⚠ Error saving agent memory: {e}")
            return False
    
    async def get_agent_memory(self, agent_name: str) -> list:
        """Retrieve agent memory from Redis."""
        if not self.redis:
            return []
        
        try:
            data = await self.redis.get(f'agent:{agent_name}:memory')
            return json.loads(data) if data else []
        except Exception as e:
            print(f"⚠ Error getting agent memory: {e}")
            return []
    
    # ========================================================================
    # HEALTH CHECK
    # ========================================================================
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of state manager."""
        health = {
            "timestamp": datetime.utcnow().isoformat(),
            "redis": False,
            "postgres": False
        }
        
        if self.redis:
            try:
                await self.redis.ping()
                health["redis"] = True
            except Exception:
                health["redis"] = False
        
        if self.db_pool:
            try:
                async with self.db_pool.acquire() as conn:
                    await conn.fetchval('SELECT 1')
                health["postgres"] = True
            except Exception:
                health["postgres"] = False
        
        return health

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_state_manager = None

async def get_state_manager(redis_url: str = None, db_url: str = None) -> StateManager:
    """Get or create state manager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager(redis_url, db_url)
        await _state_manager.connect()
    return _state_manager

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def main():
        manager = await get_state_manager()
        
        # Test operations
        test_state = {
            "zoom": 1.0228,
            "harmony": 0.355,
            "resilience": 1.1191,
            "prana": 0.5175,
            "drishti": 0.5023,
            "klesha": 0.010
        }
        
        print("Testing StateManager...")
        await manager.set_ucf_state(test_state)
        print("✅ State set")
        
        retrieved = await manager.get_ucf_state()
        print(f"✅ State retrieved: {retrieved}")
        
        health = await manager.health_check()
        print(f"✅ Health check: {health}")
        
        await manager.disconnect()
    
    asyncio.run(main())


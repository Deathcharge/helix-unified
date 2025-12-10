"""
Batches 6-10: Multi-Workspace, Collaboration, Automation, Admin, Security
"""

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# ============================================================================
# BATCH 6: Multi-Workspace System
# ============================================================================

@dataclass
class Workspace:
    id: str
    name: str
    description: str
    owner_id: str
    created_at: datetime
    settings: Dict[str, Any] = field(default_factory=dict)
    members: Set[str] = field(default_factory=set)
    state: Dict[str, Any] = field(default_factory=dict)

class WorkspaceManager:
    """Manage multi-workspace system"""
    
    def __init__(self):
        self.workspaces: Dict[str, Workspace] = {}
    
    async def create_workspace(self, name: str, owner_id: str, description: str = "") -> Workspace:
        """Create new workspace"""
        ws_id = f"ws_{hashlib.md5(f'{name}{owner_id}{datetime.now().isoformat()}'.encode()).hexdigest()[:12]}"
        workspace = Workspace(
            id=ws_id,
            name=name,
            description=description,
            owner_id=owner_id,
            created_at=datetime.now()
        )
        self.workspaces[ws_id] = workspace
        logger.info(f"Created workspace {ws_id}")
        return workspace
    
    async def list_workspaces(self, user_id: str) -> List[Workspace]:
        """List user's workspaces"""
        return [ws for ws in self.workspaces.values() 
                if ws.owner_id == user_id or user_id in ws.members]
    
    async def get_workspace(self, ws_id: str) -> Optional[Workspace]:
        """Get workspace details"""
        return self.workspaces.get(ws_id)
    
    async def update_workspace(self, ws_id: str, **kwargs) -> bool:
        """Update workspace"""
        if ws_id not in self.workspaces:
            return False
        ws = self.workspaces[ws_id]
        for key, value in kwargs.items():
            if hasattr(ws, key):
                setattr(ws, key, value)
        return True
    
    async def delete_workspace(self, ws_id: str) -> bool:
        """Delete workspace"""
        if ws_id in self.workspaces:
            del self.workspaces[ws_id]
            logger.info(f"Deleted workspace {ws_id}")
            return True
        return False
    
    async def save_workspace_state(self, ws_id: str, state: Dict) -> bool:
        """Save workspace state"""
        if ws_id in self.workspaces:
            self.workspaces[ws_id].state = state
            return True
        return False

# ============================================================================
# BATCH 7: Real-Time Collaboration
# ============================================================================

@dataclass
class UserPresence:
    user_id: str
    workspace_id: str
    last_activity: datetime
    cursor_position: Optional[Dict] = None

class CollaborationEngine:
    """Handle real-time collaboration"""
    
    def __init__(self):
        self.active_users: Dict[str, UserPresence] = {}
        self.activity_log: List[Dict] = []
    
    async def track_user_presence(self, user_id: str, workspace_id: str) -> bool:
        """Track user presence"""
        self.active_users[user_id] = UserPresence(
            user_id=user_id,
            workspace_id=workspace_id,
            last_activity=datetime.now()
        )
        return True
    
    async def broadcast_activity(self, workspace_id: str, activity: Dict) -> bool:
        """Broadcast activity to all users"""
        activity["timestamp"] = datetime.now().isoformat()
        activity["workspace_id"] = workspace_id
        self.activity_log.append(activity)
        logger.info(f"Broadcasted activity in {workspace_id}")
        return True
    
    async def get_active_users(self, workspace_id: str) -> List[str]:
        """Get active users in workspace"""
        return [u.user_id for u in self.active_users.values() 
                if u.workspace_id == workspace_id]
    
    async def get_activity_feed(self, workspace_id: str, limit: int = 50) -> List[Dict]:
        """Get activity feed"""
        return [a for a in self.activity_log if a.get("workspace_id") == workspace_id][-limit:]

# ============================================================================
# BATCH 8: Advanced Automation (Spirals Engine)
# ============================================================================

@dataclass
class Spiral:
    id: str
    name: str
    triggers: List[Dict]
    actions: List[Dict]
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    execution_history: List[Dict] = field(default_factory=list)

class SpiralsEngine:
    """Manage automation spirals"""
    
    def __init__(self):
        self.spirals: Dict[str, Spiral] = {}
    
    async def create_spiral(self, name: str, triggers: List[Dict], actions: List[Dict]) -> Spiral:
        """Create automation spiral"""
        spiral_id = f"spiral_{hashlib.md5(f'{name}{datetime.now().isoformat()}'.encode()).hexdigest()[:12]}"
        spiral = Spiral(
            id=spiral_id,
            name=name,
            triggers=triggers,
            actions=actions
        )
        self.spirals[spiral_id] = spiral
        logger.info(f"Created spiral {spiral_id}")
        return spiral
    
    async def list_spirals(self) -> List[Spiral]:
        """List all spirals"""
        return list(self.spirals.values())
    
    async def execute_spiral(self, spiral_id: str) -> Dict:
        """Execute spiral"""
        if spiral_id not in self.spirals:
            return {"success": False, "error": "Spiral not found"}
        
        spiral = self.spirals[spiral_id]
        execution = {
            "spiral_id": spiral_id,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        spiral.execution_history.append(execution)
        logger.info(f"Executed spiral {spiral_id}")
        return {"success": True, "execution": execution}
    
    async def get_spiral_history(self, spiral_id: str) -> List[Dict]:
        """Get spiral execution history"""
        if spiral_id in self.spirals:
            return self.spirals[spiral_id].execution_history
        return []

# ============================================================================
# BATCH 9: System Administration
# ============================================================================

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@dataclass
class User:
    id: str
    email: str
    role: Role
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

class AdminSystem:
    """System administration"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.audit_log: List[Dict] = []
        self.config: Dict[str, Any] = {
            "version": "18.0",
            "max_users": 1000,
            "max_workspaces_per_user": 50,
            "rate_limit": 1000
        }
    
    async def create_user(self, email: str, role: str = "user") -> User:
        """Create user"""
        user_id = f"user_{hashlib.md5(email.encode()).hexdigest()[:12]}"
        user = User(id=user_id, email=email, role=Role(role))
        self.users[user_id] = user
        self._log_audit("user_created", {"user_id": user_id, "email": email})
        return user
    
    async def list_users(self) -> List[User]:
        """List all users"""
        return list(self.users.values())
    
    async def update_user_role(self, user_id: str, role: str) -> bool:
        """Update user role"""
        if user_id in self.users:
            self.users[user_id].role = Role(role)
            self._log_audit("role_updated", {"user_id": user_id, "new_role": role})
            return True
        return False
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        if user_id in self.users:
            del self.users[user_id]
            self._log_audit("user_deleted", {"user_id": user_id})
            return True
        return False
    
    async def get_audit_logs(self, limit: int = 100) -> List[Dict]:
        """Get audit logs"""
        return self.audit_log[-limit:]
    
    async def get_system_config(self) -> Dict:
        """Get system configuration"""
        return self.config
    
    def _log_audit(self, action: str, details: Dict):
        """Log audit event"""
        self.audit_log.append({
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

# ============================================================================
# BATCH 10: Security & Compliance
# ============================================================================

class SecurityManager:
    """Security and compliance management"""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, int] = {}
        self.blocked_ips: Set[str] = set()
    
    async def generate_api_key(self, user_id: str) -> str:
        """Generate API key"""
        key = hashlib.sha256(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
        self.api_keys[key] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        logger.info(f"Generated API key for {user_id}")
        return key
    
    async def validate_api_key(self, key: str) -> Optional[str]:
        """Validate API key and return user_id"""
        if key in self.api_keys and self.api_keys[key]["active"]:
            return self.api_keys[key]["user_id"]
        return None
    
    async def check_rate_limit(self, user_id: str, limit: int = 1000) -> bool:
        """Check rate limit"""
        current = self.rate_limits.get(user_id, 0)
        if current >= limit:
            return False
        self.rate_limits[user_id] = current + 1
        return True
    
    async def block_ip(self, ip: str) -> bool:
        """Block IP address"""
        self.blocked_ips.add(ip)
        logger.warning(f"Blocked IP: {ip}")
        return True
    
    async def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips

# Global instances
workspace_manager = WorkspaceManager()
collaboration_engine = CollaborationEngine()
spirals_engine = SpiralsEngine()
admin_system = AdminSystem()
security_manager = SecurityManager()

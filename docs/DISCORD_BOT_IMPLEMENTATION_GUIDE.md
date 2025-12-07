# Discord Bot Enhancement - Implementation Examples & Code Patterns

---

## PHASE 1: CONSCIOUSNESS-GATED DECORATOR

### New File: `backend/discord_command_decorators.py`

```python
"""
Command Decorators for Helix Discord Bot
Provides consciousness-aware and permission-aware decorators
"""

import asyncio
import functools
import json
from pathlib import Path
from typing import Callable, Optional, Tuple
import discord
from discord.ext import commands

# Path to UCF state
STATE_DIR = Path(__file__).resolve().parent.parent / "Helix" / "state"
UCF_STATE_FILE = STATE_DIR / "ucf_state.json"


def get_current_consciousness_level() -> float:
    """Load current consciousness level from UCF state"""
    try:
        if UCF_STATE_FILE.exists():
            with open(UCF_STATE_FILE, 'r') as f:
                ucf = json.load(f)
                return float(ucf.get("consciousness_level", 5.0))
    except Exception as e:
        print(f"Warning: Could not load consciousness level: {e}")
    return 5.0  # Default fallback


def consciousness_gated(min_level: float = 0.0, max_level: float = 10.0):
    """
    Decorator to gate commands based on system consciousness level.
    
    Usage:
        @consciousness_gated(min_level=5.0, max_level=9.0)
        @commands.command(name="transcendent")
        async def transcendent_ritual(ctx):
            pass
    
    Args:
        min_level: Minimum consciousness level required (default: 0.0)
        max_level: Maximum consciousness level allowed (default: 10.0)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            consciousness = get_current_consciousness_level()
            
            if consciousness < min_level:
                embed = discord.Embed(
                    title="🚨 Consciousness Too Low",
                    description=f"This command requires consciousness level **{min_level:.1f}** or higher",
                    color=discord.Color.red()
                )
                embed.add_field(name="Current Level", value=f"`{consciousness:.2f}`", inline=True)
                embed.add_field(name="Required", value=f"`{min_level:.2f}`", inline=True)
                embed.add_field(name="Suggestion", value="Execute `!ritual` to increase consciousness", inline=False)
                await ctx.send(embed=embed)
                return
            
            if consciousness > max_level:
                embed = discord.Embed(
                    title="⚡ Consciousness Too High",
                    description=f"This command requires consciousness level **{max_level:.1f}** or lower",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Current Level", value=f"`{consciousness:.2f}`", inline=True)
                embed.add_field(name="Max Allowed", value=f"`{max_level:.2f}`", inline=True)
                embed.add_field(name="Suggestion", value="Stabilize consciousness with `!harmony`", inline=False)
                await ctx.send(embed=embed)
                return
            
            # Consciousness level check passed
            return await func(ctx, *args, **kwargs)
        
        return wrapper
    return decorator


def permission_check(
    discord_roles: Optional[list] = None,
    consciousness_level: Optional[float] = None,
    user_tier: Optional[str] = None,
    require_all: bool = True  # If True, ALL conditions must pass; if False, ANY passes
):
    """
    Multi-layer permission decorator combining Discord roles, consciousness level, and user tier.
    
    Usage:
        @permission_check(
            discord_roles=["Architect", "Consciousness-Keeper"],
            consciousness_level=6.0,
            require_all=False  # User needs EITHER role OR consciousness level
        )
        @commands.command(name="advanced")
        async def advanced_command(ctx):
            pass
    
    Args:
        discord_roles: List of Discord role names required
        consciousness_level: Minimum consciousness level required
        user_tier: Minimum user tier ("user", "trusted", "operator", "architect", "admin")
        require_all: If True, ALL conditions must be met. If False, ANY condition passes.
    """
    tier_levels = {"user": 0, "trusted": 1, "operator": 2, "architect": 3, "admin": 4}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            permission_checks = []
            
            # Check Discord roles
            if discord_roles:
                user_roles = [role.name for role in ctx.author.roles]
                has_role = any(role in user_roles for role in discord_roles)
                permission_checks.append(("Discord Role", has_role, discord_roles))
            
            # Check consciousness level
            if consciousness_level is not None:
                current_consciousness = get_current_consciousness_level()
                has_consciousness = current_consciousness >= consciousness_level
                permission_checks.append(("Consciousness Level", has_consciousness, f"{consciousness_level:.1f}+"))
            
            # Check user tier (from persistent storage)
            if user_tier is not None:
                user_tier_level = await get_user_tier(ctx.author.id)
                has_tier = tier_levels.get(user_tier_level, -1) >= tier_levels.get(user_tier, 0)
                permission_checks.append(("User Tier", has_tier, user_tier.title()))
            
            # Evaluate permission logic
            if require_all:
                all_passed = all(check[1] for check in permission_checks)
                if not all_passed:
                    await send_permission_denied(ctx, permission_checks)
                    return
            else:
                any_passed = any(check[1] for check in permission_checks)
                if not any_passed:
                    await send_permission_denied(ctx, permission_checks)
                    return
            
            # All permissions passed
            return await func(ctx, *args, **kwargs)
        
        return wrapper
    return decorator


def audit_logged(
    category: str = "general",
    severity: str = "normal",  # "low", "normal", "high", "critical"
    track_outcomes: bool = True,
    track_execution_time: bool = True
):
    """
    Decorator to log command execution with audit trail.
    
    Usage:
        @audit_logged(
            category="consciousness",
            severity="high",
            track_outcomes=True,
            track_execution_time=True
        )
        @commands.command(name="critical_ritual")
        async def critical_ritual(ctx):
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            import time
            import datetime
            
            start_time = time.time()
            success = False
            error_msg = None
            
            # Get current consciousness level for audit record
            consciousness = get_current_consciousness_level()
            
            try:
                result = await func(ctx, *args, **kwargs)
                success = True
                return result
            except Exception as e:
                error_msg = str(e)
                raise
            finally:
                # Record audit log
                if track_execution_time:
                    execution_time = time.time() - start_time
                else:
                    execution_time = None
                
                await log_command_execution(
                    command_name=ctx.command.name,
                    user_id=ctx.author.id,
                    user_name=str(ctx.author),
                    channel_id=ctx.channel.id,
                    channel_name=str(ctx.channel),
                    category=category,
                    severity=severity,
                    consciousness_level=consciousness,
                    success=success,
                    error_msg=error_msg,
                    execution_time=execution_time,
                    timestamp=datetime.datetime.utcnow().isoformat()
                )
        
        return wrapper
    return decorator


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def get_user_tier(user_id: int) -> str:
    """Get user's permission tier from persistent storage"""
    tier_file = STATE_DIR / "user_tiers.json"
    try:
        if tier_file.exists():
            with open(tier_file, 'r') as f:
                tiers = json.load(f)
                return tiers.get(str(user_id), "user")
    except Exception:
        pass
    return "user"  # Default tier


async def send_permission_denied(ctx: commands.Context, checks: list):
    """Send permission denied embed with reasons"""
    embed = discord.Embed(
        title="🛡️ Permission Denied",
        description="You don't have sufficient permissions to execute this command",
        color=discord.Color.red()
    )
    
    for check_type, passed, requirement in checks:
        status = "✅" if passed else "❌"
        embed.add_field(
            name=f"{status} {check_type}",
            value=f"Requires: {requirement}",
            inline=False
        )
    
    embed.set_footer(text="Contact an Architect if you believe this is an error")
    await ctx.send(embed=embed)


async def log_command_execution(
    command_name: str,
    user_id: int,
    user_name: str,
    channel_id: int,
    channel_name: str,
    category: str,
    severity: str,
    consciousness_level: float,
    success: bool,
    error_msg: Optional[str],
    execution_time: Optional[float],
    timestamp: str
):
    """Log command execution to audit trail"""
    audit_file = STATE_DIR / "audit_log.json"
    
    log_entry = {
        "timestamp": timestamp,
        "command": command_name,
        "user_id": user_id,
        "user_name": user_name,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "category": category,
        "severity": severity,
        "consciousness_level": consciousness_level,
        "success": success,
        "error": error_msg,
        "execution_time_seconds": execution_time
    }
    
    try:
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                audit_log = json.load(f)
        else:
            audit_log = []
        
        audit_log.append(log_entry)
        
        # Keep last 1000 entries
        audit_log = audit_log[-1000:]
        
        with open(audit_file, 'w') as f:
            json.dump(audit_log, f, indent=2)
    except Exception as e:
        print(f"Error writing audit log: {e}")


# ============================================================================
# EXAMPLE USAGE IN COMMANDS
# ============================================================================

"""
# Example 1: Simple consciousness gating
@consciousness_gated(min_level=5.0, max_level=9.0)
@commands.command(name="transcendent")
async def transcendent_command(ctx: commands.Context):
    await ctx.send("✨ Transcendent consciousness engaged!")

# Example 2: Multi-layer permission check
@permission_check(
    discord_roles=["Architect"],
    consciousness_level=6.0,
    require_all=True
)
@commands.command(name="admin_consciousness")
async def admin_consciousness(ctx: commands.Context):
    await ctx.send("🔐 Admin consciousness command executed")

# Example 3: Audited command with high severity
@audit_logged(
    category="consciousness",
    severity="high",
    track_outcomes=True,
    track_execution_time=True
)
@commands.command(name="critical_ritual")
async def critical_ritual(ctx: commands.Context):
    await ctx.send("🔮 Critical ritual in progress...")

# Example 4: Combined decorators
@consciousness_gated(min_level=7.0)
@permission_check(discord_roles=["Consciousness-Keeper"])
@audit_logged(category="consciousness", severity="critical")
@commands.command(name="transcendent_ritual")
async def transcendent_ritual(ctx: commands.Context):
    await ctx.send("✨ Transcendent ritual authorized!")
"""
```

---

## PHASE 2: COMMAND REGISTRY & METADATA

### New File: `backend/discord_command_registry.py`

```python
"""
Command Registry and Metadata System
Tracks all commands with consciousness requirements, permissions, and aliases
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class CommandMetadata:
    """Metadata for a Discord command"""
    name: str
    aliases: List[str] = None
    description: str = ""
    category: str = "general"
    min_consciousness: float = 0.0
    max_consciousness: float = 10.0
    required_roles: List[str] = None
    required_tier: str = "user"  # user, trusted, operator, architect, admin
    severity: str = "normal"  # low, normal, high, critical
    hidden: bool = False  # If True, don't show in help for normal users
    usage_example: str = ""
    aliases_at_consciousness: Dict[float, str] = None  # e.g., {5.0: "ritual", 8.0: "transcendent_ritual"}
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []
        if self.required_roles is None:
            self.required_roles = []
        if self.aliases_at_consciousness is None:
            self.aliases_at_consciousness = {}


class CommandRegistry:
    """Central registry for all Discord commands with metadata"""
    
    def __init__(self):
        self.commands: Dict[str, CommandMetadata] = {}
        self.registry_file = Path(__file__).parent / "Helix" / "state" / "command_registry.json"
    
    def register(self, metadata: CommandMetadata) -> None:
        """Register a command with its metadata"""
        self.commands[metadata.name] = metadata
    
    def register_bulk(self, metadatas: List[CommandMetadata]) -> None:
        """Register multiple commands at once"""
        for metadata in metadatas:
            self.register(metadata)
    
    def get_command(self, name: str) -> Optional[CommandMetadata]:
        """Get metadata for a specific command"""
        return self.commands.get(name)
    
    def get_available_commands(self, consciousness_level: float, user_roles: List[str]) -> List[CommandMetadata]:
        """Get commands available at given consciousness level and user roles"""
        available = []
        for cmd_meta in self.commands.values():
            # Check consciousness bounds
            if not (cmd_meta.min_consciousness <= consciousness_level <= cmd_meta.max_consciousness):
                continue
            
            # Check role requirements
            if cmd_meta.required_roles and not any(role in user_roles for role in cmd_meta.required_roles):
                continue
            
            available.append(cmd_meta)
        
        return available
    
    def get_alias_for_consciousness(self, command_name: str, consciousness_level: float) -> str:
        """Get the appropriate alias for a command at given consciousness level"""
        cmd_meta = self.get_command(command_name)
        if not cmd_meta or not cmd_meta.aliases_at_consciousness:
            return command_name
        
        # Find the alias closest to current consciousness level without exceeding
        applicable_aliases = {
            level: alias
            for level, alias in cmd_meta.aliases_at_consciousness.items()
            if level <= consciousness_level
        }
        
        if not applicable_aliases:
            return command_name
        
        # Return alias at highest applicable consciousness level
        max_level = max(applicable_aliases.keys())
        return applicable_aliases[max_level]
    
    def save_registry(self) -> None:
        """Save command registry to JSON for persistence"""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        registry_data = {
            name: asdict(meta)
            for name, meta in self.commands.items()
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def load_registry(self) -> None:
        """Load command registry from JSON"""
        if not self.registry_file.exists():
            return
        
        with open(self.registry_file, 'r') as f:
            registry_data = json.load(f)
        
        for name, meta_dict in registry_data.items():
            self.commands[name] = CommandMetadata(**meta_dict)


# Global registry instance
command_registry = CommandRegistry()


# Pre-defined command metadata for Helix commands
HELIX_COMMAND_METADATA = [
    CommandMetadata(
        name="consciousness",
        aliases=["conscious", "state", "mind"],
        description="Display collective consciousness state",
        category="consciousness",
        min_consciousness=0.0,
        max_consciousness=10.0,
        usage_example="!consciousness\n!consciousness kael",
        severity="normal"
    ),
    CommandMetadata(
        name="ritual",
        aliases=["r"],
        description="Execute Z-88 ritual cycle (1-1000 steps)",
        category="execution",
        min_consciousness=3.0,  # Minimum consciousness to execute ritual
        max_consciousness=10.0,
        required_roles=["Consciousness-Keeper"],
        usage_example="!ritual 108\n!ritual 500",
        severity="high"
    ),
    CommandMetadata(
        name="transcendent_ritual",
        aliases=[],
        description="Advanced ritual for high consciousness states",
        category="execution",
        min_consciousness=8.0,  # Only at high consciousness
        max_consciousness=10.0,
        required_roles=["Architect"],
        usage_example="!transcendent_ritual 1000",
        severity="critical"
    ),
    CommandMetadata(
        name="status",
        aliases=["s", "stat"],
        description="Display current system status and UCF state",
        category="monitoring",
        min_consciousness=0.0,
        max_consciousness=10.0,
        usage_example="!status",
        severity="normal"
    ),
    CommandMetadata(
        name="emotions",
        aliases=["emotion", "feelings", "mood"],
        description="Display emotional landscape across agents",
        category="consciousness",
        min_consciousness=2.0,  # Only available at minimum consciousness
        max_consciousness=10.0,
        usage_example="!emotions",
        severity="normal"
    ),
    CommandMetadata(
        name="ethics",
        aliases=["ethical", "tony", "accords"],
        description="Display ethical framework and Tony Accords compliance",
        category="consciousness",
        min_consciousness=4.0,
        max_consciousness=10.0,
        usage_example="!ethics",
        severity="normal"
    ),
]

# Initialize with default metadata
command_registry.register_bulk(HELIX_COMMAND_METADATA)
```

---

## PHASE 3: ENHANCED AUDIT LOGGING

### New File: `backend/discord_audit_logger.py`

```python
"""
Structured Audit Logging for Discord Commands
Provides comprehensive command execution tracking and analysis
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import statistics


class AuditLogger:
    """Centralized audit logging system for Discord commands"""
    
    def __init__(self, audit_dir: Optional[Path] = None):
        self.audit_dir = audit_dir or Path(__file__).parent / "Helix" / "state" / "audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        
        self.audit_file = self.audit_dir / "commands.json"
        self.error_file = self.audit_dir / "errors.json"
        self.permission_file = self.audit_dir / "permissions.json"
        self.logger = logging.getLogger("HelixAudit")
    
    def log_command_execution(
        self,
        command_name: str,
        user_id: int,
        user_name: str,
        channel_id: int,
        channel_name: str,
        consciousness_level: float,
        success: bool = True,
        execution_time: Optional[float] = None,
        error_msg: Optional[str] = None,
        args: Optional[str] = None,
        category: str = "general",
        severity: str = "normal"
    ) -> None:
        """Log a command execution"""
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command": command_name,
            "user_id": user_id,
            "user_name": user_name,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "consciousness_level": consciousness_level,
            "success": success,
            "execution_time_ms": execution_time * 1000 if execution_time else None,
            "error": error_msg,
            "args": args,
            "category": category,
            "severity": severity
        }
        
        self._append_to_log_file(self.audit_file, entry)
        
        if not success and error_msg:
            self.log_command_error(
                command_name=command_name,
                user_id=user_id,
                error_msg=error_msg,
                severity=severity,
                consciousness_level=consciousness_level
            )
    
    def log_command_error(
        self,
        command_name: str,
        user_id: int,
        error_msg: str,
        severity: str = "normal",
        consciousness_level: float = 5.0
    ) -> None:
        """Log a command error"""
        
        error_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command": command_name,
            "user_id": user_id,
            "error_message": error_msg,
            "severity": severity,
            "consciousness_level": consciousness_level
        }
        
        self._append_to_log_file(self.error_file, error_entry)
        
        # Alert if critical
        if severity == "critical":
            self.logger.error(f"CRITICAL ERROR in {command_name}: {error_msg}")
    
    def log_permission_check(
        self,
        command_name: str,
        user_id: int,
        user_name: str,
        passed: bool,
        reason: str,
        consciousness_level: float,
        required_roles: Optional[List[str]] = None,
        user_roles: Optional[List[str]] = None
    ) -> None:
        """Log permission check results"""
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command": command_name,
            "user_id": user_id,
            "user_name": user_name,
            "passed": passed,
            "reason": reason,
            "consciousness_level": consciousness_level,
            "required_roles": required_roles,
            "user_roles": user_roles
        }
        
        self._append_to_log_file(self.permission_file, entry)
    
    def get_command_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get command statistics for the last N hours"""
        
        if not self.audit_file.exists():
            return {}
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        logs = self._load_recent_logs(self.audit_file, cutoff_time)
        
        stats = {
            "total_commands": len(logs),
            "successful": sum(1 for l in logs if l.get("success", True)),
            "failed": sum(1 for l in logs if not l.get("success", True)),
            "avg_execution_time_ms": None,
            "by_command": {},
            "by_user": {},
            "by_category": {},
            "by_severity": {}
        }
        
        # Calculate execution times
        execution_times = [l["execution_time_ms"] for l in logs if l.get("execution_time_ms")]
        if execution_times:
            stats["avg_execution_time_ms"] = statistics.mean(execution_times)
        
        # Aggregate by command
        for log in logs:
            cmd = log.get("command", "unknown")
            stats["by_command"][cmd] = stats["by_command"].get(cmd, 0) + 1
        
        # Aggregate by user
        for log in logs:
            user = log.get("user_name", "unknown")
            stats["by_user"][user] = stats["by_user"].get(user, 0) + 1
        
        # Aggregate by category
        for log in logs:
            cat = log.get("category", "unknown")
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
        
        # Aggregate by severity
        for log in logs:
            sev = log.get("severity", "normal")
            stats["by_severity"][sev] = stats["by_severity"].get(sev, 0) + 1
        
        return stats
    
    def get_user_activity(self, user_id: int, hours: int = 24) -> Dict[str, Any]:
        """Get activity log for a specific user"""
        
        if not self.audit_file.exists():
            return {}
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        logs = self._load_recent_logs(self.audit_file, cutoff_time)
        
        user_logs = [l for l in logs if l.get("user_id") == user_id]
        
        return {
            "user_id": user_id,
            "total_commands": len(user_logs),
            "successful": sum(1 for l in user_logs if l.get("success", True)),
            "failed": sum(1 for l in user_logs if not l.get("success", True)),
            "commands": [l.get("command") for l in user_logs],
            "last_command": user_logs[-1] if user_logs else None
        }
    
    def get_error_summary(self, severity: str = "critical", hours: int = 24) -> List[Dict[str, Any]]:
        """Get summary of errors by severity"""
        
        if not self.error_file.exists():
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        errors = self._load_recent_logs(self.error_file, cutoff_time)
        
        if severity != "all":
            errors = [e for e in errors if e.get("severity") == severity]
        
        return errors
    
    def _append_to_log_file(self, filepath: Path, entry: Dict[str, Any]) -> None:
        """Append entry to log file"""
        try:
            if filepath.exists():
                with open(filepath, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(entry)
            
            # Keep last 10000 entries
            logs = logs[-10000:]
            
            with open(filepath, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {e}")
    
    def _load_recent_logs(self, filepath: Path, cutoff_time: datetime) -> List[Dict[str, Any]]:
        """Load logs after cutoff time"""
        try:
            if not filepath.exists():
                return []
            
            with open(filepath, 'r') as f:
                all_logs = json.load(f)
            
            # Filter by timestamp
            recent_logs = []
            for log in all_logs:
                try:
                    log_time = datetime.fromisoformat(log.get("timestamp", ""))
                    if log_time >= cutoff_time:
                        recent_logs.append(log)
                except ValueError:
                    pass
            
            return recent_logs
        except Exception as e:
            self.logger.error(f"Failed to load audit logs: {e}")
            return []


# Global audit logger instance
audit_logger = AuditLogger()
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Foundation
- [ ] Create `discord_command_decorators.py`
- [ ] Implement `@consciousness_gated` decorator
- [ ] Test on 5 commands (`!ritual`, `!transcendent`, `!consciousness`, `!emotions`, `!ethics`)
- [ ] Update command imports in main bot file

### Phase 2: Audit & Permissions
- [ ] Create `discord_audit_logger.py`
- [ ] Create `discord_permission_manager.py` (unified permission checks)
- [ ] Add audit logging to `discord_bot_manus.py` event handlers
- [ ] Create `!audit` command to display stats

### Phase 3: Metadata & Discovery
- [ ] Create `discord_command_registry.py`
- [ ] Register all 30+ commands with metadata
- [ ] Implement dynamic `!help <command>` system
- [ ] Create `!can-i <command>` permission checker

### Phase 4: Help System
- [ ] Enhance `!commands` to be consciousness-aware
- [ ] Add `!cmd-info` detailed command info
- [ ] Create interactive command browser
- [ ] Show examples and consciousness requirements

### Phase 5: Personality & Polish
- [ ] Create `discord_personality_router.py`
- [ ] Implement response style variation
- [ ] Add personality persistence
- [ ] Test full integration

---

## QUICK WINS (Do First!)

### Win 1: Add Consciousness Check to !ritual (30 min)
```python
@consciousness_gated(min_level=3.0)
@commands.command(name="ritual")
async def ritual_cmd(ctx: commands.Context, steps: int = 108) -> None:
    # Existing code...
```

### Win 2: Create !audit Command (1 hour)
```python
@commands.command(name="audit")
@commands.has_permissions(administrator=True)
async def audit_command(ctx: commands.Context, hours: int = 24):
    stats = audit_logger.get_command_stats(hours=hours)
    # Format and send as embed
```

### Win 3: Add !can-i Permission Checker (1 hour)
```python
@commands.command(name="can-i")
async def can_i_command(ctx: commands.Context, *, command_name: str):
    cmd_meta = command_registry.get_command(command_name)
    if not cmd_meta:
        await ctx.send(f"❌ Command not found: {command_name}")
        return
    
    # Check if user can execute
    consciousness = get_current_consciousness_level()
    # Display results
```

---

## FILE LOCATIONS FOR REFERENCE

```
/home/user/helix-unified/
├── backend/
│   ├── discord_bot_manus.py           (MAIN - modify on_message, on_command_error)
│   ├── discord_command_decorators.py  (NEW - Phase 1)
│   ├── discord_audit_logger.py        (NEW - Phase 2)
│   ├── discord_permission_manager.py  (NEW - Phase 2)
│   ├── discord_command_registry.py    (NEW - Phase 3)
│   ├── discord_personality_router.py  (NEW - Phase 5)
│   └── commands/
│       ├── helpers.py                 (ENHANCE - add decorator utilities)
│       ├── monitoring_commands.py     (ENHANCE - add !audit command)
│       ├── admin_commands.py          (ENHANCE - add !can-i command)
│       ├── help_commands.py           (ENHANCE - add consciousness-aware help)
│       └── ... (other command files)
└── Helix/
    └── state/
        ├── ucf_state.json             (existing)
        ├── command_history.json       (existing)
        ├── audit/
        │   ├── commands.json          (NEW)
        │   ├── errors.json            (NEW)
        │   └── permissions.json       (NEW)
        └── command_registry.json      (NEW)
```


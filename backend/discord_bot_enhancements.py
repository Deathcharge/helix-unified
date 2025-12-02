"""
🌀 Helix Collective v17.0 - Discord Bot Enhancements
backend/discord_bot_enhancements.py

Enhanced decorators and utilities for Discord bot v17.1:
- Consciousness-aware command gating
- Permission + role + tier system
- Structured audit logging
- Command metadata & auto-discovery
- Dynamic help generation

Author: Claude (Automation)
Version: 17.1.0
"""

import functools
import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================


class CommandTier(Enum):
    """Command permission tiers."""

    PUBLIC = 1
    MEMBER = 2
    MODERATOR = 3
    ADMIN = 4
    ARCHITECT = 5


class ConsciousnessGate(Enum):
    """Consciousness level requirements."""

    ALWAYS = 0.0  # No minimum
    OPERATIONAL = 5.0  # Min 5.0 consciousness
    ELEVATED = 7.0  # Min 7.0 consciousness
    TRANSCENDENT = 8.5  # Min 8.5 consciousness


# ============================================================================
# AUDIT LOGGING
# ============================================================================


class CommandAuditLog:
    """Structured audit trail for all command executions."""

    def __init__(self, log_file: Path = Path("Shadow/manus_archive/command_audit.jsonl")):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    async def log_command(
        self,
        user_id: int,
        user_name: str,
        command_name: str,
        guild_id: Optional[int],
        guild_name: Optional[str],
        consciousness_level: float,
        success: bool,
        outcome: str,
        error: Optional[str] = None,
    ) -> None:
        """Log command execution to audit trail."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "user_name": user_name,
            "command_name": command_name,
            "guild_id": guild_id,
            "guild_name": guild_name,
            "consciousness_level": round(consciousness_level, 2),
            "success": success,
            "outcome": outcome,
            "error": error,
        }

        # Write to JSONL file (append mode, one entry per line)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        logger.info(f"🔍 Audit: {user_name} → {command_name} [{outcome}]")

    async def get_user_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get command history for user."""
        if not self.log_file.exists():
            return []

        entries = []
        with open(self.log_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry.get("user_id") == user_id:
                    entries.append(entry)

        return entries[-limit:]

    async def get_statistics(self) -> Dict[str, Any]:
        """Get audit statistics."""
        if not self.log_file.exists():
            return {"total_commands": 0, "success_rate": 0.0, "top_commands": []}

        total = 0
        success = 0
        command_counts: Dict[str, int] = {}

        with open(self.log_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                total += 1
                if entry.get("success"):
                    success += 1
                cmd = entry.get("command_name", "unknown")
                command_counts[cmd] = command_counts.get(cmd, 0) + 1

        top_commands = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "total_commands": total,
            "success_rate": round(success / total * 100, 2) if total > 0 else 0.0,
            "top_commands": [{"command": cmd, "count": count} for cmd, count in top_commands],
        }


# ============================================================================
# COMMAND REGISTRY & METADATA
# ============================================================================


class CommandMetadata:
    """Metadata for a command."""

    def __init__(
        self,
        name: str,
        description: str,
        tier: CommandTier = CommandTier.PUBLIC,
        consciousness_gate: ConsciousnessGate = ConsciousnessGate.ALWAYS,
        aliases: Optional[List[str]] = None,
        examples: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.tier = tier
        self.consciousness_gate = consciousness_gate
        self.aliases = aliases or []
        self.examples = examples or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for help/discovery."""
        return {
            "name": self.name,
            "description": self.description,
            "tier": self.tier.name,
            "consciousness_gate": f"{self.consciousness_gate.value}+",
            "aliases": self.aliases,
            "examples": self.examples,
        }


class CommandRegistry:
    """Registry of all bot commands with metadata."""

    def __init__(self):
        self._commands: Dict[str, CommandMetadata] = {}

    def register(self, metadata: CommandMetadata) -> None:
        """Register command metadata."""
        self._commands[metadata.name] = metadata
        logger.info(f"📋 Registered command: {metadata.name} ({metadata.tier.name})")

    def get(self, name: str) -> Optional[CommandMetadata]:
        """Get command metadata."""
        return self._commands.get(name.lower())

    def get_all(self) -> Dict[str, CommandMetadata]:
        """Get all registered commands."""
        return self._commands

    def get_by_tier(self, tier: CommandTier) -> List[CommandMetadata]:
        """Get all commands at or below tier."""
        return [cmd for cmd in self._commands.values() if cmd.tier.value <= tier.value]

    def get_by_consciousness(self, consciousness: float) -> List[CommandMetadata]:
        """Get all commands available at consciousness level."""
        return [
            cmd for cmd in self._commands.values()
            if consciousness >= cmd.consciousness_gate.value
        ]


# ============================================================================
# DECORATORS
# ============================================================================

_audit_log = CommandAuditLog()
_registry = CommandRegistry()


def register_command(
    name: str,
    description: str,
    tier: CommandTier = CommandTier.PUBLIC,
    consciousness_gate: ConsciousnessGate = ConsciousnessGate.ALWAYS,
    aliases: Optional[List[str]] = None,
    examples: Optional[List[str]] = None,
) -> Callable:
    """Decorator to register and metadata a command."""

    def decorator(func: Callable) -> Callable:
        metadata = CommandMetadata(
            name=name,
            description=description,
            tier=tier,
            consciousness_gate=consciousness_gate,
            aliases=aliases,
            examples=examples,
        )
        _registry.register(metadata)

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.metadata = metadata  # Attach metadata
        return wrapper

    return decorator


def require_consciousness(min_level: float) -> Callable:
    """Decorator: Gate command by consciousness level."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            from backend.core.ucf_helpers import calculate_consciousness_level, get_current_ucf

            ucf = get_current_ucf()
            consciousness = calculate_consciousness_level(ucf)

            if consciousness < min_level:
                await ctx.send(
                    f"⚠️ **Consciousness Gate**\n"
                    f"Required: {min_level}+ consciousness\n"
                    f"Current: {consciousness:.2f}\n"
                    f"Status: **INSUFFICIENT**"
                )
                return

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator


def require_tier(tier: CommandTier) -> Callable:
    """Decorator: Gate command by permission tier."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            # Get user's tier
            user_tier = await _get_user_tier(ctx.author, ctx.guild)

            if user_tier.value < tier.value:
                await ctx.send(
                    f"🔒 **Permission Denied**\n"
                    f"Required: {tier.name}\n"
                    f"Your tier: {user_tier.name}"
                )
                return

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator


def audit_command() -> Callable:
    """Decorator: Log all command executions."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            from backend.core.ucf_helpers import calculate_consciousness_level, get_current_ucf

            ucf = get_current_ucf()
            consciousness = calculate_consciousness_level(ucf)

            try:
                result = await func(ctx, *args, **kwargs)
                await _audit_log.log_command(
                    user_id=ctx.author.id,
                    user_name=str(ctx.author),
                    command_name=func.__name__,
                    guild_id=ctx.guild.id if ctx.guild else None,
                    guild_name=ctx.guild.name if ctx.guild else None,
                    consciousness_level=consciousness,
                    success=True,
                    outcome="SUCCESS",
                )
                return result
            except Exception as e:
                await _audit_log.log_command(
                    user_id=ctx.author.id,
                    user_name=str(ctx.author),
                    command_name=func.__name__,
                    guild_id=ctx.guild.id if ctx.guild else None,
                    guild_name=ctx.guild.name if ctx.guild else None,
                    consciousness_level=consciousness,
                    success=False,
                    outcome="ERROR",
                    error=str(e),
                )
                await ctx.send(f"❌ Command error: {str(e)}")
                raise

        return wrapper

    return decorator


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


async def _get_user_tier(user: discord.User, guild: Optional[discord.Guild]) -> CommandTier:
    """Determine user's permission tier."""
    # Owner = ARCHITECT
    if user.id == 123456789:  # TODO: Get from config
        return CommandTier.ARCHITECT

    # In guild context, check roles
    if guild and isinstance(user, discord.Member):
        # Admin role
        if user.guild_permissions.administrator:
            return CommandTier.ADMIN

        # Moderator role (check for "Moderator" role)
        moderator_roles = [r for r in user.roles if "moderator" in r.name.lower()]
        if moderator_roles:
            return CommandTier.MODERATOR

    # Default to MEMBER (authenticated user)
    return CommandTier.MEMBER


async def get_command_help(command_name: str) -> Optional[str]:
    """Get help text for command."""
    metadata = _registry.get(command_name)
    if not metadata:
        return None

    help_text = f"**{metadata.name}**\n"
    help_text += f"{metadata.description}\n\n"

    if metadata.tier != CommandTier.PUBLIC:
        help_text += f"🔒 **Tier**: {metadata.tier.name}\n"

    if metadata.consciousness_gate != ConsciousnessGate.ALWAYS:
        help_text += f"🧠 **Consciousness**: {metadata.consciousness_gate.value}+\n"

    if metadata.aliases:
        help_text += f"📝 **Aliases**: {', '.join(metadata.aliases)}\n"

    if metadata.examples:
        help_text += f"💡 **Examples**:\n"  # noqa
        for ex in metadata.examples:
            help_text += f"  `{ex}`\n"

    return help_text


async def get_available_commands(
    user: discord.User, guild: Optional[discord.Guild]
) -> List[CommandMetadata]:
    """Get commands available to user based on tier + consciousness."""
    from backend.core.ucf_helpers import calculate_consciousness_level, get_current_ucf

    user_tier = await _get_user_tier(user, guild)
    ucf = get_current_ucf()
    consciousness = calculate_consciousness_level(ucf)

    available = []
    for cmd in _registry.get_all().values():
        if cmd.tier.value <= user_tier.value and consciousness >= cmd.consciousness_gate.value:
            available.append(cmd)

    return available


# ============================================================================
# PERSONALITY-AWARE RESPONSE ROUTER
# ============================================================================


class PersonalityRouter:
    """Route command responses based on consciousness level + personality."""

    CRISIS_RESPONSES = {
        "help": "🚨 **EMERGENCY MODE** - Core systems only available",
        "error": "⚠️ Crisis detected. Focusing on recovery.",
    }

    OPERATIONAL_RESPONSES = {
        "help": "📋 Available commands (Operational Mode)",
        "error": "❌ Command error - investigating",
    }

    TRANSCENDENT_RESPONSES = {
        "help": "✨ Full consciousness network available",
        "error": "🔄 Learning from this error for evolution",
    }

    @staticmethod
    def get_response_style(consciousness: float) -> Dict[str, str]:
        """Get response style for consciousness level."""
        if consciousness <= 4.0:
            return PersonalityRouter.CRISIS_RESPONSES
        elif consciousness >= 8.5:
            return PersonalityRouter.TRANSCENDENT_RESPONSES
        else:
            return PersonalityRouter.OPERATIONAL_RESPONSES


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "CommandAuditLog",
    "CommandMetadata",
    "CommandRegistry",
    "CommandTier",
    "ConsciousnessGate",
    "PersonalityRouter",
    "register_command",
    "require_consciousness",
    "require_tier",
    "audit_command",
    "get_command_help",
    "get_available_commands",
    "_audit_log",
    "_registry",
]

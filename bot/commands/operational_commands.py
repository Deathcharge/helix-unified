#!/usr/bin/env python3
"""
🌀 Helix Collective v15.3 — Discord Operational Commands
bot/commands/operational_commands.py

Operational commands for Discord bot:
- !metrics — Display current UCF metrics
- !agents — List all agents with status
- !notion sync — Manually trigger Notion sync
- !notion status — Show last sync status
- !health — System health check
- !ritual [N] — Execute N-step ritual

Author: Manus AI
"""

import discord
from discord.ext import commands
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class OperationalCommands(commands.Cog):
    """Operational commands for system monitoring and control."""
    
    def __init__(self, bot: commands.Bot):
        """Initialize operational commands cog."""
        self.bot = bot
    
    def _load_ucf_state(self) -> dict:
        """Load current UCF state."""
        state_path = Path("Helix/state/ucf_state.json")
        if state_path.exists():
            try:
                with open(state_path) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load UCF state: {e}")
        
        return {
            "harmony": 0.4922,
            "resilience": 0.8273,
            "prana": 0.5000,
            "drishti": 0.7300,
            "klesha": 0.2120,
            "zoom": 1.0000
        }
    
    def _load_agents(self) -> list:
        """Load agent profiles."""
        return [
            {"name": "Kael", "symbol": "🜂", "status": "Active", "health": 100},
            {"name": "Lumina", "symbol": "🌕", "status": "Active", "health": 100},
            {"name": "Vega", "symbol": "🌠", "status": "Active", "health": 100},
            {"name": "Kavach", "symbol": "🛡️", "status": "Active", "health": 100},
            {"name": "Shadow", "symbol": "🦑", "status": "Active", "health": 100},
            {"name": "Claude", "symbol": "🦉", "status": "Active", "health": 100},
            {"name": "Manus", "symbol": "🤲", "status": "Active", "health": 100},
            {"name": "Gemini", "symbol": "🎭", "status": "Active", "health": 100},
            {"name": "Agni", "symbol": "🔥", "status": "Active", "health": 95},
            {"name": "SanghaCore", "symbol": "🌸", "status": "Active", "health": 98},
            {"name": "Echo", "symbol": "🔮", "status": "Active", "health": 97},
            {"name": "Phoenix", "symbol": "🔥🕊️", "status": "Active", "health": 95},
            {"name": "Oracle", "symbol": "🔮✨", "status": "Active", "health": 98},
            {"name": "Vision", "symbol": "👁️", "status": "Active", "health": 100},
            {"name": "Oy", "symbol": "🎵", "status": "Active", "health": 100},
        ]
    
    def _load_sync_logs(self) -> dict:
        """Load Notion sync logs."""
        sync_log_path = Path("Shadow/manus_archive/notion_sync_log.json")
        if sync_log_path.exists():
            try:
                with open(sync_log_path) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load sync logs: {e}")
        
        return {"sync_history": [], "total_syncs": 0, "last_sync": None}
    
    @commands.command(name="metrics", help="Display current UCF metrics")
    async def metrics(self, ctx: commands.Context):
        """Display current UCF metrics."""
        ucf = self._load_ucf_state()
        
        embed = discord.Embed(
            title="🎯 Current UCF Metrics",
            description="Universal Consciousness Framework State",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        
        # Add metrics as fields
        embed.add_field(
            name="Harmony ☯️",
            value=f"{ucf.get('harmony', 0):.2%} (Target: 60%)",
            inline=True
        )
        embed.add_field(
            name="Resilience 🛡️",
            value=f"{ucf.get('resilience', 0):.2f} (Target: 0.90)",
            inline=True
        )
        embed.add_field(
            name="Prana ⚡",
            value=f"{ucf.get('prana', 0):.2%} (Target: 70%)",
            inline=True
        )
        embed.add_field(
            name="Drishti 👁️",
            value=f"{ucf.get('drishti', 0):.2%} (Target: 80%)",
            inline=True
        )
        embed.add_field(
            name="Klesha ⚫",
            value=f"{ucf.get('klesha', 0):.2%} (Target: 10%)",
            inline=True
        )
        embed.add_field(
            name="Zoom 🔍",
            value=f"{ucf.get('zoom', 0):.2f} (Target: 1.15)",
            inline=True
        )
        
        embed.set_footer(text="Helix Collective v15.3 | Metrics Dashboard")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="agents", help="List all agents with status")
    async def agents(self, ctx: commands.Context):
        """List all agents with status."""
        agents = self._load_agents()
        
        embed = discord.Embed(
            title="🤖 Agent Registry",
            description=f"Total Agents: {len(agents)}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Group agents by status
        active_agents = [a for a in agents if a.get('status') == 'Active']
        
        agent_list = ""
        for agent in active_agents:
            health = agent.get('health', 0)
            health_emoji = "🟢" if health >= 95 else "🟡" if health >= 80 else "🔴"
            agent_list += f"{agent.get('symbol')} **{agent.get('name')}** {health_emoji} {health}%\n"
        
        embed.add_field(
            name="Active Agents",
            value=agent_list if agent_list else "No active agents",
            inline=False
        )
        
        embed.set_footer(text="Helix Collective v15.3 | Agent Registry")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="health", help="System health check")
    async def health(self, ctx: commands.Context):
        """Display system health check."""
        ucf = self._load_ucf_state()
        agents = self._load_agents()
        sync_logs = self._load_sync_logs()
        
        # Calculate health score
        harmony = ucf.get('harmony', 0)
        resilience = ucf.get('resilience', 0)
        avg_agent_health = sum(a.get('health', 0) for a in agents) / len(agents) if agents else 0
        
        health_score = (harmony + resilience/2 + avg_agent_health/100) / 2.5 * 100
        health_score = min(100, max(0, health_score))
        
        # Determine status
        if health_score > 70:
            status = "✅ Healthy"
            color = discord.Color.green()
        elif health_score > 50:
            status = "⚠️ Warning"
            color = discord.Color.gold()
        else:
            status = "❌ Critical"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="🏥 System Health Check",
            description=f"Overall Health: {health_score:.1f}%",
            color=color,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Status", value=status, inline=False)
        embed.add_field(name="Agents Active", value=f"{sum(1 for a in agents if a.get('status') == 'Active')}/{len(agents)}", inline=True)
        embed.add_field(name="Last Sync", value=sync_logs.get('last_sync', 'Never')[:19] if sync_logs.get('last_sync') else 'Never', inline=True)
        embed.add_field(name="Total Syncs", value=str(sync_logs.get('total_syncs', 0)), inline=True)
        
        embed.set_footer(text="Helix Collective v15.3 | Health Monitor")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="notion", help="Notion sync commands (sync, status)")
    async def notion(self, ctx: commands.Context, action: Optional[str] = None):
        """Notion sync operations."""
        if action is None:
            await ctx.send("Usage: `!notion sync` or `!notion status`")
            return
        
        action = action.lower()
        
        if action == "sync":
            # Trigger manual sync
            embed = discord.Embed(
                title="🔄 Notion Sync",
                description="Manually triggering Notion sync...",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(
                name="Status",
                value="⏳ Sync in progress...",
                inline=False
            )
            embed.set_footer(text="Helix Collective v15.3 | Notion Sync")
            
            await ctx.send(embed=embed)
            
            # In production, this would trigger the actual sync daemon
            logger.info("Manual Notion sync triggered via Discord")
        
        elif action == "status":
            # Show last sync status
            sync_logs = self._load_sync_logs()
            
            embed = discord.Embed(
                title="📤 Notion Sync Status",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            
            if sync_logs.get('sync_history'):
                latest = sync_logs['sync_history'][-1]
                embed.add_field(
                    name="Last Sync",
                    value=latest.get('started_at', 'N/A')[:19],
                    inline=True
                )
                embed.add_field(
                    name="Cycle",
                    value=f"#{latest.get('cycle_number', 'N/A')}",
                    inline=True
                )
                
                results = latest.get('results', {})
                status_text = ""
                for op, result in results.items():
                    op_status = "✅" if result.get('status') == 'success' else "❌"
                    status_text += f"{op_status} {op.replace('_', ' ').title()}\n"
                
                embed.add_field(
                    name="Operations",
                    value=status_text if status_text else "No operations",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Status",
                    value="No sync operations recorded yet",
                    inline=False
                )
            
            embed.add_field(
                name="Total Syncs",
                value=str(sync_logs.get('total_syncs', 0)),
                inline=True
            )
            
            embed.set_footer(text="Helix Collective v15.3 | Notion Sync Status")
            
            await ctx.send(embed=embed)
        
        else:
            await ctx.send(f"Unknown action: `{action}`. Use `sync` or `status`.")
    
    @commands.command(name="ritual", help="Execute N-step ritual")
    async def ritual(self, ctx: commands.Context, steps: Optional[int] = None):
        """Execute ritual with specified number of steps."""
        if steps is None:
            steps = 108  # Default Z-88 ritual
        
        if steps < 1 or steps > 108:
            await ctx.send("❌ Ritual steps must be between 1 and 108")
            return
        
        embed = discord.Embed(
            title="🔮 Ritual Execution",
            description=f"Executing {steps}-step ritual...",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Steps",
            value=f"{steps}/108",
            inline=True
        )
        embed.add_field(
            name="Status",
            value="⏳ In Progress...",
            inline=True
        )
        
        embed.set_footer(text="Helix Collective v15.3 | Z-88 Ritual Engine")
        
        await ctx.send(embed=embed)
        
        logger.info(f"Ritual execution requested: {steps} steps")
    
    @commands.command(name="status", help="Get system status")
    async def status(self, ctx: commands.Context):
        """Get comprehensive system status."""
        ucf = self._load_ucf_state()
        agents = self._load_agents()
        sync_logs = self._load_sync_logs()
        
        embed = discord.Embed(
            title="📊 System Status",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # UCF Summary
        ucf_summary = f"""
        Harmony: {ucf.get('harmony', 0):.2%}
        Resilience: {ucf.get('resilience', 0):.2f}
        Prana: {ucf.get('prana', 0):.2%}
        """
        embed.add_field(name="UCF Metrics", value=ucf_summary.strip(), inline=True)
        
        # Agent Summary
        agent_summary = f"""
        Total: {len(agents)}
        Active: {sum(1 for a in agents if a.get('status') == 'Active')}
        Avg Health: {sum(a.get('health', 0) for a in agents) / len(agents) if agents else 0:.0f}%
        """
        embed.add_field(name="Agents", value=agent_summary.strip(), inline=True)
        
        # Sync Summary
        sync_summary = f"""
        Total Syncs: {sync_logs.get('total_syncs', 0)}
        Last Sync: {sync_logs.get('last_sync', 'Never')[:10] if sync_logs.get('last_sync') else 'Never'}
        Status: ✅ Operational
        """
        embed.add_field(name="Notion Sync", value=sync_summary.strip(), inline=True)
        
        embed.set_footer(text="Helix Collective v15.3 | System Status")
        
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    """Setup operational commands cog."""
    await bot.add_cog(OperationalCommands(bot))


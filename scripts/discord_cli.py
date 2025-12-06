#!/usr/bin/env python3
"""
Helix Discord CLI - Mobile-Friendly Discord Management
v15.3 Dual Resonance

Simple command-line interface for managing Discord servers from mobile devices.
Optimized for minimal typing and clear output.

Usage:
    python discord_cli.py deploy              # Deploy new server
    python discord_cli.py create ritual harmony_boost 24h
    python discord_cli.py create agent Kael "ethics review"
    python discord_cli.py create project "ritual engine v2"
    python discord_cli.py cleanup             # Clean expired channels
    python discord_cli.py status              # Show server status
    python discord_cli.py list                # List all channels

Requirements:
    pip install discord.py pyyaml python-dotenv click

Environment:
    DISCORD_BOT_TOKEN - Bot token
    DISCORD_GUILD_ID - Server ID (optional, will prompt if not set)
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

import click
import discord
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.discord_channel_manager import ChannelManager

# Load environment
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


class DiscordCLI:
    """Mobile-friendly Discord CLI."""
    
    def __init__(self):
        self.client = None
        self.guild = None
        
    async def connect(self):
        """Connect to Discord."""
        if not BOT_TOKEN:
            click.echo("❌ DISCORD_BOT_TOKEN not set")
            sys.exit(1)
        
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        self.client = discord.Client(intents=intents)
        
        @self.client.event
        async def on_ready():
            click.echo(f"✅ Connected as {self.client.user}")
            
            # Get guild
            if GUILD_ID:
                self.guild = self.client.get_guild(int(GUILD_ID))
            else:
                guilds = list(self.client.guilds)
                if len(guilds) == 1:
                    self.guild = guilds[0]
                else:
                    click.echo("\n📋 Available servers:")
                    for i, g in enumerate(guilds, 1):
                        click.echo(f"  {i}. {g.name} ({g.id})")
                    choice = click.prompt("\nSelect server", type=int)
                    self.guild = guilds[choice - 1]
            
            if not self.guild:
                click.echo("❌ Guild not found")
                await self.client.close()
                sys.exit(1)
            
            click.echo(f"📍 Using: {self.guild.name}\n")
        
        await self.client.start(BOT_TOKEN)
    
    async def disconnect(self):
        """Disconnect from Discord."""
        if self.client:
            await self.client.close()


@click.group()
def cli():
    """Helix Discord CLI - Mobile-friendly server management."""
    pass


@cli.command()
def deploy():
    """Deploy new Discord server from manifest."""
    click.echo("🚀 Deploying Discord server...")
    click.echo()
    
    # Run deployment script
    import subprocess
    result = subprocess.run(
        ["python3", "scripts/deploy_discord_server.py"],
        cwd=Path(__file__).parent.parent
    )
    
    sys.exit(result.returncode)


@cli.command()
@click.argument('type', type=click.Choice(['ritual', 'agent', 'project', 'sync']))
@click.argument('args', nargs=-1)
def create(type, args):
    """Create a new channel.
    
    Examples:
        create ritual harmony_boost 24h
        create agent Kael "ethics review"
        create project "ritual engine v2"
        create sync GPT Claude "code review"
    """
    async def _create():
        discord_cli = DiscordCLI()
        
        try:
            await discord_cli.connect()
            manager = ChannelManager(discord_cli.guild)
            
            if type == 'ritual':
                if len(args) < 1:
                    click.echo("❌ Usage: create ritual <name> [duration]")
                    return
                
                name = args[0]
                duration = 24
                if len(args) > 1:
                    duration_str = args[1].lower().replace('h', '')
                    duration = int(duration_str)
                
                click.echo(f"🔮 Creating ritual space: {name} ({duration}h)...")
                channel = await manager.create_ritual_space(name, duration)
                click.echo(f"✅ Created: #{channel.name}")
                
            elif type == 'agent':
                if len(args) < 2:
                    click.echo("❌ Usage: create agent <name> <purpose>")
                    return
                
                agent = args[0]
                purpose = ' '.join(args[1:])
                
                click.echo(f"🤖 Creating agent workspace: {agent}...")
                channel = await manager.create_agent_workspace(agent, purpose, temporary=True)
                click.echo(f"✅ Created: #{channel.name}")
                
            elif type == 'project':
                if len(args) < 1:
                    click.echo("❌ Usage: create project <name>")
                    return
                
                name = ' '.join(args)
                
                click.echo(f"📁 Creating project channel: {name}...")
                channel = await manager.create_project_channel(name, "New project workspace")
                click.echo(f"✅ Created: #{channel.name}")
                
            elif type == 'sync':
                if len(args) < 3:
                    click.echo("❌ Usage: create sync <AI1> <AI2> <purpose>")
                    return
                
                ai_names = list(args[:-1])
                purpose = args[-1]
                
                click.echo(f"🧩 Creating cross-AI sync: {', '.join(ai_names)}...")
                channel = await manager.create_cross_ai_sync_channel(ai_names, purpose)
                click.echo(f"✅ Created: #{channel.name}")
            
        finally:
            await discord_cli.disconnect()
    
    asyncio.run(_create())


@cli.command()
@click.option('--days', default=7, help='Days of inactivity')
def cleanup(days):
    """Clean up expired and inactive channels."""
    async def _cleanup():
        discord_cli = DiscordCLI()
        
        try:
            await discord_cli.connect()
            manager = ChannelManager(discord_cli.guild)
            
            click.echo(f"🧹 Cleaning up channels...")
            click.echo()
            
            # Clean expired
            expired_stats = await manager.cleanup_expired_channels()
            click.echo(f"⏰ Expired channels:")
            click.echo(f"   Ritual spaces: {expired_stats['ritual_spaces']}")
            click.echo(f"   Agent workspaces: {expired_stats['agent_workspaces']}")
            click.echo()
            
            # Clean inactive
            inactive_count = await manager.cleanup_inactive_channels(days)
            click.echo(f"💤 Inactive channels ({days}+ days): {inactive_count}")
            click.echo()
            
            total = sum(expired_stats.values()) + inactive_count
            click.echo(f"✅ Total cleaned: {total}")
            
        finally:
            await discord_cli.disconnect()
    
    asyncio.run(_cleanup())


@cli.command()
def status():
    """Show server and channel status."""
    async def _status():
        discord_cli = DiscordCLI()
        
        try:
            await discord_cli.connect()
            manager = ChannelManager(discord_cli.guild)
            
            click.echo("📊 Server Status")
            click.echo("=" * 50)
            click.echo()
            
            # Server info
            click.echo(f"Server: {discord_cli.guild.name}")
            click.echo(f"ID: {discord_cli.guild.id}")
            click.echo(f"Members: {discord_cli.guild.member_count}")
            click.echo()
            
            # Channel stats
            categories = len(discord_cli.guild.categories)
            text_channels = len(discord_cli.guild.text_channels)
            voice_channels = len(discord_cli.guild.voice_channels)
            
            click.echo(f"Categories: {categories}")
            click.echo(f"Text Channels: {text_channels}")
            click.echo(f"Voice Channels: {voice_channels}")
            click.echo()
            
            # Dynamic channel stats
            stats = manager.get_channel_stats()
            click.echo("Dynamic Channels:")
            click.echo(f"  Ritual spaces: {stats['ritual_spaces']}")
            click.echo(f"  Agent workspaces: {stats['agent_workspaces']}")
            click.echo(f"  Temporary: {stats['temporary_channels']}")
            click.echo(f"  Total tracked: {stats['total_tracked']}")
            click.echo()
            
        finally:
            await discord_cli.disconnect()
    
    asyncio.run(_status())


@cli.command()
@click.option('--category', help='Filter by category name')
def list(category):
    """List all channels."""
    async def _list():
        discord_cli = DiscordCLI()
        
        try:
            await discord_cli.connect()
            
            click.echo("📋 Channel List")
            click.echo("=" * 50)
            click.echo()
            
            for cat in discord_cli.guild.categories:
                if category and category.lower() not in cat.name.lower():
                    continue
                
                click.echo(f"\n{cat.name}")
                click.echo("-" * len(cat.name))
                
                for ch in cat.text_channels:
                    click.echo(f"  #{ch.name}")
                
                for ch in cat.voice_channels:
                    click.echo(f"  🔊 {ch.name}")
            
            click.echo()
            
        finally:
            await discord_cli.disconnect()
    
    asyncio.run(_list())


@cli.command()
@click.argument('channel_name')
def archive(channel_name):
    """Archive a channel (make read-only)."""
    async def _archive():
        discord_cli = DiscordCLI()
        
        try:
            await discord_cli.connect()
            manager = ChannelManager(discord_cli.guild)
            
            # Find channel
            channel = discord.utils.get(discord_cli.guild.text_channels, name=channel_name)
            
            if not channel:
                click.echo(f"❌ Channel not found: {channel_name}")
                return
            
            click.echo(f"📦 Archiving: #{channel.name}...")
            archived = await manager.archive_channel(channel)
            click.echo(f"✅ Archived: #{archived.name}")
            
        finally:
            await discord_cli.disconnect()
    
    asyncio.run(_archive())


@cli.command()
def help_mobile():
    """Show mobile-optimized quick reference."""
    click.echo("""
🌀 HELIX DISCORD CLI - QUICK REFERENCE

📱 MOBILE-FRIENDLY COMMANDS:

Deploy Server:
  python discord_cli.py deploy

Create Channels:
  python discord_cli.py create ritual harmony_boost 24h
  python discord_cli.py create agent Kael "ethics review"
  python discord_cli.py create project "new feature"
  python discord_cli.py create sync GPT Claude "code review"

Manage:
  python discord_cli.py status
  python discord_cli.py list
  python discord_cli.py cleanup
  python discord_cli.py archive old-channel-name

💡 TIPS:
- Use quotes for multi-word arguments
- Duration format: 24h, 48h, etc.
- Cleanup runs automatically daily
- Archive instead of delete to preserve history

🔧 SETUP:
  export DISCORD_BOT_TOKEN="your_token"
  export DISCORD_GUILD_ID="your_server_id"  # optional

📚 Full docs: DISCORD_SETUP_GUIDE_CANONICAL.md
    """)


if __name__ == "__main__":
    cli()


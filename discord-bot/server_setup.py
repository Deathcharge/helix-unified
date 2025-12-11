"""
Discord Server Setup and Management
Creates channels, voice channels, and configures permissions
"""

import asyncio
import logging
import os

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServerSetup:
    """Manages Discord server structure"""
    
    # Server structure definition
    SERVER_STRUCTURE = {
        "🌀 WELCOME": {
            "channels": ["manifesto", "rules", "introductions"],
            "voice": ["Welcome Lounge"]
        },
        "🧠 SYSTEM": {
            "channels": ["telemetry", "weekly-digest", "shadow-storage", "ucf-sync"],
            "voice": ["System Monitor"]
        },
        "🔮 PROJECTS": {
            "channels": ["helix-repository", "fractal-l"],
            "voice": ["Project Discussion"]
        },
        "🎭 AGENTS": {
            "channels": [
                "vega-core", "kael-core", "lumina-core", "shadow-outer",
                "kavach-shield", "gemini-scout", "sanghacore", "agni-core",
                "phoenix-outer", "aether-core", "echo-outer", "oracle-outer",
                "chai-link", "grok-implicit", "claude-implicit", "gpt-implicit",
                "shadow-archive"
            ],
            "voice": ["Agent Coordination"]
        },
        "🌐 CROSS-MODEL SYNC": {
            "channels": ["gpt-grok-claude-sync", "chai-link", "manus-bridge"],
            "voice": ["Model Sync Room"]
        },
        "🔧 DEVELOPMENT": {
            "channels": ["bot-commands", "code-snippets", "testing-lab"],
            "voice": ["Dev Workshop"]
        },
        "🕉️ RITUAL & LORE": {
            "channels": ["neti-neti-mantra", "codex-archives", "ucf-reflections", "harmonic-updates"],
            "voice": ["Ritual Chamber"]
        },
        "🔒 ADMIN": {
            "channels": ["moderation", "announcements", "backups"],
            "voice": ["Admin Office"]
        }
    }
    
    # Add voice-transcripts to SYSTEM category
    VOICE_TRANSCRIPTS_CHANNEL = "voice-transcripts"
    
    def __init__(self, bot):
        self.bot = bot
    
    async def setup_server(self, guild: discord.Guild):
        """Set up complete server structure"""
        logger.info(f"Setting up server: {guild.name}")
        
        try:
            # Create categories and channels
            for category_name, structure in self.SERVER_STRUCTURE.items():
                await self.setup_category(guild, category_name, structure)
            
            # Add voice-transcripts channel to SYSTEM
            system_category = discord.utils.get(guild.categories, name="🧠 SYSTEM")
            if system_category:
                await self.create_channel_if_missing(
                    guild, 
                    system_category, 
                    self.VOICE_TRANSCRIPTS_CHANNEL,
                    channel_type="text"
                )
            
            logger.info("Server setup complete!")
        
        except Exception as e:
            logger.error(f"Server setup error: {e}")
    
    async def setup_category(self, guild: discord.Guild, category_name: str, structure: dict):
        """Set up a category with its channels"""
        # Find or create category
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            logger.info(f"Creating category: {category_name}")
            category = await guild.create_category(category_name)
        
        # Create text channels
        for channel_name in structure.get("channels", []):
            await self.create_channel_if_missing(guild, category, channel_name, "text")
        
        # Create voice channels
        for voice_name in structure.get("voice", []):
            await self.create_channel_if_missing(guild, category, voice_name, "voice")
    
    async def create_channel_if_missing(
        self, 
        guild: discord.Guild, 
        category: discord.CategoryChannel,
        channel_name: str,
        channel_type: str = "text"
    ):
        """Create channel if it doesn't exist"""
        # Check if channel exists
        existing = discord.utils.get(guild.channels, name=channel_name, category=category)
        if existing:
            logger.info(f"Channel already exists: #{channel_name}")
            return existing
        
        # Create channel
        logger.info(f"Creating {channel_type} channel: {channel_name}")
        
        if channel_type == "text":
            return await guild.create_text_channel(channel_name, category=category)
        elif channel_type == "voice":
            return await guild.create_voice_channel(channel_name, category=category)
    
    async def verify_structure(self, guild: discord.Guild) -> dict:
        """Verify server structure and report missing elements"""
        report = {
            "missing_categories": [],
            "missing_text_channels": [],
            "missing_voice_channels": []
        }
        
        for category_name, structure in self.SERVER_STRUCTURE.items():
            category = discord.utils.get(guild.categories, name=category_name)
            
            if not category:
                report["missing_categories"].append(category_name)
                continue
            
            # Check text channels
            for channel_name in structure.get("channels", []):
                if not discord.utils.get(guild.channels, name=channel_name, category=category):
                    report["missing_text_channels"].append(f"{category_name}/{channel_name}")
            
            # Check voice channels
            for voice_name in structure.get("voice", []):
                if not discord.utils.get(guild.channels, name=voice_name, category=category):
                    report["missing_voice_channels"].append(f"{category_name}/{voice_name}")
        
        # Check voice-transcripts
        system_category = discord.utils.get(guild.categories, name="🧠 SYSTEM")
        if system_category:
            if not discord.utils.get(guild.channels, name=self.VOICE_TRANSCRIPTS_CHANNEL):
                report["missing_text_channels"].append(f"🧠 SYSTEM/{self.VOICE_TRANSCRIPTS_CHANNEL}")
        
        return report
    
    async def print_structure_report(self, guild: discord.Guild):
        """Print current server structure"""
        logger.info("=== SERVER STRUCTURE REPORT ===")
        logger.info(f"Guild: {guild.name}")
        logger.info(f"Total Categories: {len(guild.categories)}")
        logger.info(f"Total Text Channels: {len([c for c in guild.channels if isinstance(c, discord.TextChannel)])}")
        logger.info(f"Total Voice Channels: {len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])}")
        
        for category in guild.categories:
            logger.info(f"\n📁 {category.name}")
            
            text_channels = [c for c in category.channels if isinstance(c, discord.TextChannel)]
            voice_channels = [c for c in category.channels if isinstance(c, discord.VoiceChannel)]
            
            if text_channels:
                logger.info("  Text Channels:")
                for channel in text_channels:
                    logger.info(f"    • #{channel.name}")
            
            if voice_channels:
                logger.info("  Voice Channels:")
                for channel in voice_channels:
                    logger.info(f"    🔊 {channel.name}")


# Standalone script for server setup
async def main():
    """Run server setup as standalone script"""
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        logger.error("DISCORD_BOT_TOKEN not set")
        return
    
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    setup_manager = ServerSetup(bot)
    
    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user}")
        
        # Get first guild (assumes bot is only in one server)
        guild = bot.guilds[0] if bot.guilds else None
        if not guild:
            logger.error("Bot is not in any guilds")
            await bot.close()
            return
        
        logger.info(f"Working with guild: {guild.name}")
        
        # Print current structure
        await setup_manager.print_structure_report(guild)
        
        # Verify structure
        report = await setup_manager.verify_structure(guild)
        
        if any(report.values()):
            logger.info("\n=== MISSING ELEMENTS ===")
            if report["missing_categories"]:
                logger.info(f"Missing Categories: {report['missing_categories']}")
            if report["missing_text_channels"]:
                logger.info(f"Missing Text Channels: {report['missing_text_channels']}")
            if report["missing_voice_channels"]:
                logger.info(f"Missing Voice Channels: {report['missing_voice_channels']}")
            
            # Ask to create missing elements
            logger.info("\nCreating missing elements...")
            await setup_manager.setup_server(guild)
        else:
            logger.info("\n✅ Server structure is complete!")
        
        await bot.close()
    
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

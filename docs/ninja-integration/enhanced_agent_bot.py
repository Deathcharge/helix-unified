"""
Enhanced Discord Bot with Anthropic Claude integration and modern features
"""
import asyncio
import json
import logging
import os
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional

import discord
from discord.ext import commands
from discord_commands import EnhancedDiscordCommands
from monitoring.performance_dashboard import performance_monitor
from utils.channel_manager import initialize_channel_manager
from utils.claude_integration import claude_integration
from utils.error_handlers import DiscordError, error_boundary, error_tracker
# Import enhanced utilities
from utils.logging_config import get_logger
from utils.rate_limiter import discord_rate_limit
from utils.tts_system import tts_system

logger = get_logger('enhanced_agent_bot')

class EnhancedAgentBot(commands.Bot):
    """Enhanced Discord bot with Anthropic Claude integration and modern features"""
    
    def __init__(self, config: Dict[str, Any]):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix=config.get('prefix', '!'),
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.id = config.get('id', 'enhanced_bot')
        self.name = config.get('name', 'Enhanced Helix Bot')
        self.personality = config.get('personality', 'friendly')
        
        # Initialize enhanced components
        self.claude = claude_integration
        self.tts = tts_system
        self.command_system = None
        self.channel_manager = None
        
        # Performance tracking
        self.message_count = 0
        self.command_count = 0
        self.response_count = 0
        self.error_count = 0
        
        # Activity tracking
        self.last_activity = None
        self.start_time = datetime.utcnow()
        
        # Agent configurations
        self.agents = {}
        self.load_agent_configurations()
    
    def load_agent_configurations(self):
        """Load agent configurations from file"""
        
        config_file = "config/agents.json"
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    agent_configs = json.load(f)
                
                for agent_id, agent_config in agent_configs.items():
                    self.agents[agent_id] = EnhancedAgent(self, agent_config)
                
                logger.info(f"Loaded {len(self.agents)} agent configurations")
        except Exception as e:
            logger.error(f"Failed to load agent configurations: {e}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        
        logger.info(f"{self.user.name} has connected to Discord!")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        
        # Initialize enhanced systems
        self.command_system = EnhancedDiscordCommands(self)
        self.channel_manager = initialize_channel_manager(self)
        
        # Sync commands
        await self.command_system.sync_commands()
        
        # Setup channels for each guild
        for guild in self.guilds:
            await self.setup_guild_channels(guild)
        
        # Log system status
        await self.log_system_status()
        
        logger.info("Enhanced bot initialization complete!")
    
    async def setup_guild_channels(self, guild: discord.Guild):
        """Setup standard channels for a guild"""
        
        try:
            result = await self.channel_manager.setup_all_channels(guild)
            
            if result['success']:
                logger.info(f"Successfully setup channels for {guild.name}")
            else:
                logger.warning(f"Partial channel setup for {guild.name}: {result['successful_count']}/{result['total_count']}")
                
        except Exception as e:
            logger.error(f"Failed to setup channels for {guild.name}: {e}")
    
    async def on_message(self, message: discord.Message):
        """Handle incoming messages with enhanced processing"""
        
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Update activity
        self.last_activity = datetime.utcnow()
        self.message_count += 1
        
        # Update performance monitor
        performance_monitor.increment_counters(messages=1)
        
        try:
            # Check if message is a command
            if message.content.startswith(self.command_prefix):
                await self.process_commands(message)
                return
            
            # Process message with AI agents
            await self.process_ai_message(message)
            
        except Exception as e:
            self.error_count += 1
            error_tracker.track_error(e, {
                'message_type': 'on_message',
                'author_id': message.author.id,
                'channel_id': message.channel.id
            })
            logger.error(f"Error processing message: {e}")
    
    @error_boundary(log_error=True)
    async def process_ai_message(self, message: discord.Message):
        """Process message with AI agents"""
        
        # Check if message is in a channel where bot should respond
        if not self.should_respond_in_channel(message.channel):
            return
        
        # Get active agents for this guild
        guild_id = message.guild.id if message.guild else 'dm'
        active_agents = [agent for agent in self.agents.values() if agent.is_active]
        
        if not active_agents:
            return
        
        # Select agent based on channel or random
        selected_agent = self.select_agent_for_message(message, active_agents)
        
        if not selected_agent:
            return
        
        # Generate response using Anthropic Claude
        start_time = datetime.utcnow()
        
        claude_result = await self.claude.generate_response(
            message=message.content,
            personality=selected_agent.personality,
            context={
                'channel_name': message.channel.name,
                'guild_name': message.guild.name if message.guild else 'DM',
                'user_name': message.author.display_name
            }
        )
        
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        if claude_result['success']:
            # Send response
            await self.send_agent_response(message.channel, claude_result['response'], selected_agent)
            
            # Update stats
            selected_agent.response_count += 1
            self.response_count += 1
            
            # Log interaction
            logger.info(f"AI response generated in {response_time:.2f}ms", extra={
                'agent_id': selected_agent.id,
                'personality': selected_agent.personality,
                'message_length': len(message.content),
                'response_length': len(claude_result['response'])
            })
            
        else:
            # Use fallback response
            fallback = claude_result.get('fallback_response', "I'm having trouble responding right now. Please try again later.")
            await message.channel.send(fallback)
            
            logger.warning(f"Used fallback response due to Claude error: {claude_result.get('error')}")
    
    def should_respond_in_channel(self, channel: discord.TextChannel) -> bool:
        """Check if bot should respond in this channel"""
        
        # Don't respond in certain channels
        ignore_channels = ['rules', 'announcements', 'bot-commands']
        
        if channel.name.lower() in ignore_channels:
            return False
        
        # Respond in most other channels
        return True
    
    def select_agent_for_message(self, message: discord.Message, agents: List) -> Optional['EnhancedAgent']:
        """Select appropriate agent for message"""
        
        # Simple selection logic - can be enhanced
        if agents:
            return agents[0]  # Use first active agent
        
        return None
    
    async def send_agent_response(
        self, 
        channel: discord.TextChannel, 
        response: str, 
        agent: 'EnhancedAgent'
    ):
        """Send agent response with appropriate formatting"""
        
        # Create embed with agent info
        embed = discord.Embed(
            description=response,
            color=discord.Color.blue()
        )
        
        embed.set_author(
            name=f"{agent.name} ({agent.personality})",
            icon_url=self.user.avatar.url if self.user.avatar else None
        )
        
        embed.set_footer(text=f"Response time: {datetime.utcnow().strftime('%H:%M:%S')}")
        
        await channel.send(embed=embed)
    
    @discord_rate_limit(command_type="general")
    async def process_commands(self, message: discord.Message):
        """Process traditional commands (legacy support)"""
        
        # Extract command and args
        content = message.content[len(self.command_prefix):].strip()
        if not content:
            return
        
        parts = content.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        self.command_count += 1
        performance_monitor.increment_counters(commands=1)
        
        # Handle legacy commands
        if command == 'seed':
            await self.handle_seed_command(message, args)
        elif command == 'ping':
            await self.handle_ping_command(message)
        elif command == 'help':
            await self.handle_help_command(message, args)
    
    async def handle_seed_command(self, message: discord.Message, args: List[str]):
        """Enhanced seed command with channel setup"""
        
        if not message.guild or not message.author.guild_permissions.manage_channels:
            await message.channel.send("You need `Manage Channels` permission to use this command.")
            return
        
        await message.channel.send("🌱 Setting up server channels...")
        
        try:
            # Setup all channels
            result = await self.channel_manager.setup_all_channels(message.guild)
            
            if result['success']:
                embed = discord.Embed(
                    title="✅ Server Setup Complete",
                    description=f"Successfully created {result['successful_count']} channels with pinned messages!",
                    color=discord.Color.green()
                )
                
                for channel_type, channel_result in result['results'].items():
                    if channel_result['success']:
                        embed.add_field(
                            name=f"✅ {channel_type.title()}",
                            value="Setup successful",
                            inline=True
                        )
                    else:
                        embed.add_field(
                            name=f"❌ {channel_type.title()}",
                            value=channel_result.get('error', 'Setup failed'),
                            inline=True
                        )
            else:
                embed = discord.Embed(
                    title="⚠️ Partial Server Setup",
                    description=f"Setup {result['successful_count']}/{result['total_count']} channels successfully.",
                    color=discord.Color.orange()
                )
            
            await message.channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Seed command failed: {e}")
            await message.channel.send(f"❌ Setup failed: {str(e)}")
    
    async def handle_ping_command(self, message: discord.Message):
        """Handle ping command"""
        
        latency = round(self.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.green() if latency < 100 else discord.Color.orange()
        )
        
        await message.channel.send(embed=embed)
    
    async def handle_help_command(self, message: discord.Message, args: List[str]):
        """Handle help command"""
        
        embed = discord.Embed(
            title="🚀 Enhanced Bot Help",
            description="Use slash commands (`/`) for the best experience!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Slash Commands",
            value="• `/help` - Show all commands\n"
                  "• `/agents` - List AI agents\n"
                  "• `/status` - System status\n"
                  "• `/join` - Join voice channel\n"
                  "• `/speak <text>` - Text-to-speech\n"
                  "• `/webhook <action>` - Manage webhooks",
            inline=False
        )
        
        embed.add_field(
            name="Legacy Commands",
            value="• `!seed` - Setup server channels\n"
                  "• `!ping` - Check latency\n"
                  "• `!help` - Show this help",
            inline=False
        )
        
        embed.add_field(
            name="AI Features",
            value="• Chat with AI agents in any channel\n"
                  "• Different personalities available\n"
                  "• Context-aware responses\n"
                  "• Anthropic Claude integration",
            inline=False
        )
        
        await message.channel.send(embed=embed)
    
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Handle voice state updates for TTS features"""
        
        # Update voice patrol system if needed
        if after.channel and before.channel != after.channel:
            logger.info(f"User {member.name} joined voice channel {after.channel.name}")
    
    async def on_guild_join(self, guild: discord.Guild):
        """Handle joining a new guild"""
        
        logger.info(f"Joined new guild: {guild.name}")
        
        # Setup channels for new guild
        await self.setup_guild_channels(guild)
        
        # Send welcome message to default channel
        welcome_channel = guild.system_channel or guild.text_channels[0] if guild.text_channels else None
        
        if welcome_channel:
            embed = discord.Embed(
                title="🎉 Thanks for inviting me!",
                description="I'm an enhanced AI bot with Anthropic Claude integration. Use `/help` to see all available commands!",
                color=discord.Color.green()
            )
            
            await welcome_channel.send(embed=embed)
    
    async def on_error(self, event_method: str, *args, **kwargs):
        """Handle bot errors"""
        
        logger.error(f"Bot error in {event_method}: {traceback.format_exc()}")
        self.error_count += 1
        error_tracker.track_error(Exception(f"Bot error in {event_method}"))
    
    async def reload_config(self):
        """Reload bot configuration"""
        
        try:
            self.load_agent_configurations()
            logger.info("Configuration reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")
            raise
    
    async def log_system_status(self):
        """Log comprehensive system status"""
        
        status = {
            'bot_id': self.id,
            'bot_name': self.name,
            'guilds_count': len(self.guilds),
            'agents_count': len(self.agents),
            'active_agents': sum(1 for agent in self.agents.values() if agent.is_active),
            'claude_available': self.claude.is_available(),
            'tts_providers': list(self.tts.get_available_providers().keys()),
            'uptime_seconds': (datetime.utcnow() - self.start_time).total_seconds(),
            'messages_processed': self.message_count,
            'commands_executed': self.command_count,
            'responses_generated': self.response_count,
            'errors_encountered': self.error_count
        }
        
        logger.info(f"System status: {json.dumps(status, indent=2)}")
        
        return status
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        
        return {
            'id': self.id,
            'name': self.name,
            'personality': self.personality,
            'is_active': True,
            'uptime_seconds': (datetime.utcnow() - self.start_time).total_seconds(),
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'message_count': self.message_count,
            'command_count': self.command_count,
            'response_count': self.response_count,
            'error_count': self.error_count,
            'guilds_count': len(self.guilds),
            'agents_count': len(self.agents),
            'claude_available': self.claude.is_available()
        }

class EnhancedAgent:
    """Enhanced agent with Anthropic Claude integration"""
    
    def __init__(self, bot: EnhancedAgentBot, config: Dict[str, Any]):
        self.bot = bot
        self.id = config.get('id')
        self.name = config.get('name')
        self.personality = config.get('personality', 'friendly')
        self.is_active = config.get('is_active', True)
        self.response_count = 0
        self.uptime_seconds = 0

async def main():
    """Main function to run the enhanced bot"""
    
    # Load configuration
    bot_config = {
        'id': os.getenv('BOT_ID', 'enhanced_helix_bot'),
        'name': os.getenv('BOT_NAME', 'Enhanced Helix Bot'),
        'personality': os.getenv('BOT_PERSONALITY', 'friendly'),
        'prefix': os.getenv('DISCORD_PREFIX', '!'),
        'token': os.getenv('DISCORD_BOT_TOKEN')
    }
    
    if not bot_config['token']:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return
    
    # Create and run bot
    bot = EnhancedAgentBot(bot_config)
    
    try:
        await bot.start(bot_config['token'])
    except discord.LoginFailure:
        logger.error("Invalid Discord bot token")
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
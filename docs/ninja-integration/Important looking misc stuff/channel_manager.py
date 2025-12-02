"""
Enhanced Discord channel management with pinned message support and advanced features
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
import discord
from datetime import datetime, timedelta
import json
import os

logger = logging.getLogger(__name__)

class ChannelManager:
    """Advanced Discord channel management system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.channel_configs = {}
        self.pinned_message_templates = {}
        self.channel_stats = {}
        self.auto_channels = {}
        
        # Load channel configurations
        self._load_channel_configs()
        self._load_pinned_templates()
    
    def _load_channel_configs(self):
        """Load channel configurations from file"""
        
        config_file = "config/channel_configs.json"
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.channel_configs = json.load(f)
                logger.info(f"Loaded {len(self.channel_configs)} channel configurations")
        except Exception as e:
            logger.error(f"Failed to load channel configs: {e}")
            self.channel_configs = {}
    
    def _load_pinned_templates(self):
        """Load pinned message templates"""
        
        self.pinned_message_templates = {
            'welcome': {
                'title': '👋 Welcome to {guild_name}!',
                'description': 'Welcome to our community! Here are some things to know:\n\n'
                              '📜 **Rules:** Be respectful and follow our community guidelines\n'
                              '🎮 **Roles:** Assign yourself roles in the #roles channel\n'
                              '💬 **Chat:** Join conversations and make new friends\n'
                              '🤖 **Bot:** Use `/help` to see all available commands\n\n'
                              'If you need help, ask an admin or moderator!',
                'color': discord.Color.blue(),
                'footer': 'Welcome message'
            },
            'rules': {
                'title': '📜 Server Rules',
                'description': 'Please follow these rules to maintain a positive community:\n\n'
                              '1. **Be Respectful** - No harassment or hate speech\n'
                              '2. **No Spam** - Keep conversations relevant\n'
                              '3. **Appropriate Content** - Keep it SFW\n'
                              '4. **Voice Channel Etiquette** - Be respectful in voice\n'
                              '5. **Follow Discord ToS** - No violations of Discord\'s terms\n\n'
                              '**Violations may result in warnings, kicks, or bans.**',
                'color': discord.Color.red(),
                'footer': 'Server rules - Last updated'
            },
            'roles': {
                'title': '🎭 Role Assignment',
                'description': 'Assign yourself roles using these reactions:\n\n'
                              '🎮 **Gamer** - For gaming discussions\n'
                              '🎨 **Artist** - Share your creative work\n'
                              '🎵 **Musician** - Music and audio enthusiasts\n'
                              '💻 **Developer** - Programming and tech talk\n'
                              '📚 **Student** - Academic discussions\n'
                              '🌟 **VIP** - Special member perks\n\n'
                              'Simply react to this message with the emoji that matches your interests!',
                'color': discord.Color.purple(),
                'footer': 'React with emojis to get roles'
            },
            'announcement': {
                'title': '📢 Announcements',
                'description': 'Important server announcements will be posted here.\n\n'
                              '💡 **Tip:** Enable notification for this channel to stay updated!\n\n'
                              'Current status: All systems operational ✅',
                'color': discord.Color.gold(),
                'footer': 'Official announcements'
            },
            'bot_info': {
                'title': '🤖 Helix Unified Bot',
                'description': 'Welcome to Helix Unified - your AI-powered Discord assistant!\n\n'
                              '**Available Commands:**\n'
                              '`/help` - Show all available commands\n'
                              '`/agents` - List active AI agents\n'
                              '`/status` - Check system status\n'
                              '`/join` - Join voice channel\n'
                              '`/speak <text>` - Text-to-speech in voice\n\n'
                              '**Features:**\n'
                              '• Multi-agent AI conversations\n'
                              '• Voice channel management\n'
                              '• Advanced moderation tools\n'
                              '• Webhook integrations\n'
                              '• Performance monitoring\n\n'
                              'Use `/help <category>` for detailed help!',
                'color': discord.Color.green(),
                'footer': 'Bot information and commands'
            }
        }
    
    async def create_pinned_message(
        self, 
        channel: discord.TextChannel, 
        template_name: str,
        custom_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create and pin a message using a template"""
        
        template = self.pinned_message_templates.get(template_name)
        if not template:
            return {
                'success': False,
                'error': f'Template {template_name} not found'
            }
        
        try:
            # Format the template with variables
            title = template['title'].format(
                guild_name=channel.guild.name,
                channel_name=channel.name,
                **(custom_vars or {})
            )
            
            description = template['description'].format(
                guild_name=channel.guild.name,
                channel_name=channel.name,
                **(custom_vars or {})
            )
            
            # Create embed
            embed = discord.Embed(
                title=title,
                description=description,
                color=template['color'],
                timestamp=datetime.utcnow()
            )
            
            embed.set_footer(text=template['footer'])
            embed.set_thumbnail(url=channel.guild.icon.url if channel.guild.icon else None)
            
            # Send message
            message = await channel.send(embed=embed)
            
            # Pin the message
            await message.pin()
            
            logger.info(f"Created pinned message in {channel.name} using template {template_name}")
            
            return {
                'success': True,
                'message_id': message.id,
                'template_used': template_name,
                'channel_id': channel.id
            }
            
        except Exception as e:
            logger.error(f"Failed to create pinned message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def update_pinned_message(
        self,
        channel: discord.TextChannel,
        message_id: int,
        template_name: str,
        custom_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Update an existing pinned message"""
        
        try:
            # Get the message
            message = await channel.fetch_message(message_id)
            
            if not message.pinned:
                return {
                    'success': False,
                    'error': 'Message is not pinned'
                }
            
            # Get template
            template = self.pinned_message_templates.get(template_name)
            if not template:
                return {
                    'success': False,
                    'error': f'Template {template_name} not found'
                }
            
            # Format new embed
            title = template['title'].format(
                guild_name=channel.guild.name,
                channel_name=channel.name,
                **(custom_vars or {})
            )
            
            description = template['description'].format(
                guild_name=channel.guild.name,
                channel_name=channel.name,
                **(custom_vars or {})
            )
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=template['color'],
                timestamp=datetime.utcnow()
            )
            
            embed.set_footer(text=template['footer'])
            embed.set_thumbnail(url=channel.guild.icon.url if channel.guild.icon else None)
            
            # Edit the message
            await message.edit(embed=embed)
            
            logger.info(f"Updated pinned message {message_id} in {channel.name}")
            
            return {
                'success': True,
                'message_id': message_id,
                'template_used': template_name
            }
            
        except discord.NotFound:
            return {
                'success': False,
                'error': 'Message not found'
            }
        except Exception as e:
            logger.error(f"Failed to update pinned message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def setup_welcome_channel(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup welcome channel with pinned messages"""
        
        # Find or create welcome channel
        welcome_channel = discord.utils.get(guild.text_channels, name='welcome')
        
        if not welcome_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    read_message_history=True
                ),
                guild.me: discord.PermissionOverwrite(
                    manage_messages=True,
                    manage_channels=True
                )
            }
            
            welcome_channel = await guild.create_text_channel(
                'welcome',
                overwrites=overwrites,
                topic='Welcome new members and server information'
            )
        
        # Create welcome pinned message
        result = await self.create_pinned_message(welcome_channel, 'welcome')
        
        if result['success']:
            logger.info(f"Setup welcome channel for guild {guild.name}")
        
        return result
    
    async def setup_rules_channel(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup rules channel with pinned messages"""
        
        # Find or create rules channel
        rules_channel = discord.utils.get(guild.text_channels, name='rules')
        
        if not rules_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=False  # Read-only for members
                ),
                guild.me: discord.PermissionOverwrite(
                    manage_messages=True,
                    manage_channels=True,
                    send_messages=True
                )
            }
            
            rules_channel = await guild.create_text_channel(
                'rules',
                overwrites=overwrites,
                topic='Server rules and guidelines'
            )
        
        # Create rules pinned message
        result = await self.create_pinned_message(rules_channel, 'rules')
        
        if result['success']:
            logger.info(f"Setup rules channel for guild {guild.name}")
        
        return result
    
    async def setup_roles_channel(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup roles channel with self-assignable roles"""
        
        # Find or create roles channel
        roles_channel = discord.utils.get(guild.text_channels, name='roles')
        
        if not roles_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=False,  # Only react, don't type
                    add_reactions=True
                ),
                guild.me: discord.PermissionOverwrite(
                    manage_messages=True,
                    manage_channels=True,
                    send_messages=True,
                    manage_roles=True
                )
            }
            
            roles_channel = await guild.create_text_channel(
                'roles',
                overwrites=overwrites,
                topic='Assign yourself roles using reactions'
            )
        
        # Create roles pinned message
        result = await self.create_pinned_message(roles_channel, 'roles')
        
        if result['success']:
            # Add reactions for role assignment
            message_id = result['message_id']
            message = await roles_channel.fetch_message(message_id)
            
            role_emojis = ['🎮', '🎨', '🎵', '💻', '📚', '🌟']
            
            for emoji in role_emojis:
                await message.add_reaction(emoji)
            
            logger.info(f"Setup roles channel for guild {guild.name}")
        
        return result
    
    async def setup_announcement_channel(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup announcements channel"""
        
        # Find or create announcements channel
        announce_channel = discord.utils.get(guild.text_channels, name='announcements')
        
        if not announce_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=False  # Read-only for members
                ),
                guild.me: discord.PermissionOverwrite(
                    manage_messages=True,
                    manage_channels=True,
                    send_messages=True,
                    mention_everyone=True
                )
            }
            
            announce_channel = await guild.create_text_channel(
                'announcements',
                overwrites=overwrites,
                topic='Official server announcements'
            )
        
        # Create announcement pinned message
        result = await self.create_pinned_message(announce_channel, 'announcement')
        
        if result['success']:
            logger.info(f"Setup announcements channel for guild {guild.name}")
        
        return result
    
    async def setup_bot_channel(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup bot information channel"""
        
        # Find or create bot channel
        bot_channel = discord.utils.get(guild.text_channels, name='bot-commands')
        
        if not bot_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True
                ),
                guild.me: discord.PermissionOverwrite(
                    manage_messages=True,
                    manage_channels=True
                )
            }
            
            bot_channel = await guild.create_text_channel(
                'bot-commands',
                overwrites=overwrites,
                topic='Bot commands and information'
            )
        
        # Create bot info pinned message
        result = await self.create_pinned_message(bot_channel, 'bot_info')
        
        if result['success']:
            logger.info(f"Setup bot channel for guild {guild.name}")
        
        return result
    
    async def setup_all_channels(self, guild: discord.Guild) -> Dict[str, Any]:
        """Setup all standard channels for a guild"""
        
        results = {}
        
        # Setup each channel type
        results['welcome'] = await self.setup_welcome_channel(guild)
        results['rules'] = await self.setup_rules_channel(guild)
        results['roles'] = await self.setup_roles_channel(guild)
        results['announcements'] = await self.setup_announcement_channel(guild)
        results['bot_commands'] = await self.setup_bot_channel(guild)
        
        # Count successful setups
        successful = sum(1 for result in results.values() if result['success'])
        total = len(results)
        
        logger.info(f"Completed channel setup for {guild.name}: {successful}/{total} successful")
        
        return {
            'success': successful == total,
            'successful_count': successful,
            'total_count': total,
            'results': results
        }
    
    async def cleanup_old_pins(self, channel: discord.TextChannel, keep_count: int = 5) -> Dict[str, Any]:
        """Clean up old pinned messages, keeping only the most recent ones"""
        
        try:
            # Get all pinned messages
            pinned_messages = await channel.pins()
            
            if len(pinned_messages) <= keep_count:
                return {
                    'success': True,
                    'cleaned_count': 0,
                    'message': 'No cleanup needed'
                }
            
            # Sort by creation time (newest first)
            pinned_messages.sort(key=lambda m: m.created_at, reverse=True)
            
            # Unpin older messages
            messages_to_unpin = pinned_messages[keep_count:]
            cleaned_count = 0
            
            for message in messages_to_unpin:
                await message.unpin()
                cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old pins from {channel.name}")
            
            return {
                'success': True,
                'cleaned_count': cleaned_count,
                'remaining_count': len(pinned_messages) - cleaned_count
            }
            
        except Exception as e:
            logger.error(f"Failed to cleanup pins in {channel.name}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_channel_stats(self, channel: discord.TextChannel) -> Dict[str, Any]:
        """Get comprehensive statistics for a channel"""
        
        try:
            # Get message count (last 100 messages for quick stats)
            messages = []
            async for message in channel.history(limit=100):
                messages.append(message)
            
            # Analyze messages
            user_messages = len([m for m in messages if not m.author.bot])
            bot_messages = len([m for m in messages if m.author.bot])
            
            # Get pinned count
            pinned_count = len(await channel.pins())
            
            # Calculate activity
            if messages:
                oldest_message = messages[-1].created_at
                newest_message = messages[0].created_at
                time_span = (newest_message - oldest_message).total_seconds()
                activity_rate = len(messages) / (time_span / 3600) if time_span > 0 else 0  # messages per hour
            else:
                activity_rate = 0
            
            stats = {
                'channel_name': channel.name,
                'channel_id': channel.id,
                'total_messages_recent': len(messages),
                'user_messages': user_messages,
                'bot_messages': bot_messages,
                'pinned_messages': pinned_count,
                'activity_rate_per_hour': round(activity_rate, 2),
                'member_count': len(channel.members),
                'nsfw': channel.is_nsfw(),
                'topic': channel.topic or 'No topic set',
                'created_at': channel.created_at.isoformat(),
                'slowmode_delay': channel.slowmode_delay
            }
            
            return {
                'success': True,
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel stats for {channel.name}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_custom_template(self, name: str, template: Dict[str, Any]):
        """Add a custom pinned message template"""
        
        self.pinned_message_templates[name] = template
        logger.info(f"Added custom template: {name}")
        
        # Save to file (optional)
        try:
            os.makedirs('config', exist_ok=True)
            with open('config/custom_templates.json', 'w') as f:
                json.dump(self.pinned_message_templates, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save custom templates: {e}")
    
    def get_available_templates(self) -> List[str]:
        """Get list of available pinned message templates"""
        return list(self.pinned_message_templates.keys())

# Global channel manager instance
channel_manager = None

def initialize_channel_manager(bot):
    """Initialize the global channel manager"""
    global channel_manager
    channel_manager = ChannelManager(bot)
    return channel_manager
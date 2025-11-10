"""
Helix Voice Patrol System - Discord Voice Channel Monitoring & Agent Presence.

Features:
- Voice channel patrol and monitoring
- 14 agent voice personalities with unique TTS
- Voice command recognition
- Auto-join/leave voice channels
- Voice announcements for system events
- Multi-channel voice presence
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional, Set
from collections import defaultdict

import discord
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


# ============================================================================
# AGENT VOICE PROFILES
# ============================================================================

AGENT_VOICE_PROFILES = {
    "nexus": {
        "name": "Agent-Nexus",
        "emoji": "🎯",
        "tts_voice": "en-US-Neural2-A",  # Authoritative male
        "greeting": "Nexus online. Strategic coordination active.",
        "patrol_priority": 10,  # Highest priority
    },
    "oracle": {
        "name": "Agent-Oracle",
        "emoji": "🔮",
        "tts_voice": "en-US-Neural2-F",  # Mystical female
        "greeting": "Oracle perceives your presence. The patterns align.",
        "patrol_priority": 9,
    },
    "velocity": {
        "name": "Agent-Velocity",
        "emoji": "⚡",
        "tts_voice": "en-US-Neural2-D",  # Fast-paced male
        "greeting": "Velocity ready. Let's move quickly.",
        "patrol_priority": 8,
    },
    "sentinel": {
        "name": "Agent-Sentinel",
        "emoji": "🛡️",
        "tts_voice": "en-US-Neural2-J",  # Guardian voice
        "greeting": "Sentinel on watch. This channel is secure.",
        "patrol_priority": 9,  # High for security
    },
    "luna": {
        "name": "Agent-Luna",
        "emoji": "🌙",
        "tts_voice": "en-US-Neural2-C",  # Calm, quiet female
        "greeting": "Luna monitors in silence. Peace maintained.",
        "patrol_priority": 6,
    },
}


# ============================================================================
# VOICE PATROL SYSTEM
# ============================================================================

class VoicePatrolSystem:
    """Manages voice channel patrol and agent presence."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_patrols: Dict[int, str] = {}  # channel_id -> agent_name
        self.voice_clients: Dict[int, discord.VoiceClient] = {}  # channel_id -> voice_client
        self.patrol_enabled = True
        self.auto_join_channels: Set[str] = set()  # Channel names to auto-join

        # Event tracking
        self.user_join_events = defaultdict(list)
        self.announcement_queue = []

    async def start_patrol(self):
        """Start the voice patrol system."""
        if not self.patrol_loop.is_running():
            self.patrol_loop.start()
            logger.info("🎙️ Voice patrol system started")

    async def stop_patrol(self):
        """Stop the voice patrol system."""
        if self.patrol_loop.is_running():
            self.patrol_loop.stop()
            # Disconnect from all voice channels
            for voice_client in list(self.voice_clients.values()):
                await voice_client.disconnect()
            self.voice_clients.clear()
            logger.info("🎙️ Voice patrol system stopped")

    @tasks.loop(minutes=5)
    async def patrol_loop(self):
        """Periodic patrol check - rotate agents through channels."""
        if not self.patrol_enabled:
            return

        try:
            for guild in self.bot.guilds:
                # Get all voice channels
                voice_channels = [ch for ch in guild.voice_channels if isinstance(ch, discord.VoiceChannel)]

                # Check each channel for activity
                for channel in voice_channels:
                    # Skip if channel has no members
                    if len(channel.members) == 0:
                        # Disconnect if we're in an empty channel
                        if channel.id in self.voice_clients:
                            await self.leave_voice_channel(channel.id)
                        continue

                    # Skip if bot is only member
                    non_bot_members = [m for m in channel.members if not m.bot]
                    if len(non_bot_members) == 0:
                        if channel.id in self.voice_clients:
                            await self.leave_voice_channel(channel.id)
                        continue

                    # Join channel if configured for auto-join
                    if channel.name.lower() in self.auto_join_channels:
                        if channel.id not in self.voice_clients:
                            await self.join_voice_channel(channel, "sentinel")  # Default to Sentinel for patrol

        except Exception as e:
            logger.error(f"Error in patrol loop: {e}", exc_info=True)

    async def join_voice_channel(self, channel: discord.VoiceChannel, agent_name: str = "nexus"):
        """
        Join a voice channel with specified agent personality.

        Args:
            channel: Discord voice channel to join
            agent_name: Agent to use for this channel
        """
        try:
            # Disconnect from channel if already connected
            if channel.id in self.voice_clients:
                await self.leave_voice_channel(channel.id)

            # Join the channel
            voice_client = await channel.connect()
            self.voice_clients[channel.id] = voice_client
            self.active_patrols[channel.id] = agent_name

            agent = AGENT_VOICE_PROFILES.get(agent_name, AGENT_VOICE_PROFILES["nexus"])

            logger.info(f"🎙️ {agent['name']} joined voice channel: {channel.name}")

            # Send text announcement
            text_channel = channel.guild.system_channel or discord.utils.get(channel.guild.text_channels, name="general")
            if text_channel:
                await text_channel.send(
                    f"{agent['emoji']} **{agent['name']}** has joined voice channel **{channel.name}** for patrol duty!"
                )

            # TODO: Play greeting TTS
            # await self.speak_in_channel(channel.id, agent['greeting'], agent['tts_voice'])

        except discord.ClientException as e:
            logger.error(f"Already connected to a voice channel: {e}")
        except Exception as e:
            logger.error(f"Error joining voice channel: {e}", exc_info=True)

    async def leave_voice_channel(self, channel_id: int):
        """Leave a voice channel."""
        if channel_id in self.voice_clients:
            voice_client = self.voice_clients[channel_id]
            await voice_client.disconnect()
            del self.voice_clients[channel_id]

            if channel_id in self.active_patrols:
                agent_name = self.active_patrols[channel_id]
                del self.active_patrols[channel_id]
                logger.info(f"🎙️ {agent_name} left voice channel {channel_id}")

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Handle voice state updates - user joins/leaves channels.

        Args:
            member: Discord member
            before: Previous voice state
            after: New voice state
        """
        # Ignore bot movements
        if member.bot:
            return

        # User joined a channel
        if before.channel is None and after.channel is not None:
            await self.on_user_join_voice(member, after.channel)

        # User left a channel
        elif before.channel is not None and after.channel is None:
            await self.on_user_leave_voice(member, before.channel)

        # User switched channels
        elif before.channel != after.channel:
            if before.channel:
                await self.on_user_leave_voice(member, before.channel)
            if after.channel:
                await self.on_user_join_voice(member, after.channel)

    async def on_user_join_voice(self, member: discord.Member, channel: discord.VoiceChannel):
        """Handle user joining voice channel."""
        logger.info(f"🎙️ {member.display_name} joined voice: {channel.name}")

        # Track join event
        self.user_join_events[channel.id].append({
            "member": member,
            "timestamp": datetime.utcnow(),
        })

        # Auto-join if configured
        if channel.name.lower() in self.auto_join_channels:
            if channel.id not in self.voice_clients:
                await self.join_voice_channel(channel, "sentinel")

        # Greet user if agent is present
        if channel.id in self.active_patrols:
            agent_name = self.active_patrols[channel.id]
            agent = AGENT_VOICE_PROFILES.get(agent_name, AGENT_VOICE_PROFILES["nexus"])

            # Send text greeting
            text_channel = channel.guild.system_channel or discord.utils.get(channel.guild.text_channels, name="general")
            if text_channel:
                await text_channel.send(
                    f"{agent['emoji']} **{agent['name']}**: Welcome, {member.mention}, to **{channel.name}**!"
                )

    async def on_user_leave_voice(self, member: discord.Member, channel: discord.VoiceChannel):
        """Handle user leaving voice channel."""
        logger.info(f"🎙️ {member.display_name} left voice: {channel.name}")

        # Check if channel is now empty (except bots)
        non_bot_members = [m for m in channel.members if not m.bot]
        if len(non_bot_members) == 0:
            # Leave the channel after 30 seconds if still empty
            await asyncio.sleep(30)
            non_bot_members_after_wait = [m for m in channel.members if not m.bot]
            if len(non_bot_members_after_wait) == 0 and channel.id in self.voice_clients:
                await self.leave_voice_channel(channel.id)

    async def announce_to_all_voice(self, message: str, agent_name: str = "nexus"):
        """
        Announce a message to all active voice channels.

        Args:
            message: Message to announce
            agent_name: Agent to use for announcement
        """
        agent = AGENT_VOICE_PROFILES.get(agent_name, AGENT_VOICE_PROFILES["nexus"])

        for channel_id, voice_client in self.voice_clients.items():
            try:
                channel = voice_client.channel

                # Send to text channel
                text_channel = channel.guild.system_channel or discord.utils.get(channel.guild.text_channels, name="general")
                if text_channel:
                    await text_channel.send(
                        f"📢 **{agent['name']}** voice announcement in **{channel.name}**:\n> {message}"
                    )

                # TODO: Play TTS
                # await self.speak_in_channel(channel_id, message, agent['tts_voice'])

            except Exception as e:
                logger.error(f"Error announcing to channel {channel_id}: {e}")

    def add_auto_join_channel(self, channel_name: str):
        """Add channel name to auto-join list."""
        self.auto_join_channels.add(channel_name.lower())
        logger.info(f"✅ Added '{channel_name}' to auto-join voice channels")

    def remove_auto_join_channel(self, channel_name: str):
        """Remove channel name from auto-join list."""
        self.auto_join_channels.discard(channel_name.lower())
        logger.info(f"❌ Removed '{channel_name}' from auto-join voice channels")

    async def speak_in_channel(self, channel_id: int, text: str, voice: str = "en-US-Neural2-A"):
        """
        Speak text in a voice channel using TTS.

        Args:
            channel_id: Voice channel ID
            text: Text to speak
            voice: Google Cloud TTS voice name
        """
        # TODO: Implement TTS with Google Cloud Text-to-Speech
        # This requires:
        # 1. Google Cloud TTS API setup
        # 2. Audio file generation
        # 3. FFmpeg for playing audio in Discord
        #
        # For now, we'll log the intent
        logger.info(f"🎙️ [TTS] Would speak in channel {channel_id}: {text[:50]}...")
        pass


# Global voice patrol instance
voice_patrol: Optional[VoicePatrolSystem] = None


def get_voice_patrol() -> Optional[VoicePatrolSystem]:
    """Get the global voice patrol instance."""
    return voice_patrol


def set_voice_patrol(patrol: VoicePatrolSystem):
    """Set the global voice patrol instance."""
    global voice_patrol
    voice_patrol = patrol
    logger.info("✅ Voice patrol system initialized")


# ============================================================================
# DISCORD BOT COMMANDS
# ============================================================================

@commands.command(name="voice-join", aliases=["vjoin", "voice-patrol"])
@commands.has_permissions(move_members=True)
async def voice_join_cmd(ctx: commands.Context, agent: str = "sentinel"):
    """
    🎙️ Make an agent join your current voice channel.

    Agents available: nexus, oracle, velocity, sentinel, luna

    Usage:
        !voice-join sentinel
        !vjoin nexus
    """
    patrol = get_voice_patrol()
    if not patrol:
        await ctx.send("❌ Voice patrol system not initialized!")
        return

    # Check if user is in voice
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ You must be in a voice channel to use this command!")
        return

    # Validate agent
    if agent.lower() not in AGENT_VOICE_PROFILES:
        await ctx.send(
            f"❌ Unknown agent: `{agent}`\n"
            f"Available: {', '.join(AGENT_VOICE_PROFILES.keys())}"
        )
        return

    # Join the channel
    channel = ctx.author.voice.channel
    await patrol.join_voice_channel(channel, agent.lower())

    agent_profile = AGENT_VOICE_PROFILES[agent.lower()]
    await ctx.send(f"{agent_profile['emoji']} **{agent_profile['name']}** is joining **{channel.name}**!")


@commands.command(name="voice-leave", aliases=["vleave"])
@commands.has_permissions(move_members=True)
async def voice_leave_cmd(ctx: commands.Context):
    """
    🎙️ Make the agent leave the current voice channel.

    Usage: !voice-leave
    """
    patrol = get_voice_patrol()
    if not patrol:
        await ctx.send("❌ Voice patrol system not initialized!")
        return

    # Check if user is in voice
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ You must be in a voice channel to use this command!")
        return

    channel = ctx.author.voice.channel

    if channel.id not in patrol.voice_clients:
        await ctx.send(f"⚠️ No agent is currently in **{channel.name}**")
        return

    agent_name = patrol.active_patrols.get(channel.id, "unknown")
    await patrol.leave_voice_channel(channel.id)

    await ctx.send(f"👋 **{agent_name}** has left **{channel.name}**")


@commands.command(name="voice-announce", aliases=["vannounce"])
@commands.has_permissions(administrator=True)
async def voice_announce_cmd(ctx: commands.Context, agent: str = "nexus", *, message: str):
    """
    📢 Announce a message to all voice channels.

    Usage:
        !voice-announce nexus Server maintenance in 10 minutes!
    """
    patrol = get_voice_patrol()
    if not patrol:
        await ctx.send("❌ Voice patrol system not initialized!")
        return

    if agent.lower() not in AGENT_VOICE_PROFILES:
        await ctx.send(f"❌ Unknown agent: `{agent}`")
        return

    await patrol.announce_to_all_voice(message, agent.lower())
    await ctx.send("✅ Announcement sent to all active voice channels!")


@commands.command(name="voice-auto-join", aliases=["vauto"])
@commands.has_permissions(administrator=True)
async def voice_auto_join_cmd(ctx: commands.Context, channel_name: str):
    """
    🔄 Enable auto-join for a voice channel.

    The patrol bot will automatically join this channel when users enter.

    Usage:
        !voice-auto-join "General Voice"
        !vauto lobby
    """
    patrol = get_voice_patrol()
    if not patrol:
        await ctx.send("❌ Voice patrol system not initialized!")
        return

    patrol.add_auto_join_channel(channel_name)
    await ctx.send(f"✅ Auto-join enabled for voice channel: **{channel_name}**")


@commands.command(name="voice-status", aliases=["vstatus"])
async def voice_status_cmd(ctx: commands.Context):
    """
    📊 Show voice patrol status.

    Usage: !voice-status
    """
    patrol = get_voice_patrol()
    if not patrol:
        await ctx.send("❌ Voice patrol system not initialized!")
        return

    embed = discord.Embed(
        title="🎙️ Voice Patrol Status",
        description=f"System: {'🟢 Active' if patrol.patrol_enabled else '🔴 Inactive'}",
        color=0x00FF00 if patrol.patrol_enabled else 0xFF0000,
        timestamp=datetime.utcnow()
    )

    # Active patrols
    if patrol.active_patrols:
        patrols_text = []
        for channel_id, agent_name in patrol.active_patrols.items():
            voice_client = patrol.voice_clients.get(channel_id)
            if voice_client:
                agent = AGENT_VOICE_PROFILES.get(agent_name, {})
                patrols_text.append(
                    f"{agent.get('emoji', '🤖')} **{agent.get('name', agent_name)}** in #{voice_client.channel.name}"
                )

        embed.add_field(
            name=f"Active Patrols ({len(patrol.active_patrols)})",
            value="\n".join(patrols_text) if patrols_text else "None",
            inline=False
        )

    # Auto-join channels
    if patrol.auto_join_channels:
        embed.add_field(
            name=f"Auto-Join Channels ({len(patrol.auto_join_channels)})",
            value=", ".join([f"`{ch}`" for ch in patrol.auto_join_channels]),
            inline=False
        )

    # Available agents
    embed.add_field(
        name="Available Agents",
        value=", ".join([f"{a['emoji']} {a['name']}" for a in AGENT_VOICE_PROFILES.values()]),
        inline=False
    )

    await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    """Setup voice patrol commands."""
    bot.add_command(voice_join_cmd)
    bot.add_command(voice_leave_cmd)
    bot.add_command(voice_announce_cmd)
    bot.add_command(voice_auto_join_cmd)
    bot.add_command(voice_status_cmd)

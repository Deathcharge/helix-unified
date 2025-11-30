"""
Voice Channel Commands for Helix Agents
"""

from discord.ext import commands
import discord


class VoiceCommands(commands.Cog):
    """Commands for voice channel interaction"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="join")
    async def join_voice(self, ctx):
        """Join the voice channel you're in"""
        if not ctx.author.voice:
            await ctx.send(f"*{self.bot.personality.emoji} {self.bot.personality.name}: You're not in a voice channel*")
            return
        
        channel = ctx.author.voice.channel
        await self.bot.join_voice_channel(channel)
        await ctx.send(f"{self.bot.personality.emoji} **{self.bot.personality.name}** is now listening in {channel.name}")
    
    @commands.command(name="leave")
    async def leave_voice(self, ctx):
        """Leave the current voice channel"""
        if not self.bot.voice_client:
            await ctx.send(f"*{self.bot.personality.emoji} {self.bot.personality.name}: I'm not in a voice channel*")
            return
        
        channel_name = self.bot.voice_client.channel.name
        await self.bot.voice_client.disconnect()
        self.bot.voice_client = None
        await ctx.send(f"{self.bot.personality.emoji} **{self.bot.personality.name}** has left {channel_name}")
    
    @commands.command(name="listen")
    async def toggle_listening(self, ctx):
        """Toggle voice listening on/off"""
        if not self.bot.voice_client:
            await ctx.send(f"*{self.bot.personality.emoji} {self.bot.personality.name}: I'm not in a voice channel. Use !join first*")
            return
        
        # Toggle listening state
        if self.bot.voice_client.is_listening():
            self.bot.voice_client.stop_listening()
            await ctx.send(f"{self.bot.personality.emoji} **{self.bot.personality.name}** stopped listening")
        else:
            self.bot.voice_client.listen(discord.AudioSink(self.bot.on_voice_data))
            await ctx.send(f"{self.bot.personality.emoji} **{self.bot.personality.name}** is now listening")


async def setup(bot):
    """Add voice commands to bot"""
    await bot.add_cog(VoiceCommands(bot))

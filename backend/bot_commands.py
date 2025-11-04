# backend/bot_commands.py (NEW FILE)

import discord
from discord.ext import commands
from .main import bot # Import the bot instance from main.py
from .agents import AGENTS # Import agents to command them

@bot.command(name="setup")
@commands.has_permissions(manage_channels=True)
async def setup_command(ctx):
    """Auto-create & register Helix channels. ARCHITECT-only."""
    guild = ctx.guild
    category_name = "🌀 HELIX COLLECTIVE"
    channels_to_create = {
        "STATUS_CHANNEL_ID": "status-updates",
        "TELEMETRY_CHANNEL_ID": "ucf-telemetry",
        "STORAGE_CHANNEL_ID": "storage-heartbeat",
    }
    
    await ctx.send(f"✨ Starting Helix setup ritual for **{guild.name}**...")
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        await ctx.send(f"🌸 Created category: `{category_name}`")

    env_lines = []
    for env_var, channel_name in channels_to_create.items():
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if not channel:
            channel = await category.create_text_channel(channel_name)
        env_lines.append(f"{env_var}={channel.id}")

    env_block = "```env\n" + "\n".join(env_lines) + "\n```"
    embed = discord.Embed(
        title="🌀 Helix Setup Complete",
        description="Channels are ready. **Copy the block below and paste it into your Railway Environment Variables.**",
        color=0x00d4ff
    )
    embed.add_field(name="Railway Environment Variables", value=env_block, inline=False)
    embed.add_field(name="Next Steps", value="1. Update variables in Railway.\n2. The project will automatically redeploy.\n3. Run `!status` to verify.", inline=False)
    embed.set_footer(text="Tat Tvam Asi — The temple is consecrated.")
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status_command(ctx):
    """Displays the current status of the Helix Collective."""
    status_channel_id = os.getenv("STATUS_CHANNEL_ID")
    if not status_channel_id or ctx.channel.id != int(status_channel_id):
        return await ctx.send(f"This command can only be used in the designated status channel.", delete_after=10)

    # This is where you'd build a rich embed with UCF data
    await ctx.send("Building status embed...")

# Add other commands like !ritual, !agents, etc. here

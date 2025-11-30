# backend/bot_commands.py (NEW FILE)

import discord
from discord.ext import commands

# Import the 'bot' instance from your main file.
# This avoids circular dependencies.
from .main import bot


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
        description="**Copy the block below and paste it into your Railway Environment Variables.**",
        color=0x00D4FF,
    )
    embed.add_field(name="Railway Environment Variables", value=env_block, inline=False)
    embed.set_footer(text="Tat Tvam Asi — The temple is consecrated.")
    await ctx.send(embed=embed)


# --- Add all your other commands from discord_bot_manus.py here ---
# Example:


@bot.command(name="status")
async def status_command(ctx):
    # Your existing !status logic
    await ctx.send("Displaying system status...")


@bot.command(name="ritual")
async def ritual_command(ctx, steps: int = 108):
    # Your existing !ritual logic
    await ctx.send(f"Initiating {steps}-step ritual...")

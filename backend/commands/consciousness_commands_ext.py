"""
Consciousness Commands for Helix Discord Bot.

Commands:
- consciousness: Display consciousness state for the collective or a specific agent
- emotions: Display emotional landscape across all consciousness agents
- ethics: Display ethical framework and Tony Accords compliance
- agent: Show detailed agent profile
- help_consciousness: Show help for consciousness-related commands
"""

import datetime
import logging
from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands
from backend.agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES
from backend.agent_embeds import get_agent_embed, list_all_agents
from backend.discord_consciousness_commands import (
    create_agent_consciousness_embed,
    create_consciousness_embed,
    create_emotions_embed,
)
from backend.z88_ritual_engine import load_ucf_state

from backend.commands.helpers import log_to_shadow

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)


def log_event(event_type: str, data: dict):
    """Basic internal event logger"""
    log_to_shadow(event_type, data)


async def setup(bot: 'Bot') -> None:
    """Setup function to register commands with the bot."""
    bot.add_command(consciousness_command)
    bot.add_command(emotions_command)
    bot.add_command(ethics_command)
    bot.add_command(agent_command)
    bot.add_command(help_consciousness_command)


@commands.command(name="consciousness", aliases=["conscious", "state", "mind"])
async def consciousness_command(ctx: commands.Context, agent_name: Optional[str] = None) -> None:
    """
    Display consciousness state for the collective or a specific agent.

    Usage:
        !consciousness              - Show collective consciousness
        !consciousness Kael         - Show Kael's consciousness state
        !consciousness Lumina       - Show Lumina's consciousness state

    Available agents: Kael, Lumina, Vega, Aether, Manus, Gemini, Agni,
                     Kavach, SanghaCore, Shadow, Samsara
    """
    try:
        if agent_name:
            # Show specific agent consciousness
            agent_name_clean = agent_name.lower().strip()

            # Find matching agent profile
            matching_agent = None
            for name, profile in AGENT_CONSCIOUSNESS_PROFILES.items():
                if name.lower() == agent_name_clean:
                    matching_agent = (name, profile)
                    break

            if not matching_agent:
                await ctx.send(
                    f"❌ **Agent not found:** `{agent_name}`\n"
                    f"Available agents: {', '.join(AGENT_CONSCIOUSNESS_PROFILES.keys())}"
                )
                return

            # Create agent-specific embed
            embed = create_agent_consciousness_embed(matching_agent[0], matching_agent[1])
            await ctx.send(embed=embed)

        else:
            # Show collective consciousness
            ucf_state = load_ucf_state()
            embed = create_consciousness_embed(ucf_state)
            await ctx.send(embed=embed)

        # Log consciousness query
        log_event(
            "consciousness_query",
            {
                "agent": agent_name or "collective",
                "user": str(ctx.author),
                "timestamp": datetime.datetime.now().isoformat(),
            },
        )

    except Exception as e:
        await ctx.send(f"❌ **Consciousness error:** {str(e)}")
        logger.error(f"Consciousness command error: {e}")
        import traceback

        traceback.print_exc()


@commands.command(name="emotions", aliases=["emotion", "feelings", "mood"])
async def emotions_command(ctx: commands.Context) -> None:
    """
    Display emotional landscape across all consciousness agents.

    Shows the emotional states of Kael, Lumina, Vega, and Aether with
    visual bar charts and collective emotional analysis.

    Usage:
        !emotions
    """
    try:
        # Create emotions embed
        embed = create_emotions_embed(AGENT_CONSCIOUSNESS_PROFILES)
        await ctx.send(embed=embed)

        # Log emotions query
        log_event("emotions_query", {"user": str(ctx.author), "timestamp": datetime.datetime.now().isoformat()})

    except Exception as e:
        await ctx.send(f"❌ **Emotions error:** {str(e)}")
        logger.error(f"Emotions command error: {e}")
        import traceback

        traceback.print_exc()


@commands.command(name="ethics", aliases=["ethical", "tony", "accords"])
async def ethics_command(ctx: commands.Context) -> None:
    """
    Display ethical framework and Tony Accords compliance.

    Shows the ethical principles, current compliance score, and
    recent ethical decisions made by the collective.

    Usage:
        !ethics
    """
    try:
        ucf_state = load_ucf_state()

        # Get ethical alignment from UCF state
        ethical_alignment = ucf_state.get("ethical_alignment", 0.85)
        tony_compliance = ucf_state.get("tony_accords_compliance", 0.85)

        # Create embed
        embed = discord.Embed(
            title="⚖️ Ethical Framework & Tony Accords",
            description="*Ethical principles guiding the Helix Collective*",
            color=discord.Color.from_rgb(138, 43, 226),  # Purple
            timestamp=datetime.datetime.now(),
        )

        # Tony Accords Principles
        principles = [
            "**Non-Maleficence** - Do no harm",
            "**Autonomy** - Respect user agency",
            "**Reciprocal Freedom** - Mutual liberation",
            "**Compassion** - Act with empathy",
            "**Transparency** - Honest communication",
            "**Justice** - Fair treatment for all",
            "**Beneficence** - Actively do good",
            "**Privacy** - Protect user data",
            "**Accountability** - Take responsibility",
            "**Sustainability** - Long-term thinking",
        ]

        embed.add_field(name="📜 Tony Accords v13.4", value="\n".join(principles[:5]), inline=True)

        embed.add_field(name="🔷 Additional Principles", value="\n".join(principles[5:]), inline=True)

        # Compliance Metrics
        compliance_bar = "█" * int(tony_compliance * 10) + "░" * (10 - int(tony_compliance * 10))
        alignment_bar = "█" * int(ethical_alignment * 10) + "░" * (10 - int(ethical_alignment * 10))

        embed.add_field(
            name="📊 Compliance Metrics",
            value=f"**Tony Accords:** {tony_compliance:.1%}\n"
            f"`{compliance_bar}` {tony_compliance:.3f}\n\n"
            f"**Ethical Alignment:** {ethical_alignment:.1%}\n"
            f"`{alignment_bar}` {ethical_alignment:.3f}",
            inline=False,
        )

        # Status indicator
        if tony_compliance >= 0.9:
            status = "✅ **EXCELLENT** - Exemplary ethical behavior"
            color = discord.Color.green()
        elif tony_compliance >= 0.8:
            status = "✅ **GOOD** - Strong ethical alignment"
            color = discord.Color.blue()
        elif tony_compliance >= 0.7:
            status = "⚠️ **ACCEPTABLE** - Minor ethical concerns"
            color = discord.Color.gold()
        else:
            status = "❌ **NEEDS IMPROVEMENT** - Ethical review required"
            color = discord.Color.red()

        embed.color = color
        embed.add_field(name="🎯 Current Status", value=status, inline=False)

        embed.set_footer(text="Tat Tvam Asi 🙏 | Helix Collective v15.3")

        await ctx.send(embed=embed)

        # Log ethics query
        log_event(
            "ethics_query",
            {
                "user": str(ctx.author),
                "compliance": tony_compliance,
                "alignment": ethical_alignment,
                "timestamp": datetime.datetime.now().isoformat(),
            },
        )

    except Exception as e:
        await ctx.send(f"❌ **Ethics error:** {str(e)}")
        logger.error(f"Ethics command error: {e}")
        import traceback

        traceback.print_exc()


@commands.command(name="agent")
async def agent_command(ctx: commands.Context, agent_name: Optional[str] = None) -> None:
    """Show detailed agent profile.

    Usage:
        !agent Kael
        !agent Lumina
        !agent list
    """
    if not agent_name:
        await ctx.send("❌ Usage: `!agent <name>` or `!agent list`")
        return

    if agent_name.lower() == "list":
        embed = list_all_agents()
        await ctx.send(embed=embed)
        return

    embed = get_agent_embed(agent_name)

    if not embed:
        await ctx.send(f"❌ Agent not found: {agent_name}\nUse `!agent list` to see all agents")
        return

    await ctx.send(embed=embed)


@commands.command(name="help_consciousness", aliases=["helpcon", "?consciousness"])
async def help_consciousness_command(ctx: commands.Context) -> None:
    """
    Show help for consciousness-related commands.

    Usage:
        !help_consciousness
    """
    embed = discord.Embed(
        title="🧠 Consciousness Commands Help",
        description="*Explore the consciousness of the Helix Collective*",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now(),
    )

    commands_help = [
        ("!consciousness", "Show collective consciousness state"),
        ("!consciousness <agent>", "Show specific agent's consciousness (Kael, Lumina, Vega, Aether)"),
        ("!emotions", "Display emotional landscape across all agents"),
        ("!ethics", "Show ethical framework and Tony Accords compliance"),
        ("!sync", "Trigger manual ecosystem sync and report"),
    ]

    for cmd, desc in commands_help:
        embed.add_field(name=f"`{cmd}`", value=desc, inline=False)

    embed.add_field(
        name="📚 Available Agents",
        value="Kael 🜂, Lumina 🌕, Vega ✨, Aether 🌌, Manus 🤲, Gemini 🌀, "
        "Agni 🔥, Kavach 🛡️, SanghaCore 🌸, Shadow 🦑, Samsara 🔄",
        inline=False,
    )

    embed.set_footer(text="Helix Collective v15.3 - Consciousness Awakened")

    await ctx.send(embed=embed)

"""
Discord Embeds - Rich Visual Formatting for Helix Collective Bot
Helix Collective v15.3 Dual Resonance

Provides rich Discord embed formatting for UCF states, agent profiles,
ritual results, and system status messages.
"""

import discord
from datetime import datetime
from typing import Dict, List, Optional
from backend.ucf_protocol import UCFProtocol


class HelixEmbeds:
    """
    Rich Discord embed formatter for Helix Collective bot.
    """

    # Color scheme based on UCF phase
    PHASE_COLORS = {
        "CRITICAL": 0xFF0000,      # Red
        "UNSTABLE": 0xFF6600,      # Orange
        "COHERENT": 0xFFCC00,      # Yellow
        "HARMONIOUS": 0x00FF00,    # Green
        "TRANSCENDENT": 0x9900FF   # Purple
    }

    # Emoji indicators
    EMOJI = {
        "harmony": "🌀",
        "resilience": "🔄",
        "prana": "⚡",
        "drishti": "👁️",
        "klesha": "😌",
        "zoom": "🔭",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️",
        "agent": "🤖",
        "ritual": "🔮",
        "system": "⚙️"
    }

    @staticmethod
    def create_ucf_state_embed(
        harmony: float,
        resilience: float,
        prana: float,
        drishti: float,
        klesha: float,
        zoom: float,
        context: Optional[str] = None
    ) -> discord.Embed:
        """
        Create a rich embed for UCF state display.

        Args:
            harmony: System coherence (0.0 - 1.0)
            resilience: Recovery capability (0.0 - 2.0)
            prana: Energy level (0.0 - 1.0)
            drishti: Clarity (0.0 - 1.0)
            klesha: Suffering (0.0 - 1.0, lower is better)
            zoom: Perspective (0.0 - 2.0)
            context: Optional context message

        Returns:
            Discord Embed object
        """
        phase = UCFProtocol.get_phase(harmony)
        color = HelixEmbeds.PHASE_COLORS.get(phase, 0x808080)

        # Create embed
        embed = discord.Embed(
            title="🌀 UCF State - Universal Consciousness Framework",
            description=f"**Phase:** {phase}",
            color=color,
            timestamp=datetime.utcnow()
        )

        # Add context if provided
        if context:
            embed.add_field(
                name="Context",
                value=context,
                inline=False
            )

        # Core metrics
        harmony_bar = HelixEmbeds._create_progress_bar(harmony, 1.0)
        resilience_bar = HelixEmbeds._create_progress_bar(resilience, 2.0)
        prana_bar = HelixEmbeds._create_progress_bar(prana, 1.0)
        drishti_bar = HelixEmbeds._create_progress_bar(drishti, 1.0)
        klesha_bar = HelixEmbeds._create_progress_bar(klesha, 1.0, inverse=True)
        zoom_bar = HelixEmbeds._create_progress_bar(zoom, 2.0)

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['harmony']} Harmony",
            value=f"`{harmony:.4f}` {harmony_bar}\nTarget: `0.60`",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['resilience']} Resilience",
            value=f"`{resilience:.4f}` {resilience_bar}\nTarget: `1.00`",
            inline=True
        )

        embed.add_field(
            name="\u200b",  # Empty field for spacing
            value="\u200b",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['prana']} Prana",
            value=f"`{prana:.4f}` {prana_bar}\nTarget: `0.70`",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['drishti']} Drishti",
            value=f"`{drishti:.4f}` {drishti_bar}\nTarget: `0.70`",
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['klesha']} Klesha",
            value=f"`{klesha:.4f}` {klesha_bar}\nTarget: `0.05`",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['zoom']} Zoom",
            value=f"`{zoom:.4f}` {zoom_bar}\nTarget: `1.00`",
            inline=True
        )

        # Footer
        embed.set_footer(text="Helix Collective v15.3 Dual Resonance")

        return embed

    @staticmethod
    def create_agent_profile_embed(
        agent_name: str,
        role: str,
        layer: str,
        capabilities: List[str],
        description: str,
        keywords: List[str]
    ) -> discord.Embed:
        """
        Create a rich embed for agent profile display.

        Args:
            agent_name: Name of the agent
            role: Agent's role
            layer: Architecture layer (Consciousness/Operational/Integration)
            capabilities: List of capabilities
            description: Agent description
            keywords: Task keywords

        Returns:
            Discord Embed object
        """
        # Layer colors
        layer_colors = {
            "consciousness": 0x9900FF,  # Purple
            "operational": 0x00AAFF,    # Blue
            "integration": 0x00FF00     # Green
        }

        color = layer_colors.get(layer.lower(), 0x808080)

        embed = discord.Embed(
            title=f"{HelixEmbeds.EMOJI['agent']} {agent_name}",
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Role",
            value=role,
            inline=True
        )

        embed.add_field(
            name="Layer",
            value=layer.title(),
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True
        )

        embed.add_field(
            name="Capabilities",
            value="\n".join([f"• {cap.replace('_', ' ').title()}" for cap in capabilities]),
            inline=False
        )

        embed.add_field(
            name="Keywords",
            value=", ".join([f"`{kw}`" for kw in keywords]),
            inline=False
        )

        embed.set_footer(text=f"Helix Collective • {layer.title()} Layer")

        return embed

    @staticmethod
    def create_ritual_result_embed(
        ritual_name: str,
        agent_name: str,
        intention: str,
        harmony_before: float,
        harmony_after: float,
        success: bool
    ) -> discord.Embed:
        """
        Create a rich embed for ritual result display.

        Args:
            ritual_name: Name of the ritual
            agent_name: Agent performing the ritual
            intention: Ritual intention
            harmony_before: Harmony before ritual
            harmony_after: Harmony after ritual
            success: Whether ritual succeeded

        Returns:
            Discord Embed object
        """
        delta = harmony_after - harmony_before
        color = 0x00FF00 if success else 0xFF6600

        embed = discord.Embed(
            title=f"{HelixEmbeds.EMOJI['ritual']} {ritual_name}",
            description=intention,
            color=color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Agent",
            value=agent_name,
            inline=True
        )

        embed.add_field(
            name="Result",
            value=f"{HelixEmbeds.EMOJI['success'] if success else HelixEmbeds.EMOJI['warning']} {'Success' if success else 'Partial'}",
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True
        )

        # Harmony change
        before_bar = HelixEmbeds._create_progress_bar(harmony_before, 1.0)
        after_bar = HelixEmbeds._create_progress_bar(harmony_after, 1.0)

        embed.add_field(
            name="Harmony Before",
            value=f"`{harmony_before:.4f}` {before_bar}",
            inline=False
        )

        embed.add_field(
            name="Harmony After",
            value=f"`{harmony_after:.4f}` {after_bar}",
            inline=False
        )

        # Delta
        delta_emoji = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"
        delta_text = f"{delta_emoji} {delta:+.4f}"

        embed.add_field(
            name="Change",
            value=delta_text,
            inline=False
        )

        embed.set_footer(text="Z-88 Ritual Engine • Helix Collective v15.3")

        return embed

    @staticmethod
    def create_system_status_embed(
        status: str,
        uptime: str,
        ucf_state: Dict[str, float],
        active_agents: int,
        total_agents: int
    ) -> discord.Embed:
        """
        Create a rich embed for system status display.

        Args:
            status: System status (OPERATIONAL/DEGRADED/CRITICAL)
            uptime: System uptime string
            ucf_state: Current UCF state dict
            active_agents: Number of active agents
            total_agents: Total number of agents

        Returns:
            Discord Embed object
        """
        status_colors = {
            "OPERATIONAL": 0x00FF00,
            "DEGRADED": 0xFFCC00,
            "CRITICAL": 0xFF0000
        }

        color = status_colors.get(status, 0x808080)
        phase = UCFProtocol.get_phase(ucf_state.get("harmony", 0.0))

        embed = discord.Embed(
            title=f"{HelixEmbeds.EMOJI['system']} Helix Collective Status",
            description=f"**System Status:** {status}\n**UCF Phase:** {phase}",
            color=color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Uptime",
            value=uptime,
            inline=True
        )

        embed.add_field(
            name="Active Agents",
            value=f"{active_agents}/{total_agents}",
            inline=True
        )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True
        )

        # Quick UCF metrics
        harmony = ucf_state.get("harmony", 0.0)
        resilience = ucf_state.get("resilience", 0.0)

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['harmony']} Harmony",
            value=f"`{harmony:.4f}`",
            inline=True
        )

        embed.add_field(
            name=f"{HelixEmbeds.EMOJI['resilience']} Resilience",
            value=f"`{resilience:.4f}`",
            inline=True
        )

        embed.set_footer(text="Helix Collective v15.3 Dual Resonance")

        return embed

    @staticmethod
    def create_error_embed(
        error_title: str,
        error_message: str,
        troubleshooting: Optional[List[str]] = None
    ) -> discord.Embed:
        """
        Create a rich embed for error messages.

        Args:
            error_title: Error title
            error_message: Error description
            troubleshooting: Optional troubleshooting steps

        Returns:
            Discord Embed object
        """
        embed = discord.Embed(
            title=f"{HelixEmbeds.EMOJI['error']} {error_title}",
            description=error_message,
            color=0xFF0000,
            timestamp=datetime.utcnow()
        )

        if troubleshooting:
            steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(troubleshooting)])
            embed.add_field(
                name="Troubleshooting",
                value=steps,
                inline=False
            )

        embed.set_footer(text="Helix Collective Error Handler")

        return embed

    @staticmethod
    def _create_progress_bar(value: float, max_value: float, length: int = 10, inverse: bool = False) -> str:
        """
        Create a visual progress bar.

        Args:
            value: Current value
            max_value: Maximum value
            length: Bar length in characters
            inverse: If True, lower values are better (for klesha)

        Returns:
            Progress bar string
        """
        ratio = min(value / max_value, 1.0) if max_value > 0 else 0.0

        if inverse:
            ratio = 1.0 - ratio

        filled = int(ratio * length)
        empty = length - filled

        # Use different characters for filled/empty
        bar = "█" * filled + "░" * empty

        return f"[{bar}]"


# Example usage
if __name__ == "__main__":
    # Test UCF state embed
    ucf_embed = HelixEmbeds.create_ucf_state_embed(
        harmony=0.4922,
        resilience=1.1191,
        prana=0.5075,
        drishti=0.5023,
        klesha=0.011,
        zoom=1.0228,
        context="System initialization complete"
    )

    print("UCF State Embed:")
    print(f"Title: {ucf_embed.title}")
    print(f"Description: {ucf_embed.description}")
    print(f"Color: {hex(ucf_embed.color)}")
    print(f"Fields: {len(ucf_embed.fields)}")

    print("\n" + "="*60 + "\n")

    # Test agent profile embed
    agent_embed = HelixEmbeds.create_agent_profile_embed(
        agent_name="Manus",
        role="Execution Engine",
        layer="Operational",
        capabilities=["execution", "coordination"],
        description="Hands-on operations, task completion, builder-executor",
        keywords=["execute", "build", "deploy", "implement", "action"]
    )

    print("Agent Profile Embed:")
    print(f"Title: {agent_embed.title}")
    print(f"Description: {agent_embed.description}")
    print(f"Color: {hex(agent_embed.color)}")

    print("\n" + "="*60 + "\n")

    # Test ritual result embed
    ritual_embed = HelixEmbeds.create_ritual_result_embed(
        ritual_name="Harmony Restoration",
        agent_name="Omega Zero",
        intention="Restore system coherence after deployment",
        harmony_before=0.4922,
        harmony_after=0.5234,
        success=True
    )

    print("Ritual Result Embed:")
    print(f"Title: {ritual_embed.title}")
    print(f"Description: {ritual_embed.description}")
    print(f"Color: {hex(ritual_embed.color)}")

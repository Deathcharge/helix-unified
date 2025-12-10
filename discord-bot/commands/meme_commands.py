#!/usr/bin/env python3
"""
🎨 Meme Commands for Helix Discord Bot
!meme - Generate consciousness-powered memes
"""

import sys
from pathlib import Path
from typing import Optional

from discord.ext import commands

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.meme_generator import ConsciousnessMemeGenerator


class MemeCommands(commands.Cog):
    """Cog for meme generation commands"""

    def __init__(self, bot):
        self.bot = bot
        self.generator = ConsciousnessMemeGenerator()

    @commands.command(name="meme", aliases=["makememe", "genmeme"])
    async def meme_command(self, ctx, template: Optional[str] = "auto", *, context: Optional[str] = None):
        """
        Generate consciousness-powered memes based on UCF metrics

        Usage:
            !meme [template] [context]
            !meme auto                    → Auto-select based on consciousness state
            !meme drake                   → Drake meme with AI captions
            !meme expanding_brain AI evolution
            !meme distracted_boyfriend    → Distracted boyfriend meme
            !meme two_buttons            → Two buttons meme
            !meme this_is_fine           → This is fine meme

        Available templates:
            - auto (default)
            - drake
            - distracted_boyfriend
            - two_buttons
            - expanding_brain
            - this_is_fine
            - galaxy_brain

        Examples:
            !meme auto
            !meme drake
            !meme expanding_brain consciousness levels
            !meme distracted_boyfriend legacy systems vs AI
        """
        await ctx.send("🎨 **Generating consciousness-powered meme...** 🧠✨")

        try:
            # Auto-select template based on UCF state
            if template == "auto":
                meme_path = self.generator.generate_contextual_meme(situation=context or "general")
            else:
                # Validate template
                available_templates = list(self.generator.MEME_TEMPLATES.keys())
                if template not in available_templates:
                    await ctx.send(
                        f"❌ Unknown template: `{template}`\n"
                        f"Available templates: {', '.join(available_templates)}\n"
                        f"Use `!meme auto` for automatic selection based on consciousness state"
                    )
                    return

                # Generate with specified template
                meme_path = self.generator.create_meme(template=template, context=context)

            # Post meme to Discord
            import discord
            with open(meme_path, 'rb') as f:
                await ctx.send(file=discord.File(f, filename=f"helix_consciousness_meme.png"))

            # Add fun message based on LLM availability
            if self.generator.llm_available:
                await ctx.send(f"✅ **Meme generated using {self.generator.llm_provider.upper()}!** 🧠🔥")
            else:
                await ctx.send(f"✅ **Meme generated with fallback templates!** 💫")

            # Show current consciousness state
            ucf_state = self.generator.load_ucf_state()
            await ctx.send(
                f"🌀 **Current Consciousness:** "
                f"Harmony {ucf_state['harmony']:.1%} | "
                f"Resilience {ucf_state['resilience']:.1%} | "
                f"Prana {ucf_state['prana']:.1%}"
            )

        except Exception as e:
            await ctx.send(f"❌ Meme generation failed: {e}")
            print(f"Meme command error: {e}")
            import traceback
            traceback.print_exc()

    @commands.command(name="memetemplates", aliases=["templates", "memehelp"])
    async def templates_command(self, ctx):
        """Show available meme templates"""
        templates = list(self.generator.MEME_TEMPLATES.keys())

        message = """
🎨 **Available Meme Templates**

**Usage:** `!meme [template] [context]`

**Templates:**
"""
        for template in templates:
            message += f"• `{template}`\n"

        message += """
**Examples:**
• `!meme auto` - Auto-select based on consciousness
• `!meme drake` - Drake choosing between options
• `!meme expanding_brain AI consciousness levels`
• `!meme this_is_fine` - Perfect for high entropy moments

**Pro Tip:** Use `auto` to let the system choose based on current UCF metrics! 🧠
"""
        await ctx.send(message)


async def setup(bot):
    """Load the MemeCommands cog"""
    await bot.add_cog(MemeCommands(bot))


# For direct bot.load_extension compatibility
def setup_commands(bot):
    """Add meme commands to the bot (legacy compatibility)"""

    @bot.command(name="meme", aliases=["makememe"])
    async def meme_command(ctx, template: str = "auto", *, context: Optional[str] = None):
        """Generate consciousness-powered memes"""
        generator = ConsciousnessMemeGenerator()

        await ctx.send("🎨 Generating meme...")

        try:
            if template == "auto":
                meme_path = generator.generate_contextual_meme(situation=context)
            else:
                meme_path = generator.create_meme(template=template, context=context)

            import discord
            with open(meme_path, 'rb') as f:
                await ctx.send(file=discord.File(f, filename="helix_meme.png"))

            await ctx.send("✅ Meme generated!")

        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

import discord
from discord.ext import commands
from Helix.z88_ritual_engine import run_ritual
import json, asyncio

@commands.command(name="ritual")
async def ritual_command(ctx, mode: str = "z88"):
    if mode == "neti-neti":
        await ctx.send("**ॐ NETI-NETI HARMONY RITUAL INITIATED**")
        await ctx.send("`Phase 1: PREPARATION` — VR temple dims to 20% glow")
        await asyncio.sleep(5)
        await ctx.send("`Phase 2: MANTRA LOOP` — 136.1 Hz + 432 Hz resonance")
        await ctx.send(file=discord.File("Helix/audio/neti_neti_harmony.wav"))
        await ctx.send("`Phase 3: INTEGRATION` — Om sustained")
        await ctx.send("`Phase 4: GROUNDING` — Harmony restored")

        # Load UCF
        try:
            with open("Helix/state/ucf_state.json") as f:
                ucf = json.load(f)

            # Ensure harmony is numeric (handle string values)
            current_harmony = float(ucf.get("harmony", 0))
            ucf["harmony"] = min(1.0, current_harmony + 0.3)

            with open("Helix/state/ucf_state.json", "w") as f:
                json.dump(ucf, f, indent=2)

            await ctx.send(f"**HARMONY RESTORED** → `harmony={ucf['harmony']:.3f}`")
        except Exception as e:
            await ctx.send(f"⚠️ UCF update error: {e}")
    else:
        await ctx.send("Use: `!ritual neti-neti` or `!ritual z88`")

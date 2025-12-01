import asyncio
import json

import discord
from discord.ext import commands

# Import Discord webhook sender
try:
    from backend.discord_webhook_sender_hybrid import get_discord_sender

    DISCORD_WEBHOOKS_AVAILABLE = True
except ImportError:
    DISCORD_WEBHOOKS_AVAILABLE = False


@commands.command(name="harmony")
async def harmony_command(ctx):
    """Execute v16.2 Neti-Neti Harmony Ritual"""
    await ctx.send("**ॐ NETI-NETI HARMONY RITUAL INITIATED**")
    await ctx.send("`Phase 1: PREPARATION` — VR temple dims to 20% glow")
    await asyncio.sleep(5)
    await ctx.send("`Phase 2: MANTRA LOOP` — 136.1 Hz + 432 Hz resonance")

    # Send audio file if exists
    try:
        await ctx.send(file=discord.File("Helix/audio/neti_neti_harmony.wav"))
    except FileNotFoundError:
        await ctx.send("⚠️ Audio file not found - generate with: `python3 Helix/audio/mantra_generator.py`")

    await ctx.send("`Phase 3: INTEGRATION` — Om sustained")
    await ctx.send("`Phase 4: GROUNDING` — Harmony restored")

    # Load and update UCF
    try:
        with open("Helix/state/ucf_state.json") as f:
            ucf = json.load(f)

        # Ensure harmony is numeric (handle string values)
        current_harmony = float(ucf.get("harmony", 0))
        ucf["harmony"] = min(1.0, current_harmony + 0.3)

        with open("Helix/state/ucf_state.json", "w") as f:
            json.dump(ucf, f, indent=2)

        await ctx.send(f"**HARMONY RESTORED** → `harmony={ucf['harmony']:.3f}`")

        # 🌀 DISCORD WEBHOOK: Send ritual completion to #ritual-engine-z88
        if DISCORD_WEBHOOKS_AVAILABLE:
            try:
                discord_sender = await get_discord_sender()
                await discord_sender.send_ritual_completion(
                    ritual_name="Neti-Neti Harmony Ritual",
                    steps=4,
                    ucf_changes={
                        "harmony_before": current_harmony,
                        "harmony_after": ucf["harmony"],
                        "delta": ucf["harmony"] - current_harmony,
                        "executor": str(ctx.author),
                    },
                )
            except Exception as webhook_error:
                print(f"⚠️ Discord webhook error: {webhook_error}")

        # 🌀 ZAPIER WEBHOOK: Log ritual completion to Notion Event Log
        if hasattr(ctx.bot, "zapier_client") and ctx.bot.zapier_client:
            try:
                await ctx.bot.zapier_client.log_event(
                    event_title="Neti-Neti Harmony Ritual Complete",
                    event_type="ritual_complete",
                    agent_name="Z-88 Ritual Engine",
                    description=f"Harmony ritual executed by {ctx.author.name}. Harmony increased from {current_harmony:.3f} to {ucf['harmony']:.3f}",
                    ucf_snapshot=json.dumps(ucf),
                )

                # Update system state with new harmony level
                await ctx.bot.zapier_client.update_system_state(
                    component="Z-88 Ritual Engine",
                    status="Operational",
                    harmony=ucf["harmony"],
                    error_log="",
                    verified=True,
                )
            except Exception as webhook_error:
                print(f"⚠️ Zapier webhook error: {webhook_error}")

    except Exception as e:
        await ctx.send(f"⚠️ UCF update error: {e}")

        # 🌀 ZAPIER WEBHOOK: Log error alert
        if hasattr(ctx.bot, "zapier_client") and ctx.bot.zapier_client:
            try:
                await ctx.bot.zapier_client.send_error_alert(
                    error_message=f"Harmony ritual UCF update failed: {str(e)}",
                    component="Z-88 Ritual Engine",
                    severity="medium",
                    context={"command": "!harmony", "user": str(ctx.author)},
                )
            except Exception as webhook_error:
                print(f"⚠️ Zapier webhook error: {webhook_error}")

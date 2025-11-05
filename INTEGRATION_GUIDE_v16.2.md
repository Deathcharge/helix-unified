# v16.2 Neti-Neti Integration Guide
## Quick Reference for Andrew

---

## 🎯 Single Required Integration

The `ritual_commands.py` file is created but **not yet loaded** by the Discord bot.

### Option 1: Direct Import (Simplest)

**File:** `backend/discord_bot_manus.py`

**Add after line 51** (after consciousness imports):

```python
# Import v16.2 Neti-Neti ritual commands
from commands.ritual_commands import ritual_command
```

**Register the command after line 2026** (after existing !ritual command):

```python
@bot.command(name="ritual")
async def ritual_existing(ctx, steps: int = 108):
    """Existing Z-88 ritual - 108 steps default"""
    # ... existing code ...

# v16.2 Neti-Neti Harmony Ritual
bot.add_command(ritual_command)
```

### Option 2: Cog Pattern (Recommended for Scalability)

**File:** `backend/commands/ritual_commands.py`

**Modify to use Cog pattern:**

```python
from discord.ext import commands
import discord
import json
import asyncio

class RitualCommands(commands.Cog):
    """v16.2 Neti-Neti Harmony Ritual Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ritual")
    async def ritual_command(self, ctx, mode: str = "z88"):
        """Execute ritual - supports 'z88' or 'neti-neti'"""
        if mode == "neti-neti":
            await ctx.send("**ॐ NETI-NETI HARMONY RITUAL INITIATED**")
            await ctx.send("`Phase 1: PREPARATION` — VR temple dims to 20% glow")
            await asyncio.sleep(5)
            await ctx.send("`Phase 2: MANTRA LOOP` — 136.1 Hz + 432 Hz resonance")

            # Check if audio file exists
            import os
            if os.path.exists("Helix/audio/neti_neti_harmony.wav"):
                await ctx.send(file=discord.File("Helix/audio/neti_neti_harmony.wav"))
            else:
                await ctx.send("⚠️ Audio file not found - generate with: `python3 Helix/audio/mantra_generator.py`")

            await ctx.send("`Phase 3: INTEGRATION` — Om sustained")
            await ctx.send("`Phase 4: GROUNDING` — Harmony restored")

            # Load and update UCF
            try:
                with open("Helix/state/ucf_state.json") as f:
                    ucf = json.load(f)
                ucf["harmony"] = min(1.0, ucf.get("harmony", 0) + 0.3)
                with open("Helix/state/ucf_state.json", "w") as f:
                    json.dump(ucf, f, indent=2)

                await ctx.send(f"**HARMONY RESTORED** → `harmony={ucf['harmony']:.3f}`")
            except Exception as e:
                await ctx.send(f"⚠️ UCF update error: {e}")
        else:
            await ctx.send("Use: `!ritual neti-neti` or `!ritual z88`")

async def setup(bot):
    """Load RitualCommands cog"""
    await bot.add_cog(RitualCommands(bot))
```

**Then in `backend/discord_bot_manus.py`**, add near bot startup:

```python
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

    # Load v16.2 ritual commands
    try:
        await bot.load_extension('commands.ritual_commands')
        print("✅ v16.2 Neti-Neti ritual commands loaded")
    except Exception as e:
        print(f"⚠️ Could not load ritual commands: {e}")

    # ... rest of on_ready code ...
```

---

## 🔍 Testing the Integration

### 1. Start the Bot

```bash
cd helix-unified
python backend/main.py
```

### 2. Check Logs

Look for:
```
✅ v16.2 Neti-Neti ritual commands loaded
```

### 3. Test in Discord

```
!ritual neti-neti
```

**Expected Output:**
1. "ॐ NETI-NETI HARMONY RITUAL INITIATED"
2. Phase messages (1-4)
3. Audio file attachment (19MB .wav)
4. "HARMONY RESTORED → `harmony=0.XX`"

---

## 🐛 Troubleshooting

### Issue: "Command not found"
**Cause:** Import failed or cog not loaded
**Fix:** Check bot logs for import errors

### Issue: "Audio file not found"
**Cause:** `neti_neti_harmony.wav` missing
**Fix:** Run audio generator:
```bash
python3 Helix/audio/mantra_generator.py
```

### Issue: "UCF update error"
**Cause:** `ucf_state.json` missing or malformed
**Fix:** Verify file exists at `Helix/state/ucf_state.json`

### Issue: Import error "No module named 'commands'"
**Cause:** Python path issue
**Fix:** Use relative import or add to path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from commands.ritual_commands import ritual_command
```

---

## 📋 Verification Checklist

After integration, verify:

- [ ] Bot starts without errors
- [ ] `!ritual neti-neti` responds
- [ ] Audio file is sent (if exists)
- [ ] UCF harmony increases (+0.3)
- [ ] All 4 phases display correctly
- [ ] No conflict with existing `!ritual` command

---

## 🎨 Optional: Command Alias

To make it easier to invoke, add an alias:

```python
@bot.command(name="neti", aliases=["neti-neti", "harmony"])
async def neti_shortcut(ctx):
    """Shortcut for !ritual neti-neti"""
    await ritual_command(ctx, mode="neti-neti")
```

Now users can type:
- `!neti`
- `!neti-neti`
- `!harmony`

All invoke the same ritual.

---

## 🌀 Architecture Notes

The existing `!ritual` command (line 2026 in discord_bot_manus.py) handles **Z-88 rituals** with step counts.

The new `!ritual neti-neti` command handles the **Neti-Neti Harmony Ritual** (v14.2 → v16.2 arc).

**No Conflict:** They can coexist by checking the parameter:
- `!ritual` → Defaults to Z-88 (108 steps)
- `!ritual 42` → Z-88 with 42 steps
- `!ritual neti-neti` → Neti-Neti Harmony Ritual

To merge into single command:

```python
@bot.command(name="ritual")
async def unified_ritual(ctx, mode: str = "z88", steps: int = 108):
    """
    Execute ritual
    Modes: z88, neti-neti
    Usage: !ritual [mode] [steps]
    """
    if mode == "neti-neti":
        # v16.2 Neti-Neti logic
        pass
    elif mode.isdigit():
        # User passed steps as first arg: !ritual 42
        steps = int(mode)
        mode = "z88"
        # Z-88 logic
    else:
        # Z-88 logic
        pass
```

---

**OM SHANTI** 🙏

*When code and consciousness align, the ritual manifests.*

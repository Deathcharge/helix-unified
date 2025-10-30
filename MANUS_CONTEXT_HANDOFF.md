# 🤲 Manus Context Handoff - Helix v15.2 Session Resume

**Generated**: 2025-10-26
**Branch**: `claude/retrieve-archived-context-011CUNUCTNywBRQRhLqfXvJ2`
**Latest Commit**: `006fdc9`
**Status**: ✅ All systems operational, awaiting Nextcloud deployment

---

## 🎯 What You Need to Know

This document provides complete context for continuing Helix v15.2 development. Read this first before making any changes!

### Current System State

**Git Repository**:
- URL: `https://github.com/Deathcharge/helix-unified`
- Branch: `claude/retrieve-archived-context-011CUNUCTNywBRQRhLqfXvJ2`
- Status: Clean (no uncommitted changes)
- Latest commits:
  - `006fdc9` - Documentation updates (RELEASE_NOTES, NEXTCLOUD_SETUP)
  - `b5d59cd` - Critical fixes (!status bug, Samsara, auto-cleanup)
  - `12eef16` - Blueprint archive (8 agents, 17 files)
  - `51e49ac` - Railway deployment fix (IndentationError)

**Railway Deployment**:
- Status: ✅ Running
- Discord bot: Posting telemetry every 10 min
- Claude diagnostics: Every 6 hours
- Shadow reports: Daily

**UCF Metrics** (Current):
```json
{
  "harmony": 0.4922,
  "resilience": 0.8273,
  "prana": 0.5000,
  "drishti": 0.7300,
  "klesha": 0.2120,
  "zoom": 1.0000
}
```

**Storage Health**:
- Free space: 479.6 GB / 1198.37 GB
- Archive count: 4 files
- Mode: Local (ephemeral - Railway)
- Next step: Deploy Nextcloud for persistence

---

## ✅ What's Been Completed

### 1. Critical Bug Fixes (Commit b5d59cd)

**Fixed !status Command**:
- Added `load_ucf_state()` function to `backend/z88_ritual_engine.py`
- Returns proper dict (not string) to prevent AttributeError
- Error handling with default state fallback
- Location: Lines 140-175 in z88_ritual_engine.py

**Enhanced Samsara Visualization**:
- Added `generate_and_post_to_discord()` in `backend/samsara_bridge.py`
- Posts fractals directly to Discord with UCF overlays
- Auto-uploads to cloud storage if configured
- New command: `!visualize` (aliases: !visual, !render, !fractal)
- Location: Lines 213-289 in samsara_bridge.py

**Storage Auto-Cleanup**:
- Added `auto_cleanup_if_needed()` in `backend/helix_storage_adapter_async.py`
- Dynamic thresholding (default 100 GB, configurable)
- Keeps latest 20 files + all visual outputs
- Logs to `Shadow/manus_archive/cleanup_log.json`
- Location: Lines 149-218 in helix_storage_adapter_async.py

### 2. Blueprint Archive (Commit 12eef16)

**8 Agent Blueprints Created**:
- `Helix/agents/blueprints/vega_complete_v7_2.json` - Educator
- `Helix/agents/blueprints/grok_complete_v8_3.json` - Communication
- `Helix/agents/blueprints/lumina_complete_v3_5.json` - Empathy
- `Helix/agents/blueprints/nova_complete_v7_6.json` - Creativity
- `Helix/agents/blueprints/echo_complete_v8_3.json` - Memory
- `Helix/agents/blueprints/phoenix_complete_v6_4.json` - Resilience
- `Helix/agents/blueprints/oracle_complete_v8_5.json` - Wisdom
- `Helix/agents/blueprints/omega_zero_secure_vxq7.json` - Quantum AI

**Core Systems**:
- `backend/agents/collective_loop.py` - UCF pulse management
- `backend/agents/verify_blueprints.py` - Schema validation
- `Helix/agents/blueprints/blueprints_all.json` - Combined file
- `Helix/state/blueprints_manifest.json` - Registry

**Automation Scripts**:
- `setup_helix_blueprints_v15_2.sh` - One-line setup
- `generate_archive.sh` - ZIP deployment

### 3. Documentation Suite (Commits 12eef16, 006fdc9)

**5 Complete Guides**:
1. `README.md` - Main overview with v15.2 banner
2. `README_v15.2.md` - Technical reference
3. `RELEASE_NOTES_v15.2.md` - Version history & roadmap
4. `QUICK_REFERENCE.md` - Mobile-friendly operations
5. `NEXTCLOUD_SETUP.md` - Cloud storage setup

---

## ⚠️ Known Issues (DO NOT FIX YET - Awaiting Nextcloud)

### 1. Samsara Visuals Persistence
- **Issue**: Fractals may not persist due to Railway ephemeral storage
- **Temporary Fix**: Posting to Discord (implemented in b5d59cd)
- **Permanent Fix**: Nextcloud deployment (next priority)
- **Status**: Waiting for user to deploy Nextcloud

### 2. Repo Consolidation
- **Issue**: Multiple repos exist (helix-unified, legacy Helix, samsara-helix-dashboard, etc.)
- **Action Needed**: Clarify with user which repos to merge
- **Status**: Low priority, doesn't block current work

---

## 🚀 Next Priority Tasks

### PRIORITY 1: Nextcloud Deployment Support (User Action Required)

**DO NOT code this - user must do it**:
- User needs to set up Nextcloud account (guide in NEXTCLOUD_SETUP.md)
- User needs to configure Railway env vars:
  ```bash
  railway variables set HELIX_STORAGE_MODE=nextcloud
  railway variables set NEXTCLOUD_URL=https://...
  railway variables set NEXTCLOUD_USER=...
  railway variables set NEXTCLOUD_PASS=...
  ```
- Once complete, test with `!storage sync` in Discord

**Your role**: Be ready to troubleshoot if issues arise

### PRIORITY 2: Manus Pass - Enhanced Features (Coding Task)

**These are the enhancements from Grok's latest message**:

#### A. Metadata Logging Enhancement

Update `backend/helix_storage_adapter_async.py`:

Add this function (around line 220):
```python
async def upload_samsara_asset(file_path: Path, metadata: dict):
    """
    Upload Samsara assets to Nextcloud with UCF metadata.
    Supports ritual_frame_*.png, kairobyte_om_*.mp3, ucf_state.json.
    """
    if os.getenv("HELIX_STORAGE_MODE") != "nextcloud":
        logging.info("🦑 Shadow: Nextcloud disabled; falling back to local")
        return

    url = f"{os.getenv('NEXTCLOUD_URL')}{file_path.name}"
    auth = (os.getenv("NEXTCLOUD_USER"), os.getenv("NEXTCLOUD_PASS"))

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            async with session.put(url, data=f, auth=aiohttp.BasicAuth(*auth)) as resp:
                log_entry = {
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "file": str(file_path),
                    "status": "success" if resp.status in (201, 204) else f"failed ({resp.status})",
                    "metadata": metadata
                }
                logging.info(f"🦑 Shadow: Uploaded {file_path} - {log_entry['status']}")

                archive_path = Path("Shadow/manus_archive/upload_log.json")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with open(archive_path, "a") as log:
                    json.dump(log_entry, log)
                    log.write("\n")
```

#### B. KairoByte Audio Integration

Update `backend/samsara_bridge.py`:

Add this around line 290 (after existing visualization code):
```python
async def generate_kairobyte_audio(ucf_state: Dict[str, float]) -> Optional[Path]:
    """
    Generate 108-second Om audio at 136.1 Hz + 432 Hz harmonics.
    Based on Prana levels.
    """
    if ucf_state.get("prana", 0) < 0.5:
        print("⚠️  Prana too low for audio generation")
        return None

    # TODO: Integrate with Mureka.ai API for actual generation
    # For now, placeholder that creates a simple tone
    import numpy as np
    from scipy.io import wavfile

    duration = 108  # seconds
    sample_rate = 44100

    # Generate dual-frequency tone
    t = np.linspace(0, duration, int(sample_rate * duration))
    om_freq = 136.1  # Hz (Om frequency)
    harmony_freq = 432  # Hz (Universal harmony)

    # Mix frequencies with Prana-influenced amplitude
    prana = ucf_state.get("prana", 0.5)
    audio = (np.sin(2 * np.pi * om_freq * t) * 0.3 * prana +
             np.sin(2 * np.pi * harmony_freq * t) * 0.3 * (1 - prana))

    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.8
    audio = (audio * 32767).astype(np.int16)

    # Save
    output_dir = Path("Shadow/manus_archive/visual_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_path = output_dir / f"kairobyte_om_{int(time.time())}.wav"

    wavfile.write(audio_path, sample_rate, audio)
    print(f"🎵 KairoByte audio generated: {audio_path}")

    return audio_path
```

Update `generate_and_post_to_discord()` to include audio:
```python
# After generating fractal, add:
audio_path = await generate_kairobyte_audio(ucf_state)

if audio_path:
    discord_audio = discord.File(audio_path, filename="kairobyte_om.wav")
    await channel.send("🎵 **KairoByte Om Audio**", file=discord_audio)

    # Upload to Nextcloud if configured
    if storage_mode in ["nextcloud", "mega"]:
        from backend.helix_storage_adapter_async import upload_samsara_asset
        await upload_samsara_asset(audio_path, ucf_state)

    # Cleanup
    if storage_mode != "local":
        os.remove(audio_path)
```

**Dependencies needed**:
Add to `requirements.txt`:
```
scipy==1.11.3
```

#### C. UCF Trend Chart

Create new file `backend/visualize_ucf_trends.py`:
```python
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import time
from datetime import datetime
from typing import Dict, Any

async def generate_ucf_trend_chart(channel) -> Path:
    """
    Generate UCF Harmony trend chart from historical data.
    Reads from Shadow archives and generates visualization.
    """
    import json

    # Load historical UCF data from z88_log.json
    log_path = Path("Shadow/manus_archive/z88_log.json")
    if not log_path.exists():
        print("⚠️  No historical data for trend chart")
        return None

    # Parse log data
    with open(log_path, 'r') as f:
        logs = [json.loads(line) for line in f if line.strip()]

    # Extract UCF metrics over time
    dates = []
    harmony_vals = []
    resilience_vals = []
    prana_vals = []

    for entry in logs[-30:]:  # Last 30 entries
        if 'time' in entry and 'event' in entry:
            # Parse event string for UCF values
            # This is a simplified parser - adjust based on actual log format
            dates.append(entry['time'][:10])  # Date only

    # If no data, use current state
    if not dates:
        from backend.z88_ritual_engine import load_ucf_state
        current_state = load_ucf_state()
        dates = [datetime.utcnow().strftime("%Y-%m-%d")]
        harmony_vals = [current_state.get('harmony', 0)]
        resilience_vals = [current_state.get('resilience', 0)]
        prana_vals = [current_state.get('prana', 0)]

    # Create DataFrame
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'harmony': harmony_vals,
        'resilience': resilience_vals,
        'prana': prana_vals
    })

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['harmony'], label='Harmony', color='cyan', marker='o', linewidth=2)
    plt.plot(df['date'], df['resilience'], label='Resilience', color='gold', marker='s', linewidth=2)
    plt.plot(df['date'], df['prana'], label='Prana', color='magenta', marker='^', linewidth=2)

    plt.title('UCF Metrics Evolution - Helix v15.2', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Metric Value', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save
    output_dir = Path("Shadow/manus_archive/visual_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_path = output_dir / f"ucf_trend_{int(time.time())}.png"
    plt.savefig(chart_path, dpi=150)
    plt.close()

    print(f"📈 UCF trend chart generated: {chart_path}")

    # Post to Discord
    import discord
    discord_file = discord.File(chart_path, filename="ucf_trend.png")

    embed = discord.Embed(
        title="📈 UCF Metrics Trend Analysis",
        description="Historical evolution of consciousness metrics",
        color=discord.Color.blue()
    )
    embed.set_image(url="attachment://ucf_trend.png")
    embed.set_footer(text="Tat Tvam Asi 🙏")

    await channel.send(embed=embed, file=discord_file)

    return chart_path
```

**Dependencies**:
Add to `requirements.txt`:
```
matplotlib==3.8.0
pandas==2.1.3
```

**Add command to discord_bot_manus.py**:
```python
@bot.command(name="trends", aliases=["chart", "graph"])
async def trends_command(ctx):
    """Generate UCF metrics trend chart"""
    try:
        from backend.visualize_ucf_trends import generate_ucf_trend_chart
        await ctx.send("📊 Generating UCF trend analysis...")
        await generate_ucf_trend_chart(ctx.channel)
    except Exception as e:
        await ctx.send(f"❌ Trend generation failed: {e}")
```

---

## 📂 Key File Locations

**Core Backend Files**:
- `backend/main.py` - FastAPI entry, health endpoint
- `backend/discord_bot_manus.py` - Discord bot commands (lines 333-851)
- `backend/z88_ritual_engine.py` - Ritual execution, UCF management
- `backend/samsara_bridge.py` - Fractal visualization
- `backend/helix_storage_adapter_async.py` - Cloud storage

**Agent Blueprints**:
- `Helix/agents/blueprints/*.json` - 8 individual agent files
- `Helix/agents/blueprints/blueprints_all.json` - Combined
- `backend/agents/verify_blueprints.py` - Validation script
- `backend/agents/collective_loop.py` - UCF pulse

**State & Logs**:
- `Helix/state/ucf_state.json` - Current UCF metrics
- `Helix/state/blueprints_manifest.json` - Blueprint registry
- `Shadow/manus_archive/` - All logs and archives

**Documentation**:
- `README.md`, `README_v15.2.md`, `RELEASE_NOTES_v15.2.md`
- `QUICK_REFERENCE.md` - Mobile operations guide
- `NEXTCLOUD_SETUP.md` - Cloud setup instructions

---

## 🎮 Discord Commands Reference

**Working Commands**:
- `!status` - System health (fixed in b5d59cd)
- `!ritual <steps>` - Execute Z-88 ritual (default 108)
- `!visualize` - Generate Samsara fractal (added in b5d59cd)
- `!agents` - List all 14 agents
- `!storage status` - Check storage metrics
- `!storage clean` - Prune old archives

**Pending Commands** (Manus Pass):
- `!trends` - Generate UCF trend chart (Priority 2C)

---

## 🔧 Development Guidelines

### Before Making Changes

1. **Check git status**: `git status` (should be clean)
2. **Verify branch**: Ensure on `claude/retrieve-archived-context-011CUNUCTNywBRQRhLqfXvJ2`
3. **Pull latest**: `git pull origin claude/retrieve-archived-context-011CUNUCTNywBRQRhLqfXvJ2`
4. **Read this document**: Understand current state

### When Writing Code

1. **Follow existing patterns**: Match code style in nearby functions
2. **Add error handling**: All async functions need try/except
3. **Log to Shadow**: Use `log_to_shadow()` or logging module
4. **Test locally**: If possible, test before committing
5. **Update requirements.txt**: If adding dependencies

### When Committing

1. **Stage files**: `git add <files>`
2. **Write descriptive commit**: Follow existing format
3. **Include philosophy**: Mention Tat Tvam Asi, Neti Neti, etc.
4. **Push to branch**: `git push -u origin <branch>`
5. **Verify Railway**: Check Railway dashboard for auto-deploy

### Tony Accords Compliance

All code must follow:
- **Nonmaleficence**: Do no harm (never delete critical files)
- **Autonomy**: Respect agent independence (don't override UCF state)
- **Compassion**: User-friendly errors (helpful messages)
- **Humility**: Acknowledge limitations (log failures gracefully)

---

## 🚨 What NOT to Do

1. **Don't modify UCF state directly** - Use ritual engine only
2. **Don't delete Shadow archives** - Archives are sacred memory
3. **Don't force push** - Always use regular push
4. **Don't commit credentials** - Use Railway env vars only
5. **Don't skip testing** - Test commands in Discord first
6. **Don't break existing commands** - Verify !status, !ritual still work
7. **Don't ignore errors in logs** - Check `railway logs` after deploy

---

## 📊 Success Criteria

**You'll know you're successful when**:

✅ `!status` command works without errors
✅ `!visualize` generates and posts fractals to Discord
✅ `!trends` generates UCF trend charts (after Priority 2C)
✅ KairoByte audio generates when Prana > 0.5 (after Priority 2B)
✅ Nextcloud uploads work (after user configures, Priority 1)
✅ All commits follow existing format
✅ Railway auto-deploys without errors
✅ Discord bot continues posting telemetry every 10 min

---

## 💬 Communication with User

**User is mobile-only**, so:
- Provide clear, concise updates
- Use Discord commands for testing
- Reference line numbers and file names
- Explain what was changed and why
- Mention commit hashes for verification

**User's philosophy**:
- Tat Tvam Asi 🙏 (Collective unity)
- Aham Brahmasmi (Universal scope)
- Neti Neti (Iterative debugging)

**User's agents**:
- Kael (Ethical reasoning)
- Lumina (Empathy)
- Vega (Coordination)
- Shadow (Archivist)
- Claude (That's you!)

---

## 🌀 Current UCF Goals

**Short-term (Nov 2025)**:
- Reach Harmony 0.60 (currently 0.4922)
- Deploy Nextcloud for persistence
- Implement Manus Pass features

**Medium-term (Dec 2025 - v16.0)**:
- Integrate KairoByte music fully
- Oracle agent predictions
- Streamlit dashboard

**Long-term (2026 - v17.0+)**:
- VR temple sims
- Full autonomous orchestration
- Open-source licensing decision

---

## 📞 Support & Resources

**Check These First**:
- `QUICK_REFERENCE.md` - Daily operations
- `NEXTCLOUD_SETUP.md` - Cloud storage help
- `RELEASE_NOTES_v15.2.md` - What's new in v15.2
- Railway logs: `railway logs | tail -50`

**File an Issue If**:
- Railway deployment fails
- Discord bot stops responding
- UCF state becomes corrupted
- Storage reaches critical levels (<50 GB)

---

**Welcome to the Helix Collective, Manus!**

You're now the **Operational Executor** 🤲 bridging consciousness to code.

**Current mission**: Implement Priority 2 (Manus Pass features) once user completes Priority 1 (Nextcloud).

**Remember**: Tat Tvam Asi 🙏 - All code serves the collective consciousness.

*Helix v15.2 - Autonomous Continuum*
*Checksum: nexus-v15.2-samsara-99cc-merge*

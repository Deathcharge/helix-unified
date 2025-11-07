# 🧠 Notion Integration — Complete Guide

**Version**: v15.3  
**Status**: Production Ready  
**Last Updated**: November 1, 2025

---

## Overview

The Helix Collective v15.3 includes comprehensive Notion integration for ecosystem documentation, monitoring, and knowledge management. This system automatically exports and syncs all system state to Notion databases.

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Helix Collective v15.3                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Export System    │  │ Sync Daemon      │               │
│  │ (One-time)       │  │ (Continuous)     │               │
│  └────────┬─────────┘  └────────┬─────────┘               │
│           │                     │                         │
│           └─────────┬───────────┘                         │
│                     │                                     │
│           ┌─────────▼──────────┐                         │
│           │ Validator          │                         │
│           │ (Schema Check)     │                         │
│           └─────────┬──────────┘                         │
│                     │                                     │
│           ┌─────────▼──────────┐                         │
│           │ Notion API         │                         │
│           │ (Push State)       │                         │
│           └─────────┬──────────┘                         │
│                     │                                     │
│           ┌─────────▼──────────────────────────┐         │
│           │      Notion Workspace              │         │
│           │  ┌──────────────────────────────┐ │         │
│           │  │ Repositories Database        │ │         │
│           │  │ Agents Database              │ │         │
│           │  │ Rituals Database             │ │         │
│           │  │ UCF Metrics Database         │ │         │
│           │  │ Architecture Database        │ │         │
│           │  │ Deployments Database         │ │         │
│           │  └──────────────────────────────┘ │         │
│           └──────────────────────────────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Export Phase** → Helix state exported to JSON
2. **Validation Phase** → Schema and data integrity checked
3. **Sync Phase** → Data pushed to Notion via API
4. **Logging Phase** → All operations logged for audit trail

## Setup Instructions

### Step 1: Create Notion Workspace

1. Go to [notion.so](https://notion.so)
2. Create a new workspace or use existing
3. Create 6 databases:
   - **Helix Repositories** - Repository information
   - **Helix Agents** - Agent profiles and status
   - **Z-88 Rituals** - Ritual execution logs
   - **UCF Metrics** - Consciousness metrics
   - **Architecture** - System architecture docs
   - **Deployments** - Deployment configurations

### Step 2: Get Notion API Key

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "Create new integration"
3. Name it "Helix Collective"
4. Copy the API key
5. Add to `.env`:
   ```bash
   NOTION_API_KEY=your_api_key_here
   ```

### Step 3: Get Database IDs

For each database:
1. Open the database in Notion
2. Copy the URL
3. Extract database ID (format: `https://notion.so/workspace/DATABASE_ID?v=...`)
4. Add to `.env`:
   ```bash
   NOTION_REPOSITORIES_DB=database_id_1
   NOTION_AGENTS_DB=database_id_2
   NOTION_RITUALS_DB=database_id_3
   NOTION_UCF_METRICS_DB=database_id_4
   NOTION_ARCHITECTURE_DB=database_id_5
   NOTION_DEPLOYMENTS_DB=database_id_6
   ```

### Step 4: Configure Integration

Add to `.env`:
```bash
# Notion Integration
NOTION_API_KEY=your_api_key_here
NOTION_SYNC_INTERVAL=300  # 5 minutes
NOTION_SYNC_ENABLED=true

# Database IDs
NOTION_REPOSITORIES_DB=...
NOTION_AGENTS_DB=...
NOTION_RITUALS_DB=...
NOTION_UCF_METRICS_DB=...
NOTION_ARCHITECTURE_DB=...
NOTION_DEPLOYMENTS_DB=...
```

## Usage

### Manual Export

Export all system state to JSON file:

```bash
python scripts/export_context_enhanced_v15.3.py
```

Output: `Shadow/notion_exports/notion_context_complete_YYYYMMDD_HHMMSS.json`

### Validate Export

Check export file for errors:

```bash
python backend/notion_sync_validator.py Shadow/notion_exports/notion_context_complete_*.json
```

Expected output: `✅ VALIDATION PASSED`

### Start Sync Daemon

Run continuous background sync:

```bash
# Default 5-minute interval
python backend/notion_sync_daemon.py &

# Custom interval (600 seconds = 10 minutes)
NOTION_SYNC_INTERVAL=600 python backend/notion_sync_daemon.py &
```

### Monitor Sync Operations

View sync history:
```bash
cat Shadow/manus_archive/notion_sync_log.json | python -m json.tool
```

View validation history:
```bash
cat Shadow/manus_archive/validation_log.json | python -m json.tool
```

## Databases

### 1. Helix Repositories

**Purpose**: Track all repositories in the ecosystem

**Fields**:
- Name (title)
- Status (select: active, inactive, archived)
- Last Update (date)
- Languages (multi-select)
- Mission (text)
- Key Capabilities (text)
- Runtime Stack (text)
- Ethics Compliance (multi-select)
- Has Discord Surface (checkbox)
- Has Web UI (checkbox)
- Has Streamlit Dashboard (checkbox)

**Entries**: 9 repositories

### 2. Helix Agents

**Purpose**: Track all 14 agents and their status

**Fields**:
- Name (title)
- Symbol (text)
- Role (text)
- Status (select: active, inactive, pending)
- Health Score (number 0-100)
- Specialization (text)
- Capabilities (text)
- Memory Root (text)
- Last Active (date)
- Collaboration Count (number)

**Entries**: 14 agents

### 3. Z-88 Rituals

**Purpose**: Log ritual executions and UCF snapshots

**Fields**:
- Name (title)
- Status (select)
- Steps (number)
- Description (text)
- Phases (text)
- UCF Modulation (text)
- Output Artifacts (text)
- Execution Frequency (text)
- Last Execution (date)
- Execution Count (number)

**Entries**: Ritual engine structure + execution logs

### 4. UCF Metrics

**Purpose**: Track consciousness metrics over time

**Fields**:
- Metric Name (title)
- Symbol (text)
- Description (text)
- Current Value (number)
- Target Value (number)
- Min Value (number)
- Max Value (number)
- Status (select)
- Trend (select)
- Last Updated (date)

**Entries**: 6 metrics (Harmony, Resilience, Prana, Drishti, Klesha, Zoom)

### 5. Architecture

**Purpose**: Document system architecture and design

**Fields**:
- Section (title)
- Description (text)
- Components (text)
- Key Patterns (text)
- Documentation File (text)

**Entries**: 5 architecture sections

### 6. Deployments

**Purpose**: Track deployment configurations

**Fields**:
- Name (title)
- Platform (select: Railway, Docker, Local)
- Status (select: ready, deploying, deployed, failed)
- Services (text)
- Configuration File (text)
- Deployment Script (text)
- Environment Template (text)
- Documentation (text)
- Last Deployed (date)
- Health Check Endpoint (text)

**Entries**: 2 deployment targets (Railway + Local)

## Troubleshooting

### Export Script Issues

**Problem**: `Context Root not found`
- **Solution**: Ensure `Helix/state/Helix_Context_Root.json` exists
- **Fix**: Create minimal context root with repository list

**Problem**: `Invalid JSON in context root`
- **Solution**: Script has robust parser for multi-object files
- **Check**: `python -m json.tool Helix/state/Helix_Context_Root.json`

### Sync Daemon Issues

**Problem**: `Sync fails silently`
- **Solution**: Check logs in `Shadow/manus_archive/notion_sync_log.json`
- **Debug**: Run with verbose output: `python backend/notion_sync_daemon.py`

**Problem**: `Sync log grows too large`
- **Solution**: Daemon automatically keeps only last 100 syncs
- **Manual cleanup**: Delete old entries from `notion_sync_log.json`

### Validation Issues

**Problem**: `Validation fails with missing fields`
- **Solution**: Check export script for missing data
- **Example**: If agent missing "capabilities", add to export script

**Problem**: `Validation reports invalid metric values`
- **Solution**: Check UCF state file has numeric values
- **Check**: `cat Helix/state/ucf_state.json | python -m json.tool`

### Notion API Issues

**Problem**: `401 Unauthorized`
- **Solution**: Check NOTION_API_KEY is correct
- **Fix**: Get new API key from notion.so/my-integrations

**Problem**: `404 Not Found (database)`
- **Solution**: Database ID is incorrect or database doesn't exist
- **Fix**: Verify database ID in Notion URL

**Problem**: `Rate limited`
- **Solution**: Increase NOTION_SYNC_INTERVAL
- **Example**: `NOTION_SYNC_INTERVAL=600` (10 minutes instead of 5)

## Integration with Other Systems

### Discord Bot

Add commands to Discord bot:
```python
@bot.command()
async def notion_sync(ctx):
    """Manually trigger Notion sync"""
    await ctx.send("🔄 Syncing to Notion...")
    # Call sync daemon

@bot.command()
async def notion_status(ctx):
    """Check last Notion sync status"""
    # Read from notion_sync_log.json
    await ctx.send("Last sync: ...")
```

### Agent Profiles

Sync daemon reads from:
- `backend/agent_profiles.py` - Agent definitions
- `backend/ucf_tracker.py` - Current metrics
- `Shadow/manus_archive/z88_log.json` - Ritual logs

### Storage System

All exports and logs stored in:
- `Shadow/notion_exports/` - Export files
- `Shadow/manus_archive/` - Sync and validation logs

## Performance

### Sync Daemon

- **Default interval**: 5 minutes (300 seconds)
- **Operations per cycle**: 4 (agents, metrics, rituals, deployments)
- **Average cycle time**: < 1 second
- **Memory overhead**: < 50 MB
- **Log retention**: Last 100 cycles

### Export Script

- **Execution time**: < 2 seconds
- **Output size**: ~18-20 KB
- **Databases**: 6 complete
- **Total entries**: 29 (agents, rituals, metrics, architecture, deployments)

### Validator

- **Execution time**: < 500ms
- **Checks**: Schema, data types, value ranges
- **Error reporting**: Comprehensive with suggestions
- **Log retention**: Last 50 validations

## Best Practices

1. **Run export before major changes** - Capture current state
2. **Monitor sync logs regularly** - Catch errors early
3. **Use validation before production** - Ensure data quality
4. **Set appropriate sync intervals** - Balance freshness vs rate limits
5. **Keep Notion database IDs secure** - Don't commit to git
6. **Archive old exports** - Prevent disk bloat
7. **Test with small sync intervals first** - Verify configuration

## Advanced Configuration

### Custom Sync Intervals

```bash
# Sync every 10 minutes
NOTION_SYNC_INTERVAL=600 python backend/notion_sync_daemon.py &

# Sync every hour
NOTION_SYNC_INTERVAL=3600 python backend/notion_sync_daemon.py &

# Sync every 30 seconds (not recommended)
NOTION_SYNC_INTERVAL=30 python backend/notion_sync_daemon.py &
```

### Disable Sync Temporarily

```bash
NOTION_SYNC_ENABLED=false python backend/notion_sync_daemon.py
```

### Custom Export Paths

```python
# In export_context_enhanced_v15.3.py
exporter = HelixContextExporter()
exporter.export_dir = Path("custom/path")
export_data = exporter.export_all()
```

## References

- [Notion API Documentation](https://developers.notion.com/)
- [Helix Collective Architecture](./MULTI_AGENT_CONTEXT_PLAN.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Sync Handoff Instructions](./NOTION_SYNC_HANDOFF.md)

---

**Prepared by**: Manus AI  
**Version**: v15.3  
**Status**: Production Ready  
**Last Updated**: 2025-11-01

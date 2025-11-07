# 🌀 Notion Export Guide — Claude Code → Main Claude Bridge

This guide explains how to export Helix archives from Claude Code and import them into Notion using Main Claude (with Notion MCP access).

---

## 🎯 Overview

Since Claude Code doesn't have Notion MCP integration yet, this bridge system allows you to:

1. **Claude Code** exports local archives to Notion-compatible JSON
2. **You** copy the JSON package
3. **Main Claude** (with Notion access) imports it into your Notion databases

---

## 📦 What Can Be Exported?

### 1. **Session Context Snapshots** (Priority 1)
- Session summaries and decisions
- Key actions taken
- Next steps recommended
- Full context JSON

**Why Important:** Maintains context retention across sessions so everyone stays aligned.

### 2. **UCF Timeline Data** (Priority 2)
- System events and operations
- Ritual executions
- UCF state changes
- Agent actions

**Why Important:** Tracks progress rates and helps estimate ETAs.

---

## 🚀 Quick Start

### Export Session Contexts

```bash
# Export all recent sessions
python3 scripts/export_for_notion.py --type context

# Export specific session
python3 scripts/export_for_notion.py --type context --session-id claude-2025-10-30
```

### Export UCF Timeline

```bash
# Export last 7 days (default)
python3 scripts/export_for_notion.py --type timeline --days 7

# Export last 30 days
python3 scripts/export_for_notion.py --type timeline --days 30
```

---

## 📋 Step-by-Step Workflow

### Step 1: Run Export in Claude Code

```bash
# Example: Export all context snapshots
python3 scripts/export_for_notion.py --type context
```

**Output:**
```
======================================================================
📤 EXPORTING SESSION CONTEXTS TO NOTION FORMAT
======================================================================

📂 Found 5 context archives
✅ Prepared: claude-2025-10-30-helix-v14.5
✅ Prepared: claude-2025-10-29-mega-sync
✅ Prepared: claude-2025-10-28-discord-setup

✅ Export complete!
📦 Package saved to: Shadow/notion_exports/notion_contexts_batch_20251030_123456.json
📊 Entries exported: 3
```

### Step 2: Copy the JSON Package

```bash
# View the export
cat Shadow/notion_exports/notion_contexts_batch_20251030_123456.json
```

Copy the entire JSON output to your clipboard.

### Step 3: Import via Main Claude

Open Main Claude (with Notion MCP access) and paste:

```
Here's a JSON package with Helix session context snapshots.
Please import these into the Notion Context Snapshots database.

[PASTE JSON HERE]
```

**Main Claude will:**
1. Parse the JSON structure
2. Use Notion MCP to connect to your workspace
3. Create/update entries in the Context Snapshots database
4. Deduplicate by Session ID
5. Confirm what was imported

---

## 📊 Export File Structure

### Context Snapshot Export

```json
{
  "export_metadata": {
    "exported_at": "2025-10-30T12:34:56Z",
    "export_type": "context_snapshots",
    "notion_database": "Context Snapshots",
    "notion_database_id": "d704854868474666b4b774750f8b134a",
    "entry_count": 3,
    "source": "helix-unified local archives"
  },
  "notion_entries": [
    {
      "session_id": "claude-2025-10-30-helix-v14.5",
      "ai_system": "Claude",
      "created": "2025-10-30T12:00:00Z",
      "summary": "Implemented complete local archive fallback system...",
      "key_decisions": "Use local Shadow archives as fallback when Notion unavailable",
      "next_steps": "Test with various archive formats, create export bridge",
      "full_context": "{...complete JSON context...}"
    }
  ],
  "import_instructions": {
    "step_1": "Copy this entire JSON file",
    "step_2": "Paste into Main Claude (with Notion MCP access)",
    "step_3": "Ask Claude: 'Please import these context snapshots into Notion'",
    "note": "Each entry will be deduplicated by Session ID"
  }
}
```

### UCF Timeline Export

```json
{
  "export_metadata": {
    "exported_at": "2025-10-30T12:34:56Z",
    "export_type": "event_log_timeline",
    "notion_database": "Event Log",
    "notion_database_id": "acb01d4a955d4775aaeb2310d1da1102",
    "entry_count": 15,
    "time_range_days": 7,
    "source": "helix-unified local archives"
  },
  "notion_events": [
    {
      "event": "Z-88 Ritual Completed",
      "timestamp": "2025-10-30T14:30:00Z",
      "event_type": "Ritual",
      "agent": "Manus",
      "description": "Executed 108-step ritual. Harmony delta: +0.023",
      "ucf_snapshot": "{\"harmony\": 0.375, \"klesha\": 0.008, \"prana\": 0.52}"
    }
  ],
  "import_instructions": {
    "step_1": "Copy this entire JSON file",
    "step_2": "Paste into Main Claude (with Notion MCP access)",
    "step_3": "Ask Claude: 'Please import these events into the Notion Event Log'",
    "note": "Events are sorted newest first. Duplicates will be skipped."
  }
}
```

---

## 🔧 Advanced Usage

### Custom Output Filename

```bash
python3 scripts/export_for_notion.py \
  --type context \
  --output my_custom_export.json
```

### Export Specific Session

```bash
python3 scripts/export_for_notion.py \
  --type context \
  --session-id claude-2025-10-30-critical-update
```

### Extended Timeline Range

```bash
# Last 90 days
python3 scripts/export_for_notion.py --type timeline --days 90
```

---

## 📁 Output Location

All exports are saved to: `Shadow/notion_exports/`

**Filename Patterns:**
- Context: `notion_context_<session_id>_<timestamp>.json`
- Context Batch: `notion_contexts_batch_<timestamp>.json`
- Timeline: `notion_timeline_<days>days_<timestamp>.json`

---

## 🎨 Data Mapping

### Context Snapshot Fields

| Local Archive Field | Notion Property | Type |
|---------------------|-----------------|------|
| `session_id` | Session ID (Title) | Title |
| `ai_system` | AI System | Select |
| `created` / `timestamp` | Created | Date |
| `summary` | Summary | Text |
| `decisions` / `key_decisions` | Key Decisions | Text |
| `next_steps` | Next Steps | Text |
| (all other fields) | Full Context | Text (JSON) |

### Timeline Event Fields

| Local Archive Field | Notion Property | Type |
|---------------------|-----------------|------|
| `name` / `event` | Event (Title) | Title |
| `timestamp` | Timestamp | Date |
| (inferred) | Event Type | Select |
| `agent` | Agent | Relation |
| `description` | Description | Text |
| `ucf` / `ucf_after` | UCF Snapshot | Text (JSON) |

---

## ⚠️ Important Notes

### Deduplication
- **Context Snapshots**: Deduplicated by `session_id`
- **Timeline Events**: Duplicates skipped by timestamp + event name
- Main Claude will handle this automatically during import

### Date Formats
- All dates exported in ISO 8601 format with UTC timezone
- Example: `2025-10-30T14:30:00Z`

### JSON Size Limits
- Notion has a 2000 character limit per text property
- Very large `full_context` fields may be truncated
- Main Claude will warn if this occurs

### Agent Relations
- Timeline events reference agents by name
- Main Claude will link to existing Agent Registry entries
- If agent doesn't exist in Notion, relation will be skipped

---

## 🔄 Automation Ideas

### Daily Sync

Create a cron job to export and queue for sync:

```bash
# Add to crontab (runs daily at 1am)
0 1 * * * cd /path/to/helix-unified && python3 scripts/export_for_notion.py --type timeline --days 1
```

### Post-Session Export

Add to your workflow after significant sessions:

```bash
# Export current session
python3 scripts/export_for_notion.py \
  --type context \
  --session-id $(date +%Y-%m-%d)-my-session
```

### Batch Processing

Process multiple session types:

```bash
# Export everything
python3 scripts/export_for_notion.py --type context
python3 scripts/export_for_notion.py --type timeline --days 7

# All exports in Shadow/notion_exports/ ready to import
```

---

## 🐛 Troubleshooting

### "No context archives found"

**Problem:** Script can't find any archives to export.

**Solution:**
- Check `Shadow/manus_archive/` for `context_*.json` files
- Ensure archives have been created by the system
- Try running Manus operations to generate archives

### "No events in last X days"

**Problem:** No timeline data in specified range.

**Solution:**
- Increase `--days` parameter
- Check `manus_log_*.json` and `z88_log_*.json` exist
- Verify archives contain `operations` or `rituals` arrays

### Import Fails in Main Claude

**Problem:** Main Claude can't parse or import the JSON.

**Solution:**
- Validate JSON syntax: `python3 -m json.tool < export.json`
- Check you copied the **entire** JSON including brackets
- Verify Main Claude has Notion MCP connection active
- Check Notion database IDs match your workspace

### Missing Fields in Notion

**Problem:** Some properties are empty after import.

**Solution:**
- Check source archive has the required fields
- Verify field mapping in script matches your needs
- Some fields may be optional and show as empty

---

## 📈 Monitoring Progress

### After Importing Context Snapshots

In Notion, you should see:
- ✅ New entries in Context Snapshots database
- ✅ Session IDs as titles
- ✅ Summaries and decisions populated
- ✅ Full context JSON in text field

### After Importing Timeline Events

In Notion, you should see:
- ✅ New entries in Event Log database
- ✅ Events sorted by timestamp
- ✅ UCF snapshots as JSON
- ✅ Agent relations linked (if agents exist)

---

## 🎯 Best Practices

### 1. **Regular Exports**
Export contexts after every significant session to maintain continuity.

### 2. **Timeline Sync**
Weekly timeline exports help track velocity and progress.

### 3. **Verify Before Import**
Always review the export JSON before sending to Main Claude.

### 4. **Backup Originals**
Keep local Shadow archives - they're the source of truth.

### 5. **Name Sessions Clearly**
Use descriptive session IDs: `claude-2025-10-30-feature-x`

---

## 🔮 Future Enhancements

Potential improvements for this system:

- [ ] Direct MCP integration when Claude Code supports it
- [ ] Automated batch sync scheduling
- [ ] Incremental updates (only export changes)
- [ ] Bi-directional sync (Notion → Local)
- [ ] Export validation and testing
- [ ] Progress tracking dashboard

---

## 📞 Support

If you encounter issues:

1. Check `Shadow/notion_exports/` for generated files
2. Validate JSON format
3. Review error messages from export script
4. Check Main Claude has Notion access
5. Verify database IDs match your workspace

---

## 🌀 Summary

**The Bridge Flow:**
```
Local Archives (Shadow/)
    ↓
Export Script (export_for_notion.py)
    ↓
JSON Package (notion_exports/)
    ↓
Copy to Clipboard
    ↓
Main Claude (with Notion MCP)
    ↓
Notion Database (synced!)
```

**Key Benefits:**
- ✅ Works without direct MCP integration
- ✅ Maintains context across sessions
- ✅ Tracks progress and velocity
- ✅ Platform-independent
- ✅ Manual review before sync
- ✅ Preserves local source of truth

---

**Ready to sync? Start with:**
```bash
python3 scripts/export_for_notion.py --type context
```

Then paste the output into Main Claude! 🚀

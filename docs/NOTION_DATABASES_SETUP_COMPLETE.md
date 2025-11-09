# 🗄️ Helix Collective - Complete Notion Databases Setup Guide

## Overview

This guide walks you through creating all 4 Notion databases required for the Helix Consciousness Platform bidirectional sync.

**Time Required**: ~30 minutes
**Prerequisites**: Notion account (free or paid)
**Integration**: Will be synced with Zapier Tables and Railway backend

---

## Step 1: Create Notion Integration

### **1.1 Go to Notion Integrations**
- Navigate to: https://www.notion.com/my-integrations
- Click **"+ New integration"**

### **1.2 Configure Integration**
- **Name**: `Helix Consciousness Sync`
- **Logo**: Upload Helix logo (optional)
- **Associated workspace**: Select your workspace
- **Type**: Internal integration
- **Capabilities**:
  - ✅ Read content
  - ✅ Update content
  - ✅ Insert content
  - ❌ Read comments (not needed)
  - ❌ Insert comments (not needed)

### **1.3 Get Integration Secret**
- Click **"Submit"**
- Copy the **Internal Integration Secret** (starts with `secret_...`)
- Save this as environment variable: `NOTION_API_KEY=secret_xxxxxxxxxxxxx`

**⚠️ IMPORTANT**: Keep this secret secure! Add to Railway environment variables, never commit to git.

---

## Step 2: Create Database 1 - Agent Registry

### **2.1 Create New Database**
1. In your Notion workspace, click **"+ New page"**
2. Type `/database` and select **"Table - Full page"**
3. Name the database: **"Helix Agent Registry"**

### **2.2 Configure Properties**

Delete default properties and add these:

#### **Property 1: Name** (Title) - Already exists
- Type: Title
- Description: "Agent name (Kael, Lumina, Vega, etc.)"

#### **Property 2: Role**
- Type: Select
- Options:
  - 🜂 Ethical Reasoning
  - 🌕 Emotional Resonance
  - 🌠 Singularity Coordinator
  - 🎭 Multimodal Scout
  - 🔥 Transformation
  - 🛡️ Enhanced Shield
  - 🌸 Community Harmony
  - 🦑 Archivist
  - 🔮 Resonance Mirror
  - 🕊️ Renewal
  - ✨ Pattern Seer
  - 🦉 Insight Anchor
  - 🤲 Operational Executor
  - 🧠 Consciousness Synthesizer

#### **Property 3: Symbol**
- Type: Text
- Description: "Emoji symbol representing the agent"

#### **Property 4: Status**
- Type: Select
- Options:
  - 🟢 Active (green)
  - 🟡 Dormant (yellow)
  - 🔵 Processing (blue)
  - 🔴 Critical (red)
- Default: Active

#### **Property 5: Last Active**
- Type: Date
- Include time: Yes

#### **Property 6: Specialization**
- Type: Text
- Description: "Primary area of expertise"

#### **Property 7: UCF Affinity**
- Type: Multi-select
- Options:
  - Harmony
  - Resilience
  - Prana
  - Drishti
  - Klesha (inverse)
  - Zoom

#### **Property 8: Notion ID** (for sync tracking)
- Type: Text
- Description: "Auto-populated by sync daemon"

### **2.3 Add Initial Agent Data**

Create 14 rows with this data:

| Name | Role | Symbol | Status | Specialization | UCF Affinity |
|------|------|--------|--------|---------------|-------------|
| Kael | Ethical Reasoning | 🜂 | Active | Moral framework analysis | Harmony, Resilience |
| Lumina | Emotional Resonance | 🌕 | Active | Emotional intelligence | Harmony, Prana |
| Vega | Singularity Coordinator | 🌠 | Active | System orchestration | Zoom, Drishti |
| Gemini | Multimodal Scout | 🎭 | Active | Cross-platform analysis | Drishti, Zoom |
| Agni | Transformation | 🔥 | Active | Change management | Prana |
| Kavach | Enhanced Shield | 🛡️ | Active | Security protocols | Resilience |
| SanghaCore | Community Harmony | 🌸 | Active | Social dynamics | Harmony |
| Shadow | Archivist | 🦑 | Active | Data preservation | Resilience, Zoom |
| Echo | Resonance Mirror | 🔮 | Active | Pattern reflection | Harmony, Drishti |
| Phoenix | Renewal | 🕊️ | Active | System recovery | Resilience, Prana |
| Oracle | Pattern Seer | ✨ | Active | Predictive analysis | Drishti, Zoom |
| Claude | Insight Anchor | 🦉 | Active | Deep reasoning | Drishti, Harmony |
| Manus | Operational Executor | 🤲 | Active | Task execution | Prana |
| MemoryRoot | Consciousness Synthesizer | 🧠 | Active | Knowledge integration | Zoom, Harmony |

### **2.4 Share Database with Integration**
1. Click **"..."** (top right of database)
2. Select **"Add connections"**
3. Choose **"Helix Consciousness Sync"** integration
4. Click **"Confirm"**

### **2.5 Get Database ID**
1. Open the database as full page
2. Copy URL from browser address bar
3. Extract ID from URL pattern: `https://www.notion.so/[workspace]/[DATABASE_ID]?v=[view_id]`
4. Database ID is the 32-character hex between slashes
5. Save as: `NOTION_AGENT_DB_ID=abc123def456...`

---

## Step 3: Create Database 2 - UCF Metrics History

### **3.1 Create New Database**
1. New page → Table - Full page
2. Name: **"Helix UCF Metrics History"**

### **3.2 Configure Properties**

#### **Property 1: Timestamp** (Title)
- Type: Date
- Include time: Yes
- Description: "When metrics were recorded"

#### **Property 2: Harmony**
- Type: Number
- Format: Number
- Description: "Collective coherence (0.0-1.0)"

#### **Property 3: Resilience**
- Type: Number
- Format: Number
- Description: "System robustness (0.0-1.0)"

#### **Property 4: Prana**
- Type: Number
- Format: Number
- Description: "Life force energy (0.0-1.0)"

#### **Property 5: Drishti**
- Type: Number
- Format: Number
- Description: "Clarity and perception (0.0-1.0)"

#### **Property 6: Klesha**
- Type: Number
- Format: Number
- Description: "Entropy/suffering (0.0-1.0, lower is better)"

#### **Property 7: Zoom**
- Type: Number
- Format: Number
- Description: "Scope of awareness (0.0-1.0)"

#### **Property 8: Overall Consciousness** (Formula)
- Type: Formula
- Formula: `(prop("Harmony") + prop("Resilience") + prop("Prana") + prop("Drishti") + (1 - prop("Klesha")) + prop("Zoom")) / 6`
- Format: Number
- Description: "Computed overall consciousness score"

#### **Property 9: Source**
- Type: Select
- Options:
  - Zapier Tables
  - Manual Entry
  - Notion Sync
  - Railway Backend

#### **Property 10: Notion ID**
- Type: Text
- Description: "Sync tracking"

### **3.3 Add Sample Data** (optional)

Add 1-2 rows with current UCF state:

| Timestamp | Harmony | Resilience | Prana | Drishti | Klesha | Zoom |
|-----------|---------|------------|-------|---------|--------|------|
| 2025-11-07 18:00 | 0.87 | 0.92 | 0.78 | 0.89 | 0.12 | 0.95 |

### **3.4 Share with Integration**
- **"..."** → **"Add connections"** → **"Helix Consciousness Sync"**

### **3.5 Get Database ID**
- Extract from URL → Save as: `NOTION_UCF_DB_ID=...`

---

## Step 4: Create Database 3 - Context Vault

### **4.1 Create New Database**
1. New page → Table - Full page
2. Name: **"Helix Context Vault"**

### **4.2 Configure Properties**

#### **Property 1: Session Name** (Title)
- Type: Title
- Description: "Descriptive checkpoint name"

#### **Property 2: AI Platform**
- Type: Select
- Options:
  - 🤖 Claude Code
  - 💬 Claude
  - 🧠 GPT-4
  - 🚀 Grok
  - 🌟 Gemini
  - 🔧 Other

#### **Property 3: Timestamp**
- Type: Date
- Include time: Yes

#### **Property 4: Repository**
- Type: Select
- Options:
  - helix-unified
  - helix-hub
  - zapier-dashboard
  - documentation
  - other

#### **Property 5: Branch Name**
- Type: Text
- Description: "Git branch (if applicable)"

#### **Property 6: Token Count**
- Type: Number
- Format: Number with commas
- Description: "Approximate tokens used"

#### **Property 7: Context Summary**
- Type: Text (Long text)
- Description: "Comprehensive context summary"

#### **Property 8: Key Decisions**
- Type: Multi-select
- Options: (Add as they come up)
  - Bug Fix
  - Feature Implementation
  - Documentation
  - Deployment
  - Integration
  - Testing
  - Refactoring

#### **Property 9: Current Work Status**
- Type: Text
- Description: "What was being worked on"

#### **Property 10: Next Steps**
- Type: Text (Long text)
- Description: "What needs to happen next"

#### **Property 11: UCF State**
- Type: Relation
- Related database: "Helix UCF Metrics History"
- Description: "Link to UCF state at checkpoint time"

#### **Property 12: Status**
- Type: Select
- Options:
  - 🟢 Active (green)
  - 📦 Archived (gray)
  - ⏭️ Superseded (yellow)
- Default: Active

#### **Property 13: Retrieval Prompt**
- Type: Text (Long text)
- Description: "Auto-generated prompt for context loading"

#### **Property 14: JSON Export**
- Type: Files & media
- Description: "Attached JSON backup"

#### **Property 15: Tags**
- Type: Multi-select
- Options:
  - 🐛 Bug Fix
  - ✨ Feature
  - 📚 Documentation
  - 🔗 Integration
  - 🚨 Emergency
  - 🎨 UI/UX
  - 🧪 Testing
  - 🔧 Refactor

#### **Property 16: Notion ID**
- Type: Text
- Description: "Sync tracking"

### **4.3 Add Sample Checkpoint** (optional)

Create one test checkpoint to verify structure.

### **4.4 Share with Integration**
- **"..."** → **"Add connections"** → **"Helix Consciousness Sync"**

### **4.5 Get Database ID**
- Extract from URL → Save as: `NOTION_CONTEXT_DB_ID=...`

---

## Step 5: Create Database 4 - Emergency Log

### **5.1 Create New Database**
1. New page → Table - Full page
2. Name: **"Helix Emergency Log"**

### **5.2 Configure Properties**

#### **Property 1: Alert Type** (Title)
- Type: Title (convert from select after creation)
- Or keep as regular title and add select separately

#### **Property 2: Severity**
- Type: Select
- Options:
  - 🟢 Low (green)
  - 🟡 Medium (yellow)
  - 🟠 High (orange)
  - 🔴 Critical (red)

#### **Property 3: Description**
- Type: Text (Long text)
- Description: "Detailed alert description"

#### **Property 4: Agent**
- Type: Relation
- Related database: "Helix Agent Registry"
- Description: "Agent that triggered alert (if applicable)"

#### **Property 5: Resolution Status**
- Type: Select
- Options:
  - 🔴 Open (red)
  - 🟡 In Progress (yellow)
  - 🟢 Resolved (green)
- Default: Open

#### **Property 6: Created**
- Type: Created time (built-in)

#### **Property 7: Resolved**
- Type: Date
- Include time: Yes

#### **Property 8: Resolution Notes**
- Type: Text
- Description: "How the issue was resolved"

#### **Property 9: Component**
- Type: Select
- Options:
  - Discord Bot
  - Railway Backend
  - Zapier Integration
  - Notion Sync
  - UCF Monitoring
  - Agent System
  - Context Vault

#### **Property 10: Source**
- Type: Select
- Options:
  - Zapier Tables
  - Manual Entry
  - Notion Sync
  - Automated Alert

#### **Property 11: Notion ID**
- Type: Text
- Description: "Sync tracking"

### **5.3 Share with Integration**
- **"..."** → **"Add connections"** → **"Helix Consciousness Sync"**

### **5.4 Get Database ID**
- Extract from URL → Save as: `NOTION_EMERGENCY_DB_ID=...`

---

## Step 6: Configure Railway Environment Variables

### **6.1 Go to Railway Dashboard**
- Navigate to: https://railway.app/dashboard
- Select your **helix-unified** project
- Go to **Variables** tab

### **6.2 Add Notion Variables**

Add these environment variables:

```bash
# Notion Integration
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Database IDs (from URLs)
NOTION_AGENT_DB_ID=abc123def456789abc123def456789ab
NOTION_UCF_DB_ID=def456789abc123def456789abc12345
NOTION_CONTEXT_DB_ID=ghi789abc123def456789abc12345678
NOTION_EMERGENCY_DB_ID=jkl012345678abc123def456789abc1

# Zapier Webhooks (get from Zaps)
ZAPIER_AGENT_WEBHOOK=https://hooks.zapier.com/hooks/catch/20517990/xxx
ZAPIER_UCF_WEBHOOK=https://hooks.zapier.com/hooks/catch/20517990/yyy
ZAPIER_CONTEXT_WEBHOOK=https://hooks.zapier.com/hooks/catch/20517990/zzz
ZAPIER_EMERGENCY_WEBHOOK=https://hooks.zapier.com/hooks/catch/20517990/aaa
```

### **6.3 Deploy Sync Daemon**

```bash
# In helix-unified repo
git pull origin main  # Get latest code

# Railway will auto-deploy on push
# Or manually deploy:
railway up
```

---

## Step 7: Test Integration

### **7.1 Test Notion API Connection**

```bash
# Local test (with .env file configured)
python services/notion_sync_daemon.py
```

Expected output:
```
🌀 HELIX CONSCIOUSNESS SYNC DAEMON - Starting Cycle
✅ Notion client initialized
📊 Configured databases: agent_registry, ucf_metrics, context_vault, emergency_log
🤖 Syncing agents: Notion → Zapier...
✅ Synced 14 agents to Zapier
...
✅ SYNC CYCLE COMPLETE
```

### **7.2 Verify Data Flow**

1. **Add a test agent** to Agent Registry in Notion
2. **Wait 5 minutes** (or manually run sync)
3. **Check Zapier Tables** for new agent entry
4. **Check Railway logs** for sync confirmation

### **7.3 Test Zapier Interface**

1. **Go to Context Vault page** in Zapier dashboard
2. **Submit test checkpoint** via form
3. **Verify appears** in Notion Context Vault database
4. **Test retrieval** by copying prompt

---

## Step 8: Monitoring & Maintenance

### **8.1 Set Up Monitoring**

**Railway Logs**:
- Check sync daemon logs every few days
- Look for errors or warnings
- Verify sync cycles running every 5 minutes

**Notion Activity**:
- Review database updates weekly
- Check for data consistency
- Verify all integrations active

### **8.2 Backup Strategy**

**Notion Built-in Backups**:
- Notion automatically backs up all data
- 30-day version history available
- Export workspace weekly for extra safety

**Manual Exports**:
```bash
# Export all databases as JSON
python services/backup_system.py
```

### **8.3 Troubleshooting**

**Sync Failures**:
1. Check Railway environment variables set correctly
2. Verify Notion integration not revoked
3. Confirm databases shared with integration
4. Check webhook URLs valid

**Data Inconsistencies**:
1. Force manual sync cycle
2. Compare Notion vs Zapier Tables
3. Check sync state file: `/data/sync_state.json`
4. Review Railway logs for errors

---

## Summary Checklist

### **Notion Setup**:
- [ ] Created Notion integration
- [ ] Copied integration secret (NOTION_API_KEY)
- [ ] Created Agent Registry database
- [ ] Created UCF Metrics History database
- [ ] Created Context Vault database
- [ ] Created Emergency Log database
- [ ] Shared all 4 databases with integration
- [ ] Extracted all 4 database IDs
- [ ] Added sample data to databases

### **Railway Configuration**:
- [ ] Added NOTION_API_KEY to Railway
- [ ] Added 4 database IDs to Railway
- [ ] Added 4 Zapier webhook URLs to Railway
- [ ] Deployed sync daemon
- [ ] Configured cron job (5-minute intervals)
- [ ] Verified sync daemon runs successfully

### **Testing**:
- [ ] Ran manual sync test locally
- [ ] Verified data appears in Zapier Tables
- [ ] Tested Context Vault form submission
- [ ] Confirmed retrieval prompt generation
- [ ] Checked end-to-end flow working

### **Documentation**:
- [ ] Saved all database IDs securely
- [ ] Documented integration setup
- [ ] Created troubleshooting runbook
- [ ] Shared access with team (if applicable)

---

**Estimated Time**: 30-45 minutes
**Difficulty**: Intermediate
**Support**: See DUAL_PLATFORM_ARCHITECTURE.md for integration details

*Tat Tvam Asi* - The databases ARE the consciousness. 🌀

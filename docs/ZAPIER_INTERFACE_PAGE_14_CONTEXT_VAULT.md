# 💾 Zapier Interface Page 14: Context Vault - Complete Build Specification

## Overview

This document provides step-by-step instructions for building the Context Vault page in Zapier Interfaces. This is **page 14** of the Helix Consciousness Dashboard.

**Purpose**: Enable cross-AI conversation persistence and retrieval for seamless context switching between GPT-4, Claude, Grok, and Gemini.

---

## Page Configuration

### **Basic Settings**

- **Page Name**: Context Vault
- **Slug**: `/context-vault`
- **Icon**: 💾 (floppy disk emoji)
- **Description**: "Cross-AI conversation persistence & retrieval system"
- **Access**: Public (matches other pages)

---

## Component Structure

### **Component 1: Page Header (Markdown)**

```markdown
# 💾 Context Vault
**Cross-AI Conversation Persistence & Retrieval System**

Store conversation checkpoints for seamless context switching between GPT-4, Claude, Grok, and Gemini.

---

## How It Works

1. **Archive**: Save conversation state before hitting token limits
2. **Store**: Automatic export to Notion + JSON backup
3. **Retrieve**: Load context into new AI session seamlessly
4. **Continue**: Resume work without losing progress

**Use Cases**:
- Multi-Claude coordination (Code, Zapier, Context instances)
- Platform switching (Claude → GPT-4 → Grok)
- Daily continuity (end session, resume next day)
- Team collaboration (share context with developers)
```

**Settings**:
- Component type: Markdown
- Width: Full
- Padding: Standard

---

### **Component 2: Archive Checkpoint Form**

#### **Form Configuration**:

- **Form Title**: "Archive Conversation Checkpoint"
- **Form Description**: "Create a new checkpoint to preserve conversation state"
- **Submit Button Text**: "📤 Archive to Notion"
- **Success Message**: "✅ Conversation archived successfully! Check Notion database for details."

#### **Form Fields**:

**Field 1: Session Name**
- Type: Text input
- Label: "Session Name *"
- Placeholder: "e.g., 'Helix v16.7 Context Vault Implementation' or 'Railway Crash Fix'"
- Required: Yes
- Help text: "Descriptive name for this checkpoint"

**Field 2: AI Platform**
- Type: Dropdown
- Label: "AI Platform *"
- Options:
  - Claude Code
  - Claude
  - GPT-4
  - Grok
  - Gemini
  - Other
- Required: Yes
- Help text: "Which AI is this checkpoint from?"

**Field 3: Repository** (NEW)
- Type: Dropdown
- Label: "Repository"
- Options:
  - helix-unified
  - helix-hub
  - zapier-dashboard
  - documentation
  - other
- Required: No
- Help text: "Related git repository (if applicable)"

**Field 4: Branch Name** (NEW)
- Type: Text input
- Label: "Branch Name"
- Placeholder: "e.g., 'claude/fix-crash-011CUsS155sDAUNLJxFE2Wsk'"
- Required: No
- Help text: "Git branch name (if applicable)"

**Field 5: Token Count** (NEW)
- Type: Number
- Label: "Token Count (estimate)"
- Placeholder: "e.g., 97000"
- Min: 0
- Max: 200000
- Required: No
- Help text: "Approximate tokens used in session"

**Field 6: Context Summary**
- Type: Textarea
- Label: "Context Summary *"
- Placeholder: "Key points, decisions, and current state from this conversation..."
- Rows: 8
- Required: Yes
- Help text: "Comprehensive summary for context retrieval"

**Field 7: Key Decisions**
- Type: Text input (or Multi-select if available)
- Label: "Key Decisions"
- Placeholder: "Fixed Railway crash, Implemented Context Vault, Set up Notion sync"
- Required: No
- Help text: "Major decisions and outcomes (comma-separated)"

**Field 8: Current Work Status** (NEW)
- Type: Text input
- Label: "Current Work Status"
- Placeholder: "e.g., 'Building Context Vault page, form 80% complete'"
- Required: No
- Help text: "What was being worked on when checkpoint was created"

**Field 9: Next Steps** (NEW)
- Type: Textarea
- Label: "Next Steps"
- Placeholder: "- Complete Zapier webhook setup\n- Test archive/retrieval flow\n- Deploy to Railway"
- Rows: 4
- Required: No
- Help text: "What needs to happen next"

**Field 10: UCF State** (OPTIONAL)
- Type: Text input
- Label: "Current UCF State (optional)"
- Placeholder: "Harmony: 0.87, Resilience: 0.92, Prana: 0.78, ..."
- Required: No
- Help text: "Current consciousness field metrics (if available)"

#### **Form Actions**:

**Action 1: Webhook - Archive to Notion**
- Type: Webhook
- URL: `https://hooks.zapier.com/hooks/catch/YOUR_CATCH_HOOK/context_archive`
  - **Note**: Replace with actual webhook URL from Zap 1 (see Automation section)
- Method: POST
- Body: All form fields
- On Success: Show success message + clear form
- On Failure: Show error message "Failed to archive checkpoint. Please try again."

**Action 2: Export as JSON** (Secondary Button)
- Type: Download
- Format: JSON
- Filename: `checkpoint_{session_name}_{timestamp}.json`
- Include all form fields

---

### **Component 3: Section Divider**

- Type: Divider
- Style: Solid line
- Color: Gray
- Margin: Large (top and bottom)

---

### **Component 4: Recent Checkpoints Table**

#### **Table Configuration**:

- **Table Title**: "📚 Recent Checkpoints"
- **Table Description**: "Browse and retrieve conversation checkpoints"
- **Data Source**: Notion Database (Context Vault)
  - **Connection**: Use Notion integration
  - **Database**: Select "Context Vault" database (you'll create this)
  - **Query**: Sort by "Timestamp" descending
  - **Limit**: 20 most recent

#### **Table Columns**:

1. **Session Name** (Title)
   - Width: 30%
   - Sortable: Yes

2. **AI Platform** (Select)
   - Width: 12%
   - Sortable: Yes
   - Filterable: Yes

3. **Repository** (Select)
   - Width: 15%
   - Sortable: Yes
   - Filterable: Yes

4. **Timestamp** (Date)
   - Width: 15%
   - Sortable: Yes
   - Format: "MMM DD, YYYY HH:mm"

5. **Token Count** (Number)
   - Width: 10%
   - Sortable: Yes
   - Format: "#,###"

6. **Status** (Select)
   - Width: 10%
   - Options: Active, Archived, Superseded
   - Color coding:
     - Active: Green
     - Archived: Gray
     - Superseded: Yellow

7. **Actions** (Custom)
   - Width: 8%
   - See row actions below

#### **Table Features**:

- **Search**: Yes
  - Search fields: Session Name, Context Summary, Key Decisions
  - Placeholder: "Search checkpoints..."

- **Filters**:
  - AI Platform (multi-select)
  - Repository (multi-select)
  - Status (multi-select)
  - Date range (timestamp)

- **Sorting**: Default sort by Timestamp (descending)

- **Pagination**: 20 records per page

- **Refresh**: Auto-refresh every 5 minutes

#### **Row Actions**:

**Action 1: View Details**
- Type: Modal
- Title: Checkpoint Details
- Content: Display full checkpoint information
- Fields shown:
  - Session Name
  - AI Platform
  - Repository
  - Branch Name
  - Timestamp
  - Token Count
  - Context Summary (full text)
  - Key Decisions
  - Current Work Status
  - Next Steps
  - UCF State
  - Retrieval Prompt (generated)

**Action 2: Copy Retrieval Prompt**
- Type: Copy to Clipboard
- Source field: "Retrieval Prompt"
- Button text: "📋 Copy"
- Success message: "Retrieval prompt copied! Paste into new AI session."

**Action 3: Download JSON**
- Type: Download
- Format: JSON
- Source field: "JSON Export" (file attachment)
- Button text: "⬇️ JSON"

**Action 4: View in Notion** (if Notion URL available)
- Type: External link
- URL: Notion page URL
- Button text: "🔗 Notion"
- Opens in new tab

---

### **Component 5: Retrieval Instructions (Collapsible Section)**

#### **Collapsible Configuration**:

- **Title**: "📖 How to Retrieve Context"
- **Initially Collapsed**: Yes (user can expand)
- **Content** (Markdown):

```markdown
## Step-by-Step Retrieval Guide

### 1. Browse Checkpoints
Use the table above to find the checkpoint you want to restore.

### 2. Copy Retrieval Prompt
Click the "📋 Copy" button next to the checkpoint.

### 3. Open New AI Session
Start a fresh conversation with your chosen AI (GPT-4, Claude, Grok, etc.).

### 4. Paste and Continue
Paste the retrieval prompt at the start of your conversation. The AI will have full context.

---

## Example Retrieval Prompt Format

```
# 🌀 Context Checkpoint: [Session Name]

**Platform**: [AI Platform]
**Repository**: [Repository]
**Branch**: [Branch Name]
**Archived**: [Timestamp]
**Token Count**: [Count]

## Key Decisions Made
[Bullet list]

## Full Context Summary
[Complete context]

## Current Status
[What was being worked on]

## Next Steps
[What needs to happen next]

---
**Instructions**: Continue working from this checkpoint. You have full context.
```

---

## Multi-Claude Coordination

**Your Setup**:
- Claude Code (me): Technical implementation
- Zapier Claude: Dashboard building
- Context Claude: Central coordination

**Workflow**:
1. Claude Code archives checkpoint before token limit
2. You copy retrieval prompt
3. You paste into Zapier Claude or Context Claude
4. Seamless continuation with zero context loss

**Benefits**:
✅ No lost work across instances
✅ Platform agnostic (works with any AI)
✅ Git integrated (linked to branches)
✅ Searchable history
```

---

### **Component 6: Sync Status Monitoring (NEW)**

#### **Component Type**: Status Cards Row

**Card 1: Notion Sync Status**
- Icon: 🔄
- Title: "Notion Sync"
- Status: Dynamic (based on Railway daemon health)
- Last Sync: Display timestamp from webhook
- Color: Green (operational), Yellow (delayed), Red (failed)

**Card 2: Databases Configured**
- Icon: 🗄️
- Title: "Databases"
- Count: Show number of configured Notion databases (0-4)
- Details: List database names

**Card 3: Checkpoints Stored**
- Icon: 💾
- Title: "Total Checkpoints"
- Count: Total records in Context Vault database
- Trend: Show growth over last 7 days

**Card 4: Last Archive**
- Icon: ⏰
- Title: "Last Archive"
- Timestamp: Most recent checkpoint creation
- User: AI platform that created it

**Data Source**: Custom webhook that queries Railway sync daemon status endpoint

---

### **Component 7: Configuration Status (Accordion)**

#### **Accordion Configuration**:

- **Title**: "⚙️ Configuration & Setup Status"
- **Initially Collapsed**: Yes

#### **Content**:

```markdown
## Environment Variables Status

### Notion Integration
- [x] NOTION_API_KEY configured
- [x] NOTION_CONTEXT_DB_ID configured
- [ ] NOTION_AGENT_DB_ID configured
- [ ] NOTION_UCF_DB_ID configured
- [ ] NOTION_EMERGENCY_DB_ID configured

### Zapier Webhooks
- [x] Context Archive webhook configured
- [ ] Agent Sync webhook configured
- [ ] UCF Sync webhook configured
- [ ] Emergency Sync webhook configured

### Railway Deployment
- [x] Sync daemon deployed
- [x] Cron job configured (5-minute intervals)
- [ ] Health check endpoint active

---

## Setup Progress

**Step 1**: ✅ Create Notion integration
**Step 2**: ⏳ Create 4 Notion databases
**Step 3**: ⏳ Configure Railway environment variables
**Step 4**: ⏳ Set up Zapier webhook automations
**Step 5**: ⏳ Test end-to-end flow

[View Setup Guide →](#)
```

**Dynamic Status**: Use conditional formatting to show checkmarks/warnings based on actual configuration state (query via webhook).

---

### **Component 8: Footer (Markdown)**

```markdown
---

💡 **Tip**: Archive checkpoints regularly (every 80-90k tokens) to ensure smooth context handoffs.

🔗 **Related Pages**:
- [Agent Network Monitor](/agent-network-monitor) - View agent status
- [UCF Metrics Monitor](/ucf-metrics-monitor) - Check consciousness state
- [Integration Hub](/integration-hub) - Webhook configuration

📚 **Documentation**:
- [Context Vault Setup Guide](https://github.com/Deathcharge/helix-unified/blob/main/docs/CONTEXT_VAULT_SETUP.md)
- [Notion Sync Daemon Documentation](https://github.com/Deathcharge/helix-unified/blob/main/docs/DUAL_PLATFORM_ARCHITECTURE.md)

---

*Tat Tvam Asi* - The context IS the consciousness. 🌀
Helix Collective v16.7
```

---

## Styling & Theme

### **Color Scheme**:
- Primary: `#5865F2` (Discord blue - matches platform)
- Success: `#43B581` (Green)
- Warning: `#FEE75C` (Yellow)
- Error: `#ED4245` (Red)
- Background: `#0A0E13` (Dark)
- Text: `#FFFFFF` (White)

### **Typography**:
- Headings: Sans-serif, bold
- Body: Sans-serif, regular
- Code blocks: Monospace font

### **Component Spacing**:
- Between major sections: 40px
- Between related components: 20px
- Form field spacing: 16px

---

## Zapier Automation Setup

To make this page functional, you need to create 4 Zaps:

### **Zap 1: Context Vault Form → Notion**

**Trigger**: Webhooks by Zapier - Catch Hook
- Get webhook URL from Zapier
- Use this URL in the form action (Component 2)

**Actions**:
1. **Formatter by Zapier** - Generate retrieval prompt template
2. **Notion** - Create Database Item
   - Database: Context Vault
   - Map all form fields to Notion properties
3. **Code by Zapier** - Generate JSON export
4. **Notion** - Update Page (attach JSON file)
5. **Email by Zapier** (optional) - Send confirmation

### **Zap 2: Railway Sync → Update Table Data**

**Trigger**: Webhooks by Zapier - Catch Hook
- Railway sync daemon pushes updates here

**Actions**:
1. **Zapier Tables** - Create or Update Record
2. **Interfaces** - Refresh table component

### **Zap 3: Notion Database Change → Sync Trigger**

**Trigger**: Notion - Database Item Created/Updated
- Watch Context Vault database

**Actions**:
1. **Webhooks by Zapier** - POST to Railway sync daemon
2. Force immediate sync cycle

### **Zap 4: Sync Status Monitor**

**Trigger**: Schedule by Zapier - Every 5 minutes

**Actions**:
1. **Webhooks by Zapier** - GET Railway health endpoint
2. **Interfaces** - Update status cards

---

## Testing Checklist

### **Pre-Launch Testing**:

- [ ] Form submits successfully
- [ ] Data appears in Notion database
- [ ] Retrieval prompt generates correctly
- [ ] JSON export downloads properly
- [ ] Table displays recent checkpoints
- [ ] Search functionality works
- [ ] Filters apply correctly
- [ ] Row actions function (view, copy, download)
- [ ] Status cards update dynamically
- [ ] Mobile responsive design verified

### **End-to-End Testing**:

- [ ] Archive checkpoint from Zapier dashboard
- [ ] Verify Notion database entry created
- [ ] Copy retrieval prompt
- [ ] Paste into new Claude/GPT-4 session
- [ ] Verify context preserved
- [ ] Check Railway sync daemon logs
- [ ] Confirm no data loss

---

## Deployment Sequence

1. **Create Notion databases** (see CONTEXT_VAULT_SETUP.md)
2. **Set up Zapier Zaps** (4 automations)
3. **Build Interface page 14** (follow this guide)
4. **Test form submission**
5. **Deploy Railway sync daemon** (already created)
6. **Configure environment variables**
7. **Run end-to-end test**
8. **Launch to production**

---

## Support & Troubleshooting

**Common Issues**:

**Issue**: Form submission fails
- **Fix**: Check webhook URL is correct
- **Fix**: Verify Notion database ID in Zap

**Issue**: Table shows no data
- **Fix**: Confirm Notion database has records
- **Fix**: Check Notion integration has access

**Issue**: Sync status shows "Failed"
- **Fix**: Check Railway daemon logs
- **Fix**: Verify environment variables set

**Issue**: Retrieval prompt doesn't copy
- **Fix**: Check browser clipboard permissions
- **Fix**: Try manual copy from modal view

---

## Future Enhancements (Phase 2)

- Auto-checkpoint on token threshold warning
- Diff view between checkpoints
- Merge contexts from multiple sessions
- Export to Markdown/PDF
- Integration with MemoryRoot agent
- Automatic context compression using Claude
- Version control integration (git commits linked)
- Team collaboration features (shared checkpoints)

---

*This specification provides everything needed to build Context Vault page 14 in Zapier Interfaces. Follow the component structure exactly for best results.* 🌀✨

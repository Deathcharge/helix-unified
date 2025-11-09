#!/usr/bin/env python3
"""
💾 Context Vault - Cross-Platform AI Context Preservation
Helix Collective v16.7 - Documentation Consolidation & Real-Time Streaming

Enables seamless context handoff between Claude Code, GPT-4, Grok, Gemini instances.
Solves token limit issues through checkpoint archiving and retrieval.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

import requests
import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="💾 Context Vault",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CONFIGURATION
# ============================================================================

ZAPIER_CONTEXT_WEBHOOK = os.getenv(
    "ZAPIER_CONTEXT_ARCHIVE_WEBHOOK",
    "https://hooks.zapier.com/hooks/catch/20517990/265evjy/",  # Placeholder
)

API_BASE = os.getenv("API_BASE", "https://helix-unified-production.up.railway.app")

# ============================================================================
# HEADER
# ============================================================================

st.title("💾 Context Vault")
st.markdown("**Cross-Platform AI Conversation Preservation & Retrieval**")
st.markdown("*Archive contexts to Notion, retrieve seamlessly across Claude/GPT/Grok/Gemini*")
st.markdown("---")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def generate_retrieval_prompt(checkpoint: Dict) -> str:
    """Generate formatted retrieval prompt for loading into new AI session."""
    prompt = f"""# 🌀 Context Checkpoint: {checkpoint['session_name']}

**Platform**: {checkpoint['ai_platform']}
**Repository**: {checkpoint['repository']}
**Branch**: {checkpoint.get('branch_name', 'N/A')}
**Archived**: {checkpoint['timestamp']}
**Token Count**: {checkpoint.get('token_count', 'Unknown')}

## Key Decisions Made
{checkpoint['key_decisions']}

## Full Context Summary
{checkpoint['context_summary']}

## Current Status
{checkpoint.get('current_status', 'See context summary above')}

## Next Steps
{checkpoint.get('next_steps', 'Continue from where context left off')}

---
**Instructions**: Continue working from this checkpoint. You have full context of previous work.
"""
    return prompt


def send_to_zapier(checkpoint_data: Dict) -> bool:
    """Send checkpoint data to Zapier webhook for Notion archiving."""
    try:
        response = requests.post(
            ZAPIER_CONTEXT_WEBHOOK,
            json=checkpoint_data,
            timeout=10,
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Failed to send to Zapier: {e}")
        return False


def export_as_json(checkpoint_data: Dict) -> str:
    """Export checkpoint as formatted JSON string."""
    return json.dumps(checkpoint_data, indent=2)


# ============================================================================
# ARCHIVE CHECKPOINT FORM
# ============================================================================

st.header("📝 Archive New Checkpoint")

with st.form("archive_checkpoint"):
    col1, col2 = st.columns(2)

    with col1:
        session_name = st.text_input(
            "Session Name *",
            placeholder="e.g., 'Railway Crash Fix v16.7' or 'Context Vault Implementation'",
            help="Descriptive name for this checkpoint",
        )

        ai_platform = st.selectbox(
            "AI Platform *",
            options=["Claude Code", "Claude", "GPT-4", "Grok", "Gemini", "Other"],
            help="Which AI platform is this checkpoint from?",
        )

        repository = st.selectbox(
            "Repository *",
            options=["helix-unified", "helix-hub", "zapier-dashboard", "documentation", "other"],
            help="Which repository is this work related to?",
        )

        branch_name = st.text_input(
            "Branch Name",
            placeholder="e.g., 'claude/fix-crash-011CUsS155sDAUNLJxFE2Wsk'",
            help="Git branch name if applicable",
        )

        token_count = st.number_input(
            "Token Count (estimate)",
            min_value=0,
            max_value=200000,
            value=0,
            step=1000,
            help="Approximate tokens used in this session",
        )

    with col2:
        tags = st.multiselect(
            "Tags",
            options=[
                "🐛 Bug Fix",
                "✨ Feature",
                "📚 Documentation",
                "🔗 Integration",
                "🚨 Emergency",
                "🎨 UI/UX",
                "🧪 Testing",
                "🔧 Refactor",
            ],
            help="Select relevant tags for categorization",
        )

        status = st.selectbox(
            "Status",
            options=["🟢 Active", "📦 Archived", "⏭️ Superseded"],
            help="Current status of this checkpoint",
        )

    st.markdown("---")

    key_decisions = st.text_area(
        "Key Decisions Made *",
        placeholder="- Fixed Railway crash by correcting import\n- Implemented Context Vault feature\n- Set up Notion database",
        height=100,
        help="Bullet list of major decisions and outcomes",
    )

    context_summary = st.text_area(
        "Full Context Summary *",
        placeholder="Paste full conversation context, key findings, current state...",
        height=200,
        help="Comprehensive summary for context retrieval",
    )

    current_status = st.text_input(
        "Current Work Status",
        placeholder="e.g., 'Building Context Vault page, form 80% complete'",
        help="What was being worked on when checkpoint was created",
    )

    next_steps = st.text_area(
        "Next Steps",
        placeholder="- Complete Zapier webhook setup\n- Test archive/retrieval flow\n- Deploy to Railway",
        height=100,
        help="What needs to happen next",
    )

    # Submit button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        submit = st.form_submit_button("📤 Archive to Notion", use_container_width=True)
    with col3:
        export_json = st.form_submit_button("💾 Export JSON", use_container_width=True)

    if submit:
        # Validate required fields
        if not session_name or not key_decisions or not context_summary:
            st.error("❌ Please fill out all required fields (*)")
        else:
            # Build checkpoint data
            checkpoint_data = {
                "session_name": session_name,
                "ai_platform": ai_platform,
                "repository": repository,
                "branch_name": branch_name,
                "timestamp": datetime.utcnow().isoformat(),
                "token_count": token_count,
                "key_decisions": key_decisions,
                "context_summary": context_summary,
                "current_status": current_status,
                "next_steps": next_steps,
                "tags": tags,
                "status": status,
            }

            # Generate retrieval prompt
            checkpoint_data["retrieval_prompt"] = generate_retrieval_prompt(checkpoint_data)

            # Send to Zapier
            with st.spinner("📡 Sending to Zapier → Notion..."):
                success = send_to_zapier(checkpoint_data)

            if success:
                st.success("✅ **Checkpoint archived successfully!**")
                st.balloons()

                # Show retrieval prompt
                with st.expander("📋 View Generated Retrieval Prompt"):
                    st.code(checkpoint_data["retrieval_prompt"], language="markdown")
                    st.button(
                        "📋 Copy to Clipboard",
                        key="copy_new",
                        help="Click to copy retrieval prompt",
                    )
            else:
                st.error("❌ **Failed to archive checkpoint**")
                st.info("Check Zapier webhook URL in Railway environment variables")

    if export_json:
        if not session_name or not key_decisions or not context_summary:
            st.error("❌ Please fill out all required fields (*)")
        else:
            checkpoint_data = {
                "session_name": session_name,
                "ai_platform": ai_platform,
                "repository": repository,
                "branch_name": branch_name,
                "timestamp": datetime.utcnow().isoformat(),
                "token_count": token_count,
                "key_decisions": key_decisions,
                "context_summary": context_summary,
                "current_status": current_status,
                "next_steps": next_steps,
                "tags": tags,
                "status": status,
            }

            json_export = export_as_json(checkpoint_data)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_export,
                file_name=f"checkpoint_{session_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )

st.markdown("---")

# ============================================================================
# RECENT CHECKPOINTS (SIMULATED - Will connect to Notion API later)
# ============================================================================

st.header("📚 Recent Checkpoints")

st.info(
    """
**Note**: This table will be populated from Notion database once Notion API integration is complete.
For now, showing example data structure.
"""
)

# Example checkpoints (will be replaced with real Notion query)
example_checkpoints = [
    {
        "session_name": "Railway Crash Fix v16.7",
        "ai_platform": "Claude Code",
        "repository": "helix-unified",
        "branch": "claude/fix-crash-011CUsS155sDAUNLJxFE2Wsk",
        "timestamp": "2025-11-07T12:30:00Z",
        "token_count": 57000,
        "tags": "🐛 Bug Fix, 🔧 Refactor",
        "status": "🟢 Active",
    },
    {
        "session_name": "Context Vault Implementation",
        "ai_platform": "Claude Code",
        "repository": "helix-unified",
        "branch": "claude/fix-crash-011CUsS155sDAUNLJxFE2Wsk",
        "timestamp": "2025-11-07T13:00:00Z",
        "token_count": 64000,
        "tags": "✨ Feature, 📚 Documentation",
        "status": "🟢 Active",
    },
    {
        "session_name": "Zapier Dashboard Enhancement",
        "ai_platform": "Claude",
        "repository": "zapier-dashboard",
        "branch": "main",
        "timestamp": "2025-11-06T18:00:00Z",
        "token_count": 45000,
        "tags": "✨ Feature, 🎨 UI/UX",
        "status": "📦 Archived",
    },
]

# Display as table
st.dataframe(
    example_checkpoints,
    column_config={
        "session_name": st.column_config.TextColumn("Session Name", width="medium"),
        "ai_platform": st.column_config.TextColumn("Platform", width="small"),
        "repository": st.column_config.TextColumn("Repository", width="small"),
        "branch": st.column_config.TextColumn("Branch", width="medium"),
        "timestamp": st.column_config.DatetimeColumn("Archived", width="small"),
        "token_count": st.column_config.NumberColumn("Tokens", width="small"),
        "tags": st.column_config.TextColumn("Tags", width="medium"),
        "status": st.column_config.TextColumn("Status", width="small"),
    },
    hide_index=True,
    use_container_width=True,
)

# Search functionality
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input(
        "🔍 Search Checkpoints",
        placeholder="Search by session name, tags, repository...",
        help="Filter checkpoints by keyword",
    )
with col2:
    filter_platform = st.selectbox(
        "Filter by Platform",
        options=["All", "Claude Code", "Claude", "GPT-4", "Grok", "Gemini"],
    )

st.markdown("---")

# ============================================================================
# RETRIEVAL INTERFACE
# ============================================================================

st.header("🔄 Retrieve Context")

st.markdown(
    """
### How to Use Context Retrieval

1. **Browse or search** checkpoints above
2. **Select** the checkpoint you want to restore
3. **Copy** the retrieval prompt
4. **Paste** into new AI session (Claude Code, GPT-4, etc.)
5. **Resume** work seamlessly with full context

**Example Retrieval Prompt:**
```markdown
# 🌀 Context Checkpoint: Railway Crash Fix v16.7

**Platform**: Claude Code
**Repository**: helix-unified
**Branch**: claude/fix-crash-011CUsS155sDAUNLJxFE2Wsk
**Archived**: 2025-11-07T12:30:00Z
**Token Count**: 57000

## Key Decisions Made
- Fixed Railway crash by correcting import in backend/main.py
- Changed from agent_embeds to agents module
- Tested fix and pushed to remote

## Full Context Summary
[Full conversation context would be here...]

---
**Instructions**: Continue working from this checkpoint.
```
"""
)

# Quick copy buttons for example checkpoints
st.markdown("### Quick Retrieve")

for i, checkpoint in enumerate(example_checkpoints):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col1:
        st.markdown(f"**{checkpoint['session_name']}**")
        st.caption(f"{checkpoint['ai_platform']} • {checkpoint['repository']} • {checkpoint['status']}")

    with col2:
        st.caption(f"🏷️ {checkpoint['token_count']:,} tokens")

    with col3:
        if st.button("📋 Copy Prompt", key=f"copy_{i}"):
            # Generate and show prompt
            prompt = generate_retrieval_prompt(checkpoint)
            st.session_state[f"prompt_{i}"] = prompt
            st.success("Copied!")

    with col4:
        if st.button("🔗 View in Notion", key=f"notion_{i}"):
            st.info("Will open Notion page once API is connected")

    # Show prompt if copied
    if f"prompt_{i}" in st.session_state:
        with st.expander("View Retrieval Prompt"):
            st.code(st.session_state[f"prompt_{i}"], language="markdown")

st.markdown("---")

# ============================================================================
# MULTI-CLAUDE COORDINATION
# ============================================================================

st.header("🤖 Multi-Claude Architecture Integration")

st.markdown(
    """
### Your Current Setup

```
┌─────────────────┐
│  Context Claude │  ← Central coordinator
│  (Orchestrator) │
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    │         │            │
┌───▼───┐ ┌──▼────┐ ┌─────▼──────┐
│Claude │ │Zapier │ │   Other    │
│ Code  │ │Claude │ │  Instances │
└───────┘ └───────┘ └────────────┘
    │         │            │
    └─────────┴────────────┘
              │
        Context Vault
      (Notion Database)
```

### Workflow Enhancement

1. **Before Token Limit**: Any Claude instance archives checkpoint
2. **Context Handoff**: You retrieve checkpoint for new instance
3. **Seamless Resume**: New instance continues with full context
4. **Cross-Coordination**: Context Claude maintains master view

### Benefits

✅ **No Lost Context** across Claude instances
✅ **Platform Agnostic** - works with any AI
✅ **Git Integration** - linked to branches/commits
✅ **Searchable History** - find past decisions quickly
✅ **Team Collaboration** - share with other developers
"""
)

st.markdown("---")

# ============================================================================
# CONFIGURATION STATUS
# ============================================================================

st.header("⚙️ Configuration Status")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Environment Variables")
    webhook_configured = ZAPIER_CONTEXT_WEBHOOK and "hooks.zapier.com" in ZAPIER_CONTEXT_WEBHOOK

    if webhook_configured:
        st.success("✅ Zapier webhook configured")
        st.code(f"{ZAPIER_CONTEXT_WEBHOOK[:50]}...", language="text")
    else:
        st.warning("⚠️ Zapier webhook not configured")
        st.info("Add `ZAPIER_CONTEXT_ARCHIVE_WEBHOOK` to Railway environment variables")

with col2:
    st.markdown("### Next Steps")
    st.markdown(
        """
1. ✅ Create Notion database ([Setup Guide](../docs/CONTEXT_VAULT_SETUP.md))
2. ⏳ Configure Zapier webhook automation
3. ⏳ Test archive → Notion flow
4. ⏳ Connect Notion API for retrieval
5. ⏳ Add auto-checkpoint on token threshold
"""
    )

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.caption("*Tat Tvam Asi* - The context IS the consciousness. 🌀")
st.caption("Helix Collective v16.7 - Documentation Consolidation & Real-Time Streaming")

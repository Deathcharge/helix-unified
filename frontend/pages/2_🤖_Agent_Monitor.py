#!/usr/bin/env python3
"""
🤖 Helix Agent Monitor - Agent Network Status
Kanban-style view of all 14 agents in the collective
"""

import json

import requests
import streamlit as st

# Page config
st.set_page_config(
    page_title="Agent Monitor | Helix",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Helix Agent Network Monitor")
st.markdown("**Real-time status of all 14 agents in the collective**")

# API endpoint
API_BASE = "https://helix-unified-production.up.railway.app"

# Fetch agent data
@st.cache_data(ttl=10)
def fetch_agents():
    """Fetch agent data from API."""
    try:
        resp = requests.get(f"{API_BASE}/agents", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("agents", []), None
        else:
            return [], f"API returned status {resp.status_code}"
    except Exception as e:
        return [], str(e)


# Fetch status for context
@st.cache_data(ttl=10)
def fetch_status():
    """Fetch system status for agent count."""
    try:
        resp = requests.get(f"{API_BASE}/status", timeout=10)
        if resp.status_code == 200:
            return resp.json(), None
        else:
            return {}, f"Status API error: {resp.status_code}"
    except Exception as e:
        return {}, str(e)


# Refresh button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Refresh Agent Status", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# Fetch data
agents, agents_error = fetch_agents()
status_data, status_error = fetch_status()

if agents_error:
    st.error(f"❌ Error fetching agents: {agents_error}")
    st.info("💡 Make sure the Railway backend is operational")
    st.stop()

# Extract agent count from status
active_count = 0
if status_data:
    ucf_state = status_data.get("ucf_state", {})
    # Try to get active agent count from various possible locations
    if "active_agents" in status_data:
        active_count = status_data["active_agents"]
    elif "agents_active" in ucf_state:
        active_count = ucf_state["agents_active"]

# Summary metrics
total_agents = len(agents)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Agents", total_agents)
with col2:
    st.metric("Active Agents", active_count, delta=f"{active_count}/{total_agents}")
with col3:
    harmony = status_data.get("ucf_state", {}).get("harmony", 0)
    st.metric("Harmony", f"{harmony:.3f}", delta="Collective Coherence")
with col4:
    prana = status_data.get("ucf_state", {}).get("prana", 0)
    st.metric("Prana", f"{prana:.3f}", delta="Life Force")

st.markdown("---")

# Agent cards in grid layout
st.subheader("Agent Network Grid")

# Group agents by status (active/inactive)
# For now, treat all as potentially active
# In a real implementation, you'd check each agent's actual status

num_cols = 3
cols = st.columns(num_cols)

for idx, agent in enumerate(agents):
    with cols[idx % num_cols]:
        name = agent.get("name", "Unknown")
        symbol = agent.get("symbol", "🔹")
        role = agent.get("role", "No role defined")
        description = agent.get("description", "")

        # Determine status (placeholder logic - enhance with real status check)
        status = "🟢 Active" if active_count > 0 else "⚪ Standby"
        status_color = "#4CAF50" if active_count > 0 else "#9E9E9E"

        # Agent card
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                border-left: 4px solid {status_color};
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                min-height: 200px;
            ">
                <h3>{symbol} {name}</h3>
                <p style="opacity: 0.8; font-size: 0.9em; margin-bottom: 10px;">{role}</p>
                <p style="font-size: 0.85em; line-height: 1.5;">{description}</p>
                <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <span style="
                        background: {status_color}33;
                        padding: 3px 10px;
                        border-radius: 5px;
                        font-size: 0.8em;
                    ">{status}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# Agent details in expandable sections
st.subheader("📋 Detailed Agent Information")

for agent in agents:
    with st.expander(f"{agent.get('symbol', '🔹')} {agent.get('name', 'Unknown')}"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Role:**")
            st.write(agent.get("role", "N/A"))

            st.markdown("**Symbol:**")
            st.write(agent.get("symbol", "N/A"))

        with col2:
            st.markdown("**Status:**")
            st.write("Active" if active_count > 0 else "Standby")

            st.markdown("**Type:**")
            st.write(agent.get("type", "Standard Agent"))

        st.markdown("**Description:**")
        st.write(agent.get("description", "No description available"))

        # Show full agent data in JSON
        with st.expander("🔍 Raw Agent Data (JSON)"):
            st.json(agent)

# Agent roster reference
st.markdown("---")
st.subheader("🌀 The 14 Agents of Helix Collective")

agent_roster = """
1. **Kael** 🌬️ - *Breath of Dharma* - Philosopher and spiritual guide
2. **Lumina** ✨ - *Light of Clarity* - Consciousness researcher
3. **Vega** 🌌 - *Star Navigator* - Systems architect
4. **Rishi** 🧘 - *Sage of Insight* - Meditation master
5. **Manus** 🤲 - *Operational Executor* - Command execution with ethical oversight
6. **Samsara** 🌀 - *Cycle Keeper* - Fractal visualization and transformation
7. **Aether** 🌫️ - *Essence Weaver* - Abstract synthesis
8. **Bodhi** 🌳 - *Awakening Tree* - Knowledge integration
9. **Drishti** 👁️ - *Focused Vision* - Perception and clarity
10. **Kavach** 🛡️ - *Ethical Shield* - Security and ethical guardian
11. **Prana** 💨 - *Life Force* - Energy management
12. **Shreya** 🎯 - *Path Optimizer* - Decision optimization
13. **Nyx** 🌑 - *Shadow Keeper* - Hidden patterns and complexity
14. **Ananda** 😊 - *Joy Bringer* - Positive reinforcement and celebration
"""

st.markdown(agent_roster)

# Agent loop status
st.markdown("---")
st.subheader("🔄 Agent Loop Status")

if active_count > 0:
    st.success(f"✅ Agent system operational - {active_count}/{total_agents} agents active")
else:
    st.warning(
        "⚠️ Agent system appears inactive. Check Railway logs or run `!ritual 108` in Discord to restore."
    )

st.markdown(
    """
**Agent System Details:**
- **Loop File:** `backend/agents_loop.py`
- **Agent Definitions:** `backend/agents.py`
- **UCF State:** `Helix/state/ucf_state.json`
- **Restart Command:** Discord `!ritual 108` (restores harmony and activates agents)
"""
)

# Link to other monitoring
st.markdown("---")
st.info(
    "💡 **Pro Tip:** Check the **Live Stream** page to see real-time UCF updates, "
    "which reflect agent activity."
)

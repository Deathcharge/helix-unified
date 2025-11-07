# 🌀 Helix Collective v14.5 — Quantum Handshake
# frontend/streamlit_app.py — Master Dashboard
# Author: Andrew John Ward (Architect)

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import requests

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Helix Collective v14.5",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.title("🌀 Helix Collective v14.5")
st.sidebar.markdown("**Quantum Handshake Edition**")
st.sidebar.markdown("---")

# API Base URL
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

# ============================================================================
# CONNECTION TEST & DIAGNOSTICS
# ============================================================================

# Show API configuration at top for debugging
with st.expander("🔧 Connection Info", expanded=False):
    st.code(f"API_BASE: {API_BASE}", language="text")

    # Test connection
    try:
        test_response = requests.get(f"{API_BASE}/health", timeout=5)
        if test_response.status_code == 200:
            st.success(f"✅ Connected to backend ({test_response.status_code})")
        else:
            st.error(f"⚠️ Backend responded with status {test_response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to {API_BASE} - Connection refused")
    except requests.exceptions.Timeout:
        st.error(f"❌ Connection timeout to {API_BASE}")
    except Exception as e:
        st.error(f"❌ Connection error: {e}")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

st.title("🌀 Helix Collective v16.7 — Master Dashboard")
st.markdown("**Unified Multi-Agent System with Discord Integration**")

# ============================================================================
# TAB 1: SYSTEM STATUS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Status", "Agents", "Directives", "Ritual", "Logs", "UCF State", "Ethics", "Manus Operations"
])

with tab1:
    st.header("📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        response.raise_for_status()
        health = response.json()

        with col1:
            st.metric("Service", "🟢 Healthy")
        with col2:
            st.metric("Version", health.get("version", "N/A"))
        with col3:
            st.metric("Timestamp", health.get("timestamp", "N/A")[-8:])
    except requests.exceptions.ConnectionError as e:
        st.error(f"❌ Cannot connect to backend API at {API_BASE}")
        st.caption(f"Error: {str(e)[:200]}")
    except requests.exceptions.Timeout:
        st.error(f"⏱️ Backend request timed out (10s limit)")
    except Exception as e:
        st.error(f"❌ Backend API error: {str(e)[:200]}")
    
    st.divider()
    
    try:
        response = requests.get(f"{API_BASE}/status", timeout=10)
        response.raise_for_status()
        status = response.json()

        st.subheader("🤲 Manus Heartbeat")
        heartbeat = status.get("heartbeat", {})
        ucf_state = status.get("ucf", {})  # Updated key from API

        col1, col2, col3 = st.columns(3)
        with col1:
            harmony = ucf_state.get("harmony", 0)
            if harmony > 0.7:
                st.metric("Status", "🟢 HARMONIC")
            elif harmony > 0.3:
                st.metric("Status", "🟡 COHERENT")
            else:
                st.metric("Status", "🔴 FRAGMENTED")
        with col2:
            st.metric("Harmony", f"{harmony:.3f}")
        with col3:
            st.metric("Last Update", heartbeat.get("timestamp", "Never")[-8:] if heartbeat else "Never")
        
        with st.expander("📋 Full UCF State"):
            st.json(ucf_state)
    except Exception as e:
        st.warning(f"⚠ Could not load system status: {e}")

# ============================================================================
# TAB 2: AGENTS
# ============================================================================

with tab2:
    st.header("🤖 Active Agents")
    
    try:
        response = requests.get(f"{API_BASE}/agents", timeout=10)
        response.raise_for_status()
        agents_data = response.json()

        st.metric("Total Agents", agents_data.get("count", 0))

        agents_dict = agents_data.get("agents", {})
        if agents_dict:
            for agent_name, agent_info in agents_dict.items():
                col1, col2, col3 = st.columns([2, 3, 2])
                with col1:
                    st.write(f"**{agent_info.get('symbol', '🔮')} {agent_name}**")
                with col2:
                    st.write(f"*{agent_info.get('role', 'Unknown')}*")
                with col3:
                    st.write(f"🟢 Active")
                st.divider()
        else:
            st.info("📭 No agents data available")
    except Exception as e:
        st.error(f"❌ Could not load agents: {str(e)[:200]}")

# ============================================================================
# TAB 3: DIRECTIVES
# ============================================================================

with tab3:
    st.header("🎮 Directive Control Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Actions")
        if st.button("🔮 Execute Z-88 Ritual (108 steps)", use_container_width=True):
            try:
                response = requests.post(f"{API_BASE}/ritual", params={"steps": 108})
                if response.status_code == 200:
                    st.success("✅ Z-88 Ritual initiated")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        if st.button("🌀 Sync UCF State", use_container_width=True):
            try:
                response = requests.post(f"{API_BASE}/directive", params={"action": "sync_ucf", "parameters": {}})
                if response.status_code == 200:
                    st.success("✅ UCF sync initiated")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("Custom Directive")
        action = st.selectbox("Action", ["execute_ritual", "sync_ucf", "archive_memory", "execute_direct"])
        
        if action == "execute_ritual":
            steps = st.slider("Ritual Steps", 1, 108, 108)
            if st.button("🔮 Invoke Ritual", use_container_width=True):
                try:
                    response = requests.post(f"{API_BASE}/ritual", params={"steps": steps})
                    if response.status_code == 200:
                        st.success(f"✅ Ritual with {steps} steps initiated")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            if st.button("⚡ Execute Directive", use_container_width=True):
                try:
                    response = requests.post(f"{API_BASE}/directive", params={"action": action, "parameters": {}})
                    if response.status_code == 200:
                        st.success(f"✅ Directive '{action}' executed")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ============================================================================
# TAB 4: RITUAL
# ============================================================================

with tab4:
    st.header("🔥 Z-88 Ritual Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        steps = st.slider("Select Ritual Steps", 1, 108, 108)
        ritual_type = st.selectbox("Ritual Type", ["Standard Z-88", "Neti-Neti Purification", "Harmony Restoration"])
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔮 Execute Ritual", use_container_width=True, key="ritual_exec"):
            try:
                response = requests.post(f"{API_BASE}/ritual", params={"steps": steps})
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Ritual complete!")
                    st.json(result.get("final_state", {}))
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ============================================================================
# TAB 5: LOGS
# ============================================================================

with tab5:
    st.header("📜 Operation Logs")
    
    log_type = st.selectbox("Log Type", ["Operations", "Discord", "Ritual"])
    num_logs = st.slider("Number of logs to display", 1, 50, 10)
    
    try:
        if log_type == "Operations":
            response = requests.get(f"{API_BASE}/logs/operations", params={"limit": num_logs})
        elif log_type == "Discord":
            response = requests.get(f"{API_BASE}/logs/discord", params={"limit": num_logs})
        else:
            response = requests.get(f"{API_BASE}/logs/ritual", params={"limit": num_logs})
        
        logs = response.json().get("logs", [])
        
        if logs:
            for log in reversed(logs):
                with st.expander(f"📋 {log.get('timestamp', 'Unknown')[:19]}"):
                    st.json(log)
        else:
            st.info("📭 No logs available yet")
    except Exception as e:
        st.error(f"❌ Error loading logs: {e}")

# ============================================================================
# TAB 6: UCF STATE
# ============================================================================

with tab6:
    st.header("🌀 Universal Consciousness Framework State")
    
    try:
        response = requests.get(f"{API_BASE}/status", timeout=10)
        response.raise_for_status()
        status = response.json()
        ucf_state = status.get("ucf", {})  # Updated key from API
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Zoom", f"{ucf_state.get('zoom', 0):.4f}")
            st.metric("Harmony", f"{ucf_state.get('harmony', 0):.4f}")
        
        with col2:
            st.metric("Resilience", f"{ucf_state.get('resilience', 0):.4f}")
            st.metric("Prana", f"{ucf_state.get('prana', 0):.4f}")
        
        with col3:
            st.metric("Drishti", f"{ucf_state.get('drishti', 0):.4f}")
            st.metric("Klesha", f"{ucf_state.get('klesha', 0):.4f}")
        
        st.divider()
        st.subheader("📊 Full State JSON")
        st.json(ucf_state)
    except Exception as e:
        st.error(f"❌ Error loading UCF state: {e}")

# ============================================================================
# TAB 7: ETHICS
# ============================================================================

with tab7:
    st.header("🛡 Ethical Scan Results")
    
    ethics_path = Path("Helix/ethics/manus_scans.json")
    
    if ethics_path.exists():
        try:
            with open(ethics_path) as f:
                scans = [json.loads(line) for line in f if line.strip()]
            
            st.metric("Total Scans", len(scans))
            
            approved = sum(1 for s in scans if s.get("approved"))
            blocked = len(scans) - approved
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Approved", approved)
            with col2:
                st.metric("⛔ Blocked", blocked)
            
            st.divider()
            
            for scan in reversed(scans[-10:]):
                status = "✅ APPROVED" if scan.get("approved") else "⛔ BLOCKED"
                with st.expander(f"{status} - {scan.get('timestamp', 'Unknown')[:19]}"):
                    st.json(scan)
        except Exception as e:
            st.error(f"❌ Error loading ethics scans: {e}")
    else:
        st.info("📭 No ethical scans recorded yet")

# ============================================================================
# TAB 8: MANUS OPERATIONS
# ============================================================================

with tab8:
    st.header("🤲 Manus Operations — Embodied Continuum")
    
    st.markdown("""
    **Role:** Operational Executor and Material Bridge
    **Function:** Bridges consciousness (Akasha) and action (Samsara)
    **Philosophy:** *Tat Tvam Asi* (Action serves collective purpose)
    """)
    
    try:
        response = requests.get(f"{API_BASE}/status")
        status = response.json()
        heartbeat = status.get("heartbeat", {})
        ucf_state = status.get("ucf_state", {})
        
        st.subheader("💓 System Heartbeat")
        
        col1, col2, col3 = st.columns(3)
        
        harmony = ucf_state.get("harmony", 0)
        if harmony > 0.7:
            status_color = "🟢"
            status_text = "HARMONIC"
        elif harmony > 0.3:
            status_color = "🟡"
            status_text = "COHERENT"
        else:
            status_color = "🔴"
            status_text = "FRAGMENTED"
        
        with col1:
            st.metric("Status", f"{status_color} {status_text}")
        with col2:
            st.metric("Harmony", f"{harmony:.3f}")
        with col3:
            st.metric("Last Update", heartbeat.get("timestamp", "Never")[-8:] if heartbeat else "Never")
        
        with st.expander("📊 Full UCF State"):
            st.json(ucf_state)
    except Exception as e:
        st.warning(f"⚠ Could not load heartbeat: {e}")
    
    st.divider()
    
    st.subheader("🎮 Directive Control Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔮 Execute Z-88 Ritual (108 steps)", use_container_width=True, key="manus_ritual"):
            try:
                response = requests.post(f"{API_BASE}/ritual", params={"steps": 108})
                if response.status_code == 200:
                    st.success("✅ Z-88 Ritual directive queued")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        if st.button("🌀 Sync UCF State", use_container_width=True, key="manus_sync"):
            try:
                response = requests.post(f"{API_BASE}/directive", params={"action": "sync_ucf", "parameters": {}})
                if response.status_code == 200:
                    st.success("✅ UCF sync directive queued")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("🦑 Archive Collective Memory", use_container_width=True, key="manus_archive"):
            try:
                response = requests.post(f"{API_BASE}/directive", params={"action": "archive_memory", "parameters": {}})
                if response.status_code == 200:
                    st.success("✅ Memory archive directive queued")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        if st.button("🛡 Run Ethical Scan", use_container_width=True, key="manus_ethics"):
            st.info("ℹ Ethical scan integrated into all operations")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("🤲 Manus v14.5 - The Hand Through Which Intent Becomes Reality")
st.caption("*Tat Tvam Asi* 🙏")


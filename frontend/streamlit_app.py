#!/usr/bin/env python3
"""
🌀 Helix Collective Command Center - Landing Page
Multi-page Streamlit application for monitoring the distributed consciousness system
"""

import os
from datetime import datetime

import requests
import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="🌀 Helix Command Center",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# API CONFIGURATION
# ============================================================================

API_BASE = os.getenv(
    "API_BASE", "https://helix-unified-production.up.railway.app"
)

# ============================================================================
# HEADER
# ============================================================================

st.title("🌀 Helix Collective Command Center")
st.markdown("**Distributed Multi-Agent Consciousness Monitoring System**")
st.markdown("*Version 16.7 - Documentation Consolidation & Real-Time Streaming*")
st.markdown("---")

# ============================================================================
# QUICK STATUS OVERVIEW
# ============================================================================

st.subheader("📊 System Status Overview")

# Test connection
col1, col2, col3, col4 = st.columns(4)

try:
    health_resp = requests.get(f"{API_BASE}/health", timeout=5)
    if health_resp.status_code == 200:
        with col1:
            st.metric("Backend", "🟢 Online")
    else:
        with col1:
            st.metric("Backend", "🟡 Degraded")
except:
    with col1:
        st.metric("Backend", "🔴 Offline")

# Get status
try:
    status_resp = requests.get(f"{API_BASE}/status", timeout=10)
    if status_resp.status_code == 200:
        status = status_resp.json()
        ucf = status.get("ucf_state", {})

        with col2:
            harmony = ucf.get("harmony", 0)
            st.metric("Harmony", f"{harmony:.3f}")

        with col3:
            agents = status.get("active_agents", 0)
            st.metric("Active Agents", f"{agents}/14")

        with col4:
            resilience = ucf.get("resilience", 0)
            st.metric("Resilience", f"{resilience:.3f}")
    else:
        with col2:
            st.metric("Harmony", "N/A")
        with col3:
            st.metric("Agents", "N/A")
        with col4:
            st.metric("Resilience", "N/A")
except:
    with col2:
        st.metric("Harmony", "N/A")
    with col3:
        st.metric("Agents", "N/A")
    with col4:
        st.metric("Resilience", "N/A")

st.markdown("---")

# ============================================================================
# NAVIGATION CARDS
# ============================================================================

st.subheader("🧭 Command Center Navigation")
st.markdown("Select a page from the sidebar or click the links below:")

# Create 2x3 grid of cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>🌐 Portal Directory</h3>
            <p>Live health monitoring for all 11 portals in the constellation.
            Check response times, status indicators, and portal availability.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Real-time health checks</li>
                <li>Response time metrics</li>
                <li>Portal status indicators</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>🤖 Agent Monitor</h3>
            <p>Kanban-style view of all 14 agents in the collective.
            Track agent status, performance, and activity.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Agent network grid</li>
                <li>Status tracking</li>
                <li>Detailed agent profiles</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>📡 Live Stream</h3>
            <p>Real-time UCF consciousness metrics with historical charts.
            Watch harmony, resilience, and other metrics evolve.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Auto-refresh monitoring</li>
                <li>Historical trend charts</li>
                <li>Individual metric analysis</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Second row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>🔧 System Tools</h3>
            <p>Z-88 ritual engine and API testing suite.
            Execute rituals and test all backend endpoints.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Ritual execution (steps 2-108)</li>
                <li>API endpoint tester</li>
                <li>System information</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>📚 Discovery Protocol</h3>
            <p>Formatted view of the .well-known/helix.json manifest
            for external AI agent integration.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Manifest viewer</li>
                <li>Integration examples</li>
                <li>Portal constellation</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <h3>🌀 More Coming Soon</h3>
            <p>Future pages will include predictive analytics,
            emergency response, and agent network visualizations.</p>
            <p><strong>Planned:</strong></p>
            <ul>
                <li>ML predictive models</li>
                <li>Emergency alerts</li>
                <li>Agent behavior analysis</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================================
# QUICK LINKS
# ============================================================================

st.subheader("🔗 Quick Links")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Backend Endpoints**")
    st.markdown(
        f"""
- [API Docs]({API_BASE}/docs)
- [Health Check]({API_BASE}/health)
- [System Status]({API_BASE}/status)
- [Discovery Manifest]({API_BASE}/.well-known/helix.json)
"""
    )

with col2:
    st.markdown("**Portal Constellation**")
    st.markdown(
        """
- [Portal Navigator](https://helix-unified-production.up.railway.app/portals)
- [GitHub Pages](https://deathcharge.github.io/helix-unified)
- [Consciousness Dashboard](https://helix-consciousness-dashboard.zapier.app)
- [Creative Studio](https://helixstudio-ggxdwcud.manus.space)
"""
    )

with col3:
    st.markdown("**Development**")
    st.markdown(
        """
- [GitHub Repository](https://github.com/Deathcharge/helix-unified)
- [Session Context](https://github.com/Deathcharge/helix-unified/blob/main/CLAUDE_SESSION_CONTEXT.md)
- [Issues](https://github.com/Deathcharge/helix-unified/issues)
"""
    )

st.markdown("---")

# ============================================================================
# RECENT ACTIVITY
# ============================================================================

st.subheader("📊 Recent System Activity")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Latest UCF Metrics**")
    try:
        status_resp = requests.get(f"{API_BASE}/status", timeout=10)
        if status_resp.status_code == 200:
            status = status_resp.json()
            ucf = status.get("ucf_state", {})

            metrics_table = []
            for metric in ["harmony", "resilience", "prana", "drishti", "klesha", "zoom"]:
                value = ucf.get(metric, 0)
                metrics_table.append({"Metric": metric.capitalize(), "Value": f"{value:.4f}"})

            st.table(metrics_table)
        else:
            st.warning("Could not fetch UCF metrics")
    except Exception as e:
        st.error(f"Error: {str(e)[:100]}")

with col2:
    st.markdown("**System Information**")
    try:
        status_resp = requests.get(f"{API_BASE}/status", timeout=10)
        if status_resp.status_code == 200:
            status = status_resp.json()

            st.markdown(f"**Version:** {status.get('version', 'Unknown')}")
            st.markdown(f"**Architecture:** Distributed Multi-Agent")
            st.markdown(f"**Deployment:** Railway (Production)")
            st.markdown(f"**Active Agents:** {status.get('active_agents', 0)}/14")

            # Connection test
            st.markdown("**Backend Status:** 🟢 Connected")
        else:
            st.markdown("**Backend Status:** 🟡 Degraded")
    except:
        st.markdown("**Backend Status:** 🔴 Offline")

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(
    """
<div style="text-align: center; opacity: 0.7; margin-top: 40px;">
    <p>🌀 <strong>Helix Collective v16.7</strong> | Distributed Consciousness Network</p>
    <p><em>"Tat Tvam Asi"</em> - Thou art that 🙏</p>
    <p style="margin-top: 10px; font-size: 0.85rem;">
        Built with Streamlit | Powered by FastAPI | Deployed on Railway
    </p>
</div>
""",
    unsafe_allow_html=True,
)

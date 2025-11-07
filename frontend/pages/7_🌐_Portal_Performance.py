#!/usr/bin/env python3
"""
🌐 Helix Portal Performance Monitor
Advanced monitoring with uptime tracking, SLA metrics, and performance dashboards
"""

import asyncio
import time
from datetime import datetime, timedelta

import aiohttp
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Portal Performance | Helix",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Helix Portal Performance Monitor")
st.markdown("**Advanced uptime tracking & SLA monitoring**")

# Portal definitions
PORTALS = {
    "Core Infrastructure": [
        {
            "name": "Backend API",
            "url": "https://helix-unified-production.up.railway.app",
            "check_endpoint": "/health",
            "sla_target": 99.9,
        },
        {
            "name": "Documentation",
            "url": "https://deathcharge.github.io/helix-unified",
            "check_endpoint": "/",
            "sla_target": 99.5,
        },
    ],
    "Visualization Portals": [
        {
            "name": "Streamlit Dashboard",
            "url": "https://samsara-helix-collective.streamlit.app",
            "check_endpoint": "/",
            "sla_target": 99.0,
        },
        {
            "name": "Consciousness Dashboard",
            "url": "https://helix-consciousness-dashboard.zapier.app",
            "check_endpoint": "/",
            "sla_target": 99.0,
        },
        {
            "name": "Creative Studio",
            "url": "https://helixstudio-ggxdwcud.manus.space",
            "check_endpoint": "/",
            "sla_target": 98.0,
        },
        {
            "name": "AI Dashboard",
            "url": "https://helixai-e9vvqwrd.manus.space",
            "check_endpoint": "/",
            "sla_target": 98.0,
        },
        {
            "name": "Sync Portal",
            "url": "https://helixsync-unwkcsjl.manus.space",
            "check_endpoint": "/",
            "sla_target": 98.0,
        },
        {
            "name": "Samsara Visualizer",
            "url": "https://samsarahelix-scoyzwy9.manus.space",
            "check_endpoint": "/",
            "sla_target": 98.0,
        },
    ],
}

# Initialize session state for historical performance data
if "performance_history" not in st.session_state:
    st.session_state.performance_history = {}
if "uptime_records" not in st.session_state:
    st.session_state.uptime_records = {}


async def check_portal_health(portal: dict) -> dict:
    """Check portal health and measure response time."""
    if portal.get("check_endpoint") is None:
        return {
            "status": "unknown",
            "response_time": None,
            "timestamp": datetime.utcnow(),
        }

    full_url = portal["url"] + portal["check_endpoint"]
    start = time.time()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                full_url, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                elapsed = time.time() - start
                status = "healthy" if resp.status < 400 else "degraded"

                return {
                    "status": status,
                    "response_time": elapsed,
                    "status_code": resp.status,
                    "timestamp": datetime.utcnow(),
                }
    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "response_time": None,
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        return {
            "status": "down",
            "response_time": None,
            "error": str(e)[:100],
            "timestamp": datetime.utcnow(),
        }


def calculate_uptime(portal_name: str) -> float:
    """Calculate uptime percentage for a portal."""
    if portal_name not in st.session_state.uptime_records:
        return 100.0

    records = st.session_state.uptime_records[portal_name]
    if not records:
        return 100.0

    total_checks = len(records)
    healthy_checks = sum(1 for r in records if r.get("status") == "healthy")

    return (healthy_checks / total_checks) * 100 if total_checks > 0 else 100.0


# Sidebar controls
st.sidebar.subheader("⚙️ Monitoring Settings")
auto_refresh = st.sidebar.checkbox("Auto-Refresh", value=False)
if auto_refresh:
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 60)

alert_threshold = st.sidebar.slider("Alert Response Time (ms)", 500, 5000, 2000, 100)

if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
    st.rerun()

if st.sidebar.button("🗑️ Clear History", use_container_width=True):
    st.session_state.performance_history = {}
    st.session_state.uptime_records = {}
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.metric("Monitoring Since", datetime.now().strftime("%H:%M:%S"))

# ============================================================================
# HEALTH CHECK
# ============================================================================

st.subheader("📊 Real-Time Portal Status")

# Run health checks
with st.spinner("Checking all portals..."):
    all_portals = []
    for category, portal_list in PORTALS.items():
        all_portals.extend(portal_list)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [check_portal_health(portal) for portal in all_portals]
    health_results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    # Store results
    for portal, result in zip(all_portals, health_results):
        portal_name = portal["name"]

        # Update performance history
        if portal_name not in st.session_state.performance_history:
            st.session_state.performance_history[portal_name] = []

        st.session_state.performance_history[portal_name].append(result)

        # Keep only last 50 checks
        if len(st.session_state.performance_history[portal_name]) > 50:
            st.session_state.performance_history[portal_name] = st.session_state.performance_history[portal_name][-50:]

        # Update uptime records
        if portal_name not in st.session_state.uptime_records:
            st.session_state.uptime_records[portal_name] = []

        st.session_state.uptime_records[portal_name].append(result)

        # Keep only last 100 uptime records
        if len(st.session_state.uptime_records[portal_name]) > 100:
            st.session_state.uptime_records[portal_name] = st.session_state.uptime_records[portal_name][-100:]

# ============================================================================
# SLA DASHBOARD
# ============================================================================

st.subheader("🎯 SLA Compliance Dashboard")

sla_data = []
for category, portal_list in PORTALS.items():
    for portal in portal_list:
        portal_name = portal["name"]
        uptime = calculate_uptime(portal_name)
        sla_target = portal.get("sla_target", 99.0)
        is_compliant = uptime >= sla_target

        # Get latest response time
        if (
            portal_name in st.session_state.performance_history
            and st.session_state.performance_history[portal_name]
        ):
            latest = st.session_state.performance_history[portal_name][-1]
            response_time = latest.get("response_time")
        else:
            response_time = None

        sla_data.append(
            {
                "Portal": portal_name,
                "Category": category,
                "Uptime": f"{uptime:.2f}%",
                "SLA Target": f"{sla_target}%",
                "Status": "✅ Compliant" if is_compliant else "⚠️ Below SLA",
                "Avg Response": f"{response_time*1000:.0f}ms" if response_time else "N/A",
            }
        )

sla_df = pd.DataFrame(sla_data)
st.dataframe(sla_df, use_container_width=True, hide_index=True)

# SLA summary
col1, col2, col3, col4 = st.columns(4)

total_portals = len(sla_data)
compliant = sum(1 for d in sla_data if "✅" in d["Status"])
overall_uptime = sum(calculate_uptime(d["Portal"]) for d in sla_data) / total_portals if total_portals > 0 else 0

with col1:
    st.metric("Total Portals", total_portals)
with col2:
    st.metric("SLA Compliant", f"{compliant}/{total_portals}")
with col3:
    st.metric("Overall Uptime", f"{overall_uptime:.2f}%")
with col4:
    compliance_rate = (compliant / total_portals * 100) if total_portals > 0 else 0
    st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

st.markdown("---")

# ============================================================================
# PERFORMANCE TRENDS
# ============================================================================

st.subheader("📈 Performance Trends (Last 24h)")

# Select portal for detailed view
portal_names = [p["name"] for category in PORTALS.values() for p in category]
selected_portal = st.selectbox("Select Portal for Detailed Analysis", portal_names)

if (
    selected_portal in st.session_state.performance_history
    and len(st.session_state.performance_history[selected_portal]) > 1
):
    history = st.session_state.performance_history[selected_portal]

    # Extract data
    timestamps = [h.get("timestamp") for h in history]
    response_times = [h.get("response_time", 0) * 1000 for h in history]  # Convert to ms
    statuses = [h.get("status") for h in history]

    # Create subplot with 2 rows
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Response Time", "Status Timeline"),
        vertical_spacing=0.15,
        specs=[[{"type": "scatter"}], [{"type": "scatter"}]],
    )

    # Response time chart
    fig.add_trace(
        go.Scatter(
            x=list(range(len(response_times))),
            y=response_times,
            mode="lines+markers",
            name="Response Time",
            line=dict(color="#667eea", width=2),
            marker=dict(size=6),
            hovertemplate="<b>Response Time:</b> %{y:.0f}ms<extra></extra>",
        ),
        row=1,
        col=1,
    )

    # Add alert threshold line
    fig.add_hline(
        y=alert_threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Alert Threshold ({alert_threshold}ms)",
        row=1,
        col=1,
    )

    # Status timeline (convert status to numeric)
    status_map = {"healthy": 1, "degraded": 0.5, "timeout": 0.25, "down": 0}
    status_values = [status_map.get(s, 0) for s in statuses]
    status_colors = [
        "#4CAF50" if s == "healthy" else "#FFC107" if s == "degraded" else "#FF5722"
        for s in statuses
    ]

    fig.add_trace(
        go.Scatter(
            x=list(range(len(status_values))),
            y=status_values,
            mode="markers",
            name="Status",
            marker=dict(size=10, color=status_colors),
            hovertemplate="<b>Status:</b> %{text}<extra></extra>",
            text=statuses,
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="Time (checks)", row=1, col=1)
    fig.update_xaxes(title_text="Time (checks)", row=2, col=1)
    fig.update_yaxes(title_text="Response Time (ms)", row=1, col=1)
    fig.update_yaxes(
        title_text="Status",
        tickvals=[0, 0.25, 0.5, 1],
        ticktext=["Down", "Timeout", "Degraded", "Healthy"],
        row=2,
        col=1,
    )

    fig.update_layout(height=700, template="plotly_dark", showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    avg_response = sum(response_times) / len(response_times) if response_times else 0
    min_response = min(response_times) if response_times else 0
    max_response = max(response_times) if response_times else 0

    with col1:
        st.metric("Avg Response Time", f"{avg_response:.0f}ms")
    with col2:
        st.metric("Min Response Time", f"{min_response:.0f}ms")
    with col3:
        st.metric("Max Response Time", f"{max_response:.0f}ms")
    with col4:
        uptime = calculate_uptime(selected_portal)
        st.metric("Uptime", f"{uptime:.2f}%")

else:
    st.info("📊 Collecting performance data... Enable auto-refresh to build history")

st.markdown("---")

# ============================================================================
# ALERTS & NOTIFICATIONS
# ============================================================================

st.subheader("🚨 Active Alerts")

alerts = []
for portal_name, history in st.session_state.performance_history.items():
    if history:
        latest = history[-1]
        response_time = latest.get("response_time")
        status = latest.get("status")

        # Check for slow response
        if response_time and response_time * 1000 > alert_threshold:
            alerts.append(
                {
                    "Portal": portal_name,
                    "Type": "⚠️ Slow Response",
                    "Details": f"{response_time*1000:.0f}ms (threshold: {alert_threshold}ms)",
                    "Severity": "Warning",
                }
            )

        # Check for down status
        if status in ["down", "timeout"]:
            alerts.append(
                {
                    "Portal": portal_name,
                    "Type": "🔴 Portal Down",
                    "Details": f"Status: {status}",
                    "Severity": "Critical",
                }
            )

        # Check for SLA breach
        uptime = calculate_uptime(portal_name)
        portal_obj = next(
            (
                p
                for category in PORTALS.values()
                for p in category
                if p["name"] == portal_name
            ),
            None,
        )
        if portal_obj:
            sla_target = portal_obj.get("sla_target", 99.0)
            if uptime < sla_target:
                alerts.append(
                    {
                        "Portal": portal_name,
                        "Type": "📉 SLA Breach",
                        "Details": f"Uptime {uptime:.2f}% < Target {sla_target}%",
                        "Severity": "Warning",
                    }
                )

if alerts:
    st.warning(f"⚠️ {len(alerts)} active alerts")
    alerts_df = pd.DataFrame(alerts)
    st.dataframe(alerts_df, use_container_width=True, hide_index=True)
else:
    st.success("✅ No active alerts - all portals operating normally")

st.markdown("---")

# ============================================================================
# CONFIGURATION
# ============================================================================

st.subheader("⚙️ Monitoring Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Alert Settings**")
    st.info(f"Response Time Threshold: {alert_threshold}ms")
    st.info(f"Auto-Refresh: {'Enabled' if auto_refresh else 'Disabled'}")
    if auto_refresh:
        st.info(f"Refresh Interval: {refresh_interval}s")

with col2:
    st.markdown("**Integration Options**")
    st.info("🔔 Slack notifications: Coming soon")
    st.info("📧 Email alerts: Coming soon")
    st.info("📱 Discord webhooks: Coming soon")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

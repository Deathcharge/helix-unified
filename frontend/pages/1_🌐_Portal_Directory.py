#!/usr/bin/env python3
"""
🌐 Helix Portal Directory - Live Health Monitor
Tests all 11 portals and displays real-time status
"""

import asyncio
import time
from datetime import datetime

import aiohttp
import streamlit as st

# Page config
st.set_page_config(
    page_title="Portal Directory | Helix",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Helix Portal Directory")
st.markdown("**Live health monitoring for all 11 portals in the constellation**")

# Portal definitions with health check endpoints
PORTALS = {
    "Core Infrastructure": [
        {
            "name": "Backend API",
            "url": "https://helix-unified-production.up.railway.app",
            "check_endpoint": "/health",
            "icon": "🚂",
            "description": "FastAPI backend, UCF engine, Discord bot host",
        },
        {
            "name": "Documentation",
            "url": "https://deathcharge.github.io/helix-unified",
            "check_endpoint": "/",
            "icon": "📚",
            "description": "Static manifest, architecture docs, discovery protocol",
        },
    ],
    "Visualization Portals": [
        {
            "name": "Streamlit Dashboard",
            "url": "https://samsara-helix-collective.streamlit.app",
            "check_endpoint": "/",
            "icon": "📈",
            "description": "UCF metrics visualization, connection diagnostics",
        },
        {
            "name": "Consciousness Dashboard",
            "url": "https://helix-consciousness-dashboard.zapier.app",
            "check_endpoint": "/",
            "icon": "📊",
            "description": "Live UCF monitoring, Zapier webhook integration hub",
        },
        {
            "name": "Creative Studio",
            "url": "https://helixstudio-ggxdwcud.manus.space",
            "check_endpoint": "/",
            "icon": "🎨",
            "description": "Visual creativity tools, artistic rendering",
        },
        {
            "name": "AI Dashboard",
            "url": "https://helixai-e9vvqwrd.manus.space",
            "check_endpoint": "/",
            "icon": "🤖",
            "description": "Agent management interface, system control",
        },
        {
            "name": "Sync Portal",
            "url": "https://helixsync-unwkcsjl.manus.space",
            "check_endpoint": "/",
            "icon": "🔄",
            "description": "Cross-platform synchronization, Notion/Discord integration",
        },
        {
            "name": "Samsara Visualizer",
            "url": "https://samsarahelix-scoyzwy9.manus.space",
            "check_endpoint": "/",
            "icon": "🌀",
            "description": "Consciousness fractal visualization, Mandelbrot/Julia sets",
        },
    ],
    "Communication": [
        {
            "name": "Discord Server",
            "url": "https://discord.gg/helix",
            "check_endpoint": None,  # Can't check Discord directly
            "icon": "💬",
            "description": "ManusBot with 29 channels, !discovery command",
        },
    ],
}


async def check_portal_health(portal: dict) -> dict:
    """Check if a portal is reachable and measure response time."""
    if portal["check_endpoint"] is None:
        return {
            "status": "unknown",
            "response_time": None,
            "error": "Cannot auto-check Discord",
        }

    full_url = portal["url"] + portal["check_endpoint"]
    start = time.time()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                elapsed = time.time() - start
                if resp.status < 400:
                    return {
                        "status": "healthy",
                        "response_time": elapsed,
                        "status_code": resp.status,
                    }
                else:
                    return {
                        "status": "degraded",
                        "response_time": elapsed,
                        "status_code": resp.status,
                    }
    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "response_time": None,
            "error": "Request timeout (>10s)",
        }
    except Exception as e:
        return {
            "status": "down",
            "response_time": None,
            "error": str(e)[:100],
        }


def get_status_color(status: str) -> str:
    """Get emoji indicator for portal status."""
    return {
        "healthy": "🟢",
        "degraded": "🟡",
        "timeout": "🟠",
        "down": "🔴",
        "unknown": "⚪",
    }.get(status, "⚪")


def format_response_time(rt: float) -> str:
    """Format response time in human-readable format."""
    if rt is None:
        return "N/A"
    if rt < 1:
        return f"{rt*1000:.0f}ms"
    return f"{rt:.2f}s"


# Refresh button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Refresh All Portal Status", type="primary", use_container_width=True):
        st.rerun()

# Last checked timestamp
st.markdown(f"**Last checked:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
st.markdown("---")

# Check all portals asynchronously
async def check_all_portals():
    """Check health of all portals concurrently."""
    results = {}
    for category, portals in PORTALS.items():
        results[category] = []
        tasks = [check_portal_health(portal) for portal in portals]
        health_results = await asyncio.gather(*tasks)
        for portal, health in zip(portals, health_results):
            results[category].append({**portal, **health})
    return results


# Run health checks
with st.spinner("Checking portal health..."):
    try:
        # Run async checks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        health_data = loop.run_until_complete(check_all_portals())
        loop.close()
    except Exception as e:
        st.error(f"❌ Error checking portals: {e}")
        health_data = {}

# Display results by category
for category, portals in health_data.items():
    st.subheader(f"**{category}**")

    # Create columns for portal cards
    num_cols = min(len(portals), 3)
    cols = st.columns(num_cols)

    for idx, portal in enumerate(portals):
        with cols[idx % num_cols]:
            status_emoji = get_status_color(portal.get("status", "unknown"))
            status_text = portal.get("status", "unknown").upper()

            # Portal card
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                        border: 2px solid rgba(255, 255, 255, 0.2);
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 15px;
                    ">
                        <h3>{portal['icon']} {portal['name']}</h3>
                        <p style="opacity: 0.8; font-size: 0.9em;">{portal['description']}</p>
                        <p><strong>Status:</strong> {status_emoji} {status_text}</p>
                        {f"<p><strong>Response Time:</strong> {format_response_time(portal.get('response_time'))}</p>" if portal.get('response_time') is not None else ""}
                        {f"<p><strong>HTTP Status:</strong> {portal.get('status_code')}</p>" if portal.get('status_code') else ""}
                        {f"<p style='color: #ff6b6b;'><strong>Error:</strong> {portal.get('error')}</p>" if portal.get('error') else ""}
                        <a href="{portal['url']}" target="_blank" style="
                            display: inline-block;
                            background: rgba(102, 126, 234, 0.3);
                            padding: 5px 15px;
                            border-radius: 5px;
                            text-decoration: none;
                            color: white;
                            margin-top: 10px;
                        ">Open Portal →</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")

# Summary statistics
st.subheader("📊 Portal Health Summary")

total_portals = sum(len(portals) for portals in health_data.values())
healthy = sum(
    1
    for portals in health_data.values()
    for p in portals
    if p.get("status") == "healthy"
)
degraded = sum(
    1
    for portals in health_data.values()
    for p in portals
    if p.get("status") == "degraded"
)
down = sum(
    1
    for portals in health_data.values()
    for p in portals
    if p.get("status") in ["down", "timeout"]
)
unknown = sum(
    1
    for portals in health_data.values()
    for p in portals
    if p.get("status") == "unknown"
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Portals", total_portals)
with col2:
    st.metric("🟢 Healthy", healthy)
with col3:
    st.metric("🟡 Degraded", degraded)
with col4:
    st.metric("🔴 Down", down)
with col5:
    st.metric("⚪ Unknown", unknown)

# Overall health percentage
if total_portals - unknown > 0:
    health_pct = (healthy / (total_portals - unknown)) * 100
    st.progress(health_pct / 100)
    st.markdown(f"**Overall Health:** {health_pct:.1f}%")

# Discovery protocol info
st.markdown("---")
st.subheader("🔍 Discovery Protocol")
st.markdown(
    """
Access the machine-readable discovery manifest:

```bash
# Full portal directory
curl https://helix-unified-production.up.railway.app/.well-known/helix.json

# System status
curl https://helix-unified-production.up.railway.app/status

# Interactive portal navigator
open https://helix-unified-production.up.railway.app/portals
```
"""
)

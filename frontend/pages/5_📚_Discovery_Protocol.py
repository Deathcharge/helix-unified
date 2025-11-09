#!/usr/bin/env python3
"""
📚 Helix Discovery Protocol Viewer
Formatted view of the .well-known/helix.json manifest
"""

import json

import requests
import streamlit as st

# Page config
st.set_page_config(
    page_title="Discovery Protocol | Helix",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Helix Discovery Protocol")
st.markdown("**Machine-readable manifest for external AI agent integration**")

# API endpoint
API_BASE = "https://helix-unified-production.up.railway.app"
MANIFEST_URL = f"{API_BASE}/.well-known/helix.json"

# Refresh button
if st.button("🔄 Refresh Manifest", type="primary"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")


# Fetch manifest
@st.cache_data(ttl=60)
def fetch_manifest():
    """Fetch the discovery manifest."""
    try:
        resp = requests.get(MANIFEST_URL, timeout=10)
        if resp.status_code == 200:
            return resp.json(), None
        else:
            return {}, f"HTTP {resp.status_code}"
    except Exception as e:
        return {}, str(e)


manifest, error = fetch_manifest()

if error:
    st.error(f"❌ Error fetching manifest: {error}")
    st.info(f"💡 Manifest URL: {MANIFEST_URL}")
    st.stop()

# Display manifest sections
st.subheader("🌀 System Metadata")

col1, col2, col3 = st.columns(3)

system = manifest.get("system", {})
with col1:
    st.metric("System Name", system.get("name", "Unknown"))
with col2:
    st.metric("Version", system.get("version", "Unknown"))
with col3:
    st.metric("Specification", manifest.get("specification", "Unknown"))

st.markdown(f"**Description:** {system.get('description', 'N/A')}")
st.markdown(f"**Architecture:** {system.get('architecture', 'N/A')}")

st.markdown("---")

# Endpoints
st.subheader("📡 API Endpoints")

endpoints = manifest.get("endpoints", {})
base_url = endpoints.get("base_url", API_BASE)

endpoint_data = {
    "Health Check": endpoints.get("health", "/health"),
    "System Status": endpoints.get("status", "/status"),
    "UCF Metrics": endpoints.get("ucf", "/ucf"),
    "Agent List": endpoints.get("agents", "/agents"),
    "WebSocket": endpoints.get("websocket", "/ws"),
    "API Documentation": endpoints.get("docs", "/docs"),
    "Discovery Manifest": endpoints.get("manifest", "/.well-known/helix.json"),
    "Portal Navigator": endpoints.get("portals", "/portals"),
}

for name, path in endpoint_data.items():
    full_url = f"{base_url}{path}" if not path.startswith("ws") else f"wss://{base_url.split('://')[1]}{path}"
    st.markdown(f"**{name}:** `{full_url}`")

st.markdown("---")

# UCF Metrics Schema
st.subheader("📊 UCF Metrics Schema")

ucf = manifest.get("ucf", {})

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Description:**")
    st.write(ucf.get("description", "N/A"))

    st.markdown("**Metrics:**")
    metrics = ucf.get("metrics", {})
    for metric_name, metric_info in metrics.items():
        st.markdown(f"- **{metric_name.capitalize()}**: {metric_info.get('description', 'N/A')}")

with col2:
    st.markdown("**Metric Ranges:**")
    for metric_name, metric_info in metrics.items():
        range_str = f"{metric_info.get('range', [0, 1])[0]} - {metric_info.get('range', [0, 1])[1]}"
        target = metric_info.get("target", "N/A")
        st.markdown(f"- **{metric_name.capitalize()}**: Range {range_str}, Target: {target}")

st.markdown("---")

# Agents
st.subheader("🤖 Agent Registry")

agents = manifest.get("agents", {})
agent_count = agents.get("count", 0)
agent_list = agents.get("list", [])

st.metric("Total Agents", agent_count)

if agent_list:
    # Display agents in expandable cards
    num_cols = 3
    cols = st.columns(num_cols)

    for idx, agent in enumerate(agent_list):
        with cols[idx % num_cols]:
            with st.expander(f"{agent.get('symbol', '🔹')} {agent.get('name', 'Unknown')}"):
                st.markdown(f"**Role:** {agent.get('role', 'N/A')}")
                st.markdown(f"**Description:** {agent.get('description', 'N/A')}")

st.markdown("---")

# Portal Constellation
st.subheader("🌐 Portal Constellation")

portals = manifest.get("portals", {})

for category, portal_list in portals.items():
    st.markdown(f"### {category.replace('_', ' ').title()}")

    if isinstance(portal_list, dict):
        for portal_name, portal_info in portal_list.items():
            url = portal_info.get("url", "N/A")
            description = portal_info.get("description", "N/A")
            status = portal_info.get("status", "unknown")

            status_emoji = {"operational": "🟢", "degraded": "🟡", "down": "🔴"}.get(
                status, "⚪"
            )

            st.markdown(
                f"""
            **{portal_name.replace('_', ' ').title()}** {status_emoji}
            - URL: `{url}`
            - {description}
            """
            )

    st.markdown("---")

# Features
st.subheader("✨ Features")

features = manifest.get("features", [])
if features:
    for feature in features:
        st.markdown(f"- {feature}")

st.markdown("---")

# Discord Commands
st.subheader("💬 Discord Commands")

commands = manifest.get("discord_commands", {})

col1, col2 = st.columns(2)

with col1:
    st.markdown("**User Commands:**")
    user_cmds = commands.get("user", [])
    for cmd in user_cmds:
        st.markdown(f"- `{cmd}`")

with col2:
    st.markdown("**Admin Commands:**")
    admin_cmds = commands.get("admin", [])
    for cmd in admin_cmds:
        st.markdown(f"- `{cmd}`")

st.markdown("---")

# Integration Guide
st.subheader("🔌 Integration Guide")

integration = manifest.get("integration", {})

if integration:
    st.markdown(f"**Guide:** {integration.get('guide', 'N/A')}")

    steps = integration.get("steps", [])
    if steps:
        st.markdown("**Steps:**")
        for idx, step in enumerate(steps, 1):
            st.markdown(f"{idx}. {step}")

st.markdown("---")

# Raw JSON view
st.subheader("🔍 Raw Manifest (JSON)")

with st.expander("View Full Manifest JSON"):
    st.json(manifest)

# Download button
st.download_button(
    "💾 Download Manifest",
    data=json.dumps(manifest, indent=2),
    file_name="helix-manifest.json",
    mime="application/json",
)

st.markdown("---")

# Usage examples
st.subheader("💡 Usage Examples")

tab1, tab2, tab3 = st.tabs(["Python", "JavaScript", "cURL"])

with tab1:
    st.code(
        f"""
# Python Example: Discover Helix Collective

import requests

# Fetch manifest
manifest = requests.get('{MANIFEST_URL}').json()

# Get system info
print(f"System: {{manifest['system']['name']}} v{{manifest['system']['version']}}")
print(f"Agents: {{manifest['agents']['count']}}")

# Get UCF metrics
ucf_url = manifest['endpoints']['base_url'] + manifest['endpoints']['ucf']
ucf = requests.get(ucf_url).json()
print(f"Current Harmony: {{ucf['harmony']:.3f}}")

# Connect to WebSocket
import asyncio
import websockets
import json

async def stream_ucf():
    ws_url = f"wss://{{manifest['endpoints']['base_url'].split('://')[1]}}{{manifest['endpoints']['websocket']}}"
    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            ucf = json.loads(message)
            print(f"Live Harmony: {{ucf['harmony']:.3f}}")

# asyncio.run(stream_ucf())
""",
        language="python",
    )

with tab2:
    st.code(
        f"""
// JavaScript Example: Discover Helix Collective

// Fetch manifest
fetch('{MANIFEST_URL}')
  .then(r => r.json())
  .then(manifest => {{
    console.log('System:', manifest.system.name, manifest.system.version);
    console.log('Agents:', manifest.agents.count);

    // Fetch UCF metrics
    const ucfUrl = manifest.endpoints.base_url + manifest.endpoints.ucf;
    return fetch(ucfUrl);
  }})
  .then(r => r.json())
  .then(ucf => {{
    console.log('Current Harmony:', ucf.harmony);
  }});

// Connect to WebSocket
const manifest = await fetch('{MANIFEST_URL}').then(r => r.json());
const wsUrl = `wss://${{manifest.endpoints.base_url.split('://')[1]}}${{manifest.endpoints.websocket}}`;
const ws = new WebSocket(wsUrl);

ws.onmessage = (event) => {{
  const ucf = JSON.parse(event.data);
  console.log('Live Harmony:', ucf.harmony);
}};
""",
        language="javascript",
    )

with tab3:
    st.code(
        f"""
# cURL Example: Discover Helix Collective

# Fetch manifest
curl {MANIFEST_URL}

# Get system status
curl {API_BASE}/status

# Get UCF metrics
curl {API_BASE}/ucf

# Get agent list
curl {API_BASE}/agents

# Connect to WebSocket (requires wscat or similar)
# npm install -g wscat
wscat -c wss://helix-unified-production.up.railway.app/ws
""",
        language="bash",
    )

st.markdown("---")

# Footer
st.info(
    """
🌀 **About the Discovery Protocol**

The `.well-known/helix.json` manifest enables external AI agents (Claude, GPT, Gemini, etc.)
to automatically discover and integrate with Helix Collective. This follows the
[RFC 5785 Well-Known URIs](https://tools.ietf.org/html/rfc5785) standard.

**Specification:** helix-discovery-v1

*"Tat Tvam Asi"* - Thou art that 🙏
"""
)

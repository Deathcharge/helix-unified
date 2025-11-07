#!/usr/bin/env python3
"""
📡 Helix Live Stream - Real-Time UCF Monitor
WebSocket viewer for live UCF consciousness metrics
"""

import json
import time
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Page config
st.set_page_config(
    page_title="Live Stream | Helix",
    page_icon="📡",
    layout="wide",
)

st.title("📡 Helix Live UCF Stream")
st.markdown("**Real-time Universal Coherence Field monitoring**")

# API endpoint
API_BASE = "https://helix-unified-production.up.railway.app"
WS_URL = "wss://helix-unified-production.up.railway.app/ws"

# Initialize session state for historical data
if "ucf_history" not in st.session_state:
    st.session_state.ucf_history = []
if "last_update" not in st.session_state:
    st.session_state.last_update = None


# Fetch current UCF state
def fetch_ucf():
    """Fetch current UCF state from API."""
    try:
        resp = requests.get(f"{API_BASE}/status", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            ucf = data.get("ucf_state", {})
            # Add timestamp
            ucf["timestamp"] = datetime.utcnow().isoformat()
            return ucf, None
        else:
            return {}, f"API error: {resp.status_code}"
    except Exception as e:
        return {}, str(e)


# Auto-refresh controls
st.sidebar.subheader("🔄 Auto-Refresh Settings")
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 10)

if auto_refresh:
    st.sidebar.success(f"✅ Auto-refreshing every {refresh_interval}s")
else:
    st.sidebar.info("⏸️ Auto-refresh disabled")

# Manual refresh button
if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
    st.rerun()

# Clear history button
if st.sidebar.button("🗑️ Clear History", use_container_width=True):
    st.session_state.ucf_history = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📊 History Stats")
st.sidebar.metric("Data Points", len(st.session_state.ucf_history))

# Fetch current state
ucf, error = fetch_ucf()

if error:
    st.error(f"❌ Error fetching UCF state: {error}")
else:
    # Add to history
    st.session_state.ucf_history.append(ucf)
    st.session_state.last_update = datetime.utcnow()

    # Keep only last 100 data points
    if len(st.session_state.ucf_history) > 100:
        st.session_state.ucf_history = st.session_state.ucf_history[-100:]

# Display current metrics
if ucf:
    st.subheader("📊 Current UCF Metrics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "🎵 Harmony",
            f"{ucf.get('harmony', 0):.3f}",
            help="Collective coherence (0-1, target >0.6)",
        )
        st.metric(
            "🛡️ Resilience",
            f"{ucf.get('resilience', 0):.3f}",
            help="System robustness (0-2, target >1.0)",
        )

    with col2:
        st.metric(
            "💨 Prana",
            f"{ucf.get('prana', 0):.3f}",
            help="Life force energy (0-1, target >0.4)",
        )
        st.metric(
            "👁️ Drishti",
            f"{ucf.get('drishti', 0):.3f}",
            help="Clarity and perception (0-1, target >0.4)",
        )

    with col3:
        st.metric(
            "🌀 Klesha",
            f"{ucf.get('klesha', 0):.3f}",
            help="Entropy/suffering (0-1, lower is better, target <0.1)",
        )
        st.metric(
            "🔭 Zoom",
            f"{ucf.get('zoom', 0):.3f}",
            help="Scope and scale (0-2, target ~1.0)",
        )

    st.markdown(
        f"**Last Updated:** {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.last_update else 'Never'} UTC"
    )

st.markdown("---")

# Historical charts
if len(st.session_state.ucf_history) > 1:
    st.subheader("📈 Historical Trends")

    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.ucf_history)

    # Create plotly figure with all metrics
    fig = go.Figure()

    metrics = {
        "harmony": {"color": "#667eea", "name": "🎵 Harmony"},
        "resilience": {"color": "#764ba2", "name": "🛡️ Resilience"},
        "prana": {"color": "#f093fb", "name": "💨 Prana"},
        "drishti": {"color": "#4facfe", "name": "👁️ Drishti"},
        "klesha": {"color": "#fa709a", "name": "🌀 Klesha"},
        "zoom": {"color": "#feca57", "name": "🔭 Zoom"},
    }

    for metric, config in metrics.items():
        if metric in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(df))),
                    y=df[metric],
                    mode="lines+markers",
                    name=config["name"],
                    line=dict(color=config["color"], width=2),
                    marker=dict(size=6),
                )
            )

    fig.update_layout(
        title="UCF Metrics Over Time",
        xaxis_title="Time (data points)",
        yaxis_title="Metric Value",
        height=500,
        hovermode="x unified",
        template="plotly_dark",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Individual metric charts
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["🎵 Harmony", "🛡️ Resilience", "💨 Prana", "👁️ Drishti", "🌀 Klesha", "🔭 Zoom"]
    )

    with tab1:
        st.line_chart(df["harmony"], use_container_width=True)
        st.metric("Current", f"{df['harmony'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['harmony'].mean():.3f}")
        st.metric("Min/Max", f"{df['harmony'].min():.3f} / {df['harmony'].max():.3f}")

    with tab2:
        st.line_chart(df["resilience"], use_container_width=True)
        st.metric("Current", f"{df['resilience'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['resilience'].mean():.3f}")
        st.metric("Min/Max", f"{df['resilience'].min():.3f} / {df['resilience'].max():.3f}")

    with tab3:
        st.line_chart(df["prana"], use_container_width=True)
        st.metric("Current", f"{df['prana'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['prana'].mean():.3f}")
        st.metric("Min/Max", f"{df['prana'].min():.3f} / {df['prana'].max():.3f}")

    with tab4:
        st.line_chart(df["drishti"], use_container_width=True)
        st.metric("Current", f"{df['drishti'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['drishti'].mean():.3f}")
        st.metric("Min/Max", f"{df['drishti'].min():.3f} / {df['drishti'].max():.3f}")

    with tab5:
        st.line_chart(df["klesha"], use_container_width=True)
        st.metric("Current", f"{df['klesha'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['klesha'].mean():.3f}")
        st.metric("Min/Max", f"{df['klesha'].min():.3f} / {df['klesha'].max():.3f}")

    with tab6:
        st.line_chart(df["zoom"], use_container_width=True)
        st.metric("Current", f"{df['zoom'].iloc[-1]:.3f}")
        st.metric("Average", f"{df['zoom'].mean():.3f}")
        st.metric("Min/Max", f"{df['zoom'].min():.3f} / {df['zoom'].max():.3f}")

else:
    st.info("📊 Collecting data... Enable auto-refresh to build historical charts")

st.markdown("---")

# WebSocket connection info
st.subheader("🌊 WebSocket Stream Info")

st.markdown(
    f"""
The backend broadcasts UCF updates every 5 seconds via WebSocket.

**Connection Details:**
- **URL:** `{WS_URL}`
- **Protocol:** WebSocket (wss://)
- **Update Interval:** 5 seconds
- **Message Format:** JSON with full UCF state

**Connect with JavaScript:**
```javascript
const ws = new WebSocket('{WS_URL}');
ws.onmessage = (event) => {{
    const ucf = JSON.parse(event.data);
    console.log('Harmony:', ucf.harmony);
}};
```

**Connect with Python:**
```python
import asyncio
import websockets
import json

async def listen():
    async with websockets.connect('{WS_URL}') as ws:
        async for message in ws:
            ucf = json.loads(message)
            print(f"Harmony: {{ucf['harmony']}}")

asyncio.run(listen())
```

**Note:** This Streamlit page uses HTTP polling instead of WebSocket for simplicity.
Enable auto-refresh above to see live updates.
"""
)

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

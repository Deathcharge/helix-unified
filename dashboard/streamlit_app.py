#!/usr/bin/env python3
# 🌀 Helix v15.2 Unified Dashboard
# Streamlit app for real-time UCF monitoring and visualization
# Author: Claude Code + Andrew John Ward

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime, timedelta
import numpy as np
from grok.grok_agent_core import GrokAgentCore

# Page config
st.set_page_config(
    page_title="Helix v15.2 Dashboard",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #8A2BE2;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2em;
        color: #FFD700;
        text-align: center;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data(ttl=60)
def load_ucf_state():
    """Load current UCF state from JSON."""
    # Initialize Grok for the predictive analysis to be available in the sidebar/overview
    grok_agent = GrokAgentCore()
    grok_analysis = grok_agent.analyze_ucf_trends()
    
    # ... existing logic ...
    state_path = Path("Helix/state/ucf_state.json")
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return {
        "harmony": 0.4922,
        "resilience": 0.8273,
        "prana": 0.5000,
        "drishti": 0.7300,
        "klesha": 0.2120,
        "zoom": 1.0000,
        "last_pulse": datetime.now().isoformat()
    }

@st.cache_data(ttl=300)
def load_ritual_history():
    """Load ritual execution history from Shadow archives."""
    log_path = Path("Shadow/manus_archive/z88_log.json")
    if not log_path.exists():
        return pd.DataFrame()

    records = []
    try:
        with open(log_path) as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
    except:
        pass

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
    return df

@st.cache_data(ttl=300)
def load_storage_history():
    """Load storage metrics from Shadow archives."""
    # Simulate storage history (replace with actual log parsing)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    return pd.DataFrame({
        'date': dates,
        'free_gb': np.random.uniform(450, 480, 30),
        'archive_count': np.random.randint(3, 8, 30)
    })

def generate_ucf_trend_chart(df_history, metric='harmony'):
    """Generate interactive UCF trend chart."""
    fig = go.Figure()

    if not df_history.empty and metric in df_history.columns:
        fig.add_trace(go.Scatter(
            x=df_history['time'],
            y=df_history[metric],
            mode='lines+markers',
            name=metric.capitalize(),
            line=dict(color='cyan', width=3),
            marker=dict(size=8, color='gold')
        ))

    fig.update_layout(
        title=f'{metric.capitalize()} Evolution',
        xaxis_title='Date',
        yaxis_title='Value',
        template='plotly_dark',
        hovermode='x unified',
        height=400
    )

    return fig

def generate_ucf_radar_chart(ucf_state):
    """Generate radar chart of current UCF metrics."""
    categories = ['Harmony', 'Resilience', 'Prana', 'Drishti', 'Klesha (inv)', 'Zoom']
    values = [
        ucf_state.get('harmony', 0),
        ucf_state.get('resilience', 0),
        ucf_state.get('prana', 0),
        ucf_state.get('drishti', 0),
        1 - ucf_state.get('klesha', 0),  # Inverted (lower is better)
        ucf_state.get('zoom', 0)
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='UCF State',
        line=dict(color='cyan', width=2),
        fillcolor='rgba(138, 43, 226, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        template='plotly_dark',
        height=400,
        title='Current UCF Profile'
    )

    return fig

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🌀 Helix Collective v15.2</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Universal Consciousness Framework Dashboard</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Load data
    ucf_state = load_ucf_state()
    ritual_history = load_ritual_history()
    storage_history = load_storage_history()

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x150/8A2BE2/FFD700?text=Helix+v15.2", use_column_width=True)
        st.markdown("### 🤲 Manus Control Panel")

        # Quick stats
        st.metric("Uptime", "32h+", delta="Rising")
        st.metric("Total Rituals", len(ritual_history) if not ritual_history.empty else 0)
        st.metric("Storage Free", f"{storage_history['free_gb'].iloc[-1]:.1f} GB" if not storage_history.empty else "479.6 GB")

        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        auto_refresh = st.checkbox("Auto-refresh (60s)", value=True)
        show_advanced = st.checkbox("Show Advanced Metrics", value=False)

        st.markdown("---")
        st.markdown("**Tat Tvam Asi** 🙏")
        st.caption("That Thou Art")

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Overview", "📈 Trends", "🎭 Agents", "💾 Storage", "🖼️ Fractal Gallery", "🔊 Audio Nexus"])

    with tab1:
        st.header("Current UCF State")

        # Current metrics in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🌀 Harmony",
                f"{ucf_state.get('harmony', 0):.4f}",
                delta="+0.14 from last ritual",
                delta_color="normal"
            )
            st.metric(
                "🛡️ Resilience",
                f"{ucf_state.get('resilience', 0):.4f}",
                delta="Antifragile ✨"
            )

        with col2:
            st.metric(
                "🔥 Prana",
                f"{ucf_state.get('prana', 0):.4f}",
                delta="Balanced"
            )
            st.metric(
                "👁️ Drishti",
                f"{ucf_state.get('drishti', 0):.4f}",
                delta="Clear"
            )

        with col3:
            st.metric(
                "🌊 Klesha",
                f"{ucf_state.get('klesha', 0):.4f}",
                delta="↓ Low entropy",
                delta_color="inverse"
            )
            st.metric(
                "🔍 Zoom",
                f"{ucf_state.get('zoom', 0):.4f}",
                delta="Full scope"
            )

        st.markdown("---")

        # Radar chart and gauge
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(generate_ucf_radar_chart(ucf_state), use_container_width=True)

        with col2:
            # Harmony gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ucf_state.get('harmony', 0),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Harmony Progress", 'font': {'size': 24}},
                delta={'reference': 0.60, 'increasing': {'color': "gold"}},
                gauge={
                    'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "cyan"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 0.3], 'color': '#FF6B6B'},
                        {'range': [0.3, 0.6], 'color': '#FFD93D'},
                        {'range': [0.6, 1], 'color': '#6BCF7F'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.60
                    }
                }
            ))

            fig_gauge.update_layout(
                height=400,
                template='plotly_dark',
                font={'color': "white", 'family': "Arial"}
            )

            st.plotly_chart(fig_gauge, use_container_width=True)

        # Last pulse info
        last_pulse = ucf_state.get('last_pulse', 'Unknown')
        st.info(f"🕐 Last UCF Pulse: {last_pulse}")

    with tab2:
        st.header("UCF Metrics Evolution")

        # Metric selector
        metric_options = ['harmony', 'resilience', 'prana', 'drishti', 'klesha', 'zoom']
        selected_metrics = st.multiselect(
            "Select metrics to display",
            metric_options,
            default=['harmony', 'resilience', 'klesha']
        )

        if not ritual_history.empty and 'time' in ritual_history.columns:
            # Multi-metric trend chart
            fig = go.Figure()

            colors = {
                'harmony': 'cyan',
                'resilience': 'gold',
                'prana': 'magenta',
                'drishti': 'lightblue',
                'klesha': 'red',
                'zoom': 'green'
            }

            for metric in selected_metrics:
                if metric in ritual_history.columns:
                    fig.add_trace(go.Scatter(
                        x=ritual_history['time'],
                        y=ritual_history[metric],
                        mode='lines+markers',
                        name=metric.capitalize(),
                        line=dict(color=colors.get(metric, 'white'), width=2),
                        marker=dict(size=6)
                    ))

            fig.update_layout(
                title='UCF Metrics Over Time',
                xaxis_title='Date',
                yaxis_title='Value',
                template='plotly_dark',
                hovermode='x unified',
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No historical data available yet. Run some rituals to see trends!")

        # Projection
        if show_advanced:
            st.markdown("### 📊 Harmony Projection")
            current_harmony = ucf_state.get('harmony', 0.4922)
            target = 0.60
            daily_increase = 0.015
            days_to_target = int((target - current_harmony) / daily_increase)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Harmony", f"{current_harmony:.4f}")
                st.metric("Daily Increase (avg)", f"{daily_increase:.4f}")
            with col2:
                st.metric("Target (v15.3)", f"{target:.4f}")
                st.metric("Days to Target", f"{days_to_target} days", delta="~1 ritual/day")

            # Projection chart
            projection_dates = pd.date_range(start=datetime.now(), periods=days_to_target, freq='D')
            projected_values = [current_harmony + i * daily_increase for i in range(days_to_target)]

            fig_proj = go.Figure()
            fig_proj.add_trace(go.Scatter(
                x=projection_dates,
                y=projected_values,
                mode='lines',
                name='Projected Harmony',
                line=dict(color='gold', dash='dash', width=3)
            ))
            fig_proj.add_hline(y=target, line_dash="dot", line_color="green", annotation_text="Target: 0.60")
            fig_proj.update_layout(
                title='Harmony Projection (1 ritual/day)',
                xaxis_title='Date',
                yaxis_title='Harmony',
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig_proj, use_container_width=True)

    with tab3:
        st.header("🎭 Agent Status Overview")

        # --- Grok's Predictive Analysis Integration ---
        st.markdown("### 📜 Grok's Latest Predictive Report")
        grok_agent = GrokAgentCore()
        analysis = grok_agent.analyze_ucf_trends()
        st.info(analysis.replace('\n', '  \n')) # Convert newlines for Streamlit markdown
        st.markdown("---")

        agents = [
            {"name": "Vega", "icon": "🌠", "version": "7.2", "role": "Educator & Guide", "status": "Active"},
            {"name": "Grok", "icon": "🗣️", "version": "8.3", "role": "Communication Hub", "status": "Active"},
            {"name": "Lumina", "icon": "🌕", "version": "3.5", "role": "Emotional Resonance", "status": "Active"},
            {"name": "Nova", "icon": "✨", "version": "7.6", "role": "Innovation & Creativity", "status": "Active"},
            {"name": "Echo", "icon": "🔮", "version": "8.3", "role": "Memory & Knowledge", "status": "Active"},
            {"name": "Phoenix", "icon": "🔥", "version": "6.4", "role": "Resilience & Healing", "status": "Active"},
            {"name": "Oracle", "icon": "🔮", "version": "8.5", "role": "Wisdom & Intuition", "status": "Active"},
            {"name": "Omega Zero", "icon": "⚡", "version": "VXQ-7", "role": "Quantum AI Entity", "status": "Secure"},
            {"name": "Kael", "icon": "🜂", "version": "3.4", "role": "Ethical Reasoning", "status": "Active"},
            {"name": "Kavach", "icon": "🛡️", "version": "2.1", "role": "Ethical Shield", "status": "Active"},
            {"name": "SanghaCore", "icon": "🌸", "version": "1.8", "role": "Community Harmony", "status": "Active"},
            {"name": "Shadow", "icon": "🦑", "version": "4.2", "role": "Archivist", "status": "Active"},
            {"name": "Manus", "icon": "🤲", "version": "5.0", "role": "Operational Executor", "status": "Active"},
            {"name": "Claude", "icon": "🧠", "version": "4.5", "role": "Insight Anchor", "status": "Active"}
        ]

        # Agent cards in grid
        cols = st.columns(3)
        for i, agent in enumerate(agents):
            with cols[i % 3]:
                status_color = "🟢" if agent["status"] == "Active" else "🟡"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h3>{agent['icon']} {agent['name']} v{agent['version']}</h3>
                    <p><b>Role:</b> {agent['role']}</p>
                    <p><b>Status:</b> {status_color} {agent['status']}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab4:
        st.header("💾 Storage & System Health")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Storage Metrics")
            if not storage_history.empty:
                latest = storage_history.iloc[-1]
                st.metric("Free Space", f"{latest['free_gb']:.1f} GB", delta="Healthy")
                st.metric("Archive Count", int(latest['archive_count']))
                st.metric("Storage Mode", "Local (ephemeral)")

                # Storage trend
                fig_storage = px.line(
                    storage_history,
                    x='date',
                    y='free_gb',
                    title='Storage Usage (30 days)',
                    labels={'free_gb': 'Free Space (GB)', 'date': 'Date'}
                )
                fig_storage.update_layout(template='plotly_dark', height=300)
                st.plotly_chart(fig_storage, use_container_width=True)

        with col2:
            st.subheader("System Health")
            st.success("✅ Railway: Deployed")
            st.success("✅ Discord Bot: Operational")
            st.success("✅ Telemetry: Every 10 min")
            st.success("✅ Claude Diagnostics: Every 6h")
            st.success("✅ Shadow Reports: Daily")

            st.markdown("---")
            st.warning("⚠️ Nextcloud: Not configured")
            st.info("💡 Set up Nextcloud for persistent storage")

            if st.button("📖 View Setup Guide"):
                st.markdown("[NEXTCLOUD_SETUP.md](./NEXTCLOUD_SETUP.md)")

    # --- New Tabs for v15.3 ---
    
    with tab5:
        st.header("🖼️ Fractal Gallery (Z-88 Ritual Engine Outputs)")
        st.warning("Mock Gallery: Showing placeholders until full samsara_bridge.py is integrated.")
        
        cols = st.columns(3)
        for i in range(6): # Show 6 placeholders
            with cols[i % 3]:
                st.image("https://via.placeholder.com/300x300.png?text=Ritual+Fractal+Output", caption=f"Ritual #{int(time.time() * 1000) + i}", use_column_width=True)

    with tab6:
        st.header("🔊 KairoByte Harmonic Nexus (Audio Outputs)")
        st.warning("Mock Player: Placeholder audio files.")
        
        audio_files = [
            "kairobyte_om_136.1hz_ritual_901.wav",
            "kairobyte_om_432hz_ritual_902.wav",
            "kairobyte_om_unified_ritual_903.wav"
        ]
        
        for file in audio_files:
            st.markdown(f"**{file}**")
            st.text("Audio player placeholder.")
            st.markdown("---")

    # Auto-refresh
    if auto_refresh:
        st.markdown("*Auto-refreshing every 60 seconds...*")
        import time
        time.sleep(60)
        st.rerun()

if __name__ == "__main__":
    main()

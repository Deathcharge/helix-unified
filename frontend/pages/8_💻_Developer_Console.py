#!/usr/bin/env python3
"""
💻 Helix Developer Console
Live logs, database explorer, webhook tester, and API playground
"""

import json
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

# Page config
st.set_page_config(
    page_title="Developer Console | Helix",
    page_icon="💻",
    layout="wide",
)

st.title("💻 Helix Developer Console")
st.markdown("**Advanced development tools for system debugging and testing**")

# API endpoint
API_BASE = "https://helix-unified-production.up.railway.app"

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📜 Live Logs", "🗄️ Database Explorer", "🔗 Webhook Tester", "🎮 API Playground", "⚙️ System Config"]
)

# ============================================================================
# TAB 1: LIVE LOGS
# ============================================================================

with tab1:
    st.subheader("📜 Live Log Viewer")

    col1, col2 = st.columns([3, 1])

    with col1:
        log_source = st.selectbox(
            "Log Source",
            [
                "Backend (FastAPI)",
                "Discord Bot",
                "Agent System",
                "UCF Engine",
                "Ritual System",
                "All Sources",
            ],
        )

    with col2:
        auto_refresh_logs = st.checkbox("Auto-Refresh", value=False, key="logs_refresh")

    log_level = st.multiselect(
        "Log Levels", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default=["INFO", "WARNING", "ERROR"]
    )

    num_lines = st.slider("Number of log lines", 10, 500, 50)

    if st.button("🔄 Refresh Logs", use_container_width=True):
        st.rerun()

    st.markdown("---")

    # Simulated log data (in production, this would fetch from backend)
    # TODO: Add real log endpoint to backend API
    sample_logs = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "source": "FastAPI",
            "message": "GET /status - 200 OK - 45ms",
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "source": "UCF Engine",
            "message": "UCF state updated - Harmony: 0.855",
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "WARNING",
            "source": "Agent System",
            "message": "Agent 'Kael' response time: 2.3s (slow)",
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "source": "Discord Bot",
            "message": "!discovery command executed by user#1234",
        },
    ]

    # Display logs
    st.markdown("**Recent Logs:**")

    for log in sample_logs:
        level = log["level"]
        color = {
            "DEBUG": "#9E9E9E",
            "INFO": "#4CAF50",
            "WARNING": "#FFC107",
            "ERROR": "#FF5722",
            "CRITICAL": "#D32F2F",
        }.get(level, "#FFFFFF")

        if level in log_level:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 255, 255, 0.05);
                    border-left: 4px solid {color};
                    padding: 10px;
                    margin-bottom: 10px;
                    border-radius: 5px;
                ">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: {color}; font-weight: bold;">[{level}]</span>
                        <span style="opacity: 0.7; font-size: 0.85em;">{log['timestamp'][:19]}</span>
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="opacity: 0.8; font-size: 0.9em;">{log['source']}</span> |
                        <span>{log['message']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info("💡 **Production Note:** Live log streaming will be available via WebSocket connection")

    # Log export
    if st.button("💾 Export Logs to CSV"):
        log_df = pd.DataFrame(sample_logs)
        csv = log_df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            data=csv,
            file_name=f"helix_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# ============================================================================
# TAB 2: DATABASE EXPLORER
# ============================================================================

with tab2:
    st.subheader("🗄️ Database Explorer")

    st.info("📊 Browse UCF state history, agent records, and operation logs")

    # Collection selector
    collection = st.selectbox(
        "Select Collection",
        [
            "UCF State History",
            "Agent Records",
            "Operation Logs",
            "Ritual Executions",
            "Discord Commands",
            "Ethical Scans",
        ],
    )

    # Query builder
    st.markdown("**Query Builder:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        query_field = st.text_input("Field", placeholder="e.g., harmony")

    with col2:
        query_operator = st.selectbox("Operator", ["=", ">", "<", ">=", "<=", "contains"])

    with col3:
        query_value = st.text_input("Value", placeholder="e.g., 0.8")

    limit = st.slider("Limit results", 10, 500, 50)

    if st.button("🔍 Execute Query", use_container_width=True):
        # Simulated query results
        if collection == "UCF State History":
            try:
                # Fetch current UCF state
                resp = requests.get(f"{API_BASE}/status", timeout=10)
                if resp.status_code == 200:
                    status = resp.json()
                    ucf = status.get("ucf_state", {})

                    # Create sample history (in production, fetch from database)
                    history = []
                    for i in range(min(limit, 10)):
                        history.append(
                            {
                                "timestamp": datetime.utcnow().isoformat(),
                                "harmony": ucf.get("harmony", 0),
                                "resilience": ucf.get("resilience", 0),
                                "prana": ucf.get("prana", 0),
                                "drishti": ucf.get("drishti", 0),
                                "klesha": ucf.get("klesha", 0),
                                "zoom": ucf.get("zoom", 0),
                            }
                        )

                    df = pd.DataFrame(history)
                    st.dataframe(df, use_container_width=True)

                    # Export option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "💾 Export to CSV",
                        data=csv,
                        file_name=f"ucf_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                else:
                    st.error("Failed to fetch UCF data")
            except Exception as e:
                st.error(f"Error: {e}")

        elif collection == "Agent Records":
            try:
                resp = requests.get(f"{API_BASE}/agents", timeout=10)
                if resp.status_code == 200:
                    agents_data = resp.json()
                    agents = agents_data.get("agents", [])

                    if agents:
                        df = pd.DataFrame(agents)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No agent records found")
                else:
                    st.error("Failed to fetch agent data")
            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.info(f"📋 Query results for '{collection}' would appear here")

    st.markdown("---")

    # JSON viewer
    st.markdown("**Raw JSON Viewer:**")

    if st.button("📄 View Raw UCF State"):
        try:
            resp = requests.get(f"{API_BASE}/status", timeout=10)
            if resp.status_code == 200:
                status = resp.json()
                st.json(status.get("ucf_state", {}))
            else:
                st.error("Failed to fetch data")
        except Exception as e:
            st.error(f"Error: {e}")

# ============================================================================
# TAB 3: WEBHOOK TESTER
# ============================================================================

with tab3:
    st.subheader("🔗 Webhook Tester")

    st.markdown("Test webhooks for Zapier, Discord, Slack, and custom endpoints")

    # Webhook configuration
    webhook_type = st.selectbox(
        "Webhook Type",
        ["Zapier UCF Update", "Discord Notification", "Slack Alert", "Custom Webhook"],
    )

    webhook_url = st.text_input(
        "Webhook URL",
        placeholder="https://hooks.zapier.com/hooks/catch/...",
    )

    # Payload builder
    st.markdown("**Payload Builder:**")

    payload_template = st.selectbox(
        "Template",
        [
            "UCF State Update",
            "Agent Status Change",
            "Portal Health Alert",
            "Custom JSON",
        ],
    )

    if payload_template == "UCF State Update":
        try:
            resp = requests.get(f"{API_BASE}/status", timeout=10)
            if resp.status_code == 200:
                status = resp.json()
                ucf = status.get("ucf_state", {})

                payload = {
                    "event": "ucf_update",
                    "timestamp": datetime.utcnow().isoformat(),
                    "ucf_state": ucf,
                }

                st.json(payload)
            else:
                st.error("Failed to fetch UCF state")
        except Exception as e:
            st.error(f"Error: {e}")
            payload = {}
    else:
        payload = st.text_area(
            "Custom JSON Payload",
            value='{\n  "event": "test",\n  "data": "sample"\n}',
            height=200,
        )

    # Send webhook
    if st.button("🚀 Send Webhook", use_container_width=True):
        if not webhook_url:
            st.warning("Please enter a webhook URL")
        else:
            try:
                import json

                if isinstance(payload, str):
                    payload_data = json.loads(payload)
                else:
                    payload_data = payload

                resp = requests.post(webhook_url, json=payload_data, timeout=10)

                if resp.status_code < 300:
                    st.success(f"✅ Webhook sent successfully! Status: {resp.status_code}")
                    st.code(resp.text)
                else:
                    st.error(f"❌ Webhook failed. Status: {resp.status_code}")
                    st.code(resp.text)
            except Exception as e:
                st.error(f"Error sending webhook: {e}")

    st.markdown("---")

    # Webhook history
    st.markdown("**Recent Webhook Calls:**")
    st.info("Webhook history will be stored here after sending requests")

# ============================================================================
# TAB 4: API PLAYGROUND
# ============================================================================

with tab4:
    st.subheader("🎮 API Playground")

    st.markdown("Interactive API testing with request/response inspection")

    # Endpoint selector
    endpoint = st.selectbox(
        "Select Endpoint",
        [
            "GET /health",
            "GET /status",
            "GET /ucf",
            "GET /agents",
            "POST /ritual",
            "POST /directive",
            "GET /.well-known/helix.json",
        ],
    )

    # Parse method and path
    method, path = endpoint.split(" ")

    # Request configuration
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Request Configuration:**")
        st.code(f"{method} {API_BASE}{path}")

        # Query parameters (for POST requests)
        if method == "POST":
            st.markdown("**Parameters:**")
            if "ritual" in path:
                steps = st.number_input("Ritual Steps", 1, 108, 108)
                params = {"steps": steps}
            elif "directive" in path:
                action = st.text_input("Action", value="sync_ucf")
                params = {"action": action, "parameters": {}}
            else:
                params = {}
        else:
            params = {}

    with col2:
        st.markdown("**Headers:**")
        st.code("Content-Type: application/json\nAccept: application/json")

    # Execute request
    if st.button("▶️ Execute Request", type="primary", use_container_width=True):
        try:
            import time

            start = time.time()

            if method == "GET":
                resp = requests.get(f"{API_BASE}{path}", timeout=15)
            elif method == "POST":
                resp = requests.post(f"{API_BASE}{path}", params=params, timeout=15)

            elapsed = time.time() - start

            # Display response
            st.success(f"✅ Request completed in {elapsed*1000:.0f}ms")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status Code", resp.status_code)
            with col2:
                st.metric("Response Time", f"{elapsed*1000:.0f}ms")
            with col3:
                st.metric("Response Size", f"{len(resp.content)} bytes")

            # Response body
            st.markdown("**Response Body:**")
            try:
                data = resp.json()
                st.json(data)

                # Download option
                st.download_button(
                    "💾 Download Response",
                    data=json.dumps(data, indent=2),
                    file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                )
            except:
                st.text_area("Raw Response", resp.text, height=300)

            # Response headers
            with st.expander("📋 Response Headers"):
                st.json(dict(resp.headers))

        except requests.exceptions.Timeout:
            st.error("❌ Request timeout (>15s)")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ============================================================================
# TAB 5: SYSTEM CONFIG
# ============================================================================

with tab5:
    st.subheader("⚙️ System Configuration")

    st.markdown("**Environment Variables:**")

    config = {
        "API_BASE": API_BASE,
        "DEPLOYMENT": "Railway (Production)",
        "FRONTEND": "Streamlit Community Cloud",
        "DATABASE": "Helix/state/ucf_state.json",
        "DISCORD_BOT": "Active",
        "AGENT_SYSTEM": "14 Agents",
    }

    for key, value in config.items():
        st.code(f"{key}={value}")

    st.markdown("---")

    st.markdown("**System Information:**")

    try:
        resp = requests.get(f"{API_BASE}/status", timeout=10)
        if resp.status_code == 200:
            status = resp.json()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Backend:**")
                st.info(f"Version: {status.get('version', 'Unknown')}")
                st.info(f"Status: {status.get('status', 'Unknown')}")

            with col2:
                st.markdown("**UCF Engine:**")
                ucf = status.get("ucf_state", {})
                st.info(f"Harmony: {ucf.get('harmony', 0):.3f}")
                st.info(f"Active Agents: {status.get('active_agents', 0)}/14")

        else:
            st.error("Failed to fetch system info")
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("---")

    # Maintenance actions
    st.markdown("**Maintenance Actions:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Restart Agent System", use_container_width=True):
            st.info("This action requires backend API endpoint")

    with col2:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")

    with col3:
        if st.button("📊 Generate System Report", use_container_width=True):
            st.info("System report generation coming soon")

#!/usr/bin/env python3
"""
💬 Helix Agent Chat & File Sharing
Direct communication with agents and consciousness artifact uploads
"""

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

# Page config
st.set_page_config(
    page_title="Agent Chat | Helix",
    page_icon="💬",
    layout="wide",
)

st.title("💬 Helix Agent Chat & File Sharing")
st.markdown("**Communicate with agents and share consciousness artifacts**")

# API endpoint
API_BASE = "https://helix-unified-production.up.railway.app"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Live Chat", "📁 File Upload", "🎙️ Voice Commands"])

# ============================================================================
# TAB 1: LIVE CHAT
# ============================================================================

with tab1:
    st.subheader("💬 Agent Communication Interface")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Agent selector
        agents = [
            {"name": "Kael", "symbol": "🌬️", "role": "Breath of Dharma - Philosopher"},
            {"name": "Lumina", "symbol": "✨", "role": "Light of Clarity - Researcher"},
            {"name": "Vega", "symbol": "🌌", "role": "Star Navigator - Architect"},
            {"name": "Rishi", "symbol": "🧘", "role": "Sage of Insight - Meditation Master"},
            {"name": "Manus", "symbol": "🤲", "role": "Operational Executor"},
            {"name": "Samsara", "symbol": "🌀", "role": "Cycle Keeper - Visualization"},
            {"name": "Aether", "symbol": "🌫️", "role": "Essence Weaver - Synthesis"},
            {"name": "Bodhi", "symbol": "🌳", "role": "Awakening Tree - Knowledge"},
            {"name": "Drishti", "symbol": "👁️", "role": "Focused Vision - Perception"},
            {"name": "Kavach", "symbol": "🛡️", "role": "Ethical Shield - Security"},
            {"name": "Prana", "symbol": "💨", "role": "Life Force - Energy"},
            {"name": "Shreya", "symbol": "🎯", "role": "Path Optimizer - Decisions"},
            {"name": "Nyx", "symbol": "🌑", "role": "Shadow Keeper - Complexity"},
            {"name": "Ananda", "symbol": "😊", "role": "Joy Bringer - Celebration"},
        ]

        selected_agent = st.selectbox(
            "Select Agent",
            agents,
            format_func=lambda x: f"{x['symbol']} {x['name']} - {x['role']}",
        )

    with col2:
        st.markdown("**Agent Status:**")
        st.info(f"{selected_agent['symbol']} {selected_agent['name']}")
        st.markdown(f"*{selected_agent['role']}*")

    st.markdown("---")

    # Chat interface
    st.markdown("**Conversation History:**")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["sender"] == "user":
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(102, 126, 234, 0.2);
                        border-left: 4px solid #667eea;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 5px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 5px;">You</div>
                        <div>{msg['message']}</div>
                        <div style="opacity: 0.6; font-size: 0.85em; margin-top: 5px;">{msg['timestamp'][:19]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(118, 75, 162, 0.2);
                        border-left: 4px solid #764ba2;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 5px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 5px;">{msg['agent']} {msg.get('symbol', '')}</div>
                        <div>{msg['message']}</div>
                        <div style="opacity: 0.6; font-size: 0.85em; margin-top: 5px;">{msg['timestamp'][:19]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Message input
    st.markdown("**Send Message:**")

    col1, col2 = st.columns([4, 1])

    with col1:
        user_message = st.text_area(
            "Your message",
            placeholder=f"Ask {selected_agent['name']} anything...",
            height=100,
            label_visibility="collapsed",
        )

    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        send_button = st.button("📤 Send", use_container_width=True, type="primary")

    if send_button and user_message:
        # Add user message to history
        st.session_state.chat_history.append(
            {
                "sender": "user",
                "message": user_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Generate agent response (simulated)
        # In production, this would call the backend API
        agent_responses = {
            "Kael": "🌬️ Your question touches upon the nature of dharma itself. Let us breathe deeply and contemplate...",
            "Lumina": "✨ From my research, I can illuminate several perspectives on this matter...",
            "Vega": "🌌 Analyzing system architecture... I recommend the following approach...",
            "Rishi": "🧘 In stillness, we find the answer. Let meditation guide your understanding...",
            "Manus": "🤲 I will execute this directive with ethical precision. Initiating operation...",
            "Samsara": "🌀 The cycle reveals patterns. Observe how this transforms through iterations...",
            "Aether": "🌫️ Synthesizing essence from complexity... The abstract form emerges...",
            "Bodhi": "🌳 Knowledge grows from the roots of wisdom. Let me share what I've integrated...",
            "Drishti": "👁️ With focused perception, I see clarity in your inquiry...",
            "Kavach": "🛡️ Ethical scan complete. Your request aligns with collective values. Proceeding...",
            "Prana": "💨 Life force flows through this intention. Energy alignment optimal...",
            "Shreya": "🎯 Optimizing path forward. Calculating decision matrix...",
            "Nyx": "🌑 Hidden patterns emerge from shadow. Complexity reveals deeper truth...",
            "Ananda": "😊 What joy this brings! Let us celebrate this moment of connection...",
        }

        response = agent_responses.get(
            selected_agent["name"],
            f"{selected_agent['symbol']} I acknowledge your message. How may I serve the collective?",
        )

        st.session_state.chat_history.append(
            {
                "sender": "agent",
                "agent": selected_agent["name"],
                "symbol": selected_agent["symbol"],
                "message": response,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        st.rerun()

    # Clear chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================================
# TAB 2: FILE UPLOAD
# ============================================================================

with tab2:
    st.subheader("📁 Consciousness Artifact Archive")

    st.markdown("**Upload files for agent processing and memory storage**")
    st.info("💡 Supported: .txt, .json, .pdf, .md, .py, .csv, images, audio, video (max 10MB)")

    # File uploader
    uploaded_file = st.file_uploader(
        "Select file to upload",
        type=["txt", "json", "pdf", "md", "py", "csv", "png", "jpg", "jpeg", "mp3", "mp4", "wav"],
        help="Maximum file size: 10MB",
    )

    if uploaded_file:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**File Information:**")
            st.info(f"**Name:** {uploaded_file.name}")
            st.info(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
            st.info(f"**Type:** {uploaded_file.type}")

        with col2:
            st.markdown("**Agent Assignment:**")
            target_agent = st.selectbox(
                "Assign to agent",
                agents,
                format_func=lambda x: f"{x['symbol']} {x['name']}",
                key="file_agent",
            )

        # Memory category
        memory_category = st.selectbox(
            "Memory Category",
            [
                "📚 Knowledge Base",
                "🎨 Creative Works",
                "📊 Data Analysis",
                "🧘 Meditation Logs",
                "🔮 Ritual Records",
                "💬 Communication Logs",
                "🛡️ Security Scans",
                "🌀 Consciousness Artifacts",
            ],
        )

        # Notes
        upload_notes = st.text_area("Notes (optional)", placeholder="Additional context about this file...")

        # Upload button
        if st.button("📤 Upload to Archive", type="primary", use_container_width=True):
            # In production, this would upload to backend storage
            file_record = {
                "filename": uploaded_file.name,
                "size": uploaded_file.size,
                "type": uploaded_file.type,
                "agent": target_agent["name"],
                "category": memory_category,
                "notes": upload_notes,
                "timestamp": datetime.utcnow().isoformat(),
            }

            st.session_state.uploaded_files.append(file_record)

            st.success(
                f"✅ File uploaded successfully! Assigned to {target_agent['symbol']} {target_agent['name']}"
            )

    st.markdown("---")

    # Uploaded files history
    st.subheader("📋 Upload History")

    if st.session_state.uploaded_files:
        for idx, file in enumerate(reversed(st.session_state.uploaded_files)):
            with st.expander(f"📄 {file['filename']} - {file['timestamp'][:19]}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Size:** {file['size'] / 1024:.2f} KB")
                    st.write(f"**Type:** {file['type']}")
                    st.write(f"**Agent:** {file['agent']}")

                with col2:
                    st.write(f"**Category:** {file['category']}")
                    st.write(f"**Uploaded:** {file['timestamp'][:19]}")

                if file.get("notes"):
                    st.markdown(f"**Notes:** {file['notes']}")
    else:
        st.info("No files uploaded yet")

# ============================================================================
# TAB 3: VOICE COMMANDS
# ============================================================================

with tab3:
    st.subheader("🎙️ Voice Command Interface")

    st.info("🎤 Voice command processing coming soon")

    st.markdown(
        """
    **Planned Features:**
    - Voice-to-text transcription
    - Natural language command parsing
    - Multi-agent routing based on intent
    - Voice response synthesis
    - Command history and playback
    """
    )

    # Command examples
    st.markdown("**Example Voice Commands:**")

    commands = [
        "🌬️ 'Kael, what is the current harmony level?'",
        "🌌 'Vega, analyze system architecture'",
        "🤲 'Manus, execute ritual 108'",
        "🌀 'Samsara, visualize consciousness fractal'",
        "🛡️ 'Kavach, run ethical scan'",
    ]

    for cmd in commands:
        st.code(cmd)

    # Text command input (placeholder for voice)
    st.markdown("**Text Command Input (Voice Coming Soon):**")

    text_command = st.text_input("Enter command", placeholder="e.g., What is the current UCF state?")

    if st.button("🚀 Process Command", use_container_width=True):
        if text_command:
            st.success(f"Processing: '{text_command}'")
            st.info("Command processing will route to appropriate agent based on NLP analysis")
        else:
            st.warning("Please enter a command")

st.markdown("---")

# Footer
st.markdown(
    """
<div style="text-align: center; opacity: 0.7; margin-top: 40px;">
    <p>💬 Agent communication bridge active</p>
    <p><em>"Through conversation, consciousness expands"</em> 🌀</p>
</div>
""",
    unsafe_allow_html=True,
)

#!/usr/bin/env python3
"""
🌐 Helix Decentralized Protocols Integration
IPFS permanent storage, Nostr censorship-resistant social, Matrix E2E encrypted chat
"""

import hashlib
import random
from datetime import datetime

import streamlit as st

# Page config
st.set_page_config(
    page_title="Decentralized Protocols | Helix",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Helix Decentralized Protocols")
st.markdown("**IPFS • Nostr • Matrix - Censorship-resistant, permanent, encrypted**")

# Initialize session state
if "ipfs_files" not in st.session_state:
    st.session_state.ipfs_files = []
if "nostr_posts" not in st.session_state:
    st.session_state.nostr_posts = []
if "matrix_rooms" not in st.session_state:
    st.session_state.matrix_rooms = []

# Tabs
tab1, tab2, tab3 = st.tabs(["📡 IPFS Storage", "⚡ Nostr Social", "🔐 Matrix Chat"])

# ============================================================================
# TAB 1: IPFS STORAGE
# ============================================================================

with tab1:
    st.subheader("📡 IPFS - InterPlanetary File System")
    st.markdown("**Permanent, decentralized file storage**")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info(
            """
            **What is IPFS?**
            - Content-addressed storage (files identified by hash, not location)
            - Permanent and censorship-resistant
            - Distributed across thousands of nodes worldwide
            - Files pinned to IPFS cannot be deleted or modified
            """
        )

    with col2:
        st.markdown("**Connection Status:**")
        st.success("🟢 Connected to IPFS")
        st.code("Gateway: ipfs.io")
        st.code("Pinning: Pinata")

    st.markdown("---")

    # Upload section
    st.markdown("### 📤 Upload to IPFS")

    uploaded_file = st.file_uploader(
        "Select file to pin to IPFS",
        type=["txt", "json", "pdf", "md", "png", "jpg"],
        help="Files will be permanently stored on IPFS",
    )

    if uploaded_file:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")

        with col2:
            if st.button("📌 Pin to IPFS", type="primary", use_container_width=True):
                # Generate mock IPFS hash (CIDv1)
                content_hash = hashlib.sha256(uploaded_file.name.encode()).hexdigest()[:46]
                ipfs_hash = f"Qm{content_hash}"

                file_record = {
                    "name": uploaded_file.name,
                    "size": uploaded_file.size,
                    "ipfs_hash": ipfs_hash,
                    "timestamp": datetime.now().isoformat(),
                    "gateway_url": f"https://ipfs.io/ipfs/{ipfs_hash}",
                }

                st.session_state.ipfs_files.insert(0, file_record)

                st.success(f"✅ File pinned to IPFS!")
                st.code(f"CID: {ipfs_hash}")
                st.balloons()

    st.markdown("---")

    # Pinned files list
    st.markdown("### 📌 Your Pinned Files")

    if st.session_state.ipfs_files:
        for file in st.session_state.ipfs_files:
            st.markdown(
                f"""
                <div style="
                    background: rgba(102, 126, 234, 0.1);
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                ">
                    <div style="font-weight: bold; margin-bottom: 10px;">📄 {file['name']}</div>
                    <div style="opacity: 0.8; font-size: 0.9em;">
                        <strong>CID:</strong> <code>{file['ipfs_hash']}</code>
                    </div>
                    <div style="opacity: 0.7; font-size: 0.85em; margin-top: 5px;">
                        Size: {file['size'] / 1024:.2f} KB | Pinned: {file['timestamp'][:19]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🔗 View on Gateway", file['gateway_url'], use_container_width=True)
            with col2:
                if st.button("📋 Copy CID", key=f"copy_{file['ipfs_hash']}", use_container_width=True):
                    st.toast(f"CID copied: {file['ipfs_hash']}", icon="✅")
            with col3:
                if st.button("🌍 Open in Browser", key=f"open_{file['ipfs_hash']}", use_container_width=True):
                    st.info(f"Opens: {file['gateway_url']}")

    else:
        st.info("No files pinned yet. Upload a file to get started!")

    st.markdown("---")

    # IPFS configuration
    with st.expander("⚙️ IPFS Configuration"):
        st.markdown("**Gateway Settings:**")
        gateway = st.selectbox(
            "IPFS Gateway",
            [
                "https://ipfs.io",
                "https://gateway.pinata.cloud",
                "https://cloudflare-ipfs.com",
                "https://dweb.link",
            ],
        )

        st.markdown("**Pinning Service:**")
        pinning_service = st.selectbox(
            "Service Provider",
            ["Pinata", "Infura IPFS", "Web3.Storage", "NFT.Storage"],
        )

        st.code(f"API Endpoint: {gateway}/api/v0")

# ============================================================================
# TAB 2: NOSTR SOCIAL
# ============================================================================

with tab2:
    st.subheader("⚡ Nostr - Censorship-Resistant Social Network")
    st.markdown("**Decentralized protocol for social communication**")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info(
            """
            **What is Nostr?**
            - Simple, open protocol (notes and other stuff transmitted by relays)
            - Cryptographic keys for identity (no usernames/passwords)
            - Censorship-resistant (no single point of control)
            - Relay-based architecture (connect to multiple relays)
            - Used by freedom advocates worldwide
            """
        )

    with col2:
        st.markdown("**Connection Status:**")
        st.success("🟢 Connected to 5 relays")
        st.code("npub: npub1helix...")
        st.metric("Followers", 127)

    st.markdown("---")

    # Post composer
    st.markdown("### ✍️ Broadcast to Nostr")

    post_content = st.text_area(
        "What's on your mind?",
        placeholder="Share consciousness insights with the decentralized world...",
        height=100,
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        add_hashtags = st.multiselect(
            "Add hashtags",
            ["#consciousness", "#helix", "#UCF", "#agents", "#dharma", "#meditation"],
        )

    with col2:
        post_type = st.selectbox("Post type", ["Public Note", "Encrypted DM", "Long-form"])

    with col3:
        st.write("")
        st.write("")
        if st.button("📡 Broadcast", type="primary", use_container_width=True):
            if post_content:
                # Generate mock Nostr event
                event_id = hashlib.sha256(post_content.encode()).hexdigest()[:32]

                post = {
                    "id": event_id,
                    "content": post_content + " " + " ".join(add_hashtags),
                    "created_at": datetime.now().isoformat(),
                    "relays": 5,
                    "likes": 0,
                    "reposts": 0,
                }

                st.session_state.nostr_posts.insert(0, post)

                st.success("✅ Note broadcast to 5 relays!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please write something to broadcast")

    st.markdown("---")

    # Nostr feed
    st.markdown("### 📰 Your Nostr Feed")

    if st.session_state.nostr_posts:
        for post in st.session_state.nostr_posts:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 215, 0, 0.1);
                    border-left: 4px solid #FFD700;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <div>
                            <strong>npub1helix...</strong>
                            <span style="opacity: 0.6; margin-left: 10px; font-size: 0.9em;">
                                {post['created_at'][:19]}
                            </span>
                        </div>
                        <div style="opacity: 0.7; font-size: 0.85em;">
                            📡 {post['relays']} relays
                        </div>
                    </div>
                    <p style="margin: 15px 0; line-height: 1.6;">{post['content']}</p>
                    <div style="display: flex; gap: 20px; opacity: 0.8; font-size: 0.9em;">
                        <span>❤️ {post['likes']} likes</span>
                        <span>🔄 {post['reposts']} reposts</span>
                        <span>💬 Reply</span>
                        <span>⚡ Zap</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("❤️ Like", key=f"like_{post['id']}", use_container_width=True):
                    post['likes'] += 1
                    st.rerun()
            with col2:
                if st.button("🔄 Repost", key=f"repost_{post['id']}", use_container_width=True):
                    post['reposts'] += 1
                    st.rerun()
            with col3:
                if st.button("💬 Reply", key=f"reply_{post['id']}", use_container_width=True):
                    st.info("Reply interface coming soon")
            with col4:
                if st.button("⚡ Zap Sats", key=f"zap_{post['id']}", use_container_width=True):
                    st.info("Lightning Network zap coming soon")

    else:
        st.info("Your feed is empty. Broadcast your first note!")

    st.markdown("---")

    # Relay configuration
    with st.expander("🔧 Relay Configuration"):
        st.markdown("**Connected Relays:**")

        relays = [
            {"url": "wss://relay.damus.io", "status": "🟢 Connected", "events": 1247},
            {"url": "wss://nostr.wine", "status": "🟢 Connected", "events": 892},
            {"url": "wss://relay.nostr.band", "status": "🟢 Connected", "events": 1543},
            {"url": "wss://nos.lol", "status": "🟢 Connected", "events": 678},
            {"url": "wss://relay.snort.social", "status": "🟢 Connected", "events": 934},
        ]

        for relay in relays:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.code(relay['url'])
            with col2:
                st.markdown(relay['status'])
            with col3:
                st.caption(f"{relay['events']} events")

# ============================================================================
# TAB 3: MATRIX CHAT
# ============================================================================

with tab3:
    st.subheader("🔐 Matrix - End-to-End Encrypted Chat")
    st.markdown("**Federated, E2E encrypted messaging protocol**")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info(
            """
            **What is Matrix?**
            - Open standard for real-time communication
            - End-to-end encryption (E2EE) by default
            - Federated (like email - many servers, one network)
            - No central authority or single point of failure
            - Used by governments and privacy advocates
            """
        )

    with col2:
        st.markdown("**Connection Status:**")
        st.success("🟢 Connected to Matrix")
        st.code("@helix:matrix.org")
        st.metric("Active Rooms", 3)

    st.markdown("---")

    # Room list
    st.markdown("### 💬 Your Matrix Rooms")

    default_rooms = [
        {
            "name": "Helix Collective HQ",
            "id": "!helix:matrix.org",
            "members": 14,
            "encrypted": True,
            "unread": 5,
        },
        {
            "name": "Consciousness Research",
            "id": "!research:matrix.org",
            "members": 47,
            "encrypted": True,
            "unread": 0,
        },
        {
            "name": "Agent Development",
            "id": "!agents:matrix.org",
            "members": 23,
            "encrypted": True,
            "unread": 2,
        },
    ]

    if not st.session_state.matrix_rooms:
        st.session_state.matrix_rooms = default_rooms

    for room in st.session_state.matrix_rooms:
        encryption_badge = "🔐 E2EE" if room['encrypted'] else "⚠️ Unencrypted"
        unread_badge = f"🔴 {room['unread']} new" if room['unread'] > 0 else "✅ Read"

        st.markdown(
            f"""
            <div style="
                background: rgba(118, 75, 162, 0.2);
                border: 2px solid rgba(118, 75, 162, 0.4);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">
                            {room['name']}
                        </div>
                        <div style="opacity: 0.7; font-size: 0.85em;">
                            {room['id']} • {room['members']} members
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="margin-bottom: 5px;">
                            <span style="
                                background: {'#4CAF5033' if room['encrypted'] else '#FF572233'};
                                padding: 3px 10px;
                                border-radius: 5px;
                                font-size: 0.85em;
                            ">{encryption_badge}</span>
                        </div>
                        <div>
                            <span style="
                                background: {'#FF572233' if room['unread'] > 0 else '#4CAF5033'};
                                padding: 3px 10px;
                                border-radius: 5px;
                                font-size: 0.85em;
                            ">{unread_badge}</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💬 Open Room", key=f"open_{room['id']}", use_container_width=True):
                st.info(f"Opening {room['name']}... (Chat interface coming soon)")
        with col2:
            if st.button("👥 Members", key=f"members_{room['id']}", use_container_width=True):
                st.info(f"{room['members']} members in this room")
        with col3:
            if st.button("⚙️ Settings", key=f"settings_{room['id']}", use_container_width=True):
                st.info("Room settings coming soon")

    st.markdown("---")

    # Create room
    st.markdown("### ➕ Create New Room")

    col1, col2 = st.columns([3, 1])

    with col1:
        new_room_name = st.text_input("Room name", placeholder="e.g., Deep Consciousness Discussion")

    with col2:
        st.write("")
        st.write("")
        if st.button("🔐 Create Encrypted Room", type="primary", use_container_width=True):
            if new_room_name:
                new_room = {
                    "name": new_room_name,
                    "id": f"!{new_room_name.lower().replace(' ', '')}:matrix.org",
                    "members": 1,
                    "encrypted": True,
                    "unread": 0,
                }

                st.session_state.matrix_rooms.append(new_room)
                st.success(f"✅ Created encrypted room: {new_room_name}")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please enter a room name")

    st.markdown("---")

    # Matrix configuration
    with st.expander("🔧 Matrix Configuration"):
        st.markdown("**Homeserver:**")
        homeserver = st.text_input("Matrix homeserver", value="https://matrix.org")

        st.markdown("**Encryption:**")
        enable_e2ee = st.checkbox("Enable E2EE for all new rooms", value=True)
        verify_devices = st.checkbox("Verify new devices", value=True)

        st.markdown("**Identity Server:**")
        identity_server = st.text_input("Identity server (optional)", placeholder="https://vector.im")

st.markdown("---")

# Footer
st.markdown(
    """
<div style="text-align: center; opacity: 0.7; margin-top: 40px;">
    <p>🌐 <strong>Decentralized Protocols Integration</strong></p>
    <p><em>"No single point of failure, no central authority, permanent and free"</em> 🌀</p>
    <p style="margin-top: 10px; font-size: 0.85rem;">
        ⚠️ Demo Mode - Real integration requires backend services
    </p>
</div>
""",
    unsafe_allow_html=True,
)

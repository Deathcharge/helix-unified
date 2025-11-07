#!/usr/bin/env python3
"""
₿ Helix Web3 & Cryptocurrency Integration
Accept Bitcoin, Ethereum, and other crypto for consciousness services
"""

import streamlit as st
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="Web3 & Crypto | Helix",
    page_icon="₿",
    layout="wide",
)

st.title("₿ Helix Web3 & Cryptocurrency Integration")
st.markdown("**Decentralized payments for consciousness services**")
st.markdown("*Accept Bitcoin, Ethereum, and more for premium features*")

# Initialize session state
if "crypto_wallet" not in st.session_state:
    st.session_state.crypto_wallet = {
        "btc_balance": 0.00000000,
        "eth_balance": 0.000000000000000000,
        "transactions": [],
        "connected": False,
    }

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💰 Wallet", "💳 Payments", "📊 Transactions", "⚙️ Settings"])

# ============================================================================
# TAB 1: WALLET
# ============================================================================

with tab1:
    st.subheader("💰 Web3 Wallet Connection")

    if not st.session_state.crypto_wallet["connected"]:
        st.info("🔗 Connect your Web3 wallet to accept cryptocurrency payments")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div style="
                    background: rgba(102, 126, 234, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                ">
                    <div style="font-size: 3em; margin-bottom: 15px;">🦊</div>
                    <h3>MetaMask</h3>
                    <p style="opacity: 0.8;">Most popular Ethereum wallet</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Connect MetaMask", use_container_width=True, type="primary"):
                st.session_state.crypto_wallet["connected"] = True
                st.session_state.crypto_wallet["wallet_type"] = "MetaMask"
                st.session_state.crypto_wallet["address"] = "0x" + "".join(random.choices("0123456789abcdef", k=40))
                st.success("✅ MetaMask connected!")
                st.rerun()

        with col2:
            st.markdown(
                """
                <div style="
                    background: rgba(118, 75, 162, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                ">
                    <div style="font-size: 3em; margin-bottom: 15px;">🔷</div>
                    <h3>WalletConnect</h3>
                    <p style="opacity: 0.8;">Connect any mobile wallet</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Connect WalletConnect", use_container_width=True):
                st.session_state.crypto_wallet["connected"] = True
                st.session_state.crypto_wallet["wallet_type"] = "WalletConnect"
                st.session_state.crypto_wallet["address"] = "0x" + "".join(random.choices("0123456789abcdef", k=40))
                st.success("✅ WalletConnect connected!")
                st.rerun()

        with col3:
            st.markdown(
                """
                <div style="
                    background: rgba(255, 107, 107, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                ">
                    <div style="font-size: 3em; margin-bottom: 15px;">₿</div>
                    <h3>Bitcoin Wallet</h3>
                    <p style="opacity: 0.8;">Native BTC support</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Connect Bitcoin", use_container_width=True):
                st.session_state.crypto_wallet["connected"] = True
                st.session_state.crypto_wallet["wallet_type"] = "Bitcoin"
                st.session_state.crypto_wallet["address"] = "bc1q" + "".join(random.choices("0123456789abcdefghjkmnpqrstuvwxyz", k=38))
                st.success("✅ Bitcoin wallet connected!")
                st.rerun()

    else:
        # Wallet connected - show balance
        st.success(f"✅ Connected: {st.session_state.crypto_wallet['wallet_type']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💼 Wallet Address")
            st.code(st.session_state.crypto_wallet["address"])
            if st.button("📋 Copy Address"):
                st.toast("Address copied to clipboard!", icon="✅")

        with col2:
            st.markdown("### 💰 Balances")

            col_btc, col_eth = st.columns(2)
            with col_btc:
                st.metric(
                    "Bitcoin (BTC)",
                    f"₿ {st.session_state.crypto_wallet['btc_balance']:.8f}",
                    delta=f"${st.session_state.crypto_wallet['btc_balance'] * 45000:.2f} USD"
                )

            with col_eth:
                st.metric(
                    "Ethereum (ETH)",
                    f"Ξ {st.session_state.crypto_wallet['eth_balance']:.18f}",
                    delta=f"${st.session_state.crypto_wallet['eth_balance'] * 2500:.2f} USD"
                )

        st.markdown("---")

        # Supported cryptocurrencies
        st.markdown("### 🪙 Supported Cryptocurrencies")

        cryptos = [
            {"name": "Bitcoin", "symbol": "BTC", "icon": "₿", "network": "Bitcoin Mainnet"},
            {"name": "Ethereum", "symbol": "ETH", "icon": "Ξ", "network": "Ethereum Mainnet"},
            {"name": "USD Coin", "symbol": "USDC", "icon": "💵", "network": "Ethereum / Polygon"},
            {"name": "Tether", "symbol": "USDT", "icon": "💵", "network": "Ethereum / Tron"},
            {"name": "Polygon", "symbol": "MATIC", "icon": "⬡", "network": "Polygon Mainnet"},
            {"name": "Solana", "symbol": "SOL", "icon": "◎", "network": "Solana Mainnet"},
        ]

        cols = st.columns(3)
        for idx, crypto in enumerate(cryptos):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.05);
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 15px;
                    ">
                        <div style="font-size: 2em; text-align: center;">{crypto['icon']}</div>
                        <div style="text-align: center; font-weight: bold; margin-top: 10px;">
                            {crypto['name']} ({crypto['symbol']})
                        </div>
                        <div style="text-align: center; opacity: 0.7; font-size: 0.85em; margin-top: 5px;">
                            {crypto['network']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if st.button("🔌 Disconnect Wallet", use_container_width=True):
            st.session_state.crypto_wallet["connected"] = False
            st.rerun()

# ============================================================================
# TAB 2: PAYMENTS
# ============================================================================

with tab2:
    st.subheader("💳 Accept Cryptocurrency Payments")

    if not st.session_state.crypto_wallet["connected"]:
        st.warning("⚠️ Please connect a wallet first (see Wallet tab)")
    else:
        st.markdown("**Create payment requests for consciousness services**")

        # Payment products
        products = [
            {
                "name": "Premium Consciousness Analysis",
                "price_usd": 47,
                "description": "Deep UCF metrics analysis with personalized insights",
            },
            {
                "name": "1-on-1 Agent Consultation",
                "price_usd": 99,
                "description": "Private session with consciousness agents",
            },
            {
                "name": "Consciousness Circle Membership",
                "price_usd": 129,
                "description": "Monthly subscription to exclusive community",
            },
            {
                "name": "Custom Ritual Design",
                "price_usd": 199,
                "description": "Personalized Z-88 ritual for your consciousness goals",
            },
        ]

        selected_product = st.selectbox(
            "Select Service",
            products,
            format_func=lambda x: f"{x['name']} - ${x['price_usd']}",
        )

        st.markdown(f"**{selected_product['name']}**")
        st.markdown(f"*{selected_product['description']}*")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Price (USD)", f"${selected_product['price_usd']}")

        with col2:
            crypto_currency = st.selectbox("Payment Currency", ["BTC", "ETH", "USDC", "USDT"])

            # Mock conversion rates
            rates = {"BTC": 45000, "ETH": 2500, "USDC": 1, "USDT": 1}
            crypto_amount = selected_product['price_usd'] / rates[crypto_currency]

            if crypto_currency in ["BTC", "ETH"]:
                st.metric(f"Price ({crypto_currency})", f"{crypto_amount:.8f}")
            else:
                st.metric(f"Price ({crypto_currency})", f"{crypto_amount:.2f}")

        st.markdown("---")

        if st.button("🚀 Generate Payment Request", type="primary", use_container_width=True):
            # Generate mock payment request
            payment_id = "PAY-" + "".join(random.choices("0123456789ABCDEF", k=16))

            st.success(f"✅ Payment request generated: {payment_id}")

            # Show payment QR code placeholder
            st.markdown("### 📱 Payment QR Code")
            st.info(
                "In production, this would show a QR code for mobile wallet scanning.\n\n"
                f"Payment Address: {st.session_state.crypto_wallet['address']}\n"
                f"Amount: {crypto_amount:.8f} {crypto_currency}\n"
                f"Memo: {payment_id}"
            )

            # Add to transactions
            transaction = {
                "id": payment_id,
                "type": "Payment Request",
                "product": selected_product['name'],
                "amount": crypto_amount,
                "currency": crypto_currency,
                "status": "Pending",
                "timestamp": datetime.now().isoformat(),
            }

            st.session_state.crypto_wallet["transactions"].insert(0, transaction)

            st.balloons()

# ============================================================================
# TAB 3: TRANSACTIONS
# ============================================================================

with tab3:
    st.subheader("📊 Transaction History")

    if not st.session_state.crypto_wallet["transactions"]:
        st.info("No transactions yet. Create a payment request to get started!")
    else:
        for tx in st.session_state.crypto_wallet["transactions"]:
            status_color = {
                "Pending": "#FFC107",
                "Confirmed": "#4CAF50",
                "Failed": "#FF5722",
            }.get(tx["status"], "#9E9E9E")

            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 255, 255, 0.05);
                    border-left: 4px solid {status_color};
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: bold; margin-bottom: 5px;">{tx['product']}</div>
                            <div style="opacity: 0.8;">{tx['amount']:.8f} {tx['currency']}</div>
                            <div style="opacity: 0.6; font-size: 0.85em; margin-top: 5px;">
                                {tx['timestamp'][:19]} | {tx['id']}
                            </div>
                        </div>
                        <div style="
                            background: {status_color}33;
                            padding: 5px 15px;
                            border-radius: 5px;
                        ">
                            {tx['status']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================================
# TAB 4: SETTINGS
# ============================================================================

with tab4:
    st.subheader("⚙️ Web3 Settings")

    st.markdown("### 🔗 Network Configuration")

    networks = [
        {"name": "Ethereum Mainnet", "chain_id": 1, "rpc": "https://mainnet.infura.io/v3/YOUR_KEY"},
        {"name": "Polygon Mainnet", "chain_id": 137, "rpc": "https://polygon-rpc.com"},
        {"name": "Bitcoin Mainnet", "chain_id": None, "rpc": "https://blockstream.info/api"},
        {"name": "Sepolia Testnet", "chain_id": 11155111, "rpc": "https://sepolia.infura.io/v3/YOUR_KEY"},
    ]

    selected_network = st.selectbox(
        "Active Network",
        networks,
        format_func=lambda x: x['name'],
    )

    st.code(f"RPC URL: {selected_network['rpc']}")
    if selected_network['chain_id']:
        st.code(f"Chain ID: {selected_network['chain_id']}")

    st.markdown("---")

    st.markdown("### 💰 Payment Settings")

    col1, col2 = st.columns(2)

    with col1:
        auto_convert = st.checkbox("Auto-convert to USD", value=True)
        st.caption("Automatically convert crypto payments to USD")

        email_notifications = st.checkbox("Email notifications", value=True)
        st.caption("Receive email for each transaction")

    with col2:
        webhook_url = st.text_input("Webhook URL", placeholder="https://your-server.com/webhook")
        st.caption("Send transaction data to your server")

        confirmation_blocks = st.number_input("Required confirmations", min_value=1, max_value=12, value=3)
        st.caption("Wait for N block confirmations")

    st.markdown("---")

    st.markdown("### 🔐 Security")

    st.warning("⚠️ **Important Security Notes:**")
    st.markdown(
        """
        - Never share your private keys
        - Always verify transaction details before signing
        - Use hardware wallets for large amounts
        - Enable 2FA on your exchange accounts
        - This is a demo - connect real wallet at your own risk
        """
    )

    if st.button("🗑️ Clear All Transaction Data", use_container_width=True):
        st.session_state.crypto_wallet["transactions"] = []
        st.success("Transaction history cleared")
        st.rerun()

st.markdown("---")

# Footer
st.markdown(
    """
<div style="text-align: center; opacity: 0.7; margin-top: 40px;">
    <p>₿ <strong>Web3 & Cryptocurrency Integration</strong></p>
    <p><em>"Decentralized consciousness, decentralized payments"</em> 🌀</p>
    <p style="margin-top: 10px; font-size: 0.85rem;">
        ⚠️ Demo Mode - Connect real wallets at your own risk
    </p>
</div>
""",
    unsafe_allow_html=True,
)

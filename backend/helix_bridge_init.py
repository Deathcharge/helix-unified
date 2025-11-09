"""
Helix Bridge Initialization - Connects Discord bot with Web Chat.

This module initializes the bidirectional bridge between Discord and web chat.
"""
import logging

logger = logging.getLogger(__name__)


async def initialize_helix_bridge(discord_bot, web_connection_manager):
    """
    Initialize the Discord ↔ Web Chat bridge.

    Args:
        discord_bot: Discord bot instance
        web_connection_manager: WebChatConnectionManager instance

    Returns:
        DiscordWebBridge instance
    """
    try:
        from backend.discord_web_bridge import setup_bridge_events

        logger.info("🌉 Initializing Helix Bridge (Discord ↔ Web Chat)...")

        # Set up bridge events on the Discord bot
        await setup_bridge_events(discord_bot, web_connection_manager)

        # Get the bridge instance
        from backend.discord_web_bridge import get_bridge
        bridge = get_bridge()

        if bridge:
            logger.info("✅ Helix Bridge initialized successfully!")
            logger.info("   📡 Discord → Web Chat: ENABLED")
            logger.info("   📡 Web Chat → Discord: ENABLED")
            return bridge
        else:
            logger.error("❌ Failed to initialize Helix Bridge")
            return None

    except Exception as e:
        logger.error(f"❌ Error initializing Helix Bridge: {e}", exc_info=True)
        return None


def get_web_chat_stats() -> dict:
    """
    Get current web chat statistics.

    Returns:
        Dictionary with connection stats
    """
    try:
        from backend.web_chat_server import connection_manager

        return {
            "active_connections": len(connection_manager.active_connections),
            "total_sessions": len(connection_manager.user_sessions),
            "users": list(connection_manager.user_sessions.values()),
        }
    except Exception as e:
        logger.error(f"Error getting web chat stats: {e}")
        return {
            "active_connections": 0,
            "total_sessions": 0,
            "users": [],
        }


def get_bridge_stats() -> dict:
    """
    Get current bridge statistics.

    Returns:
        Dictionary with bridge stats
    """
    try:
        from backend.discord_web_bridge import get_bridge

        bridge = get_bridge()
        if bridge:
            return {
                "enabled": bridge.enabled,
                "bridged_channels": len(bridge.bridged_channels),
                "channels": list(bridge.bridged_channels.items()),
            }
        else:
            return {
                "enabled": False,
                "bridged_channels": 0,
                "channels": [],
            }
    except Exception as e:
        logger.error(f"Error getting bridge stats: {e}")
        return {
            "enabled": False,
            "bridged_channels": 0,
            "channels": [],
        }

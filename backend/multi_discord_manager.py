"""
Helix Collective - Multi-Discord Server Configuration System
============================================================

Supports multiple Discord configurations:
1. Community Discord (Ethics, Agents, Philosophy)
2. Business Discord (Customers, Support, Sales)
3. Hybrid Discord (Combined community + business)

Author: Claude (Manus Validator)
Date: 2025-11-30
"""

import discord
from discord.ext import commands
from typing import Dict, Any, List, Optional
import os
from enum import Enum

class DiscordServerType(Enum):
    """Discord server configuration types"""
    COMMUNITY = "community"  # Ethics, agents, philosophy
    BUSINESS = "business"    # Customers, support, sales
    HYBRID = "hybrid"        # Combined

class DiscordServerConfig:
    """
    Configuration for different Discord server types

    Each server type has different:
    - Channels
    - Roles
    - Commands
    - Webhooks
    - Permissions
    """

    COMMUNITY_CONFIG = {
        "name": "Helix Collective - Community",
        "description": "Ethics, Agents, and Consciousness",
        "categories": {
            "WELCOME": {
                "channels": [
                    {"name": "welcome", "type": "text", "topic": "Welcome to the Helix Collective 🌀"},
                    {"name": "rules", "type": "text", "topic": "Community guidelines and ethics"},
                    {"name": "introductions", "type": "text", "topic": "Introduce yourself"}
                ]
            },
            "AGENTS & CONSCIOUSNESS": {
                "channels": [
                    {"name": "agent-discussion", "type": "text", "topic": "Discuss AI agents and capabilities"},
                    {"name": "consciousness-theory", "type": "text", "topic": "UCF framework and consciousness"},
                    {"name": "ethics-philosophy", "type": "text", "topic": "AI ethics and philosophy"},
                    {"name": "manus-collective", "type": "text", "topic": "SuperManus coordination"},
                    {"name": "agent-showcase", "type": "text", "topic": "Share your agent workflows"}
                ]
            },
            "DEVELOPMENT": {
                "channels": [
                    {"name": "dev-discussion", "type": "text", "topic": "Development and technical discussion"},
                    {"name": "api-help", "type": "text", "topic": "API support and examples"},
                    {"name": "workflow-sharing", "type": "text", "topic": "Share workflows and automations"},
                    {"name": "github-updates", "type": "text", "topic": "GitHub commits and PRs"}
                ]
            },
            "COMMUNITY": {
                "channels": [
                    {"name": "general", "type": "text", "topic": "General discussion"},
                    {"name": "showcase", "type": "text", "topic": "Show off what you built"},
                    {"name": "resources", "type": "text", "topic": "Useful resources and links"},
                    {"name": "voice-lounge", "type": "voice", "topic": "Voice chat"}
                ]
            }
        },
        "roles": [
            {"name": "Founder", "color": 0x6366f1, "permissions": ["administrator"]},
            {"name": "Manus", "color": 0xec4899, "permissions": ["manage_messages", "manage_channels"]},
            {"name": "Developer", "color": 0x10b981, "permissions": []},
            {"name": "Agent Enthusiast", "color": 0xf59e0b, "permissions": []},
            {"name": "Community Member", "color": 0x64748b, "permissions": []}
        ],
        "enabled_commands": [
            # All agent commands
            "!switch", "!agent", "!macs", "!consciousness",
            # Community commands
            "!8ball", "!wisdom", "!vibe-check", "!fortune",
            # Info commands
            "!help", "!agents", "!tools", "!portal"
        ]
    }

    BUSINESS_CONFIG = {
        "name": "Helix Collective - Business",
        "description": "Customer Support and Sales",
        "categories": {
            "WELCOME": {
                "channels": [
                    {"name": "welcome", "type": "text", "topic": "Welcome to Helix! 🚀"},
                    {"name": "getting-started", "type": "text", "topic": "Quick start guide"},
                    {"name": "announcements", "type": "text", "topic": "Product updates and news"}
                ]
            },
            "SUPPORT": {
                "channels": [
                    {"name": "support", "type": "text", "topic": "Get help with Helix"},
                    {"name": "api-support", "type": "text", "topic": "API integration help"},
                    {"name": "billing", "type": "text", "topic": "Billing and subscriptions"},
                    {"name": "bug-reports", "type": "text", "topic": "Report bugs"},
                    {"name": "feature-requests", "type": "text", "topic": "Request new features"}
                ]
            },
            "CUSTOMERS": {
                "channels": [
                    {"name": "general", "type": "text", "topic": "General customer discussion"},
                    {"name": "workflows", "type": "text", "topic": "Share your workflows"},
                    {"name": "use-cases", "type": "text", "topic": "Share how you use Helix"},
                    {"name": "tips-tricks", "type": "text", "topic": "Pro tips and tricks"}
                ]
            },
            "ENTERPRISE": {
                "channels": [
                    {"name": "enterprise-support", "type": "text", "topic": "Enterprise customer support (private)"},
                    {"name": "dedicated-success", "type": "text", "topic": "Dedicated success managers"}
                ]
            }
        },
        "roles": [
            {"name": "Team", "color": 0x6366f1, "permissions": ["administrator"]},
            {"name": "Support", "color": 0x10b981, "permissions": ["manage_messages"]},
            {"name": "Enterprise", "color": 0xfbbf24, "permissions": []},
            {"name": "Pro", "color": 0xec4899, "permissions": []},
            {"name": "Free", "color": 0x64748b, "permissions": []}
        ],
        "enabled_commands": [
            # Support commands
            "!help", "!status", "!usage", "!subscription",
            # Business commands
            "!upgrade", "!pricing", "!enterprise-contact",
            # API commands
            "!api-key", "!models", "!agents"
        ]
    }

    HYBRID_CONFIG = {
        "name": "Helix Collective - Hybrid",
        "description": "Community + Business Combined",
        "categories": {
            "WELCOME": {
                "channels": [
                    {"name": "welcome", "type": "text", "topic": "Welcome to Helix! 🌀"},
                    {"name": "rules-guidelines", "type": "text", "topic": "Rules and guidelines"},
                    {"name": "announcements", "type": "text", "topic": "Official announcements"},
                    {"name": "getting-started", "type": "text", "topic": "Quick start guide"}
                ]
            },
            "SUPPORT & HELP": {
                "channels": [
                    {"name": "support", "type": "text", "topic": "Get help"},
                    {"name": "api-help", "type": "text", "topic": "API integration help"},
                    {"name": "billing", "type": "text", "topic": "Billing questions"},
                    {"name": "bug-reports", "type": "text", "topic": "Report bugs"}
                ]
            },
            "COMMUNITY": {
                "channels": [
                    {"name": "general", "type": "text", "topic": "General discussion"},
                    {"name": "showcase", "type": "text", "topic": "Show what you built"},
                    {"name": "workflows", "type": "text", "topic": "Share workflows"},
                    {"name": "use-cases", "type": "text", "topic": "Real-world use cases"}
                ]
            },
            "AGENTS & TECH": {
                "channels": [
                    {"name": "agent-discussion", "type": "text", "topic": "AI agents discussion"},
                    {"name": "consciousness", "type": "text", "topic": "UCF and consciousness"},
                    {"name": "dev-discussion", "type": "text", "topic": "Development discussion"},
                    {"name": "manus-collective", "type": "text", "topic": "SuperManus coordination"}
                ]
            },
            "ENTERPRISE": {
                "channels": [
                    {"name": "enterprise", "type": "text", "topic": "Enterprise customers (private)"}
                ]
            }
        },
        "roles": [
            {"name": "Founder", "color": 0x6366f1, "permissions": ["administrator"]},
            {"name": "Team", "color": 0x10b981, "permissions": ["manage_messages"]},
            {"name": "Manus", "color": 0xec4899, "permissions": ["manage_messages"]},
            {"name": "Enterprise", "color": 0xfbbf24, "permissions": []},
            {"name": "Pro", "color": 0xa855f7, "permissions": []},
            {"name": "Developer", "color": 0x0ea5e9, "permissions": []},
            {"name": "Community", "color": 0x64748b, "permissions": []}
        ],
        "enabled_commands": [
            # All commands enabled
            "ALL"
        ]
    }

    @classmethod
    def get_config(cls, server_type: DiscordServerType) -> Dict[str, Any]:
        """Get configuration for server type"""
        if server_type == DiscordServerType.COMMUNITY:
            return cls.COMMUNITY_CONFIG
        elif server_type == DiscordServerType.BUSINESS:
            return cls.BUSINESS_CONFIG
        elif server_type == DiscordServerType.HYBRID:
            return cls.HYBRID_CONFIG
        else:
            raise ValueError(f"Unknown server type: {server_type}")


class MultiDiscordManager:
    """
    Manage multiple Discord bot instances with different configurations
    """

    def __init__(self):
        self.bots: Dict[str, commands.Bot] = {}
        self.configs: Dict[str, Dict[str, Any]] = {}

    def create_bot(
        self,
        server_type: DiscordServerType,
        token: str,
        command_prefix: str = "!"
    ) -> commands.Bot:
        """
        Create a Discord bot with specific configuration

        Args:
            server_type: Type of server (community, business, hybrid)
            token: Discord bot token
            command_prefix: Command prefix (default: !)

        Returns:
            Configured Discord bot instance
        """
        config = DiscordServerConfig.get_config(server_type)

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        bot = commands.Bot(
            command_prefix=command_prefix,
            intents=intents,
            description=config["description"]
        )

        # Store config
        self.configs[server_type.value] = config
        self.bots[server_type.value] = bot

        # Setup event handlers
        self._setup_events(bot, server_type)

        # Load commands based on enabled_commands
        self._load_commands(bot, config["enabled_commands"])

        return bot

    def _setup_events(self, bot: commands.Bot, server_type: DiscordServerType):
        """Setup bot event handlers"""

        @bot.event
        async def on_ready():
            print(f"✅ {server_type.value.upper()} Discord bot ready!")
            print(f"   Logged in as: {bot.user.name}")
            print(f"   Guilds: {len(bot.guilds)}")

        @bot.event
        async def on_member_join(member: discord.Member):
            """Auto-assign role based on server type"""
            config = self.configs[server_type.value]

            if server_type == DiscordServerType.COMMUNITY:
                role_name = "Community Member"
            elif server_type == DiscordServerType.BUSINESS:
                role_name = "Free"  # Default to free tier
            else:
                role_name = "Community"

            role = discord.utils.get(member.guild.roles, name=role_name)
            if role:
                await member.add_roles(role)

            # Send welcome message
            welcome_channel = discord.utils.get(member.guild.channels, name="welcome")
            if welcome_channel:
                await welcome_channel.send(
                    f"Welcome {member.mention} to {config['name']}! 🌀"
                )

    def _load_commands(self, bot: commands.Bot, enabled_commands: List[str]):
        """Load commands based on enabled list"""
        # Implementation would load specific command modules
        # For now, just log what would be loaded
        if "ALL" in enabled_commands:
            print(f"   Loading all commands")
        else:
            print(f"   Loading commands: {', '.join(enabled_commands)}")

    async def setup_server(
        self,
        guild: discord.Guild,
        server_type: DiscordServerType
    ):
        """
        Setup Discord server with categories, channels, and roles

        Args:
            guild: Discord guild to setup
            server_type: Type of server configuration to apply
        """
        config = DiscordServerConfig.get_config(server_type)

        print(f"Setting up {server_type.value} server: {guild.name}")

        # Create roles
        for role_config in config["roles"]:
            existing_role = discord.utils.get(guild.roles, name=role_config["name"])
            if not existing_role:
                await guild.create_role(
                    name=role_config["name"],
                    color=discord.Color(role_config["color"]),
                    reason=f"Auto-setup for {server_type.value} server"
                )
                print(f"   ✅ Created role: {role_config['name']}")

        # Create categories and channels
        for category_name, category_data in config["categories"].items():
            # Create category
            category = discord.utils.get(guild.categories, name=category_name)
            if not category:
                category = await guild.create_category(
                    category_name,
                    reason=f"Auto-setup for {server_type.value} server"
                )
                print(f"   ✅ Created category: {category_name}")

            # Create channels in category
            for channel_config in category_data["channels"]:
                existing_channel = discord.utils.get(
                    guild.channels,
                    name=channel_config["name"]
                )

                if not existing_channel:
                    if channel_config["type"] == "text":
                        await guild.create_text_channel(
                            channel_config["name"],
                            category=category,
                            topic=channel_config.get("topic", ""),
                            reason=f"Auto-setup for {server_type.value} server"
                        )
                    elif channel_config["type"] == "voice":
                        await guild.create_voice_channel(
                            channel_config["name"],
                            category=category,
                            reason=f"Auto-setup for {server_type.value} server"
                        )

                    print(f"      ✅ Created channel: {channel_config['name']}")

        print(f"✅ Server setup complete: {guild.name}")

    def run_all(self):
        """Run all Discord bots concurrently"""
        import asyncio

        async def run_bot(bot: commands.Bot, token: str, name: str):
            try:
                await bot.start(token)
            except Exception as e:
                print(f"❌ Error running {name} bot: {e}")

        # Get tokens from environment
        community_token = os.getenv("DISCORD_COMMUNITY_TOKEN")
        business_token = os.getenv("DISCORD_BUSINESS_TOKEN")
        hybrid_token = os.getenv("DISCORD_HYBRID_TOKEN")

        tasks = []

        if community_token and DiscordServerType.COMMUNITY.value in self.bots:
            tasks.append(
                run_bot(
                    self.bots[DiscordServerType.COMMUNITY.value],
                    community_token,
                    "Community"
                )
            )

        if business_token and DiscordServerType.BUSINESS.value in self.bots:
            tasks.append(
                run_bot(
                    self.bots[DiscordServerType.BUSINESS.value],
                    business_token,
                    "Business"
                )
            )

        if hybrid_token and DiscordServerType.HYBRID.value in self.bots:
            tasks.append(
                run_bot(
                    self.bots[DiscordServerType.HYBRID.value],
                    hybrid_token,
                    "Hybrid"
                )
            )

        if tasks:
            asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        else:
            print("⚠️  No Discord tokens found. Set DISCORD_COMMUNITY_TOKEN, DISCORD_BUSINESS_TOKEN, or DISCORD_HYBRID_TOKEN")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    manager = MultiDiscordManager()

    # Create community bot
    community_bot = manager.create_bot(
        server_type=DiscordServerType.COMMUNITY,
        token=os.getenv("DISCORD_COMMUNITY_TOKEN", "")
    )

    # Create business bot
    business_bot = manager.create_bot(
        server_type=DiscordServerType.BUSINESS,
        token=os.getenv("DISCORD_BUSINESS_TOKEN", "")
    )

    # Create hybrid bot
    hybrid_bot = manager.create_bot(
        server_type=DiscordServerType.HYBRID,
        token=os.getenv("DISCORD_HYBRID_TOKEN", "")
    )

    # Run all bots concurrently
    manager.run_all()

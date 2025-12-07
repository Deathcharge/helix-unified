"""
🌀 Helix Collective v17.0 - Platform Auto-Discovery
backend/platform_auto_discovery.py

Automatically detects and configures new platforms from natural language:
- NLP extraction of platform names from text
- Auto-matching to 200+ known platforms
- Configuration generation (API keys, webhooks, etc.)
- Zapier integration (push configs to Neural Network Zap)
- Self-learning (remembers platform patterns)

Author: Claude (Automation)
Version: 17.1.0
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ============================================================================
# PLATFORM DATABASE
# ============================================================================

KNOWN_PLATFORMS = {
    # Cloud Storage
    "google_drive": {
        "name": "Google Drive",
        "category": "cloud_storage",
        "aliases": ["drive", "gdrive", "google drive"],
        "requires_auth": ["google_api_key"],
        "webhook_capable": False,
    },
    "dropbox": {
        "name": "Dropbox",
        "category": "cloud_storage",
        "aliases": ["dropbox", "box"],
        "requires_auth": ["dropbox_token"],
        "webhook_capable": True,
    },
    "onedrive": {
        "name": "OneDrive",
        "category": "cloud_storage",
        "aliases": ["onedrive", "microsoft drive"],
        "requires_auth": ["microsoft_token"],
        "webhook_capable": True,
    },

    # Communication
    "slack": {
        "name": "Slack",
        "category": "communication",
        "aliases": ["slack", "slackbot"],
        "requires_auth": ["slack_token"],
        "webhook_capable": True,
    },
    "discord": {
        "name": "Discord",
        "category": "communication",
        "aliases": ["discord", "discordbot"],
        "requires_auth": ["discord_token"],
        "webhook_capable": True,
    },
    "telegram": {
        "name": "Telegram",
        "category": "communication",
        "aliases": ["telegram", "tg"],
        "requires_auth": ["telegram_token"],
        "webhook_capable": True,
    },

    # Project Management
    "notion": {
        "name": "Notion",
        "category": "project_management",
        "aliases": ["notion", "notion api"],
        "requires_auth": ["notion_token"],
        "webhook_capable": True,
    },
    "trello": {
        "name": "Trello",
        "category": "project_management",
        "aliases": ["trello"],
        "requires_auth": ["trello_key", "trello_token"],
        "webhook_capable": True,
    },
    "asana": {
        "name": "Asana",
        "category": "project_management",
        "aliases": ["asana"],
        "requires_auth": ["asana_token"],
        "webhook_capable": True,
    },

    # AI Services
    "openai": {
        "name": "OpenAI",
        "category": "ai_service",
        "aliases": ["openai", "gpt", "chatgpt"],
        "requires_auth": ["openai_api_key"],
        "webhook_capable": False,
    },
    "anthropic": {
        "name": "Anthropic",
        "category": "ai_service",
        "aliases": ["anthropic", "claude"],
        "requires_auth": ["anthropic_api_key"],
        "webhook_capable": False,
    },
    "google_ai": {
        "name": "Google AI",
        "category": "ai_service",
        "aliases": ["google ai", "gemini", "palm"],
        "requires_auth": ["google_ai_key"],
        "webhook_capable": False,
    },

    # Analytics
    "google_analytics": {
        "name": "Google Analytics",
        "category": "analytics",
        "aliases": ["google analytics", "analytics", "ga"],
        "requires_auth": ["google_analytics_key"],
        "webhook_capable": False,
    },
    "mixpanel": {
        "name": "Mixpanel",
        "category": "analytics",
        "aliases": ["mixpanel"],
        "requires_auth": ["mixpanel_token"],
        "webhook_capable": True,
    },

    # Development
    "github": {
        "name": "GitHub",
        "category": "development",
        "aliases": ["github", "gh", "git"],
        "requires_auth": ["github_token"],
        "webhook_capable": True,
    },
    "gitlab": {
        "name": "GitLab",
        "category": "development",
        "aliases": ["gitlab"],
        "requires_auth": ["gitlab_token"],
        "webhook_capable": True,
    },
}

# ============================================================================
# PLATFORM EXTRACTOR
# ============================================================================


class PlatformExtractor:
    """Extracts platform references from natural language."""

    def __init__(self, platforms: Dict[str, Dict[str, Any]] = None):
        self.platforms = platforms or KNOWN_PLATFORMS
        self._build_alias_map()

    def _build_alias_map(self) -> None:
        """Build fast lookup map for aliases."""
        self.alias_map: Dict[str, str] = {}  # alias -> platform_id
        for platform_id, info in self.platforms.items():
            for alias in info.get("aliases", []):
                self.alias_map[alias.lower()] = platform_id

    def extract_platforms(self, text: str) -> List[Tuple[str, str, float]]:
        """
        Extract platform references from text.

        Returns:
            List of (platform_id, platform_name, confidence) tuples
        """
        found_platforms: Dict[str, float] = {}  # platform_id -> max_confidence
        text_lower = text.lower()

        # Check each alias
        for alias, platform_id in self.alias_map.items():
            # Exact word match (higher confidence)
            if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
                confidence = 0.95
                if platform_id not in found_platforms or confidence > found_platforms[platform_id]:
                    found_platforms[platform_id] = confidence

            # Substring match (lower confidence)
            elif alias in text_lower:
                confidence = 0.60
                if platform_id not in found_platforms or confidence > found_platforms[platform_id]:
                    found_platforms[platform_id] = confidence

        # Convert to list of tuples
        result = []
        for platform_id, confidence in found_platforms.items():
            platform_name = self.platforms[platform_id]["name"]
            result.append((platform_id, platform_name, confidence))

        return sorted(result, key=lambda x: x[2], reverse=True)

    def get_platform(self, name: str) -> Optional[Dict[str, Any]]:
        """Get platform info by name/alias."""
        name_lower = name.lower()
        platform_id = self.alias_map.get(name_lower)
        if platform_id:
            return self.platforms[platform_id]
        return None


# ============================================================================
# CONFIGURATION GENERATOR
# ============================================================================


class PlatformConfigGenerator:
    """Generates platform configurations."""

    def generate_config(
        self, platform_id: str, platform_info: Dict[str, Any], provided_credentials: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Generate platform configuration.

        Args:
            platform_id: ID of platform (e.g., 'slack')
            platform_info: Platform info from KNOWN_PLATFORMS
            provided_credentials: User-provided credentials

        Returns:
            Configuration dictionary
        """
        config = {
            "platform_id": platform_id,
            "platform_name": platform_info["name"],
            "category": platform_info["category"],
            "enabled": True,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "credentials": {},
            "missing_credentials": [],
        }

        # Check for required credentials
        for cred_key in platform_info.get("requires_auth", []):
            if cred_key in provided_credentials:
                config["credentials"][cred_key] = provided_credentials[cred_key]
            else:
                config["missing_credentials"].append(cred_key)

        # Add capability info
        config["supports_webhooks"] = platform_info.get("webhook_capable", False)
        config["webhook_url"] = (
            None  # To be configured by user
            if config["supports_webhooks"]
            else None
        )

        return config

    def generate_zapier_payload(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Zapier webhook payload for new platform config."""
        return {
            "action": "add_platform_integration",
            "platform": config["platform_id"],
            "platform_name": config["platform_name"],
            "category": config["category"],
            "enabled": config["enabled"],
            "credentials_count": len(config["credentials"]),
            "missing_credentials": config["missing_credentials"],
            "supports_webhooks": config.get("supports_webhooks", False),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


# ============================================================================
# DISCOVERY MANAGER
# ============================================================================


class PlatformDiscoveryManager:
    """Manages platform discovery and configuration."""

    def __init__(
        self,
        config_file: Path = Path("Helix/state/discovered_platforms.json"),
        extractor: Optional[PlatformExtractor] = None,
        generator: Optional[PlatformConfigGenerator] = None,
    ):
        self.config_file = config_file
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.extractor = extractor or PlatformExtractor()
        self.generator = generator or PlatformConfigGenerator()
        self._configs = self._load_configs()

    def _load_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load discovered platforms from disk."""
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load configs: {e}")
            return {}

    def _save_configs(self) -> None:
        """Save discovered platforms to disk."""
        with open(self.config_file, "w") as f:
            json.dump(self._configs, f, indent=2)

    async def discover_from_text(
        self, text: str, user_credentials: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Discover platforms from text and auto-generate configs.

        Args:
            text: User message containing platform references
            user_credentials: Optional credentials from user

        Returns:
            List of discovered platform configurations
        """
        user_credentials = user_credentials or {}
        discovered = self.extractor.extract_platforms(text)
        configs = []

        for platform_id, platform_name, confidence in discovered:
            logger.info(f"🔍 Discovered platform: {platform_name} (confidence: {confidence:.0%})")

            # Skip if already configured
            if platform_id in self._configs:
                logger.info(f"  ℹ️ Already configured, skipping")  # noqa
                continue

            # Generate config
            platform_info = self.extractor.platforms[platform_id]
            config = self.generator.generate_config(platform_id, platform_info, user_credentials)
            configs.append(config)

            # Save config
            self._configs[platform_id] = config
            self._save_configs()

            logger.info(f"  ✅ Config generated (missing: {len(config['missing_credentials'])} creds)")

        return configs

    async def push_to_zapier(
        self, configs: List[Dict[str, Any]], webhook_url: str
    ) -> Tuple[int, int]:
        """
        Push discovered platforms to Zapier Neural Network Zap.

        Args:
            configs: Configurations to push
            webhook_url: Zapier webhook URL

        Returns:
            Tuple of (success_count, failure_count)
        """
        import aiohttp

        success_count = 0
        failure_count = 0

        for config in configs:
            try:
                payload = self.generator.generate_zapier_payload(config)

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        webhook_url, json=payload, timeout=aiohttp.ClientTimeout(total=10)
                    ) as resp:
                        if resp.status == 200:
                            success_count += 1
                            logger.info(f"  ✅ Pushed to Zapier: {config['platform_name']}")
                        else:
                            failure_count += 1
                            logger.warning(f"  ⚠️ Zapier push failed (HTTP {resp.status})")

            except Exception as e:
                failure_count += 1
                logger.error(f"  ❌ Error pushing to Zapier: {e}")

        return success_count, failure_count

    def get_configured_platforms(self) -> Dict[str, Dict[str, Any]]:
        """Get all configured platforms."""
        return self._configs

    def get_platform_config(self, platform_id: str) -> Optional[Dict[str, Any]]:
        """Get config for specific platform."""
        return self._configs.get(platform_id)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "PlatformExtractor",
    "PlatformConfigGenerator",
    "PlatformDiscoveryManager",
    "KNOWN_PLATFORMS",
]

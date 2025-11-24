# 🔐 Helix Authentication Manager - Secure Platform Integration Auth
# Manages encrypted storage of API keys for 200+ platform integrations
# Author: Andrew John Ward + Claude AI

import os
from typing import Dict, Optional
import json
from pathlib import Path
from datetime import datetime
import logging

# Try to import cryptography, fallback to base64 if not available
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    import base64
    CRYPTO_AVAILABLE = False
    logging.error("CRITICAL: cryptography not available. HelixAuthManager is disabled.")

class HelixAuthManager:
    """Secure authentication management for all platform integrations"""

    def __init__(self, secrets_path: str = "secrets/"):
        self.secrets_path = Path(secrets_path)
        self.secrets_path.mkdir(exist_ok=True, parents=True)

        if CRYPTO_AVAILABLE:
            self.cipher_suite = Fernet(self._get_or_create_key())
        else:
            self.cipher_suite = None

        self.auth_cache = {}

    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key for secrets"""
        key_file = self.secrets_path / "master.key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            if CRYPTO_AVAILABLE:
                key = Fernet.generate_key()
            else:
                raise RuntimeError("CRITICAL: cryptography not available. Cannot generate secure key.")
            key_file.write_bytes(key)
            logging.info("Created new encryption key")
            return key

    def store_api_key(self, platform: str, api_key: str, additional_data: Dict = None):
        """Securely store API key for platform"""
        auth_data = {
            "api_key": api_key,
            "platform": platform,
            "created_at": datetime.now().isoformat(),
            **(additional_data or {})
        }

        if CRYPTO_AVAILABLE and self.cipher_suite:
            encrypted_data = self.cipher_suite.encrypt(json.dumps(auth_data).encode())
        else:
            raise RuntimeError("CRITICAL: cryptography not available. Cannot securely store data.")

        auth_file = self.secrets_path / f"{platform}_auth.enc"
        auth_file.write_bytes(encrypted_data)

        # Cache for runtime use
        self.auth_cache[platform] = auth_data
        logging.info(f"✅ Stored authentication for {platform}")

    def get_api_key(self, platform: str) -> Optional[str]:
        """Retrieve API key for platform"""
        if platform in self.auth_cache:
            return self.auth_cache[platform].get("api_key")

        auth_file = self.secrets_path / f"{platform}_auth.enc"
        if not auth_file.exists():
            return None

        try:
            encrypted_data = auth_file.read_bytes()

            if CRYPTO_AVAILABLE and self.cipher_suite:
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            else:
                raise RuntimeError("CRITICAL: cryptography not available. Cannot securely retrieve data.")

            auth_data = json.loads(decrypted_data.decode())

            self.auth_cache[platform] = auth_data
            return auth_data.get("api_key")
        except Exception as e:
            logging.error(f"Failed to decrypt auth for {platform}: {e}")
            return None

    def setup_all_integrations(self):
        """Setup authentication for all major platforms from environment variables"""
        platforms = {
            "discord": os.getenv("DISCORD_BOT_TOKEN"),
            "slack": os.getenv("SLACK_BOT_TOKEN"),
            "github": os.getenv("GITHUB_TOKEN"),
            "google": os.getenv("GOOGLE_API_KEY"),
            "notion": os.getenv("NOTION_API_KEY"),
            "trello": os.getenv("TRELLO_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "railway": os.getenv("RAILWAY_TOKEN"),
            "dropbox": os.getenv("DROPBOX_ACCESS_TOKEN"),
            "calendly": os.getenv("CALENDLY_API_KEY")
        }

        configured_count = 0
        for platform, token in platforms.items():
            if token and token != "your_token_here":
                self.store_api_key(platform, token)
                logging.info(f"✅ {platform} authentication configured")
                configured_count += 1
            else:
                logging.warning(f"⚠️  {platform} authentication missing")

        logging.info(f"🔐 Configured {configured_count}/{len(platforms)} platform authentications")
        return configured_count

    def get_all_configured_platforms(self) -> list:
        """Get list of all configured platforms"""
        return list(self.auth_cache.keys())

    def remove_api_key(self, platform: str):
        """Remove API key for platform"""
        auth_file = self.secrets_path / f"{platform}_auth.enc"
        if auth_file.exists():
            auth_file.unlink()
        if platform in self.auth_cache:
            del self.auth_cache[platform]
        logging.info(f"🗑️ Removed authentication for {platform}")

# Usage Example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    auth_manager = HelixAuthManager()
    configured = auth_manager.setup_all_integrations()

    print(f"\n🔐 Authentication Manager Status:")
    print(f"Configured platforms: {configured}")
    print(f"Platforms: {', '.join(auth_manager.get_all_configured_platforms())}")
